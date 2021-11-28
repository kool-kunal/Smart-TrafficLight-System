import os
import pickle
import time

import matplotlib.pyplot as plt
import neat

import utils
import visualize
from generator import TrafficGenerator
from simulator import Approach1, Approach2, TimeBasedTrafficLigthSystem


def test_with_model(episode, test_config, genome_path_1, genome_path_2):
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
                    test_config['gui'], genome_id=genome_1.key)
    fitness, avg_waiting_time, avg_queue_length = s_1.run_test(net_1)

    approach1_data = {'rms': fitness, 'avg_waiting_time': avg_waiting_time,
                      'avg_queue_length': avg_queue_length}

    config_2 = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation, currentdir + f'/{test_config["neat_config_2"]}')
    genome_2 = pickle.load(open(genome_path_2, 'rb'))
    net_2 = neat.nn.feed_forward.FeedForwardNetwork.create(genome_2, config_2)

    s_2 = Approach2(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                    test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                    test_config['gui'], genome_id=genome_2.key)
    fitness, avg_waiting_time, avg_queue_length = s_2.run_test(net_2)

    approach2_data = {'rms': fitness, 'avg_waiting_time': avg_waiting_time,
                      'avg_queue_length': avg_queue_length}

    print(f"Episode {episode} Approach 1 loss:", approach1_data['rms'])
    print(
        f"Episode {episode} Approach 2 loss: ", approach2_data['rms'])

    return approach1_data, approach2_data


def test_with_ttl(episode, test_config, genome_path):
    currentdir = os.getcwd()
    configdir = currentdir + f'/{test_config["neat_config_1"]}'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)

    genome = pickle.load(open(genome_path, 'rb'))

    tf = TrafficGenerator(test_config['max_steps'], test_config['n_cars'])
    tf.generate_routefile(int(time.time() % 1000))

    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome, config)
    s = Approach1(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                  test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                  test_config['gui'], genome_id=genome.key)
    fitness, avg_waiting_time, avg_queue_length = s.run_test(net)

    approach1_data = {'rms': fitness, 'avg_waiting_time': avg_waiting_time,
                      'avg_queue_length': avg_queue_length}

    s = TimeBasedTrafficLigthSystem(test_config['max_steps'], test_config['n_cars'], test_config['num_states'],
                                    test_config['sumocfg_file_name'], test_config['green_duration'], test_config['yellow_duration'],
                                    test_config['gui'], genome_id=genome.key)
    fitness, avg_waiting_time, avg_queue_length = s.run_test()

    ttl_data = {'rms': fitness, 'avg_waiting_time': avg_waiting_time,
                'avg_queue_length': avg_queue_length}

    print(f"Episode {episode} loss:", approach1_data['rms'])
    print(
        f"Episode {episode} time based traffic light system loss: ", ttl_data['rms'])
    return approach1_data, ttl_data


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
    model_waiting_time = []
    model_queue_length = []
    x = range(test_runs)

    with_ttl = test_config['with_ttl']

    approach1_count = 0

    if with_ttl:

        ttl_fitness = []
        ttl_waiting_time = []
        ttl_queue_length = []

        for _ in range(test_runs):
            approach1_data, ttl_data = test_with_ttl(
                _, test_config, genome_path)
            model_fitness.append(-approach1_data['rms'])
            model_waiting_time.append(-approach1_data['avg_waiting_time'])
            model_queue_length.append(-approach1_data['avg_queue_length'])
            ttl_fitness.append(-ttl_data['rms'])
            ttl_waiting_time.append(-ttl_data['avg_waiting_time'])
            ttl_queue_length.append(-ttl_data['avg_queue_length'])

            if approach1_data['rms'] > ttl_data['rms']:
                approach1_count += 1

        print('\n----------- testing result -----------')
        print('number of times approach1 did better :', approach1_count,
              '', '', 'percentage = ', f'{(approach1_count/test_runs)*100}%')
        print(f'mean of losses of approach1 over {test_runs} test runs :', sum(
            model_fitness)/test_runs)
        print(f'mean of average waiting times of approach1 over {test_runs} test runs :', sum(
            model_waiting_time)/test_runs)
        print(f'mean of average queue lengths of approach1 over {test_runs} test runs :', sum(
            model_queue_length)/test_runs)
        print()
        print(f'mean of losses of ttls over {test_runs} test runs :', sum(
            ttl_fitness)/test_runs)
        print(f'mean of average waiting times of ttls over {test_runs} test runs :', sum(
            ttl_waiting_time)/test_runs)
        print(f'mean of average queue lengths of ttls over {test_runs} test runs :', sum(
            ttl_queue_length)/test_runs)

        visualize.bar_graph_plot(loss_1=model_fitness, loss_2=ttl_fitness, labels=[
                                 'Approach_1', 'ttl'])
        visualize.pi_chart_plot(loss_1=model_fitness, loss_2=ttl_fitness, labels=[
                                'Approach_1', 'ttl'])

    else:
        genome_path2 = input(
            'Enter path of Approach 2 model you want to test: \n')
        if genome_path2[0] == '\"' or genome_path2[0] == '\'':
            genome_path2 = genome_path2[1:]

        if genome_path2[-1] == '\"' or genome_path2[-1] == '\'':
            genome_path2 = genome_path2[:-1]

        model2_fitness = []
        model2_waiting_time = []
        model2_queue_length = []

        for _ in range(test_runs):
            approach1_data, approach2_data = test_with_model(
                _, test_config, genome_path, genome_path2)
            model_fitness.append(-approach1_data['rms'])
            model_waiting_time.append(-approach1_data['avg_waiting_time'])
            model_queue_length.append(-approach1_data['avg_queue_length'])
            model2_fitness.append(-approach2_data['rms'])
            model2_waiting_time.append(-approach2_data['avg_waiting_time'])
            model2_queue_length.append(-approach2_data['avg_queue_length'])

            if approach1_data['rms'] > approach2_data['rms']:
                approach1_count += 1

        print('\n----------- testing result -----------')
        print('number of times approach1 did better :', approach1_count,
              '', '', 'percentage = ', f'{(approach1_count/test_runs)*100}%')
        print(f'mean of losses of approach1 over {test_runs} test runs :', sum(
            model_fitness)/test_runs)
        print(f'mean of average waiting times of approach1 over {test_runs} test runs :', sum(
            model_waiting_time)/test_runs)
        print(f'mean of average queue lengths of approach1 over {test_runs} test runs :', sum(
            model_queue_length)/test_runs)
        print()
        print('number of times approach2 did better :', approach1_count,
              '', '', 'percentage = ', f'{((test_runs-approach1_count)/test_runs)*100}%')
        print(f'mean of losses of approach2 over {test_runs} test runs :', sum(
            model2_fitness)/test_runs)
        print(f'mean of average waiting times of approach2 over {test_runs} test runs :', sum(
            model2_waiting_time)/test_runs)
        print(f'mean of average queue lengths of approach2 over {test_runs} test runs :', sum(
            model2_queue_length)/test_runs)

        visualize.bar_graph_plot(loss_1=model_fitness, loss_2=model2_fitness, labels=[
                                 'Approach_1', 'Approach_2'])
        visualize.pi_chart_plot(loss_1=model_fitness, loss_2=model2_fitness, labels=[
                                'Approach_1', 'Approach_2'])

    # plt.bar(x,model_fitness,label="Model Fitness",color="blue")
    # plt.bar(x,ttl_fitness,label="TTL_Fitness",color="red")
    # plt.ylabel('Loss')
    # plt.xlabel('Episodes')
    # plt.legend()
    # plt.show()
