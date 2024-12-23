class CentralizedState:
    def __init__(self, initial_values=None):
        if initial_values is None:
            initial_values = {}

        self.T = initial_values.get('T', None)
        self.N_H2_out_dot = initial_values.get('N_H2_out_dot', None)
        self.Q_electric = initial_values.get('Q_electric', None)
        self.J = initial_values.get('J', None)
        self.N_H2O_in = initial_values.get('N_H2O_in', None)
        self.V = initial_values.get('V', None)
        self.lambda_a = initial_values.get('lambda_a', None)
        self.lambda_c = initial_values.get('lambda_c', None)
        self.L = initial_values.get('L', None)
        self.alpha = initial_values.get('alpha', None)
        self.eta_act = initial_values.get('eta_act', None)
        self.J0 = initial_values.get('J0', None)
        self.x = initial_values.get('x', 0)
        self.lambda_x = self.calculate_lambda_x()
        self.R_PEM = initial_values.get('R_PEM', None)
        self.eta_ohm = initial_values.get('eta_ohm', None)

    def update_T(self, new_T):
        self.T = new_T

    def update_N_H2_out_dot(self, new_N_H2_out_dot):
        self.N_H2_out_dot = new_N_H2_out_dot

    def update_Q_electric(self, new_Q_electric):
        self.Q_electric = new_Q_electric

    def update_J(self, new_J):
        self.J = new_J
        self.lambda_x = self.calculate_lambda_x()  # lambda_x depends on J, so we recalculate it when J changes

    def update_N_H2O_in(self, new_N_H2O_in):
        self.N_H2O_in = new_N_H2O_in

    def update_V(self, new_V):
        self.V = new_V

    def update_lambda_a(self, new_lambda_a):
        self.lambda_a = new_lambda_a
        self.lambda_x = self.calculate_lambda_x()  # lambda_x depends on lambda_a, so we recalculate it when lambda_a changes

    def update_lambda_c(self, new_lambda_c):
        self.lambda_c = new_lambda_c
        self.lambda_x = self.calculate_lambda_x()  # lambda_x depends on lambda_c, so we recalculate it when lambda_c changes

    def update_L(self, new_L):
        self.L = new_L
        self.lambda_x = self.calculate_lambda_x()  # lambda_x depends on L, so we recalculate it when L changes

    def update_alpha(self, new_alpha):
        self.alpha = new_alpha

    def update_eta_act(self, new_eta_act):
        self.eta_act = new_eta_act

    def update_J0(self, new_J0):
        self.J0 = new_J0

    def update_x(self, new_x):
        self.x = new_x
        self.lambda_x = self.calculate_lambda_x()  # lambda_x depends on x, so we recalculate it when x changes

    def update_R_PEM(self, new_R_PEM):
        self.R_PEM = new_R_PEM

    def update_eta_ohm(self, new_eta_ohm):
        self.eta_ohm = new_eta_ohm

    def calculate_lambda_x(self):
        if self.lambda_a is not None and self.lambda_c is not None and self.L is not None:
            return ((self.lambda_a - self.lambda_c) / self.L) * self.x + self.lambda_c
        else:
            return None
