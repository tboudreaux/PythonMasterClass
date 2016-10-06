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
    global ax, a, Spec      # lazy code, but here to allow easy interaction with other objects
    a.set_ydata(Spec['amp'] * (ApInc.val/500))  # change the data in y based on the current slider value
    # ax.set_ylim([0, max(Spec['amp']*ApInc.val/500)])  # change the scaling on the y axis
    plt.draw()  # redraw the plot

spectrum1_name = '../Data/testspectrum.tsv'     # Path name to data

Spec = pd.read_csv(spectrum1_name, delimiter='\t', names=['freq', 'amp'])       # Read in data

Spec['amp'] = [(x/np.mean(Spec['amp']))-1 for x in Spec['amp']]  # Mean normalize the amplitude using list comprehension
Spec['freq'] = [x * 1*10**6 for x in Spec['freq']]  # convert units o Hz to micro hertz using list comprehension

fig = plt.figure(figsize=(10, 7))       # Define a figure of a fixed size (inches theoretically)

ax = fig.add_subplot(111)       # add axes (what you draw your plot on) to the figure
a, = ax.plot(Spec['freq'], Spec['amp'], label='Data')       # Plot data
ax.legend()     # toggle legend on
ax.grid()       # toggle grid lines on
ax.axvline(x=8200, linestyle='-.', color='r')       # add a vertical line at specified x
ax.axhline(y=1.5*10**-15, linestyle='--', color='g')        # Add a horizontal line at specified y

axApp = plt.axes([0.25, 0.01, 0.65, 0.01])      # define a new set of axes (some box to do stuff on)
ApInc = plt.Slider(axApp, 'Scaling', 0, 1000, valinit=500)  # slave a slider to those axis -- between 0, 1000 start 500
ApInc.on_changed(update_plot)   # when slider changes call update_plot function


ax.set_xlabel('Frequency (' + u'\u00B5' + 'Hz)')    # x label including unicode character
ax.set_ylabel('Amplitude')
ax.set_title('FT of some GALEX target')
plt.show()  # Display graph object
