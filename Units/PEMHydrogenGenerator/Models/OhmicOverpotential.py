import sympy as sp
from pint import UnitRegistry
import simpy
import numpy as np  # Importing numpy for numerical calculations
from State.CentralizedState import CentralizedState as PEMStateOhmic


class PEMParametersOhmic:
    def __init__(self, T, z, F, R):
        self.T = T  # Temperature
        self.z = z  # Number of electrons transferred in the cell reaction
        self.F = F  # Faraday constant
        self.R = R  # Gas constant


class PEMOhmicOverpotentialModel:
    def __init__(self):
        self.ureg = UnitRegistry()

    def calculate_sigma(self, lambda_x, params: PEMParametersOhmic):
        T = params.T * self.ureg.kelvin
        sigma_eq = (0.5139 * lambda_x - 0.326) * sp.exp(1268 * (1 / 303 - 1 / T.magnitude))
        return sigma_eq * (self.ureg.S / self.ureg.m)

    def calculate_R_PEM(self, params: PEMParametersOhmic, state: PEMStateOhmic, num_points=1000):
        delta_x = state.L / num_points  # Width of each trapezoid
        total_resistance = 0  # Initialize total resistance to 0

        for i in range(num_points):
            x1 = i * delta_x  # x-coordinate of the left point of the trapezoid
            x2 = (i + 1) * delta_x  # x-coordinate of the right point of the trapezoid

            # Calculate λ(x) and σ[λ(x)] for x1 and x2
            lambda_x1 = ((state.lambda_a - state.lambda_c) / state.L) * x1 + state.lambda_c
            lambda_x2 = ((state.lambda_a - state.lambda_c) / state.L) * x2 + state.lambda_c
            sigma1 = self.calculate_sigma(lambda_x1, params)
            sigma2 = self.calculate_sigma(lambda_x2, params)

            # Calculate the area of the trapezoid and add it to the total resistance
            total_resistance += (1 / sigma1 + 1 / sigma2) * delta_x / 2

        return total_resistance

    def calculate_eta_ohm(self, state: PEMStateOhmic):
        J = state.J * self.ureg.ampere / (self.ureg.meter ** 2)
        R_PEM = state.R_PEM * self.ureg.ohm * (self.ureg.meter ** 2)
        eta_ohm_eq = J * R_PEM
        return eta_ohm_eq.to(self.ureg.V)

    def calculate_J_act(self, state: PEMStateOhmic, params: PEMParametersOhmic):
        J0 = state.J0 * self.ureg.ampere / (self.ureg.meter ** 2)
        eta_act = state.eta_act * self.ureg.V
        T = params.T * self.ureg.kelvin
        alpha = state.alpha
        z = params.z
        F = params.F * self.ureg.coulomb / self.ureg.mole
        R = params.R * self.ureg.joule / (self.ureg.mole * self.ureg.kelvin)

        J_act_eq = J0 * (
                sp.exp((alpha * z * F * eta_act) / (R * T)) - sp.exp(((1 - alpha) * z * F * eta_act) / (R * T)))
        return J_act_eq.to(self.ureg.A / (self.ureg.meter ** 2))

    def update(self, params: PEMParametersOhmic, state: PEMStateOhmic):
        # Update lambda_x in state
        updated_lambda_x = state.calculate_lambda_x()
        state.lambda_x = updated_lambda_x  # Update lambda_x in the state

        # Update R_PEM
        updated_R_PEM = self.calculate_R_PEM(params, state)
        state.R_PEM = updated_R_PEM.magnitude  # Update R_PEM in the state

        # Update eta_ohm using updated R_PEM
        updated_eta_ohm = self.calculate_eta_ohm(state)
        state.eta_ohm = updated_eta_ohm.magnitude  # Update eta_ohm in the state


def pem_simpy_process(env, model: PEMOhmicOverpotentialModel, params: PEMParametersOhmic, state: PEMStateOhmic):
    while True:
        # Update the state at each step before calculations
        model.update(params, state)

        sigma = model.calculate_sigma(state.lambda_x, params)
        eta_ohm = model.calculate_eta_ohm(state)
        J_act = model.calculate_J_act(state, params)

        print(f"sigma: {sigma}, lambda_x: {state.lambda_x}, eta_ohm: {eta_ohm}, J_act: {J_act}")

        yield env.timeout(1)  # Here, I'm assuming you want to wait for 1 time unit between each step, adjust if needed.
