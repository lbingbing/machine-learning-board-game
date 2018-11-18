import tensorflow as tf
import numpy as np

from board_game.players.model import Model

class PolicyValueNetModel(Model):
    def create_network(self, action_dim):
        self.input_target_P_t = tf.placeholder(dtype = tf.float32, shape = (None, action_dim))
        self.input_target_V_t = tf.placeholder(dtype = tf.float32, shape = (None, 1))

        self.create_policyvaluenet_conv_network()
        self.create_policyvaluenet_P_network()
        self.create_policyvaluenet_V_network()

        self.P_logits_t = tf.layers.dense(inputs = self.policyvaluenet_P_out_t, units = action_dim)
        self.P_t = tf.nn.softmax(logits = self.P_logits_t)

        self.V_logit_t = tf.layers.dense(inputs = self.policyvaluenet_V_out_t, units = 1)
        self.V_t = tf.nn.tanh(self.V_logit_t)

        self.value_loss = tf.reduce_mean(tf.square(self.V_t - self.input_target_V_t))
        self.policy_loss = -tf.reduce_mean(tf.reduce_sum(self.input_target_P_t * tf.log(self.P_t + 1e-20), axis = -1))
        self.l2_loss = self.get_l2_loss_factor() * tf.add_n([tf.nn.l2_loss(v) for v in tf.trainable_variables() if 'bias' not in v.name])
        self.loss = self.value_loss + self.policy_loss + self.l2_loss
        self.optimizer = tf.train.AdamOptimizer(learning_rate = self.learning_rate).minimize(self.loss)

    def create_policyvaluenet_conv_network(self):
        pass

    def create_policyvaluenet_P_network(self):
        pass

    def create_policyvaluenet_V_network(self):
        pass

    def get_l2_loss_factor(self):
        pass

    def train(self, state_m_batch, target_P_m_batch, target_V_m_batch, learning_rate):
        loss, value_loss, policy_loss, l2_loss, _ = self.sess.run([self.loss, self.value_loss, self.policy_loss, self.l2_loss, self.optimizer], feed_dict = {self.input_state_t: state_m_batch, self.input_target_P_t: target_P_m_batch, self.input_target_V_t: target_V_m_batch, self.learning_rate: learning_rate})
        return loss, value_loss, policy_loss, l2_loss

    def evaluate(self, state_m):
        P_logits_m, Ps_m, V_logit_m, V_m = self.sess.run([self.P_logits_t, self.P_t, self.V_logit_t, self.V_t], feed_dict = {self.input_state_t: state_m})
        return P_logits_m, Ps_m.reshape(-1), np.asscalar(V_logit_m), np.asscalar(V_m)

