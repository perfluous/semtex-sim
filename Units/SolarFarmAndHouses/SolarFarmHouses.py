import simpy
import pandas as pd


class SolarFarm:
    def __init__(self, env, file_path):
        self.env = env
        self.energy_data = pd.read_csv(file_path, parse_dates=['Datetime'])
        self.current_hour = 0

    def process(self):
        while True:
            # Get the energy supplied for the current hour
            energy_supplied = self.energy_data.iloc[self.current_hour]['Energy Supplied (MJ)']
            print(f"Hour: {self.current_hour}, Energy Supplied by Solar Farm: {energy_supplied} MJ")
            # Go to the next hour
            self.current_hour += 1
            if self.current_hour >= len(self.energy_data):
                self.current_hour = 0  # Reset to the first hour after a year
            # Process runs every hour
            yield self.env.timeout(1)


class Houses:
    def __init__(self, env, file_path):
        self.env = env
        self.demand_data = pd.read_csv(file_path, parse_dates=['Datetime'])
        self.current_hour = 0

    def process(self):
        while True:
            # Get the energy demand for the current hour
            energy_demand = self.demand_data.iloc[self.current_hour]['Energy Demand (MJ)']
            print(f"Hour: {self.current_hour}, Energy Demand by 3200 Houses: {energy_demand} MJ")
            # Go to the next hour
            self.current_hour += 1
            if self.current_hour >= len(self.demand_data):
                self.current_hour = 0  # Reset to the first hour after a year
            # Process runs every hour
            yield self.env.timeout(1)


# # Initialize SimPy environment
# env = simpy.Environment()
#
# # Initialize Solar Farm and 3200 Houses
# houses_demand_file_path = '/SimulationData/energy_demand_3200_houses.csv'
# solar_farm_file_path = '/SimulationData/hourly_solar_energy_production.csv'
#
# solar_farm = SolarFarm(env, solar_farm_file_path)
# houses = Houses(env, houses_demand_file_path)
#
# # Add the processes to the environment
# env.process(solar_farm.process())
# env.process(houses.process())
#
# # Run the simulation for 24 hours as an example
# env.run(until=24)
