import simulation
import pickle
import neat
from traffic_generator import TrafficGenerator
import json
import os
from visualise import generate_test_plots

MAX_STEPS = 3000
N_CARS = 200
NUM_STATES = 40
SUMO_CONFIG_FILE_NAME = 'sumo_config.sumocfg'
NEAT_CONFIG_FILE_PATH = 'config/config-feedforward.txt'
TEST_MODEL_PATH = 'C:/Users/karti/Desktop/New_Training/Smart-TrafficLight-System/checkpoints/training_with_avg_waiting_time_only/winner_1110.p'
GREEN_DURATION = 15
YELLOW_DURATION = 3
TEST_RUNS = 100
GUI = False


def run_test(net):
    results = {}

    simulator = simulation.ModelSimulation(
        MAX_STEPS, N_CARS, NUM_STATES, SUMO_CONFIG_FILE_NAME, GREEN_DURATION, YELLOW_DURATION, GUI)

    results['net'] = simulator.run_test_net(net)
    results['ttl'] = simulator.run_test_ttl()

    return results


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

    generator = TrafficGenerator(MAX_STEPS, N_CARS)

    results = {}

    parameters = ['RMS_WAITING_TIME_FITNESS', 'HARMONIC_MEAN_FITNESS',
                  'AVERAGE_QUEUE_LENGTH', 'AVERAGE_WAITING_TIME']

    for i in range(TEST_RUNS):
        generator.generate_routefile(i)
        result = run_test(net)
        results[i+1] = result

    new_dir_path = allocate_new_dir('car_200_ttl_120')

    with open(new_dir_path + "/test_results.json", "w") as test:
        json.dump(results, test, indent=4)

    generate_test_plots(new_dir_path)
