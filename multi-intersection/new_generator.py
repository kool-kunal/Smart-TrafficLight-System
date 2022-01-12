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

            <route id="r_0_0" edges="N1_L_N1 N1_N2 N2_N2_R"/>
            <route id="r_0_1" edges="N3_U_N3 N3_N2 N2_N2_D"/>
            <route id="r_0_2" edges="N4_L_N4 N4_N3 N3_N3_R"/>
            <route id="r_0_3" edges="N4_U_N4 N4_N1 N1_N1_D"/>
            <route id="r_1_4" edges="N1_D_N1 N1_N1_L"/>
            <route id="r_1_5" edges="N1_D_N1 N1_N2 N2_N2_R"/>
            <route id="r_1_6" edges="N1_L_N1 N1_N1_D"/>
            <route id="r_1_7" edges="N1_L_N1 N1_N2 N2_N2_D"/>
            <route id="r_1_8" edges="N2_D_N2 N2_N2_R"/>
            <route id="r_1_9" edges="N2_R_N2 N2_N2_D"/>
            <route id="r_1_10" edges="N3_R_N3 N3_N2 N2_N2_D"/>
            <route id="r_1_11" edges="N3_R_N3 N3_N3_U"/>
            <route id="r_1_12" edges="N3_U_N3 N3_N2 N2_N2_R"/>
            <route id="r_1_13" edges="N3_U_N3 N3_N3_R"/>
            <route id="r_1_14" edges="N4_L_N4 N4_N1 N1_N1_D"/>
            <route id="r_1_15" edges="N4_L_N4 N4_N3 N3_N2 N2_N2_D"/>
            <route id="r_1_16" edges="N4_L_N4 N4_N3 N3_N3_U"/>
            <route id="r_1_17" edges="N4_L_N4 N4_N4_U"/>
            <route id="r_1_18" edges="N4_U_N4 N4_N1 N1_N1_L"/>
            <route id="r_1_19" edges="N4_U_N4 N4_N1 N1_N2 N2_N2_R"/>
            <route id="r_1_20" edges="N4_U_N4 N4_N3 N3_N3_R"/>
            <route id="r_1_21" edges="N4_U_N4 N4_N4_L"/>
            <route id="r_2_22" edges="N1_D_N1 N1_N2 N2_N2_D"/>
            <route id="r_2_23" edges="N1_D_N1 N1_N4 N4_N3 N3_N3_R"/>
            <route id="r_2_24" edges="N1_D_N1 N1_N4 N4_N4_L"/>
            <route id="r_2_25" edges="N1_D_N1 N1_N4 N4_N4_U"/>
            <route id="r_2_26" edges="N1_L_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_2_27" edges="N1_L_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_2_28" edges="N1_L_N1 N1_N4 N4_N3 N3_N3_R"/>
            <route id="r_2_29" edges="N1_L_N1 N1_N4 N4_N4_L"/>
            <route id="r_2_30" edges="N1_L_N1 N1_N4 N4_N4_U"/>
            <route id="r_2_31" edges="N2_D_N2 N2_N1 N1_N1_D"/>
            <route id="r_2_32" edges="N2_D_N2 N2_N1 N1_N1_L"/>
            <route id="r_2_33" edges="N2_D_N2 N2_N3 N3_N3_R"/>
            <route id="r_2_34" edges="N2_D_N2 N2_N3 N3_N3_U"/>
            <route id="r_2_35" edges="N2_R_N2 N2_N1 N1_N1_D"/>
            <route id="r_2_36" edges="N2_R_N2 N2_N1 N1_N1_L"/>
            <route id="r_2_37" edges="N2_R_N2 N2_N3 N3_N3_R"/>
            <route id="r_2_38" edges="N2_R_N2 N2_N3 N3_N3_U"/>
            <route id="r_2_39" edges="N3_R_N3 N3_N2 N2_N2_R"/>
            <route id="r_2_40" edges="N3_R_N3 N3_N4 N4_N1 N1_N1_D"/>
            <route id="r_2_41" edges="N3_R_N3 N3_N4 N4_N4_L"/>
            <route id="r_2_42" edges="N3_R_N3 N3_N4 N4_N4_U"/>
            <route id="r_2_43" edges="N3_U_N3 N3_N2 N2_N1 N1_N1_D"/>
            <route id="r_2_44" edges="N3_U_N3 N3_N2 N2_N1 N1_N1_L"/>
            <route id="r_2_45" edges="N3_U_N3 N3_N4 N4_N1 N1_N1_D"/>
            <route id="r_2_46" edges="N3_U_N3 N3_N4 N4_N4_L"/>
            <route id="r_2_47" edges="N3_U_N3 N3_N4 N4_N4_U"/>
            <route id="r_2_48" edges="N4_L_N4 N4_N1 N1_N1_L"/>
            <route id="r_2_49" edges="N4_L_N4 N4_N1 N1_N2 N2_N2_R"/>
            <route id="r_2_50" edges="N4_L_N4 N4_N3 N3_N2 N2_N2_R"/>
            <route id="r_2_51" edges="N4_U_N4 N4_N1 N1_N2 N2_N2_D"/>
            <route id="r_2_52" edges="N4_U_N4 N4_N3 N3_N2 N2_N2_D"/>
            <route id="r_2_53" edges="N4_U_N4 N4_N3 N3_N3_U"/>
            <route id="r_3_54" edges="N1_D_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_3_55" edges="N1_D_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_3_56" edges="N1_D_N1 N1_N4 N4_N3 N3_N2 N2_N2_D"/>
            <route id="r_3_57" edges="N1_D_N1 N1_N4 N4_N3 N3_N3_U"/>
            <route id="r_3_58" edges="N1_L_N1 N1_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_3_59" edges="N1_L_N1 N1_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_3_60" edges="N1_L_N1 N1_N4 N4_N3 N3_N2 N2_N2_D"/>
            <route id="r_3_61" edges="N1_L_N1 N1_N4 N4_N3 N3_N3_U"/>
            <route id="r_3_62" edges="N2_D_N2 N2_N1 N1_N4 N4_N3 N3_N3_R"/>
            <route id="r_3_63" edges="N2_D_N2 N2_N1 N1_N4 N4_N4_L"/>
            <route id="r_3_64" edges="N2_D_N2 N2_N1 N1_N4 N4_N4_U"/>
            <route id="r_3_65" edges="N2_D_N2 N2_N3 N3_N4 N4_N1 N1_N1_D"/>
            <route id="r_3_66" edges="N2_D_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_3_67" edges="N2_D_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_3_68" edges="N2_R_N2 N2_N1 N1_N4 N4_N3 N3_N3_R"/>
            <route id="r_3_69" edges="N2_R_N2 N2_N1 N1_N4 N4_N4_L"/>
            <route id="r_3_70" edges="N2_R_N2 N2_N1 N1_N4 N4_N4_U"/>
            <route id="r_3_71" edges="N2_R_N2 N2_N3 N3_N4 N4_N1 N1_N1_D"/>
            <route id="r_3_72" edges="N2_R_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_3_73" edges="N2_R_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_3_74" edges="N3_R_N3 N3_N2 N2_N1 N1_N1_D"/>
            <route id="r_3_75" edges="N3_R_N3 N3_N2 N2_N1 N1_N1_L"/>
            <route id="r_3_76" edges="N3_R_N3 N3_N4 N4_N1 N1_N1_L"/>
            <route id="r_3_77" edges="N3_R_N3 N3_N4 N4_N1 N1_N2 N2_N2_R"/>
            <route id="r_3_78" edges="N3_U_N3 N3_N2 N2_N1 N1_N4 N4_N4_L"/>
            <route id="r_3_79" edges="N3_U_N3 N3_N2 N2_N1 N1_N4 N4_N4_U"/>
            <route id="r_3_80" edges="N3_U_N3 N3_N4 N4_N1 N1_N1_L"/>
            <route id="r_3_81" edges="N3_U_N3 N3_N4 N4_N1 N1_N2 N2_N2_R"/>
            <route id="r_3_82" edges="N4_L_N4 N4_N1 N1_N2 N2_N2_D"/>
            <route id="r_3_83" edges="N4_L_N4 N4_N3 N3_N2 N2_N1 N1_N1_D"/>
            <route id="r_3_84" edges="N4_L_N4 N4_N3 N3_N2 N2_N1 N1_N1_L"/>
            <route id="r_3_85" edges="N4_U_N4 N4_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_3_86" edges="N4_U_N4 N4_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_3_87" edges="N4_U_N4 N4_N3 N3_N2 N2_N2_R"/>
            <route id="r_4_88" edges="N1_D_N1 N1_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_4_89" edges="N1_D_N1 N1_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_4_90" edges="N1_D_N1 N1_N4 N4_N3 N3_N2 N2_N2_R"/>
            <route id="r_4_91" edges="N1_L_N1 N1_N4 N4_N3 N3_N2 N2_N2_R"/>
            <route id="r_4_92" edges="N2_D_N2 N2_N1 N1_N4 N4_N3 N3_N3_U"/>
            <route id="r_4_93" edges="N2_D_N2 N2_N3 N3_N4 N4_N1 N1_N1_L"/>
            <route id="r_4_94" edges="N2_R_N2 N2_N1 N1_N4 N4_N3 N3_N3_U"/>
            <route id="r_4_95" edges="N2_R_N2 N2_N3 N3_N4 N4_N1 N1_N1_L"/>
            <route id="r_4_96" edges="N3_R_N3 N3_N2 N2_N1 N1_N4 N4_N4_L"/>
            <route id="r_4_97" edges="N3_R_N3 N3_N2 N2_N1 N1_N4 N4_N4_U"/>
            <route id="r_4_98" edges="N3_R_N3 N3_N4 N4_N1 N1_N2 N2_N2_D"/>
            <route id="r_4_99" edges="N3_U_N3 N3_N4 N4_N1 N1_N2 N2_N2_D"/>
            <route id="r_4_100" edges="N4_L_N4 N4_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_4_101" edges="N4_L_N4 N4_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_4_102" edges="N4_U_N4 N4_N3 N3_N2 N2_N1 N1_N1_D"/>
            <route id="r_4_103" edges="N4_U_N4 N4_N3 N3_N2 N2_N1 N1_N1_L"/>""", file=routes)

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
        
#         visited[curr]=False
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
#     reset_visited(edges,visited)
#     sources = ["N1_L","N1_D","N2_D","N2_R","N3_R","N3_U","N4_U","N4_L"]

#     paths = []

#     for source in sources:
#         # reset_visited(edges,visited)
#         paths = paths + dfs(edges,source,visited)

#     directions = {
#             "N1_N1_L" : "W",
#             "N1_L_N1" : "E",
#             "N1_N2" : "E",
#             "N2_N1" : "W",
#             "N1_N1_D" : "S",
#             "N1_D_N1" : "N",
#             "N1_N4" : "N",
#             "N4_N1" : "S",
#             "N2_N2_D" : "S",
#             "N2_D_N2" : "N",
#             "N2_R_N2" : "W",
#             "N2_N2_R" : "E",
#             "N2_N3" : "N",
#             "N3_N2" : "S",
#             "N3_N3_U" : "N",
#             "N3_U_N3" : "S",
#             "N3_N3_R" : "E",
#             "N3_R_N3" : "W",
#             "N3_N4" : "W",
#             "N4_N3" : "E",
#             "N4_N4_U" : "N",
#             "N4_U_N4" : "S",
#             "N4_L_N4" : "E",
#             "N4_N4_L" : "W"
#          }

#     routes = []

#     for path in paths:
#         edges = path.split(" ")
#         turn = 0
#         for i in range(1,len(edges)):
#             d = directions[edges[i]]
#             d_prev = directions[edges[i-1]]

#             if d=="N" or d=="S" and (d_prev == "W" or d_prev == "E"):
#                 turn = turn+1
#             elif d=="W" or d=="E" and (d_prev == "N" or d_prev=="S"):
#                 turn = turn +1
        
#         routes.append((turn,path))

#     routes = sorted(routes)
#     print(routes)

#     for id,route in enumerate(routes):
#         route_id = "r_" + str(route[0]) + "_" + str(id)
#         route = f"""<route id="{route_id}" edges="{route[1]}"/>"""
#         with open("routes.txt","a") as f:
#             print(route,file=f)
    
    
# gen_routes()