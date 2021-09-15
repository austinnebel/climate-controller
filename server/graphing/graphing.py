import gc
import logging
import time
from os.path import join
from matplotlib.dates import date2num
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

def plot_temps(temp_times, temps, location):

    graphs = plt.figure(num=100, clear=True)
    plt.plot_date(temp_times, temps, linestyle='solid', fmt=".")
    graphs.autofmt_xdate()
    plt.ylim((70, 90))
    plt.title("Temperature")
    plt.grid()
    plt.savefig(join(location, "temps.png"))

    close(graphs)

def plot_humidity(hum_times, hums, activation_times, location):
    """
    Plots a graph of humidity data, including humidifer activation times.

    Args:
        hum_times (list[datetime]): Times that correspond to each humidity value (x-axis)
        hums (float): Humidity values (y-axis)
        activation_times (list[datetime]): Times that the humidifier was activated.
        location (str): Location to save graph image.
    """
    graphs = plt.figure(num=100, clear=True)
    plt.plot_date(hum_times, hums, linestyle='solid', fmt=".")

    # plots vertical line at each activation time
    for t in activation_times:
        plt.axvline(t)

    graphs.autofmt_xdate()
    plt.ylim((70, 100))
    plt.title("Humidity")
    plt.grid()
    plt.savefig(join(location, "hum.png"))

    close(graphs)

def generate_graphs(readings, humidifier_times, location):
    """
    Generates and saves graphs for temperature and humidity to .png files.

    Args:
        readings (list[Reading]): List of Reading objects to get data from.
        humidifier_times (list[datetime]): List of times that the humidifier was activated.
        location (str): Location to save .png files to.
    """
    s = time.time()

    temps, hums, times = ([], [], [])
    for r in readings:
        temps.append(r.temp)
        hums.append(r.hum)
        times.append(r.time)

    dates = date2num(times)

    plot_temps(times, temps, location)
    plot_humidity(times, hums, humidifier_times, location)

    # prevents memory leak
    del dates, temps, hums, times
    gc.collect()

    LOGGER.debug(f"Generated graphs in {round(time.time()-s, 2)} seconds.")
