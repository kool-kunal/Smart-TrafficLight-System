from simulator import Simulation
import neat
import os
import pickle
import visualize

os.environ['PATH'] += "D:\softwares\Graphviz2.38\\bin"

# s = Simulation().TTL()
# print(s)



def test(genome, config):
    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
    s = Simulation().run(net, True)
    

currentdir = os.getcwd()
configdir = currentdir +'\\config' + '\\config-feedforward.txt'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)
genome  = pickle.load(open(currentdir + '\\winner.p', 'rb'))
#visualize.draw_net(config, genome, True)
genome = pickle.load(open(currentdir + '\\' + 'winner.p' , 'rb'))
#test(genome, config)
print(genome)


