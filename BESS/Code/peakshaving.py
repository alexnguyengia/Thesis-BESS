'''
This Module  is for calculating the model in the case of peak shaving
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

import model 
import lifecycleplotting as lcplot
import degradetime as degrade
import plotting 
import bessresult


def peak_shaving(df1):
    """First case - Peak shaving"""
    #Dataframe of the average values per day:
    dfmean=pd.DataFrame(df1.groupby(pd.Grouper(key='Data', freq='D')).mean()) #to calculate the average value of the power per day
    
    #This explains the recommended values in which it is possible to perform peak shaving
    print('The maximum desired peak power must be between', round(dfmean.Power.max(),1), 'kW and ', round(df1.Power.max(),1), 'kW')
    #Input of the maximum desires power in the new load profile
    Pdes = float(input('Maximum desired peak power[kW]: '))
        
    
    if (dfmean.Power.max()>Pdes):
        #If the user selects a power above the maximum average, then it is plotted the average values per day and it is a warning
        dfmean.Power.plot() 
        print("\nWarning:The desired Power is less than the maximum average\n")
        print("This means the battery cannot charge totally during the charge hours, so there will be hours without shaving.")
    else:
        df2 = pd.DataFrame(df1.loc[df1["Power"] >= Pdes])#this dataframe selects the data higher than the desired power
        df2['Dif']= df2["Power"]-Pdes#to calculate the power of bess (the peak power - the desired power)
        df2 = df2.reset_index(drop=True) #Just to make the calculations easy the index is reset
        df2['Hours']=1 #In this case it is created a column in the dataframe to know how many hours the load power is above the desired maximum power
        
        #Dataframe to calculate the energy, for this it is necesarry to have the sum of the P>Pdes per day so at the end I can have the energy per day required
        df3=pd.DataFrame(df2.groupby(pd.Grouper(key='Data', freq='D')).sum())#to calculate the energy of the bess
        
        Pmax=df2['Dif'].max()#Value of the power of the BESS
        Emax=df3['Dif'].max()#Maximum value of energy in the dataframe (Energy of the BESS without the correction factors)
        
        #======================================================
        #======================================================
        #In the follow code lines, it is performed the calculation of the energy in the battery.
        
        new=[] #new is the list with the values of the new load profile
        E=[Emax] #List with the values of the energy in each moment. I assumed that the battery starts totally charged and ready
        change=[] #List to know when the battery changes the status of discharging to charging
        
        k=[]#List in which I select each power value per hour
        k=df1.Power.tolist()

        for i in range(len(k)):
            if k[i]>Pdes:#Discharge
                if E[i]-(k[i]-Pdes)>=0:
                    E.append(E[i]-(k[i]-Pdes))
                else:
                    E.append(0)
                new.append(k[i]-(E[i]-E[i+1]))
            elif k[i]<Pdes:#Charge
                if (E[i]+Pmax<=Emax) & (Pdes-k[i]>=Pmax):
                    E.append(E[i]+Pmax)
                elif (E[i]+Pdes-k[i]<=Emax) & (Pdes-k[i]<Pmax):
                    E.append(E[i]+Pdes-k[i])
                elif (E[i]+Pmax>Emax) | (E[i]+Pdes-k[i]>Emax):
                    E.append(Emax)
                else:
                    E.append(0)
                new.append(k[i]+E[i+1]-E[i])
            else:
                E.append(E[i])
                new.append(k[i])
                
            if (round(new[i-1]-k[i-1],0)<abs(0))&(round(new[i]-k[i],0)>=abs(0)):
                change.append(1)
            else:
                change.append(0)

        if change[len(k)-1]==1:
                change.append(1)
        else:
            change.append(0)
        
        
        E=E[1:]
        change=change[1:]
        
        #======================================================
        #Dataframe to collect the hourly power in the previous values (without battery) and the new values (with the battery in the system)
        df_peak=pd.DataFrame()
        df_peak["Data"]=df1["Data"]
        df_peak["Power"]=df1["Power"]
        df_peak["E"]= pd.DataFrame(E)
        df_peak["NP"]= np.round(pd.DataFrame(new), decimals=1)
        df_peak["Dif"]=np.round(df_peak.NP-df_peak.Power, decimals = 0) #Negative is disharging and positive is charging
        df_peak["cycles"]=pd.DataFrame(change)#np.sign(df.Dif)
        df_peak["Hours"]=0
        df_peak.loc[df_peak.Dif<0,"Hours"]=1#To know the number of hours of discharging
        df_peak["DoD"]=np.round((Emax-df_peak.E)*100/Emax,decimals=1)
        
        #======================================================
        #To calculate the equivalent cycles with the use of the energy
        eqcycles=(0.5*(pd.DataFrame(df_peak.DoD[1:]).reset_index()-pd.DataFrame(df_peak.DoD[:8758]).reset_index())/100).dropna()
        eq=abs(eqcycles.DoD).cumsum().max()

        #======================================================
        #Dataframe to export the new load profile into excel file
        df_ps_new=pd.DataFrame()
        df_ps_new["Power"]=df_peak["NP"]
        df_ps_new.index=df_peak.Data
        df_ps_new.to_excel('New_Profile_Peak-Shaving.xlsx')

        #=========================================================
        #This is just to be sure that any of the power values in the new load profile are higher than the desired power
        if ((df_peak.NP>Pdes).any()):        
          print("\nWarning: There are values higher than:", Pdes, "kW\n")
        else:
          print("\nThere are no values in the new profile higher than:", Pdes,"kW\n")

        #==========================================================
        #Dataframe to select the data when a cycle (partial or full) is completed
        df6 = pd.DataFrame(df_peak.loc[df_peak["cycles"] == 1]) #Whn a discharge is done it is 1 
        df6 = df6.reset_index(drop=True)
        df6["Days"]=1 #It is one when 
        
        #This is to put all the data related of the DoD in the dataframe above in a list to do some calculations later
        DoD=[]
        DoD=df6.DoD.tolist()
                
        #dataframe of sum per day
        df4=pd.DataFrame(df_peak.groupby(pd.Grouper(key='Data', freq='D')).sum())
        
        dftemp=pd.DataFrame(df4.loc[df4["cycles"] == 1])
        dftemp = dftemp.reset_index()
        df6["Hours"]=dftemp["Hours"]
        
              
        #==========================================================
        #Functions for the calculation of the parameters in both models
        opt= model.model1()        
        bessresult.table_DoD(df6,eq)
        (deg1, year1)=degrade.years(eq, opt)            
        (deg2, year2)=lcplot.cycles(np.mean(df6.DoD), DoD)
        plotting.degradation(deg1, year1, deg2, year2)
        
        #==========================================================
        #Results
              
        bessresult.results(round(df2['Dif'].max(),1), round(df3['Dif'].max(),1), df3.Hours.max(),opt,deg1,year1,deg2,year2)
        plotting.pltload(df_peak,2120,2250,"Peak-Shaving")
        return   