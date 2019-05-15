import sensor
import api_base as api
import urllib.request
import json
import ssl

context = ssl._create_unverified_context()
show_messages = True

class NodeLocation:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

class Node:
    def __init__(self, supported_sensors, json_data):
        self.node_id = json_data["ID"]

        lat = json_data["Latitude"]
        long = json_data["Longitude"]
        self.location = NodeLocation(lat, long)

        self.supported_sensors = supported_sensors
        self.sensors = []

    def __get_sensor_url(self, node_id, sensor, start_dt, end_dt):
        sensor_data_url = "/rawDataFrom"
        sensor_source = "airu"
        sensor_url = "{0}{1}?id={2}&sensorSource={3}&start={4}&end={5}&show={6}".format(api.api_base_url,
                                                                                    sensor_data_url,
                                                                                    node_id,
                                                                                    sensor_source,
                                                                                    start_dt,
                                                                                    end_dt,
                                                                                    sensor)
        return sensor_url

    def get_sensors(self, start_dt, end_dt):
        for sensor_type in self.supported_sensors:
            if show_messages:
                print("Retrieving {} data...".format(sensor_type))
            sensor_url = self.__get_sensor_url(self.node_id, sensor_type, start_dt, end_dt)
            url_request = urllib.request.urlopen(sensor_url, context=context)
            url_response = url_request.read().decode()

            sensor_data_json = json.loads(url_response)["data"]
            sensor_item = sensor.Sensor(sensor_type, start_dt, end_dt, sensor_data_json)
            self.sensors.append(sensor_item)
            if show_messages:
                print("Retrieved {} data".format(sensor_type))

    def __str__(self):
        return "Node ID: {}\nLat: {}\nLong: {}\n".format(self.node_id, self.location.lat, self.location.long)
