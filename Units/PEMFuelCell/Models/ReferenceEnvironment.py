import sympy as sp
from pint import UnitRegistry


class ReferenceEnvironment:
    """
    This class holds the parameters for the reference environment in the exergy analysis.
    It acts as a container for all relevant parameters related to the restricted and unrestricted dead states.
    """

    def __init__(self, T0, P0, components):
        self.T0 = T0  # Reference Temperature (298 K)
        self.P0 = P0  # Reference Pressure (1 atm)
        self.components = components  # Components of the reference environment with mole fractions and chemical exergy

    def get_restricted_state(self):
        """
        Returns the restricted dead state conditions, i.e., Temperature and Pressure.

        Returns:
        - tuple: (Temperature, Pressure) of the restricted dead state.
        """
        return self.T0, self.P0

    def get_unrestricted_state(self):
        """
        Returns the unrestricted dead state conditions, i.e., Composition of the reference environment.

        Returns:
        - dict: Composition of the reference environment with mole fractions and chemical exergy.
        """
        return self.components


# Define the components of the reference environment
components = {
    'N2': {'mole_fraction': 0.775, 'chemical_exergy': 631.51},
    'O2': {'mole_fraction': 0.206, 'chemical_exergy': 3914.26},
    'H2O': {'mole_fraction': 0.018, 'chemical_exergy': 9953.35},
    'CO2': {'mole_fraction': 0.0003, 'chemical_exergy': 20108.5},
    'Ar': {'mole_fraction': 0.0007, 'chemical_exergy': 17998.14}
}

# Create an object of the ReferenceEnvironment class
ureg = UnitRegistry()
ref_env = ReferenceEnvironment(T0=298 * ureg.K, P0=1 * ureg.atm, components=components)

# Use the object to get the restricted and unrestricted states
restricted_state = ref_env.get_restricted_state()
unrestricted_state = ref_env.get_unrestricted_state()
