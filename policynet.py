import tensorflow as tf
import numpy as np

class PolicyNetModel:
    def __init__(self, board_shape, action_dim, model_name):
        self.model_path = model_name + '/model'

        self.graph = tf.Graph()
        with self.graph.as_default():
            self.input_state_t = tf.placeholder(dtype = tf.float32, shape = (None, board_shape[0], board_shape[1], 2))

            self.input_action_t = tf.placeholder(dtype = tf.float32, shape = (None, action_dim))
            self.input_advantage_t = tf.placeholder(dtype = tf.float32, shape = (None, 1))

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
            self.logits_t = tf.layers.dense(inputs = dense_t, units = action_dim)
            self.action_t = tf.nn.softmax(logits = self.logits_t)

            self.loss = tf.reduce_mean(-tf.log(tf.reduce_sum(self.action_t * self.input_action_t, axis = 1)) * self.input_advantage_t)
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

    def get_action(self, state_m):
        return self.sess.run([self.logits_t, self.action_t], feed_dict = {self.input_state_t: state_m})

    def train(self, state_m_time_batch, action_m_time_batch, advantage_m_time_batch, learning_rate):
        self.sess.run(self.optimizer, feed_dict = {self.input_state_t: state_m_time_batch, self.input_action_t: action_m_time_batch, self.input_advantage_t: advantage_m_time_batch, self.learning_rate: learning_rate})

def get_action(model, state, player_id):
    state_m = state.to_state_m()
    _, action_m = model.get_action(state_m)
    action_m = action_m.reshape(-1)
    legal_action_m = np.zeros(state.get_action_dim())
    legal_action_indexes = [state.action_to_action_index(legal_action) for legal_action in state.get_legal_actions(player_id)]
    legal_action_m[legal_action_indexes] = action_m[legal_action_indexes]
    legal_action_m /= np.sum(legal_action_m)
    action_index = np.random.choice(state.get_action_dim(), p = legal_action_m)
    action = state.action_index_to_action(action_index)
    return action

def get_entropy(action_m):
    return np.sum(-np.log(action_m + 1e-20) * action_m) / np.log(action_m.shape[0])

