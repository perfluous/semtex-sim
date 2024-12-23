import sympy as sp
import simpy
from pint import UnitRegistry
from State.CentralizedState import CentralizedState as PEMHeatExergyState

class PEMHeatExergyParameters:
    def __init__(self, F, eta_act_a, eta_act_c, eta_ohm, Delta_S, T0):
        self.F = F
        self.eta_act_a = eta_act_a
        self.eta_act_c = eta_act_c
        self.eta_ohm = eta_ohm
        self.Delta_S = Delta_S
        self.T0 = T0

class PEMHeatExergyCalculator:
    def __init__(self):
        self.ureg = UnitRegistry()
        self.F, self.eta_act_a, self.eta_act_c, self.eta_ohm, self.J, self.T, self.Delta_S, self.T0 = sp.symbols(
            'F eta_act_a eta_act_c eta_ohm J T Delta_S T0'
        )
        self.sigma_eq = 2 * self.F * (self.eta_act_a + self.eta_act_c + self.eta_ohm)
        self.Q_heat_PEM_eq = (self.J / (2 * self.F)) * (self.T * self.Delta_S - self.sigma_eq)
        self.E_heat_PEM_eq = self.Q_heat_PEM_eq * (1 - (self.T0 / self.T))
        self.sigma_func = sp.lambdify(
            (self.F, self.eta_act_a, self.eta_act_c, self.eta_ohm),
            self.sigma_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math']
        )
        self.Q_heat_PEM_func = sp.lambdify(
            (self.J, self.F, self.T, self.Delta_S, self.eta_act_a, self.eta_act_c, self.eta_ohm),
            self.Q_heat_PEM_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math']
        )
        self.E_heat_PEM_func = sp.lambdify(
            (self.J, self.F, self.T, self.Delta_S, self.eta_act_a, self.eta_act_c, self.eta_ohm, self.T0),
            self.E_heat_PEM_eq, modules=[{'Quantity': self.ureg.Quantity}, 'math']
        )

    def calculate_entropy_generation(self, params: PEMHeatExergyParameters):
        return self.sigma_func(params.F, params.eta_act_a, params.eta_act_c, params.eta_ohm)

    def calculate_Q_heat_PEM(self, params: PEMHeatExergyParameters, state: PEMHeatExergyState):
        return self.Q_heat_PEM_func(state.J, params.F, state.T, params.Delta_S, params.eta_act_a, params.eta_act_c,
                                    params.eta_ohm)

    def calculate_E_heat_PEM(self, params: PEMHeatExergyParameters, state: PEMHeatExergyState):
        return self.E_heat_PEM_func(state.J, params.F, state.T, params.Delta_S, params.eta_act_a, params.eta_act_c,
                                    params.eta_ohm, params.T0)

    def update(self, params: PEMHeatExergyParameters, state: PEMHeatExergyState):
        """
        Updates the state based on the current parameter values.

        :param params: The parameters object containing the current parameters.
        :param state: The state object containing the current state.
        """
        # Compute σ using η_act,a, η_act,c, η_ohm, and other constants.
        sigma = self.calculate_entropy_generation(params)

        # Update Q_heat.PFM and E_heat,pEM using J, TΔS, σ, and T_0.
        q_heat_pem = self.calculate_Q_heat_PEM(params, state)
        e_heat_pem = self.calculate_E_heat_PEM(params, state)

        # Here, you can add logic to update the state object if needed.
        # For instance:
        # state.update_J(new_J)
        # state.update_T(new_T)

        return sigma, q_heat_pem, e_heat_pem  # Return updated values


def pem_process(env, params: PEMHeatExergyParameters, state: PEMHeatExergyState, calculator: PEMHeatExergyCalculator):
    while True:
        # hypothetical new values for J and T.
        new_J = state.J + 1  # Placeholder, replace with your logic or data
        new_T = state.T + 1  # Placeholder, replace with your logic or data
        state.update_J(new_J)
        state.update_T(new_T)

        entropy_gen = calculator.calculate_entropy_generation(params)
        q_heat_pem = calculator.calculate_Q_heat_PEM(params, state)
        e_heat_pem = calculator.calculate_E_heat_PEM(params, state)

        print(f"Entropy Generation: {entropy_gen}, Q Heat PEM: {q_heat_pem}, E Heat PEM: {e_heat_pem}")

        yield env.timeout(1)  # replace with your desired time step
