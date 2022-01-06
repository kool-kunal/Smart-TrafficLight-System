import numpy as np
import math
import random


class TrafficGenerator:
    def __init__(self, max_steps, n_cars_generated):
        self._n_cars_generated = n_cars_generated
        self._max_steps = max_steps*0.8

    def generate_routefile(self, seed):
        """
        Generation of the route of every car for one episode
        """
        np.random.seed(seed)

        timings = np.random.weibull(2, self._n_cars_generated)
        timings = np.sort(timings)

        car_id_list = []

        # reshape the distribution to fit the interval 0:max_steps
        car_gen_steps = []
        min_old = math.floor(timings[1])
        max_old = math.ceil(timings[-1])
        min_new = 0
        max_new = self._max_steps
        for value in timings:
            car_gen_steps = np.append(car_gen_steps, ((
                max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)

        # round every value to int -> effective steps when a car will be generated
        car_gen_steps = np.rint(car_gen_steps)

        # produce the file for cars generation, one car per line
        with open("environment/env.rou.xml", "w") as routes:
            print("""<routes>
            <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="25" sigma="0.5" />

            <route id="W_N" edges="E1 -E3"/>
            <route id="W_E" edges="E1 -E2"/>
            <route id="W_S" edges="E1 -E4"/>
            <route id="N_W" edges="E3 -E1"/>
            <route id="N_E" edges="E3 -E2"/>
            <route id="N_S" edges="E3 -E4"/>
            <route id="E_W" edges="E2 -E1"/>
            <route id="E_N" edges="E2 -E3"/>
            <route id="E_S" edges="E2 -E4"/>
            <route id="S_W" edges="E4 -E1"/>
            <route id="S_N" edges="E4 -E3"/>
            <route id="S_E" edges="E4 -E2"/>""", file=routes)

            for car_counter, step in enumerate(car_gen_steps):
                straight_or_turn = np.random.uniform()
                if straight_or_turn < 0.75:  # choose direction: straight or turn - 75% of times the car goes straight
                    # choose a random source & destination
                    route_straight = np.random.randint(1, 5)
                    if route_straight == 1:
                        print('    <vehicle id="W_E_%i" type="standard_car" route="W_E" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'W_E_{car_counter}')
                    elif route_straight == 2:
                        print('    <vehicle id="E_W_%i" type="standard_car" route="E_W" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'E_W_{car_counter}')
                    elif route_straight == 3:
                        print('    <vehicle id="N_S_%i" type="standard_car" route="N_S" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'N_S_{car_counter}')
                    else:
                        print('    <vehicle id="S_N_%i" type="standard_car" route="S_N" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'S_N_{car_counter}')
                else:  # car that turn -25% of the time the car turns
                    # choose random source source & destination
                    route_turn = np.random.randint(1, 9)
                    if route_turn == 1:
                        print('    <vehicle id="W_N_%i" type="standard_car" route="W_N" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'W_N_{car_counter}')
                    elif route_turn == 2:
                        print('    <vehicle id="W_S_%i" type="standard_car" route="W_S" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'W_S_{car_counter}')
                    elif route_turn == 3:
                        print('    <vehicle id="N_W_%i" type="standard_car" route="N_W" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'N_W_{car_counter}')
                    elif route_turn == 4:
                        print('    <vehicle id="N_E_%i" type="standard_car" route="N_E" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'N_E_{car_counter}')
                    elif route_turn == 5:
                        print('    <vehicle id="E_N_%i" type="standard_car" route="E_N" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'E_N_{car_counter}')
                    elif route_turn == 6:
                        print('    <vehicle id="E_S_%i" type="standard_car" route="E_S" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'E_S_{car_counter}')
                    elif route_turn == 7:
                        print('    <vehicle id="S_W_%i" type="standard_car" route="S_W" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'S_W_{car_counter}')
                    elif route_turn == 8:
                        print('    <vehicle id="S_E_%i" type="standard_car" route="S_E" depart="%s" departLane="random" departSpeed="10" />' %
                              (car_counter, step), file=routes)
                        car_id_list.append(f'S_E_{car_counter}')

            print("</routes>", file=routes)

        return car_id_list
