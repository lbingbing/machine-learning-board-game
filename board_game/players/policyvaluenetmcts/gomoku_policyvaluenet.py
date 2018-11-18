import tensorflow as tf

from .policyvaluenet import PolicyValueNetModel

class GomokuPolicyValueNetModel(PolicyValueNetModel):
    def create_policyvaluenet_conv_network(self):
        conv_t = tf.layers.conv2d(inputs = self.input_state_t, filters = 16, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
        conv_t = tf.layers.conv2d(inputs = conv_t, filters = 32, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
        conv_t = tf.layers.conv2d(inputs = conv_t, filters = 64, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
        conv_t = tf.layers.conv2d(inputs = conv_t, filters = 128, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
        conv_t = tf.layers.conv2d(inputs = conv_t, filters = 256, kernel_size = (3, 3), padding = 'same', activation = tf.nn.relu)
        self.policyvaluenet_conv_out_t = tf.layers.flatten(inputs = conv_t)

    def create_policyvaluenet_P_network(self):
        dense_t = tf.layers.dense(inputs = self.policyvaluenet_conv_out_t, units = 81, activation = tf.nn.relu)
        self.policyvaluenet_P_out_t = tf.layers.dense(inputs = dense_t, units = 81, activation = tf.nn.relu)

    def create_policyvaluenet_V_network(self):
        dense_t = tf.layers.dense(inputs = self.policyvaluenet_conv_out_t, units = 81, activation = tf.nn.relu)
        self.policyvaluenet_V_out_t = tf.layers.dense(inputs = dense_t, units = 81, activation = tf.nn.relu)

    def get_l2_loss_factor(self):
        return 0.0001

