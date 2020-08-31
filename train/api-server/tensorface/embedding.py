import os
import re

import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

from tensorface.const import PRETREINED_MODEL_DIR

MODEL_PATH = os.environ.get("MODEL_PATH")

# to get Flask not complain
global tf
_tf = tf
global sess
sess = None

def load_model(model, input_map=None):
    global _tf
    global sess
    if sess is None:
        sess = _tf.Session()
        # Check if the model is a model directory (containing a metagraph and a checkpoint file)
        #  or if it is a protobuf file with a frozen graph
        model_exp = os.path.expanduser(model)
        if (os.path.isfile(model_exp)):
            print('Model filename: %s' % model_exp)
            with gfile.FastGFile(model_exp,'rb') as f:
                graph_def = _tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _tf.import_graph_def(graph_def, input_map=input_map, name='')
        else:
            print('Model directory: %s' % model_exp)
            meta_file, ckpt_file = get_model_filenames(model_exp)

            print('Metagraph file: %s' % meta_file)
            print('Checkpoint file: %s' % ckpt_file)

            saver = _tf.train.import_meta_graph(os.path.join(model_exp, meta_file), input_map=input_map)
            #saver.restore(_tf.get_default_session(), os.path.join(model_exp, ckpt_file))
            saver.restore(sess, os.path.join(model_exp, ckpt_file))

def get_model_filenames(model_dir):
    global _tf
    files = os.listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files)==0:
        raise ValueError('No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files)>1:
        raise ValueError('There should not be more than one meta file in the model directory (%s)' % model_dir)
    meta_file = meta_files[0]
    ckpt = _tf.train.get_checkpoint_state(model_dir)
    if ckpt and ckpt.model_checkpoint_path:
        ckpt_file = os.path.basename(ckpt.model_checkpoint_path)
        return meta_file, ckpt_file

    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups())>=2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file


load_model(MODEL_PATH)


# inception net requires this
def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj)
    return y


def embedding(face_np):
    global sess
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    x = prewhiten(face_np)
    feed_dict = {images_placeholder: [x], phase_train_placeholder: False}
    result = sess.run(embeddings, feed_dict=feed_dict)[0]
    return result


def input_shape():
    return _tf.get_default_graph().get_tensor_by_name("input:0").get_shape()


def embedding_size():
    return _tf.get_default_graph().get_tensor_by_name("embeddings:0").get_shape()[1]


