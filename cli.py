import airu
import timer
airu.show_messages = False

print("WELCOME TO THE AIRU EXPORTER CLI")
print("The following questions will help export the correct data\n")

yes_no_answer = "Please use either yes or no for your answer\n"

every_sensor_answered = False
export_every_sensor = True
while every_sensor_answered == False:
    every_sensor = input("Would you like to export data for every sensor type? (yes or no)\n").lower()
    if every_sensor == "yes" or every_sensor == "no":
        every_sensor_answered = True
        if every_sensor == "no":
            export_every_sensor = False
    else:
        print(yes_no_answer)

sensors_using = []
if export_every_sensor == False:
    sensor_list = ""
    for index in range(len(airu.sensors)):
        sensor = airu.sensors[index]
        sensor_list += "{}. {}\n".format(index+1, sensor)

    returned_none = False
    first_entry = True
    which_sensor_text = "Which of the following sensors would you like to export data from?\n\nSensors:\n" + sensor_list + "\nType the sensor number on each line. Return an empty line to go to the next step.\n"

    while returned_none == False:
        which_sensor = input(which_sensor_text)
        which_sensor_text = ""

        error_text = "Please enter the number corresponding to the sensor you would like to choose."
        if first_entry == True:
            if which_sensor != "":
                first_entry = False
            else:
                print(error_text)

        if first_entry == False:
            if which_sensor != "":
                try:
                    entry = int(which_sensor)
                    if entry <= len(airu.sensors) and entry > 0:
                        sensors_using.append(entry-1)
                    else:
                        print(error_text)
                except:
                    print(error_text)
            else:
                returned_none = True

def check_date_format(date):
    try:
        for index in range(len(date)):
            character = date[index]
            is_year = index <= 3
            is_month = index <= 6 and index > 4
            is_day = index <= 9 and index > 7
            is_hour = index <= 12 and index > 10
            is_minute = index <= 15 and index > 13
            is_second = index <= 18 and index > 16

            if is_year or is_month or is_day or is_hour or is_minute or is_second:
                try:
                    num = int(index)
                except:
                    return False
        if date[4] != "-" and date[7] != "-" and date[10] != " " and date[13] != ":" and date[16] != ":":
            return False

        return True
    except:
        return False

sd_correct = False
start_date = ""
while sd_correct == False:
    start_date = input("\nWhich start date would you like to use for downloading sensor data?\nPlease use the format: YYYY-MM-DD hh:mm:ss\n")
    if check_date_format(start_date) == True:
        sd_correct = True

ed_correct = False
end_date = ""
while ed_correct == False:
    end_date = input("\nWhich end date would you like to use for downloading sensor data?\nPlease use the format: YYYY-MM-DD hh:mm:ss\n")
    if check_date_format(end_date) == True:
        ed_correct = True

output_location = input("\nWhat directory would you like to export the data to?\nWe default to the current directory if you do not enter a path.\n")

print("\nBeginning export...")
start_time = time.time()

if export_every_sensor == False:
    def get_sensor(index):
        return airu.sensors[index]
    airu.sensors = list(map(get_sensor, sensors_using))

s_year = start_date[0:4]
s_month = start_date[5:7]
s_day = start_date[8:10]
s_hour = start_date[11:13]
s_minute = start_date[14:16]
s_second = start_date[17:19]

e_year = end_date[0:4]
e_month = end_date[5:7]
e_day = end_date[8:10]
e_hour = end_date[11:13]
e_minute = end_date[14:16]
e_second = end_date[17:19]

start = airu.get_formatted_time(s_year, s_month, s_day, s_hour, s_minute, s_second)
end = airu.get_formatted_time(e_year, e_month, e_day, e_hour, e_minute, e_second)

if output_location != "":
    if output_location[-1] != "/":
        output_location += "/"
    airu.output_location_path = output_location

airu.export_node_data(start, end)
end_time = time.time()
total_time = round(end_time-start_time, 2)
print("Export completed in {} seconds. Enjoy!".format(total_time))
