from multiprocessing import Pool
import utils

class CustomParallelEvaluator(object):

    def __init__(self, num_workers, eval_function, timeout=None):
            """
            eval_function should take one argument, a tuple of
            (genome object, config object), and return
            a single float (the genome's fitness).
            """
            self.num_workers = num_workers
            self.eval_function = eval_function
            self.timeout = timeout
            self.pool = Pool(num_workers)
            self._program_config = utils.training_configuration('config/training_config.ini')

    def __del__(self):
            self.pool.close() # should this be terminate?
            self.pool.join()

    def evaluate(self, genomes, config):
            jobs = []
            for ignored_genome_id, genome in genomes:
                jobs.append(self.pool.apply_async(self.eval_function, (genome, config,self._program_config)))

            # assign the fitness back to each genome
            for job, (ignored_genome_id, genome) in zip(jobs, genomes):
                genome.fitness = job.get(timeout=self.timeout)
