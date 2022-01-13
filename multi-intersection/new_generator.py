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

            <route id="r_0_2_0" edges="N1_L_N1 N1_N2 N2_N2_R"/>
            <route id="r_0_2_1" edges="N2_D_N2 N2_N3 N3_N3_U"/>
            <route id="r_0_2_2" edges="N3_U_N3 N3_N2 N2_N2_D"/>
            <route id="r_0_2_3" edges="N4_U_N4 N4_N1 N1_N1_D"/>
            <route id="r_1_0_4" edges="N1_D_N1 N1_N1_L"/>
            <route id="r_1_0_5" edges="N1_L_N1 N1_N1_D"/>
            <route id="r_1_0_6" edges="N2_D_N2 N2_N2_R"/>
            <route id="r_1_0_7" edges="N2_R_N2 N2_N2_D"/>
            <route id="r_1_0_8" edges="N3_R_N3 N3_N3_U"/>
            <route id="r_1_0_9" edges="N3_U_N3 N3_N3_R"/>
            <route id="r_1_0_10" edges="N4_L_N4 N4_N4_U"/>
            <route id="r_1_0_11" edges="N4_U_N4 N4_N4_L"/>
            <route id="r_1_1_12" edges="N1_D_N1 N1_N2 N2_N2_R"/>
            <route id="r_1_1_13" edges="N1_L_N1 N1_N2 N2_N2_D"/>
            <route id="r_1_1_14" edges="N2_D_N2 N2_N3 N3_N3_R"/>
            <route id="r_1_1_15" edges="N2_R_N2 N2_N3 N3_N3_U"/>
            <route id="r_1_1_16" edges="N3_R_N3 N3_N2 N2_N2_D"/>
            <route id="r_1_1_17" edges="N3_U_N3 N3_N2 N2_N2_R"/>
            <route id="r_1_1_18" edges="N4_L_N4 N4_N1 N1_N1_D"/>
            <route id="r_1_1_19" edges="N4_U_N4 N4_N1 N1_N1_L"/>
            <route id="r_1_2_20" edges="N1_L_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_1_2_21" edges="N2_D_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_1_2_22" edges="N3_U_N3 N3_N2 N2_N1 N1_N1_L"/>
            <route id="r_1_2_23" edges="N4_U_N4 N4_N1 N1_N2 N2_N2_R"/>
            <route id="r_2_0_24" edges="N1_D_N1 N1_N2 N2_N2_D"/>
            <route id="r_2_0_25" edges="N2_R_N2 N2_N3 N3_N3_R"/>
            <route id="r_2_0_26" edges="N3_R_N3 N3_N2 N2_N2_R"/>
            <route id="r_2_0_27" edges="N4_L_N4 N4_N1 N1_N1_L"/>
            <route id="r_2_1_28" edges="N1_D_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_2_1_29" edges="N1_L_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_2_1_30" edges="N2_D_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_2_1_31" edges="N2_R_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_2_1_32" edges="N3_R_N3 N3_N2 N2_N1 N1_N1_L"/>
            <route id="r_2_1_33" edges="N3_U_N3 N3_N2 N2_N1 N1_N1_D"/>
            <route id="r_2_1_34" edges="N4_L_N4 N4_N1 N1_N2 N2_N2_R"/>
            <route id="r_2_1_35" edges="N4_U_N4 N4_N1 N1_N2 N2_N2_D"/>
            <route id="r_2_2_36" edges="N1_L_N1 N1_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_2_2_37" edges="N2_D_N2 N2_N3 N3_N4 N4_N1 N1_N1_D"/>
            <route id="r_2_2_38" edges="N3_U_N3 N3_N2 N2_N1 N1_N4 N4_N4_U"/>
            <route id="r_2_2_39" edges="N4_U_N4 N4_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_3_0_40" edges="N1_D_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_3_0_41" edges="N2_R_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_3_0_42" edges="N3_R_N3 N3_N2 N2_N1 N1_N1_D"/>
            <route id="r_3_0_43" edges="N4_L_N4 N4_N1 N1_N2 N2_N2_D"/>
            <route id="r_3_1_44" edges="N1_D_N1 N1_N2 N2_N3 N3_N4 N4_N4_L"/>
            <route id="r_3_1_45" edges="N1_L_N1 N1_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_3_1_46" edges="N2_D_N2 N2_N3 N3_N4 N4_N1 N1_N1_L"/>
            <route id="r_3_1_47" edges="N2_R_N2 N2_N3 N3_N4 N4_N1 N1_N1_D"/>
            <route id="r_3_1_48" edges="N3_R_N3 N3_N2 N2_N1 N1_N4 N4_N4_U"/>
            <route id="r_3_1_49" edges="N3_U_N3 N3_N2 N2_N1 N1_N4 N4_N4_L"/>
            <route id="r_3_1_50" edges="N4_L_N4 N4_N1 N1_N2 N2_N3 N3_N3_U"/>
            <route id="r_3_1_51" edges="N4_U_N4 N4_N1 N1_N2 N2_N3 N3_N3_R"/>
            <route id="r_4_0_52" edges="N1_D_N1 N1_N2 N2_N3 N3_N4 N4_N4_U"/>
            <route id="r_4_0_53" edges="N2_R_N2 N2_N3 N3_N4 N4_N1 N1_N1_L"/>
            <route id="r_4_0_54" edges="N3_R_N3 N3_N2 N2_N1 N1_N4 N4_N4_L"/>
            <route id="r_4_0_55" edges="N4_L_N4 N4_N1 N1_N2 N2_N3 N3_N3_R"/>""", file=routes)

            id_list = ['r_0_2_0', 'r_0_2_1', 'r_0_2_2', 'r_0_2_3', 'r_1_0_4', 'r_1_0_5', 'r_1_0_6', 'r_1_0_7', 'r_1_0_8', 'r_1_0_9', 'r_1_0_10', 'r_1_0_11', 'r_1_1_12', 'r_1_1_13', 'r_1_1_14', 'r_1_1_15', 'r_1_1_16', 'r_1_1_17', 'r_1_1_18', 'r_1_1_19', 'r_1_2_20', 'r_1_2_21', 'r_1_2_22', 'r_1_2_23', 'r_2_0_24', 'r_2_0_25', 'r_2_0_26', 'r_2_0_27',
                       'r_2_1_28', 'r_2_1_29', 'r_2_1_30', 'r_2_1_31', 'r_2_1_32', 'r_2_1_33', 'r_2_1_34', 'r_2_1_35', 'r_2_2_36', 'r_2_2_37', 'r_2_2_38', 'r_2_2_39', 'r_3_0_40', 'r_3_0_41', 'r_3_0_42', 'r_3_0_43', 'r_3_1_44', 'r_3_1_45', 'r_3_1_46', 'r_3_1_47', 'r_3_1_48', 'r_3_1_49', 'r_3_1_50', 'r_3_1_51', 'r_4_0_52', 'r_4_0_53', 'r_4_0_54', 'r_4_0_55']
            for car_counter, step in enumerate(car_gen_steps):

                index = random.randint(0, len(id_list)-1)

                print('    <vehicle id="%i" type="standard_car" route="%s" depart="%s" departLane="random" departSpeed="10" />' %
                      (car_counter, id_list[index], step), file=routes)
                car_id_list.append(f'{car_counter}')

                # straight_or_turn = np.random.uniform()
                # if straight_or_turn < 0.75:  # choose direction: straight or turn - 75% of times the car goes straight
                #     # choose a random source & destination
                #     route_straight = np.random.randint(1, 5)
                #     if route_straight == 1:
                #         print('    <vehicle id="W_E_%i" type="standard_car" route="W_E" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'W_E_{car_counter}')
                #     elif route_straight == 2:
                #         print('    <vehicle id="E_W_%i" type="standard_car" route="E_W" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'E_W_{car_counter}')
                #     elif route_straight == 3:
                #         print('    <vehicle id="N_S_%i" type="standard_car" route="N_S" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'N_S_{car_counter}')
                #     else:
                #         print('    <vehicle id="S_N_%i" type="standard_car" route="S_N" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'S_N_{car_counter}')
                # else:  # car that turn -25% of the time the car turns
                #     # choose random source source & destination
                #     route_turn = np.random.randint(1, 9)
                #     if route_turn == 1:
                #         print('    <vehicle id="W_N_%i" type="standard_car" route="W_N" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'W_N_{car_counter}')
                #     elif route_turn == 2:
                #         print('    <vehicle id="W_S_%i" type="standard_car" route="W_S" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'W_S_{car_counter}')
                #     elif route_turn == 3:
                #         print('    <vehicle id="N_W_%i" type="standard_car" route="N_W" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'N_W_{car_counter}')
                #     elif route_turn == 4:
                #         print('    <vehicle id="N_E_%i" type="standard_car" route="N_E" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'N_E_{car_counter}')
                #     elif route_turn == 5:
                #         print('    <vehicle id="E_N_%i" type="standard_car" route="E_N" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'E_N_{car_counter}')
                #     elif route_turn == 6:
                #         print('    <vehicle id="E_S_%i" type="standard_car" route="E_S" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'E_S_{car_counter}')
                #     elif route_turn == 7:
                #         print('    <vehicle id="S_W_%i" type="standard_car" route="S_W" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'S_W_{car_counter}')
                #     elif route_turn == 8:
                #         print('    <vehicle id="S_E_%i" type="standard_car" route="S_E" depart="%s" departLane="random" departSpeed="10" />' %
                #               (car_counter, step), file=routes)
                #         car_id_list.append(f'S_E_{car_counter}')

            print("</routes>", file=routes)

        return car_id_list


# print(TrafficGenerator(600, 400).generate_routefile(0))

# def gen_routes():

#     def reset_visited(edges, visited):
#         for key in edges:
#             visited[key] = False

#     def dfs(edges, curr, visited):
#         visited[curr] = True

#         paths = []
#         for mapping in edges[curr]:
#             for neighbour, edge in mapping.items():
#                 if not visited[neighbour]:
#                     temp = dfs(edges, neighbour, visited)
#                     new_paths = []
#                     for path in temp:
#                         new_paths.append(edge + " " + path)
#                     if len(new_paths) == 0:
#                         new_paths = [edge]
#                     paths = paths + new_paths

#         return paths

#     edges = {
#         "N1_L": [{"N1": "N1_L_N1"}],
#         "N1_D": [{"N1": "N1_D_N1"}],
#         "N1": [{"N1_L": "N1_N1_L"}, {"N1_D": "N1_N1_D"}, {"N2": "N1_N2"}, {"N4": "N1_N4"}],
#         "N2": [{"N2_R": "N2_N2_R"}, {"N2_D": "N2_N2_D"}, {"N3": "N2_N3"}, {"N1": "N2_N1"}],
#         "N2_R": [{"N2": "N2_R_N2"}],
#         "N2_D": [{"N2": "N2_D_N2"}],
#         "N3": [{"N3_U": "N3_N3_U"}, {"N3_R": "N3_N3_R"}, {"N2": "N3_N2"}, {"N4": "N3_N4"}],
#         "N3_U": [{"N3": "N3_U_N3"}],
#         "N3_R": [{"N3": "N3_R_N3"}],
#         "N4": [{"N4_U": "N4_N4_U"}, {"N4_L": "N4_N4_L"}, {"N1": "N4_N1"}, {"N3": "N4_N3"}],
#         "N4_U": [{"N4": "N4_U_N4"}],
#         "N4_L": [{"N4": "N4_L_N4"}],
#     }

#     visited = {}
#     reset_visited(edges, visited)
#     sources = ["N1_L", "N1_D", "N2_D", "N2_R", "N3_R", "N3_U", "N4_U", "N4_L"]

#     paths = []

#     for source in sources:
#         reset_visited(edges,visited)
#         paths = paths + dfs(edges, source, visited)

#     directions = {
#         "N1_N1_L": "W",
#         "N1_L_N1": "E",
#         "N1_N2": "E",
#         "N2_N1": "W",
#         "N1_N1_D": "S",
#         "N1_D_N1": "N",
#         "N1_N4": "N",
#         "N4_N1": "S",
#         "N2_N2_D": "S",
#         "N2_D_N2": "N",
#         "N2_R_N2": "W",
#         "N2_N2_R": "E",
#         "N2_N3": "N",
#         "N3_N2": "S",
#         "N3_N3_U": "N",
#         "N3_U_N3": "S",
#         "N3_N3_R": "E",
#         "N3_R_N3": "W",
#         "N3_N4": "W",
#         "N4_N3": "E",
#         "N4_N4_U": "N",
#         "N4_U_N4": "S",
#         "N4_L_N4": "E",
#         "N4_N4_L": "W"
#     }

#     routes = []

#     for path in paths:
#         edges = path.split(" ")
#         turn = 0
#         straight = 0
#         for i in range(1, len(edges)):
#             d = directions[edges[i]]
#             d_prev = directions[edges[i-1]]

#             if (d == "N" or d == "S") and (d_prev == "W" or d_prev == "E"):
#                 turn = turn+1
#             elif (d == "W" or d == "E") and (d_prev == "N" or d_prev == "S"):
#                 turn = turn+1
#             else:
#                 straight = straight + 1

#         routes.append((turn, straight, path))

#     routes = sorted(routes)

#     id_list = []

#     for id, route in enumerate(routes):
#         route_id = "r_" + str(route[0]) + "_" + str(route[1]) + "_" + str(id)
#         route = f"""<route id="{route_id}" edges="{route[2]}"/>"""

#         id_list.append(route_id)
#         with open("routes.txt", "a") as f:
#             print(route, file=f)
#     return id_list

# id_list = gen_routes()
# print(id_list)
