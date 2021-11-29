import os
import sys
import absl
from typing import Dict, List, Text, Optional
from kfp import gcp
import tfx
from tfx.proto import example_gen_pb2, infra_validator_pb2
from tfx.orchestration import pipeline, data_types
from tfx.dsl.components.base import executor_spec
from tfx.components.trainer import executor as trainer_executor
from tfx.extensions.google_cloud_ai_platform.trainer import executor as ai_platform_trainer_executor
from tfx.extensions.google_cloud_big_query.example_gen.component import BigQueryExampleGen
from ml_metadata.proto import metadata_store_pb2
import tensorflow_model_analysis as tfma

from tfx.components import CsvExampleGen
from tfx.components import Evaluator
from tfx.components import ExampleValidator
from tfx.components import Pusher
from tfx.components import SchemaGen
from tfx.components import StatisticsGen
from tfx.components import Trainer
from tfx.components import Transform

from tfx.dsl.components.common import resolver
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import metadata
from tfx.orchestration import pipeline
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
from tfx.proto import pusher_pb2
from tfx.proto import trainer_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model
from tfx.types.standard_artifacts import ModelBlessing

def _create_pipeline(
    pipeline_name: str,
    pipeline_root: str,
    data_root: str,
    trainer_module_file: str,
    evaluator_module_file: str,
    ai_platform_training_args: Optional[Dict[str, str]],
    ai_platform_serving_args: Optional[Dict[str, str]],
    beam_pipeline_args: List[str],
) -> tfx.dsl.Pipeline:
  """Implements the Penguin pipeline with TFX."""
  # Brings data into the pipeline or otherwise joins/converts training data.
  example_gen = tfx.components.CsvExampleGen(
      input_base=os.path.join(data_root, 'labelled'))

  # Computes statistics over data for visualization and example validation.
  statistics_gen = tfx.components.StatisticsGen(
      examples=example_gen.outputs['examples'])

  # Generates schema based on statistics files.
  schema_gen = tfx.components.SchemaGen(
      statistics=statistics_gen.outputs['statistics'], infer_feature_shape=True)

  # Performs anomaly detection based on statistics and data schema.
  example_validator = tfx.components.ExampleValidator(
      statistics=statistics_gen.outputs['statistics'],
      schema=schema_gen.outputs['schema'])
  
  # TODO(humichael): Handle applying transformation component in Milestone 3.

  # Uses user-provided Python function that trains a model.
  # Num_steps is not provided during evaluation because the scikit-learn model
  # loads and evaluates the entire test set at once.
  trainer = tfx.extensions.google_cloud_ai_platform.Trainer(
      module_file=trainer_module_file,
      examples=example_gen.outputs['examples'],
      schema=schema_gen.outputs['schema'],
      train_args=tfx.proto.TrainArgs(num_steps=2000),
      eval_args=tfx.proto.EvalArgs(),
      custom_config={
          tfx.extensions.google_cloud_ai_platform.TRAINING_ARGS_KEY:
          ai_platform_training_args,
      })

  # Get the latest blessed model for model validation.
  model_resolver = tfx.dsl.Resolver(
      strategy_class=tfx.dsl.experimental.LatestBlessedModelStrategy,
      model=tfx.dsl.Channel(type=tfx.types.standard_artifacts.Model),
      model_blessing=tfx.dsl.Channel(
          type=tfx.types.standard_artifacts.ModelBlessing)).with_id(
              'latest_blessed_model_resolver')
  
  # Uses TFMA to compute evaluation statistics over features of a model and
  # perform quality validation of a candidate model (compared to a baseline).
  eval_config = tfma.EvalConfig(
      model_specs=[tfma.ModelSpec(label_key='species')],
      slicing_specs=[tfma.SlicingSpec()],
      metrics_specs=[
          tfma.MetricsSpec(metrics=[
              tfma.MetricConfig(
                  class_name='Accuracy',
                  threshold=tfma.MetricThreshold(
                      value_threshold=tfma.GenericValueThreshold(
                          lower_bound={'value': 0.6}),
                      change_threshold=tfma.GenericChangeThreshold(
                          direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                          absolute={'value': -1e-10})))
          ])
      ])

  evaluator = tfx.components.Evaluator(
      module_file=evaluator_module_file,
      examples=example_gen.outputs['examples'],
      model=trainer.outputs['model'],
      baseline_model=model_resolver.outputs['model'],
      eval_config=eval_config)

  pusher = tfx.extensions.google_cloud_ai_platform.Pusher(
      model=trainer.outputs['model'],
      model_blessing=evaluator.outputs['blessing'],
      custom_config={
          tfx.extensions.google_cloud_ai_platform.experimental
          .PUSHER_SERVING_ARGS_KEY: ai_platform_serving_args,
      })
  
  return tfx.dsl.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      components=[
          example_gen,
          statistics_gen,
          schema_gen,
          example_validator,
          trainer,
          model_resolver,
          evaluator,
          pusher,
      ],
      enable_cache=True,
      beam_pipeline_args=beam_pipeline_args,
  )
