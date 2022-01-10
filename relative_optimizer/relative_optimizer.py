import neat
from neat import genome
from neat.population import Population


class RelativeOptimizer:

    def optimize(self, population, config):
        species = population.species
        generation = population.generation
        population = population.population

        genome = population[1]
        print(genome.fitness)

        network = neat.nn.FeedForwardNetwork.create(genome, config)
        for t in network.node_evals:
            for y in t:
                print("   ", y)
            print()