#
#=====================================================================================
#       Filename:  zigbee_channel_calculation.py
# 
#    Description:  reconstruct the overlapped ZigBee signal and calculate the ZigBee to WiFi cross-technology channel.
#        Version:  1.0
#
#         Author:  Shuai Wang
#         Email :  <shine.hitcs@gmail.com>
#   Organization:  Smart and Mobile Systems (Smile) Lab @ KAIST 
#				   https://sites.google.com/view/smilelab/
#
#   Copyright (c)  Smart and Mobile Systems (Smile) Lab @ KAIST 
# =====================================================================================
#

import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn import linear_model
import copy
import cmath
from scipy.optimize import curve_fit


# load the transmitted ZigBee signal (20MHz sampling rate)

zigbee=scipy.fromfile(open('./zigbee_signal.txt'),dtype=scipy.complex64)


# center frequency difference between WiFi and ZigBee channel is 4MHz.
offset_frequency=4000000

n_samples=np.arange(64)

offset_real=np.cos(np.pi*2*offset_frequency*n_samples/20000000)


offset_imag=np.sin(np.pi*2*offset_frequency*n_samples/20000000)

offset_signal=[]

for i in range(len(offset_imag)):
	offset_signal.append(np.complex(offset_real[i],offset_imag[i]))

offset_signal=np.array(offset_signal)

# only first 64 samples of ZigBee preamble overlaps with WiFi HT-LTF
# shift the ZigBee signal by 4MHz
shifted_zigbee=zigbee[:64]*offset_signal

fft_shift=np.fft.fft(shifted_zigbee)
fft_shift[:9] = 0j
fft_shift[17:] = 0j





# set the total number of CSIs we want to process
total_number=100



# load the CSI collected from teh first WiFi Fragment.
sourceFile = open("antenna1_wifi_csi_imag.csv", "r")


imag_part = []
for line in sourceFile.readlines():
	strline = line.split(',')
	imag_part_temp=[]
	for i in range(len(strline)):
		imag_part_temp.append(float(strline[i]))
	imag_part_temp=np.array(imag_part_temp)
	imag_part.append(imag_part_temp)
sourceFile.close()




sourceFile = open("antenna1_wifi_csi_real.csv", "r")


real_part = []
for line in sourceFile.readlines():
	real_part_temp=[]
	strline = line.split(',')
	for i in range(len(strline)):
		real_part_temp.append(float(strline[i]))
	real_part_temp=np.array(real_part_temp)
	real_part.append(real_part_temp)

sourceFile.close()

wifi_csi=[]

for j in range(total_number):
	wifi_csi_temp=[]
	for i in range(56):
		wifi_csi_temp.append(np.complex(real_part[j][i],imag_part[j][i]))

	wifi_csi_temp=np.array(wifi_csi_temp)
	wifi_csi.append(wifi_csi_temp)



# load the CSI collected from the second WiFi Fragment (overlapped with ZigBee).


sourceFile = open("antenna1_mix_csi_imag.csv", "r")


imag_part = []
for line in sourceFile.readlines():
	strline = line.split(',')
	imag_part_temp=[]
	for i in range(len(strline)):
		imag_part_temp.append(float(strline[i]))
	imag_part_temp=np.array(imag_part_temp)
	imag_part.append(imag_part_temp)
sourceFile.close()




sourceFile = open("antenna1_mix_csi_real.csv", "r")


real_part = []
for line in sourceFile.readlines():
	real_part_temp=[]
	strline = line.split(',')
	for i in range(len(strline)):
		real_part_temp.append(float(strline[i]))
	real_part_temp=np.array(real_part_temp)
	real_part.append(real_part_temp)

sourceFile.close()

mix_csi=[]

for j in range(total_number):
	mix_csi_temp=[]
	for i in range(56):
		mix_csi_temp.append(np.complex(real_part[j][i],imag_part[j][i]))

	mix_csi_temp=np.array(mix_csi_temp)
	mix_csi.append(mix_csi_temp)

import copy

# cross-technology channel is stored in zigbee_channel list
# the reconstructed overlapped ZigBee signal is stored in "reconstructed_zigbee_signal" list
zigbee_channel=[]
reconstructed_zigbee_signal=[]


for index in range(total_number):

	csi_wifi=wifi_csi[index]
	csi_mix=mix_csi[index]

	diff=csi_mix/csi_wifi

#	compensating the phase and amplitude change caused by the hardware imperfections including 
	def f(x, A, B): # this is a 'straight line' y=f(x)
	    return A*x + B

	popt, pcov = curve_fit(f, np.arange(0,28), np.unwrap(np.angle(diff))[:28]) # your data x, y to fit

	fit=np.arange(0,56)*popt[0]+popt[1]
	effective_phase=fit[37:37+8]


	popt, pcov = curve_fit(f, np.arange(0,28), np.abs(diff)[:28]) # your data x, y to fit

	fit_am=np.arange(0,56)*popt[0]+popt[1]

	effective_am=fit_am[37:37+8]


	effective_diff=[]
	for i in range(8):
		effective_diff.append(cmath.rect(effective_am[i],effective_phase[i]))
	effective_diff=np.array(effective_diff)


# the CSI induced by the overlapped ZigBee singal:
	pure_zigbee_csi=csi_mix[36:36+8]-(csi_wifi[36:36+8]*effective_diff)



	ht_ltf=[ 0,  0,  0,  0,  1,  1,  1,  1, -1, -1,
		 1,  1, -1,  1, -1,  1,  1,  1,  1,  1,
		 1, -1, -1,  1,  1, -1,  1, -1,  1,  1,
		 1,  1,  0,  1, -1, -1,  1,  1, -1,  1,
		-1,  1, -1, -1, -1, -1, -1,  1,  1, -1,
		-1,  1, -1,  1, -1,  1,  1,  1,  1,  -1,
		 -1,  0,  0,  0]

	ht_ltf=np.array(ht_ltf)






	recover_csi=[0j for i in range(64)]
	recover_csi=np.array(recover_csi)
	recover_csi[41:49]=pure_zigbee_csi




	recover_signal=recover_csi*ht_ltf

	recover_signal=np.fft.fftshift(recover_signal)


	recovered_wrong_order=np.fft.ifft(recover_signal)

	recovered_correct_order=copy.deepcopy(recovered_wrong_order)



	recovered_correct_order[:4]=recovered_wrong_order[60:]

	recovered_correct_order[4:]=recovered_wrong_order[:60]

	recover_zigbee=recovered_correct_order;

	recovered_fft=np.fft.fft(recover_zigbee)

	reconstructed_zigbee=recovered_fft[9:17]

	ideal_zigbee=fft_shift[9:17]


#	cross-technology channel is stored in "zigbee_csi"
	zigbee_csi=reconstructed_zigbee/ideal_zigbee
	




	# remove the center frequency difference in the reconstructed ZigBee signal 
	recovered_correct_order=copy.deepcopy(recovered_wrong_order)

	n_samples=np.arange(64)

	offset_frequency=-4000000


	offset_real=np.cos(np.pi*2*offset_frequency*n_samples/20000000)


	offset_imag=np.sin(np.pi*2*offset_frequency*n_samples/20000000)

	offset_signal=[]

	for i in range(len(offset_imag)):
		offset_signal.append(np.complex(offset_real[i],offset_imag[i]))

	offset_signal=np.array(offset_signal)

	shifted_zigbee=recovered_correct_order*offset_signal


	ff_shift=np.fft.fft(shifted_zigbee)



	ff_shift[4:60]=0j

	recovered_no_freq_diff=np.fft.ifft(ff_shift)

	recovered_correct_order[4:]=recovered_no_freq_diff[:60]

	recovered_correct_order[:4]=recovered_no_freq_diff[60:]



	zigbee_channel.append(zigbee_csi)
	reconstructed_zigbee_signal.append(recovered_correct_order)





# plot the reconstructed ZigBee signal and estimated cross-technology channel.
import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation



# Sent for figure
font = {'size'   : 12}
plt.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = total_number)
f0.suptitle("Cross-technology Channel Estimation", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))
ax02 = subplot2grid((2, 2), (0, 1))
ax03 = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
ax04 = ax03.twinx()
#tight_layout()

# Set titles of subplots
ax01.set_title('ZigBee CSI phase')
ax02.set_title('ZigBee CSI amplitude')
ax03.set_title('Reconstructed Overlapped ZigBee signal')

# set y-limits
ax01.set_ylim(-4,4)
ax02.set_ylim(0,20)
ax03.set_ylim(-20,20)
ax04.set_ylim(-20,20)

# sex x-limits
ax01.set_xlim(0,8)
ax02.set_xlim(0,8)
ax03.set_xlim(0,64)
ax04.set_xlim(0,64)

# Turn on grids
ax01.grid(True)
ax02.grid(True)
ax03.grid(True)

# set label names
ax01.set_xlabel("Subcarrier")
ax01.set_ylabel("Phase")
ax02.set_xlabel("Subcarrier")
ax02.set_ylabel("Amplitude")
ax03.set_xlabel("Sample Index")
ax03.set_ylabel("I/Q Amplitude")
#ax04.set_ylabel("vy")

# Data Placeholders
yp1=zeros(0)
yv1=zeros(0)
yp2=zeros(0)
yv2=zeros(0)
t=zeros(0)


# set plots
p011, = ax01.plot(np.unwrap(np.angle(zigbee_channel[0])),'b-', label="Zigbee CSI phase")
#p012, = ax01.plot(t,yp2,'g-', label="yp2")

p021, = ax02.plot(np.abs(zigbee_channel[0]),'b-', label="ZigBee CSI amplitude")
#p022, = ax02.plot(t,yv2,'g-', label="yv2")

p031, = ax03.plot(reconstructed_zigbee_signal[0].imag,'b-', label="imag")
p032, = ax04.plot(reconstructed_zigbee_signal[0].real,'r-', label="real")

# set lagends
#ax01.legend([p011,p012], [p011.get_label(),p012.get_label()])
#ax02.legend([p021,p022], [p021.get_label(),p022.get_label()])
#ax03.legend([p031,p032], [p031.get_label(),p032.get_label()])

# Data Update
xmin = 0.0
xmax = 5.0
x = 0.0
t=0
pause=False
def onClick(event):
    global pause
    pause ^= True
def updateData(self,):

	global t
	p011.set_data(np.arange(8),np.unwrap(np.angle(zigbee_channel[t])))
	p021.set_data(np.arange(8),np.abs(zigbee_channel[t]))
	p031.set_data(np.arange(64),reconstructed_zigbee_signal[t].imag)
	p032.set_data(np.arange(64),reconstructed_zigbee_signal[t].real)
	t=t+1
	if t==total_number:
		t=0


	return p011, p021, p031, p032
f0.canvas.mpl_connect('button_press_event', onClick)
# interval: draw new frame every 'interval' ms
# frames: number of frames to draw



simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=5, interval=400, repeat=False)

# save the animation
simulation.save(filename='./cross_technology_channel_estimation.gif',writer='imagemagick', fps=2)

plt.show()







