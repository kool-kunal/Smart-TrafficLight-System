import simulation
import pickle
import neat
from new_generator import TrafficGenerator

MAX_STEPS = 3000
N_CARS = 300
NUM_STATES = 40
SUMO_CONFIG_FILE_NAME = 'sumo_config.sumocfg'
NEAT_CONFIG_FILE_PATH =  'config/config-feedforward.txt'
TEST_MODEL_PATH = '/home/kunal/Desktop/college/major_project/Smart-TrafficLight-System/winner.p'
GREEN_DURATION = 15
YELLOW_DURATION = 3
TEST_RUNS = 2
GUI = False

def run_test(simulator : simulation.ModelSimulation,net):
    results = {}

    results['net'] = simulator.run_test_net(net)
    results['ttl'] = simulator.run_test_ttl()

    return results
    
if __name__ == "__main__":
    simulator = simulation.ModelSimulation(
        MAX_STEPS, N_CARS, NUM_STATES, SUMO_CONFIG_FILE_NAME, GREEN_DURATION, YELLOW_DURATION, GUI)

    genome = pickle.load(open(
        TEST_MODEL_PATH, 'rb'))

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, NEAT_CONFIG_FILE_PATH)

    net = neat.nn.FeedForwardNetworknet = neat.nn.feed_forward.FeedForwardNetwork.create(
        genome, config)
    
    generator = TrafficGenerator(MAX_STEPS,N_CARS)

    results = {}

    for i in range(TEST_RUNS):
        generator.generate_routefile(i)
        result = run_test(simulator,net)
        results[i+1] = result

    for key, value in results.items():
        print('=======TEST %i======='%key)
        print('net              ttl')

        for net_v, ttl_v in zip(value['net'], value['ttl']):
            print("%.2f           %.2f"% (net_v, ttl_v))

        print('\n')
