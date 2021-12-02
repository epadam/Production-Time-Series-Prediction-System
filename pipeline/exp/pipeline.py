import os
import sys
import absl
from typing import Dict, List, Text, Optional
from kfp import gcp
import tfx
from tfx.proto import example_gen_pb2, infra_validator_pb2
from tfx.proto import pusher_pb2
from tfx.proto import trainer_pb2

from tfx.orchestration import pipeline, data_types
from tfx.orchestration import metadata
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

from tfx.extensions.google_cloud_ai_platform.trainer import executor as ai_platform_trainer_executor
from tfx.extensions.google_cloud_big_query.example_gen.component import BigQueryExampleGen

from tfx.components.trainer import executor as trainer_executor


from tfx.dsl.components.base import executor_spec
from tfx.dsl.components.common import resolver
from tfx.dsl.experimental import latest_blessed_model_resolver


from tfx.types import Channel
from tfx.types.standard_artifacts import Model
from tfx.types.standard_artifacts import ModelBlessing

from ml_metadata.proto import metadata_store_pb2
import tensorflow_model_analysis as tfma


def create_pipeline(
    pipeline_name: str,
    pipeline_root: str,
    data_path: Text,
    preprocessing_fn: Text,
    run_fn: Text,
    train_args: tfx.proto.TrainArgs,
    eval_args: tfx.proto.EvalArgs,
    #eval_accuracy_threshold: float,
    serving_model_dir: Text,
    metadata_connection_config: metadata_store_pb2.ConnectionConfig,
    beam_pipeline_args: Optional[List[Text]] = None,
    #trainer_module_file: str,
    #evaluator_module_file: str,
    #ai_platform_training_args: Optional[Dict[str, str]],
    #ai_platform_serving_args: Optional[Dict[str, str]],
    #beam_pipeline_args: List[str],
) -> tfx.dsl.Pipeline:
  """Implements the Penguin pipeline with TFX."""

  # Brings data into the pipeline or otherwise joins/converts training data.
  example_gen = tfx.components.CsvExampleGen(input_base=configs.DATA_PATH)

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
  
  transform = tfx.components.Transform(
      examples=example_gen.outputs['examples'],
      schema=schema_gen.outputs['schema'],
      preprocessing_fn=configs.PREPROCESSING_FN)

  trainer_args = {
      'run_fn': run_fn,
      'transformed_examples': transform.outputs['transformed_examples'],
      'schema': schema_gen.outputs['schema'],
      'transform_graph': transform.outputs['transform_graph'],
      'train_args': train_args,
      'eval_args': eval_args,
  }
    
  trainer = tfx.components.Trainer(**trainer_args)

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
      model_specs=[tfma.ModelSpec(signature_name='serving_default', label_key='cnt')],
      slicing_specs=[tfma.SlicingSpec(),
                     tfma.SlicingSpec(feature_keys=['weekday'])],
      metrics_specs=[
          tfma.MetricsSpec(metrics=[
              tfma.MetricConfig(
                  class_name='MeanSquaredError',
                  threshold=tfma.MetricThreshold(
                      value_threshold=tfma.GenericValueThreshold(
                          lower_bound={'value': 1}),
                      change_threshold=tfma.GenericChangeThreshold(
                          direction=tfma.MetricDirection.LOWER_IS_BETTER,
                          absolute={'value': -1e-1})))
          ])
      ])

  evaluator = tfx.components.Evaluator(
      #module_file=evaluator_module_file,
      examples=example_gen.outputs['examples'],
      model=trainer.outputs['model'],
      baseline_model=model_resolver.outputs['model'],
      eval_config=eval_config)
  
  pusher = tfx.components.Pusher(
      model=trainer.outputs['model'],
      model_blessing=evaluator.outputs['blessing'],
      push_destination=tfx.proto.PushDestination(
        filesystem=tfx.proto.PushDestination.Filesystem(
            base_directory=configs.SERVING_MODEL_DIR)))  

  
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
      metadata_connection_config=metadata_connection_config,
      beam_pipeline_args=beam_pipeline_args,
  )
