import json

import paho.mqtt.client as mqtt

from Sensors.Connection import DEVICE_CONNECTION_STRINGS


class MQTTManager:
    def __init__(self):
        self.broker_address = "semtex-iot-hub.azure-devices.net"
        self.client = mqtt.Client("P1")
        self.client.on_connect = self.on_connect
        self.connect_to_broker()
        self.clients = {}
        self.initialize_clients(DEVICE_CONNECTION_STRINGS)
        self.device_connection_strings = [
            "sensor/electric_charge_sensor_device/electric_charge/#",
            "sensor/pressure_sensor_device/pressure/value",
            "sensor/temp_sensor_device/temperature/value",
            "sensor/voltage_sensor_device/voltage/value",
            "sensor/h2o_in_flow_sensor_device/flow_rate/value",
            "sensor/resistance_sensor_device/resistance/value",
            "sensor/current_density_sensor_device/current_density/value",
            "sensor/h2_out_flow_sensor_device/flow_rate/value",
        ]

    def connect_to_broker(self):
        try:
            self.client.connect(self.broker_address)
            self.client.loop_start()
        except Exception as e:
            print(f"Could not connect to MQTT Broker: {e}")

    def initialize_clients(self, device_connection_strings):
        for device_id, connection_info in device_connection_strings.items():
            try:
                client = mqtt.Client(client_id=device_id)
                client.on_connect = self.on_connect
                client.on_message = self.on_message

                hostname = connection_info['con_str'].split(";")[0].split("=")[1]
                password = connection_info['key']

                client.username_pw_set(username=device_id, password=password)
                client.connect(host=hostname, port=443)
                client.loop_start()

                self.clients[device_id] = client

            except Exception as e:
                print(f"Error initializing client {device_id}: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            for topic in self.TOPICS:
                client.subscribe(topic)
        else:
            print("Connection failed - Return Code: ", str(rc))

    def on_message(self, client, userdata, msg):
        try:
            print(msg.topic + " " + str(msg.payload))
            sensor_data = json.loads(msg.payload.decode())
            _, device_id, sensor_type, _ = msg.topic.split('/')
            print(f"Received {sensor_type} data from {device_id}: {sensor_data}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def send_sensor_data(self, device_id, topic, payload):
        if device_id in self.clients:
            return self.clients[device_id].publish(topic,   payload)
        else:
            print(f"Device {device_id} is not initialized.")
            return None

    def stop_clients(self):
        for client in self.clients.values():
            client.loop_stop()
            client.disconnect()
        self.client.loop_stop()
        self.client.disconnect()
