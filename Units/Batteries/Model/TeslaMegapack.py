import simpy


class TeslaMegapack:
    def __init__(self, env, capacity_mwh, max_charge_rate_mw, max_discharge_rate_mw):
        self.env = env  # SimPy environment
        self.capacity_mwh = capacity_mwh
        self.max_charge_rate_mw = max_charge_rate_mw
        self.max_discharge_rate_mw = max_discharge_rate_mw
        self.stored_energy_mwh = 0  # Initially, the battery is empty
        self.state = "IDLE"  # Initial state is IDLE
        self.process_ref = env.process(self.process())  # Registering the process method with the environment

    def process(self):
        while True:
            # Logic to interact with other components and manage the battery state
            # Logic for charging, discharging, and messaging will be added here
            # based on the interactions with other components in your system

            print(f"At {self.env.now}, Battery State: {self.state}, Stored Energy: {self.stored_energy_mwh} MWh")

            yield self.env.timeout(1)  # Run the process every hour or as needed

    def charge(self, energy_mwh):
        # Logic to charge the battery with the specified amount of energy
        # Ensure that the battery does not overcharge
        energy_to_charge = min(energy_mwh, self.capacity_mwh - self.stored_energy_mwh)
        self.stored_energy_mwh += energy_to_charge
        self.state = "CHARGING" if energy_to_charge > 0 else "IDLE"

    def discharge(self, energy_mwh):
        # Logic to discharge the battery with the specified amount of energy
        # Ensure that the battery does not over-discharge
        energy_to_discharge = min(energy_mwh, self.stored_energy_mwh)
        self.stored_energy_mwh -= energy_to_discharge
        self.state = "DISCHARGING" if energy_to_discharge > 0 else "IDLE"

    def get_state_of_charge(self):
        # Return the state of charge as a percentage
        return (self.stored_energy_mwh / self.capacity_mwh) * 100

    def get_stored_energy(self):
        # Return the amount of energy currently stored in the battery
        return self.stored_energy_mwh


# # Example of how to use this class with SimPy
# if __name__ == "__main__":
#     env = simpy.Environment()
#     battery = TeslaMegapack(env, capacity_mwh=10, max_charge_rate_mw=2, max_discharge_rate_mw=2)
#     env.run(until=5)
