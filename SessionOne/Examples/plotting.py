import matplotlib
matplotlib.use('Qt4Agg')        # If code is crashing on load comment out this line
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pandas as pd
import numpy as np


"""
Matplotlib section
    Advantages to Matplotlib:
        Basically universal in python plotting
        Large support base
        support for GUIs and interaction
        Quick to generate a plot
        fantastic documentation
        Nice looking plots
        very powerful
            you can basically do everything in matplot lib if you are willing to put enough time into setting it up
    Disadvantages:
        Some more complex functions can be hard to get used to -- wierd syntax
        Hard to store interactive version of plot
        Many backends can make incompatibility an issue sometimes
"""


def update_plot(event):     # takes slider event (think about like namespace)
    global ax, a, Spec, data_state, fill_state      # lazy code, but here to allow easy interaction with other objects
    if data_state is True:
        a.set_ydata(Spec['amp'] * ApInc.val)  # change the data in y based on the current slider value

        if fill_state is True:  # check if fill has been drawn
            for coll in ax.collections:
                ax.collections.remove(coll)     # remove all but the last element of the axes collection
            ax.collections.remove(ax.collections[0])        # remove the final element
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,    # redraw fill
                    facecolor='red', interpolate=True, alpha=0.5)
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,    # redraw fill
                    where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)

        if ApInc.val < 0.2:     # rescale axes for small scalings
            ax.set_ylim([min(Spec['amp']*0.02), max(Spec['amp']*0.02)])  # change the scaling on the y axis
        elif ApInc.val >= 0.2:  # rescale acxes for large scalings
            ax.set_ylim([min(Spec['amp']), max(Spec['amp'])])  # change the scaling on the y axis
        plt.draw()  # redraw the plot


def toggle_data(event): # turn on and off curve
    global ax, a, Spec, data_state
    if data_state is True:
        a.set_ydata([])     # get rid of curve data
        a.set_xdata([])     # get rid of curve data
        data_state = False
    else:
        a.set_ydata(Spec['amp'] * ApInc.val)        # reset data
        a.set_xdata(Spec['freq'])                   # reset data
        data_state = True

    plt.draw()


def toggle_fill(event):     # toggle on and off the fill of the axes
    global ax, a, Spec, fill_state
    if fill_state is True:
        for coll in ax.collections:     # remove fill
            ax.collections.remove(coll)
        fill_state = False
        ax.collections.remove(ax.collections[0])
    else:       # reintroduce fill
        ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                facecolor='red', interpolate=True, alpha=0.5)
        ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)
        fill_state = True

    plt.draw()


def toggle_all(event):      # control toggle of fill and curve
    global ax, Spec, fill_state, data_state, a

    if data_state is True:
        if fill_state is True:
            for coll in ax.collections:
                ax.collections.remove(coll)     # remove fill
            ax.collections.remove(ax.collections[0])
            fill_state = False
        a.set_ydata([])         # remove curve =
        a.set_xdata([])
        data_state = False

    else:
        if fill_state is False:
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,    # redraw fill
                    facecolor='red', interpolate=True, alpha=0.5)
            ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                    where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)
            fill_state = True
        a.set_ydata(Spec['amp'] * ApInc.val)    # reindroduce curve
        a.set_xdata(Spec['freq'])
        data_state = True

    plt.draw()


def on_click(event):     # preform some event on a user mouse click
    global ax, a, Spec, data_state, b, an, last_rem
    if data_state is True:
        if b is None:
            b, = ax.plot([event.xdata], [event.ydata], 'D')     # define the point for the first time
            an = ax.annotate('Last Click', xy=(event.xdata, event.ydata), xytext=(event.xdata+1, event.ydata+0.5))
            last_rem = True
        else:
            if last_rem is False:
                try:    # error handeling
                    an = ax.annotate('Last Click', xy=(event.xdata, event.ydata), xytext=(event.xdata+1,
                                                                                          event.ydata+0.5))
                except TypeError:       # Type errors are expected to ignore them
                    pass
            try:
                an.remove()
                an = ax.annotate('Last Click', xy=(event.xdata, event.ydata), xytext=(event.xdata+1, event.ydata+0.5))
                last_rem = True
            except (ValueError, TypeError) as e:        # these tyes of errors are expected so ignore them
                last_rem = False
            b.set_ydata([event.ydata])      # move the point
            b.set_xdata([event.xdata])
    plt.draw()


def on_press(event):    # preform some action on a key press
    key = event.key     # get the key press
    if key == 'escape':
        exit()  # close program if escape pressed
    elif key.upper() == 'T':
        toggle_all(1)

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
last_rem = False

axButton1 = plt.axes([0.915, 0.5, 0.075, 0.1])      # Some axes for a button to sit on
bToggle_curve = plt.Button(axButton1, 'Curve')  # slave a botton to those axis
bToggle_curve.on_clicked(toggle_data)   # call some function when button is pressed

# Another button
axButton2 = plt.axes([0.915, 0.75, 0.075, 0.1])
bToggle_fill = plt.Button(axButton2, 'Fill')
bToggle_fill.on_clicked(toggle_fill)

# Another button
axButton3 = plt.axes([0.915, 0.25, 0.075, 0.1])
bToggle_all = plt.Button(axButton3, 'All')
bToggle_all.on_clicked(toggle_all)


# Plot title and axes
ax.set_xlabel('Frequency (' + u'\u00B5' + 'Hz)')    # x label including unicode character
ax.set_ylabel('Amplitude')
ax.set_title('FT of some GALEX target')


# Fill between curve and certain y values
ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                facecolor='red', interpolate=True, alpha=0.5)
ax.fill_between(Spec['freq'], min(Spec['amp']*ApInc.val), Spec['amp']*ApInc.val,
                where=0 <= Spec['amp']*ApInc.val, facecolor='green', interpolate=True, alpha=0.7)

b = None
an = None

# Tell matplotlib to listen for mouse/button press click event and call the onclick function when one happens
mou = fig.canvas.mpl_connect('button_press_event', on_click)    # mouse click
key = fig.canvas.mpl_connect('key_press_event', on_press)       # keyboard key press

plt.show()  # Display graph object


"""
Plotly
    Plotly is a nice alternative to matplotlib for both saving interactive plots and sharing plots with others when
    you wish them to be interactive

    plotly is a web plotting library that generates HTML files which can be opened in a web browser
        they will store plots for you so a URL can be used to access them anywhere
        one can also output HTML locally and just open the file in a browser

    There is also a data streaming abilit which can be used
        allows for near real time data streaming to plotly which can be useful for long term monitoring of a system
        without actually being present at that system

    Plotly also offeres interactive 3D plots somehting that, I at least, have not been able to figure out how
        to do in MPL yet

    bult in curve fitting abilities (dont use them, they are significantly less powerful than scipy) however they
        do exits

    However plotly is -- from a pure plotting perspective -- not as powerful as MPL
        Widgets (buttons, sliders, etc) are not currently supported
            However these can be replicated with webprograming tho it is MUCH more work
        Subplots while arguably easier to impliment do not have as granular control
        it take longer to spin up a simple plot in plotly than it does in MPL

    If you need a lot of plot storage (>100 plots hosted by them per day) pro is required
        if you store locally this is avoided and you can do unlimited
"""