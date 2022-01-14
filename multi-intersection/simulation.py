import enum
import os
from sumolib import checkBinary
import traci
import numpy as np
from enum import Enum

PHASE_N_GREEN = 0
PHASE_N_YELLOW = 1

PHASE_E_GREEN = 2
PHASE_E_YELLOW = 3

PHASE_S_GREEN = 4
PHASE_S_YELLOW = 5

PHASE_W_GREEN = 6
PHASE_W_YELLOW = 7


class LightType(Enum):
    Green = 1
    Yellow = 2


class ModelSimulation:
    def __init__(self, max_steps, n_cars, num_states, sumocfg_file_name, green_light_dur, yellow_light_dur, show, node_graph=None, junctions=None, starvation_penalty = 1.0) -> None:
        self._max_steps = max_steps
        self._n_cars_generated = n_cars
        self._num_states = num_states
        self._sumoBinary = checkBinary(
            'sumo-gui') if show else checkBinary('sumo')
        self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name),
                          "--no-step-log", "true", "-W", "--duration-log.disable", "--waiting-time-memory", str(max_steps)]
        self._queue_lengths = np.zeros(16)
        self._waiting_times = {}
        self._yellow_light_dur = yellow_light_dur
        self._green_light_dur = green_light_dur
        self._number_of_cars_on_map = 0
        self._starvation_penalty = starvation_penalty
        self._graph = {
            "N1_L": [{"N1": "N1_L_N1"}],
            "N1_D": [{"N1": "N1_D_N1"}],
            "N1": [{"N1_L": "N1_N1_L"}, {"N1_D": "N1_N1_D"}, {"N2": "N1_N2"}, {"N4": "N1_N4"}],
            "N2": [{"N2_R": "N2_N2_R"}, {"N2_D": "N2_N2_D"}, {"N3": "N2_N3"}, {"N1": "N2_N1"}],
            "N2_R": [{"N2": "N2_R_N2"}],
            "N2_D": [{"N2": "N2_D_N2"}],
            "N3": [{"N3_U": "N3_N3_U"}, {"N3_R": "N3_N3_R"}, {"N2": "N3_N2"}, {"N4": "N3_N4"}],
            "N3_U": [{"N3": "N3_U_N3"}],
            "N3_R": [{"N3": "N3_R_N3"}],
            "N4": [{"N4_U": "N4_N4_U"}, {"N4_L": "N4_N4_L"}, {"N1": "N4_N1"}, {"N3": "N4_N3"}],
            "N4_U": [{"N4": "N4_U_N4"}],
            "N4_L": [{"N4": "N4_L_N4"}],
        } if node_graph == None else node_graph

        self._junctions = ['N1', 'N2', 'N3',
                           'N4'] if junctions == None else junctions

        # print(self._green_light_dur)

    def _update_queue_length(self):
        self._queue_lengths[0] += traci.edge.getLastStepHaltingNumber("N1_L_N1")
        self._queue_lengths[1] += traci.edge.getLastStepHaltingNumber("N1_D_N1")
        self._queue_lengths[2] += traci.edge.getLastStepHaltingNumber("N2_N1")
        self._queue_lengths[3] += traci.edge.getLastStepHaltingNumber("N4_N1")
        self._queue_lengths[4] += traci.edge.getLastStepHaltingNumber("N1_N2")
        self._queue_lengths[5] += traci.edge.getLastStepHaltingNumber("N2_D_N2")
        self._queue_lengths[6] += traci.edge.getLastStepHaltingNumber("N2_R_N2")
        self._queue_lengths[7] += traci.edge.getLastStepHaltingNumber("N3_N2")
        self._queue_lengths[8] += traci.edge.getLastStepHaltingNumber("N4_N3")
        self._queue_lengths[9] += traci.edge.getLastStepHaltingNumber("N2_N3")
        self._queue_lengths[10] += traci.edge.getLastStepHaltingNumber("N3_R_N3")
        self._queue_lengths[11] += traci.edge.getLastStepHaltingNumber("N3_U_N3")
        self._queue_lengths[12] += traci.edge.getLastStepHaltingNumber("N4_L_N4")
        self._queue_lengths[13] += traci.edge.getLastStepHaltingNumber("N1_N4")
        self._queue_lengths[14] += traci.edge.getLastStepHaltingNumber("N4_U_N4")
        self._queue_lengths[15] += traci.edge.getLastStepHaltingNumber("N3_N4")

    def _average_queue_length(self):
        return np.sum(self._queue_lengths/self._max_steps)

    def _update_waiting_time(self):
        car_list = traci.vehicle.getIDList()
        for car_id in car_list:
            wait_time = traci.vehicle.getAccumulatedWaitingTime(car_id)
            self._waiting_times[car_id] = wait_time

    def _average_waiting_time(self):
        avg_waiting_time = np.sum(
            [wait_time for car_id, wait_time in self._waiting_times.items()])/self._n_cars_generated
        return avg_waiting_time


    def _check_cars(self):
        self._number_of_cars_on_map = len(traci.vehicle.getIDList())

    def _penalize_for_starvation(self, fitness):
        if self._number_of_cars_on_map > 0:
            return fitness * self._starvation_penalty

        return fitness

    def _rms_waiting_time(self):
        squared_list = [x**2 for car_id, x in self._waiting_times.items()]
        sum_squared = sum(squared_list)
        mean_squared = sum_squared/self._n_cars_generated
        root_mean_squared_waiting_time = mean_squared**0.5
        return self._penalize_for_starvation(root_mean_squared_waiting_time)

    def _harmonic_mean_fitness(self):
        avg_queue_length = self._average_queue_length()
        avg_waiting_time = self._average_waiting_time()
        harmonic_mean = 2 * (avg_queue_length * avg_waiting_time) / \
            (avg_queue_length + avg_waiting_time)
        return self._penalize_for_starvation(harmonic_mean)

    def _run_ttl(self):
        traci.start(self._sumo_cmd)
        current_step = 0

        while current_step <= self._max_steps:
            traci.simulationStep()
            current_step += 1
            self._update_waiting_time()
            self._update_queue_length()

        self._check_cars()
        traci.close()

    def _run(self, net):
        starvation_counter = 1.0
        traci.start(self._sumo_cmd)

        initial_state = np.zeros(shape=(4,))
        initial_state[0] = 1

        junction_record = dict((key, {'next_time': 0, 'next_state': initial_state,
                               'light_type': LightType.Green, 'last_state': initial_state}) for key in self._junctions)

        # print(junction_record)
        current_step = 0
        while current_step <= self._max_steps:
            print(current_step)
            for junction_id, junction in junction_record.items():

                if junction['next_time'] == current_step:
                    print('\t', junction_id, junction['light_type'])
                    if junction['light_type'] == LightType.Yellow:

                        action = np.argmax(junction['last_state'])
                        junction_record[junction_id]['next_time'] = junction['next_time'] + \
                            self._green_light_dur
                        junction_record[junction_id]['light_type'] = LightType.Green
                        self._setGreenPhase(action, junction_id)

                        # predicted_state = self._predict_next_state(
                        #     junction_id, junction['next_state'], net)
                        # action = np.argmax(junction['next_state'])

                        # self._setGreenPhase(action, junction_id)
                        # junction_record[junction_id]['next_state'] = predicted_state
                        # junction_record[junction_id]['next_time'] = junction['next_time'] + \
                        #     self._green_light_dur
                        # junction_record[junction_id]['light_type'] = LightType.Green
                    else:
                        predicted_state = self._predict_next_state(
                            junction_id, junction['next_state'], net)

                        #print('\t', np.argmax(predicted_state))

                        previous_action = np.argmax(junction['last_state'])

                        junction_record[junction_id]['last_state'] = junction_record[junction_id]['next_state']
                        junction_record[junction_id]['next_state'] = predicted_state

                        action = np.argmax(junction['last_state'])
                        #print('\t', action)

                        if action == previous_action:
                            junction_record[junction_id]['next_state'][action] *=starvation_counter
                            starvation_counter -= 0.05
                            junction_record[junction_id]['next_time'] = junction['next_time'] + \
                                self._green_light_dur
                        else:
                            starvation_counter = 1.0
                            junction_record[junction_id]['next_time'] = junction['next_time'] + \
                                self._yellow_light_dur
                            junction_record[junction_id]['light_type'] = LightType.Yellow
                            self._setYellowPhase(previous_action, junction_id)

                        # if action == np.argmax(junction['last_light']):
                        #     junction_record[junction_id]['next_time'] = junction['next_time'] + \
                        #         self._green_light_dur
                        # else:
                        #     junction_record[junction_id]['next_time'] = junction['next_time'] + \
                        #         self._yellow_light_dur
                        #     junction_record[junction_id]['light_type'] = LightType.Yellow
                        #     self._setYellowPhase(action, junction_id)

            current_step += 1
            traci.simulationStep()
            self._update_queue_length()
            self._update_waiting_time()
        
        self._check_cars()
        traci.close()

    def _predict_next_state(self, junction, light_state, net):
        state = self._get_state(junction)

        network_input = np.concatenate((state, light_state))
        output = net.activate(network_input)

        return output

    def _get_state(self, junction_id):

        state = np.zeros(self._num_states)
        car_list = traci.vehicle.getIDList()

        for car_id in car_list:
            lane_pos = traci.vehicle.getLanePosition(car_id)
            lane_id = traci.vehicle.getLaneID(car_id)
            lane_pos = 200 - lane_pos
            if lane_pos < 7:
                lane_cell = 0
            elif lane_pos < 7:
                lane_cell = 1
            elif lane_pos < 14:
                lane_cell = 2
            elif lane_pos < 21:
                lane_cell = 3
            elif lane_pos < 28:
                lane_cell = 4
            elif lane_pos < 50:
                lane_cell = 5
            elif lane_pos < 80:
                lane_cell = 6
            elif lane_pos < 120:
                lane_cell = 7
            elif lane_pos < 160:
                lane_cell = 8
            elif lane_pos <= 200:
                lane_cell = 9

            if junction_id == 'N1':
                if lane_id == 'N1_L_N1_0':
                    lane_group = 0
                elif lane_id == 'N2_N1_0':
                    lane_group = 1
                elif lane_id == 'N4_N1_0':
                    lane_group = 2
                elif lane_id == 'N1_D_N1_0':
                    lane_group = 3
                else:
                    lane_group = -1

            elif junction_id == 'N2':
                if lane_id == 'N1_N2_0':
                    lane_group = 0
                elif lane_id == 'N2_R_N2_0':
                    lane_group = 1
                elif lane_id == 'N3_N2_0':
                    lane_group = 2
                elif lane_id == 'N2_D_N2_0':
                    lane_group = 3
                else:
                    lane_group = -1

            elif junction_id == 'N3':
                if lane_id == 'N4_N3_0':
                    lane_group = 0
                elif lane_id == 'N3_R_N3_0':
                    lane_group = 1
                elif lane_id == 'N3_U_N3_0':
                    lane_group = 2
                elif lane_id == 'N2_N3_0':
                    lane_group = 3
                else:
                    lane_group = -1

            else:
                if lane_id == 'N4_L_N4_0':
                    lane_group = 0
                elif lane_id == 'N3_N4_0':
                    lane_group = 1
                elif lane_id == 'N4_U_N4_0':
                    lane_group = 2
                elif lane_id == 'N1_N4_0':
                    lane_group = 3
                else:
                    lane_group = -1

            # if lane_id == "E1_0":
            #     lane_group = 0
            # elif lane_id == "E2_0":
            #     lane_group = 1
            # elif lane_id == "E3_0":
            #     lane_group = 2
            # elif lane_id == "E4_0":
            #     lane_group = 3
            # else:
            #     lane_group = -1

            if lane_group >= 1 and lane_group <= 3:
                car_position = int(str(lane_group) + str(lane_cell))
                valid_car = True
            elif lane_group == 0:
                car_position = lane_cell
                valid_car = True
            else:
                valid_car = False

            if valid_car:
                state[car_position] += 1

        return state

    def _setYellowPhase(self, action_number, junction_id):
        if action_number == 0:
            traci.trafficlight.setPhase(junction_id, PHASE_N_YELLOW)
        elif action_number == 1:
            traci.trafficlight.setPhase(junction_id, PHASE_E_YELLOW)
        elif action_number == 2:
            traci.trafficlight.setPhase(junction_id, PHASE_S_YELLOW)
        elif action_number == 3:
            traci.trafficlight.setPhase(junction_id, PHASE_W_YELLOW)

    def _setGreenPhase(self, action_number, junction_id):
        if action_number == 0:
            traci.trafficlight.setPhase(junction_id, PHASE_N_GREEN)
        elif action_number == 1:
            traci.trafficlight.setPhase(junction_id, PHASE_E_GREEN)
        elif action_number == 2:
            traci.trafficlight.setPhase(junction_id, PHASE_S_GREEN)
        elif action_number == 3:
            traci.trafficlight.setPhase(junction_id, PHASE_W_GREEN)


    def _refersh_params(self):
        self._queue_lengths = np.zeros(16)
        self._waiting_times = {}
        self._number_of_cars_on_map = 0

    def run_test_ttl(self):
        self._refersh_params()
        self._run_ttl()
        return -1*self._rms_waiting_time(),-1*self._harmonic_mean_fitness(),self._average_queue_length(),self._average_waiting_time()

    def run_test_net(self,net):
        self._refersh_params()
        self._run(net)
        return -1*self._rms_waiting_time(),-1*self._harmonic_mean_fitness(),self._average_queue_length(),self._average_waiting_time()