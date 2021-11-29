"""KFP runner"""

import kfp
from kfp import gcp
from tfx.orchestration import data_types
from tfx.orchestration.kubeflow import kubeflow_dag_runner

from typing import Optional, Dict, List, Text

import config
import pipeline


import os
from absl import logging


from pipeline import create_pipeline
from tfx.orchestration.kubeflow import kubeflow_dag_runner
from tfx.utils import telemetry_utils

PIPELINE_NAME = 'sentiment3'
GOOGLE_CLOUD_PROJECT = 'sascha-playground-doit'
GCS_BUCKET_NAME = GOOGLE_CLOUD_PROJECT + '-kubeflowpipelines-default'
OUTPUT_DIR = os.path.join('gs://', GCS_BUCKET_NAME)
PIPELINE_ROOT = os.path.join(OUTPUT_DIR, PIPELINE_NAME)


def run():
    metadata_config = kubeflow_dag_runner.get_default_kubeflow_metadata_config()
    tfx_image = "gcr.io/sascha-playground-doit/sentiment-pipeline"
    runner_config = kubeflow_dag_runner.KubeflowDagRunnerConfig(
        kubeflow_metadata_config=metadata_config, tfx_image=tfx_image)

    kubeflow_dag_runner.KubeflowDagRunner(config=runner_config).run(
                                              create_pipeline(
                                                  pipeline_name=PIPELINE_NAME,
                                                  pipeline_root=PIPELINE_ROOT))


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    run()
    
    
pipeline_root = f'{config.ARTIFACT_STORE_URI}/{config.PIPELINE_NAME}/{kfp.dsl.RUN_ID_PLACEHOLDER}'

  # Set KubeflowDagRunner settings
  metadata_config = kubeflow_dag_runner.get_default_kubeflow_metadata_config()

  runner_config = kubeflow_dag_runner.KubeflowDagRunnerConfig(
    kubeflow_metadata_config = metadata_config,
    pipeline_operator_funcs = kubeflow_dag_runner.get_default_pipeline_operator_funcs(
      config.USE_KFP_SA == 'True'),
    tfx_image=config.ML_IMAGE_URI
  )

  # Compile the pipeline
  kubeflow_dag_runner.KubeflowDagRunner(config=runner_config).run(
    pipeline.create_pipeline(
      pipeline_name=config.PIPELINE_NAME,
      pipeline_root=pipeline_root,
      project_id=config.PROJECT_ID,
      bq_dataset_name=config.BQ_DATASET_NAME,
      min_item_frequency=min_item_frequency,
      max_group_size=max_group_size,
      dimensions=dimensions,
      num_leaves=num_leaves,
      eval_min_recall=eval_min_recall,
      eval_max_latency=eval_max_latency,
      ai_platform_training_args=ai_platform_training_args,
      beam_pipeline_args=beam_pipeline_args,
      model_regisrty_uri=config.MODEL_REGISTRY_URI)
  )
