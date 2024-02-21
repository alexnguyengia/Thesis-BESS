'''
This Module  is for displaying the table of DOD of the batteries, results and considerations
'''

import numpy as np
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import time
import datetime
import tabulate
from tabulate import tabulate
from datetime import datetime, timedelta, timezone

'''
______________________________________________________________________________________________________________________________
'''
#Function to print the table of DoD 
def table_DoD(dtfm, eq):
    a=dtfm.loc[(dtfm["DoD"]>=90)].cumsum().max().fillna(0)
    b=dtfm.loc[(dtfm["DoD"]>=70)&(dtfm["DoD"]<90)].cumsum().max().fillna(0)
    c=dtfm.loc[(dtfm["DoD"]>=40)&(dtfm["DoD"]<70)].cumsum().max().fillna(0)
    d=dtfm.loc[(dtfm["DoD"]>20)&(dtfm["DoD"]<40)].cumsum().max().fillna(0)
    e=dtfm.loc[(dtfm["DoD"]<=20)].cumsum().max().fillna(0)

    # assign data
    mydata = [
        ["Full cycles", "90-100%", a.cycles, a.Hours, a.Days],
        ["High-Partial cycles","70-90%", b.cycles, b.Hours, b.Days],
        ["Medium cycles","40-70%", c.cycles, c. Hours, c.Days],
        ["Low-Partial cycles","20-40%", d.cycles, d.Hours, d.Days],
        ["Mycrocycles","0-20%", e.cycles, e.Hours, e.Days],
        ["TOTAL PER YEAR" ,  "Equivalent Cycles", round(eq,1), a.Hours+b.Hours+c.Hours+d.Hours+e.Hours, a.Days+b.Days+c.Days+d.Days+e.Days]
    ]
    
    # header
    head = ["Category","Range Discharge", "#Cycles", "Hours per year", "Days per year"]

    # display table
    print(tabulate(mydata, headers=head, tablefmt="grid"))
    return

'''
______________________________________________________________________________________________________________________________
'''
#Function to print in a table the results and the considerations, in this function, the battery size and the correction factors are calculated to compare the size according to the two models
def results(a,b,c,chem,deg1,ye1,deg2,ye2):
    
    print("=====================================")
    print("   Results")
    print("=====================================")
    
    #Initial considerations for the calculation
    grow=25 #Grow of the load
    loss=10 #Discharge losses
    
    if (chem==1):
        DoD1=80
        bat='Lithium NMC'
    elif(chem==2):
        DoD1=80
        bat='Lithium LFP'
    elif(chem==3):
        DoD1=95
        bat='Lithium LTO'
    elif(chem==4):
        DoD1=100
        bat='Vanadium'
    elif(chem==5):
        DoD1=100
        bat='NaS'
    else:
        print("Option no valid")
    
    
    F1=((1+deg1/100)*(1+grow/100))/((1-loss/100)*DoD1/100) #Correction factor model 1
    F2=((1+deg2/100)*(1+grow/100))/((1-loss/100)*80/100) #Correction factor model 2
    
    mydata = [
        ["Parameter","Model 1","Model 2"],
        ["Battery Power [kW]", round(a,1), round(a,1)],
        ["Battery Energy [kWh]",round(b*F1,1), round(b*F2,1)],
        ["Hours [h]",c,c],
        ["Degradation per year[%]",round(deg1,3),round(deg2,3)],
        ["Years",round(ye1,1),round(ye2,1)],
        ["Chemical",bat,'LiFePO4'],
        ['Factor correction',round(F1,3),round(F2,3)]
    ]
    print(tabulate(mydata, tablefmt="grid"))
    
    print('Follow considerations:')
    print('Grow of the load = ', grow,'%')
    print('Discharge losses = ', loss,'%')
    
    return