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
