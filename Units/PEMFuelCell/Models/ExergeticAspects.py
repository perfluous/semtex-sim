import sympy as sp
from pint import UnitRegistry


class ExergeticParameters:
    """
    This class holds the parameters for the Exergetic aspects of a PEM Hydrogen Fuel Cell.
    It acts as a container for all relevant parameters.
    """

    def __init__(self, T0, h, s, h0, s0, xj, mu_j0, mu_j00):
        self.T0 = T0  # Reference Environment Temperature
        self.h = h  # Specific enthalpy at a given state
        self.s = s  # Specific entropy at a given state
        self.h0 = h0  # Specific enthalpy at the reference environment
        self.s0 = s0  # Specific entropy at the reference environment
        self.xj = xj  # Mole fraction of the species j in the flow
        self.mu_j0 = mu_j0  # Chemical potential of species j in the flow evaluated at T0 and P0
        self.mu_j00 = mu_j00  # Chemical potential of species j in the flow evaluated in the reference environment


class ExergeticAspects:
    """
    This class calculates the thermomechanical exergy, chemical exergy, and total exergy
    for a PEM Hydrogen Fuel Cell using the parameters stored in the ExergeticParameters object.
    """

    def __init__(self):
        self.ureg = UnitRegistry()

    def compute_thermomechanical_exergy(self, params: ExergeticParameters):
        """
        Compute the specific thermomechanical exergy using the provided ExergeticParameters object.

        Args:
        - params (ExergeticParameters): Object containing the relevant parameters.

        Returns:
        - Pint Quantity: Specific thermomechanical exergy.
        """
        T0 = params.T0 * self.ureg.K
        h = params.h * self.ureg.J / self.ureg.mol
        s = params.s * self.ureg.J / (self.ureg.mol * self.ureg.K)
        h0 = params.h0 * self.ureg.J / self.ureg.mol
        s0 = params.s0 * self.ureg.J / (self.ureg.mol * self.ureg.K)

        ex_tm_symbolic = (h - h0) - T0 * (s - s0)

        # Lambdify the expression
        ex_tm_func = sp.lambdify((), ex_tm_symbolic, modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        return ex_tm_func()

    def compute_chemical_exergy(self, params: ExergeticParameters):
        """
        Compute the specific chemical exergy on a molar basis using the provided ExergeticParameters object.

        Args:
        - params (ExergeticParameters): Object containing the relevant parameters.

        Returns:
        - Pint Quantity: Specific chemical exergy.
        """
        xj = params.xj
        mu_j0 = params.mu_j0 * self.ureg.J / self.ureg.mol
        mu_j00 = params.mu_j00 * self.ureg.J / self.ureg.mol

        ex_ch_symbolic = xj * (mu_j0 - mu_j00)

        # Lambdify the expression
        ex_ch_func = sp.lambdify((), ex_ch_symbolic, modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        return ex_ch_func()

    def compute_total_exergy(self, params: ExergeticParameters):
        """
        Compute the total exergy which is the sum of thermomechanical and chemical exergies
        using the provided ExergeticParameters object.

        Args:
        - params (ExergeticParameters): Object containing the relevant parameters.

        Returns:
        - Pint Quantity: Total exergy.
        """
        ex_tm = self.compute_thermomechanical_exergy(params)
        ex_ch = self.compute_chemical_exergy(params)

        return (ex_tm + ex_ch).to(self.ureg.J / self.ureg.mol)
