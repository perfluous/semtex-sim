import sympy as sp
from pint import UnitRegistry


class PEMFuelCellPerformance:
    """
    This class represents the PEM fuel cell performance model developed by Baschuk and Li.
    It includes methods to calculate the reversible cell voltage, irreversible cell voltage loss,
    activation overpotential, ohmic overpotential, concentration overpotential, and stack power.
    """

    def __init__(self, T, C_H2, C_O2, I, A_cell, n_fc):
        self.ureg = UnitRegistry()
        self.T = T * self.ureg.kelvin  # Temperature
        self.C_H2 = C_H2 * (self.ureg.mol / self.ureg.L)  # Concentration of H2
        self.C_O2 = C_O2 * (self.ureg.mol / self.ureg.L)  # Concentration of O2
        self.I = I * (self.ureg.ampere / self.ureg.square_cm)  # Current density
        self.A_cell = A_cell * self.ureg.square_cm  # Geometric area of the cell
        self.n_fc = n_fc  # Number of fuel cells in the stack

    def reversible_cell_voltage(self):
        """
        Calculate the reversible cell voltage (Er) at the specified operating conditions.

        Returns:
        - Quantity: Reversible cell voltage in volts.
        """
        Er_symbolic = sp.Symbol('Er')
        Er_eq = sp.Eq(Er_symbolic, 1.299 + 0.85e-3 * (self.T - 295.15) + 4.31e-5 * self.T * sp.log(
            (self.C_H2 / 22.22) * (self.C_O2 / 7.033) ** 0.5))
        Er_func = sp.lambdify((), Er_eq.rhs, modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        return Er_func()

    def irreversible_cell_voltage_loss(self, eta_act, eta_ohmic, eta_con):
        """
        Calculate the irreversible cell voltage loss or overpotential (Eirr).

        Args:
        - eta_act (Quantity): Activation overpotential in volts.
        - eta_ohmic (Quantity): Ohmic overpotential in volts.
        - eta_con (Quantity): Concentration overpotential in volts.

        Returns:
        - Quantity: Irreversible cell voltage loss in volts.
        """
        Eirr = eta_act + eta_ohmic + eta_con
        return Eirr

    def stack_power(self):
        """
        Calculate the power produced by the entire stack (Ẇstack) at the specified operating conditions.

        Returns:
        - Quantity: Stack power in watts.
        """
        E = self.reversible_cell_voltage() - self.irreversible_cell_voltage_loss()  # Placeholder, replace with actual values
        W_cell = E * self.I * self.A_cell
        W_stack = self.n_fc * W_cell
        return W_stack.to(self.ureg.watt)
