import gc
import logging
import time
from os.path import join
from matplotlib.dates import date2num
from matplotlib import pyplot as plt

logging.getLogger("matplotlib").setLevel(logging.ERROR)

LOGGER = logging.getLogger()

def save_graph(title, readings, location, xlabel = "time", ylabel = "temp", ):

    s = time.time()

    temps = []
    hums = []
    times = []
    for r in readings:
        temps.append(r.temp)
        hums.append(r.hum)
        times.append(r.time)

    dates = date2num(times)

    graphs = plt.figure(num=100, clear=True)
    #temps = graphs.add_subplot()
    plt.plot_date(dates, temps, linestyle='solid', fmt=".")
    graphs.autofmt_xdate()
    plt.ylim((70, 90))
    plt.title("Temperature")
    plt.grid()
    plt.savefig(join(location, "temps.png"))

    # Clear the current axes and figure, then close.
    graphs.clf()
    graphs.clear()
    plt.cla()
    plt.clf()
    plt.close(graphs)

    #hum = graphs.add_subplot()
    graphs = plt.figure(num=100, clear=True)
    plt.plot_date(dates, hums, linestyle='solid', fmt=".")
    graphs.autofmt_xdate()
    plt.ylim((70, 100))
    plt.title("Humidity")
    plt.savefig(join(location, "hum.png"))

    # Clear the current axes and figure, then close.
    graphs.clf()
    graphs.clear()
    plt.cla()
    plt.clf()
    plt.grid()
    plt.close(graphs)

    # prevents memory leak
    del dates, temps, hums, times
    gc.collect()

    LOGGER.debug(f"Generated graphs in {round(time.time()-s, 2)} seconds.")
