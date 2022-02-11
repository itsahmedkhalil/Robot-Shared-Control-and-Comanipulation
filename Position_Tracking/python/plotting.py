from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import serial
import collections
import random
from time import time
import math
import numpy as np
from scipy.spatial.transform import Rotation as R

from tf import TransformBroadcaster
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rospy import Time
from scipy.spatial.transform import Rotation as R
import random
import sys
sys.path.append('/home/ahmedkhalil/openzen')
import openzen

openzen.set_log_level(openzen.ZenLogLevel.Warning)

error, client = openzen.make_client()
if not error == openzen.ZenError.NoError:
    print("Error while initializing OpenZen library")
    sys.exit(1)

error = client.list_sensors_async()

# check for events
sensor_desc_connect = None
while True:
    zenEvent = client.wait_for_next_event()

    if zenEvent.event_type == openzen.ZenEventType.SensorFound:
        print("Found sensor {} on IoType {}".format(zenEvent.data.sensor_found.name,
                                                    zenEvent.data.sensor_found.io_type))
        if sensor_desc_connect is None:
            sensor_desc_connect = zenEvent.data.sensor_found

    if zenEvent.event_type == openzen.ZenEventType.SensorListingProgress:
        lst_data = zenEvent.data.sensor_listing_progress
        print("Sensor listing progress: {} %".format(lst_data.progress * 100))
        if lst_data.complete > 0:
            break
print("Sensor Listing complete")

if sensor_desc_connect is None:
    print("No sensors found")
    sys.exit(1)
# connect to the first sensor found
error, sensor = client.obtain_sensor(sensor_desc_connect)

# or connect to a sensor by name
#error, sensor = client.obtain_sensor_by_name("LinuxDevice", "LPMSCU2000003")

if not error == openzen.ZenSensorInitError.NoError:
    print("Error connecting to sensor")
    sys.exit(1)

print("Connected to sensor !")

imu = sensor.get_any_component_of_type(openzen.component_type_imu)
if imu is None:
    print("No IMU found")
    sys.exit(1)

# read bool property
error, is_streaming = imu.get_bool_property(openzen.ZenImuProperty.StreamData)
if not error == openzen.ZenError.NoError:
    print("Can't load streaming settings")
    sys.exit(1)

    print("Sensor is streaming data: {}".format(is_streaming))


calibratedData = []
def getGravity():
    try:
        for i in range(400):
            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                    zenEvent.sensor == imu.sensor and \
                    zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data
                acc_init = np.array(imu_data.a)
                quat_init = imu_data.q
                r_init = R.from_quat(
                    [quat_init[1], quat_init[2], quat_init[3], quat_init[0]])
                cal_acc = r_init.apply(acc_init)
                calibratedData.append(cal_acc)  # cal_acc)
                i += 1
            pass
        np_calibratedData = np.array(calibratedData)
        x_offset = 0  # np.mean(np_calibratedData[:, 0])
        y_offset = 0  # np.mean(np_calibratedData[:, 1])
        z_offset = 0  # np.mean(np_calibratedData[:, 2])
        g = np.sum(np.linalg.norm(np_calibratedData, axis=1) /
                   np.shape(np_calibratedData)[0])
        print("Calibration Completed", g)
    except Exception as e:
        print(e)
        g = 9.81
        print("Calibration Failed", g)
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
        self.p4 = self.win.addPlot(title="Rotated Acc X")
        self.p5 = self.win.addPlot(title="Rotated Acc Y")
        self.p6 = self.win.addPlot(title="Rotated Acc Z")
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
        try:
            zenEvent = client.wait_for_next_event()

            # check if its an IMU sample event and if it
            # comes from our IMU and sensor component
            if zenEvent.event_type == openzen.ZenEventType.ImuData and \
                    zenEvent.sensor == imu.sensor and \
                    zenEvent.component.handle == imu.component.handle:

                imu_data = zenEvent.data.imu_data
            t = float(time())

            acc = np.array(imu_data.a)
            quat = imu_data.q
            print(quat)
            r = R.from_quat([quat[1], quat[2], quat[3], quat[0]])
            r_acc = r.apply(acc)
            r_acc = r_acc 
            
            self.dt = t - self.t_old
            for i in range(len(r_acc)):
                    x_n = (2*self.x_n_1 - self.x_n_2 + self.damp*self.x_n_1*self.dt+r_acc*self.dt*self.dt)/(self.damp*self.dt+1)

            self.t_old = t
            self.x_n_2 = self.x_n_1
            self.x_n_1 = x_n
            return acc,r_acc,x_n
        except Exception as e:
            #t = float(time())
            print(e)

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
    g = getGravity()
    print("gravity:",g)
    m = DynamicPlotter(sampleinterval=0.01, timewindow=10.)
    m.run()



