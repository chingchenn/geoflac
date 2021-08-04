# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 20:08:41 2020

@author: jiching

"""
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

def save_1array(title,path,array1,name1):
    aaa=DataFrame(array1,columns=[str(name1)])
    aaa.to_csv(path+'/'+str(title)+'.csv',index=False)

def save_2array(title,path,array1,array2,name1,name2):
    aaa=DataFrame(array1,columns=[str(name1)])
    bbb=DataFrame(array2,columns=[str(name2)])
    n2 = pd.concat([aaa,bbb],axis=1)
    n2.to_csv(path+'/'+str(title)+'.csv',index=False)
   
def save_3array(title,path,array1,array2,array3,name1,name2,name3):
    aaa=DataFrame(array1,columns=[str(name1)])
    bbb=DataFrame(array2,columns=[str(name2)])
    ccc=DataFrame(array3,columns=[str(name3)])
    n3 = pd.concat([aaa,bbb,ccc],axis=1)
    n3.to_csv(path+'/'+str(title)+'.csv',index=False)
    
def save_4array(title,path,array1,array2,array3,array4,name1,name2,name3,name4):
    aaa=DataFrame(array1,columns=[str(name1)])
    bbb=DataFrame(array2,columns=[str(name2)])
    ccc=DataFrame(array3,columns=[str(name3)])
    ddd=DataFrame(array4,columns=[str(name4)])
    n4 = pd.concat([aaa,bbb,ccc,ddd],axis=1)
    n4.to_csv(path+'/'+str(title)+'.csv',index=False) 

def save_5array(title,path,array1,array2,array3,array4,array5,name1,name2,name3,name4,name5):
    aaa=DataFrame(array1,columns=[str(name1)])
    bbb=DataFrame(array2,columns=[str(name2)])
    ccc=DataFrame(array3,columns=[str(name3)])
    ddd=DataFrame(array4,columns=[str(name4)])
    eee=DataFrame(array5,columns=[str(name5)])
    n5 = pd.concat([aaa,bbb,ccc,ddd,eee],axis=1)
    n5.to_csv(path+'/'+str(title)+'.csv',index=False)
    
def save_6array(title,path,array1,array2,array3,array4,array5,array6,name1,name2,name3,name4,name5,name6):
    aaa=DataFrame(array1,columns=[str(name1)])
    bbb=DataFrame(array2,columns=[str(name2)])
    ccc=DataFrame(array3,columns=[str(name3)])
    ddd=DataFrame(array4,columns=[str(name4)])
    eee=DataFrame(array5,columns=[str(name5)])
    fff=DataFrame(array6,columns=[str(name6)])
    n6 = pd.concat([aaa,bbb,ccc,ddd,eee,fff],axis=1)
    n6.to_csv(path+'/'+str(title)+'.csv',index=False)

def read_data(title,path):
    file=pd.read_csv(path+'/'+title+'.csv')
    file=np.array(file)
    return file

def read_data_column(title,path,column_index):
    file=pd.read_csv(path+'/'+title+'.csv')
    temp2=file[(column_index-1)]
    temp2=temp2.tolist()
    return temp2
