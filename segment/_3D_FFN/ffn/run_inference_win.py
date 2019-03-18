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
"""Runs FFN inference within a dense bounding box.

Inference is performed within a single process.
"""
import os
import sys
import time

from os import path, pardir
main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
sys.path.append(main_dir)

# for tensorflow
import gast
import astor
import termcolor
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
#############

from google.protobuf import text_format
from absl import app
from absl import flags
from tensorflow import gfile

from ffn.utils import bounding_box_pb2
from ffn.inference import inference
from ffn.inference import inference_flags
from ffn.inference import inference_pb2


FLAGS = flags.FLAGS

flags.DEFINE_string('image_size_x', None, 'image size x')
flags.DEFINE_string('image_size_y', None, 'image size y')
flags.DEFINE_string('image_size_z', None, 'image size z')
flags.DEFINE_string('parameter_file', None, 'JSON parameter file')

def main(unused_argv):

  request = inference_pb2.InferenceRequest()
  with open(FLAGS.parameter_file, mode='r') as f:
    text_list = f.readlines()
  text = ' '.join(text_list)
  text_format.Parse(text, request)

  if not gfile.Exists(request.segmentation_output_dir):
    gfile.MakeDirs(request.segmentation_output_dir)
  runner = inference.Runner()
  runner.start(request)
  #  runner.run((bbox.start.z, bbox.start.y, bbox.start.x),
  #             (bbox.size.z, bbox.size.y, bbox.size.x))
  runner.run((0, 0, 0),
             (int(FLAGS.image_size_z), int(FLAGS.image_size_y), int(FLAGS.image_size_x)))



  counter_path = os.path.join(request.segmentation_output_dir, 'counters.txt')
  if not gfile.Exists(counter_path):
    runner.counters.dump(counter_path)


if __name__ == '__main__':
  app.run(main)
