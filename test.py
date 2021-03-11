from simulator import Simulation
import neat
import os
import pickle
import visualize
from generator import TrafficGenerator
import time
import utils


def test(test_config,genome_path,simulation):
    currentdir = os.getcwd()
    configdir = currentdir +f'/{test_config["neat_config"]}'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)

    genome = pickle.load(open(genome_path , 'rb'))

    tf = TrafficGenerator(test_config['max_steps'], test_config['n_cars'])
    tf.generate_routefile(int(time.time()%1000))

    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
    fitness = simulation.run(net)

    ttl_fitness = simulation.TTL()
    print("loss:", fitness)
    print("time based traffic light system loss: ", ttl_fitness)

if __name__ == '__main__':

    os.environ['PATH'] += "D:\softwares\Graphviz2.38\\bin"

    test_config=utils.testing_configuration('testing_config.ini')

    genome_path = input('Enter path of model you want to test: \n')
    if genome_path[0] == '\"':
        genome_path = genome_path[1:]

    if genome_path[-1] == '\"':
        genome_path = genome_path[:-1]

    s = Simulation(test_config['max_steps'],test_config['n_cars'],test_config['num_states'],
                    test_config['sumocfg_file_name'],test_config['green_duration'],test_config['yellow_duration'],
                    test_config['gui'])
    

    test(test_config,genome_path,s)


