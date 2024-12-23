import sympy as sp
import simpy
from pint import UnitRegistry
import math
from State.CentralizedState import CentralizedState as PEMState

class PEMParameters:
    def __init__(self, R, T, F, J_ref_a, J_ref_c, E_act_a, E_act_c):
        self.R = R
        self.T = T
        self.F = F
        self.J_ref_a = J_ref_a
        self.J_ref_c = J_ref_c
        self.E_act_a = E_act_a
        self.E_act_c = E_act_c



class ActivationOverpotential:
    def __init__(self):
        self.ureg = UnitRegistry()

    def update(self, params: PEMParameters, state: PEMState):
        # Compute exchange current density for anode and cathode
        J_0_a = self.compute_exchange_current_density('a', params)
        J_0_c = self.compute_exchange_current_density('c', params)

        # Compute activation overpotential for anode and cathode
        eta_act_a = self.compute_activation_overpotential(state, 'a', params)
        eta_act_c = self.compute_activation_overpotential(state, 'c', params)

        return eta_act_a, eta_act_c, J_0_a, J_0_c  # Return updated values

    def compute_exchange_current_density(self, electrode, params: PEMParameters):
        R = params.R * self.ureg.joule / (self.ureg.mol * self.ureg.kelvin)
        T = params.T * self.ureg.kelvin
        J_ref_a = params.J_ref_a * self.ureg.ampere / (self.ureg.meter ** 2)
        J_ref_c = params.J_ref_c * self.ureg.ampere / (self.ureg.meter ** 2)
        E_act_a = params.E_act_a * self.ureg.joule / self.ureg.mol
        E_act_c = params.E_act_c * self.ureg.joule / self.ureg.mol

        if electrode == 'a':
            J_0 = J_ref_a * math.exp(-float(E_act_a / (R * T)))
        elif electrode == 'c':
            J_0 = J_ref_c * math.exp(-float(E_act_c / (R * T)))
        else:
            raise ValueError("Electrode should be either 'a' for anode or 'c' for cathode.")

        return J_0

    def compute_activation_overpotential(self, state: PEMState, electrode, params: PEMParameters):
        J = state.J * self.ureg.ampere / (self.ureg.meter ** 2)
        R = params.R * self.ureg.joule / (self.ureg.mol * self.ureg.kelvin)
        T = params.T * self.ureg.kelvin
        F = params.F * self.ureg.coulomb / self.ureg.mol
        J_0 = self.compute_exchange_current_density(electrode, params)

        eta_act = (R * T / F) * math.log((J / (2 * J_0)) + math.sqrt((J / (2 * J_0)) ** 2 + 1))
        return eta_act


def pem_simulation(env, params: PEMParameters, state: PEMState, activation_overpotential: ActivationOverpotential):
    time_step = 1  # Define a suitable time step for your simulation
    while True:
        new_J = state.J  # This is just a placeholder, replace with actual logic to update J

        state.update_J(new_J)

        eta_act_a = activation_overpotential.compute_activation_overpotential(state, 'a', params)
        eta_act_c = activation_overpotential.compute_activation_overpotential(state, 'c', params)

        print(f"Time: {env.now}, J: {state.J}, eta_act_a: {eta_act_a}, eta_act_c: {eta_act_c}")

        yield env.timeout(time_step)
