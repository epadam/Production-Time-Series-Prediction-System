"""KFP runner"""

import os
from absl import logging
from typing import Optional, Dict, List, Text
import kfp
from kfp import gcp
from tfx.orchestration import data_types
from tfx.orchestration.kubeflow.v2 import kubeflow_v2_dag_runner
from tfx.proto import trainer_pb2
from tfx.utils import telemetry_utils
from ml_metadata.proto import metadata_store_pb2
from ml_metadata import metadata_store


import config
from pipeline import create_pipeline


# TFX pipeline produces many output files and metadata. All output data will be
# stored under this OUTPUT_DIR.
# NOTE: It is recommended to have a separated OUTPUT_DIR which is *outside* of
#       the source code structure. Please change OUTPUT_DIR to other location
#       where we can store outputs of the pipeline.
_OUTPUT_DIR = os.path.join('gs://', configs.GCS_BUCKET_NAME)

# TFX produces two types of outputs, files and metadata.
# - Files will be created under PIPELINE_ROOT directory.
# - Metadata will be written to metadata service backend.
_PIPELINE_ROOT = os.path.join(_OUTPUT_DIR, 'tfx_pipeline_output',
                              configs.PIPELINE_NAME)
pipeline_root = f'{config.ARTIFACT_STORE_URI}/{config.PIPELINE_NAME}/{kfp.dsl.RUN_ID_PLACEHOLDER}'



# The last component of the pipeline, "Pusher" will produce serving model under
# SERVING_MODEL_DIR.
_SERVING_MODEL_DIR = os.path.join(_PIPELINE_ROOT, 'serving_model')

_DATA_PATH = 'gs://{}/tfx-template/data/taxi/'.format(configs.GCS_BUCKET_NAME)
# how to version the training data

connection_config = metadata_store_pb2.ConnectionConfig()

'''
connection_config.mysql.host = '...'
connection_config.mysql.port = '...'
connection_config.mysql.database = '...'
connection_config.mysql.user = '...'
connection_config.mysql.password = '...'
store = metadata_store.MetadataStore(connection_config)
'''


def run():
  metadata_config = kubeflow_dag_runner.get_default_kubeflow_metadata_config()
  runner_config = kubeflow_v2_dag_runner.KubeflowV2DagRunnerConfig(
      default_image=configs.PIPELINE_IMAGE, kubeflow_metadata_config=metadata_config)
  
  dsl_pipeline = create_pipeline(
      pipeline_name=configs.PIPELINE_NAME,
      pipeline_root=_PIPELINE_ROOT,
      data_path=_DATA_PATH,
      preprocessing_fn=configs.PREPROCESSING_FN,
      run_fn=configs.RUN_FN,
      train_args=trainer_pb2.TrainArgs(num_steps=configs.TRAIN_NUM_STEPS),
      eval_args=trainer_pb2.EvalArgs(num_steps=configs.EVAL_NUM_STEPS),
      eval_accuracy_threshold=configs.EVAL_ACCURACY_THRESHOLD,
      serving_model_dir=_SERVING_MODEL_DIR,
      
  )
  runner = kubeflow_v2_dag_runner.KubeflowV2DagRunner(config=runner_config)
  runner.run(pipeline=dsl_pipeline)
  

  
  
  
  
  
'''  

def run():
  """Define a pipeline to be executed using Kubeflow V2 runner."""

  runner_config = kubeflow_v2_dag_runner.KubeflowV2DagRunnerConfig(
      default_image=configs.PIPELINE_IMAGE)

  dsl_pipeline = create_pipeline(
      pipeline_name=configs.PIPELINE_NAME,
      pipeline_root=_PIPELINE_ROOT,
      data_path=_DATA_PATH,
      # TODO(step 7): (Optional) Uncomment here to use BigQueryExampleGen.
      # query=configs.BIG_QUERY_QUERY,
      preprocessing_fn=configs.PREPROCESSING_FN,
      run_fn=configs.RUN_FN,
      train_args=trainer_pb2.TrainArgs(num_steps=configs.TRAIN_NUM_STEPS),
      eval_args=trainer_pb2.EvalArgs(num_steps=configs.EVAL_NUM_STEPS),
      eval_accuracy_threshold=configs.EVAL_ACCURACY_THRESHOLD,
      serving_model_dir=_SERVING_MODEL_DIR,
    
      # Uncomment below to use Dataflow.
      # beam_pipeline_args=configs.DATAFLOW_BEAM_PIPELINE_ARGS,
    
      ai_platform_training_args=configs.GCP_AI_PLATFORM_TRAINING_ARGS,
    
      # Uncomment below to use Cloud AI Platform.
      # ai_platform_serving_args=configs.GCP_AI_PLATFORM_SERVING_ARGS,
  )

  runner = kubeflow_v2_dag_runner.KubeflowV2DagRunner(config=runner_config)

  runner.run(pipeline=dsl_pipeline)

  

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
'''    
    
    
if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    run()
