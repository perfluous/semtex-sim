import sympy as sp
from pint import UnitRegistry
import simpy
from State.CentralizedState import CentralizedState as H2GeneratorFlowRatesState


# Parameters Class
class H2GeneratorFlowRatesParameters:
    """
    This class holds the parameters for calculating flow rates in the PEM electrolyzer.
    It acts as a container for all relevant parameters.
    """

    def __init__(self, F):
        self.F = F  # Faraday constant


# Main Calculation Class
class H2GeneratorFlowRates:
    """
    This class calculates flow rates associated with a PEM electrolyzer system using the parameters
    stored in the H2GeneratorFlowRatesParameters object and state in the H2GeneratorFlowRatesState object.
    """

    def __init__(self, params: H2GeneratorFlowRatesParameters, state: H2GeneratorFlowRatesState):
        self.ureg = UnitRegistry()
        self.params = params
        self.state = state

    def compute_N_H2_out(self):
        N_H2_out_eq = self.state.J / (2 * self.params.F)
        return N_H2_out_eq * self.ureg.mol / self.ureg.s

    def compute_N_O2_out(self):
        N_O2_out_eq = self.state.J / (4 * self.params.F)
        return N_O2_out_eq * self.ureg.mol / self.ureg.s

    def compute_N_H2O_out(self):
        N_H2O_out_eq = self.state.N_H2O_in - self.state.J / (2 * self.params.F)
        return N_H2O_out_eq * self.ureg.mol / self.ureg.s

    def update(self):
        # Compute the flow rates using the current state value of J
        N_H2_out = self.compute_N_H2_out()
        N_O2_out = self.compute_N_O2_out()
        N_H2O_out = self.compute_N_H2O_out()

        # return the computed values if needed in the controller
        return N_H2_out, N_O2_out, N_H2O_out
