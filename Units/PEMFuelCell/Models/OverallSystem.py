import sympy as sp
from pint import UnitRegistry


class OverallSystem:
    """
    This class holds the methods and expressions for the overall system analysis.
    It acts as a container for all relevant methods and provides
    methods to calculate exergy balance equation and energy and exergy efficiencies of the system.
    """

    def __init__(self):
        self.ureg = UnitRegistry()
        self.T0 = 298 * self.ureg.kelvin  # Reference Temperature

        # Define sympy symbols
        self.N1, self.N2, self.N9, self.N_air, self.N14, self.N18 = sp.symbols('N1 N2 N9 N_air N14 N18')
        self.ex1, self.ex2, self.ex9, self.ex_air, self.ex14, self.ex18 = sp.symbols('ex1 ex2 ex9 ex_air ex14 ex18')
        self.W_net, self.Q_stack, self.Q_radiator, self.I_system = sp.symbols('W_net Q_stack Q_radiator I_system')
        self.T_stack, self.T_radiator = sp.symbols('T_stack T_radiator')
        self.h1, self.h9, self.eta_system, self.psi_system = sp.symbols('h1 h9 eta_system psi_system')

        # Define exergy balance equation
        self.exergy_balance_expr = self.N1 * self.ex1 + self.N2 * self.ex2 + self.N9 * self.ex9 - self.N_air * self.ex_air - self.N14 * self.ex14 - self.N18 * self.ex18 - self.W_net - (
                    1 - self.T0 / self.T_stack) * (0.2 * self.Q_stack) - (
                                               1 - self.T0 / self.T_radiator) * self.Q_radiator - self.I_system

        # Define energy and exergy efficiency expressions
        self.energy_efficiency_expr = self.W_net / (self.N1 * self.h1 + self.N9 * self.h9)
        self.exergy_efficiency_expr = self.W_net / (self.N1 * self.ex1 + self.N9 * self.ex9)

        # Lambdify the expressions
        self.exergy_balance_func = sp.lambdify((self.N1, self.ex1, self.N2, self.ex2, self.N9, self.ex9, self.N_air,
                                                self.ex_air, self.N14, self.ex14, self.N18, self.ex18, self.W_net,
                                                self.T_stack, self.Q_stack, self.T_radiator, self.Q_radiator,
                                                self.I_system), self.exergy_balance_expr,
                                               modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        self.energy_efficiency_func = sp.lambdify((self.W_net, self.N1, self.h1, self.N9, self.h9),
                                                  self.energy_efficiency_expr,
                                                  modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        self.exergy_efficiency_func = sp.lambdify((self.W_net, self.N1, self.ex1, self.N9, self.ex9),
                                                  self.exergy_efficiency_expr,
                                                  modules=[{'Quantity': self.ureg.Quantity}, 'math'])

    def compute_exergy_balance(self, **kwargs):
        """
        Compute the exergy balance for the overall system using the provided inputs.

        Args:
        - **kwargs: Values for N1, ex1, N2, ex2, N9, ex9, N_air, ex_air, N14, ex14, N18, ex18, W_net, T_stack, Q_stack, T_radiator, Q_radiator, and I_system.

        Returns:
        - Quantity: Exergy balance for the overall system.
        """
        # Evaluate the lambdified function with provided inputs
        return self.exergy_balance_func(**kwargs)

    def compute_energy_efficiency(self, W_net, N1, h1, N9, h9):
        """
        Compute the energy efficiency of the overall system using the provided inputs.

        Args:
        - W_net (Quantity): Net system power in watts.
        - N1 (float): Molar flow rate at state 1.
        - h1 (Quantity): Specific enthalpy at state 1.
        - N9 (float): Molar flow rate at state 9.
        - h9 (Quantity): Specific enthalpy at state 9.

        Returns:
        - float: Energy efficiency of the overall system.
        """
        # Evaluate the lambdified function with provided inputs
        return self.energy_efficiency_func(W_net, N1, h1, N9, h9)

    def compute_exergy_efficiency(self, W_net, N1, ex1, N9, ex9):
        """
        Compute the exergy efficiency of the overall system using the provided inputs.

        Args:
        - W_net (Quantity): Net system power in watts.
        - N1 (float): Molar flow rate at state 1.
        - ex1 (Quantity): Specific exergy at state 1.
        - N9 (float): Molar flow rate at state 9.
        - ex9 (Quantity): Specific exergy at state 9.

        Returns:
        - float: Exergy efficiency of the overall system.
        """
        # Evaluate the lambdified function with provided inputs
        return self.exergy_efficiency_func(W_net, N1, ex1, N9, ex9)
