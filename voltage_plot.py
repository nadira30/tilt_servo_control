import matplotlib.pyplot as plt
import numpy as np
 
# define data arrays
time_data = []
vol0 = []
 
# read in the data
 
lines= np.loadtxt('sensor_voltage.txt', delimiter=',')
for line in lines:
    time_data.append(line[0]) # the first item in row is the time
    vol0.append(line[1])
 
 
# exponential decay function
# def my_func(x,a,b):
#     return a*np.exp(-b*x)
 
# have to do the following to use the time data in the exponential function
fit_time_data=np.array(time_data)
 
# make a plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
# ax.set_ylim(ymin=0)
 
# make an xy scatter plot
plt.scatter(time_datavol0,color='red', marker='.', label='channel 1')
 
 
# label the axes etc
ax.set_xlabel('Time (s)')
ax.set_ylabel('tVoltage(V))')
ax.set_title('Voltage vs time')
plt.legend(loc = 'upper right') # legend location can be changed
 
#ax.text(0.4,1.5, 'annotate the plot if needed')
plt.savefig('predict_voltage.png')