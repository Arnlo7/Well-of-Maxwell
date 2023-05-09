import libm2k
import matplotlib.pyplot as plt
import time
import numpy as np
import csv
from scipy.signal import butter,filtfilt
#Code seen here adapted from https://github.com/analogdevicesinc/libm2k/releases/tag/v0.7.0

# filter

fs = 1000.0       # sample rate, Hz
cutoff = 2      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
nyq = 0.5 * fs  # Nyquist Frequency
order = 2 

#Butterworth filter that smoothes out data and reduces noise in the input
def butter_lowpass_filter(data, cutoff, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

ctx=libm2k.m2kOpen()
if ctx is None:
	print("Connection Error: No ADALM2000 device available/connected to your PC.")
	exit(1)


ain=ctx.getAnalogIn()
aout=ctx.getAnalogOut()
trig=ain.getTrigger()

# Prevent bad initial config for ADC and DAC
ain.reset()
aout.reset()

ctx.calibrateADC()
ctx.calibrateDAC()

ain.enableChannel(0,True)
ain.enableChannel(1,True)
ain.setSampleRate(100000)
ain.setRange(0,-10,10)

### uncomment the following block to enable triggering
#trig.setAnalogSource(0) # Channel 0 as source
#trig.setAnalogCondition(0,libm2k.RISING_EDGE_ANALOG)
#trig.setAnalogLevel(0,0.5)  # Set trigger level at 0.5
#trig.setAnalogDelay(0) # Trigger is centered
#trig.setAnalogMode(1, libm2k.ANALOG)

aout.setSampleRate(0, fs)
aout.setSampleRate(1, fs)
aout.enableChannel(0, True)
aout.enableChannel(1, True)

x=np.linspace(-np.pi,np.pi,1024)
buffer1=np.linspace(-2.0,2.00,1024)
buffer2=np.sin(x)

buffer = [buffer1, buffer2]

aout.setCyclic(True)
aout.push(buffer)

while True: # Constantly takes samples to update the plots while this script runs
    #Channel 1:
    plt.clf()
    plt.ylim(-5,5)
    data = ain.getSamples(40000)
    sig_filtered = butter_lowpass_filter(data[0],cutoff,order)
    plt.plot(sig_filtered)
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.savefig('static/well_of_maxwell/images/plot1.png')
    plt.close()
    #Channel 2:
    plt.clf()
    plt.ylim(-5,5)
    data = ain.getSamples(40000)
    sig_filtered = butter_lowpass_filter(data[1],cutoff,order)
    plt.plot(sig_filtered)
    plt.savefig('static/well_of_maxwell/images/plot2.png')
    plt.close()
    time.sleep(.001)
    with open('example.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(sig_filtered)):
            v = round(sig_filtered[i], 3)

            row = [i, v]
            writer.writerow(row)

libm2k.contextClose(ctx)