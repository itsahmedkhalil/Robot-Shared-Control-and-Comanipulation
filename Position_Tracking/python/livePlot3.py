"""Credits to https://github.com/ap--/python-live-plotting"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import collections
import random
import time
import math
import numpy as np
from scipy.spatial.transform import Rotation as R

calibratedData = []
def getGravity():
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
    except:
        g=9.81
    return g


class DynamicPlotter():

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        # Data stuff
        self._interval = int(sampleinterval*10)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_2 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=float)
        self.y_2 = np.zeros(self._bufsize, dtype=float)
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])
        self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'accileration', 'm/s^2')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen=(255,0,0))
        self.curve_2 = self.plt.plot(self.x, self.y_2, pen=(0,255,0))
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def getdata(self):
        frequency = 0.5
        ser_bytes = ser.readline()  
        decoded_bytes = str(ser_bytes.decode("ascii"))
        if decoded_bytes[0] != 'C':
            rawData = [float(x) for x in decoded_bytes.split(",")]
            acc = np.array(rawData[0:3])
            quat = rawData[3:]
            print("real:",acc)

        r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
        r_acc = r.apply(acc)

        r_acc = r_acc - np.array([0, 0, g])
        return acc[0],r_acc[0]

    def updateplot(self):
        self.databuffer.append( self.getdata()[0] )
        self.databuffer_2.append( self.getdata()[1] )
        self.y[:] = self.databuffer
        self.y_2[:] = self.databuffer_2
        self.curve.setData(self.x, self.y)
        self.curve_2.setData(self.x, self.y_2)
        self.app.processEvents()

    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    g = getGravity()
    m = DynamicPlotter(sampleinterval=0.01, timewindow=10.)
    m.run()