import io_csv
import math
import numpy

a=numpy.linspace(0,2*numpy.pi*(7.0/8.0),8)
r=numpy.linspace(-0.2,0.2,3)

vec_0=numpy.matrix([[0],[1],[0]])
vec_1=numpy.matrix([[0],[0],[1]])

coords=[]

for ita in a:
	Rz=numpy.matrix([[math.cos(ita),math.sin(ita),0],[-math.sin(ita),math.cos(ita),0],[0,0,1]])
	Rx=numpy.matrix([[1,0,0],[0,math.cos(ita/2),math.sin(ita/2)],[0,-math.sin(ita/2),math.cos(ita/2)]])
	vec=Rz*vec_0
	for itr in r:
		vec_r=vec+itr*Rz*Rx*vec_1
		coords.append([ita,itr,vec_r[0],vec_r[1],vec_r[2]])

io_csv.saveCSV("example_mobius.csv",coords,delimiter=',')