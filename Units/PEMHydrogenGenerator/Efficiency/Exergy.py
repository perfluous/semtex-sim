import sympy as sp
import simpy
from pint import UnitRegistry
from State.CentralizedState import CentralizedState as ExergyState

class ExergyParameters:
    def __init__(self, E_chem, E_phy, H, S, T0, S0):
        self.E_chem = E_chem  # Chemical exergy
        self.E_phy = E_phy  # Physical exergy
        self.H = H  # Enthalpy
        self.S = S  # Entropy
        self.T0 = T0  # Reference temperature
        self.S0 = S0  # Reference entropy


class ExergyCalculator:
    def __init__(self, env, params: ExergyParameters,  state: ExergyState, time_step):
        self.ureg = UnitRegistry()
        self.env = env
        self.params = params
        self.state = state
        self.time_step = time_step  # Time step for the simulation

        # Define symbolic variables
        self.E_chem, self.E_phy, self.H, self.S, self.T, self.T0, self.S0 = sp.symbols('E_chem E_phy H S T T0 S0')

        # Define symbolic equations for total exergy
        self.E_phy_eq = self.E_phy * (self.T * (self.S - self.S0))
        self.E_total_eq = self.E_chem + self.E_phy_eq

        # Convert symbolic equations into callable functions
        self.E_total_func = sp.lambdify((self.E_chem, self.E_phy, self.H, self.S, self.T, self.T0, self.S0),
                                        self.E_total_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math'])

    def update(self):
        E_total = self.compute_total_exergy()
        print(f"Time: {self.env.now}, Temperature: {self.state.T}, Total Exergy: {E_total}")

    def compute_total_exergy(self):
        E_total = self.E_total_func(
            self.params.E_chem, self.params.E_phy, self.params.H, self.params.S,
            self.state.T, self.params.T0, self.params.S0
        )
        # Assuming E_total is a float. If E_total is supposed to be a Pint Quantity,
        # then there might be an issue with the way it is being calculated.
        return E_total * self.ureg.J / self.ureg.mol  # Convert the float to a pint quantity
