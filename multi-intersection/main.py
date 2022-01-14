import simulation
import pickle
import neat

MAX_STEPS = 3000
N_CARS = 300
NUM_STATES = 40
SUMO_CONFIG_FILE_NAME = 'sumo_config.sumocfg'
GREEN_DURATION = 15
YELLOW_DURATION = 3
GUI = True

simulator = simulation.ModelSimulation(
    MAX_STEPS, N_CARS, NUM_STATES, SUMO_CONFIG_FILE_NAME, GREEN_DURATION, YELLOW_DURATION, GUI)

genome = pickle.load(open(
    '/home/kunal/Desktop/college/major_project/Smart-TrafficLight-System/winner.p', 'rb'))

config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, '/home/kunal/Desktop/college/major_project/Smart-TrafficLight-System/multi-intersection/config/config-feedforward.txt')


net = neat.nn.FeedForwardNetworknet = neat.nn.feed_forward.FeedForwardNetwork.create(
    genome, config)
simulator.run(net)
