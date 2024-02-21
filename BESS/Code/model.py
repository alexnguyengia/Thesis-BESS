'''
This module comprises of 2 functions: 
model1()
years()
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
#model 1: this is the function to select the desired chemistry of the battery. The output is the option selected by the user.
def model1():
    print("\n====================================================")
    print("   Which is the chemistry desired of the battery")
    print("=======================================================")
    print('1. Lithium NMC\n2. Lithium LFP\n3. Lithium LTO\n4. Vanadium\n5. NaS\n')
    print('Select an option:')
    opt=int(input(''))
    return (opt)

'''
______________________________________________________________________________________________________________________________
______________________________________________________________________________________________________________________________

'''
#years: According to the chemistry selected for the battery this calculates the degradation and the years of life with the model 1. The inputs are the equivalent cycles and the option selected in model 1. 
def years(cycles, opt):
    print("=====================================")
    print("   Model 1")
    print("=====================================")
    
    print('Equivalent full cycles:', round(cycles,1))
    if (opt==1):
        print('\nBattery Chemistry: Lithium NMC\nCycles: 4000, DoD=80%, Degradation:5% per 1000 cycles, Calendar life: 10 years')
        year1=4000/cycles
        deg=5*cycles/1000 #this is the degradation per year
        year2=(100-80)/deg
        year=min(year1,year2)
        print('Years:', round(year,1))
        print('Degradation:',round(deg,3),'%per year')
        print('The capacity available of the battery at the end of the first year is:',round(100*(1-5/100*cycles/1000),1),'%\n')
    elif(opt==2):
        print('\nBattery Chemistry: Lithium LFP\nCycles: 6000, DoD=80%, Degradation:5% per 1000 cycles, Calendar life: 10 years')
        year1=6000/cycles
        deg=5*cycles/1000 #this is the degradation per year
        year2=(100-80)/deg
        year=min(year1,year2)
        print('Years:', round(year,1))
        print('Degradation:',round(deg,3),'%per year')
        print('The capacity available of the battery at the end of the first year is:',round(100*(1-5/100*cycles/1000),1),'%\n')
    elif(opt==3):
        print('\nBattery Chemistry: Lithium LTO\nCycles: 10000, DoD=95%, Degradation:2% per 1000 cycles, Calendar life: 25 years')
        year1=10000/cycles
        deg=2*cycles/1000 #this is the degradation per year
        year2=(100-80)/deg
        year=min(year1,year2)
        print('Years:', round(year,1))
        print('Degradation:',round(deg,3),'%per year')
        print('The capacity available of the battery at the end of the first year is:',round(100*(1-2/100*cycles/1000),1),'%\n')
    elif(opt==4):
        print('\nBattery Chemistry: Vanadium\nCycles: 20000, DoD=100%, Degradation:0.5% per 1000 cycles, Calendar life: 20 years')
        year1=20000/cycles
        deg=0.5*cycles/1000 #this is the degradation per year
        year2=(100-90)/deg
        year=min(year1,year2)
        print('Years:', round(year,1))
        print('Degradation:',round(deg,3),'%per year')
        print('The capacity available of the battery at the end of the first year is:',round(100*(1-0.5/100*cycles/1000),1),'%\n')
    elif(opt==5):
        print('\nBattery Chemistry: NaS\nCycles: 7300, DoD=100%, Degradation:5% per 1000 cycles, Calendar life: 20 years')
        year1=10000/cycles
        deg=5*cycles/1000 #this is the degradation per year
        year2=(100-63.5)/deg
        year=min(year1,year2)
        print('Years:', round(year,1))  
        print('Degradation:',round(deg,3),'%per year')
        print('The capacity available of the battery at the end of the first year is:',round(100*(1-5/100*cycles/1000),1),'%\n')
    else:
        print("Option no valid")
    return (deg, round(year,1))