import paho.mqtt.client as mqtt

from Sensors.MQTTManager import MQTTManager
from State.CentralizedState import CentralizedState


class TemperatureSensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_TempSensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        temperature = self.state.T
        result = self.mqtt_manager.send_sensor_data(device_id="TempSensorDevice", topic=self.topic, payload=temperature)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {temperature}")
        else:
            print(f"Failed to Publish Message to {self.topic}")




class ElectricChargeSensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_ElectricChargeSensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        electric_charge = self.state.Q_electric
        result = self.mqtt_manager.send_sensor_data(device_id="ElectricChargeSensorDevice", topic=self.topic, payload=electric_charge)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {electric_charge}")
        else:
            print(f"Failed to Publish Message to {self.topic}")



class CurrentDensitySensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_CurrentDensitySensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        current_density = self.state.J
        result = self.mqtt_manager.send_sensor_data(device_id="CurrentDensitySensorDevice", topic=self.topic, payload=current_density)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {current_density}")
        else:
            print(f"Failed to Publish Message to {self.topic}")




class VoltageSensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_VoltageSensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        voltage = self.state.V
        result = self.mqtt_manager.send_sensor_data(device_id="VoltageSensorDevice", topic=self.topic, payload=voltage)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {voltage}")
        else:
            print(f"Failed to Publish Message to {self.topic}")




class HydrogenOutputFlowSensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_HydrogenOutputFlowSensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        hydrogen_flow = self.state.N_H2_out_dot
        result = self.mqtt_manager.send_sensor_data(device_id="H2OutFlowSensorDevice", topic=self.topic, payload=hydrogen_flow)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {hydrogen_flow}")
        else:
            print(f"Failed to Publish Message to {self.topic}")




class WaterInputFlowSensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_WaterInputFlowSensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        water_flow = self.state.N_H2O_in
        result = self.mqtt_manager.send_sensor_data(device_id="H2OInFlowSensorDevice", topic=self.topic, payload=water_flow)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {water_flow}")
        else:
            print(f"Failed to Publish Message to {self.topic}")




class ResistanceSensor:
    def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_ResistanceSensor"):
        self.state = state
        self.mqtt_manager = mqtt_manager
        self.topic = topic

    def read_and_publish(self):
        resistance = self.state.R_PEM
        result = self.mqtt_manager.send_sensor_data(device_id="ResistanceSensorDevice", topic=self.topic, payload=resistance)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message Published Successfully to {self.topic} with payload {resistance}")
        else:
            print(f"Failed to Publish Message to {self.topic}")




# class PressureSensor:
#     def __init__(self, state: CentralizedState, mqtt_manager: MQTTManager, topic="H2PEMHydrogenGenerator_PressureSensor"):
#         self.state = state  # assuming that the pressure will be added to the state
#         self.mqtt_manager = mqtt_manager
#         self.topic = topic
#
#     def read_and_publish(self):
#         pressure = self.state.P  # assuming that P represents pressure in the state
#
#         result = self.mqtt_manager.send_sensor_data(device_id="some_device_id", topic=self.topic, payload=temperature)
#         if result.rc == mqtt.MQTT_ERR_SUCCESS:
#             print(f"Message Published Successfully to {self.topic} with payload {temperature}")
#         else:
#             print(f"Failed to Publish Message to {self.topic}")


