import neat
from neat import genome
from neat.population import Population


class RelativeOptimizer:

    def __init__(self, config) -> None:
        self.input_keys = config.genome_config.input_keys
        self.output_keys = config.genome_config.output_keys
        self.config = config

    def optimize(self, population, best_genome=None):

        best_genome = self._getbestgenome(
            population=population) if best_genome is None else best_genome
        # print(best_genome.connections)

        self._backpropogate(best_genome, population[1])
        # network = neat.nn.FeedForwardNetwork.create(best_genome, config)
        # for t in network.node_evals:
        #     for y in t:
        #         print("   ", y)
        #     print()

    def _backpropogate(self, best_genome, genome):
        loss = self._getloss(best_genome=best_genome, genome=genome)

        layers = self._getNodes(genome.connections)

        d_bias = {}
        d_weight = {}

        for layer in layers:
            for node in layer:
                bias = genome.nodes[node].bias
                activation_function = genome.nodes[node].activation

                weight = dict((key, genome.connections[key].weight)
                              for key in genome.connections if key[1] == node)
                print('node', node)
                print('activation', activation_function)
                print('weights', weight)
                print('bias', bias)
                print()

    def _getbestgenome(self, population):
        best_genome = None
        for id, genome in population.items():
            if genome == None or genome.fitness == None:
                continue
            if best_genome == None or best_genome.fitness < genome.fitness:
                best_genome = genome

        if best_genome == None:
            best_genome = population[1]

        return best_genome

    def _getloss(self, best_genome, genome, loss_function='squared_distance'):
        if loss_function == 'mean_squared_distance':
            if best_genome.fitness is None or genome.fitness is None:
                return 0

            return (best_genome.fitness - genome.fitness)**2
        else:
            return 0

    def _getNodes(self, connections):
        s = set(self.output_keys)

        layers = [s]
        while True:
            c = set(a for (a, b) in connections if b in s and a not in s)
            t = set()
            for n in c:
                if n not in self.input_keys and all(b in s for (a, b) in connections if a == n):
                    t.add(n)

            if not t:
                break

            layers.append(t)
            s = s.union(t)

        return layers
