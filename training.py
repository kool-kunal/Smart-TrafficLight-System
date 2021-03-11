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
    best_genome_id = None
    tf = TrafficGenerator(400, 100)
    tf.generate_routefile(int(time.time()%1000))
    
    for _, genome in genomes:
        
        net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
        genome.fitness = Simulation().run(net, False)
        if genome.fitness > curr_max_fitness :
            curr_max_fitness = genome.fitness
            best_genome = genome
            best_genome_id = _
            
        
        print(f"#{_}", genome.fitness)
        
    if f'{best_genome_id}' not in os.listdir("models"):
        try:
            os.makedirs(f"models\\{best_genome_id}")
        except:
            pass
    f = open(f"models\\{best_genome_id}\\genome.k", "wb")
    visualize.draw_net(config, best_genome, False, filename=f"models\\{best_genome_id}\\net")
    pickle.dump(best_genome, f)
    f.close()
        
        
    

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
    