import os
import neat
from config_manager import TRAINING_CONFIG
from simulator import Approach1, Approach2, Approach3
from generator import TrafficGenerator
import time
import pickle
import visualize
import utils
import argparse
import reporter
from evaluator import CustomParallelEvaluator

GEN = 0
program_config = None


def simulation_single(genome, config, program_config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    simulator = Approach1(program_config['max_steps'], program_config['n_cars'], program_config['num_states'],
                          program_config['sumocfg_file_name'], program_config['green_duration'], program_config['yellow_duration'],
                          program_config['gui'], genome_id=genome.key, starvation_penalty=program_config['starvation_penalty'])
    genome.fitness = simulator.run(net)
    return genome.fitness


def run(checkpoint=None):
    global program_config
    p = None
    if checkpoint == None:
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation, program_config['neat_config_1'])
        p = neat.Population(config)
    else:
        p = neat.Checkpointer.restore_checkpoint(checkpoint)
        print("loaded population from:", checkpoint)
    p.add_reporter(reporter.CustomReporter(
        True, checkpoint != None, program_config['n_cars']==-1))

    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(
        program_config['checkpoint'], filename_prefix="checkpoints/checkpoint-"))

    pe = CustomParallelEvaluator(8, simulation_single)
    winner = p.run(pe.evaluate, program_config['generations'])

    # winner = p.run(simulation, program_config['generations'])

    # print(winner)
    f = open('winner.p', 'wb')
    pickle.dump(winner, f)
    f.close()
    # visualize.draw_net(config, winner, True)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-load', metavar='-l')
    args = parser.parse_args()
    program_config = TRAINING_CONFIG
    if args.load != None:
        run(args.load)
    else:
        run()
