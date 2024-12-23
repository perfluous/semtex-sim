class CentralizedControlSystem:
    def __init__(self):
        self.units = {}  # Dictionary to hold references to all connected units

    def register_unit(self, unit_name, unit_reference):
        """Register a unit with the CCS."""
        self.units[unit_name] = unit_reference

    def retrieve_data_from_unit(self, unit_name, data_request):
        """Retrieve specific data from a registered unit."""
        unit = self.units.get(unit_name)
        if not unit:
            print(f"Error: {unit_name} not registered!")
            return None
        return unit.handle_data_request(data_request)

    def send_command_to_unit(self, unit_name, command, *args, **kwargs):
        """Send a command to a registered unit."""
        unit = self.units.get(unit_name)
        if not unit:
            print(f"Error: {unit_name} not registered!")
            return
        unit.handle_command(command, *args, **kwargs)

# This represents just the foundational structure.
# More methods and refinements can be added as we proceed.
