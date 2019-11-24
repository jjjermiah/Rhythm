# -*- coding: utf-8 -*-
"""
Created on November 23rd 2019

Jermiah, Luke, Ajith, Nevalen
"""

import csv
import serial
import pandas as pd
try:
    arduino = serial.Serial("COM8", timeout=1, baudrate=9600)   # Try opening the port at a determined baud rate (bits per second)
except:
    print('Please check the port')


with open("datafile2.csv", "w") as new_file:
    csv_writer = csv.writer(new_file, lineterminator=',')

    line_count = 0
    while True:
        rawdata = str(arduino.readline().strip())  # Receive data and append to the list
        line_count += 1
        if(line_count>2):
            def clean(L):  # L is a list
                temp = L[2:]
                temp = temp[:-1]
                return int(temp)/1024
            cleandata = clean(rawdata)
            csv_writer.writerow([cleandata])

        if(line_count>188):
            break

print("Recording Complete")
