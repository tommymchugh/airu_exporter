import sensor_data

class Sensor:
    def __init__(self, sensor_type, start_dt, end_dt, json_data):
        self.sensor_type = sensor_type
        self.start_dt = start_dt
        self.end_dt = end_dt

        self.data = []

        for data in json_data:
            value_id = self.sensor_type.upper()
            value_key = ""
            value_keys = data.keys()
            for key in value_keys:
                if value_id.lower() == key.lower():
                    value_key = key
                    break
            
            value = data[value_key]
            timestamp = data["time"]
            
            data_entry = sensor_data.Data(value, timestamp)
            self.data.append(data_entry)

    def __str__(self):
        return "Sensor Type: {}\nStart: {}\nEnd: {}\n".format(self.sensor_type, self.start_dt, self.end_dt)  
