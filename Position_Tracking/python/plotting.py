from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import collections
import random
from time import time
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
        self.databuffer_accX = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_accY = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_accZ = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_velX = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_velY = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_velZ = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_posX = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_posY = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffer_posZ = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.accX = np.zeros(self._bufsize, dtype=float)
        self.accY = np.zeros(self._bufsize, dtype=float)
        self.accZ = np.zeros(self._bufsize, dtype=float)
        self.velX = np.zeros(self._bufsize, dtype=float)
        self.velY = np.zeros(self._bufsize, dtype=float)
        self.velZ = np.zeros(self._bufsize, dtype=float)
        self.posX = np.zeros(self._bufsize, dtype=float)
        self.posY = np.zeros(self._bufsize, dtype=float)
        self.posZ = np.zeros(self._bufsize, dtype=float)

        self.app = pg.mkQApp("IMU Plotting")
        #mw = QtWidgets.QMainWindow()
        #mw.resize(800,800)

        self.win = pg.GraphicsLayoutWidget(show=True, title="IMU Plotting")
        self.win.resize(1000,600)
        self.win.setWindowTitle('IMU Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        # PyQtGraph stuff

        self.p1 = self.win.addPlot(title="Acceleration X")
        self.p2 = self.win.addPlot(title="Acceleration Y")
        self.p3 = self.win.addPlot(title="Acceleration Z")
        self.win.nextRow()
        self.p4 = self.win.addPlot(title="Velocity X")
        self.p5 = self.win.addPlot(title="Velocity Y")
        self.p6 = self.win.addPlot(title="Velocity Z")
        self.win.nextRow()
        self.p7 = self.win.addPlot(title="Displacement X")
        self.p8 = self.win.addPlot(title="Displacement Y")
        self.p9 = self.win.addPlot(title="Displacement Z")

        self.accXplot = self.p1.plot(self.x, self.accX, pen=(255,0,0))
        self.accYplot = self.p2.plot(self.x, self.accY, pen=(255,0,0))
        self.accZplot = self.p3.plot(self.x, self.accZ, pen=(255,0,0))
        self.velXplot = self.p4.plot(self.x, self.velX, pen=(0,255,0))
        self.velYplot = self.p5.plot(self.x, self.velY, pen=(0,255,0))
        self.velZplot = self.p6.plot(self.x, self.velZ, pen=(0,255,0))
        self.posXplot = self.p7.plot(self.x, self.posX, pen=(255,255,0))
        self.posYplot = self.p8.plot(self.x, self.posY, pen=(255,255,0))
        self.posZplot = self.p9.plot(self.x, self.posZ, pen=(255,255,0))
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

        self.dist = np.zeros(3)  
        self.counter = 0
        self.x_n = 0
        self.x_n_1 = 0
        self.x_n_2 = 0
        self.t_old = float(time())
        self.damp = 1


    def getdata(self):
        t = float(time())
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
        self.dt = t - self.t_old
        for i in range(len(r_acc)):
                x_n = (2*self.x_n_1 - self.x_n_2 + self.damp*self.x_n_1*self.dt+r_acc*self.dt*self.dt)/(self.damp*self.dt+1)

        self.t_old = t
        self.x_n_2 = self.x_n_1
        self.x_n_1 = x_n
        return acc,r_acc,x_n

    def updateplot(self):
        acc = self.getdata()[0]
        r_acc = self.getdata()[1]
        pos = self.getdata()[2]
        self.databuffer_accX.append(acc[0])
        self.databuffer_accY.append(acc[1])
        self.databuffer_accZ.append(acc[2])
        self.databuffer_velX.append(r_acc[0])
        self.databuffer_velY.append(r_acc[1])
        self.databuffer_velZ.append(r_acc[2])
        self.databuffer_posX.append(pos[0])
        self.databuffer_posY.append(pos[1])
        self.databuffer_posZ.append(pos[2])
        self.accX[:] = self.databuffer_accX
        self.accY[:] = self.databuffer_accY
        self.accZ[:] = self.databuffer_accZ
        self.velX[:] = self.databuffer_velX
        self.velY[:] = self.databuffer_velY
        self.velZ[:] = self.databuffer_velZ
        self.posX[:] = self.databuffer_posX
        self.posY[:] = self.databuffer_posY
        self.posZ[:] = self.databuffer_posZ
        self.accXplot.setData(self.x, self.accX)
        self.accYplot.setData(self.x, self.accY)
        self.accZplot.setData(self.x, self.accZ)
        self.velXplot.setData(self.x, self.velX)
        self.velYplot.setData(self.x, self.velY)
        self.velZplot.setData(self.x, self.velZ)
        self.posXplot.setData(self.x, self.posX)
        self.posYplot.setData(self.x, self.posY)
        self.posZplot.setData(self.x, self.posZ)
        self.app.processEvents()

    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    g = getGravity()
    m = DynamicPlotter(sampleinterval=0.01, timewindow=10.)
    m.run()



