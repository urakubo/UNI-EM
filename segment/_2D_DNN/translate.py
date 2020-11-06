from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

import tensorflow as tf
import tensorflow.contrib as contrib
import numpy as np
import argparse
import os
import json
import glob
import random
import collections
import math
import time


if tf.__version__ == '1.12.0':
    from tensorflow.python.util import deprecation
    deprecation._PRINT_DEPRECATION_WARNINGS = False

if ('1.14' in tf.__version__) | ('1.15' in tf.__version__):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


parser = argparse.ArgumentParser()
parser.add_argument("--mode", required=True, choices=["train", "test", "predict"])
parser.add_argument("--input_dir", required=True, help="path to folder containing images")
parser.add_argument("--target_dir", help="path to folder containing images")
parser.add_argument("--image_height", type=int, help="image height")
parser.add_argument("--image_width", type=int, help="image width")
parser.add_argument("--patch_size", type=int, default=256, help="(cropped) size of images in batch")
parser.add_argument("--batch_size", type=int, default=1, help="number of images in batch")
parser.add_argument("--output_dir", required=True, help="where to put output files")
parser.add_argument("--seed", type=int)
parser.add_argument("--checkpoint", default=None,
                    help="directory with checkpoint to resume training from or use for testing")

parser.add_argument("--network", default="unet", choices=["unet", "resnet", "highwaynet", "densenet"])
parser.add_argument("--u_depth", type=int, default=8, help="depth of u net (maximum 8)")
parser.add_argument("--n_res_blocks", type=int, default= 9, help="number of residual blocks in res net")
parser.add_argument("--n_highway_units", type=int, default=9, help="number of highway units in highway net")
parser.add_argument("--n_dense_blocks", type=int, default=5, help="number of dense blocks in dense net")
parser.add_argument("--n_dense_layers", type=int, default=5, help="number of dense connected layers in each block of the dense net")

parser.add_argument("--loss", default="hinge", choices=["hinge", "square", "softmax", "approx", "dice", "logistic"])

parser.add_argument("--max_steps", type=int, help="number of training steps (0 to disable)")
parser.add_argument("--max_epochs", type=int, help="number of training epochs")
parser.add_argument("--summary_freq", type=int, default=100, help="update summaries every summary_freq steps")
parser.add_argument("--progress_freq", type=int, default=50, help="display progress every progress_freq steps, 0 to disable")
parser.add_argument("--trace_freq", type=int, default=0, help="trace execution every trace_freq steps, 0 to disable")
parser.add_argument("--display_freq", type=int, default=0, help="write current training images every display_freq steps, 0 to disable")
parser.add_argument("--save_freq", type=int, default=5000, help="save model every save_freq steps, 0 to disable")  

parser.add_argument("--filter_size", type=int, default=3, help="size of generator filters in first conv layer")
parser.add_argument("--filter_depth", type=int, default=32, help="number of generator filters in first conv layer")
parser.add_argument("--fliplr", dest="fliplr", action="store_true", help="flip images horizontally (default)")
parser.add_argument("--no_fliplr", dest="fliplr", action="store_false", help="don't flip images horizontally")
parser.set_defaults(fliplr=True)
parser.add_argument("--flipud", dest="flipud", action="store_true", help="flip images vertically (default)")
parser.add_argument("--no_flipud", dest="flipud", action="store_false", help="don't flip images vertically")
parser.set_defaults(flipud=True)
parser.add_argument("--transpose", dest="transpose", action="store_true", help="transpose images (default)")
parser.add_argument("--no_transpose", dest="transpose", action="store_false", help="don't transpose images")
parser.set_defaults(transpose=True)

parser.add_argument("--lr", type=float, default=0.0002, help="initial learning rate for adam")
parser.add_argument("--beta1", type=float, default=0.5, help="momentum term of adam")


a = parser.parse_args()

EPS = 1e-12

if a.mode == 'train':
    a.image_height = a.patch_size
    a.image_width = a.patch_size
else:
    # TODO Read image from input path and determine width, height
    pass

if a.network == "unet":
    a.filter_depth = a.filter_depth * 2

if (a.mode == "test") or (a.mode == "predict"):
    if a.checkpoint is None:
        raise Exception("checkpoint required for test and predict mode")

    # load options from the checkpoint, except for
    excepted_options = {"mode", "input_dir", "target_dir", "image_height", "image_width",
                        "batch_size", "output_dir", "seed", "checkpoint"}

    with open(os.path.join(a.checkpoint, "options.json")) as f:
        for key, val in json.loads(f.read()).items():
            # if key in options:
            if not key in excepted_options:
                print("loaded", key, "=", val)
                setattr(a, key, val)

if a.mode == "predict":
    a.target_dir = a.input_dir   # This is a hack to supply target images for the fetches TODO rewrite sess.run(..) for predict
    # get size of images
    if a.image_height or a.image_width:
        print ("Ignore image_height and image_width parameters for prediction")


Examples = collections.namedtuple("Examples", "input_paths, target_paths, inputs, targets, steps_per_epoch")
Model = collections.namedtuple("Model", "outputs, loss, grads_and_vars, train")


def preprocess(image):
    with tf.name_scope("preprocess"):
        # [0, 1] => [-1, 1]
        return image * 2 - 1


def deprocess(image):
    with tf.name_scope("deprocess"):
        # [-1, 1] => [0, 1]
        return tf.image.convert_image_dtype((image + 1) / 2, dtype=tf.uint8, saturate=True)


def conv(batch_input, out_channels, size=a.filter_size, stride=2, initializer=tf.random_normal_initializer(0, 0.02)):
    with tf.variable_scope("conv"):
        in_channels = batch_input.get_shape()[3]
        filter = tf.get_variable("filter", [size, size, in_channels, out_channels], dtype=tf.float32, initializer=initializer)
        # [batch, in_height, in_width, in_channels], [filter_width, filter_height, in_channels, out_channels]
        #     => [batch, out_height, out_width, out_channels]
        p = int((size - 1) / 2)
        padded_input = tf.pad(batch_input, [[0, 0], [p, p], [p, p], [0, 0]], mode="CONSTANT")
        conv = tf.nn.conv2d(padded_input, filter, [1, stride, stride, 1], padding="VALID")
        return conv


def lrelu(x, a):
    with tf.name_scope("lrelu"):
        # adding these together creates the leak part and linear part
        # then cancels them out by subtracting/adding an absolute value term
        # leak: a*x/2 - a*abs(x)/2
        # linear: x/2 + abs(x)/2

        # this block looks like it has 2 inputs on the graph unless we do this
        x = tf.identity(x)
        return (0.5 * (1 + a)) * x + (0.5 * (1 - a)) * tf.abs(x)


def batchnorm(input, offset_initializer=tf.zeros_initializer()):
    with tf.variable_scope("batchnorm"):
        # this block looks like it has 3 inputs on the graph unless we do this
        input = tf.identity(input)
        channels = input.get_shape()[3]
        offset = tf.get_variable("offset", [channels], dtype=tf.float32, initializer=offset_initializer)
        scale = tf.get_variable("scale", [channels], dtype=tf.float32, initializer=tf.random_normal_initializer(1.0, 0.02))
        mean, variance = tf.nn.moments(input, axes=[0, 1, 2], keep_dims=False)
        variance_epsilon = 1e-5
        normalized = tf.nn.batch_normalization(input, mean, variance, offset, scale, variance_epsilon=variance_epsilon)
        return normalized


def deconv(batch_input, out_channels, size=a.filter_size):
    with tf.variable_scope("deconv"):
        batch, in_height, in_width, in_channels = [int(d) for d in batch_input.get_shape()]
        filter = tf.get_variable("filter", [size, size, out_channels, in_channels], dtype=tf.float32, initializer=tf.random_normal_initializer(0, 0.02))
        # [batch, in_height, in_width, in_channels], [filter_width, filter_height, out_channels, in_channels]
        #     => [batch, out_height, out_width, out_channels]
        conv = tf.nn.conv2d_transpose(batch_input, filter, [batch, in_height * 2, in_width * 2, out_channels], [1, 2, 2, 1], padding="SAME")
        return conv


def check_image(image):
    assertion = tf.assert_equal(tf.shape(image)[-1], 3, message="image must have 3 color channels")
    with tf.control_dependencies([assertion]):
        image = tf.identity(image)

    if image.get_shape().ndims not in (3, 4):
        raise ValueError("image must be either 3 or 4 dimensions")

    # make the last dimension 3 so that you can unstack the colors
    shape = list(image.get_shape())
    shape[-1] = 3
    image.set_shape(shape)
    return image


seed_for_random_cropping = random.randint(0, 2 ** 31 - 1)


def random_transpose(image, seed=None):
  """Randomly transposes an image (rotation by 90 degrees counter clock wise and flip up down).
  With a 1 in 2 chance, outputs the contents of `image` first and second dimensions are transposed,
  which is `height` and `width`.  Otherwise output the image as-is.
  """
  image = tf.convert_to_tensor(image, name='image')
  uniform_random = tf.random_uniform([], 0, 1.0, seed=seed)
  mirror_cond = tf.less(uniform_random, .5)
  result = tf.cond(mirror_cond,
                   lambda: tf.transpose(image, perm=[1, 0, 2]),
                   lambda: image)
  return result


def transform(image, seed):
    r = image
    if a.mode == 'train':  # augment image by flipping and cropping
        if a.fliplr:
            r = tf.image.random_flip_left_right(r, seed=seed)
        if a.flipud:
            r = tf.image.random_flip_up_down(r, seed=seed)
        if a.transpose:
            r = random_transpose(r, seed=seed)

        r = tf.random_crop(r, size=[a.patch_size, a.patch_size, 3], seed=seed)

        r.set_shape([a.patch_size, a.patch_size, 3])  # must do this if tf.image.resize is not used, otherwise shape unknown

    else:  # use full sized original image
        r.set_shape([a.image_height, a.image_width, 3])  # use full size image

    return r


def load_examples():
    if a.input_dir is None or not os.path.exists(a.input_dir):
        raise Exception("input_dir does not exist")

    if a.target_dir is None:   # image pair A and B
        n_images, a_paths, raw_image = load_images(a.input_dir, 'AB')
        # break apart image pair and move to range [-1, 1]
        width = tf.shape(raw_image)[1] # [height, width, channels]
        a_images = preprocess(raw_image[:,:width//2,:])
        b_images = preprocess(raw_image[:,width//2:,:])
        b_paths = a_paths
        print("examples count = %d (each A and B)" % n_images)

    elif not os.path.exists(a.target_dir):  # images B in other directory
        raise Exception("target_dir does not exist")
    else:  # load A and B images
        n_a_images, a_paths, raw_a_image = load_images(a.input_dir, 'A')
        a_images = preprocess(raw_a_image)
        n_b_images, b_paths, raw_b_image = load_images(a.target_dir, 'B')
        b_images = preprocess(raw_b_image)
        print("examples count = %d, %d (A, B)" % (n_a_images, n_b_images))
        n_images = max(n_a_images, n_b_images)

    inputs, targets = [a_images, b_images]
    input_paths, target_paths = [a_paths, b_paths]

    with tf.name_scope("input_images"):
        input_images = transform(inputs, seed=seed_for_random_cropping)

    with tf.name_scope("target_images"):
        target_images = transform(targets, seed=seed_for_random_cropping)

    # paired images
    input_paths_batch, target_paths_batch, inputs_batch, targets_batch = \
        tf.train.batch([input_paths, target_paths, input_images, target_images], batch_size=a.batch_size, name="paired_batch")

    steps_per_epoch = int(math.ceil(n_images / a.batch_size))

    return Examples(
        input_paths=input_paths_batch,
        target_paths=target_paths_batch,
        inputs=inputs_batch,
        targets=targets_batch,
        steps_per_epoch=steps_per_epoch,
    )


def load_images(input_dir, input_name=''):
    input_paths = glob.glob(os.path.join(input_dir, "*.jpg"))
    decode = tf.image.decode_jpeg
    if len(input_paths) == 0:
        input_paths = glob.glob(os.path.join(input_dir, "*.png"))
        decode = tf.image.decode_png
    if len(input_paths) == 0:
        raise Exception("%s contains no images (jpg/png)" % input_dir)
    else:
        def get_name(path):
            name, _ = os.path.splitext(os.path.basename(path))
            return name

        # if the image names are numbers, sort by the value rather than asciibetically
        # having sorted inputs means that the outputs are sorted in test mode
        if all(get_name(path).isdigit() for path in input_paths):
            input_paths = sorted(input_paths, key=lambda path: int(get_name(path)))
        else:
            input_paths = sorted(input_paths)

        with tf.name_scope("load_%simages" % input_name):
            path_queue = tf.train.string_input_producer(input_paths, shuffle=a.mode == "train")
            reader = tf.WholeFileReader()
            paths, contents = reader.read(path_queue)
            raw_input = decode(contents)
            raw_input = tf.image.convert_image_dtype(raw_input, dtype=tf.float32)

            assertion = tf.assert_equal(tf.shape(raw_input)[2], 3, message="image does not have 3 channels")
            with tf.control_dependencies([assertion]):
                raw_input = tf.identity(raw_input)

            raw_input.set_shape([None, None, 3])

    return len(input_paths), paths, raw_input


def create_u_net(generator_inputs, generator_outputs_channels):

    ngf = a.filter_depth * np.array([1, 2, 4, 8, 8, 8, 8, 8])

    def encoder_decoder(input, depth):
        if depth > a.u_depth:
            return input

        with tf.variable_scope("encoder_%d" % depth):
            down = lrelu(input, 0.2)
            down = conv(down, ngf[depth-1], stride=2)
            down = batchnorm(down)

        up = encoder_decoder(down, depth + 1)

        with tf.variable_scope("decoder_%d" % depth):
            output = tf.concat([up, down], axis=3)
            output = tf.nn.relu(output)
            output = deconv(output, ngf[depth-1])
            output = batchnorm(output)
            if depth > 5:
                output = tf.nn.dropout(output, keep_prob=0.5)

        return output

    with tf.variable_scope("encoder_1"):  # [batch, 256, 256, in_channels] => [batch, 128, 128, ngf]
        down = conv(generator_inputs, ngf[1], stride=2)

    up = encoder_decoder(down, 2)

    with tf.variable_scope("decoder_1"):  # [batch, 128, 128, ngf * 2] => [batch, 256, 256, generator_outputs_channels]
        output = tf.concat([up, down], axis=3)
        output = tf.nn.relu(output)
        output = deconv(output, generator_outputs_channels)
        output = tf.tanh(output)

    return output


def create_res_net(generator_inputs, generator_outputs_channels):
    layers = []

    encoder(generator_inputs, layers)

    # 9 residual blocks = r128: [batch, 64, 64, ngf*4] => [batch, 64, 64, ngf*4]
    with tf.variable_scope("resnet"):
        for block in range(a.n_res_blocks):
            with tf.variable_scope("residual_block_%d" % (block + 1)):
                input = layers[-1]
                output = input
                for layer in range(2):
                    with tf.variable_scope("layer_%d" % (layer + 1)):
                        output = conv(output, a.filter_depth * 4, size=3, stride=1)
                        output = batchnorm(output)
                        output = tf.nn.relu(output)
                layers.append(input+output)

    decoder(generator_outputs_channels, layers)

    return layers[-1]


def create_highway_net(generator_inputs, generator_outputs_channels):
    layers = []

    encoder(generator_inputs, layers)

    # n_layers = 2 * n_highway_units
    with tf.variable_scope("highwaynet"):
        for block in range(a.n_highway_units):
            with tf.variable_scope("highway_unit_%d" % (block + 1)):
                input = layers[-1]
                with tf.variable_scope("transform"):
                    output = input
                    for layer in range(2):
                        with tf.variable_scope("layer_%d" % (layer + 1)):
                            output = conv(output, a.filter_depth * 4, size=3, stride=1)
                            output = batchnorm(output)
                            output = tf.nn.relu(output)
                with tf.variable_scope("gate"):
                    gate = conv(input, a.filter_depth * 4, size=3, stride=1)
                    gate = batchnorm(gate, offset_initializer=tf.constant_initializer(-10.0))
                    gate = (tf.nn.sigmoid(gate)+1.)/2.   # [-inf, +inf] --> [-1, +1]  --> [0, 1]

                layers.append(input*(1.0-gate) + output*gate)

    decoder(generator_outputs_channels, layers)

    return layers[-1]


def create_dense_net(generator_inputs, generator_outputs_channels):
    layers = []

    encoder(generator_inputs, layers)

    # n_layers = n_dense_blocks * n_dense_layers
    with tf.variable_scope("densenet"):
        for block in range(a.n_dense_blocks):
            with tf.variable_scope("dense_block_%d" % (block + 1)):
                nodes = []
                nodes.append(layers[-1])
                for layer in range(a.n_dense_layers):
                    with tf.variable_scope("dense_layer_%d" % (layer + 1)):
                        input = tf.concat(nodes, 3)
                        output = conv(input, a.filter_depth * 4, size=3, stride=1)
                        output = batchnorm(output)
                        output = tf.nn.relu(output)
                        nodes.append(output)
                layers.append(nodes[-1])

    decoder(generator_outputs_channels, layers)

    return layers[-1]


def encoder(generator_inputs, layers):
    with tf.variable_scope("encoder"):
        # encoder_1 = c7s1 - 32: [batch, 256, 256, in_channels] => [batch, 256, 256, ngf]
        with tf.variable_scope("conv_1"):
            output = conv(generator_inputs, a.filter_depth, size=7, stride=1)
            layers.append(output)

        # encoder_2 = d64: [batch, 256, 256, ngf] => [batch, 128, 128, ngf*2]
        with tf.variable_scope("conv_2"):
            output = conv(layers[-1], a.filter_depth * 2, size=3, stride=2)
            layers.append(output)

        # encoder_3 = d128: [batch, 128, 128, ngf*2] => [batch, 64, 64, ngf*4]
        with tf.variable_scope("conv_3"):
            output = conv(layers[-1], a.filter_depth * 4, size=3, stride=2)
            layers.append(output)


def decoder(generator_outputs_channels, layers):
    with tf.variable_scope("decoder"):
        # decoder_3 = u64: [batch, 64, 64, ngf*4] => [batch, 128, 128, ngf*2]
        with tf.variable_scope("deconv_1"):
            input = layers[-1]
            output = deconv(input, a.filter_depth * 2)
            output = batchnorm(output)
            rectified = tf.nn.relu(output)
            layers.append(rectified)

        # decoder_2 = u32: [batch, 128, 128, ngf*2] => [batch, 256, 256, ngf]
        with tf.variable_scope("deconv_2"):
            input = layers[-1]
            output = deconv(input, a.filter_depth)
            output = batchnorm(output)
            rectified = tf.nn.relu(output)
            layers.append(rectified)

        # decoder_1 = c7s1-3: [batch, 256, 256, ngf] => [batch, 256, 256, generator_output_channels]
        with tf.variable_scope("deconv_3"):
            input = layers[-1]
            output = conv(input, generator_outputs_channels, size=7, stride=1)
            output = tf.tanh(output)
            layers.append(output)


def log_loss(real, fake):
    # minimizing -tf.log(x) will try to get x to 1
    # predict_real => 1
    # predict_fake => 0
    with tf.name_scope("log_loss_paired_images"):
        result = tf.reduce_mean(-(tf.log(real + EPS) + tf.log(1 - fake + EPS)))
    return result


def square_loss(real, fake):
    # minimizing tf.square(1 - x) will try to get x to 1
    # predict_real => 1
    # predict_fake => 0
    if a.model == 'CycleGAN':  # unpaired images in loss
        result = tf.reduce_mean(tf.square(real - 1)) + tf.reduce_mean(tf.square(fake))
    else:   # paired images in loss
        result = tf.reduce_mean(tf.square(real - 1) + tf.square(fake))
    return result


def cross_entropy(targets, outputs):
    # Note: Numerical instability: getting NaN after approximately 100 epochs
    with tf.name_scope('cross_entropy'):
        clipped = tf.clip_by_value(outputs, EPS, 1. - EPS)  # clip to avoid log(0)
        result = -tf.reduce_mean(targets * tf.log(clipped) + (1. - targets) * tf.log(1. - clipped))
    return result


def approx_cross_entropy(targets, outputs):
    def approx_log(x):
        # log(x) = (x-1)^1/1 - (x-1)^2/2 + O(x^3)
        return (x - 1.) - tf.square(x - 1.) / 2.
    return -tf.reduce_mean(targets * approx_log(outputs) + (1. - targets) * approx_log(1. - outputs))


def dice_coe(output, target, epsilon=1e-10):
    """
    Differentiable Soerensen-Dice coefficient for comparing the similarity of two distributions, usually be used
    for binary image segmentation i.e. labels are binary. The coefficient = [0, 1], 1 if totally match.
    From http://tensorlayer.readthedocs.io/en/latest/_modules/tensorlayer/cost.html
    See https://en.wikipedia.org/wiki/Soerensen-Dice_coefficient
    """
    inse = tf.reduce_sum( output * target )
    l = tf.reduce_sum( output * output )
    r = tf.reduce_sum( target * target )
    dice = 2 * (inse) / (l + r)
    if epsilon == 0:
        return dice
    else:
        return tf.clip_by_value(dice, 0, 1.0-epsilon)


def classic_loss(outputs, targets, target_loss):

    if target_loss == "hinge":
        # Absolute value loss / L1 loss
        gen_loss_classic = tf.reduce_mean(tf.abs(targets - outputs))

    elif target_loss == "square":
        # Mean squared error, L2^2 loss
        gen_loss_classic = tf.reduce_mean(tf.square(targets - outputs))

    elif target_loss == "softmax":
        # Softmax cross entropy loss for one-hot-labels
        # Note: Conversion needed: [-1,+1] ==> [0, 1]
        gen_loss_classic = tf.reduce_mean(tf.losses.softmax_cross_entropy(targets/2+0.5, outputs/2+0.5))

    elif target_loss == "approx":
        # Cross entropy for multi-class multi-label
        # Using an approximation of cross entropy to avoid numerical instability
        # Note: Conversion needed: [-1,+1] ==> [0, 1]
        gen_loss_classic = approx_cross_entropy(targets / 2. + 0.5, outputs / 2. + 0.5)

    elif target_loss == "dice":
        # # Dice coefficient
        gen_loss_classic = 1. - dice_coe(outputs, targets)

    elif target_loss == "logistic":
        # # [-1,+1] ==> [0, 1] for labels
        gen_loss_classic = tf.losses.log_loss(targets / 2. + 0.5, outputs / 2. + 0.5)

    # experimental implementations:

    elif target_loss == "naive":
        # # Without softmax for multi-class, multi-label prediction, unstable!
        gen_loss_classic = cross_entropy(targets/2.+0.5, outputs/2.+0.5)

    elif target_loss == "sqr0":
        # # Square loss for numerical stability ----> Implemented without rescaling: THIS WORKS But why?
        gen_loss_classic = tf.reduce_mean(targets * tf.square(outputs - 1.) + (1. - targets) * tf.square(outputs))

    elif target_loss == "sqr1":
        # # Square loss for numerical stability +1/+1 --> 0, +1/-1 --> 8, -1/+1 --> 0, -1/-1 --> 8 TODO: Testing this
        gen_loss_classic = tf.reduce_mean((1. + targets) * tf.square(1. - outputs) + (1. - targets) * tf.square(outputs + 1.))

    else:
        raise ValueError("Unknown classic loss: ", target_loss)

    return gen_loss_classic


def create_model(inputs, targets, network=a.network, target_loss=a.loss):

    with tf.variable_scope(network):
        out_channels = int(targets.get_shape()[-1])
        if network == 'unet':
            outputs = create_u_net(inputs, out_channels)
        elif network == 'resnet':
            outputs = create_res_net(inputs, out_channels)
        elif network == 'highwaynet':
            outputs = create_highway_net(inputs, out_channels)
        elif network == 'densenet':
            outputs = create_dense_net(inputs, out_channels)

    with tf.name_scope("loss"):
        loss = classic_loss(outputs, targets, target_loss)

    with tf.name_scope("train"):
        gen_tvars = [var for var in tf.trainable_variables() if var.name.startswith(network)]
        gen_optim = tf.train.AdamOptimizer(a.lr, a.beta1)
        grads_and_vars = gen_optim.compute_gradients(loss, var_list=gen_tvars)

        # without gradient clipping
        train = gen_optim.apply_gradients(grads_and_vars)

    ema = tf.train.ExponentialMovingAverage(decay=0.99)
    update_losses = ema.apply([ loss])

    global_step = tf.contrib.framework.get_or_create_global_step()
    incr_global_step = tf.assign(global_step, global_step+1)

    return Model(
        loss=ema.average(loss),
        grads_and_vars=grads_and_vars,
        outputs=outputs,
        train=tf.group(update_losses, incr_global_step, train),
    )


def save_predicted_images(fetches):
    if not os.path.exists(a.output_dir):
        os.makedirs(a.output_dir)

    fileset = []
    for i, in_path in enumerate(fetches["input_paths"]):
        name, _ = os.path.splitext(os.path.basename(in_path.decode("utf8")))
        filename = name + ".png"
        out_path = os.path.join(a.output_dir, filename)
        contents = fetches['outputs'][i]
        with open(out_path, "wb") as f:
            f.write(contents)
        fileset.append(filename)
    return fileset


def save_images(fetches, step=None,image_kinds=("inputs", "outputs", "targets")):
    image_dir = os.path.join(a.output_dir, "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    filesets = []
    for i, in_path in enumerate(fetches["input_paths"]):
        name, _ = os.path.splitext(os.path.basename(in_path.decode("utf8")))
        fileset = {"name": name, "step": step}
        for kind in image_kinds:
            filename = name + "-" + kind + ".png"
            if step is not None:
                filename = "%08d-%s" % (step, filename)
            fileset[kind] = filename
            out_path = os.path.join(image_dir, filename)
            contents = fetches[kind][i]
            with open(out_path, "wb") as f:
                f.write(contents)
        filesets.append(fileset)
    return filesets


def append_index(filesets, step=False, image_kinds=("inputs", "outputs", "targets")):
    index_path = os.path.join(a.output_dir, "index.html")
    if os.path.exists(index_path):
        index = open(index_path, "a")
    else:
        index = open(index_path, "w")
        index.write("<html><body><table><tr>")
        if step:
            index.write("<th>step</th>")
        index.write("<th>name</th><th>input</th><th>output</th><th>target</th></tr>\n")

    for fileset in filesets:
        index.write("<tr>")

        if step:
            index.write("<td>%d</td>" % fileset["step"])
        index.write("<td>%s</td>" % fileset["name"])

        for kind in image_kinds:
            index.write("<td><img src='images/%s'></td>" % fileset[kind])

        index.write("</tr>\n")
    return index_path


def main():
    if tf.__version__.split('.')[0] != "1":
        raise Exception("Tensorflow version 1 required")

    if a.seed is None:
        a.seed = random.randint(0, 2**31 - 1)

    tf.set_random_seed(a.seed)
    np.random.seed(a.seed)
    random.seed(a.seed)

    if not os.path.exists(a.output_dir):
        os.makedirs(a.output_dir)

    for k, v in a._get_kwargs():
        print(k, "=", v)

    with open(os.path.join(a.output_dir, "options.json"), "w") as filename:
        filename.write(json.dumps(vars(a), sort_keys=True, indent=4))

    examples = load_examples()

    model = create_model(examples.inputs, examples.targets)

    # encoding images for saving
    with tf.name_scope("encode_images"):
        display_fetches = {}
        for name, value in examples._asdict().items():
            if "path" in name:
                display_fetches[name] = value
            elif tf.is_numeric_tensor(value):
                display_fetches[name] = tf.map_fn(tf.image.encode_png, deprocess(value), dtype=tf.string, name=name+"_pngs")
        for name, value in model._asdict().items():
            if tf.is_numeric_tensor(value) and "predict_" not in name:
                display_fetches[name] = tf.map_fn(tf.image.encode_png, deprocess(value), dtype=tf.string, name=name+"_pngs")

    # progress report for all losses
    with tf.name_scope("progress_summary"):
        progress_fetches = {}
        for name, value in model._asdict().items():
            if not tf.is_numeric_tensor(value) and "grads_and_vars" not in name and not name == "train":
                progress_fetches[name] = value

    # summaries for model: images, scalars, histograms
    for name, value in examples._asdict().items():
        if tf.is_numeric_tensor(value):
            with tf.name_scope(name + "_summary"):
                tf.summary.image(name, deprocess(value))
    for name, value in model._asdict().items():
        if tf.is_numeric_tensor(value):
            with tf.name_scope(name + "_summary"):
                if "predict_" in name:    # discriminators produce values in [0, 1]
                    tf.summary.image(name, tf.image.convert_image_dtype(value, dtype=tf.uint8))
                else:   # generators produce values in [-1, 1]
                    tf.summary.image(name, deprocess(value))
        elif "grads_and_vars" in name:
            for grad, var in value:
                tf.summary.histogram(var.op.name + "/gradients", grad)
        elif not name == "train":
            tf.summary.scalar(name, value)

    for var in tf.trainable_variables():
        tf.summary.histogram(var.op.name + "/values", var)

    with tf.name_scope("parameter_count"):
        parameter_count = tf.reduce_sum([tf.reduce_prod(tf.shape(v)) for v in tf.trainable_variables()])

    saver = tf.train.Saver(max_to_keep=1)

    logdir = a.output_dir if (a.trace_freq > 0 or a.summary_freq > 0) else None
    sv = tf.train.Supervisor(logdir=logdir, save_summaries_secs=0, saver=None)
    with sv.managed_session() as sess:
        print("parameter_count =", sess.run(parameter_count))

        if a.checkpoint is not None:
            checkpoint = tf.train.latest_checkpoint(a.checkpoint)
            saver.restore(sess, checkpoint)

        max_steps = 2**32
        if a.max_epochs is not None:
            max_steps = examples.steps_per_epoch * a.max_epochs
        if a.max_steps is not None:
            max_steps = a.max_steps

        if a.mode == "test":
            # testing
            # at most, process the test data once
            max_steps = min(examples.steps_per_epoch, max_steps)
            for step in range(max_steps):
                results = sess.run(display_fetches)
                filesets = save_images(results)
                for i, filename in enumerate(filesets):
                    print("evaluated image", filename["name"])
                index_path = append_index(filesets)

            print("wrote index at %s" % index_path)

        if a.mode == "predict":
            # predicting
            # at most, process the test data once
            max_steps = min(examples.steps_per_epoch, max_steps)
            for step in range(max_steps):
                results = sess.run(display_fetches)
                fileset = save_predicted_images(results)
                for filename in fileset:
                    print("predicted image", filename)
            print("wrote predicted labels at %s" % a.output_dir)

        if a.mode == "train":
            # training
            start = time.time()

            for step in range(max_steps):
                def should(freq):
                    return freq > 0 and ((step + 1) % freq == 0 or step == max_steps - 1)

                options = None
                run_metadata = None
                if should(a.trace_freq):
                    options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                    run_metadata = tf.RunMetadata()

                fetches = {
                    "train": model.train,
                    "global_step": sv.global_step,
                }

                if should(a.progress_freq):
                    fetches["progress"] = progress_fetches

                if should(a.summary_freq):
                    fetches["summary"] = sv.summary_op

                if should(a.display_freq):
                    fetches["display"] = display_fetches

                results = sess.run(fetches, options=options, run_metadata=run_metadata)

                if should(a.summary_freq):
                    print("recording summary")
                    sv.summary_writer.add_summary(results["summary"], results["global_step"])

                if should(a.display_freq):
                    print("saving display images")
                    filesets = save_images(results["display"], step=results["global_step"])
                    append_index(filesets, step=True)

                if should(a.trace_freq):
                    print("recording trace")
                    sv.summary_writer.add_run_metadata(run_metadata, "step_%d" % results["global_step"])

                if should(a.progress_freq):
                    # global_step will have the correct step count if we resume from a checkpoint
                    train_epoch = math.ceil(results["global_step"] / examples.steps_per_epoch)
                    train_step = (results["global_step"] - 1) % examples.steps_per_epoch + 1
                    rate = (step + 1) * a.batch_size / (time.time() - start)
                    remaining = (max_steps - step) * a.batch_size / rate
                    print("progress  epoch %d  step %d  image/sec %0.1f  remaining %d min" % (train_epoch, train_step, rate, remaining / 60))
                    for name, value in results["progress"].items():
                        print (name, value)

                if should(a.save_freq):
                    print("saving model")
                    saver.save(sess, os.path.join(a.output_dir, "model"), global_step=sv.global_step)

                if sv.should_stop():
                    break


main()
