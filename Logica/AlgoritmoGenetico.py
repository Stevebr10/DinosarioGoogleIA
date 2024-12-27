
from Logica.RedNeuronal import NeuralNetwork
import numpy as np


class GeneticAlgorithm:
    def __init__(self, population_size):
        self.population = [NeuralNetwork(3, 10, 3) for _ in range(population_size)]

    def evaluate_fitness(self, dinos):
        return [dino.fitness for dino in dinos]

    def select_parents(self, fitness_scores):
        # Selección proporcional al puntaje de aptitud
        total_fitness = sum(fitness_scores)
        probabilities = [score / total_fitness for score in fitness_scores]
        parents = np.random.choice(self.population, size=2, p=probabilities)
        return parents

    def crossover(self, parent1, parent2):
        # Combina los pesos de dos padres para crear un hijo
        child = NeuralNetwork(3, 10, 3)
        child.weights_input_hidden = (parent1.weights_input_hidden + parent2.weights_input_hidden) / 2
        child.weights_hidden_output = (parent1.weights_hidden_output + parent2.weights_hidden_output) / 2
        return child

    def mutate(self, network, mutation_rate=0.1):
        # Aplica mutaciones a los pesos
        if np.random.rand() < mutation_rate:
            network.weights_input_hidden += np.random.uniform(-0.5, 0.5, network.weights_input_hidden.shape)
            network.weights_hidden_output += np.random.uniform(-0.5, 0.5, network.weights_hidden_output.shape)
