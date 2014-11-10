# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 21:13:07 2014

@author: Richard
"""

import math
from util import *
import numpy as np
import cv2

def init2D(width, height, value=0):
    newList=[]
    temp=[]
    for i in range(0,width):
        for j in range(0,height):
            temp.append(value)
        newList.append(temp)
        temp=[]
    return newList
    
class FieldMapGenerator:
    def __init__(self, mapSize, goal, obstacles,minDistance):
        self.mapSize=mapSize
        self.obstacles=obstacles
        self.goal=goal
        self.minDistance=minDistance
        self.map=init2D(mapSize[1],mapSize[0])
    
    def computeField(self):
        self.attractionField()
        self.repulsionField()
        self.map=self.boxFilter(5)
        return self.map
    
    def boxFilter(self,winSize):
        temp=init2D(self.mapSize[1],self.mapSize[0])
        for x in range(self.mapSize[0]):
            for y in range(self.mapSize[1]):
                s=0
                count=0
                for i in range(-winSize,winSize):
                    for j in range(-winSize,winSize):

                        if x+i>0 and y+j>0 and x+i<self.mapSize[0] and y+j<self.mapSize[1]:
                            s+=self.map[y][x]
                            count+=1
                temp[y][x]=s/count
        return temp
                         
                        
    
    #to start this will just compute linear distance function (Quadradic to be added later)
    def attractionField(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                self.map[y][x]+=math.sqrt(pow(self.goal[0]-x,2)+pow(self.goal[1]-y,2))
        return self.map
    
#    def applyGaussian(winSize,sigma):
        
    
    def repulsionField(self):
        for x in range(self.mapSize[0]):
            for y in range(self.mapSize[1]):
                hitSomething,hitWhat= self.collisionCheck((x,y))
                if hitSomething:
                    #I believe the factor v here is up to me, try a couple
                    v=4000
                    highestPoint=0
                    for o in hitWhat:
                        if o.distanceTo((x,y))<=0:
                            highestPoint=255
                        else:
                            if .5*v*pow(1/o.distanceTo((x,y))-1/self.minDistance,2)>255:
                                highestPoint=255
                            else:
                                num=.5*v*pow(1/o.distanceTo((x,y))-1/self.minDistance,2)
                                if num>highestPoint:
                                    highestPoint=num
                    self.map[y][x]+=highestPoint
        return self.map
        
    def collisionCheck(self, point):
        o=[]
        for obs in self.obstacles:
            if obs.nearCheck(point,self.minDistance):
                o.append(obs)
        if len(o)>=1:
            return True,o
        return False, None
    
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
        self.plan=[]
        
    
    def run(self):
        self.plan=[start]
        
        fmapGen=FieldMapGenerator(mapSize,goal,obstacles,minDistance)
        fmap=fmapGen.computeField()
        print "Made the map"
        while not self.atGoal(self.curPos):
            nextPos=self.chooseNext(fmap)
            if nextPos==self.curPos and not self.atGoal(self.curPos):
                print "Algorithm got stuck"
                break;
            self.plan.append(nextPos)
            self.curPos=nextPos
        return self.plan,fmap
            
    def chooseNext(self,fmap):
        best=fmap[self.curPos[1]][self.curPos[0]]
        bestPos=self.curPos
        for x in range(-1,2):
            for y in range(-1,2):
                if self.curPos[1]+y>=0 and self.curPos[1]+y< self.mapSize[1] and self.curPos[0]+x>=0 and self.curPos[0]+x<= self.mapSize[0] and fmap[self.curPos[1]+y][self.curPos[0]+x]<best:
                    best=fmap[self.curPos[1]+y][self.curPos[0]+x]
                    bestPos=(self.curPos[0]+x,self.curPos[1]+y)
        return bestPos
                
    
    def atGoal(self, pos):
        return pos == self.goal
        
def fit(array, nmax):
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
    
#TESTING AREA
obstacles=[CircleObstacle(50,60,20),CircleObstacle(150,75,35)]
#,CircleObstacle(150,130,10)
start=(10,60)
goal=(210,75)
mapSize=(230,150)
minDistance=30

#fmg=FieldMapGenerator(mapSize, goal, obstacles,minDistance)
#fmg.repulsionField()

a=Agent(start,goal,mapSize,obstacles,minDistance)
#FMG=FieldMapGenerator(mapSize, goal, obstacles,minDistance)
#img=FMG.computeField()
plan,fmap=a.run()
fmap=fit(fmap,255)
print len(plan)
for elt in plan:
    fmap[elt[1]][elt[0]]=255#-fmap[elt[1]][elt[0]]



cv2.imwrite("test.jpg",np.array(fmap))

