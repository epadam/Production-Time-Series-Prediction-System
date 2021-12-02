import os
import pickle
from typing import Tuple

import absl
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from tfx.components.trainer.fn_args_utils import DataAccessor
from tfx.components.trainer.fn_args_utils import FnArgs
from tfx.dsl.io import fileio
from tfx.utils import io_utils
from tfx_bsl.tfxio import dataset_options

from tensorflow_metadata.proto.v0 import schema_pb2
import tensorflow as tf
from tensorflow import keras
import tensorflow_transform as tft

_FEATURE_KEYS = [
   'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed'
]
_LABEL_KEY = 'cnt'


def _get_serve_tf_examples_fn(model, tf_transform_output):
  """Returns a function that parses a serialized tf.Example and applies TFT."""

  model.tft_layer = tf_transform_output.transform_features_layer()

  @tf.function
  def serve_tf_examples_fn(serialized_tf_examples):
    """Returns the output to be used in the serving signature."""
    feature_spec = tf_transform_output.raw_feature_spec()
    feature_spec.pop(_LABEL_KEY)
    parsed_features = tf.io.parse_example(serialized_tf_examples, feature_spec)
    transformed_features = model.tft_layer(parsed_features)
    return model(transformed_features)

  return serve_tf_examples_fn

_FEATURE_KEYS = [
   'season_xf', 'yr_xf', 'mnth_xf', 'holiday_xf', 'weekday_xf', 'workingday_xf', 'weathersit_xf', 'temp_xf', 'atemp_xf', 'hum_xf', 'windspeed_xf'
]


_TRAIN_DATA_SIZE = 658
_TRAIN_BATCH_SIZE = 20
_EVAL_BATCH_SIZE = 20

'''
def _input_fn(
    file_pattern: str,
    data_accessor: DataAccessor,
    schema: schema_pb2.Schema,
    batch_size: int = 20,
) -> Tuple[np.ndarray, np.ndarray]:

  record_batch_iterator = data_accessor.record_batch_factory(
      file_pattern,
      dataset_options.RecordBatchesOptions(batch_size=batch_size, num_epochs=1),
      schema)

  feature_list = []
  label_list = []
  for record_batch in record_batch_iterator:
    record_dict = {}
    for column, field in zip(record_batch, record_batch.schema):
      record_dict[field.name] = column.flatten()

    label_list.append(record_dict[_LABEL_KEY])
    features = [record_dict[key] for key in _FEATURE_KEYS]
    feature_list.append(np.stack(features, axis=-1))

  return np.concatenate(feature_list), np.concatenate(label_list)
'''

def _input_fn(
    file_pattern: str,
    data_accessor: DataAccessor,
    tf_transform_output: tft.TFTransformOutput,
    batch_size: int = 20,
) -> tf.data.Dataset:
  return data_accessor.tf_dataset_factory(
      file_pattern,
      dataset_options.TensorFlowDatasetOptions(
          batch_size=batch_size,
          label_key=features.transformed_name(_LABEL_KEY)
          ),
      schema=tf_transform_output.transformed_metadata.schema).repeat()


def _build_keras_model() -> tf.keras.Model:
  """Creates a DNN Keras model for classifying penguin data.
  Returns:
    A Keras Model.
  """
  # The model below is built with Functional API, please refer to
  # https://www.tensorflow.org/guide/keras/overview for all API options.
  inputs = [keras.layers.Input(shape=(1,), name=f) for f in _FEATURE_KEYS]
  d = keras.layers.concatenate(inputs)
  for _ in range(2):
    d = keras.layers.Dense(8, activation='relu')(d)
  outputs = keras.layers.Dense(1)(d)

  model = keras.Model(inputs=inputs, outputs=outputs)
  model.compile(
      optimizer=keras.optimizers.Adam(1e-2),
      loss=tf.keras.losses.mse,
      metrics=[keras.metrics.MeanSquaredError()])

  model.summary(print_fn=logging.info)
  return model


def run_fn(fn_args: FnArgs):
  tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

  train_dataset = _input_fn(
      fn_args.train_files,
      fn_args.data_accessor,
      tf_transform_output,
      batch_size=_TRAIN_BATCH_SIZE)
  eval_dataset = _input_fn(
      fn_args.eval_files,
      fn_args.data_accessor,
      tf_transform_output,
      batch_size=_EVAL_BATCH_SIZE)

  model = _build_keras_model()

  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=fn_args.model_run_dir, update_freq='batch')
   
  model.fit(
      train_dataset,
      steps_per_epoch=fn_args.train_steps,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps,
      callbacks=[tensorboard_callback])
   
  signatures = {
      'serving_default':
          _get_serve_tf_examples_fn(model,
                                    tf_transform_output).get_concrete_function(
                                        tf.TensorSpec(
                                            shape=[None],
                                            dtype=tf.string,
                                            name='examples')),
  }
  model.save(fn_args.serving_model_dir, save_format='tf', signatures=signatures)

   
'''
def run_fun(fn_args: FnArgs):
   schema = schema_utils.schema_from_feature_spec(_FEATURE_SPEC)

   train_dataset = _input_fn(
      fn_args.train_files,
      fn_args.data_accessor,
      schema,
      batch_size=_TRAIN_BATCH_SIZE)
   eval_dataset = _input_fn(
      fn_args.eval_files,
      fn_args.data_accessor,
      schema,
      batch_size=_EVAL_BATCH_SIZE)

   model = _build_keras_model()
   model.fit(
      train_dataset,
      steps_per_epoch=fn_args.train_steps,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps)
   model.save(fn_args.serving_model_dir, save_format='tf')


def run_fn(fn_args: FnArgs):
  """Train the model based on given args.
  Args:
    fn_args: Holds args used to train the model as name/value pairs.
  """
  schema = io_utils.parse_pbtxt_file(fn_args.schema_file, schema_pb2.Schema())

  x_train, y_train = _input_fn(fn_args.train_files, fn_args.data_accessor,
                               schema)
  x_eval, y_eval = _input_fn(fn_args.eval_files, fn_args.data_accessor, schema)

  steps_per_epoch = _TRAIN_DATA_SIZE / _TRAIN_BATCH_SIZE
  
  estimator = MLPClassifier(
      hidden_layer_sizes=[8, 8, 8],
      activation='relu',
      solver='adam',
      batch_size=_TRAIN_BATCH_SIZE,
      learning_rate_init=0.0005,
      max_iter=int(fn_args.train_steps / steps_per_epoch),
      verbose=True)

  # Create a pipeline that standardizes the input data before passing it to an
  # estimator. Once the scaler is fit, it will use the same mean and stdev to
  # transform inputs at both training and serving time.
  model = Pipeline([
      ('scaler', StandardScaler()),
      ('estimator', estimator),
  ])
  model.feature_keys = _FEATURE_KEYS
  model.label_key = _LABEL_KEY
  model.fit(x_train, y_train)
  absl.logging.info(model)

  score = model.score(x_eval, y_eval)
  absl.logging.info('Accuracy: %f', score)

  # Export the model as a pickle named model.pkl. AI Platform Prediction expects
  # sklearn model artifacts to follow this naming convention.
  os.makedirs(fn_args.serving_model_dir)
  
  model_path = os.path.join(fn_args.serving_model_dir, 'model.pkl')
  with fileio.open(model_path, 'wb+') as f:
    pickle.dump(model, f)
'''
