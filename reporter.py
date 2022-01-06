from __future__ import division, print_function

import time

from neat.math_util import mean, stdev
from neat.six_util import itervalues, iterkeys
import os
from config_manager import TRAINING_CONFIG
import utils
from generator import TrafficGenerator
import pickle
import random


class ReporterSet(object):
    def __init__(self):
        self.reporters = []

    def add(self, reporter):
        self.reporters.append(reporter)

    def remove(self, reporter):
        self.reporters.remove(reporter)

    def start_generation(self, gen):
        for r in self.reporters:
            r.start_generation(gen)

    def end_generation(self, config, population, species_set):
        for r in self.reporters:
            r.end_generation(config, population, species_set)

    def post_evaluate(self, config, population, species, best_genome):
        for r in self.reporters:
            r.post_evaluate(config, population, species, best_genome)

    def post_reproduction(self, config, population, species):
        for r in self.reporters:
            r.post_reproduction(config, population, species)

    def complete_extinction(self):
        for r in self.reporters:
            r.complete_extinction()

    def found_solution(self, config, generation, best):
        for r in self.reporters:
            r.found_solution(config, generation, best)

    def species_stagnant(self, sid, species):
        for r in self.reporters:
            r.species_stagnant(sid, species)

    def info(self, msg):
        for r in self.reporters:
            r.info(msg)


class BaseReporter(object):

    def start_generation(self, generation):
        pass

    def end_generation(self, config, population, species_set):
        pass

    def post_evaluate(self, config, population, species, best_genome):
        pass

    def post_reproduction(self, config, population, species):
        pass

    def complete_extinction(self):
        pass

    def found_solution(self, config, generation, best):
        pass

    def species_stagnant(self, sid, species):
        pass

    def info(self, msg):
        pass


class CustomReporter(BaseReporter):
    """Uses `print` to output information about the run; an example reporter class."""

    def __init__(self, show_species_detail, training_continued, is_random_density):
        self.show_species_detail = show_species_detail
        self.generation = None
        self.generation_start_time = None
        self.generation_times = []
        self.num_extinctions = 0
        self.file_name = None
        self.data = []
        if not os.path.exists('training'):
            os.mkdir('training')
        files = os.listdir('training')
        count = 0
        if len(files) > 0:
            count = int(sorted(files)[-1].split('-')[-1].split('.')[0])
            if not training_continued:
                count += 1

        self.file_name = f'training/trainingInfo-{count}.txt'
        self.program_config = TRAINING_CONFIG
        self.random_density = is_random_density

    def start_generation(self, generation):

        if self.random_density:
            TRAINING_CONFIG['n_cars'] = random.randint(50, 200)

        print(self.program_config['n_cars'])

        tf = TrafficGenerator(
            self.program_config['max_steps'], self.program_config['n_cars'])
        new_list = tf.generate_routefile(int(time.time() % 1000))

        self.generation = generation
        print('\n ****** Running generation {0} ****** \n'.format(generation))
        self.generation_start_time = time.time()

    def end_generation(self, config, population, species_set):
        ng = len(population)
        ns = len(species_set.species)
        if self.show_species_detail:
            print(
                'Population of {0:d} members in {1:d} species:'.format(ng, ns))
            sids = list(iterkeys(species_set.species))
            sids.sort()
            print("   ID   age  size  fitness  adj fit  stag")
            print("  ====  ===  ====  =======  =======  ====")
            for sid in sids:
                s = species_set.species[sid]
                a = self.generation - s.created
                n = len(s.members)
                f = "--" if s.fitness is None else "{:.1f}".format(s.fitness)
                af = "--" if s.adjusted_fitness is None else "{:.3f}".format(
                    s.adjusted_fitness)
                st = self.generation - s.last_improved
                print(
                    "  {: >4}  {: >3}  {: >4}  {: >7}  {: >7}  {: >4}".format(sid, a, n, f, af, st))
        else:
            print(
                'Population of {0:d} members in {1:d} species'.format(ng, ns))

        elapsed = time.time() - self.generation_start_time
        self.generation_times.append(elapsed)
        self.generation_times = self.generation_times[-10:]
        average = sum(self.generation_times) / len(self.generation_times)
        print('Total extinctions: {0:d}'.format(self.num_extinctions))
        if len(self.generation_times) > 1:
            print("Generation time: {0:.3f} sec ({1:.3f} average)".format(
                elapsed, average))
        else:
            print("Generation time: {0:.3f} sec".format(elapsed))

    def post_evaluate(self, config, population, species, best_genome):
        # pylint: disable=no-self-use
        fitnesses = [c.fitness for c in itervalues(population)]
        fit_mean = mean(fitnesses)
        fit_std = stdev(fitnesses)
        best_species_id = species.get_species_id(best_genome.key)
        print('Population\'s average fitness: {0:3.5f} stdev: {1:3.5f}'.format(
            fit_mean, fit_std))
        print(
            'Best fitness: {0:3.5f} - size: {1!r} - species {2} - id {3}'.format(best_genome.fitness,
                                                                                 best_genome.size(),
                                                                                 best_species_id,
                                                                                 best_genome.key))
        if self.random_density:
            self.data.append(
                'Gen={},Mean={},StdDev={},Best={},Cars={}'.format(self.generation, fit_mean, fit_std, best_genome.fitness, self.program_config['n_cars']))
        else:
            self.data.append(
                f'Gen={self.generation},Mean={fit_mean},StdDev={fit_std},Best={best_genome.fitness}')

        if(self.generation != 0 and self.generation % self.program_config['checkpoint'] == self.program_config['checkpoint']-1):
            with open(self.file_name, 'a') as trainingInfo:
                for d in self.data:
                    print(d, file=trainingInfo)
            self.data = []

        f = open('winner.p', 'wb')
        pickle.dump(best_genome, f)
        f.close()

    def complete_extinction(self):
        self.num_extinctions += 1
        print('All species extinct.')

    def found_solution(self, config, generation, best):
        print('\nBest individual in generation {0} meets fitness threshold - complexity: {1!r}'.format(
            self.generation, best.size()))

    def species_stagnant(self, sid, species):
        if self.show_species_detail:
            print("\nSpecies {0} with {1} members is stagnated: removing it".format(
                sid, len(species.members)))

    def info(self, msg):
        print(msg)
