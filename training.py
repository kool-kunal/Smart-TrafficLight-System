import os
import neat
from simulator import Simulation
from generator import TrafficGenerator
import time
import pickle
import visualize

def simulation(genomes, config):
    curr_max_fitness = -1000000000000.0
    best_genome = None
    
    tf = TrafficGenerator(400, 100)
    tf.generate_routefile(int(time.time()%1000))
    
    for _, genome in genomes:
        
        net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
        genome.fitness = Simulation().run(net, False)
        if genome.fitness > curr_max_fitness :
            curr_max_fitness = genome.fitness
            best_genome = genome
            
        if genome.fitness > -27:
            os.makedirs(f"models\\reward{genome.fitness}")
            f = open(f"models\\reward{genome.fitness}\\{_}.k", "wb")
            visualize.draw_net(config, genome, True, filename=f"models\\reward{genome.fitness}\\net.gv.svg")
            pickle.dump(genome, f)
        
        print(f"#{_}", genome.fitness)
    
    # net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    # print(Simulation().run(net, True))
        
        
    

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #checkpoint = neat.Checkpointer(10)
    #p.add_reporter(checkpoint)
    
    winner = p.run(simulation,100)
    
    print(winner)
    f = open('winner.p', 'wb')
    pickle.dump(winner, f)
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_dir = os.path.join(local_dir, "config")
    config_path = os.path.join(config_dir, "config-feedforward.txt")
    run(config_path)
    