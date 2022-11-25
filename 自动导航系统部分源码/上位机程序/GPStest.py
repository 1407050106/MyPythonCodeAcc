# coding:UTF-8
import os
import serial
import pynmea2

f = 'yes'
g = 'no'
j=116.3499066
k=40.0049290
h=0

def Love(inputdata):
    global f
    global g
    global j
    global k
    global h
    if inputdata.startswith('$GNRMC'):
        rmc=pynmea2.parse(inputdata)
        if (len(str(rmc.latitude).split(".")[1]) >= 14) and (len(str(rmc.longitude).split(".")[1]) >= 14):
            a = round(rmc.latitude,7)
            b = round(rmc.longitude,7)
            if (abs(a-j)<=4e-2)and(abs(b-k)<=4e-2):
                print(f)
            else:
                print(g)
            # print("Latitude:",round(rmc.latitude,6))
            # print("Longitude:",round(rmc.longitude,6))
        #os.system("python video2new.py {}".format(h))

if __name__ == '__main__':
    ser = serial.Serial('com5', '38400', timeout=0.5)
    print(ser.is_open)
    while (1):
        datahex = ser.readline()
        datahex = str(datahex, encoding='utf-8')
        Love(datahex)
