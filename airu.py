import urllib.request
import node
import sensor
import json
import api_base as api
import ssl

show_messages = True

context = ssl._create_unverified_context()
sensor_list_url = "/liveSensors/airU"
sensors = ["pm25", "pm10", "pm1", "co", "no", "temperature", "humidity"]

def get_formatted_time(year, month, day, hour, minute, second):
    return "{0}-{1}-{2}T{3}:{4}:{5}Z".format(year, month, day, hour, minute, second)

def get_nodes():
    if show_messages:
        print("Retrieving Node List...")
    nodes = []
    node_list_url = api.api_base_url + sensor_list_url
    url_request = urllib.request.urlopen(node_list_url, context=context)
    url_response = url_request.read().decode()

    node_list_json = json.loads(url_response)
    for node_list_item in node_list_json:
        if show_messages == False:
            node.show_messages = False
        node_item = node.Node(sensors, node_list_item)
        nodes.append(node_item)
    if show_messages:
        print("Retrieved {} Nodes\n".format(len(nodes)))
    return nodes

def get_nodes_data(nodes, start_dt, end_dt):
    if show_messages:
        print("Retrieving sensor data for nodes...")
    for node_item in nodes:
        if show_messages:
            print("Retrieving sensor data for node {}".format(node_item.node_id))
        node_item.get_sensors(start_dt, end_dt)
        if show_messages:
            print("Retrieved sensor data for node {}\n".format(node_item.node_id))
    return nodes

def export_to_csv(nodes, output_node_file, output_data_file):
    if show_messages:
        print("Exporting node and sensor data to csv...")
    # Node output first
    node_output = open(output_node_file, 'w')
    node_output.write("node_id,lat,long\n")
    data_output = open(output_data_file, 'w')
    data_output.write("node_id,sensor,timestamp,value\n")

    for node_item in nodes:
        node_id = node_item.node_id
        node_lat = node_item.location.lat
        node_long = node_item.location.long
        node_output.write("{},{},{}\n".format(node_id, node_lat, node_long))

        for sensor_item in node_item.sensors:
            sensor_type = sensor_item.sensor_type

            for data_item in sensor_item.data:
                timestamp = "{}-{}-{} {}:{}:{}".format(data_item.year,
                                      data_item.month,
                                      data_item.day,
                                      data_item.hour,
                                      data_item.minute,
                                      data_item.second)
                value = data_item.value
                data_output.write("{},{},{},{}\n".format(node_id,
                                                       sensor_type,
                                                       timestamp,
                                                       value))

    node_output.close()
    data_output.close()
    if show_messages:
        print("Data exported to files\n")

output_location_path = ""

def export_node_data(start_dt, end_dt):
    if show_messages:
        print("WELCOME TO THE AIRU EXPORTER", "Beginning the export...\n", sep="\n")
    nodes = get_nodes()
    nodes = get_nodes_data(nodes, start_dt, end_dt)

    output_node_file = output_location_path + "nodes.csv"
    output_data_file = output_location_path + "data.csv"
    export_to_csv(nodes, output_node_file, output_data_file)
    if show_messages:
        print("Export complete. Enjoy!")
