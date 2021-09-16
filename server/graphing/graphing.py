import logging
import time
from os.path import join
from matplotlib.dates import DateFormatter
from matplotlib import pyplot as plt

logging.getLogger("matplotlib").setLevel(logging.ERROR)

LOGGER = logging.getLogger()


def close(fig):
    """
    Clears the provided figure, then closes.

    Args:
        fig (matplotlib.figure): Figure to close.
    """
    fig.clf()
    fig.clear()
    plt.cla()
    plt.clf()
    plt.close(fig)

def plot_temps(axes, temp_times, temps):
    """
    Plots a graph of temperature data.

    Args:
        axes (matplotlib.axes): Subplot to graph on.
        temp_times (list[datetime]): Times that correspond to each humidity value (x-axis)
        temps (float): Temperature values (y-axis)
    """
    axes.plot_date(temp_times, temps, linestyle='solid', fmt=".")
    axes.set_ylim((70, 90))
    axes.set_title("Temperature")
    axes.grid()

def plot_humidity(axes, hum_times, hums, activation_times):
    """
    Plots a graph of humidity data, including humidifer activation times.

    Args:
        axes (matplotlib.axes): Subplot to graph on.
        hum_times (list[datetime]): Times that correspond to each humidity value (x-axis)
        hums (float): Humidity values (y-axis)
        activation_times (list[datetime]): Times that the humidifier was activated.
    """
    axes.plot_date(hum_times, hums, linestyle='solid', fmt=".")

    # plots vertical line at each activation time
    LOGGER.debug(f"Plotting {len(activation_times)} humidifier activation times: {activation_times}")
    for t in activation_times:
        axes.axvline(t, color = "orange")

    axes.set_ylim((70, 100))
    axes.set_title("Humidity")
    axes.grid()

def generate_graphs(readings, humidifier_times, location):
    """
    Generates and saves graphs for temperature and humidity to .png files.

    Args:
        readings (list[Reading]): List of Reading objects to get data from.
        humidifier_times (list[datetime]): List of times that the humidifier was activated.
        location (str): Location to save .png files to.

    Ref: https://medium.com/@kapil.mathur1987/matplotlib-an-introduction-to-its-object-oriented-interface-a318b1530aed
    """
    s = time.time()

    temps, hums, times = ([], [], [])
    for r in readings:
        temps.append(r.temp)
        hums.append(r.hum)
        times.append(r.time)

    # create a single plotting figure of size 6x11, add 2 subplots at position 1 and 2 with 1 column & 2 rows
    fig = plt.figure(num=100, clear=True, figsize=(6, 10))
    temp_graph = fig.add_subplot(2,1,1, adjustable='box')
    hum_graph = fig.add_subplot(2,1,2, adjustable='box')



    # formats axes
    xformatter = DateFormatter('%H:%M')
    temp_graph.xaxis.set_major_formatter(xformatter)
    hum_graph.xaxis.set_major_formatter(xformatter)
    temp_graph.yaxis.set_major_formatter("{x}°F")
    hum_graph.yaxis.set_major_formatter("{x}%")


    plot_temps(temp_graph, times, temps)
    plot_humidity(hum_graph, times, hums, humidifier_times)

    #temp_graph.set_yticklabels([f"{x}°F" for x in temp_graph.get_yticks()])
    #hum_graph.set_yticklabels([f"{x}%" for x in hum_graph.get_yticks()])

    fig.savefig(join(location, "graphs.png"))
    fig.clear()

    LOGGER.debug(f"Generated graphs in {round(time.time()-s, 2)} seconds.")
