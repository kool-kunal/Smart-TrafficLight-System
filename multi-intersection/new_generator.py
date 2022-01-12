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

            <route id=N1_L_N1_N1_N1_D edges=N1_L_N1 N1_N1_D/>
            <route id=N1_L_N1_N2_N2_R edges=N1_L_N1 N1_N2 N2_N2_R/>
            <route id=N1_L_N1_N2_N2_D edges=N1_L_N1 N1_N2 N2_N2_D/>
            <route id=N1_L_N1_N3_N3_U edges=N1_L_N1 N1_N2 N2_N3 N3_N3_U/>
            <route id=N1_L_N1_N3_N3_R edges=N1_L_N1 N1_N2 N2_N3 N3_N3_R/>
            <route id=N1_L_N1_N4_N4_U edges=N1_L_N1 N1_N2 N2_N3 N3_N4 N4_N4_U/>
            <route id=N1_L_N1_N4_N4_L edges=N1_L_N1 N1_N2 N2_N3 N3_N4 N4_N4_L/>
            <route id=N1_D_N1_N1_N1_L edges=N1_D_N1 N1_N1_L/>
            <route id=N1_D_N1_N2_N2_R edges=N1_D_N1 N1_N2 N2_N2_R/>
            <route id=N1_D_N1_N2_N2_D edges=N1_D_N1 N1_N2 N2_N2_D/>
            <route id=N1_D_N1_N3_N3_U edges=N1_D_N1 N1_N2 N2_N3 N3_N3_U/>
            <route id=N1_D_N1_N3_N3_R edges=N1_D_N1 N1_N2 N2_N3 N3_N3_R/>
            <route id=N1_D_N1_N4_N4_U edges=N1_D_N1 N1_N2 N2_N3 N3_N4 N4_N4_U/>
            <route id=N1_D_N1_N4_N4_L edges=N1_D_N1 N1_N2 N2_N3 N3_N4 N4_N4_L/>
            <route id=N2_D_N2_N2_N2_R edges=N2_D_N2 N2_N2_R/>
            <route id=N2_D_N2_N3_N3_U edges=N2_D_N2 N2_N3 N3_N3_U/>
            <route id=N2_D_N2_N3_N3_R edges=N2_D_N2 N2_N3 N3_N3_R/>
            <route id=N2_D_N2_N4_N4_U edges=N2_D_N2 N2_N3 N3_N4 N4_N4_U/>
            <route id=N2_D_N2_N4_N4_L edges=N2_D_N2 N2_N3 N3_N4 N4_N4_L/>
            <route id=N2_D_N2_N1_N1_L edges=N2_D_N2 N2_N3 N3_N4 N4_N1 N1_N1_L/>
            <route id=N2_D_N2_N1_N1_D edges=N2_D_N2 N2_N3 N3_N4 N4_N1 N1_N1_D/>
            <route id=N2_R_N2_N2_N2_D edges=N2_R_N2 N2_N2_D/>
            <route id=N2_R_N2_N3_N3_U edges=N2_R_N2 N2_N3 N3_N3_U/>
            <route id=N2_R_N2_N3_N3_R edges=N2_R_N2 N2_N3 N3_N3_R/>
            <route id=N2_R_N2_N4_N4_U edges=N2_R_N2 N2_N3 N3_N4 N4_N4_U/>
            <route id=N2_R_N2_N4_N4_L edges=N2_R_N2 N2_N3 N3_N4 N4_N4_L/>
            <route id=N2_R_N2_N1_N1_L edges=N2_R_N2 N2_N3 N3_N4 N4_N1 N1_N1_L/>
            <route id=N2_R_N2_N1_N1_D edges=N2_R_N2 N2_N3 N3_N4 N4_N1 N1_N1_D/>
            <route id=N3_R_N3_N3_N3_U edges=N3_R_N3 N3_N3_U/>
            <route id=N3_R_N3_N2_N2_R edges=N3_R_N3 N3_N2 N2_N2_R/>
            <route id=N3_R_N3_N2_N2_D edges=N3_R_N3 N3_N2 N2_N2_D/>
            <route id=N3_R_N3_N1_N1_L edges=N3_R_N3 N3_N2 N2_N1 N1_N1_L/>
            <route id=N3_R_N3_N1_N1_D edges=N3_R_N3 N3_N2 N2_N1 N1_N1_D/>
            <route id=N3_R_N3_N4_N4_U edges=N3_R_N3 N3_N2 N2_N1 N1_N4 N4_N4_U/>
            <route id=N3_R_N3_N4_N4_L edges=N3_R_N3 N3_N2 N2_N1 N1_N4 N4_N4_L/>
            <route id=N3_U_N3_N3_N3_R edges=N3_U_N3 N3_N3_R/>
            <route id=N3_U_N3_N2_N2_R edges=N3_U_N3 N3_N2 N2_N2_R/>
            <route id=N3_U_N3_N2_N2_D edges=N3_U_N3 N3_N2 N2_N2_D/>
            <route id=N3_U_N3_N1_N1_L edges=N3_U_N3 N3_N2 N2_N1 N1_N1_L/>
            <route id=N3_U_N3_N1_N1_D edges=N3_U_N3 N3_N2 N2_N1 N1_N1_D/>
            <route id=N3_U_N3_N4_N4_U edges=N3_U_N3 N3_N2 N2_N1 N1_N4 N4_N4_U/>
            <route id=N3_U_N3_N4_N4_L edges=N3_U_N3 N3_N2 N2_N1 N1_N4 N4_N4_L/>
            <route id=N4_U_N4_N4_N4_L edges=N4_U_N4 N4_N4_L/>
            <route id=N4_U_N4_N1_N1_L edges=N4_U_N4 N4_N1 N1_N1_L/>
            <route id=N4_U_N4_N1_N1_D edges=N4_U_N4 N4_N1 N1_N1_D/>
            <route id=N4_U_N4_N2_N2_R edges=N4_U_N4 N4_N1 N1_N2 N2_N2_R/>
            <route id=N4_U_N4_N2_N2_D edges=N4_U_N4 N4_N1 N1_N2 N2_N2_D/>
            <route id=N4_U_N4_N3_N3_U edges=N4_U_N4 N4_N1 N1_N2 N2_N3 N3_N3_U/>
            <route id=N4_U_N4_N3_N3_R edges=N4_U_N4 N4_N1 N1_N2 N2_N3 N3_N3_R/>
            <route id=N4_L_N4_N4_N4_U edges=N4_L_N4 N4_N4_U/>
            <route id=N4_L_N4_N1_N1_L edges=N4_L_N4 N4_N1 N1_N1_L/>
            <route id=N4_L_N4_N1_N1_D edges=N4_L_N4 N4_N1 N1_N1_D/>
            <route id=N4_L_N4_N2_N2_R edges=N4_L_N4 N4_N1 N1_N2 N2_N2_R/>
            <route id=N4_L_N4_N2_N2_D edges=N4_L_N4 N4_N1 N1_N2 N2_N2_D/>
            <route id=N4_L_N4_N3_N3_U edges=N4_L_N4 N4_N1 N1_N2 N2_N3 N3_N3_U/>
            <route id=N4_L_N4_N3_N3_R edges=N4_L_N4 N4_N1 N1_N2 N2_N3 N3_N3_R/>""", file=routes)

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


# def gen_routes():

#     def reset_visited(edges,visited):
#         for key in edges:
#             visited[key] = False

#     def dfs(edges, curr, visited):
#         visited[curr]=True

#         paths = []
#         for mapping in edges[curr]:
#             for neighbour,edge in mapping.items():
#                 if not visited[neighbour]:
#                     temp = dfs(edges,neighbour,visited)
#                     new_paths = []
#                     for path in temp:
#                         new_paths.append(edge + " " + path)
#                     if len(new_paths) == 0:
#                         new_paths = [edge]
#                     paths = paths + new_paths
        
#         return paths

#     edges = { 
#         "N1_L" : [{"N1" : "N1_L_N1"}] , 
#         "N1_D" : [{"N1" : "N1_D_N1"}] , 
#         "N1" : [{"N1_L" : "N1_N1_L"} , {"N1_D" : "N1_N1_D"}, {"N2" : "N1_N2"}, {"N4" : "N1_N4"}],
#         "N2" : [{"N2_R" : "N2_N2_R"} , {"N2_D" : "N2_N2_D"}, {"N3" : "N2_N3"}, {"N1" : "N2_N1"}],
#         "N2_R" : [{"N2" : "N2_R_N2"}] ,
#         "N2_D" : [{"N2" : "N2_D_N2"}] ,
#         "N3" : [{"N3_U" : "N3_N3_U"} , {"N3_R" : "N3_N3_R"}, {"N2" : "N3_N2"}, {"N4" : "N3_N4"}],
#         "N3_U" : [{"N3" : "N3_U_N3"}] ,
#         "N3_R" : [{"N3" : "N3_R_N3"}] ,
#         "N4" : [{"N4_U" : "N4_N4_U"}, {"N4_L" : "N4_N4_L"}, {"N1" : "N4_N1"} , {"N3" : "N4_N3"}],
#         "N4_U" : [{"N4" : "N4_U_N4"}] ,
#         "N4_L" : [{"N4" : "N4_L_N4"}],
#         }

#     visited = {}

#     sources = ["N1_L","N1_D","N2_D","N2_R","N3_R","N3_U","N4_U","N4_L"]

#     paths = []

#     for source in sources:
#         reset_visited(edges,visited)
#         paths = paths + dfs(edges,source,visited)

#     for path in paths:
#         edges = path.split(" ")
#         route_id = edges[0] + "_" + edges[-1]
#         route = f"""<route id={route_id} edges={path}/>"""
#         with open("routes.txt","a") as f:
#             print(route,file=f)
    
    
# gen_routes()