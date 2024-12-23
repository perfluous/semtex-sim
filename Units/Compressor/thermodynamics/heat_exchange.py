# Heat exchange
from pint import UnitRegistry

ureg = UnitRegistry()

class HeatExchange:
    def __init__(self, initial_temperature, final_temperature_desired, cooling_medium='ambient_air', heat_exchanger_efficiency=0.85):
        self.initial_temperature = initial_temperature * ureg.kelvin
        self.final_temperature = None  # Actual final temperature after cooling (in K)
        self.final_temperature_desired = final_temperature_desired * ureg.kelvin  # Desired temperature after cooling
        self.heat_removed = None  # Amount of heat removed during the cooling process (in J)
        self.cooling_medium = cooling_medium
        self.cooling_medium_temperature = self.determine_cooling_medium_temperature()
        self.heat_exchanger_efficiency = heat_exchanger_efficiency
        self.cooling_medium_heat_capacity = self.determine_cooling_medium_heat_capacity()

    def calculate_heat_generated(self, compression_work):
        return compression_work

    def determine_cooling_medium_temperature(self):
        if self.cooling_medium == 'ambient_air':
            return 298 * ureg.kelvin
        # More conditions can be added for different cooling mediums

    def determine_cooling_medium_heat_capacity(self):
        # Placeholder method to set heat capacity based on cooling medium
        # For now, we'll assume ambient air with a heat capacity of about 1005 J/kg.K
        if self.cooling_medium == 'ambient_air':
            return 1005 * ureg.joule / ureg.kilogram / ureg.kelvin
        # More conditions can be added for different cooling mediums

    def calculate_heat_removed(self, compression_heat):
        self.heat_removed = compression_heat

    def perform_cooling(self):
        # Enhanced method to simulate the cooling process
        temperature_gradient = self.initial_temperature - self.cooling_medium_temperature
        self.final_temperature = self.initial_temperature - (self.heat_exchanger_efficiency * temperature_gradient)

    # Note: Additional methods can be added to handle efficiency of heat exchangers, etc.
