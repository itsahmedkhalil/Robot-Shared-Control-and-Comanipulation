import csv
from time import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
np.set_printoptions(threshold=sys.maxsize)


plt.ion()
fig = plt.figure() #Create a figure

ser = serial.Serial('/dev/arduinoNano', timeout=None) #Change serial port

t_0 = float(time()) #Time when code is first run
noise_accx = 0  #Dummy variable for accelerometer noise in x axes
noise_accy = 0  #Dummy variable for accelerometer noise in y axes
noise_accz = 0  #Dummy variable for accelerometer noise in z axes

rowlist = []
calibratedData = []
rawDataList = []
calibratedDataList = []
vel = [0, 0 , 0]
dist = [0, 0, 0]

# i = 0
# for i in range(100):
while True: #To terminate this code, you have to ctrl+c or close the terminal. Closing the graph is not enough. 
    ser_bytes = ser.readline() 
    if ser_bytes != "": #Make sure that the line is not empty
         
        decoded_bytes = str(ser_bytes.decode("ascii"))
        rawData = [float(x) for x in decoded_bytes.split(",")]
        t_from_start = round(float(time()) - t_0,3) #Time from when the code when initally run
        rawData.insert(0, t_from_start)   #Insert time for each respective point 
        #rowlist.append(rows)   #Append row to l
        calibratedData = rawData
        
        calibratedData[1] = rawData[1] - noise_accx
        calibratedData[2] = rawData[2] - noise_accy
        calibratedData[3] = rawData[3] - noise_accz

        #Method 2: Creating threshold to get rid of noise
        if abs(calibratedData[1])<0.03:
            calibratedData[1] = 0
        if abs(calibratedData[2])<0.03:
            calibratedData[2] = 0
        if abs(calibratedData[3])<0.03:
            calibratedData[3] = 0

        #Plotting the acceleration for each axes
        plt.scatter(t_from_start, calibratedData[1], s=10, c='r', marker="s")    #acc_x
        plt.scatter(t_from_start, calibratedData[2], s=10, c='y', marker="s")    #acc_y
        plt.scatter(t_from_start, calibratedData[3], s=10, c='k', marker="s")    #acc_z
        plt.show()  #Show the plot
        plt.pause(0.000001)

        #Converting raw data into a dataframe
        rawDataList.append(rawData)
        
        #Converting 'calibrating' data in a dataframe
        calibratedDataList.append(calibratedData)

        acc = np.array([calibratedData[1], calibratedData[2],calibratedData[3]])

        #Method 1: Subtracting off bias
        #This is to get rid of noise. To use you have to make sure that the IMU is stationary for ~10 seconds. 
        #The code will collect 100 data points, average them, and subtract that number from all 
        #incoming accelerometer data in each respective axes. 
        print(len(rawDataList))
        if len(rawDataList)== 100:
            calibratedDataDF = pd.DataFrame(calibratedDataList, columns =['time', 'accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 
            rawDataDF = pd.DataFrame(rawDataList, columns =['time', 'accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 
            noise_accx = np.sum(rawDataDF['accx'])/np.size(rawDataDF['accx'])
            noise_accy = np.sum(rawDataDF['accy'])/np.size(rawDataDF['accy'])
            noise_accz = np.sum(rawDataDF['accz'])/np.size(rawDataDF['accz'])
            vel = [0, 0 , 0]
            dist = [0, 0, 0]
            print('CALIBRATION DONE!')
        else:
            dt = 25/1000
            if acc[0] == 0:
                vel[0] = 0
            if acc[1] == 0:
                vel[1] = 0
            if acc[2] == 0:
                vel[2] = 0
            vel = vel + acc*dt
            dist = dist + vel*dt

        # print(np.sum(rawDataDF['accz']),np.size(rawDataDF['accz']), noise_accz)

        print(rawData)
        t_from_start_old = t_from_start


