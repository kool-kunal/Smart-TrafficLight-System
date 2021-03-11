from simulator import Simulation
import neat
import os
import pickle
import visualize
from generator import TrafficGenerator
import time

os.environ['PATH'] += "D:\softwares\Graphviz2.38\\bin"

# s = Simulation().TTL()
# print(s)



def test(genome, config):
    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
    s = Simulation().run(net, True)
    return s
    

genome_path = input()
if genome_path[0] == '\"':
    genome_path = genome_path[1:]

if genome_path[-1] == '\"':
    genome_path = genome_path[:-1]

currentdir = os.getcwd()
configdir = currentdir +'\\config' + '\\config-feedforward.txt'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)
#genome  = pickle.load(open(currentdir + '\\winner.p', 'rb'))
#visualize.draw_net(config, genome, True)
genome = pickle.load(open(genome_path , 'rb'))
tf = TrafficGenerator(400, 100)
tf.generate_routefile(int(time.time()%1000))
fitness = test(genome, config)
ttl_fitness = Simulation().TTL()
print("loss:", fitness)
print("time based traffic light system loss: ", ttl_fitness)




