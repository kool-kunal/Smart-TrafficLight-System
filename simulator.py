import os
from sumolib import checkBinary
import traci
import numpy as np

sumocfg_file_name = "sumo_config.sumocfg"

sumoBinary = checkBinary('sumo')

# sumo_cmd = [sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(500)]

# traci.start(sumo_cmd)
# curr_step = 0
# while curr_step < 500:
#     curr_step +=1
#     traci.simulationStep()
    

class Simulation:
    def __init__(self) -> None:
        self._max_steps = 300
        self._sumo_cmd = [sumoBinary, "-c", os.path.join('environment', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(300)]

    def run(self, net) -> float:
        traci.start(self._sumo_cmd)
        fitness = 0.0
        curr_step = 0
        while curr_step < self._max_steps:
            curr_step +=1
            
            
            halt_W = traci.edge.getLastStepHaltingNumber("E1")
            halt_S = traci.edge.getLastStepHaltingNumber("E4")
            halt_E = traci.edge.getLastStepHaltingNumber("E2")
            halt_N = traci.edge.getLastStepHaltingNumber("E3")
            
            
            output = net.activate((halt_W, halt_E, halt_S, halt_N))
            
            green_light = np.argmax(output)
            if green_light == 1:
                green_light =2
            traci.trafficlight.setPhase("N2", green_light)
            fitness -= self._collect_waiting_times()
            traci.simulationStep()
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
            
        
        
        
        