class Data:
    def __init__(self, value, timestamp):
        self.value = value

        self.timestamp = timestamp
        
        self.year = timestamp[0:4]
        self.month = timestamp[5:7]
        self.day = timestamp[8:10]
        self.hour = timestamp[11:13]
        self.minute = timestamp[14:16]
        self.second = timestamp[17:19]
        self.milliseconds = timestamp[20:-2]

    def __str__(self):
        return "Timestamp: {}\nValue: {}".format(self.timestamp, self.value)
