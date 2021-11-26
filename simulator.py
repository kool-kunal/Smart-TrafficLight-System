import os
from sumolib import checkBinary
import traci
import numpy as np
from abc import ABC, abstractmethod

PHASE_N_GREEN = 0
PHASE_N_YELLOW = 1

PHASE_E_GREEN = 2
PHASE_E_YELLOW = 3

PHASE_S_GREEN = 4
PHASE_S_YELLOW = 5

PHASE_W_GREEN = 6
PHASE_W_YELLOW = 7


class Simulation(ABC):
    @abstractmethod
    def run(self, net):
        pass

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def run_test(self):
        pass

    def setYellowPhase(self, action_number):
        if action_number == 0:
            traci.trafficlight.setPhase("N2", PHASE_N_YELLOW)
        elif action_number == 1:
            traci.trafficlight.setPhase("N2", PHASE_E_YELLOW)
        elif action_number == 2:
            traci.trafficlight.setPhase("N2", PHASE_S_YELLOW)
        elif action_number == 3:
            traci.trafficlight.setPhase("N2", PHASE_W_YELLOW)

    def setGreenPhase(self, action_number):
        if action_number == 0:
            traci.trafficlight.setPhase("N2", PHASE_N_GREEN)
        elif action_number == 1:
            traci.trafficlight.setPhase("N2", PHASE_E_GREEN)
        elif action_number == 2:
            traci.trafficlight.setPhase("N2", PHASE_S_GREEN)
        elif action_number == 3:
            traci.trafficlight.setPhase("N2", PHASE_W_GREEN)

    def _average_waiting_time(self):
        avg_waiting_time = np.sum([wait_time for car_id,wait_time in self._waiting_times.items()])/self._n_cars_generated
        return avg_waiting_time

    def _average_queue_length(self):
        avg_queue_length = np.sum(self._queue_lengths / self._max_steps)
        return avg_queue_length

    def _rms_waiting_time(self):
        squared_list = [x**2 for car_id,x in self._waiting_times.items()]
        sum_squared = sum(squared_list)
        mean_squared = sum_squared/self._n_cars_generated
        root_mean_squared_waiting_time = mean_squared**0.5
        return root_mean_squared_waiting_time

    def _harmonic_mean_fitness(self):
        avg_queue_length = self._average_queue_length()
        avg_waiting_time = self._average_waiting_time()
        harmonice_mean = 2 * (avg_queue_length * avg_waiting_time)/(avg_queue_length + avg_waiting_time)
        return harmonice_mean
    
    def _update_waiting_times(self):
        car_list = traci.vehicle.getIDList()
        for car_id in car_list:
            wait_time = traci.vehicle.getAccumulatedWaitingTime(car_id)
            self._waiting_times[car_id] = wait_time

    def _update_queue_lengths(self):
        self._queue_lengths[0] += traci.edge.getLastStepHaltingNumber("E1")
        self._queue_lengths[1] += traci.edge.getLastStepHaltingNumber("E4")
        self._queue_lengths[2] += traci.edge.getLastStepHaltingNumber("E2")
        self._queue_lengths[3] += traci.edge.getLastStepHaltingNumber("E3")


class Approach1(Simulation):
    def __init__(self, max_steps, n_cars, num_states, sumocfg_file_name, green_light_dur, yellow_light_dur, show, genome_id) -> None:
        self._max_steps = max_steps
        self._n_cars_generated = n_cars
        self._sumoBinary = checkBinary(
            'sumo-gui') if show else checkBinary('sumo')
        self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name),
                          "--no-step-log", "true", "-W", "--duration-log.disable", "--waiting-time-memory", str(max_steps)]
        self._num_states = num_states
        self._queue_lengths = np.zeros(4)
        self._waiting_times = {}
        self._yellow_light_dur = yellow_light_dur
        self._green_light_dur = green_light_dur
        self._genome_id = genome_id

    def run_test(self,net):
        _ = self.run(net)
        return -self._rms_waiting_time()
    
    def run(self, net) -> float:

        traci.start(self._sumo_cmd)
        curr_step = 0
        last_light = 0
        counter = 0
        current_light = np.zeros(shape=(4,))
        current_light[0] = 1

        while curr_step < self._max_steps:

            current_state = self._get_state()
            output = np.argmax(current_light)
            '''remove comments while testing.. to prevent starvation'''
            # if output == last_light:
            #     counter += 1
            # else:
            #     counter = 0

            # if counter == 3:
            #     print(output, current_light)
            #     current_light[output] = -1.0
            #     output = np.argmax(current_light)
            #     counter = 0
            network_input = np.concatenate((current_state, current_light))
            net_output = net.activate(network_input)
            current_light = net_output

            if output != last_light:
                self.setYellowPhase(last_light)
                curr_yellow_step = 0
                while curr_yellow_step < self._yellow_light_dur and curr_step < self._max_steps:
                    traci.simulationStep()
                    curr_yellow_step += 1
                    curr_step += 1
                    self._update_queue_lengths()
                    self._update_waiting_times()

            self.setGreenPhase(output)
            curr_green_step = 0
            while curr_green_step < self._green_light_dur and curr_step < self._max_steps:
                traci.simulationStep()
                curr_green_step += 1
                curr_step += 1
                self._update_queue_lengths()
                self._update_waiting_times()

            last_light = output

        fitness = self.fitness()
        traci.close()
        return fitness

    def fitness(self):
        fitness = -1*self._harmonic_mean_fitness()
        print(f'#{self._genome_id}', fitness, "avg_waiting_time=",
              self._average_waiting_time(), "avg_queue_length=", self._average_queue_length())
        return fitness

    def _get_state(self):

        state = np.zeros(self._num_states)
        car_list = traci.vehicle.getIDList()

        for car_id in car_list:
            lane_pos = traci.vehicle.getLanePosition(car_id)
            lane_id = traci.vehicle.getLaneID(car_id)
            lane_pos = 400 - lane_pos

            if lane_pos < 7:
                lane_cell = 0
            elif lane_pos < 14:
                lane_cell = 1
            elif lane_pos < 21:
                lane_cell = 2
            elif lane_pos < 28:
                lane_cell = 3
            elif lane_pos < 40:
                lane_cell = 4
            elif lane_pos < 60:
                lane_cell = 5
            elif lane_pos < 100:
                lane_cell = 6
            elif lane_pos < 160:
                lane_cell = 7
            elif lane_pos < 250:
                lane_cell = 8
            elif lane_pos <= 400:
                lane_cell = 9

            if lane_id == "E1_0":
                lane_group = 0
            elif lane_id == "E2_0":
                lane_group = 1
            elif lane_id == "E3_0":
                lane_group = 2
            elif lane_id == "E4_0":
                lane_group = 3
            else:
                lane_group = -1

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

# Approach 1 + input flow on 4 lanes
# Change num_input to 48 in config/config-feedforward.txt
class Approach2(Simulation): 
    def __init__(self, max_steps, n_cars, num_states, sumocfg_file_name, green_light_dur, yellow_light_dur, show, genome_id) -> None:
        self._max_steps = max_steps
        self._n_cars_generated = n_cars
        self._sumoBinary = checkBinary(
            'sumo-gui') if show else checkBinary('sumo')
        self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name),
                          "--no-step-log", "true", "-W", "--duration-log.disable", "--waiting-time-memory", str(max_steps)]
        self._num_states = num_states
        self._queue_lengths = np.zeros(4)
        self._waiting_times = {}
        self._car_ids = { 0 : [] , 1: [] , 2: [], 3: []}
        self._yellow_light_dur = yellow_light_dur
        self._green_light_dur = green_light_dur
        self._genome_id = genome_id

    def run_test(self,net):
        _=self.run(net)
        return -1*self._rms_waiting_time()

    def run(self, net) -> float:

        traci.start(self._sumo_cmd)
        curr_step = 0
        last_light = 0

        counter = 0

        current_light = np.zeros(shape=(4,))
        current_light[0] = 1

        while curr_step < self._max_steps:

            current_state,input_flow = self._get_state()
            output = np.argmax(current_light)
            '''remove comments while testing.. to prevent starvation'''
            # if output == last_light:
            #     counter += 1
            # else:
            #     counter = 0

            # if counter == 3:
            #     print(output, current_light)
            #     current_light[output] = -1.0
            #     output = np.argmax(current_light)
            #     counter = 0
            network_input = np.concatenate((current_state,input_flow,current_light))
            net_output = net.activate(network_input)
            current_light = net_output

            if output != last_light:
                self.setYellowPhase(last_light)
                curr_yellow_step = 0
                while curr_yellow_step < self._yellow_light_dur and curr_step < self._max_steps:
                    traci.simulationStep()
                    curr_yellow_step += 1
                    curr_step += 1
                    self._update_queue_lengths()
                    self._update_waiting_times()

            self.setGreenPhase(output)
            curr_green_step = 0
            while curr_green_step < self._green_light_dur and curr_step < self._max_steps:
                traci.simulationStep()
                curr_green_step += 1
                curr_step += 1
                self._update_queue_lengths()
                self._update_waiting_times()

            last_light = output

        fitness = self.fitness()
        traci.close()
        return fitness

    def fitness(self):
        fitness = -1*self._rms_waiting_time()

        print(f'#{self._genome_id}', fitness, "avg_waiting_time=",
              self._average_waiting_time(), "avg_queue_length=", self._average_queue_length())

        return fitness

    def _get_state(self):

        state = np.zeros(self._num_states)
        car_list = traci.vehicle.getIDList()
        new_car_ids = { 0 : [], 1: [], 2: [], 3: []}

        for car_id in car_list:
            lane_pos = traci.vehicle.getLanePosition(car_id)
            lane_id = traci.vehicle.getLaneID(car_id)
            lane_pos = 400 - lane_pos

            if lane_pos < 7:
                lane_cell = 0
            elif lane_pos < 14:
                lane_cell = 1
            elif lane_pos < 21:
                lane_cell = 2
            elif lane_pos < 28:
                lane_cell = 3
            elif lane_pos < 40:
                lane_cell = 4
            elif lane_pos < 60:
                lane_cell = 5
            elif lane_pos < 100:
                lane_cell = 6
            elif lane_pos < 160:
                lane_cell = 7
            elif lane_pos < 250:
                lane_cell = 8
            elif lane_pos <= 400:
                lane_cell = 9

            if lane_id == "E1_0":
                lane_group = 0
            elif lane_id == "E2_0":
                lane_group = 1
            elif lane_id == "E3_0":
                lane_group = 2
            elif lane_id == "E4_0":
                lane_group = 3
            else:
                lane_group = -1

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
                new_car_ids[lane_group].append(car_id)

        input_flow = self._get_input_flow(new_car_ids)
        self._car_ids = new_car_ids
        return state,input_flow

    def _get_input_flow(self,new_car_ids):

        def get_difference(list1, list2):
            present = {}
            count = 0
            for id in list1:
                present[id]=True

            for id in list2:
                if id in present.keys():
                    continue
                count=count+1
        
            count2 = len(list1) - (len(list2)-count)
            return count - count2

        input_flow = np.zeros(4)
        for i in range(4):
            input_flow[i] = get_difference(self._car_ids[i],new_car_ids[i])
        return input_flow


class TimeBasedTrafficLigthSystem(Simulation):
    def __init__(self, max_steps, n_cars, num_states, sumocfg_file_name, green_light_dur, yellow_light_dur, show, genome_id) -> None:
        self._max_steps = max_steps
        self._n_cars_generated = n_cars
        self._sumoBinary = checkBinary(
            'sumo-gui') if show else checkBinary('sumo')
        self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name),
                          "--no-step-log", "true", "-W", "--duration-log.disable", "--waiting-time-memory", str(max_steps)]
        self._num_states = num_states
        self._queue_lengths = np.zeros(4)
        self._waiting_times = {}
        self._yellow_light_dur = yellow_light_dur
        self._green_light_dur = green_light_dur
        self._genome_id = genome_id

    def run_test(self):
        _ = self.run()
        return -1*self._rms_waiting_time()

    def run(self) -> float:

        curr_step = 0
        traci.start(self._sumo_cmd)
        while curr_step < self._max_steps:
            curr_step += 1
            traci.simulationStep()
            self._update_queue_lengths()
            self._update_waiting_times()

        fitness = self.fitness()
        traci.close()
        return fitness

    def fitness(self):
        fitness = -1*self._rms_waiting_time()

        print(f'#{self._genome_id}', fitness, "avg_waiting_time=",
              self._average_waiting_time(), "avg_queue_length=", self._average_queue_length())
        return fitness
