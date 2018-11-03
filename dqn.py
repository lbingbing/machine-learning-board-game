import tensorflow as tf
import numpy as np
import h5py
import os

class DqnModel:
    def __init__(self, board_shape, action_dim, model_name):
        self.model_path = model_name + '/model'

        self.graph = tf.Graph()
        with self.graph.as_default():
            self.input_state_t = tf.placeholder(dtype = tf.float32, shape = (None, board_shape[0], board_shape[1], 2))

            self.input_target_Q_t = tf.placeholder(dtype = tf.float32, shape = (None, action_dim))
            self.input_Q_mask_t = tf.placeholder(dtype = tf.float32, shape = (None, action_dim))

            self.learning_rate = tf.placeholder(dtype = tf.float32)

            reshape_t = tf.reshape(tensor = self.input_state_t, shape = (-1, board_shape[0], board_shape[1], 2))
            conv_t = tf.layers.conv2d(inputs = reshape_t, filters = 16, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
            conv_t = tf.layers.conv2d(inputs = conv_t, filters = 32, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
            conv_t = tf.layers.conv2d(inputs = conv_t, filters = 64, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
            conv_t = tf.layers.conv2d(inputs = conv_t, filters = 128, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
            conv_t = tf.layers.conv2d(inputs = conv_t, filters = 256, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
            flatten_t = tf.layers.flatten(inputs = conv_t)

            dense_t = tf.layers.dense(inputs = flatten_t, units = action_dim, activation = tf.nn.relu)
            dense_t = tf.layers.dense(inputs = dense_t, units = action_dim, activation = tf.nn.relu)
            self.Q_logit_t = tf.layers.dense(inputs = dense_t, units = action_dim)
            self.Q_t = tf.nn.tanh(self.Q_logit_t)

            self.loss = tf.reduce_mean(tf.square(tf.reduce_sum(self.Q_t * self.input_Q_mask_t - self.input_target_Q_t, axis = 1)))
            self.optimizer = tf.train.AdamOptimizer(learning_rate = self.learning_rate).minimize(self.loss)

            self.saver = tf.train.Saver()

        self.sess = tf.Session(graph = self.graph)

    def init_parameters(self):
        with self.graph.as_default():
            init_op = tf.global_variables_initializer()
            self.sess.run(init_op)

    def save(self):
        self.saver.save(self.sess, self.model_path)

    def load(self):
        self.saver.restore(self.sess, self.model_path)

    def get_parameters(self):
        with self.graph.as_default():
            variables_dict = {variable.name: self.sess.run(variable) for variable in tf.trainable_variables()}
        return variables_dict

    def get_Q(self, state_m):
        return self.sess.run([self.Q_logit_t, self.Q_t], feed_dict = {self.input_state_t: state_m})

    def train(self, state_m_batch, target_Q_m_batch, action_m_batch, learning_rate):
        _, loss = self.sess.run([self.optimizer, self.loss], feed_dict = {self.input_state_t: state_m_batch, self.input_target_Q_t: target_Q_m_batch, self.input_Q_mask_t: action_m_batch, self.learning_rate: learning_rate})
        return loss

def get_legal_Q_m(model, state_m, legal_action_mask_m):
    Q_logit_m, Q_m = model.get_Q(state_m)
    legal_Q_logit_m = np.where(legal_action_mask_m, Q_logit_m, -np.inf)
    legal_Q_m = np.where(legal_action_mask_m, Q_m, -np.inf)
    return legal_Q_logit_m, legal_Q_m

def get_opt_action(model, state):
    state_m = state.to_state_m()
    legal_action_mask_m = state.get_legal_action_mask_m()
    _, legal_Q_m = get_legal_Q_m(model, state_m, legal_action_mask_m)
    opt_action_index = np.asscalar(legal_Q_m.argmax(axis = 1))
    action = state.action_index_to_action(opt_action_index)
    return action

def get_max_Q_m(model, state_m, legal_action_mask_m):
    legal_Q_logit_m, legal_Q_m = get_legal_Q_m(model, state_m, legal_action_mask_m)
    max_Q_m = np.max(legal_Q_m, axis = 1).reshape(-1, 1)
    max_Q_logit_m = np.max(legal_Q_logit_m, axis = 1).reshape(-1, 1)
    return max_Q_logit_m, max_Q_m

