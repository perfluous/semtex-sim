import sympy as sp
import simpy
from pint import UnitRegistry
from State.CentralizedState import CentralizedState as PEMStateElectrochemical


class PEMParametersElectrochemical:
    """
    This class holds the parameters for the PEMElectrochemicalModel.
    It acts as a container for all relevant parameters.
    """

    def __init__(self, V0, eta_act_a, eta_act_c, eta_ohm, area):
        self.V0 = V0
        self.eta_act_a = eta_act_a
        self.eta_act_c = eta_act_c
        self.eta_ohm = eta_ohm
        self.area = area


class PEMElectrochemicalModel:
    """
    This class implements the electrochemical model for determining the energy and
    exergy of electricity involved in the PEM electrolyzer operation.
    """

    def __init__(self):
        self.ureg = UnitRegistry()

    def calculate_Q_electric(self, params: PEMParametersElectrochemical, state: PEMStateElectrochemical):
        J = state.J * self.ureg.ampere / (self.ureg.m ** 2)
        V = state.V * self.ureg.V
        area = params.area * (self.ureg.m ** 2)
        return (J * V * area).to(self.ureg.J / self.ureg.s)

    def calculate_V(self, params: PEMParametersElectrochemical, state: PEMStateElectrochemical):
        V0 = params.V0 * self.ureg.V
        eta_act_a = params.eta_act_a * self.ureg.V
        eta_act_c = params.eta_act_c * self.ureg.V
        eta_ohm = params.eta_ohm * self.ureg.V
        return (V0 + eta_act_a + eta_act_c + eta_ohm).to(self.ureg.V)

    def update(self, params: PEMParametersElectrochemical, state: PEMStateElectrochemical, eta_ohm):
        V0 = params.V0 * self.ureg.V
        eta_act_a = params.eta_act_a * self.ureg.V
        eta_act_c = params.eta_act_c * self.ureg.V
        updated_V = (V0 + eta_act_a + eta_act_c + eta_ohm).to(self.ureg.V)
        state.update_V(updated_V.magnitude)
