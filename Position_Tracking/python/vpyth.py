from vpython import *
from ahrs.filters import Madgwick
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import integrate as intg
from scipy.integrate import cumtrapz
import time
import math
def quaternionProduct(a, b):
    ab = np.zeros([len(a),len(a[0])])
    a = np.array(a)
    b = np.array(b)
    #print(b)
    ab[0] = a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3]
    ab[1] = a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2]
    ab[2] = a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1]
    ab[3] = a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]
    #print(len(ab[0,:]))
    #print('quaternProd ran', ab, type(ab), len(ab), len(ab[0]))
    #print(ab)
    return ab
def quaternionRotate(v, q):
    size = np.shape(v)

    col = size[0]
    row = size[1]

    v = [list((np.zeros(row))),v[0],v[1],v[2]]
    #print(v)
    v = np.array(v)
    v0XYZ = quaternionProduct(quaternionProduct(q, v), quaternionConjugate(q))
    #print('v0XYZ ran', v0XYZ, type(v0XYZ), len(v0XYZ), len(v0XYZ[0]))
    v = [v0XYZ[1], v0XYZ[2], v0XYZ[3]]
    
    return v

def quaternionConjugate(q):
    if len(q)==4:
        q = np.transpose(q)
    #print(q)
    # print(q, len(q), len(q[0]))
    qConj = np.array([q[:,0], -q[:,1], -q[:,2], -q[:,3]])
    #print('quaternConj ran', qConj, type(qConj), len(qConj), len(qConj[0]))
    return qConj

with open("StationaryIMUWithQuat2.csv", "r") as i:
    rawdata = list(csv.reader(i,delimiter=","))
exampledata = np.array(rawdata[0:],dtype=float)

acc_data = exampledata[:,1:4]
gyro_data = exampledata[:,4:7]
mag_data = exampledata[:,7:10]
q_data = exampledata[:,10:14]
sampling_t = exampledata[:,0]
num_samples = len(acc_data)
accX = acc_data[:,0]
accY = acc_data[:,1]
accZ = acc_data[:,2]
quat = q_data
acc = quaternionRotate([accX, accY, accZ], quaternionConjugate(quat))
acc = np.array(acc) - np.array([np.zeros(num_samples), np.zeros(num_samples), np.ones(num_samples)])
acc = acc*9.81
t_sample = int(sampling_t[-1]-sampling_t[0])/len(sampling_t)
#time_xaxis = np.linspace(0, 0.1, len)
#Placing the plots in the plane
xdata = acc[0]
ydata = acc[1]
zdata = acc[2]

dt = t_sample#time between samples THIS SHOULD BE 1/sampling frequency from the ARDUINO (1/40Hz)
#double integrating using the composite trapezoidal rule each acceleration vector to get position
posx =cumtrapz(cumtrapz(xdata,dx=dt),dx=dt)
posy =cumtrapz(cumtrapz(ydata,dx=dt),dx=dt)
posz =cumtrapz(cumtrapz(zdata,dx=dt),dx=dt)

#creat a transparent box that is 10x10x10 centered at the origin 
left = box(pos=vector(-5,0,0), length=.1, width=10,height = 10, color=color.white, opacity=.2)
right = box(pos=vector(5,0,0), length=.1, width=10,height = 10, color=color.white, opacity=.2)
top = box(pos=vector(0,5,0), length=10, width=10,height = .1, color=color.white, opacity=.2)
bottom = box(pos=vector(0,-5,0), length=10, width=10,height = .1, color=color.white, opacity=.2)
back = box(pos=vector(0,0,-5), length=10, width=.1,height = 10, color=color.white, opacity=.2)
front = box(pos=vector(0,0,5), length=10, width=.1,height = 10, color=color.white, opacity=.2)

#imu dimensions 1.8x0.9x0.6in
imu = box(length=1.8, width=0.9,height = .6,color=color.blue)

#initial position set
xpos = posx[0]
ypos = posy[0]
zpos = posz[0]

print("hello")
#runs without any conditions until the break statement executes inside the loop
while True:
    #counter initialized
    i = 0
    #loop over the whole range of data 
    for v in range(len(posx)):
        #the position vector of the imu
        imu.pos=vector(xpos,ypos,zpos)
        #x,y,z positions update to new position
        #xpos += posx[i] are the positions adding up?
        #ypos += posx[i]
        #zpos += posx[i]
        xpos = posx[i]
        ypos = posx[i]
        zpos = posx[i]
        """
        todo:
            -   add orientation to the imu block from gyro data
            -   connect this piece of code to the imu automatically using the recieve_imu.py 
                to get live feedback of the imu
        
        """
        i +=1
        #sleep time so the for loop doesn't loop over the data quickly 
        time.sleep(dt)


