#!/usr/bin/env python3

import tensorflow as tf
from tensorflow.python.framework import graph_io
from NetworkBuilder import NetworkBuilder
import datetime
import numpy as np
import os, os.path, sys

def getLayerNames():
    ##namegraph = get_names()
    tensor_names = [t.name for op in tf.get_default_graph().get_operations() for t in op.values()]
    for t in tensor_names:
        print("\t{}".format(t))

def get_names(graph=tf.get_default_graph()):
    return [t.name for op in graph.get_operations() for t in op.values()]

with tf.name_scope("Input") as scope:
    #
    # input shape is [batch size, height, width, channels]
    #

    input_img = tf.placeholder(dtype='float', shape=[None, 128, 128, 3], name="Inputs")

with tf.name_scope("Target") as scope:
    target_labels = tf.placeholder(dtype='float', shape=[None, 2], name="Targets")
    nb = NetworkBuilder()

#with tf.name_scope("ModelWithCustomLayer") as scope:
with tf.name_scope("ModCosh") as scope:
    model = input_img
    model = nb.attach_cosh_layer(model)
    model = nb.attach_conv_layer(model, 32, summary='True')
    model = nb.attach_relu_layer(model)
    model = nb.attach_conv_layer(model, 32, summary='True')
    model = nb.attach_relu_layer(model)
    model = nb.attach_pooling_layer(model)

    model = nb.attach_cosh_layer(model)
    model = nb.attach_conv_layer(model, 64, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_conv_layer(model, 64, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_pooling_layer(model)

    model = nb.attach_cosh_layer(model)
    model = nb.attach_conv_layer(model, 128, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_conv_layer(model, 128, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_pooling_layer(model)

    model = nb.flatten(model)
    model = nb.attach_dense_layer(model, 200, summary=True)
    model = nb.attach_sigmoid_layer(model)
    model = nb.attach_dense_layer(model, 32, summary=True)
    model = nb.attach_sigmoid_layer(model)
    model = nb.attach_dense_layer(model, 2)
    prediction = nb.attach_softmax_layer(model)

with tf.name_scope("Optimization") as scope:
    global_step = tf.Variable(0, name='global_step', trainable=False)
    cost = tf.nn.softmax_cross_entropy_with_logits_v2(labels=target_labels, logits=model)
    cost = tf.reduce_mean(cost)
    tf.summary.scalar("cost", cost)

    optimizer = tf.train.AdamOptimizer().minimize(cost, global_step=global_step)

with tf.name_scope('accuracy') as scope:
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(target_labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

savedir = ""

if len(sys.argv) > 1:
  hm_dir = sys.argv[1]

  if os.path.isdir(hm_dir):
    savedir = hm_dir
  else:
    print("\nError: Directory ({}) doesn't exist.  Exiting.".format(hm_dir))
    sys.exit(1)

if not savedir: 
  hm_dir = os.path.expanduser('~')
  savedir = "{}/{}".format(hm_dir, "cl_new")

with tf.Session() as sess:
    #output_layer = "ModCosh/Activation_8/softmax_output:0"
    #output_layer = "ModCosh/Merge/MergeSummary:0"
    #output_layer = "ModCosh/Activation_8/softmax_output:0"
    output_layer = "ModCosh/Activation_8/softmax_output"
    saver = tf.train.Saver()
    summaryMerged = tf.summary.merge_all()
    LOGDIR="logs"
    writer = tf.summary.FileWriter(LOGDIR)
    writer.add_graph(sess.graph)
    tf.global_variables_initializer().run()
    nodes = [n.name for n in tf.get_default_graph().as_graph_def().node]
    #save_path = saver.save(sess, "{}/{}".format(savedir, model))
    tf.train.write_graph(sess.graph_def, savedir, 'graph.pb')

    save_path = saver.save(sess, "{}/{}".format(savedir, "model.ckpt"))
    print("Model saved in path: %s" % save_path)


    frozen = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, [output_layer])
    graph_io.write_graph(frozen, savedir, 'frozen_inference_graph.pb', as_text=False)

