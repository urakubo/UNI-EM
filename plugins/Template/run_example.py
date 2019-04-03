import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--training_image_folder", type=str)
parser.add_argument("--ground_truth_folder", type=str)
parser.add_argument("--tensorflow_model_folder", type=str)
parser.add_argument("--test_image_folder", type=str)
parser.add_argument("--inferred_segmentation_folder", type=str)
parser.add_argument("--tensorflow_model_file", type=str)

a = parser.parse_args()

print('arg1: ', a.training_image_folder)
print('arg2: ', a.ground_truth_folder)
print('arg3: ', a.tensorflow_model_folder)
print('arg4: ', a.test_image_folder)
print('arg5: ', a.inferred_segmentation_folder)
print('arg6: ', a.tensorflow_model_file)


