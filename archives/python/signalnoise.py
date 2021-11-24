import csv
from time import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
np.set_printoptions(threshold=sys.maxsize)

ser = serial.Serial('/dev/arduinoNano', timeout=None) #Change serial port

t_0 = float(time()) #Time when code is first run

acc = []
rawDataList = []
for i in range(50): #To terminate this code, you have to ctrl+c or close the terminal. Closing the graph is not enough. 
    ser_bytes = ser.readline() 
    if ser_bytes != "": #Make sure that the line is not empty
        decoded_bytes = str(ser_bytes.decode("ascii"))
        rawData = [float(x) for x in decoded_bytes.split(",")]

        t_from_start = round(float(time()) - t_0,3) #Time from when the code when initally run
        rawData.insert(0, t_from_start)   #Insert time for each respective point 

        # for j in range(3):
        #     j +=1
        #     rawData[j] = rawData[j] *9.81
        
        rawDataList.append(rawData)
        print(rawData)
        i+=1


rawDataDF = pd.DataFrame(rawDataList, columns =['time', 'accx','accy', 'accz','gyrx', 'gyry','gyrz', 'magx','magy', 'magz']) 
print(rawDataDF)
plt.subplot(2, 2, 1)
plt.scatter(rawDataDF['time'], rawDataDF['accx'], s=10, c='r', marker="s")  
plt.plot(rawDataDF['time'], [0]*len(rawDataDF), c = 'k')
plt.title("Acc_x noise, Stationary")

plt.subplot(2, 2, 2)
plt.scatter(rawDataDF['time'], rawDataDF['accy'], s=10, c='r', marker="s")   
plt.plot(rawDataDF['time'], [0]*len(rawDataDF), c = 'k')
plt.title("Acc_y noise, Stationary")

plt.subplot(2, 2, 3)
plt.scatter(rawDataDF['time'], rawDataDF['accz'], s=10, c='r', marker="s") 
plt.plot(rawDataDF['time'], [1]*len(rawDataDF), c = 'k')
plt.title("Acc_z noise, Stationary")
plt.show()  #Show the plot
