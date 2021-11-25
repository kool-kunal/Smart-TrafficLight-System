import os
import pickle
import time

import matplotlib.pyplot as plt
import neat

import utils
import visualize
from generator import TrafficGenerator
from simulator import Approach1, Approach2, TimeBasedTrafficLigthSystem


def test_with_model(episode,test_config,genome_path_1,genome_path_2):
    currentdir = os.getcwd()
    configdir = currentdir + f'/{test_config["neat_config_1"]}'
    config_1 = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)

    tf = TrafficGenerator(test_config['max_steps'], test_config['n_cars'])
    tf.generate_routefile(int(time.time() % 1000))

    genome_1 = pickle.load(open(genome_path_1, 'rb'))
    net_1 = neat.nn.feed_forward.FeedForwardNetwork.create(genome_1, config_1)

    s_1 = Approach1(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                   test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                   test_config['gui'], genome_id= genome_1.key)
    fitness_1 = s_1.run_test(net_1)

    config_2 = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, currentdir + f'/{test_config["neat_config_2"]}' )
    genome_2 = pickle.load(open(genome_path_2, 'rb'))
    net_2 = neat.nn.feed_forward.FeedForwardNetwork.create(genome_2, config_2)

    s_2 = Approach2(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                   test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                   test_config['gui'], genome_id= genome_2.key)
    fitness_2 = s_2.run_test(net_2)

    print(f"Episode {episode} Approach 1 loss:", fitness_1)
    print(
        f"Episode {episode} Approach 2 loss: ", fitness_2)

    return fitness_1,fitness_2

def test_with_ttl(episode, test_config, genome_path):
    currentdir = os.getcwd()
    configdir = currentdir + f'/{test_config["neat_config_2"]}'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)

    genome = pickle.load(open(genome_path, 'rb'))

    tf = TrafficGenerator(test_config['max_steps'], test_config['n_cars'])
    tf.generate_routefile(int(time.time() % 1000))

    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome, config)
    print(net)
    print(genome)
    s = Approach2(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                   test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                   test_config['gui'], genome_id= genome.key)
    fitness = s.run(net)

    s = TimeBasedTrafficLigthSystem(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                   test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                   test_config['gui'], genome_id= genome.key)
    ttl_fitness = s.run_test()

    print(f"Episode {episode} loss:", fitness)
    print(
        f"Episode {episode} time based traffic light system loss: ", ttl_fitness)
    return fitness, ttl_fitness


if __name__ == '__main__':

    #os.environ['PATH'] += "D:\softwares\Graphviz2.38\\bin"

    test_config = utils.testing_configuration('config/testing_config.ini')

    genome_path = input('Enter path of Approach 1 you want to test: \n')
    if genome_path[0] == '\"' or genome_path[0] == '\'':
        genome_path = genome_path[1:]

    if genome_path[-1] == '\"' or genome_path[-1] == '\'':
        genome_path = genome_path[:-1]

    test_runs = test_config['test_runs']

    model_fitness = []
    ttl_fitness = []
    x = range(test_runs)

    with_ttl = test_config['with_ttl']

    if with_ttl:
        for _ in range(test_runs):
            fitness, ttl_fitness_ = test_with_ttl(_, test_config, genome_path)
            model_fitness.append(-fitness)
            ttl_fitness.append(-ttl_fitness_)

        visualize.bar_graph_plot(model_loss=model_fitness, ttl_loss=ttl_fitness)
        visualize.pi_chart_plot(model_loss=model_fitness, ttl_loss=ttl_fitness)

    else:
        genome_path2 = input('Enter path of Approach 2 model you want to test: \n')
        if genome_path2[0] == '\"' or genome_path2[0] == '\'':
            genome_path2 = genome_path2[1:]

        if genome_path2[-1] == '\"' or genome_path2[-1] == '\'':
            genome_path2 = genome_path2[:-1]

        model_2_fitness= []

        for _ in range(test_runs):
            fitness_1, fitness_2 = test_with_model(_, test_config, genome_path,genome_path2)
            model_fitness.append(-fitness_1)
            model_2_fitness.append(-fitness_2)

        visualize.bar_graph_plot(model_loss=model_fitness, ttl_loss=model_2_fitness)
        visualize.pi_chart_plot(model_loss=model_fitness, ttl_loss=model_2_fitness)
        
    # plt.bar(x,model_fitness,label="Model Fitness",color="blue")
    # plt.bar(x,ttl_fitness,label="TTL_Fitness",color="red")
    # plt.ylabel('Loss')
    # plt.xlabel('Episodes')
    # plt.legend()
    # plt.show()
