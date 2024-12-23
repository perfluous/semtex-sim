import simpy
import pandas as pd
import logging
import os


from Units.PEMHydrogenGenerator.Models.OhmicOverpotential import PEMParametersOhmic, PEMStateOhmic, PEMOhmicOverpotentialModel  # Adjust the import path accordingly
from Controllers.PEMHydrogenGeneratorController import PEMHydrogenGeneratorController
# noinspection PyInterpreter
from Units.Batteries.Model.TeslaMegapack import TeslaMegapack
from Units.SolarFarmAndHouses.SolarFarmHouses import SolarFarm, Houses


def mj_to_mwh(energy_mj):
    return energy_mj * 0.000277778


class Controller:
    def __init__(self, env, battery, solar_farm, houses, pem_hydrogen_generator_controller, pem_ohmic_model, pem_ohmic_params, pem_ohmic_state):
        self.env = env
        self.battery = battery
        self.solar_farm = solar_farm
        self.houses = houses
        self.pem_hydrogen_generator_controller = pem_hydrogen_generator_controller
        self.pem_ohmic_model = pem_ohmic_model
        self.pem_ohmic_par  ams = pem_ohmic_params
        self.pem_ohmic_state = pem_ohmic_state
        self.process_ref = env.process(self.process())

    def process(self):
        while True:
            try:
                # Get the energy supplied and demanded for the current hour
                energy_supplied = self.solar_farm.energy_data.iloc[self.solar_farm.current_hour]['Energy Supplied (MJ)']
                energy_demand = self.houses.demand_data.iloc[self.houses.current_hour]['Energy Demand (MJ)']

                # Convert energy to MWh for operations
                energy_supplied_mwh = mj_to_mwh(energy_supplied)
                energy_demand_mwh = mj_to_mwh(energy_demand)

                # Here, SolarFarm directly supplies energy to PEMHydrogenGeneratorController
                self.pem_hydrogen_generator_controller.receive_energy(energy_supplied_mwh)

                # Calculate energy deficit or surplus
                energy_deficit_mwh = max(0, energy_demand_mwh - energy_supplied_mwh)
                energy_surplus_mwh = max(0, energy_supplied_mwh - energy_demand_mwh)

                # Charge or discharge the battery as needed
                if energy_deficit_mwh > 0:
                    self.battery.discharge(energy_deficit_mwh)
                elif energy_surplus_mwh > 0:
                    self.battery.charge(energy_surplus_mwh)

                # Update PEM Ohmic Model State
                self.pem_ohmic_model.update(self.pem_ohmic_params, self.pem_ohmic_state)

                # Log PEM Ohmic Model State
                sigma = self.pem_ohmic_model.calculate_sigma(self.pem_ohmic_state.lambda_x, self.pem_ohmic_params)
                lambda_x = self.pem_ohmic_state.lambda_x
                eta_ohm = self.pem_ohmic_model.calculate_eta_ohm(self.pem_ohmic_state)
                J_act = self.pem_ohmic_model.calculate_J_act(self.pem_ohmic_state, self.pem_ohmic_params)
                logging.info(f"sigma: {sigma}, lambda_x: {lambda_x}, eta_ohm: {eta_ohm}, J_act: {J_act}")

                logging.info(
                    f"At {self.env.now}, Energy Supplied: {energy_supplied_mwh} MWh, Energy Demand: {energy_demand_mwh} MWh, Battery Stored Energy: {self.battery.get_stored_energy()} MWh")

            except Exception as e:
                logging.error(f"Error in Controller process: {e}")

            yield self.env.timeout(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    env = simpy.Environment()

    # Initialize the components
    houses_file_path = os.getenv('HOUSES_FILE_PATH', 'sim/SimulationData/energy_demand_3200_houses.csv')
    solar_farm_file_path = os.getenv('SOLAR_FARM_FILE_PATH', 'sim/SimulationData/hourly_solar_energy_production.csv')

    houses = Houses(env, houses_file_path)
    solar_farm = SolarFarm(env, solar_farm_file_path)
    battery = TeslaMegapack(env, capacity_mwh=4.32, max_charge_rate_mw=1, max_discharge_rate_mw=1)

    # Initialize the PEMHydrogenGeneratorController and related components
    pem_hydrogen_generator_controller = PEMHydrogenGeneratorController(env)  # Assuming you have properly initialized it

    # Initialize the PEM Ohmic Overpotential Model
    pem_ohmic_model = PEMOhmicOverpotentialModel()
    pem_ohmic_params = PEMParametersOhmic(T=300, z=2, F=96500, R=8.314)
    pem_ohmic_state = PEMStateOhmic(lambda_a=20, lambda_c=10, L=0.01, J=0.1, alpha=0.5, eta_act=0.1, J0=1e-3)

    # Register the processes of the solar farm, the houses
    env.process(solar_farm.process())
    env.process(houses.process())

    # Initialize and run the main controller
    controller = Controller(env, battery, solar_farm, houses, pem_hydrogen_generator_controller, pem_ohmic_model, pem_ohmic_params, pem_ohmic_state)
    env.run(until=24)
