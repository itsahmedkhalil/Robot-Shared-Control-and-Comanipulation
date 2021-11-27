from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import collections
import random
from time import time
import math
import numpy as np
from scipy.spatial.transform import Rotation as R
#from calibration import *

calibratedData = []
def getGravity():
    try:
        for i in range(400):
            ser_bytes = ser.readline() 
            decoded_bytes = str(ser_bytes.decode("ascii"))
            if decoded_bytes[0] != 'C':
                rawData = [float(x) for x in decoded_bytes.split(",")]
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

class DynamicPlotter():
    def __init__(self):
        self.vel = np.zeros(3)  
        self.counter = 0
        self.x_n = np.zeros(3)
        self.x_n_1 = np.zeros(3)
        self.x_n_2 = np.zeros(3)
        self.t_old = float(time())
        self.damp = np.zeros(3)#0.2
        self.damp_high = 1000
        self.damp_low = 1
        self.total_freq = 0

    def getdata(self):
        t = float(time())
        ser_bytes = ser.readline()  
        decoded_bytes = str(ser_bytes.decode("ascii"))
        if decoded_bytes[0] != 'C':
            rawData = [float(x) for x in decoded_bytes.split(",")]
            acc = np.array(rawData[0:3])
            quat = rawData[3:]

        is_all_zero = not np.any(acc)
        if is_all_zero:
            r_acc = np.array([0,0,0])
        else:
            r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
            r_acc = r.apply(acc)
            r_acc = r_acc - np.array([0, 0, g])
        self.dt = t - self.t_old
        for i in range(len(r_acc)):
            if abs(r_acc[i]) < 0.2:
                r_acc[i] = 0
                self.damp[i] = self.damp_high
            else:
                self.damp[i] = self.damp_low
                
        vel = (self.vel + r_acc*self.dt)/(1+self.damp*self.dt)
        for v in range(len(vel)):
            if abs(vel[v]) < 0.05:
                vel[v] = 0

        x_n = self.x_n_1 + self.dt*vel
                
        self.t_old = t
        self.vel = vel
        self.x_n_2 = self.x_n_1
        self.x_n_1 = x_n


if __name__ == '__main__':
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = '/dev/ttyUSB0'
    ser.open()
    g = getGravity()
    print("gravity:",g)
    m = DynamicPlotter()



