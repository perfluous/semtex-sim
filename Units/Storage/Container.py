import unittest
import logging
import sympy as sp
from scipy.integrate import solve_ivp
from pint import UnitRegistry

# Set up logging
logging.basicConfig(filename='hydrogen_container_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
class HydrogenContainerParameters:
    def __init__(self, V, T, n, a, b, inflow_rate, outflow_rate, heat_exchange_rate):
        self.V = V  # Volume of the container
        self.T = T  # Initial temperature of the hydrogen gas
        self.n = n  # Initial number of moles of hydrogen gas
        self.a = a  # Van der Waals parameter for hydrogen
        self.b = b  # Van der Waals parameter for hydrogen
        self.inflow_rate = inflow_rate  # Rate of inflow of hydrogen gas in moles per second
        self.outflow_rate = outflow_rate  # Rate of outflow of hydrogen gas in moles per second
        self.heat_exchange_rate = heat_exchange_rate  # Rate of heat exchange with the surroundings in Joules per second

class HydrogenContainerModel:
    def __init__(self):
        self.ureg = UnitRegistry()
        self.R = 8.314 * self.ureg.J / (self.ureg.mol * self.ureg.K)  # Ideal Gas Constant

    def van_der_waals_equation(self, params: HydrogenContainerParameters):
        """
        Apply the Van der Waals equation to calculate pressure.

        Parameters:
        - params (HydrogenContainerParameters): Object containing the relevant parameters.

        Returns:
        - Pressure as a pint quantity.

        Raises:
        - ValueError: If the effective volume (V - n*b) is non-positive.
        - TypeError: If the parameters are not of the correct type or unit.
        """
        try:
            try:
                V = params.V * self.ureg.m ** 3
                T = params.T * self.ureg.K
                n = params.n * self.ureg.mol
                a = params.a * self.ureg.Pa * (self.ureg.m ** 6) / (self.ureg.mol ** 2)
                b = params.b * self.ureg.m ** 3 / self.ureg.mol
            except AttributeError as e:
                raise TypeError("Parameters are missing or not convertible to the expected units.") from e

            V_eff = V - n * b
            if V_eff <= 0 * self.ureg.m ** 3:
                raise ValueError("Non-positive effective volume encountered in Van der Waals equation.")

            try:
                P = ((n * self.R * T) / V_eff - a * (n / V) ** 2).to(self.ureg.Pa)
            except ZeroDivisionError as e:
                raise ValueError("Division by zero encountered in pressure calculation.") from e
        except ValueError:
            logging.error(f"ValueError encountered in van_der_waals_equation with parameters: "
                          f"V={params.V}, T={params.T}, n={params.n}, a={params.a}, b={params.b}")
            raise
        return P

    def dynamic_simulation(self, params: HydrogenContainerParameters, t_span, y0):
        """
        Perform a dynamic simulation considering inflow, outflow, and heat exchange.

        Parameters:
        - params (HydrogenContainerParameters): Object containing the relevant parameters.
        - t_span (tuple): The time span of simulation as (t_start, t_end).
        - y0 (list): Initial conditions as [initial_moles, initial_temperature].

        Returns:
        - The result of the dynamic simulation.

        Raises:
        - ValueError: If the initial conditions are not valid.
        - TypeError: If the parameters are not of the correct type or unit.
        """
        if not isinstance(t_span, tuple) or not all(isinstance(i, (int, float)) for i in t_span):
            raise TypeError("t_span must be a tuple of numbers (t_start, t_end).")

        if not isinstance(y0, list) or not all(isinstance(i, (int, float)) for i in y0):
            raise TypeError("y0 must be a list of initial conditions [initial_moles, initial_temperature].")

        if any(i <= 0 for i in y0):
            raise ValueError("Initial conditions in y0 must be positive.")

        def dydt(t, y):
            try:
                n = y[0] * self.ureg.mol
                T = y[1] * self.ureg.K
                inflow_rate = params.inflow_rate * self.ureg.mol / self.ureg.s
                outflow_rate = params.outflow_rate * self.ureg.mol / self.ureg.s
                heat_exchange_rate = params.heat_exchange_rate * self.ureg.J / self.ureg.s
                V = params.V * self.ureg.m ** 3
            except AttributeError as e:
                raise TypeError("Parameters are missing or not convertible to the expected units.") from e

            dn_dt = inflow_rate - outflow_rate
            dT_dt = (heat_exchange_rate / (n * self.R * T / V)).to(self.ureg.K / self.ureg.s)

            return [dn_dt.magnitude, dT_dt.magnitude]

        try:
            sol = solve_ivp(dydt, t_span, y0, method='RK45')
        except Exception as e:
            raise RuntimeError("Failed to perform dynamic simulation.") from e

        return sol


# Test Suite
class TestHydrogenContainerModel(unittest.TestCase):
    def setUp(self):
        self.params = HydrogenContainerParameters(
            V=2,  # m^3
            T=300,  # K
            n=1000,  # mol
            a=0.025,  # Pa * m^6 * mol^-2
            b=0.026,  # m^3 * mol^-1
            inflow_rate=1,  # mol/s
            outflow_rate=0.5,  # mol/s
            heat_exchange_rate=1000  # J/s
        )
        self.model = HydrogenContainerModel()

    def test_van_der_waals_equation(self):
        pressure = self.model.van_der_waals_equation(self.params)
        self.assertIsNotNone(pressure, "Pressure should not be None.")
        self.assertGreater(pressure.magnitude, 0, "Pressure should be positive.")

    def test_dynamic_simulation(self):
        t_span = (0, 10)  # seconds
        y0 = [1000, 300]  # [mol, K]
        sol = self.model.dynamic_simulation(self.params, t_span, y0)
        self.assertIsNotNone(sol, "Solution should not be None.")
        self.assertTrue(hasattr(sol, 'y'), "Solution should have attribute 'y'.")
        self.assertGreater(len(sol.y[0]), 0, "Solution should have data points.")
        self.assertGreater(len(sol.y[1]), 0, "Solution should have data points.")

    def test_error_handling(self):
        with self.assertRaises(TypeError):
            self.model.van_der_waals_equation(None)

        with self.assertRaises(ValueError):
            self.model.dynamic_simulation(self.params, (0, 10), [0, 300])


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
