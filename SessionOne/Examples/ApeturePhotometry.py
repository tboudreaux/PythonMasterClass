import matplotlib
matplotlib.use('Qt4Agg')
from pylab import *
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import numpy as np
import cv2
from cv2 import *
import datetime
import time
import numpy as np

c1 = '#66ff66'
c2 = '#ff0000'
c3 = '#33ccff'
opts = dict(fc='none', ec=c1, lw=2)
opts2 = dict(fc='none', ec=c2, lw=2)
opts3 = dict(fc='none', ec=c2, lw=4)
opts4 = dict(fc='none', ec=c3, lw=2)
axcolor = 'lightgoldenrodyellow'

length = 0

def update_ap(event):
	"""
	redraw annulus
	:param event: Slider change event
	:return: N/A
	"""
	global Aperture
	global ax
	Aperture.remove()
	Aperture = Circle((prev_x, prev_y), ApInc.val, **opts)
	ax.add_patch(Aperture)
def update_anin(event):
	global InnerAnnulus
	global ax
	InnerAnnulus.remove()
	InnerAnnulus = Circle((prev_x, prev_y), AnInInc.val, **opts2)
	ax.add_patch(InnerAnnulus)
def update_anout(event):
	global OuterAnnulus
	global ax
	OuterAnnulus.remove()
	OuterAnnulus = Circle((prev_x, prev_y), AnOutInc.val, **opts3)
	ax.add_patch(OuterAnnulus)

def setApp(event):
	global length
	length = ApInc.val
	plt.close()


def stream(width, InWidth, OutWidth):
	py.sign_in('tboudreaux', '3sfbtww4bj')
	cam = VideoCapture(-1)
	cam.set(3, 1280)
	cam.set(4, 720)
	cam.set(15, 0.1)
	stream_ids = tls.get_credentials_file()['stream_ids']
	stream_id = stream_ids[0]

	stream_1 = go.Stream(
	    token=stream_id,  # link stream id to 'token' key
	    maxpoints=100      # keep a max of 80 pts on screen
	)

	trace1 = go.Scatter(
	    x=[],
	    y=[],
	    mode='lines+markers',
	    stream=stream_1         # (!) embed stream id, 1 per trace
	)

	data = go.Data([trace1])	
	layout = go.Layout(title='RealTimeLightCurve')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='RealTimeLightCurve', auto_open=False)	
	# Initialize trace of streaming plot by embedding the unique stream_id
	global prev_x, prev_y

	while True:
		s, img = cam.read()
		if s:
			img = np.fliplr(img.reshape(-1, 3)).reshape(img.shape)
			brightness = 0
			center = (prev_y, prev_x)
			array = []
			barray = []
			backBrightness = 0
			for i in xrange(int(center[0] - OutWidth/2), int((center[1] + OutWidth/2)-1)):
				for j in xrange(int(center[1] - width/2), int((center[1] + width/2)-1)):
					a = i - center[0]
					b = j - center[1]
					if a*a + b*b <= (OutWidth/2)*(OutWidth/2) and a*a+b*b >= (InWidth/2)*(InWidth/2):
						backBrightness += 0.2126*img[i][j][0] + 0.7152 * img[i][j][1] + 0.0722*img[i][j][2]
			for i in xrange(int(center[0] - width/2), int((center[0] + width/2)-1)):
				temp = []
				bt = []
				for j in xrange(int(center[1] - width/2), int((center[1] + width/2)-1)):
					a = i - center[0]
					b = j - center[1]
					if a*a + b*b <= (width/2)*(width/2):
						temp.append([img[i][j][0], img[i][j][1], img[i][j][2]])
						brightness += 0.2126*img[i][j][0] + 0.7152 * img[i][j][1] + 0.0722*img[i][j][2]
						# brightness -= backBrightness
						brightnessmapsum = 0.2126*img[i][j][0] + 0.7152*img[i][j][1] + 0.0722*img[i][j][2]
						bt.append(brightnessmapsum)
					else:
						temp.append([0,0,0])
						brightnessmapsum = 0
						bt.append(brightnessmapsum)
				barray.append(bt)
				array.append(temp)
			# f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
			# ax1.imshow(array)
			# ax2.set_title('Image')
			# ax2.imshow(barray)
			# ax2.set_title('B Map')
			#f.subplots_adjust(hspace=0)
			# plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
			# plt.show()
			st = py.Stream(stream_id)
			st.open()
			x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			y = brightness
			st.write(dict(x=x, y=y))
			time.sleep(0.05)
	st.close()

def key_control(event):
	keydown = event.key
	global Aperture, InnerAnnulus, OuterAnnulus, prev_x, prev_y
	if keydown == 'r':
		x_loc = event.xdata
		y_loc = event.ydata
		prev_x = x_loc
		prev_y = y_loc
		Aperture.remove()
		Aperture = Circle((prev_x, prev_y), ApInc.val, **opts)
		ax.add_patch(Aperture)
		InnerAnnulus.remove()
		InnerAnnulus = Circle((prev_x, prev_y), AnInInc.val, **opts2)
		ax.add_patch(InnerAnnulus)
		OuterAnnulus.remove()
		OuterAnnulus = Circle((prev_x, prev_y), AnOutInc.val, **opts3)
		ax.add_patch(OuterAnnulus)
		plt.draw()
if __name__ == '__main__':
	cam = VideoCapture(-1)
	cam.set(3, 1280)
	cam.set(4, 720)
	cam.set(15, 0.25)
	s, img = cam.read()
	#img = cvtColor(img, COLOR_BGR2GRAY)
	#print img.shape
	#flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
	#print flags
	img = np.fliplr(img.reshape(-1,3)).reshape(img.shape)
	if s:
		prev_x = len(img[0])/2
		prev_y = len(img)/2
		fig = plt.figure(figsize=(10, 10))
		ax = fig.add_subplot(111)
		implot = ax.imshow(img)
		axApp = axes([0.25, 0.01, 0.65, 0.01])
		ApInc = Slider(axApp, 'Aperture radius', 0, 1000, valinit=500)
		AppR = ApInc.val
		axAnIn = axes([0.25, 0.03, 0.65, 0.01])
		AnInInc = Slider(axAnIn, 'Inner Annulus radius', 0, 1000, valinit=500)
		AnInR = AnInInc.val
		axAnOut = axes([0.25, 0.05, 0.65, 0.01])
		AnOutInc = Slider(axAnOut, 'Outer Annulus radius', 0, 1000, valinit=500)
		AnOutR = AnOutInc.val
		axSet = axes([0.91, 0.40, 0.075, 0.075], axisbg=axcolor)
		bSet = Button(axSet, 'Set')
		Aperture = Circle((prev_x, prev_y), AppR, **opts)
		ax.add_patch(Aperture)
		InnerAnnulus = Circle((prev_x, prev_y), AnInR, **opts2)
		ax.add_patch(InnerAnnulus)
		OuterAnnulus = Circle((prev_x, prev_y), AnOutR, **opts3)
		ax.add_patch(OuterAnnulus)
		ApInc.on_changed(update_ap)
		AnInInc.on_changed(update_anin)
		AnOutInc.on_changed(update_anout)
		bSet.on_clicked(setApp)
		fig.canvas.mpl_connect('key_press_event', key_control)
		plt.show()
	print 'LENGTH IS:', length
	cam.release()
	stream(length, AnInInc.val, AnOutInc.val)
