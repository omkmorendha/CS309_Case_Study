# with open('Data.csv', 'r') as inp:
#     lines = inp.readlines()

# with open('purged_csv_file.csv', 'w') as out:
#     for line in lines:
#         if not '?' in line:
#             out.write(line)

import pandas as pd
import random as rand

def mean(arr):
    total = 0
    for element in arr:
        total += element
    
    return total / len(arr)

def sd(arr):
    ans = 0
    m = mean(arr)

    for element in arr:
        ans += (element - m) ** 2

    return ans / len(arr)

def srs(arr, n):
    visited = []

    while(len(visited) < n and len(visited) < len(arr)):
        i = rand.randint(0, len(arr) - 1)        
        
        if (arr[i] not in visited):
            visited.append(arr[i])

    return visited        

data = pd.read_csv("purged_csv_file.csv")
index = data["index"].tolist()
date = data["Date"].tolist()
time = data["Time"].tolist()
gap = data["Global_active_power"].tolist()
grp = data["Global_reactive_power"].tolist()

vol = data["Voltage"].tolist()
vol = [float(i) for i in vol]

gint = data["Global_intensity"].tolist()
sub1 = data["Sub_metering_1"].tolist()
sub2 = data["Sub_metering_2"].tolist()
sub3 = data["Sub_metering_3"].tolist() 
