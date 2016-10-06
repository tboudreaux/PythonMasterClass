import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from matplotlib.colors import LogNorm
import pandas as pd


def update_plot(event):
    global ax
    global Spec
    del[ax.lines[0]]
    ax.plot(Spec['freq'], Spec['amp'] * ApInc.val)
    plt.draw()


c1 = '#66ff66'
c2 = '#ff0000'
c3 = '#33ccff'
opts = dict(fc='none', ec=c1, lw=2)
opts2 = dict(fc='none', ec=c2, lw=2)
opts3 = dict(fc='none', ec=c2, lw=4)
opts4 = dict(fc='none', ec=c3, lw=2)
axcolor = 'lightgoldenrodyellow'

spectrum1_name = '../Data/testspectrum.tsv'

Spec = pd.read_csv(spectrum1_name, delimiter='\t', names=['freq', 'amp'])

fig = plt.figure(figsize=(10, 7))

ax = fig.add_subplot(111)
ax.plot(Spec['freq'], Spec['amp'], label='Data')
ax.legend()
ax.grid()
ax.axvline(x=0.0082, linestyle='-.', color='r')
ax.axhline(y=1.5*10**-15, linestyle='--', color='g')

axApp = plt.axes([0.25, 0.01, 0.65, 0.01])
ApInc = plt.Slider(axApp, 'Aperture radius', 0, 1000, valinit=500)
ApInc.on_changed(update_plot)


plt.show()
