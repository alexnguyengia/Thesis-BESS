#%%
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

#%%
class Battery:
#This class is for defining Battery parameters and calculate its time-dependent profile based on the charge/discharge pattern
#type: Battery chemistry such as LTO, LFP, NMC
#pmax: Power capacity of the battery in MW
#qmax: Energy capacity of the battery in MWh
#efficiency: Round-trip efficiency of the battery 
#initialSoC is assumed to be 100% if no value is passed
    iSoC=100
    def __init__(self, type,  pmax, qmax, efficiency, iSoC=100):
        self.type = type         
        self.pmax = pmax         
        self.qmax = qmax
        self.efficiency = efficiency
        self.iSoC = iSoC

        #self.degradation_factor = degradation_factor
        #self.average_dod = average_dod
        
        #SoH to be added later
        self.profile = pd.DataFrame(columns=['P', 'SoC', 'DoD']) # a time-series with charge/discharge profile and the associated DOD, SOC, SOH
        self.DoD_profile=pd.Series()
        self.SoC= iSoC

    def add_profile(self, p_profile, SoC_profile):
        self.profile['P'] = p_profile 
        #self.profile['Q'] 
        self.profile['SoC'] = SoC_profile
        self.profile['DoD'] = my_battery.DoD_calculation(p_profile, SoC_profile)
        #self.profile['SoH']
        return self.profile
    
    def SoH_calculation():
    #Updated SoH after every timestamp.
    #SoH has to take the whole time-series as input
        pass
        

#done, no more changes made
    def SoC_calculation(self, p, time_interval):
        #calculate the Soc at a timestamp from the power and the previous SoC
        self.SoC = self.SoC - (time_interval*p/self.qmax)*100
        #iSoC= self.SoC 
        return self.SoC    
    
#done, no more changes made
    def DoD_calculation(self, p_profile, SoC_profile):
    #Calculate DOD from SOC or P
        for i in p_profile.index:
            self.DoD_profile[i]=(100-SoC_profile[i]) if p_profile[i] >0 else 0
        return self.DoD_profile

    
    def get_battery_info(self):
        print("Battery type: ", self.type, "\n")
        print("Battery power: ", self.pmax, "\n")
        print("Battery capacity: ", self.qmax, "\n")
        print("Battery efficiency: ", self.efficiency, "\n" )


    def get_time_series(self):
        return self.profile
#%%
if __name__ == "__main__":
    my_battery = Battery(type="NMC",pmax=100, qmax=200, efficiency=0.95)
    my_battery.get_battery_info()
#%%
    power_timeseries=pd.Series()
    soc_timeseries=pd.Series()
    index=pd.date_range(start="2020-01-01 00:00:00", end = "2020-01-01 23:45:00", freq = "15min")
    time_interval = index.diff().mean().total_seconds()/3600
#%%
    for i in index:
        if (my_battery.SoC > 0) & (my_battery.SoC<=100) :
            power_timeseries[i]= 0.5*my_battery.pmax
        else:
            power_timeseries[i]=0
            
        soc_timeseries[i]= my_battery.SoC_calculation(power_timeseries[i], time_interval)
        
           
    my_battery.add_profile(power_timeseries, soc_timeseries)


# %%
fig=go.Figure()
fig.add_trace(go.Scatter(y=my_battery.profile['P'], mode='lines', name ='Power'))
fig.add_trace(go.Scatter(y=my_battery.profile['SoC'], mode='lines', name='SoC'))
fig.add_trace(go.Scatter(y=my_battery.profile['DoD'], mode='lines', name ='DoD'))
fig.show()
# %%
