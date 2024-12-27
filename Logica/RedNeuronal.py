import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Inicialización de pesos y sesgos
        self.weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))
        self.bias_hidden = np.random.uniform(-1, 1, (hidden_size,))
        self.bias_output = np.random.uniform(-1, 1, (output_size,))

    def forward(self, inputs):
        # Capa oculta
        hidden_layer = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden_layer = self.sigmoid(hidden_layer)
        
        # Capa de salida
        output_layer = np.dot(hidden_layer, self.weights_hidden_output) + self.bias_output
        output_layer = self.softmax(output_layer)
        return output_layer

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))  # Evita overflow numérico
        return exp_x / exp_x.sum(axis=0)
