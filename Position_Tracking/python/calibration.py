import csv
from time import time
import serial
import numpy as np
from numpy import linalg as LA
import os
from pathlib import Path

x_pos = [1., 0., 0.]
x_neg = [-1., 0., 0.]
y_pos = [0., 1., 0.]
y_neg = [0., -1., 0.]
z_pos = [0., 0., 1.]
z_neg = [0., 0., -1.]

A = []
for i in range(1000):
    A.append(x_pos)
for i in range(1000):
    A.append(x_neg)
for i in range(1000):
    A.append(y_pos)
for i in range(1000):
    A.append(y_neg)
for i in range(1000):
    A.append(z_pos)
for i in range(1000):
    A.append(z_neg)

dir = str(os.path.abspath(os.curdir))#[:-8]
print(dir)

files = ["/lpmsData/posX.csv", "lpmsData/negX.csv", "lpmsData/posY.csv", "lpmsData/negY.csv", "lpmsData/posZ.csv", "lpmsData/negZ.csv"]

fil_path = [dir + "/" + s for s in files]
B = []

for f in fil_path:    
    #with open(file, 'r') as csvfile:
    file = open(f,"r")
    reader = csv.reader(file)
    for row in reader:        
        B.append(row)
print(len(B))

def least_squares_fit(A, B):
    """Does least squares fit to find x of Ax = B.  Returns best guess of original distortion
     matrix x and its inverse.  A is ideal values.  B is distorted values.  Use inverse to
     correct real data back to ideal data."""

    # Need to extend A and B
    A = np.hstack((A, np.ones(len(A)).reshape(-1, 1)))
    B = np.hstack((B, np.ones(len(B)).reshape(-1, 1)))
    
    A = A.astype('float32')
    B = B.astype('float32')
    #print(A)
    #print(B)
    X, res, rank, s = np.linalg.lstsq(A, B, rcond=1)
    #print(X) 
    X = X.T # Transpose
    
    Xi = np.linalg.inv(X) #inverse of Matrix X
    return (np.asmatrix(X), np.asmatrix(Xi), np.sum(res))

f = np.array([[0.99,-0.02,-0.08]])
f = f.reshape(3,1)
b_a = least_squares_fit(A, B)[0][:3,3] #offset
M = least_squares_fit(A, B)[0][:3, :3] #sensitivity matrix
#Mi = np.linalg.inv(M)


print(b_a)
print(M)
# # Your serial port might be diffrent!
# ser = serial.Serial('/dev/ttyACM0', timeout=1) #Change serial port
f_hat = np.linalg.inv(M) * (np.array(f) - b_a)
#print(f_hat)
f_hat = f_hat.reshape(3)
f_hat = np.asarray(f_hat)

# f = open("noise_test_NANO.csv", "a+")
# writer = csv.writer(f, delimiter=',')

# while True:
#     s = ser.readline().decode()
#     if s[0] != 'C' and s != "":
#     #if s != "":
#         #print(s)
        # rows = [float(x.replace("\r\n","")) for x in s.split(",")]
        # if len(rows) == 3:
           # rows = np.array(rows).reshape(3,1)
            #print(np.array(rows).reshape(3,1))
            # f_hat = np.linalg.inv(M) * (np.array(rows) - b_a)
            # f_hat = f_hat.reshape(3)
            # f_hat = np.asarray(f_hat)
            # fin_rows = f_hat[0].tolist()
            # # Insert local time to list's first position
            # fin_rows.insert(0, time())
            # print(fin_rows)
            # writer.writerow(fin_rows)
            # f.flush()