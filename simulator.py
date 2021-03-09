import os
from sumolib import checkBinary
import traci
import numpy as np

sumocfg_file_name = "sumo_config.sumocfg"



# sumo_cmd = [sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(500)]

# traci.start(sumo_cmd)
# curr_step = 0
# while curr_step < 500:
#     curr_step +=1
#     traci.simulationStep()


# YELLOW_LIGHT_TIME = 5
# GREEN_LIGHT_TIME = 15

# PHASE_N_GREEN = 0
# PHASE_N_YELLOW = 1

# PHASE_E_GREEN = 2
# PHASE_E_YELLOW = 3

# PHASE_S_GREEN = 4
# PHASE_S_YELLOW = 5

# PHASE_W_GREEN = 6
# PHASE_W_YELLOW = 7

PHASE_N_GREEN = 0
PHASE_E_GREEN = 1
PHASE_S_GREEN = 2
PHASE_W_GREEN = 3

    

class Simulation:
    def __init__(self) -> None:
        self._max_steps = 400
        self._n_cars_generated=100
        self._sumoBinary = checkBinary('sumo')
        self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(400)]
        self._num_states = 40
        self._queue_lengths = np.zeros(4)

    def run(self, net, show = False) -> float:
        if show:
            self._sumoBinary = checkBinary('sumo-gui')
            self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(300)]
        else:
            self._sumoBinary = checkBinary('sumo')
            self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true","-W", "--duration-log.disable", "--waiting-time-memory", str(300)]
        traci.start(self._sumo_cmd)
        curr_step = 0
        #last_light = 0
        
        while curr_step < self._max_steps:
            
            curr_step +=1
            
            output = np.argmax(net.activate(self._get_state()))
            #print(output)
            # self._set_yellow_phase(output)
            # curr_yellow_step = 0
            # while curr_yellow_step < YELLOW_LIGHT_TIME and curr_step < self._max_steps and output!=last_light:
            #     traci.simulationStep()
            #     curr_yellow_step +=1
            #     curr_step +=1
            #     fitness -= self._collect_waiting_times()
                
            self._set_green_phase(output)
            traci.simulationStep()
            # curr_green_step = 0
            # while curr_green_step < GREEN_LIGHT_TIME and curr_step < self._max_steps:
            #     traci.simulationStep()
            #     curr_green_step +=1
            #     curr_step +=1
            #     fitness -= self._collect_waiting_times()
            self._update_queue_lengths()
            #last_light = output

            
        
        fitness = self._fitness()
        traci.close()
        return fitness
    
    def _update_queue_lengths(self):
        self._queue_lengths[0] += traci.edge.getLastStepHaltingNumber("E1")
        self._queue_lengths[1] += traci.edge.getLastStepHaltingNumber("E4")
        self._queue_lengths[2] += traci.edge.getLastStepHaltingNumber("E2")
        self._queue_lengths[3] += traci.edge.getLastStepHaltingNumber("E3")
        
    
    def _fitness(self):
        fitness = 0 
        fitness -= np.sum(self._queue_lengths / self._max_steps) / 4
        
        fitness -= self._collect_waiting_times()/self._n_cars_generated
        
        return fitness
        
        
        
        
        
        
            
    def _collect_waiting_times(self):
        """
        Retrieve the waiting time of every car in the incoming roads
        """
        total_waiting_time = 0.0
        incoming_roads = ["E1", "E2", "E3", "E4"]
        car_list = traci.vehicle.getIDList()
        for car_id in car_list:
            wait_time = traci.vehicle.getAccumulatedWaitingTime(car_id)
            road_id = traci.vehicle.getRoadID(car_id)  # get the road id where the car is located
            if road_id in incoming_roads:  # consider only the waiting times of cars in incoming road
                total_waiting_time += wait_time
        
        return total_waiting_time
    
    # def _set_yellow_phase(self, action_number):
    #     """
    #     Activate the correct yellow light combination in sumo
    #     """
    #      # obtain the yellow phase code, based on the old action (ref on environment.net.xml)
    #     if action_number == 0:
    #         traci.trafficlight.setPhase("N2", PHASE_N_YELLOW)
    #     elif action_number == 1:
    #         traci.trafficlight.setPhase("N2", PHASE_E_YELLOW)
    #     elif action_number == 2:
    #         traci.trafficlight.setPhase("N2", PHASE_S_YELLOW)
    #     elif action_number == 3:
    #         traci.trafficlight.setPhase("N2", PHASE_W_YELLOW)


    def _set_green_phase(self, action_number):
        """
        Activate the correct green light combination in sumo
        """
        if action_number == 0:
            traci.trafficlight.setPhase("N2", PHASE_N_GREEN)
        elif action_number == 1:
            traci.trafficlight.setPhase("N2", PHASE_E_GREEN)
        elif action_number == 2:
            traci.trafficlight.setPhase("N2", PHASE_S_GREEN)
        elif action_number == 3:
            traci.trafficlight.setPhase("N2", PHASE_W_GREEN)
            
    def _get_state(self):
        """
        Retrieve the state of the intersection from sumo, in the form of cell occupancy
        """
        state = np.zeros(self._num_states)
        car_list = traci.vehicle.getIDList()

        for car_id in car_list:
            lane_pos = traci.vehicle.getLanePosition(car_id)
            lane_id = traci.vehicle.getLaneID(car_id)
            lane_pos = 400 - lane_pos  # inversion of lane pos, so if the car is close to the traffic light -> lane_pos = 0 --- 750 = max len of a road

            # distance in meters from the traffic light -> mapping into cells
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

            # finding the lane where the car is located 
            # x2TL_3 are the "turn left only" lanes
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
                car_position = int(str(lane_group) + str(lane_cell))  # composition of the two postion ID to create a number in interval 0-79
                valid_car = True
            elif lane_group == 0:
                car_position = lane_cell
                valid_car = True
            else:
                valid_car = False  # flag for not detecting cars crossing the intersection or driving away from it

            if valid_car:
                state[car_position] += 1  # write the position of the car car_id in the state array in the form of "cell occupied"

        return state
        
            
        