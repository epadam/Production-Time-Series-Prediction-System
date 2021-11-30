from typing import List

import absl
import tensorflow as tf
import tensorflow_transform as tft

from tfx_bsl.tfxio import dataset_options

import features

_DENSE_FLOAT_FEATURE_KEYS = features.DENSE_FLOAT_FEATURE_KEYS
_VOCAB_FEATURE_KEYS = features.VOCAB_FEATURE_KEYS
_VOCAB_SIZE = features.VOCAB_SIZE
_OOV_SIZE = features.OOV_SIZE
_FEATURE_BUCKET_COUNT =features.FEATURE_BUCKET_COUNT
_BUCKET_FEATURE_KEYS = features.BUCKET_FEATURE_KEYS
_CATEGORICAL_FEATURE_KEYS = features.CATEGORICAL_FEATURE_KEYS
_FARE_KEY = features.FARE_KEY
_LABEL_KEY = features.LABEL_KEY


# Tf.Transform considers these features as "raw"
def _get_raw_feature_spec(schema):
  return schema_utils.schema_as_feature_spec(schema).feature_spec



def _fill_in_missing(x):
  """Replace missing values in a SparseTensor.
  Fills in missing values of `x` with '' or 0, and converts to a dense tensor.
  Args:
    x: A `SparseTensor` of rank 2.  Its dense shape should have size at most 1
      in the second dimension.
  Returns:
    A rank 1 tensor where missing values of `x` have been filled in.
  """
  if not isinstance(x, tf.sparse.SparseTensor):
    return x

  default_value = '' if x.dtype == tf.string else 0
  return tf.squeeze(
      tf.sparse.to_dense(
          tf.SparseTensor(x.indices, x.values, [x.dense_shape[0], 1]),
          default_value),
      axis=1)



def preprocessing_fn(inputs):
  """tf.transform's callback function for preprocessing inputs.
  Args:
    inputs: map from feature keys to raw not-yet-transformed features.
  Returns:
    Map from string feature key to transformed feature operations.
  """
  outputs = {}
  for key in _DENSE_FLOAT_FEATURE_KEYS:
    # If sparse make it dense, setting nan's to 0 or '', and apply zscore.
    outputs[key] = tft.scale_to_z_score(
        _fill_in_missing(inputs[key]))

  for key in _VOCAB_FEATURE_KEYS:
    # Build a vocabulary for this feature.
    outputs[key] = tft.compute_and_apply_vocabulary(
        _fill_in_missing(inputs[key]),
        top_k=_VOCAB_SIZE,
        num_oov_buckets=_OOV_SIZE)

  for key in _BUCKET_FEATURE_KEYS:
    outputs[key] = tft.bucketize(
        _fill_in_missing(inputs[key]), _FEATURE_BUCKET_COUNT)

  for key in _CATEGORICAL_FEATURE_KEYS:
    outputs[key] = _fill_in_missing(inputs[key])

  # Was this passenger a big tipper?
  '''
  taxi_fare = _fill_in_missing(inputs[_FARE_KEY])
  tips = _fill_in_missing(inputs[_LABEL_KEY])
  outputs[_transformed_name(_LABEL_KEY)] = tf.compat.v1.where(
      tf.math.is_nan(taxi_fare),
      tf.cast(tf.zeros_like(taxi_fare), tf.int64),
      # Test if the tip was > 20% of the fare.
      tf.cast(
          tf.greater(tips, tf.multiply(taxi_fare, tf.constant(0.2))), tf.int64))
  '''

  return outputs


