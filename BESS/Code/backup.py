import numpy as np
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import time
import datetime
from tabulate import tabulate
from datetime import datetime, timedelta, timezone

import model 
import lifecycleplotting as lcplot
import degradetime as degrade
import plotting 
import bessresult

def backup(df1):
    """Third case - Backup"""
    
    horas=float(input("How many hours of Back-up energy?: "))#Number of hours of blackout
    eq=float(input("How many days of the year?: ")) #Probability of the black out in the year (number of cycles that could happen)
    critical=float(input("What is the % of the critical load: "))
    df_test=pd.DataFrame(df1.groupby(pd.Grouper(key='Data', freq=pd.Timedelta(hours=horas) )).sum())#In this dataframe it is collected the ammount of energy during the specific number of hours
     
    
    chem=model.model1() 
    degrade.years(eq,chem)
    
    #===================================================================
    #Calculations
    grow=25 #Grow of the load
    loss=10 #Discharge losses
    
    if (chem==1):
        DoD_bat=80
        deg=5*eq/1000
    elif(chem==2):
        DoD_bat=80
        deg=5*eq/1000
    elif(chem==3):
        DoD_bat=95 
        deg=2*eq/1000
    elif(chem==4):
        DoD_bat=100 
        deg=0.5*eq/1000
    elif(chem==5):
        DoD_bat=100 
        deg=5*eq/1000
    else:
        print("Option no valid")
    
    F=((1+deg/100)*(1+grow/100))/((1-loss/100)*DoD_bat/100) #Correction factor
    
    #===================================================================
    #Results....this considers just model 1 since it is not possible to know the DoD in each hour for the model 2
    print("\nThe results are:")
    mydata = [
        ["Battery Power [kW]", round(df1.Power.max(),1)*critical/100],
        ["Battery Energy [kWh]",round(df_test.Power.max()*F,1)*critical/100],
        ["Hours [h]",horas]
    ]
    print(tabulate(mydata, tablefmt="grid"))
    
    print('Follow considerations:')
    print('Grow of the load = ', grow,'%')
    print('Discharge losses = ', loss,'%')
    return