import matplotlib.pyplot as plt
import cv2 as cv
import json
import math
import csv
import progressbar 
from csv import writer
import time

#File handling
f = open("pathweaver.json")
data = json.load(f)


#CONSTANTS
HEIGHT = 10
WIDTH = 5
PATHS = 2
SCALE = 10/306.391625574076 
paths_array, slopes_array, degrees_array, real_distances = [] ,[], [], []

#animation for build
widgets = ['$Building Pathweaver 1.0 beta ', progressbar.AnimatedMarker()]
bar = progressbar.ProgressBar(widgets = widgets).start()
  
for i in range(10):
    time.sleep(0.1)
    bar.update(i)

#create waypoints
def createWaypoint(paths):
    global copy_x, copy_y
    ax = plt.gca()
    xy = plt.ginput(paths)
    x = [point[0] for point in xy]
    y = [point[1] for point in xy]
    line = plt.plot(x,y)
    ax.figure.canvas.draw()
   
    try:
        while len(x) != 1 and len(y) != 1:
            distance = getDistance(x[0], y[0], x[1], y[1])
            slope = getSlope(x[0], y[0], x[1], y[1])
            paths_array.append(distance)
            slopes_array.append(slope)
            x.pop(0)
            y.pop(0)
            
    except IndexError:
        print("PROGRAM MALFUNCTIONED")
   
    return paths_array
       

#distance between two points
def getDistance(x1, y1, x2, y2):
    distance = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    return distance

def scaleDistance(field_distances):
    global SCALE
    for i in field_distances:
        real_distances.append(SCALE*i)
        
    return real_distances
          
def getSlope(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    return slope

def getAngle(slope1, slope2):
    angle = (slope1 - slope2) / ((slope1 * slope2) + 1)
    
    return math.degrees(math.atan(angle))

def convertAngles(slopes_array):
    for i in range(len(slopes_array) - 1):
        angle = abs(getAngle(slopes_array[i], slopes_array[i + 1]))
        degrees_array.append(angle)
    return degrees_array

def csv_dump(degree, map_distances, real_distances):
    with open('paths.csv', mode = 'w') as deploy_paths:
        deploy = writer(deploy_paths, delimiter=',', quoting = csv.QUOTE_MINIMAL)
        deploy.writerow([degree, map_distances, real_distances])
       
        
#load pathweaver image
display = cv.imread(r"C:\Users\laks\Desktop\field.png")
plt.figure(figsize=(HEIGHT, WIDTH))
plt.gcf().canvas.set_window_title("Pathweaver v1.0 beta")
plt.imshow(display)

#Create custom path
createWaypoint(PATHS*2)
csv_dump(convertAngles(slopes_array), paths_array, scaleDistance(paths_array))

#animation for saving 
plt.show()