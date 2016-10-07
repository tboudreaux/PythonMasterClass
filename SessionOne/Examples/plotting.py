import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from matplotlib.colors import LogNorm
import pandas as pd
import numpy as np


"""
Matplotlib section
    Advantages to Matplotlib
        Basically universal in python plotting
        Large support base
        support for GUIs and interaction

"""


def update_plot(event):     # takes slider event (think about like namespace)
    global ax, a, Spec, data_state, fill_state      # lazy code, but here to allow easy interaction with other objects
    if data_state is True:
        a.set_ydata(Spec['amp'] * ApInc.val)  # change the data in y based on the current slider value

        if fill_state is True:
            for coll in ax.collections:
                ax.collections.remove(coll)
            ax.collections.remove(ax.collections[0])
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                    facecolor='red', interpolate=True, alpha=0.5)
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                    where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)

        if ApInc.val < 0.2:
            ax.set_ylim([min(Spec['amp']*0.02), max(Spec['amp']*0.02)])  # change the scaling on the y axis
        elif ApInc.val >= 0.2:
            ax.set_ylim([min(Spec['amp']), max(Spec['amp'])])  # change the scaling on the y axis
        plt.draw()  # redraw the plot
    else:
        pass


def toggle_data(event):
    global ax, a, Spec, data_state
    if data_state is True:
        a.set_ydata([])
        a.set_xdata([])
        plt.draw()
        data_state = False
    else:
        a.set_ydata(Spec['amp'] * ApInc.val)
        a.set_xdata(Spec['freq'])
        plt.draw()
        data_state = True


def toggle_fill(event):
    global ax, a, Spec, fill_state
    if fill_state is True:
        for coll in ax.collections:
            ax.collections.remove(coll)
        fill_state = False
        ax.collections.remove(ax.collections[0])
    else:
        ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                facecolor='red', interpolate=True, alpha=0.5)
        ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)
        fill_state = True
    plt.draw()


def toggle_all(event):
    global ax, Spec, fill_state, data_state, a
    if data_state is True:
        if fill_state is True:
            for coll in ax.collections:
                ax.collections.remove(coll)
            ax.collections.remove(ax.collections[0])
            fill_state = False
        a.set_ydata([])
        a.set_xdata([])
        plt.draw()
        data_state = False

    else:
        if fill_state is False:
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                    facecolor='red', interpolate=True, alpha=0.5)
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                    where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)
            fill_state = True
        a.set_ydata(Spec['amp'] * ApInc.val)
        a.set_xdata(Spec['freq'])
        plt.draw()
        data_state = True


def onclick(event):
    global ax, a, Spec, data_state, b
    if data_state is True:
        if b is None:
            b, = ax.plot([event.xdata], [event.ydata], 'D')
        else:
            b.set_ydata([event.ydata])
            b.set_xdata([event.xdata])
    plt.draw()

spectrum1_name = '../Data/testspectrum.tsv'     # Path name to data

Spec = pd.read_csv(spectrum1_name, delimiter='\t', names=['freq', 'amp'])       # Read in data

Spec['amp'] = [(x/np.mean(Spec['amp']))-1 for x in Spec['amp']]  # Mean normalize the amplitude using list comprehension
Spec['freq'] = [x * 1*10**6 for x in Spec['freq']]  # convert units o Hz to micro hertz using list comprehension

fig = plt.figure(figsize=(10, 7))       # Define a figure of a fixed size (inches theoretically)

ax = fig.add_subplot(111)       # add axes (what you draw your plot on) to the figure
a, = ax.plot(Spec['freq'], Spec['amp'], 'o-',  label='Data')       # Plot data
ax.legend()     # toggle legend on
ax.grid()       # toggle grid lines on
ax.axvline(x=8200, linestyle='-.', color='r')       # add a vertical line at specified x
ax.axhline(y=1.5*10**-15, linestyle='--', color='g')        # Add a horizontal line at specified y

                # xpos  ypos xwidth ywidth
axApp = plt.axes([0.25, 0.01, 0.65, 0.01])      # define a new set of axes (some box to do stuff on)
ApInc = plt.Slider(axApp, 'Scaling', 0.001, 2, valinit=1, dragging=True)  # slave a slider to those axis -- between 0, 2 start 1
ApInc.on_changed(update_plot)   # when slider changes call update_plot function

data_state = True
fill_state = True

axButton1 = plt.axes([0.915, 0.5, 0.075, 0.1])      # define a new set of axes (some box to do stuff on)
bToggle_curve = plt.Button(axButton1, 'Curve')  # slave a slider to those axis -- between 0, 2 start 1
bToggle_curve.on_clicked(toggle_data)   # when slider changes call update_plot function


axButton2 = plt.axes([0.915, 0.75, 0.075, 0.1])      # define a new set of axes (some box to do stuff on)
bToggle_fill = plt.Button(axButton2, 'Fill')  # slave a slider to those axis -- between 0, 2 start 1
bToggle_fill.on_clicked(toggle_fill)   # when slider changes call update_plot function


axButton3 = plt.axes([0.915, 0.25, 0.075, 0.1])      # define a new set of axes (some box to do stuff on)
bToggle_all = plt.Button(axButton3, 'All')  # slave a slider to those axis -- between 0, 2 start 1
bToggle_all.on_clicked(toggle_all)   # when slider changes call update_plot function


ax.set_xlabel('Frequency (' + u'\u00B5' + 'Hz)')    # x label including unicode character
ax.set_ylabel('Amplitude')
ax.set_title('FT of some GALEX target')


ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                facecolor='red', interpolate=True, alpha=0.5)
ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)

b = None

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()  # Display graph object
