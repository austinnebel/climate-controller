import logging
import time
from os.path import join
from matplotlib.dates import DateFormatter
from matplotlib import pyplot as plt

logging.getLogger("matplotlib").setLevel(logging.ERROR)

LOGGER = logging.getLogger()


def plot_temps(axes, temp_times, temps, heatmat, lamp):
    """
    Plots a graph of temperature data.

    Args:
        axes (matplotlib.axes): Subplot to graph on.
        temp_times (list[datetime]): Times that correspond to each humidity value (x-axis)
        temps (float): Temperature values (y-axis)
        heatmat (RelayDevice): RelayDevice object that controls the heat mat.
        lamp (RelayDevice): RelayDevice object that controls the heat lamp.
    """
    axes.plot_date(temp_times, temps, linestyle='solid', fmt=".")

    for t in heatmat.activations:
        axes.axvline(t, color = "orange")
    for t in heatmat.deactivations:
        axes.axvline(t, color = "blue")
    for t in lamp.activations:
        axes.axvline(t, color = "red")
    for t in lamp.deactivations:
        axes.axvline(t, color = "purple")

    axes.set_ylim((70, 90))
    axes.set_title("Temperature", fontsize=20)
    axes.grid()

def plot_humidity(axes, hum_times, hums, activation_times):
    """
    Plots a graph of humidity data, including humidifier activation times.

    Args:
        axes (matplotlib.axes): Subplot to graph on.
        hum_times (list[datetime]): Times that correspond to each humidity value (x-axis)
        hums (float): Humidity values (y-axis)
        activation_times (list[datetime]): Times that the humidifier was activated.
    """
    axes.plot_date(hum_times, hums, linestyle='solid', fmt=".")

    # plots vertical line at each activation time
    for t in activation_times:
        axes.axvline(t, color = "orange")

    axes.set_ylim((60, 100))
    axes.set_title("Humidity", fontsize=20)
    axes.grid()

def generate_graphs(readings, heatmat, lamp, humidifier, location):
    """
    Generates and saves graphs for temperature and humidity to .png files.

    Args:
        readings (list[Reading]): List of Reading objects to get data from.
        heatmat (RelayDevice): RelayDevice object that controls the heat mat.
        lamp (RelayDevice): RelayDevice object that controls the heat lamp.
        humidifier (RelayDevice): RelayDevice object that controls the humidifier.
        location (str): Location to save .png files to.

    Ref: https://medium.com/@kapil.mathur1987/matplotlib-an-introduction-to-its-object-oriented-interface-a318b1530aed
    """
    s = time.time()

    # add provided past readings to separated lists
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


    plot_temps(temp_graph, times, temps, heatmat, lamp)
    plot_humidity(hum_graph, times, hums, humidifier.activations)

    # save figure to png file, clear figure to save memory
    fig.savefig(join(location, "graphs.png"))
    fig.clear()

    LOGGER.debug(f"Generated graphs in {round(time.time()-s, 2)} seconds.")
