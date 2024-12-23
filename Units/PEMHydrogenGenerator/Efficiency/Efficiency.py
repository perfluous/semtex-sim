import sympy as sp
import simpy
from pint import UnitRegistry
from State.CentralizedState import CentralizedState as H2GeneratorEfficiencyState

class H2GeneratorEfficiencyParameters:
    """
    This class holds the static parameters for the H2 generator's efficiency calculations.
    It acts as a container for all relevant parameters for energy and exergy efficiencies.
    """
    def __init__(self, LHV_H2, Q_heatpEM, Q_heat_H2O, E_H2, E_electric, E_heatpEM, E_heat_H2O):
        self.LHV_H2 = LHV_H2
        self.Q_heatpEM = Q_heatpEM
        self.Q_heat_H2O = Q_heat_H2O
        self.E_H2 = E_H2
        self.E_electric = E_electric
        self.E_heatpEM = E_heatpEM
        self.E_heat_H2O = E_heat_H2O


class H2GeneratorEfficiency:
    """
    This class provides methods to compute energy and exergy efficiencies
    for a hypothetical Hydrogen generator system using the parameters stored in the
    H2GeneratorEfficiencyParameters object and state variables stored in the H2GeneratorEfficiencyState object.
    """
    def __init__(self):
        self.ureg = UnitRegistry()
        self.LHV_H2, self.N_H2_out_dot, self.Q_electric, self.Q_heatpEM, self.Q_heat_H2O, self.E_H2, self.E_electric, self.E_heatpEM, self.E_heat_H2O = sp.symbols(
            'LHV_H2 N_H2_out_dot Q_electric Q_heatpEM Q_heat_H2O E_H2 E_electric E_heatpEM E_heat_H2O'
        )
        self.eta_en_eq = (self.LHV_H2 * self.N_H2_out_dot) / (self.Q_electric + self.Q_heatpEM + self.Q_heat_H2O)
        self.eta_en_func = sp.lambdify(
            (self.LHV_H2, self.N_H2_out_dot, self.Q_electric, self.Q_heatpEM, self.Q_heat_H2O),
            self.eta_en_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math']
        )
        self.eta_ex_eq = (self.E_H2 * self.N_H2_out_dot) / (self.E_electric + self.E_heatpEM + self.E_heat_H2O)
        self.eta_ex_func = sp.lambdify(
            (self.E_H2, self.N_H2_out_dot, self.E_electric, self.E_heatpEM, self.E_heat_H2O),
            self.eta_ex_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math']
        )

    def calculate_eta_en(self, params: H2GeneratorEfficiencyParameters, state: H2GeneratorEfficiencyState):
        return self.eta_en_func(params.LHV_H2, state.N_H2_out_dot, state.Q_electric, params.Q_heatpEM, params.Q_heat_H2O)

    def calculate_eta_ex(self, params: H2GeneratorEfficiencyParameters, state: H2GeneratorEfficiencyState):
        return self.eta_ex_func(params.E_H2, state.N_H2_out_dot, params.E_electric, params.E_heatpEM, params.E_heat_H2O)

    def update(self, params: H2GeneratorEfficiencyParameters, state: H2GeneratorEfficiencyState):
        eta_en = self.calculate_eta_en(params, state)
        eta_ex = self.calculate_eta_ex(params, state)
        return eta_en, eta_ex  # return the computed efficiencies


def efficiency_process(env, params, state, efficiency_calculator, time_step=1):
    while True:
        eta_en = efficiency_calculator.calculate_eta_en(params, state)
        eta_ex = efficiency_calculator.calculate_eta_ex(params, state)
        print(f"At time {env.now}, Energy Efficiency: {eta_en}, Exergy Efficiency: {eta_ex}")
        yield env.timeout(time_step)  # Proceed to the next time step
