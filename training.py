import os
import neat
from simulator import Simulation

def simulation(genomes, config):
    for genomeId, genome in genomes:
        
        net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
        
        genome.fitness = Simulation().run(net)
        print(genome.fitness)
    

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    checkpoint = neat.Checkpointer(10)
    p.add_reporter(checkpoint)
    
    p.run(simulation,5)
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(local_dir, "config")
    config_path = os.path.join(config_dir, "config-feedforward.txt")
    run(config_path)
    