import neat
from relative_optimizer import  RelativeOptimizer
from config_manager import TRAINING_CONFIG

program_config = TRAINING_CONFIG
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, program_config['neat_config_1'])
p = neat.Population(config)
optimizer = RelativeOptimizer()

optimizer.optimize(p, config)
