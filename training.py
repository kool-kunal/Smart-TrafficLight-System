import os
import neat
from simulator import Simulation
from generator import TrafficGenerator
import time
import pickle
import visualize
import utils


GEN = 0
program_config = None

def simulation(genomes, config):
    curr_max_fitness = -1000000000000.0
    best_genome = None
    global program_config
    tf = TrafficGenerator(program_config['max_steps'], program_config['n_cars'])
    tf.generate_routefile(int(time.time()%1000))
    global GEN
    GEN += 1
    
    for _, genome in genomes:
        
        net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
        s=Simulation(program_config['max_steps'],program_config['n_cars'],program_config['num_states'],
                    program_config['sumocfg_file_name'],program_config['green_duration'],program_config['yellow_duration'],
                    program_config['gui'])
        genome.fitness = s.run(net)
        if genome.fitness > curr_max_fitness :
            curr_max_fitness = genome.fitness
            best_genome = genome
            
        
        print(f"#{_}", genome.fitness)
        
    if f'{GEN}' not in os.listdir("models"):
        try:
            os.makedirs(f"models\\{GEN}")
        except:
            pass
    f = open(f"models\\{GEN}\\genome.k", "wb")
    visualize.draw_net(config, best_genome, False, filename=f"models\\{GEN}\\net")
    pickle.dump(best_genome, f)
    f.close()
        
        
    

def run():
    
    global program_config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, program_config['neat_config'])
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(simulation,program_config['generations'])
    
    print(winner)
    f = open('winner.p', 'wb')
    pickle.dump(winner, f)
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    
if __name__ == "__main__":
    program_config = utils.training_configuration('config/training_config.ini')
    run()
    