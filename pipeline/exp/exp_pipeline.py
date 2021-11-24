import os
from typing import List

import absl

import tensorflow_model_analysis as tfma
from tfx.components import ImportExampleGen
from tfx.components import ExampleValidator
from tfx.components import SchemaGen
from tfx.components import StatisticsGen
from tfx.components import Transform
from tfx.components import Trainer
from tfx.components import Evaluator
from tfx.components import Pusher
from tfx.dsl.components.common import resolver
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import metadata
from tfx.orchestration import pipeline
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
from tfx.proto import example_gen_pb2
from tfx.proto import pusher_pb2
from tfx.proto import trainer_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model
from tfx.types.standard_artifacts import ModelBlessing

_pipeline_name = 'cifar10_native_keras'

# This example assumes that CIFAR10 train set data is stored in
# ~/cifar10/data/train, test set data is stored in ~/cifar10/data/test, and
# the utility function is in ~/cifar10. Feel free to customize as needed.
_cifar10_root = os.path.join(os.environ['HOME'], 'cifar10')
_data_root = os.path.join(_cifar10_root, 'data')
# Python module files to inject customized logic into the TFX components. The
# Transform and Trainer both require user-defined functions to run successfully.
_module_file = os.path.join(_cifar10_root, 'cifar10_utils_native_keras.py')
# Path which can be listened to by the model server. Pusher will output the
# trained model here.
_serving_model_dir_lite = os.path.join(_cifar10_root, 'serving_model_lite',
                                       _pipeline_name)

# Directory and data locations.  This example assumes all of the images,
# example code, and metadata library is relative to $HOME, but you can store
# these files anywhere on your local filesystem.
_tfx_root = os.path.join(os.environ['HOME'], 'tfx')
_pipeline_root = os.path.join(_tfx_root, 'pipelines', _pipeline_name)
# Sqlite ML-metadata db path.
_metadata_path = os.path.join(_tfx_root, 'metadata', _pipeline_name,
                              'metadata.db')
# Path to labels file for mapping model outputs.
_labels_path = os.path.join(_data_root, 'labels.txt')


# Pipeline arguments for Beam powered Components.
_beam_pipeline_args = [
    '--direct_running_mode=multi_processing',
    # 0 means auto-detect based on on the number of CPUs available
    # during execution time.
    '--direct_num_workers=0',
]

