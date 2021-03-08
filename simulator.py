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


YELLOW_LIGHT_TIME = 5
GREEN_LIGHT_TIME = 15

PHASE_N_GREEN = 0
PHASE_N_YELLOW = 1

PHASE_E_GREEN = 2
PHASE_E_YELLOW = 3

PHASE_S_GREEN = 4
PHASE_S_YELLOW = 5

PHASE_W_GREEN = 6
PHASE_W_YELLOW = 7

    

class Simulation:
    def __init__(self) -> None:
        self._max_steps = 300
        self._sumoBinary = checkBinary('sumo')
        self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(300)]

    def run(self, net, show = False) -> float:
        if show:
            self._sumoBinary = checkBinary('sumo-gui')
            self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(300)]
        else:
            self._sumoBinary = checkBinary('sumo')
            self._sumo_cmd = [self._sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(300)]
        traci.start(self._sumo_cmd)
        fitness = 0.0
        curr_step = 0
        last_light = 0
        
        while curr_step < self._max_steps:
            curr_step +=1
            
            
            halt_W = traci.edge.getLastStepHaltingNumber("E1")
            halt_S = traci.edge.getLastStepHaltingNumber("E4")
            halt_E = traci.edge.getLastStepHaltingNumber("E2")
            halt_N = traci.edge.getLastStepHaltingNumber("E3")
            
            
            output = net.activate((halt_W, halt_E, halt_S, halt_N))
            
            self._set_yellow_phase(output)
            curr_yellow_step = 0
            while curr_yellow_step < YELLOW_LIGHT_TIME and curr_step < self._max_steps and output!=last_light:
                traci.simulationStep()
                curr_yellow_step +=1
                curr_step +=1
                fitness -= self._collect_waiting_times()
                
            self._set_green_phase(output)
            curr_green_step = 0
            while curr_green_step < GREEN_LIGHT_TIME and curr_step < self._max_steps:
                traci.simulationStep()
                curr_green_step +=1
                curr_step +=1
                fitness -= self._collect_waiting_times()
            last_light = output

            
        traci.close()
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
    
    def _set_yellow_phase(self, action_number):
        """
        Activate the correct yellow light combination in sumo
        """
         # obtain the yellow phase code, based on the old action (ref on environment.net.xml)
        if action_number == 0:
            traci.trafficlight.setPhase("N2", PHASE_N_YELLOW)
        elif action_number == 1:
            traci.trafficlight.setPhase("N2", PHASE_E_YELLOW)
        elif action_number == 2:
            traci.trafficlight.setPhase("N2", PHASE_S_YELLOW)
        elif action_number == 3:
            traci.trafficlight.setPhase("N2", PHASE_W_YELLOW)


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
            
        