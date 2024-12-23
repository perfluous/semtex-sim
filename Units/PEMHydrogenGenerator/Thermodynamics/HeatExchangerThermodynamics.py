import sympy as sp
from pint import UnitRegistry
import simpy
from State.CentralizedState import CentralizedState as HeatExchangerState

class HeatExchangerParameters:
    def __init__(self, Q_max, F, H_H2O_T, H_H2O_T0, T0, T_source, epsilon):
        self.Q_max = Q_max  # Maximum theoretical heat exchange rate
        self.F = F  # Faraday constant
        self.H_H2O_T = H_H2O_T  # Enthalpy of H2O at temperature T
        self.H_H2O_T0 = H_H2O_T0  # Enthalpy of H2O at reference temperature T0
        self.T0 = T0  # Reference temperature
        self.T_source = T_source  # Temperature of heat source
        self.epsilon = epsilon  # Temperature of heat source



class HeatExchangerThermodynamics:
    def __init__(self, env, params: HeatExchangerParameters, state: HeatExchangerState, time_step):
        self.ureg = UnitRegistry()
        self.env = env
        self.params = params
        self.state = state
        self.time_step = time_step  # Time step for the simulation

        # Define symbolic variables
        self.epsilon, self.Q_max, self.J, self.F, self.H_H2O_T, self.H_H2O_T0, self.T0, self.T_source = sp.symbols(
            'epsilon Q_max J F H_H2O_T H_H2O_T0 T0 T_source'
        )

        # Define symbolic equations based on the given descriptions
        self.Q_eq = self.epsilon * self.Q_max
        self.Q_theoretical_eq = (self.J / (2 * self.F)) * (self.H_H2O_T - self.H_H2O_T0)
        self.E_heat_H2O_eq = self.Q_theoretical_eq * (1 - (self.T0 / self.T_source))

        # Convert symbolic equations into callable functions
        self.Q_func = sp.lambdify((self.epsilon, self.Q_max), self.Q_eq,
                                  modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        self.Q_theoretical_func = sp.lambdify((self.J, self.F, self.H_H2O_T, self.H_H2O_T0), self.Q_theoretical_eq,
                                              modules=[{'Quantity': self.ureg.Quantity}, 'math'])
        self.E_heat_H2O_func = sp.lambdify((self.J, self.F, self.H_H2O_T, self.H_H2O_T0, self.T0, self.T_source),
                                           self.E_heat_H2O_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math'])

        # Start the process
        self.action = env.process(self.run())

    def run(self):
        while True:
            # Perform the calculations and potentially update state variables
            Q = self.calculate_Q()
            Q_theoretical = self.calculate_Q_theoretical()
            E_heat_H2O = self.calculate_E_heat_H2O()

            # Simulation waits for the next time step
            yield self.env.timeout(self.time_step)

    def calculate_Q(self):
        return self.Q_func(self.params.epsilon, self.params.Q_max)

    def calculate_Q_theoretical(self):
        return self.Q_theoretical_func(self.state.J, self.params.F, self.params.H_H2O_T, self.params.H_H2O_T0)

    def calculate_E_heat_H2O(self):
        return self.E_heat_H2O_func(self.state.J, self.params.F, self.params.H_H2O_T, self.params.H_H2O_T0,
                                    self.params.T0, self.params.T_source)

    def update(self):
        # Perform the calculations
        Q = self.calculate_Q()
        Q_theoretical = self.calculate_Q_theoretical()
        E_heat_H2O = self.calculate_E_heat_H2O()

        # Update state or parameters if needed
        # For example, if epsilon needs to be updated based on Q, Q_theoretical, or E_heat_H2O,
        # you can do it here like this:
        # self.state.update_epsilon(new_epsilon)

        # Return the calculated values if they are needed in the calling function
        return Q, Q_theoretical, E_heat_H2O
