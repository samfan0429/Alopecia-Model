# %matplotlib notebook
from numpy import *
from numpy.random import rand, randint
import matplotlib.pyplot as plt


deltaTCell = 0.5

# Hair Entities
class Hair(object):
    def __init__(self):
        self.growing = True
        self.growthCapacity = 1.0
        self.growth = 0.5
        self.growthRate = 0.1
        self.TCell = 1.6
        self.artery = False
    def checkGrowing(self):
        if self.growthRate<0.01:
            self.growing = False
        return self.growing
    def TCellGrow(self,growthRate):
        if self.artery:
            self.TCell+=0.2
        self.TCell+=growthRate

# Creating the head
class SadHair(object):
    def __init__(self,size):
        # N is the total number of hair slots
        self.N=size
        self.hairs = empty((self.N,self.N),dtype=object)
        self.fillHairs()

    def fillHairs(self):
        for j in range(self.N):
            for i in range(self.N):
                tmp = Hair()
                self.hairs[j,i] = tmp

    def setUp(self):
        for j in range(self.N):
            for i in range(self.N):
                self.hairs[j,i].growth = rand()
                if j>0.90*self.N and (i<0.4*self.N or i>0.6*self.N):
                    self.hairs[j,i].TCell+=0.4
                    self.hairs[j,i].artery = True
                if j>0.3*self.N and j<0.6*self.N and (i<0.6*self.N and i>0.4*self.N):
                    self.hairs[j,i].TCell+=0.4
                    self.hairs[j,i].artery = True

    def action(self):
        for j in range(self.N):
            for i in range(self.N):
                oneHair = self.hairs[j,i]
                # Hair pops off when reaching max capacity
                if oneHair.growth >=oneHair.growthCapacity:
                    oneHair.growth = 0
                # if oneHair.checkGrowing() == True:
                #     # Hair growth update
                oneHair.growth += oneHair.growthRate
                oneHair.growthRate = 0.1*oneHair.growthCapacity # Update growth rate
                oneHair.growthCapacity = 1-1/(1+exp((-1)*oneHair.TCell+7.0)) # Update capacity
                TCellGrowth = 0
                # if oneHair.TCell>=10.0:
                #     continue
                # We need to make the balding equally possible on left and right
                if i>= 0.5*self.N:
                    if i+1 < self.N:
                        if self.hairs[j,i+1].TCell > 1.00:
                            TCellGrowth+=self.hairs[j,i+1].TCell*0.2
                            self.hairs[j,i+1].TCell-=self.hairs[j,i+1].TCell*0.2
                    if i-1 >=0:
                        if self.hairs[j,i-1].TCell > 1.00:
                            TCellGrowth+=self.hairs[j,i-1].TCell*0.2
                            self.hairs[j,i-1].TCell-=self.hairs[j,i-1].TCell*0.2
                elif i<= 0.5*self.N:
                    if i-1 >=0:
                        if self.hairs[j,i-1].TCell > 1.00:
                            TCellGrowth+=self.hairs[j,i-1].TCell*0.2
                            self.hairs[j,i-1].TCell-=self.hairs[j,i-1].TCell*0.2
                    if i+1 < self.N:
                        if self.hairs[j,i+1].TCell > 1.00:
                            TCellGrowth+=self.hairs[j,i+1].TCell*0.2
                            self.hairs[j,i+1].TCell-=self.hairs[j,i+1].TCell*0.2
                # Check the front and back part of its location first.
                if j+1 < self.N:
                    if self.hairs[j+1,i].TCell > 1.20:
                        TCellGrowth+=self.hairs[j+1,i].TCell*0.2
                        self.hairs[j+1,i].TCell-=self.hairs[j+1,i].TCell*0.2
                if j-1 >=0:
                    if self.hairs[j-1,i].TCell > 1.20:
                        TCellGrowth+=self.hairs[j-1,i].TCell*0.2
                        self.hairs[j-1,i].TCell-=self.hairs[j-1,i].TCell*0.2
                oneHair.TCellGrow(TCellGrowth)

    def getTCells(self):
        res = zeros((self.N,self.N),dtype=float64)
        for j in range(self.N):
            for i in range(self.N):
                res[j,i]=self.hairs[j,i].TCell
        return res

    def getHairs(self):
        res = zeros((self.N,self.N),dtype=float64)
        for j in range(self.N):
            for i in range(self.N):
                res[j,i]=self.hairs[j,i].growth
        return res

    def getCapacities(self):
        res = zeros((self.N,self.N),dtype=float64)
        for j in range(self.N):
            for i in range(self.N):
                res[j,i]=self.hairs[j,i].growthCapacity
        return res

origin = 'lower'

Tlevels = linspace(0.0,2.5,10)#[0.0,1.0,2.0,3.0,4.0]#,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0]

height = 20
width = 20
size =100

hairLevels = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

x = linspace(0,width,size)
y = linspace(0,height,size)
# Z = x**2+(y+4)**2

X,Y =meshgrid(x,y)

hairs = SadHair(size)
hairs.setUp()
res = hairs.getHairs()

fig1, ax2 = plt.subplots(constrained_layout=True)
CS = ax2.contourf(X, Y, res, hairLevels, cmap=plt.cm.bone, origin=origin)

# Note that in the following, we explicitly pass in a subset of
# the contour levels used for the filled contours.  Alternatively,
# We could pass in additional levels to provide extra resolution,
# or leave out the levels kwarg to use all of the original levels.

CS2 = ax2.contour(CS, Tlevels, origin=origin)

# ax2.set_title('T-Cell Level')
ax2.set_title('Hair Growth')
ax2.set_xlabel('x-direction of the head')
ax2.set_ylabel('y-direction of the head')

# Make a colorbar for the ContourSet returned by the contourf call.
cbar = fig1.colorbar(CS)
# cbar.ax.set_ylabel('T-Cell Level')
cbar.ax.set_ylabel('Hair Growth')
# Add the contour line levels to the colorbar
cbar.add_lines(CS2)

# plt.savefig("Hair_test_t=0.png")
# plt.savefig("TCell_t=0.png")

# For simplicity, let dt=1
for t in range(1,201):
    
    hairs.action()
    if t>100:
        res = hairs.getHairs()
        fig1, ax2 = plt.subplots(constrained_layout=True)
        CS = ax2.contourf(X, Y, res, hairLevels, cmap=plt.cm.bone, origin=origin)

        # Note that in the following, we explicitly pass in a subset of
        # the contour levels used for the filled contours.  Alternatively,
        # We could pass in additional levels to provide extra resolution,
        # or leave out the levels kwarg to use all of the original levels.

        CS2 = ax2.contour(CS, hairLevels, origin=origin)

        # ax2.set_title('T-Cell Concentration')
        ax2.set_title('Hair Growth')
        ax2.set_xlabel('x-direction of the head')
        ax2.set_ylabel('y-direction of the head')

        # Make a colorbar for the ContourSet returned by the contourf call.
        cbar = fig1.colorbar(CS)
        cbar.ax.set_ylabel('T-Cell Concentration')
        cbar.ax.set_ylabel('Hair Growth')
        # Add the contour line levels to the colorbar
        cbar.add_lines(CS2)

        plt.savefig("Hair_test_t={}.png".format(t))
# plt.show()
