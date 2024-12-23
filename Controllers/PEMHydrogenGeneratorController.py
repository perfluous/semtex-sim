import json
import time
import simpy
from Sensors.MQTTManager import MQTTManager
from Sensors.IoTSensors import (
    TemperatureSensor,
    ElectricChargeSensor,
    CurrentDensitySensor,
    VoltageSensor,
    HydrogenOutputFlowSensor,
    WaterInputFlowSensor,
    ResistanceSensor
)
from State.CentralizedState import CentralizedState
from Units.PEMHydrogenGenerator.Efficiency.Efficiency import H2GeneratorEfficiencyParameters, H2GeneratorEfficiency
from Units.PEMHydrogenGenerator.Efficiency.Exergy import ExergyParameters, ExergyCalculator
from Units.PEMHydrogenGenerator.Efficiency.FlowRates import H2GeneratorFlowRatesParameters, H2GeneratorFlowRates
from Units.PEMHydrogenGenerator.Models.ActivationOverpotential import PEMParameters, ActivationOverpotential
from Units.PEMHydrogenGenerator.Models.Electrochemical import PEMParametersElectrochemical, PEMElectrochemicalModel
from Units.PEMHydrogenGenerator.Models.HeatExergy import PEMHeatExergyParameters, PEMHeatExergyCalculator
from Units.PEMHydrogenGenerator.Models.OhmicOverpotential import PEMParametersOhmic, PEMOhmicOverpotentialModel
from Units.PEMHydrogenGenerator.Thermodynamics.HeatExchangerThermodynamics import HeatExchangerParameters, \
    HeatExchangerThermodynamics

TIME_STEP = 1  # Define the time step as a constant

DEVICE_CONNECTION_STRINGS ={
    "ElectricChargeSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "PressureSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "TempSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "VoltageSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "H2OInFlowSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "ResistanceSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "CurrentDensitySensorDevice": {
        "con_str": "<...>",
        "key": "<...>"},
    "H2OutFlowSensorDevice": {
        "con_str": "<...>",
        "key": "<...>"}
}

class PEMHydrogenGeneratorController:
    def __init__(self, env: simpy.Environment, time_step=TIME_STEP):
        self.env = env
        self.time_step = time_step  # Initialize the time_step

        central_state = CentralizedState(initial_values={
            'T': 300,
            'N_H2_out_dot': 5,
            'Q_electric': 10,
            'J': 10,
            'N_H2O_in': 20,
            'V': 1.5,
            'lambda_a': 20,
            'lambda_c': 10,
            'L': 0.01,
            'alpha': 0.5,
            'eta_act': 0.1,
            'J0': 1e-3,
            'x': 0.001
        })

        # Instantiate MQTTManager
        self.mqtt_manager = MQTTManager()

        # Instantiate Sensor Objects
        self.temperature_sensor = TemperatureSensor(central_state, self.mqtt_manager)
        self.electric_charge_sensor = ElectricChargeSensor(central_state, self.mqtt_manager)
        self.current_density_sensor = CurrentDensitySensor(central_state, self.mqtt_manager)
        self.voltage_sensor = VoltageSensor(central_state, self.mqtt_manager)
        self.hydrogen_output_flow_sensor = HydrogenOutputFlowSensor(central_state, self.mqtt_manager)
        self.water_input_flow_sensor = WaterInputFlowSensor(central_state, self.mqtt_manager)
        self.resistance_sensor = ResistanceSensor(central_state, self.mqtt_manager)



        # Define shared parameters
        SHARED_F = 96500
        SHARED_T = 300
        SHARED_R = 8.314

        # Initialize each component with shared or specific parameters
        self.efficiency_params = H2GeneratorEfficiencyParameters(LHV_H2=120, Q_heatpEM=10, Q_heat_H2O=10,
                                                                 E_H2=10, E_electric=10, E_heatpEM=10, E_heat_H2O=10)
        self.efficiency_state = central_state
        self.efficiency_calculator = H2GeneratorEfficiency()

        exergy_params = ExergyParameters(E_chem=100, E_phy=50, H=200, S=1, T0=273.15, S0=0.8)
        self.exergy_calculator = ExergyCalculator(self.env, exergy_params, central_state, time_step)

        flow_rates_params = H2GeneratorFlowRatesParameters(F=SHARED_F)
        self.flow_rates_generator = H2GeneratorFlowRates(flow_rates_params, central_state)

        self.activation_params = PEMParameters(R=SHARED_R, T=SHARED_T, F=SHARED_F, J_ref_a=0.1, J_ref_c=0.1,
                                               E_act_a=80000,
                                               E_act_c=80000)
        self.activation_overpotential = ActivationOverpotential()

        electrochemical_params = PEMParametersElectrochemical(V0=1.23, eta_act_a=0.1, eta_act_c=0.1, eta_ohm=0.1,
                                                              area=1.0)
        self.electrochemical_model = PEMElectrochemicalModel()

        self.heat_exergy_params = PEMHeatExergyParameters(F=SHARED_F, eta_act_a=0.1, eta_act_c=0.1, eta_ohm=0.1,
                                                          Delta_S=10, T0=SHARED_T)
        self.heat_exergy_calculator = PEMHeatExergyCalculator()

        ohmic_params = PEMParametersOhmic(T=SHARED_T, z=2, F=SHARED_F, R=SHARED_R)
        self.ohmic_model = PEMOhmicOverpotentialModel()

        heat_exchanger_params = HeatExchangerParameters(Q_max=100, F=SHARED_F, H_H2O_T=3000, H_H2O_T0=2000, T0=SHARED_T,
                                                        T_source=400, epsilon=0.8)
        self.heat_exchanger = HeatExchangerThermodynamics(self.env, heat_exchanger_params, central_state, time_step)

        self.received_energy_mj = 0

    def process(self):
        while True:
            # Update each component at every time step
            eta_act_a, eta_act_c, J_0_a, J_0_c = self.activation_overpotential.update(self.activation_params,
                                                                                      self.efficiency_state)
            entropy_gen, q_heat_pem, e_heat_pem = self.heat_exergy_calculator.update(self.heat_exergy_params,
                                                                                     self.efficiency_state)

            self.exergy_calculator.update()
            eta_en, eta_ex = self.efficiency_calculator.update(self.efficiency_params, self.efficiency_state)
            Q, Q_theoretical, E_heat_H2O = self.heat_exchanger.update()

            # Update and publish flow rates
            try:
                N_H2_out, N_O2_out, N_H2O_out = self.flow_rates_generator.update()
                flow_data = {
                    "N_H2_out": N_H2_out,
                    "N_O2_out": N_O2_out,
                    "N_H2O_out": N_H2O_out
                }
                print(flow_data)
                # flow_value_json = json.dumps(flow_data)
                # self.mqtt_client.publish("H2PEMHydrogenGenerator/FlowRates", flow_value_json)
                self.log_status(eta_act_a, eta_act_c, J_0_a, J_0_c, entropy_gen, q_heat_pem, e_heat_pem, eta_en, eta_ex,
                                Q, Q_theoretical, E_heat_H2O, N_H2_out, N_O2_out, N_H2O_out)
            except Exception as e:
                print(f"Error updating and publishing flow rates: {e}")

            # Use Sensor Objects
            self.temperature_sensor.read_and_publish()
            self.electric_charge_sensor.read_and_publish()
            self.current_density_sensor.read_and_publish()
            self.voltage_sensor.read_and_publish()
            self.hydrogen_output_flow_sensor.read_and_publish()
            self.water_input_flow_sensor.read_and_publish()
            self.resistance_sensor.read_and_publish()
            # self.pressure_sensor.read_and_publish()

            time.sleep(self.time_step)  # introduce a real-time delay
            yield self.env.timeout(self.time_step)

    def log_status(self, eta_act_a, eta_act_c, J_0_a, J_0_c, entropy_gen, q_heat_pem, e_heat_pem, eta_en, eta_ex, Q,
                   Q_theoretical, E_heat_H2O, N_H2_out, N_O2_out, N_H2O_out):
        # Centralized logging method
        print(
            f"Time: {self.env.now}, Activation Overpotential at Anode: {eta_act_a}, Activation Overpotential at Cathode: {eta_act_c}")
        print(
            f"Time: {self.env.now}, Exchange Current Density at Anode: {J_0_a}, Exchange Current Density at Cathode: {J_0_c}")
        print(f"Entropy Generation: {entropy_gen}, Q Heat PEM: {q_heat_pem}, E Heat PEM: {e_heat_pem}")
        print(f"At time {self.env.now}, Energy Efficiency: {eta_en}, Exergy Efficiency: {eta_ex}")
        print(f"Time: {self.env.now}, Q: {Q}, Q_theoretical: {Q_theoretical}, E_heat_H2O: {E_heat_H2O}")
        print(
            f"Time: {self.env.now}, Updated N_H2_out: {N_H2_out}, Updated N_O2_out: {N_O2_out}, Updated N_H2O_out: {N_H2O_out}")

    def receive_energy(self, energy_mj):
        # TODO: Implement the logic or remove if not needed
        pass


if __name__ == "__main__":
    env = simpy.Environment()
    pem_hydrogen_generator_controller = PEMHydrogenGeneratorController(env, time_step=TIME_STEP)
    env.process(pem_hydrogen_generator_controller.process())
    env.run(until=10)  # Run for 10 hours as an example