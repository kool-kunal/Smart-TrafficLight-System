from __future__ import print_function
import matplotlib.pyplot as plt

# def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.svg'):
#     """ Plots the population's average and best fitness. """
#     if plt is None:
#         warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
#         return

#     generation = range(len(statistics.most_fit_genomes))
#     best_fitness = [c.fitness for c in statistics.most_fit_genomes]
#     avg_fitness = np.array(statistics.get_fitness_mean())
#     stdev_fitness = np.array(statistics.get_fitness_stdev())

#     plt.plot(generation, avg_fitness, 'b-', label="average")
#     plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
#     plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
#     plt.plot(generation, best_fitness, 'r-', label="best")

#     plt.title("Population's average and best fitness")
#     plt.xlabel("Generations")
#     plt.ylabel("Fitness")
#     plt.grid()
#     plt.legend(loc="best")
#     if ylog:
#         plt.gca().set_yscale('symlog')

#     plt.savefig(filename)
#     if view:
#         plt.show()

#     plt.close()


# def plot_spikes(spikes, view=False, filename=None, title=None):
#     """ Plots the trains for a single spiking neuron. """
#     t_values = [t for t, I, v, u, f in spikes]
#     v_values = [v for t, I, v, u, f in spikes]
#     u_values = [u for t, I, v, u, f in spikes]
#     I_values = [I for t, I, v, u, f in spikes]
#     f_values = [f for t, I, v, u, f in spikes]

#     fig = plt.figure()
#     plt.subplot(4, 1, 1)
#     plt.ylabel("Potential (mv)")
#     plt.xlabel("Time (in ms)")
#     plt.grid()
#     plt.plot(t_values, v_values, "g-")

#     if title is None:
#         plt.title("Izhikevich's spiking neuron model")
#     else:
#         plt.title("Izhikevich's spiking neuron model ({0!s})".format(title))

#     plt.subplot(4, 1, 2)
#     plt.ylabel("Fired")
#     plt.xlabel("Time (in ms)")
#     plt.grid()
#     plt.plot(t_values, f_values, "r-")

#     plt.subplot(4, 1, 3)
#     plt.ylabel("Recovery (u)")
#     plt.xlabel("Time (in ms)")
#     plt.grid()
#     plt.plot(t_values, u_values, "r-")

#     plt.subplot(4, 1, 4)
#     plt.ylabel("Current (I)")
#     plt.xlabel("Time (in ms)")
#     plt.grid()
#     plt.plot(t_values, I_values, "r-o")

#     if filename is not None:
#         plt.savefig(filename)

#     if view:
#         plt.show()
#         plt.close()
#         fig = None

#     return fig


# def plot_species(statistics, view=False, filename='speciation.svg'):
#     """ Visualizes speciation throughout evolution. """
#     if plt is None:
#         warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
#         return

#     species_sizes = statistics.get_species_sizes()
#     num_generations = len(species_sizes)
#     curves = np.array(species_sizes).T

#     fig, ax = plt.subplots()
#     ax.stackplot(range(num_generations), *curves)

#     plt.title("Speciation")
#     plt.ylabel("Size per Species")
#     plt.xlabel("Generations")

#     plt.savefig(filename)

#     if view:
#         plt.show()

#     plt.close()


# def draw_net(config, genome, view=False, filename=None, node_names=None, show_disabled=True, prune_unused=False,
#              node_colors=None, fmt='svg'):
#     # Attributes for network nodes.
#     if graphviz is None:
#         warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
#         return

#     if node_names is None:
#         node_names = {}

#     assert type(node_names) is dict

#     if node_colors is None:
#         node_colors = {}

#     assert type(node_colors) is dict

#     node_attrs = {
#         'shape': 'circle',
#         'fontsize': '9',
#         'height': '0.2',
#         'width': '0.2'}

#     dot = graphviz.Digraph(format=fmt, node_attr=node_attrs)

#     inputs = set()
#     for k in config.genome_config.input_keys:
#         inputs.add(k)
#         name = node_names.get(k, str(k))
#         input_attrs = {'style': 'filled', 'shape': 'box', 'fillcolor': node_colors.get(k, 'lightgray')}
#         dot.node(name, _attributes=input_attrs)

#     outputs = set()
#     for k in config.genome_config.output_keys:
#         outputs.add(k)
#         name = node_names.get(k, str(k))
#         node_attrs = {'style': 'filled', 'fillcolor': node_colors.get(k, 'lightblue')}

#         dot.node(name, _attributes=node_attrs)

#     if prune_unused:
#         connections = set()
#         for cg in genome.connections.values():
#             if cg.enabled or show_disabled:
#                 connections.add((cg.in_node_id, cg.out_node_id))

#         used_nodes = copy.copy(outputs)
#         pending = copy.copy(outputs)
#         while pending:
#             new_pending = set()
#             for a, b in connections:
#                 if b in pending and a not in used_nodes:
#                     new_pending.add(a)
#                     used_nodes.add(a)
#             pending = new_pending
#     else:
#         used_nodes = set(genome.nodes.keys())

#     for n in used_nodes:
#         if n in inputs or n in outputs:
#             continue

#         attrs = {'style': 'filled',
#                  'fillcolor': node_colors.get(n, 'white')}
#         dot.node(str(n), _attributes=attrs)

#     for cg in genome.connections.values():
#         if cg.enabled or show_disabled:
#             input, output = cg.key
#             a = node_names.get(input, str(input))
#             b = node_names.get(output, str(output))
#             style = 'solid' if cg.enabled else 'dotted'
#             color = 'green' if cg.weight > 0 else 'red'
#             width = str(0.1 + abs(cg.weight / 5.0))
#             dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

#     dot.render(filename, view=view)

#     return dot

# def bar_graph_plot(loss_1, loss_2,labels):
#     X = range(1, len(loss_1)+1)
#     # bar_width = 0.25
#     #fig = plt.subplots(figsize =(12, 8)) 
#     # br1 = X
#     # br2 = [x + bar_width for x in X]
    
#     plt.plot(X,loss_1, color = 'g', label = labels[0])
#     plt.plot(X,loss_2, color = 'b', label = labels[1])
    
#     plt.xlabel('episode')
#     plt.ylabel('loss')
    
#     # plt.xticks([x + bar_width for x in X], X)
    
#     plt.legend()
#     plt.show()

# def pi_chart_plot(loss_1,loss_2, labels):
#     counter = [int(0), int(0)]
#     for i in range(len(loss_1)):
#         if loss_1[i] < loss_2[i]:
#             counter[0]+=int(1)
#         else:
#             counter[1]+=int(1)
    
#     counter = tuple(counter)
#     labels = tuple(labels)
#     plt.pie(x=counter, labels=labels)
#     plt.legend()
#     plt.show()
        


from cmath import exp
import json
import matplotlib.pyplot as plt


def aggregate_line_plots(rms_waiting_time_loss_net, rms_waiting_time_loss_ttl, harmonic_mean_loss_net, harmonic_mean_loss_ttl, average_queue_length_net, average_queue_length_ttl, average_waiting_time_net, average_waiting_time_ttl, dir_path):
    X = range(1, len(rms_waiting_time_loss_net)+1)
    plt.plot(X, rms_waiting_time_loss_net,
             color='springgreen', label='RMS WAITING TIME NET')
    plt.plot(X, rms_waiting_time_loss_ttl,
             color='darkslategrey', label='RMS WAITING TIME TTL')
    plt.plot(X, harmonic_mean_loss_net,
             color='springgreen', label='HARMONIC MEAN LOSS NET')
    plt.plot(X, harmonic_mean_loss_ttl,
             color='darkslategrey', label='HARMONIC MEAN LOSS TTL')
    plt.plot(X, average_queue_length_net,
             color='springgreen', label='AVERAGE QUEUE LENGTH NET')
    plt.plot(X, average_queue_length_ttl,
             color='darkslategrey', label='AVERAGE QUEUE LENGTH TTL')
    plt.plot(X, average_waiting_time_net,
             color='springgreen', label='AVERAGE WAITING TIME NET')
    plt.plot(X, average_waiting_time_ttl,
             color='darkslategrey', label='AVERAGE WAITING TIME TTL')

    plt.xlabel('episode')
    plt.ylabel('units')
    plt.legend()

    if dir_path:
        plt.savefig(dir_path + '/' + 'aggregated_line_plot' + ".png")


def line_graph_plot(loss_1, loss_2, labels, y_label, dir_path=None):
    X = range(1, len(loss_1)+1)
    plt.plot(X, loss_1, color='springgreen', label=labels[0])
    plt.plot(X, loss_2, color='darkslategrey', label=labels[1])

    plt.xlabel('episode')
    plt.ylabel(y_label)
    plt.legend()

    if dir_path:
        plt.savefig(dir_path + '/' + y_label + ".png")

    plt.show()


def pi_chart_plot(loss_1, loss_2, labels, dir_path=None):
    counter = [int(0), int(0)]
    for i in range(len(loss_1)):
        if loss_1[i] < loss_2[i]:
            counter[0] += int(1)
        else:
            counter[1] += int(1)

    counter = tuple(counter)
    labels = tuple(labels)
    explode = [0.1, 0.0]
    plt.pie(x=counter, labels=labels, autopct='%1.2f%%',
            explode=explode, colors=['springgreen', 'darkslategrey'])
    plt.legend()

    if dir_path:
        plt.savefig(dir_path + '/comaprison_plot.png')

    plt.show()


def generate_test_plots(dir_path):

    results = {}

    with open(dir_path + '/test_results.json', 'r') as f:
        results = json.load(f)

    rms_waiting_time_loss_net = [results[test]["net"]
                                 ["RMS_WAITING_TIME_LOSS"] for test in results]
    rms_waiting_time_loss_ttl = [results[test]["ttl"]
                                 ["RMS_WAITING_TIME_LOSS"] for test in results]
    harmonic_mean_loss_net = [results[test]["net"]
                              ["HARMONIC_MEAN_LOSS"] for test in results]
    harmonic_mean_loss_ttl = [results[test]["ttl"]
                              ["HARMONIC_MEAN_LOSS"] for test in results]
    average_queue_length_net = [results[test]["net"]
                                ["AVERAGE QUEUE LENGTH"] for test in results]
    average_queue_length_ttl = [results[test]["ttl"]
                                ["AVERAGE QUEUE LENGTH"] for test in results]
    average_waiting_time_net = [results[test]["net"]
                                ["AVERAGE WAITING TIME"] for test in results]
    average_waiting_time_ttl = [results[test]["ttl"]
                                ["AVERAGE WAITING TIME"] for test in results]

    line_graph_plot(rms_waiting_time_loss_net, rms_waiting_time_loss_ttl, [
                    "Net", "TTL"], "RMS_WAITING_TIME_LOSS", dir_path)
    line_graph_plot(harmonic_mean_loss_net, harmonic_mean_loss_ttl, [
                    "Net", "TTL"], "HARMONIC_MEAN_LOSS", dir_path)
    line_graph_plot(average_queue_length_net, average_queue_length_ttl, [
                    "Net", "TTL"], "AVERAGE QUEUE LENGTH", dir_path)
    line_graph_plot(average_waiting_time_net, average_waiting_time_ttl, [
                    "Net", "TTL"], "AVERAGE WAITING TIME", dir_path)

    pi_chart_plot(harmonic_mean_loss_net, harmonic_mean_loss_ttl,
                  ["Net", "TTL"], dir_path)
    aggregate_line_plots(rms_waiting_time_loss_net, rms_waiting_time_loss_ttl, harmonic_mean_loss_net, harmonic_mean_loss_ttl,
                         average_queue_length_net, average_queue_length_ttl, average_waiting_time_net, average_waiting_time_ttl, dir_path)
