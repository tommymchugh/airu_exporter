import airu

start = airu.get_formatted_time("2017", "01", "01", "00", "00", "00")
end = airu.get_formatted_time("2019", "05", "01", "00", "00", "00")

airu.export_node_data(start, end)
