from __future__ import unicode_literals
import os
import numpy as np
data_type = {0: 'pants', 1: 'tshirts', 2: 'kurta', 3: 'lehenga', 4: 'one piece', 5: 'saree'}

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

import pickle
import numpy as np

n_nodes_hl1 = 1000
n_nodes_hl2 = 1000
n_nodes_hl3 = 1000
n_classes = 6
batch_size = 100
x = tf.placeholder('float', [None, 900])
y = tf.placeholder('float')
hidden_1_layer = {'weights': tf.Variable(tf.random_normal([900, n_nodes_hl1])),
                  'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                  'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                  'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                'biases': tf.Variable(tf.random_normal([n_classes]))}


def neural_network_model(data_input):

    l1 = tf.add(tf.matmul(data_input, hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)
    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)
    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']
    return output

saver = tf.train.Saver()


def train_neural_network(x):

    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    hm_epochs = 100
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            epoch_x = data
            epoch_y = labels
            _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
            epoch_loss += c
            print('Epoch', epoch + 1, 'completed out of', hm_epochs, 'loss:', epoch_loss)
        saver.save(sess, 'model.ckpt')
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:', accuracy.eval({x: test_data, y: test_labels}))


def use_neural_network(v):

    prediction= neural_network_model(x)
    g=prediction.graph
    with tf.Session(graph=g) as sess:

        sess.run(tf.global_variables_initializer())
        saver.restore(sess, "model.ckpt")


        z = prediction.eval(session=sess,feed_dict={x: v})
        print (z)
        result1=max(max(z))
        result = (sess.run(tf.argmax(prediction.eval(session=sess,feed_dict={x: v}),1)))
        return [result,result1]


#train_neural_network(x)
