# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Simplest FFN model, as described in https://arxiv.org/abs/1611.00421."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


## Modified by HU

import pkg_resources
ver = pkg_resources.get_distribution('tensorflow').version
if ( '2.' in ver ):
  import tensorflow.compat.v1 as tf
  tf.disable_v2_behavior()
elif ('1.15' in ver) :
  import tensorflow.compat.v1 as tf
  tf.disable_v2_behavior()
  import tensorflow.contrib as tf_contrib
else:
  import tensorflow as tf
  import tensorflow.contrib as tf_contrib
##
#import os
#import logging
#import warnings
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#warnings.simplefilter(action='ignore', category=FutureWarning)
#warnings.simplefilter(action='ignore', category=Warning)
#tf.get_logger().setLevel('INFO')
#tf.autograph.set_verbosity(0)
#tf.get_logger().setLevel(logging.ERROR)
##
## Modified by HU


import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
tf.logging.set_verbosity(tf.logging.INFO)


import sys
from os import path
main_dir = path.abspath(path.dirname(sys.argv[0]))
current_dir = path.join(main_dir, "ffn","training")
sys.path.append(current_dir)
import model



# Note: this model was originally trained with conv3d layers initialized with
# TruncatedNormalInitializedVariable with stddev = 0.01.
def _predict_object_mask_TF1(net, depth=9):
 
  conv = tf_contrib.layers.conv3d
  with tf_contrib.framework.arg_scope([conv], num_outputs=32,
                                      kernel_size=(3, 3, 3),
                                      padding='SAME'):
    net = conv(net, scope='conv0_a')
    net = conv(net, scope='conv0_b', activation_fn=None)

    for i in range(1, depth):
      with tf.name_scope('residual%d' % i):
        in_net = net
        net = tf.nn.relu(net)
        net = conv(net, scope='conv%d_a' % i)
        net = conv(net, scope='conv%d_b' % i, activation_fn=None)
        net += in_net

  net = tf.nn.relu(net)
  logits = conv(net, 1, (1, 1, 1), activation_fn=None, scope='conv_lom')

  return logits


## Modified by HU

def _predict_object_mask_TF2(net, depth=9):

  conv = tf.layers.conv3d
  net   = conv(net, filters=32, kernel_size=(3, 3, 3), padding='same', activation=tf.nn.relu, name='conv0_a')
  net   = conv(net, filters=32, kernel_size=(3, 3, 3), padding='same', activation=None, name='conv0_b')

  for i in range(1, depth):
    with tf.name_scope('residual%d' % i):
      in_net = net
      net   = tf.nn.relu(net)
      net   = conv(net, filters=32, kernel_size=(3, 3, 3), padding='same', activation=tf.nn.relu, name='conv%d_a' % i)
      net   = conv(net, filters=32, kernel_size=(3, 3, 3), padding='same', activation=None, name='conv%d_b' % i)
      net  += in_net

  net    = tf.nn.relu(net)
  logits = conv(net, filters=1, kernel_size=(1, 1, 1), activation=None, name='conv_lom')

  return logits

## End: modified by HU



class ConvStack3DFFNModel(model.FFNModel):
  dim = 3

  def __init__(self, fov_size=None, deltas=None, batch_size=None, depth=9):
    super(ConvStack3DFFNModel, self).__init__(deltas, batch_size)
    self.set_uniform_io_size(fov_size)
    self.depth = depth

  def define_tf_graph(self):
    self.show_center_slice(self.input_seed)

    if self.input_patches is None:
      self.input_patches = tf.placeholder(
          tf.float32, [1] + list(self.input_image_size[::-1]) +[1],
          name='patches')

    net = tf.concat([self.input_patches, self.input_seed], 4)

    with tf.variable_scope('seed_update', reuse=False):

      if ( '2.' in ver ):
          logit_update = _predict_object_mask_TF2(net, self.depth)
      else:
          logit_update = _predict_object_mask_TF1(net, self.depth)


    logit_seed = self.update_seed(self.input_seed, logit_update)

    # Make predictions available, both as probabilities and logits.
    self.logits = logit_seed
    self.logistic = tf.sigmoid(logit_seed)

    if self.labels is not None:
      self.set_up_sigmoid_pixelwise_loss(logit_seed)
      self.set_up_optimizer()
      self.show_center_slice(logit_seed)
      self.show_center_slice(self.labels, sigmoid=False)
      self.add_summaries()

    # self.saver = tf.train.Saver(keep_checkpoint_every_n_hours=1)
    self.saver = tf.train.Saver(keep_checkpoint_every_n_hours=1, save_relative_paths=True) # 221222HU
