import simulator
import neat
import pickle
from generator import TrafficGenerator
import json
import os
from visualize import generate_test_plots

MAX_STEPS = 600
N_CARS = 50
NUM_STATES = 40
SUMO_CONFIG_FILE_NAME = 'sumo_config.sumocfg'
NEAT_CONFIG_FILE_PATH = 'config/config-feedforward_1.txt'
TEST_MODEL_PATH = 'winner_1110.p'
GREEN_DURATION = 15
YELLOW_DURATION = 3
TEST_RUNS = 1
GUI = True


def run_test(net):
    results = {}

    net_simulator = simulator.Approach1(
        MAX_STEPS, N_CARS, NUM_STATES, SUMO_CONFIG_FILE_NAME, GREEN_DURATION, YELLOW_DURATION, GUI, 1)
    ttl_simulator = simulator.TimeBasedTrafficLigthSystem(
        MAX_STEPS, N_CARS, NUM_STATES, SUMO_CONFIG_FILE_NAME, GREEN_DURATION, YELLOW_DURATION, GUI, 1)

    results['net'] = net_simulator.run_test(net)
    results['ttl'] = ttl_simulator.run_test()

    return results


def print_result(results):
    print("{:<15} {:<8} {:<10} {:<10} {:<8} {:<8}".format(
        'Test run', 'Model', 'RMS_LOSS', 'HM_LOSS', 'AQL', 'AWT'))
    print("------------------------------------------------------------")
    for i in range(len(results)):
        print(f"{i+1:<15} {'net':<8} {results[i+1]['net']['RMS_WAITING_TIME_LOSS']:<10.3f} {results[i+1]['net']['HARMONIC_MEAN_LOSS']:<10.3f} {results[i+1]['net']['AVERAGE QUEUE LENGTH']:<8.3f} {results[i+1]['net']['AVERAGE WAITING TIME']:<8.3f}")
        print(f"{i+1:<15} {'ttl':<8} {results[i+1]['ttl']['RMS_WAITING_TIME_LOSS']:<10.3f} {results[i+1]['ttl']['HARMONIC_MEAN_LOSS']:<10.3f} {results[i+1]['ttl']['AVERAGE QUEUE LENGTH']:<8.3f} {results[i+1]['ttl']['AVERAGE WAITING TIME']:<8.3f}")


def allocate_new_dir(folder_name):
    if 'test_results' not in os.listdir():
        os.mkdir('test_results')
    new_dir_path = 'test_results/' + folder_name
    if folder_name not in os.listdir('test_results'):
        os.mkdir(new_dir_path)
    return new_dir_path


if __name__ == "__main__":

    genome = pickle.load(open(
        TEST_MODEL_PATH, 'rb'))

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, NEAT_CONFIG_FILE_PATH)

    net = neat.nn.FeedForwardNetworknet = neat.nn.feed_forward.FeedForwardNetwork.create(
        genome, config)

    #generator = TrafficGenerator(MAX_STEPS, N_CARS)

    results = {}

    parameters = ['RMS_WAITING_TIME_FITNESS', 'HARMONIC_MEAN_FITNESS',
                  'AVERAGE_QUEUE_LENGTH', 'AVERAGE_WAITING_TIME']

    for i in range(TEST_RUNS):
        # generator.generate_routefile(i)
        result = run_test(net)
        results[i+1] = result

    print('\n\n')
    print_result(results)

    # new_dir_path = allocate_new_dir('car_50_ttl_120')

    # with open(new_dir_path + "/test_results.json", "w") as test:
    #     json.dump(results, test, indent=4)

    # generate_test_plots(new_dir_path)
