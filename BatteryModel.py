#%%
import pandas as pd
from datetime import datetime

#%%
class Battery:
    def __init__(self, type,  pmax, qmax, efficiency, average_dod, degradation_factor):
        self.type = type
        self.pmax = pmax
        self.qmax = qmax
        self.efficiency = efficiency

        self.degradation_factor = degradation_factor
        self.average_dod = average_dod
        self.profile = pd.DataFrame(columns=['P', 'Q', 'SoC', 'DoD', 'SoH']) # a time-series with charge/discharge profile and the associated DOD, SOC, SOH

    def add_data_point(self, timestamp, p, q, soc, dod, soh):
        self.profile.loc[timestamp] = [p, q, soc, dod, soh]
        return self.profile
    
    def get_battery_info(self):
        print("Battery type: ", self.type, "\n")
        print("Battery power: ", self.pmax, "\n")
        print("Battery capacity: ", self.qmax, "\n")
        print("Battery efficiency: ", self.efficiency, "\n" )


    def get_time_series(self):
        return self.profile

if __name__ == "__main__":
    my_battery = Battery(type="NMC",pmax=100, qmax=200, efficiency=0.95, average_dod=0.2, degradation_factor=1)
    my_battery.get_battery_info()

    # Adding data points to the time series with datetime indices and getting the updated DataFrame
    updated_time_series = my_battery.add_data_point(timestamp=datetime(2024, 1, 1, 12, 0, 0), p=50, q=100, soc=0.6, dod=0.4, soh=0.9)
    print("Updated Time Series:")
    print(updated_time_series)

    # Adding another data point and getting the updated DataFrame
    updated_time_series = my_battery.add_data_point(timestamp=datetime(2024, 1, 2, 12, 0, 0), p=75, q=150, soc=0.5, dod=0.5, soh=0.85)
    print("\nUpdated Time Series:")
    print(updated_time_series)



