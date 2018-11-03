import tensorflow as tf
import numpy as np

class PolicyValueNetModel:
    def __init__(self, board_shape, action_dim, model_name):
        self.model_path = model_name + '/model'

        self.graph = tf.Graph()
        with self.graph.as_default():
            self.input_state_t = tf.placeholder(dtype = tf.float32, shape = (None, board_shape[0], board_shape[1], 2))

            self.input_target_P_t = tf.placeholder(dtype = tf.float32, shape = (None, action_dim))
            self.input_target_V_t = tf.placeholder(dtype = tf.float32, shape = (None, 1))

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
            self.P_logits_t = tf.layers.dense(inputs = dense_t, units = action_dim)
            self.P_t = tf.nn.softmax(logits = self.P_logits_t)

            dense_t = tf.layers.dense(inputs = flatten_t, units = action_dim, activation = tf.nn.relu)
            dense_t = tf.layers.dense(inputs = dense_t, units = action_dim, activation = tf.nn.relu)
            self.V_logit_t = tf.layers.dense(inputs = dense_t, units = 1)
            self.V_t = tf.nn.tanh(self.V_logit_t)

            self.value_loss = tf.reduce_mean(tf.square(self.V_t - self.input_target_V_t))
            self.policy_loss = -tf.reduce_mean(tf.reduce_sum(self.input_target_P_t * tf.log(self.P_t + 1e-20), axis = -1))
            self.l2_loss = 0.0001 * tf.add_n([tf.nn.l2_loss(v) for v in tf.trainable_variables() if 'bias' not in v.name])
            self.loss = self.value_loss + self.policy_loss + self.l2_loss
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

    def evaluate(self, state_m):
        P_logits_m, Ps_m, V_logit_m, V_m = self.sess.run([self.P_logits_t, self.P_t, self.V_logit_t, self.V_t], feed_dict = {self.input_state_t: state_m})
        return P_logits_m, Ps_m.reshape(-1), np.asscalar(V_logit_m), np.asscalar(V_m)

    def train(self, state_m_batch, target_P_m_batch, target_V_m_batch, learning_rate):
        loss, value_loss, policy_loss, l2_loss, _ = self.sess.run([self.loss, self.value_loss, self.policy_loss, self.l2_loss, self.optimizer], feed_dict = {self.input_state_t: state_m_batch, self.input_target_P_t: target_P_m_batch, self.input_target_V_t: target_V_m_batch, self.learning_rate: learning_rate})
        return loss, value_loss, policy_loss, l2_loss

def get_entropy(Ps_m):
    return np.sum(-np.log(Ps_m + 1e-20) * Ps_m) / np.log(Ps_m.shape[0])

