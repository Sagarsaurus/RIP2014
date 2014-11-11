# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 20:28:14 2014

@author: Richard
"""
from util import *
import random 

class RRT:
    
    def __init__(self, mapSize, start, goal, obstacles):
        self.mapSize=mapSize
        self.start=start
        self.goal=goal
        self.obstacles=obstacles
        self.availablePoints=[]
        self.treeNodes=[]
        self.treePoints=[]
        
    def avPoints(self):
        for x in range(self.mapSize[0]):
            for y in range(self.mapSize[1]):
                hitSomething=False
                for o in self.obstacles:
                    if not o.collisionCheck((x,y)):
                       hitSomething=True
                if not hitSomething:
                    self.availablePoints.append((x,y))
        
    def baseline(self):
        self.availablePoints=[]
        self.avPoints()
        self.availablePoints.remove(self.start)
        self.treeNodes.append(self.start)
        self.treePoints.append(self.start)
        k=0
        while k<10:
            randIndex=random.randrange(len(self.availablePoints))
            point=self.availablePoints[randIndex]
            closestPoint=self.findClosestPoint(point)
#            newLine=Line(point,closestPoint)
            if len(raycast(Vector2(point[0],point[1]), Vector2(closestPoint[0],closestPoint[1]), self.obstacles, limitedRay = True))<1:
                self.treeNodes.append(point)
            
            k+=1
            
    def findClosestPoint(self,point):
        closestVal=self.mapSize[0]+self.mapSize[1]
        closestPoint=None
        pVector=Vector2(point[1],point[1])
        for tPoint in self.treePoints:
            val=(pVector-Vector2(tPoint[0],tPoint[1])).magnitude()
            if val<closestVal:
                closestVal=val
                closestPoint=tPoint
        return closestPoint
    
    def goalDirected(self):
        self.avPoints=[]
        self.avPoints()
        
    def connect(self):
        self.avPoints=[]
        self.avPoints()
    
    def bidirectional(self):
        self.avPoints=[]
        self.avPoints()
        

start=(10,60)
goal=(210,75)
mapsize=(230,150)
randomTree1=RRT(mapsize,start,goal,[])
obs=[CircleObstacle(50,60,20),CircleObstacle(150,75,35)]
randomTree1.baseline()

#zArr=np.zeroes((randomTree1.mapSize))
#cv2.imwrite("test.jpg",randomTree1.points)