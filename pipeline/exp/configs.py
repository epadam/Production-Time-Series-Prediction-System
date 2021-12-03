import os

PIPELINE_NAME=os.getenv('PIPELINE_NAME', 'bike_sharing')

### GCP setup

# Following code will retrieve your GCP project. You can choose which project
# to use by setting GOOGLE_CLOUD_PROJECT environment variable.
try:
  import google.auth  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error
  try:
    _, GOOGLE_CLOUD_PROJECT = google.auth.default()
  except google.auth.exceptions.DefaultCredentialsError:
    GOOGLE_CLOUD_PROJECT = ''
except ImportError:
  GOOGLE_CLOUD_PROJECT = ''
  

PROJECT_ID=os.getenv('PROJECT_ID', 'tfx-cloudml')
REGION=os.getenv('REGION', 'europe-west1')
GOOGLE_CLOUD_REGION = 'us-central1'  # ex) 'us-central1'


if not (GOOGLE_CLOUD_PROJECT and  GOOGLE_CLOUD_PROJECT_NUMBER and GOOGLE_CLOUD_REGION and GCS_BUCKET_NAME):
    from absl import logging
    logging.error('Please set all required parameters.')

GCS_BUCKET_NAME = GOOGLE_CLOUD_PROJECT + '-kubeflowpipelines-default'

BQ_DATASET_NAME=os.getenv('BQ_DATASET_NAME', 'recommendations')
RUNTIME_VERSION=os.getenv('RUNTIME_VERSION', '2.2')
PYTHON_VERSION=os.getenv('PYTHON_VERSION', '3.7')
USE_KFP_SA=os.getenv('USE_KFP_SA', 'False')
ML_IMAGE_URI=os.getenv('ML_IMAGE_URI', 'tensorflow/tfx:0.23.0')

# Following image will be used to run pipeline components run if Kubeflow
# Pipelines used.
# This image will be automatically built by CLI if we use --build-image flag.
PIPELINE_IMAGE = f'gcr.io/{GOOGLE_CLOUD_PROJECT}/{PIPELINE_NAME}'

BEAM_RUNNER=os.getenv('BEAM_RUNNER', 'DirectRunner')
MODEL_REGISTRY_URI=os.getenv('MODEL_REGISTRY_URI', 'gs://tfx-cloudml-artifacts/model_registry')


### Metadata ans artifact Storage

ARTIFACT_STORE_URI=os.getenv('ARTIFACT_STORE_URI', 'gs://tfx-cloudml-artifacts')

### User defined functions for transform and trainer

PREPROCESSING_FN = 'preprocessing.preprocessing_fn'
RUN_FN = 'model.run_fn'
# NOTE: Uncomment below to use an estimator based model.
# RUN_FN = 'models.estimator_model.model.run_fn'

trainer_module_file = os.path.join(
    _bike_root, 'util', 'bike_utils_sklearn.py')

### Training parameters

TRAIN_NUM_STEPS = 1000
EVAL_NUM_STEPS = 150

# Change this value according to your use cases.
EVAL_ACCURACY_THRESHOLD = 0.6
