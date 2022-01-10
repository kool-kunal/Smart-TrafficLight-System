import neat
from neat import genome
from neat.population import Population


class RelativeOptimizer:


    def _getbestgenome(self, population):
        best_genome = None
        for genome in population:
            if genome == None or genome.fitness == None:
                continue
            if best_genome == None or best_genome.fitness < genome.fitness:
                best_genome = genome

        if best_genome == None:
            best_genome = population[0]

        return best_genome

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