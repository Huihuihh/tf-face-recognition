import os
import re

import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

from tensorface.const import PRETREINED_MODEL_DIR
from openvino.inference_engine import IENetwork, IECore

MODEL_PATH = '../lrmodels/facenet.xml'

# to get Flask not complain
global tf
_tf = tf
global sess
sess = None

# inception net requires this
def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0 / np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1 / std_adj)
    return y

def embedding(face_np):
    model_xml = MODEL_PATH
    model_bin = os.path.splitext(model_xml)[0] + ".bin"
    ie = IECore()
    net = IENetwork(model=model_xml, weights=model_bin)
    input_blob,out_blob,net.batch_size = next(iter(net.inputs)),next(iter(net.outputs)),1
    n, c, h, w = net.inputs[input_blob].shape
    exec_net = ie.load_network(network=net, device_name='MYRIAD')
    face_np = face_np.reshape(1,3,160,160)
    res = exec_net.infer(inputs={input_blob: face_np})[out_blob]
    return res


def input_shape():
    return _tf.get_default_graph().get_tensor_by_name("input:0").get_shape()


def embedding_size():
    return _tf.get_default_graph().get_tensor_by_name("embeddings:0").get_shape()[1]


