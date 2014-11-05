# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 21:13:07 2014

@author: Richard
"""

import math
import numpy as np
from matplotlib import pyplot as plt
from util import *
import cv2

class FieldMapGenerator:
    def __init__(self, mapSize, goal, obstacles,minDistance):
        self.mapSize=mapSize
        self.obstacles=obstacles
        self.goal=goal
        self.minDistance=minDistance
        self.map=[]
    
    def computeField(self):
        self.map=np.zeros((mapSize[1],mapSize[0]))
        self.attractionField()
        self.repulsionField()
        return self.map
    
    #to start this will just compute linear distance function (Quadradic to be added later)
    def attractionField(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                self.map[y][x]+=math.sqrt(pow(self.goal[0]-x,2)+pow(self.goal[1]-y,2))
        return self.map
        
    def repulsionField(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                hitSomething,hitWhat= self.collisionCheck((x,y))
                if not hitSomething:
                    #I believe the factor v here is up to me, try a couple
                    v=1
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print x
                    print y
                    print hitWhat.distanceTo((x,y))
                    print hitWhat.x
                    print hitWhat.y
                    self.map[y][x]+=.5*v*pow(1/hitWhat.distanceTo((x,y))-1/self.minDistance,2)
        
        
    def collisionCheck(self, point):
        for obs in self.obstacles:
            if obs.nearCheck(point,self.minDistance):
                return False,obs
        return True, None
    
    #Leave this here for a moment to normalize for visualization purposes
    def fit(self, array, nmax):
        min=array[0][0]
        max=array[0][0]
        for x in array:
            for y in x:
                if y>max:
                    max=y
                if y<min:
                    min=y
        max-=min
        for x in range(len(array)):
            for y in range(len(array[x])):
                array[x][y]=(array[x][y]-min)/max*nmax
        return array

class Agent:
    def __init__(self,start,goal,mapSize,obstacles,minDistance):
        self.start=start
        self.goal=goal
        self.mapSize=mapSize
        self.obstacles=obstacles
        self.curPos=start
        self.minDistance=minDistance
        
    
    def run(self):
        fmapGen=FieldMapGenerator(mapSize,goal,obstacles,minDistance)
        fmap=fmapGen.computeField()
        while not self.atGoal(self.curPos):
            nextPos=self.chooseNext(fmap)
            if nextPost==self.curPos and not self.atGoal(self.curPos):
                print "Algorithm got stuck"
                break;
            self.curPos=nextPos
            
    def chooseNext(self,fmap):
        best=fmap[self.curPos[0]][self.curPos[1]]
        bestPos=self.curPos
        for x in range(-1,1):
            for y in range(-1,1):
                if fmap[self.bestPos[0]+x][self.bestPos[1]+y]<best:
                    best=fmap[self.bestPos[0]+x][self.bestPos[1]+y]
                    bestPos=(self.bestPos[0]+x,self.bestPos[1]+y)
        return bestPos
                
    
    def atGoal(self, pos):
        return pos == self.goal(self.curPos)
        
#TESTING AREA
obstacles=[CircleObstacle(50,60,20),CircleObstacle(150,75,135)]
start=(10,60)
goal=(210,75)
mapSize=(230,300)
minDistance=5
a=Agent(start,goal,mapSize,obstacles,minDistance)
FMG=FieldMapGenerator(mapSize, goal, obstacles,minDistance)
#plt.imshow(FMG.computeField,cmap="gray")
cv2.imwrite("test.jpg",FMG.computeField())
