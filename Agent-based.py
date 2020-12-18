# %matplotlib notebook
from numpy import *
from numpy.random import rand, randint
import matplotlib.pyplot as plt


# deltaTCell = 0.5

# Hair Entities
class Hair(object):
    def __init__(self):
        # self.growing = True # It is not used for our simulation please ignore
        self.growthCapacity = 1.0
        self.growth = 0.5
        self.growthRate = 0.1
        self.TCell = 1.5
        self.artery = False # This tells us if the hair will be introducing new T-Cells to the system.
    def checkGrowing(self):
        if self.growthRate<0.01:
            self.growing = False
        return self.growing
    def TCellGrow(self, growth):
        if self.artery:
            self.TCell+=0.3
        self.TCell+=growth

# Creating the head
class SadHair(object):
    def __init__(self,size):
        # N is the total number of hair slots
        self.N=size
        self.hairs = empty((self.N,self.N),dtype=object)
        self.fillHairs()
    # Initializes each grid with Hair object.
    def fillHairs(self):
        for j in range(self.N):
            for i in range(self.N):
                tmp = Hair()
                self.hairs[j,i] = tmp
    # Initialize places with extra T-Cells and the sources of T-Cells
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
    # Gets T-Cells spilled from back
    def toBack(self,j,i):
        if j-1 >=0:
            if self.hairs[j-1,i].TCell > 1.20:
                increase = self.hairs[j-1,i].TCell*0.25
                self.hairs[j-1,i].TCell-=self.hairs[j-1,i].TCell*0.25
                return increase
        return 0
    # Gets T-Cells spilled from front
    def toFront(self,j,i):
        if j+1 < self.N:
            if self.hairs[j+1,i].TCell > 1.20:
                increase = self.hairs[j+1,i].TCell*0.25
                self.hairs[j+1,i].TCell-=self.hairs[j+1,i].TCell*0.25
                return increase
        return 0
    # Gets T-Cells spilled from right
    def toRight(self,j,i):
        if i-1 < self.N:
            if self.hairs[j,i-1].TCell > 1.20:
                increase = self.hairs[j,i-1].TCell*0.25
                self.hairs[j,i-1].TCell-=self.hairs[j,i-1].TCell*0.25
                return increase
        return 0
    # Gets T-Cells spilled from left
    def toLeft(self,j,i):
        if i+1 < self.N:
            if self.hairs[j,i+1].TCell > 1.20:
                increase = self.hairs[j,i+1].TCell*0.25
                self.hairs[j,i+1].TCell-=self.hairs[j,i+1].TCell*0.25
                return increase
        return 0
    # We progress in time one step in action function.
    def action(self,t):
        for j in range(self.N):
            for i in range(self.N):
                oneHair = self.hairs[j,i]
                # Hair pops off when reaching max capacity
                if oneHair.growth >=oneHair.growthCapacity:
                    oneHair.growth = 0

                oneHair.growth += oneHair.growthRate

                oneHair.growthCapacity = 1-1/(1+exp((-1)*oneHair.TCell+4.0)) # Update capacity
                TCellGrowth = 0

                # T-Cell spills from one of the 4 directions.
                dir = randint(4)
                
                if dir == 0:
                    TCellGrowth+=self.toBack(j,i)
                elif dir == 1:
                    TCellGrowth+=self.toFront(j,i)
                elif dir == 2:
                    TCellGrowth+=self.toRight(j,i)
                else:
                    TCellGrowth+=self.toLeft(j,i)
                oneHair.TCellGrow(TCellGrowth)
    # Return T-Cell values for the grid.
    def getTCells(self):
        res = zeros((self.N,self.N),dtype=float64)
        for j in range(self.N):
            for i in range(self.N):
                res[j,i]=self.hairs[j,i].TCell
        return res
    # Return current growth values for the grid.
    def getHairs(self):
        res = zeros((self.N,self.N),dtype=float64)
        for j in range(self.N):
            for i in range(self.N):
                res[j,i]=self.hairs[j,i].growth
        return res
    # Return current growth capacities values for the grid.
    def getCapacities(self):
        res = zeros((self.N,self.N),dtype=float64)
        for j in range(self.N):
            for i in range(self.N):
                res[j,i]=self.hairs[j,i].growthCapacity
        return res

origin = 'lower'
# Show the levels of T-Cells
TLevels = [0.0,0.5, 1.0,1.5,2.0,2.5,3.0]#,4.0]#,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0]
# Tlevels = linspace(0.0,3,3)
# Tlevels = [0.0,1.0,2.0,3.0,4.0]
height = 20
width = 20
size =100 # The grids will be creates with the number of size-by-size.
# The levels of hair growth divided into 1/10
hairLevels = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

x = linspace(0,width,size)
y = linspace(0,height,size)
# Z = x**2+(y+4)**2

X,Y =meshgrid(x,y)

hairs = SadHair(size)
hairs.setUp()
# res = hairs.getTCells()
res = hairs.getHairs()

fig1, ax2 = plt.subplots(constrained_layout=True)
CS = ax2.contourf(X, Y, res, hairLevels, cmap=plt.cm.bone, origin=origin)

CS2 = ax2.contour(CS, hairLevels, origin=origin)

# ax2.set_title('T-Cell Contour')
ax2.set_title('Hair Growth')
ax2.set_xlabel('x-direction of the head')
ax2.set_ylabel('y-direction of the head')

# Make a colorbar for the ContourSet returned by the contourf call.
cbar = fig1.colorbar(CS)
# cbar.ax.set_ylabel('T-Cell Excess Level')
cbar.ax.set_ylabel('Hair Growth')
# Add the contour line levels to the colorbar
cbar.add_lines(CS2)

plt.savefig("HairGrowth_t=0.png")
# plt.savefig("TCell_t=0.png")

# For simplicity, let dt=1
for t in range(1,721):
    
    # number = randint(4)
    # counter[number]+=1
    # print("Random Number is {}".format(number))
    hairs.action(t)
    if t>700:
        # res = hairs.getTCells()
        res = hairs.getHairs()
        fig1, ax2 = plt.subplots(constrained_layout=True)
        CS = ax2.contourf(X, Y, res, hairLevels, cmap=plt.cm.bone, origin=origin)

        CS2 = ax2.contour(CS, hairLevels, origin=origin)

        # ax2.set_title('T-Cell Level')
        ax2.set_title('Hair Growth')
        ax2.set_xlabel('x-direction of the head')
        ax2.set_ylabel('y-direction of the head')

        # Make a colorbar for the ContourSet returned by the contourf call.
        cbar = fig1.colorbar(CS)
        # cbar.ax.set_ylabel('T-Cell Concentration')
        cbar.ax.set_ylabel('Hair Growth')
        # Add the contour line levels to the colorbar
        cbar.add_lines(CS2)

        plt.savefig("HairGrowth_t={}.png".format(t))
        # plt.savefig("TCell_t={}.png".format(t))
        del(fig1)
        del(ax2)
        plt.close('all')
# plt.show()
