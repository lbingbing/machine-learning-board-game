import tensorflow as tf

from board_game.players.model import Model

class EvaluationNetModel(Model):
    def create_network(self, action_dim):
        self.input_target_V_t = tf.placeholder(dtype = tf.float32, shape = (None, 1))

        self.create_evaluationnet_network()

        self.V_logit_t = tf.layers.dense(inputs = self.evaluationnet_out_t, units = 1)
        self.V_t = tf.nn.tanh(self.V_logit_t)

        self.loss = tf.reduce_mean(tf.square(self.V_t - self.input_target_V_t))
        self.optimizer = tf.train.AdamOptimizer(learning_rate = self.learning_rate).minimize(self.loss)

    def create_evaluationnet_network(self):
        pass

    def train(self, state_m_batch, target_V_m_batch, learning_rate):
        self.sess.run(self.optimizer, feed_dict = {self.input_state_t: state_m_batch, self.input_target_V_t: target_V_m_batch, self.learning_rate: learning_rate})

    def get_V(self, state_m):
        return self.sess.run([self.V_logit_t, self.V_t], feed_dict = {self.input_state_t: state_m})

