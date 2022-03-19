import io_csv
import math
import numpy

a=numpy.linspace(0,2*numpy.pi*(15.0/16.0),16)
phi=numpy.linspace(0,2*numpy.pi*(15.0/16.0),16)
r=5
coords=[]

for itp in phi:
    Ry=numpy.matrix([[1,0,0],[0,math.cos(itp),math.sin(itp)],[0,-math.sin(itp),math.cos(itp)]])
    for ita in a:
        vec_0=numpy.matrix([[1.6*(math.sin(ita)**3)],[0],[r+1.3*math.cos(ita)-0.5*math.cos(2*ita)-0.2*math.cos(3*ita)-0.1*math.cos(4*ita)]]);
        vec=Ry*vec_0
        coords.append([itp,ita,vec[0],vec[1],vec[2]])

io_csv.saveCSV("example_hearttorus.csv",coords,delimiter=',')