import csv
from time import time
import serial
import numpy as np
from scipy.spatial.transform import Rotation as R
import pandas as pd
import matplotlib.pyplot as plt
import scipy.fftpack

# Your serial port might be different!
ser = serial.Serial('/dev/ttyACM0', timeout=1) #Change serial port
calibratedData = []
def getGravity():
    try:
        for i in range(100):
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
    except:
        g=9.81
    return g

g = getGravity()
i = 0
accX = []
accY = []
accZ = []

time_bf = float(time())
for i in range(100):
    ser_bytes = ser.readline()  
    decoded_bytes = str(ser_bytes.decode("ascii"))
    if decoded_bytes[0] != 'C':
        rawData = [float(x) for x in decoded_bytes.split(",")]
        acc = np.array(rawData[0:3])
        quat = rawData[3:]
    r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
    r_acc = r.apply(acc)

    r_acc = r_acc - np.array([0, 0, g])
    r_acc.tolist()
    accX.append(r_acc[0])
    accY.append(r_acc[1])
    accZ.append(r_acc[2])
    i +=1
time_af = float(time())
N = len(accX)
T = (time_af- time_bf)/N


x = np.linspace(0.0, N*T, N)
#acc_df = pd.DataFrame({"accX": accX, "accY": accY, "accZ": accZ})
accXf = scipy.fftpack.fft(accX)
accYf = scipy.fftpack.fft(accY)
accZf = scipy.fftpack.fft(accZ)
interval = 1.0/(2.0*T)
xf = np.linspace(0.0, interval, N//2)
print(interval)
fig, ax = plt.subplots()
plt.subplot(3,1,1)
plt.plot(xf, 2.0/N * np.abs(accXf[:N//2]))
plt.xlabel('Frequency [Hz]')
plt.ylabel('Acceleration in X [dB]')
plt.subplot(3,1,2)
plt.plot(xf, 2.0/N * np.abs(accYf[:N//2]))
plt.subplot(3,1,3)
plt.plot(xf, 2.0/N * np.abs(accZf[:N//2]))
plt.show()