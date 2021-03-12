from simulator import Simulation
import neat
import os
import pickle
import visualize
from generator import TrafficGenerator
import time
import utils
import matplotlib.pyplot as plt


def test(episode,test_config,genome_path):
    currentdir = os.getcwd()
    configdir = currentdir +f'/{test_config["neat_config"]}'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)

    genome = pickle.load(open(genome_path , 'rb'))

    tf = TrafficGenerator(test_config['max_steps'], test_config['n_cars'])
    tf.generate_routefile(int(time.time()%1000))

    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)

    s=Simulation(test_config['max_steps'],test_config['n_cars'],test_config['num_states'],
                    test_config['sumocfg_file_name'],test_config['green_duration'],test_config['yellow_duration'],
                    test_config['gui'])
    fitness = s.run(net)

    s=Simulation(test_config['max_steps'],test_config['n_cars'],test_config['num_states'],
                test_config['sumocfg_file_name'],test_config['green_duration'],test_config['yellow_duration'],
                test_config['gui'])
    ttl_fitness = s.TTL()

    print(f"Episode {episode} loss:", fitness)
    print(f"Episode {episode} time based traffic light system loss: ", ttl_fitness)
    return fitness,ttl_fitness

if __name__ == '__main__':

    os.environ['PATH'] += "D:\softwares\Graphviz2.38\\bin"

    test_config=utils.testing_configuration('testing_config.ini')

    genome_path = input('Enter path of model you want to test: \n')
    if genome_path[0] == '\"':
        genome_path = genome_path[1:]

    if genome_path[-1] == '\"':
        genome_path = genome_path[:-1]

    
    test_runs=test_config['test_runs']

    model_fitness=[]
    ttl_fitness=[]
    x=range(test_runs)

    for _ in range(test_runs):
        fitness,ttl_fitness_=test(_,test_config,genome_path)
        model_fitness.append(-fitness)
        ttl_fitness.append(-ttl_fitness_)

    plt.plot(x,model_fitness,label="Model Fitness",color="blue")
    plt.plot(x,ttl_fitness,label="TTL_Fitness",color="red")
    plt.ylabel('Loss')
    plt.xlabel('Episodes')
    plt.legend()
    plt.show()


