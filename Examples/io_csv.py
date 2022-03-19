#!/usr/bin/python3
# by Sun Smallwhite <niasw@pku.edu.cn>(https://github.com/niasw)

import csv
import numpy

def loadCSV(filename,delimiter='\t',skiprows=0,skipcols=0):
  '''
# Load CSV data
# by Sun Smallwhite <niasw@pku.edu.cn>(https://github.com/niasw)
# default delimiter = whitespace

# input:
#  filename
# output:
#  data
  '''
  f=None;
  ret=None;
  try:
    f=open(filename,'r');
    reader=csv.reader(f,delimiter=delimiter);
    current_row=0;
    while (current_row<skiprows):
        current_row+=1;
        ret_row=next(reader);
    ret=[]
    for row in reader:
        ret_tmp=[float(it) for it in row[skipcols:]];
        ret.append(ret_tmp);
    #ret=numpy.loadtxt(f,delimiter=delimiter,skiprows=skiprows);
  except Exception as e:
    raise(e);
  finally:
    if f is not None:
      f.close();
  return ret;

def loadCSV_whitespace(filename,skiprows=0,skipcols=0):
  '''
# Load Text data splited with whitespace
# by Sun Smallwhite <niasw@pku.edu.cn>(https://github.com/niasw)

# input:
#  filename
# output:
#  text
  '''
  fileobj=None;
  try:
    fileobj=open(filename,'r');
    data=fileobj.readlines();
  finally:
    if fileobj is not None:
      fileobj.close()
  num=len(data);
  ret=[];
  for it in range(skiprows,num):
    row=data[it].split();
    ret_tmp=[float(da) for da in row[skipcols:]];
    ret.append(ret_tmp);
  return ret;

def saveCSV(filename,variable,delimiter=' '):
  '''
# Save CSV data
# by Sun Smallwhite <niasw@pku.edu.cn>(https://github.com/niasw)

# input:
#  filename
# output:
#  data
  '''
  f=None;
  try:
    f=open(filename,'w');
    numpy.savetxt(f,variable,fmt="%g",delimiter=delimiter);
  except Exception as e:
    raise(e);
  finally:
    if f is not None:
      f.close();

