import sympy as sp
from pint import UnitRegistry


class PEMFuelCellAssumptions:
    """
    This class holds the assumptions for the PEM fuel cell analysis.
    It acts as a container for all relevant assumptions and provides
    methods to calculate net system power and exergy balance based on these assumptions.
    """

    def __init__(self):
        self.ureg = UnitRegistry()
        self.H2_pressure = 10 * self.ureg.bar
        self.H2_temperature = 298 * self.ureg.kelvin
        self.compressor_efficiency = 0.7
        self.cooling_pump_efficiency = 0.7
        self.radiator_fan_efficiency = 0.7
        self.heat_loss_fraction = 0.2
        self.environmental_state = {'P': 1 * self.ureg.atm, 'T': 298 * self.ureg.kelvin}
        self.dead_state = {'N2': 0.775, 'O2': 0.206, 'H2O': 0.018, 'CO2': 0.0003, 'Ar': 0.0007}

        # Define sympy symbols
        self.W_stack_symbol, self.W_ac_symbol, self.W_cp_symbol, self.W_rf_symbol = sp.symbols('W_stack W_ac W_cp W_rf')

        # Define net system power expression
        self.W_net_expr = self.W_stack_symbol - self.W_ac_symbol - self.W_cp_symbol - self.W_rf_symbol

        # Lambdify the expression
        self.W_net_func = sp.lambdify((self.W_stack_symbol, self.W_ac_symbol, self.W_cp_symbol, self.W_rf_symbol),
                                      self.W_net_expr,
                                      modules=[{'Quantity': self.ureg.Quantity}, 'math'])

    def net_system_power(self, W_stack, W_ac, W_cp, W_rf):
        """
        Calculate the net system power produced by the fuel cell power system.

        Args:
        - W_stack (Quantity): Stack power in watts.
        - W_ac (Quantity): Power input to air compressor in watts.
        - W_cp (Quantity): Power input to cooling pump in watts.
        - W_rf (Quantity): Power input to radiator fan in watts.

        Returns:
        - Quantity: Net system power in watts.
        """
        # Evaluate the lambdified function with provided inputs
        return self.W_net_func(W_stack, W_ac, W_cp, W_rf)
