from influxdb import InfluxDBClient
import subprocess
import multiprocessing
import time
import datetime

cpu_cores  = range(multiprocessing.cpu_count())
cpu_temp = range(multiprocessing.cpu_count())

clock_points = []
temp_points = []

client = InfluxDBClient(host="192.168.1.49",port=8086,database="telegraf")

while True:
    lines = subprocess.check_output(['cat','/proc/cpuinfo']).decode("utf-8")
    lines = lines.split("\n")

    core = 0
    for line in lines:
        if "MHz" in line:
            clock_point = [
                {
                    "measurement": "cpu_clock",
                    "tags": {
                        "Cpu_core": f"Cpu_core{core}"
                    },

                    "fields": {
                        "value": float(line[11:])
                    }
                }
            ]
            core = core +1
            clock_points.append(clock_point)

    try:
        client.write_points(clock_points,protocol="json")
    except:
        while True:
            time.sleep(10)
            if client.write_points(clock_points,protocol="json"):
                break

    lines = subprocess.check_output(['sensors']).decode("utf-8")
    lines = lines.split("\n")

    core = 0
    for line in lines:
        if "Core" in line:
            point_temp = [
                {
                    "measurement": "cpu_temp",
                    "tags": {
                        "Cpu_core_temp": f"Cpu_core_temp_{core}"
                    },

                    "fields": {
                        "value": float(line[15:19])
                    }
                }
            ]
            temp_points.append(point_temp)
            core = core + 1

    try:
        client.write_points(temp_points,protocol="json")
    except:
        while True:
            time.sleep(10)
            if client.write_points(temp_points):
                break

    time.sleep(10)
    print(datetime.datetime.now())
