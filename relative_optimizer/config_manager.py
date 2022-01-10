import configparser
import random


def training_configuration(config_file):
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {}
    config['gui'] = content['simulation'].getboolean('gui')
    config['max_steps'] = content['simulation'].getint('max_steps')
    config['n_cars'] = content['simulation'].getint('n_cars_generated')
    config['generations'] = content['simulation'].getint('total_episodes')
    config['green_duration'] = content['simulation'].getint('green_duration')
    config['yellow_duration'] = content['simulation'].getint('yellow_duration')
    config['sumocfg_file_name'] = content['dir']['sumocfg_file_name']
    config['neat_config_1'] = '../' + content['dir']['neat_config_1']
    config['neat_config_2'] = '../' + content['dir']['neat_config_2']
    config['neat_config_3'] = '../' + content['dir']['neat_config_3']
    config['num_states'] = content['model'].getint('num_states')
    config['actions'] = content['model'].getint('actions')
    config['checkpoint'] = content['model'].getint('checkpoint')
    config['starvation_penalty'] = content['simulation'].getfloat(
        'starvation_penalty')

    return config


TRAINING_CONFIG = training_configuration(
    '/home/kunal/Desktop/college/major_project/Smart-TrafficLight-System/config/training_config.ini')
