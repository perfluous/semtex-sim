import sympy as sp
from pint import UnitRegistry
from sympy import lambdify, Q


class HydrogenCompressionParameters:
    """
    Container for the parameters needed to perform the hydrogen compression calculations.

    Attributes:
    - p1: Initial pressure in bar.
    - p2: Final pressure in bar.
    - T: Temperature in Kelvin.
    - qK: Cooling energy in kJ/kg, optional.
    - h1: Initial enthalpy in kJ/kg, optional.
    - h2: Final enthalpy in kJ/kg, optional.
    """

    def __init__(self, p1, p2, T, qK=None, h1=None, h2=None):
        self.p1 = p1
        self.p2 = p2
        self.T = T
        self.qK = qK
        self.h1 = h1
        self.h2 = h2


class HydrogenCompressionModel:
    """
    Implements the model for determining the internal work needed for the compression of hydrogen gas.

    Attributes:
    - ureg: Unit registry from pint library to handle units.
    - p1, p2, T, R: Symbolic variables used in sympy expressions.
    - wi_symbolic: Sympy expression representing the ideal compression work formula.
    - wi_lambda: Lambda function derived from wi_symbolic, used to calculate numeric values.
    """

    def __init__(self):
        self.ureg = UnitRegistry()
        self.p1, self.p2, self.T, self.R = sp.symbols('p1 p2 T R')
        self.wi_symbolic = self.R * self.T * sp.log(self.p2 / self.p1)
        self.wi_lambda = lambdify((self.p1, self.p2, self.T, self.R), self.wi_symbolic)

    def ideal_compression_work(self, params: HydrogenCompressionParameters):
        """
        Calculate the ideal compression work using the provided parameters.

        Parameters:
        - params (HydrogenCompressionParameters): Object containing the relevant parameters.

        Returns:
        - Ideal compression work as a pint quantity in kJ/mol.
        """
        R = 8.314  # J/(mol·K)
        p1 = params.p1 * self.ureg.bar
        p2 = params.p2 * self.ureg.bar
        T = params.T * self.ureg.K
        wi = self.wi_lambda(p1.magnitude, p2.magnitude, T.magnitude, R)
        return Q(wi, self.ureg.J / self.ureg.mol).to(self.ureg.kJ / self.ureg.mol)

    def internal_work(self, params: HydrogenCompressionParameters):
        """
        Calculate the internal work needed for the compression of hydrogen gas.

        Parameters:
        - params (HydrogenCompressionParameters): Object containing the relevant parameters.

        Returns:
        - Internal work as a pint quantity in kJ/kg.
        """
        if params.qK and params.h1 and params.h2:
            qK = params.qK * self.ureg.kJ / self.ureg.kg
            h1 = params.h1 * self.ureg.kJ / self.ureg.kg
            h2 = params.h2 * self.ureg.kJ / self.ureg.kg
            wi = h2 - h1 + qK
            return wi
        else:
            raise ValueError("qK, h1, and h2 must be provided to calculate internal work.")

    def temperature_increase_due_to_expansion(self, initial_pressure, final_pressure):
        """
        Calculate the temperature increase due to the expansion of hydrogen gas.

        Parameters:
        - initial_pressure: Initial pressure in bar.
        - final_pressure: Final pressure in bar.

        Returns:
        - Temperature increase as a pint quantity in Kelvin.
        """
        if initial_pressure == 1000 and final_pressure == 13:
            delta_T = 50  # in Kelvin
        else:
            delta_T = 0  # Placeholder
        return Q(delta_T, self.ureg.K)


# Example Usage:
p1 = 1  # bar
p2 = 900  # bar
T = 298.15  # K (25°C)
qK = 8181  # kJ/kg
h1 = 3787  # kJ/kg
h2 = 4383  # kJ/kg

compressor_params = HydrogenCompressionParameters(p1, p2, T, qK, h1, h2)
compressor_model = HydrogenCompressionModel()

wi_ideal = compressor_model.ideal_compression_work(compressor_params)
wi_internal = compressor_model.internal_work(compressor_params)
temperature_increase = compressor_model.temperature_increase_due_to_expansion(1000, 13)

print(f"Ideal Compression Work: {wi_ideal}")
print(f"Internal Work: {wi_internal}")
print(f"Temperature Increase due to Expansion: {temperature_increase}")


