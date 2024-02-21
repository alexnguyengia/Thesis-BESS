'''
This module comprises of 3 functions: 
pltload() 
degradation()
cycles()
______________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________

'''

import numpy as np
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import time
import datetime
from tabulate import tabulate
from datetime import datetime, timedelta, timezone

'''
______________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________

'''
#pltload: This function graphs the load profiles before and after (new load profile) with the battery. 
#The inputs are the dataframe with the information of the load profiles, the interval in which the graph will be plot and the name of the graph.
def pltload(df,a,b,c):
    plt.plot(df.Data[a:b], df.Power[a:b], label='Load Profile')
    plt.plot(df.Data[a:b], df.NP[a:b], '-b', label='New Profile')
    plt.grid(True)
    plt.fill_between(df.Data[a:b], df['Power'][a:b], df['NP'][a:b], where=df['Power'][a:b] >= df['NP'][a:b],facecolor='green', alpha=0.2, interpolate=True, label='Discharging')
    plt.fill_between(df.Data[a:b], df['Power'][a:b], df['NP'][a:b], where=df['Power'][a:b] <= df['NP'][a:b],facecolor='red', alpha=0.2, interpolate=True, label='Charging')
    plt.xlabel("Time")
    plt.ylabel("Power")
    plt.title(c)
    plt.legend()
    plt.show()
    return


'''
______________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________

'''
#degradation: The inputs are the degradation and years of life in both models. This function graphs the comparison of the degradation in both models along the years.
def degradation(deg1, years1, deg2, years2):
    
    print("\n=====================================")
    print("   Degradation comparison")
    print("=====================================")
    
    year = int(min(years1, years2))
        
    x=[]
    y1=[]
    y2=[]
    
    for i in range (year):
        x.append(i)
        y1.append(100*(1-deg1/100*i))
        y2.append(100*(1-deg2/100*i))
    
    plt.plot(x, y1, label='Model 1')
    plt.plot(x, y2, label='Model 2')
    plt.grid(True)
    plt.xlabel("Years")
    plt.ylabel("SoH[%]")
    plt.title('Degradation comparison Model 1 (Equivalent cycles at DoD=100%) and Model 2 (Cycles per each DoD)')
    plt.legend()
    plt.show()
    return


'''
______________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________

'''
#cycles: This function is related to lithium battery model. It has the graph of the cycles vs. DoD and calculates the degradation according to the cycles in each DoD. 
#The input is the average number of DoD per cycle (partial or full) and the list with the value of every DoD per hour. The outputs of this function are the degradation and the number of years of the battery life.

def cycles(cl, DoD):
    x = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y = [10**6, 2*10**5, 6*10**4, 4*10**4, 2*10**4, 1.5*10**4, 1.1*10**4, 10**4, 8*10**3, 7*10**3, 6*10**3]
    
    #Calculation of the sum of the delta of the state of health
    SoH=[]
    for i in range(len(DoD)):
        if DoD[i]==0:
            SoH.append(0)
        else:
            if DoD[i]<10:
                SoH.append(1/(-160000*DoD[i]+2*10**6))
            elif (DoD[i]>=10)&(DoD[i]<20):
                SoH.append(1/(-14000*DoD[i]+340000))
            elif (DoD[i]>=20)&(DoD[i]<40):
                SoH.append(1/(-2000*DoD[i]+100000))
            elif (DoD[i]>=40)&(DoD[i]<=100):
                SoH.append(1/((2.38*10**6)*DoD[i]**-1.297))
            else:
                SoH.append(0)
    Delta_SoH=sum(SoH)
    
    
    ax=np.round(cl,2)
    if ax<10:
        ay=-160000*ax+2*10**6
    elif (ax>=10)&(ax<20):
        ay=-14000*ax+340000
    elif (ax>=20)&(ax<40):
        ay=-2000*ax+100000
    elif (ax>=40)&(ax<=100):
        ay=round((2.38*10**6)*ax**-1.297,1)
    else:
        ay=0
    
    print("=====================================")
    print("   Model 2")
    print("=====================================")
    
    plt.grid(True)
    plt.plot(x,y)
    plt.plot(ax,ay, "o")
    plt.xlabel("DoD - Depth of Discharge")
    plt.ylabel("Cycle life")
    plt.title("Model 2: Cycle-life Battery LiFePO4")
    plt.text(ax+1,ay+1, "DoD: "+str(round(ax,1))+"%\n Cycles: "+str("{:,}".format(ay)))
    plt.show()
    
    print('According to this model the number of cycles are:', round(ay, 1))
    print('with this considerations the years are:',round(ay/(2*365),2),'with a degradation of', round(Delta_SoH*20,3), '% per year')
    print('the capacity available at the end of the first year is', 100-round(Delta_SoH*20,2), '%')
    print("This model was created considering articles about lithium batteries.")
    return (round(Delta_SoH*20,3), round(ay/(2*365),2))