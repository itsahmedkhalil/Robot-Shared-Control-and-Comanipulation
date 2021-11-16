"""Slow Plotter"""
from time import time
from time import sleep
import serial
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from matplotlib import style
import numpy as np

ser = serial.Serial('/dev/ttyACM0', timeout=1)
calibratedData = []
style.use('fivethirtyeight')
t_old = float(time())
damp = 1

def getGarvity():
    try:
        for i in range(200):
            ser_bytes = ser.readline() 
            decoded_bytes = str(ser_bytes.decode("ascii"))
            if decoded_bytes[0] != 'C':
                rawData = [float(x) for x in decoded_bytes.split(",")]
                #rawDataList.append(rawData)
                acc_init = np.array(rawData[0:3])
                quat_init = rawData[3:]
                r_init = R.from_quat([quat_init[1], quat_init[2], quat_init[3], quat_init[0]])
                cal_acc = r_init.apply(acc_init)
                calibratedData.append(cal_acc)
                i+=1
            pass
        np_calibratedData = np.array(calibratedData)
        g = np.sum(np.linalg.norm(np_calibratedData, axis=1)/np.shape(np_calibratedData)[0])
        #print(g)
    except:
        g=9.81
    return g

g = getGarvity()


x_accel = []
t_list = []
raw = []
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
index = count()
t_initial = float(time())
def animate(i):
    t = float(time())-t_initial
    #print(t)
    ser_bytes = ser.readline()  
    decoded_bytes = str(ser_bytes.decode("ascii"))
    print(decoded_bytes[0])
    if decoded_bytes[0] != 'C':
        rawData = [float(x) for x in decoded_bytes.split(",")]
        acc = np.array(rawData[0:3])
        quat = rawData[3:]
        #print(acc)

    r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
    r_acc = r.apply(acc)

    r_acc = r_acc - np.array([0, 0, g])
    dt = 0.01#t - t_old
    print(t)
    t_list.append(t)
    x_accel.append(r_acc[0])
    raw.append(acc[0])
    ax1.clear()
    ax1.plot(t_list, x_accel, label='x_accel', color='r')
    ax1.plot(t_list, raw, label='raw', color='b')
    ax1.legend(loc='upper left')
  
ani = FuncAnimation(fig, animate, interval=1, frames=200)
plt.pause(0.00000000001)
plt.show()
