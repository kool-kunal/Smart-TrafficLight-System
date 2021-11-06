import configparser


def training_configuration(config_file):
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {}
    config['gui']=content['simulation'].getboolean('gui')
    config['max_steps'] = content['simulation'].getint('max_steps')
    config['n_cars'] = content['simulation'].getint('n_cars_generated')
    config['generations'] = content['simulation'].getint('total_episodes')
    config['green_duration'] = content['simulation'].getint('green_duration')
    config['yellow_duration'] = content['simulation'].getint('yellow_duration')
    config['sumocfg_file_name'] = content['dir']['sumocfg_file_name']
    config['neat_config'] = content['dir']['neat_config']
    config['num_states']=content['model'].getint('num_states')
    config['actions']=content['model'].getint('actions')
    config['checkpoint'] = content['model'].getint('checkpoint')

    return config


def testing_configuration(config_file):
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {}
    config['gui']=content['simulation'].getboolean('gui')
    config['max_steps'] = content['simulation'].getint('max_steps')
    config['n_cars'] = content['simulation'].getint('n_cars_generated')
    config['generations'] = content['simulation'].getint('total_episodes')
    config['green_duration'] = content['simulation'].getint('green_duration')
    config['yellow_duration'] = content['simulation'].getint('yellow_duration')
    config['test_runs']=content['simulation'].getint('test_runs')
    config['sumocfg_file_name'] = content['dir']['sumocfg_file_name']
    config['neat_config'] = content['dir']['neat_config']
    config['num_states']=content['model'].getint('num_states')
    config['actions']=content['model'].getint('actions')

    return config