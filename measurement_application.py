import datetime
import glob
import subprocess
import time
import os

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# information of tempreture sensor
root_path = "/sys/bus/w1/devices/"
device_id = glob.glob(root_path + '28*')[0]
device_file = device_id + "/w1_slave"

magnification = 1000.0

def read_tempreture_file():
    cmd = ['cat', device_file]
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r_stdout, r_stderr = result.communicate()
    r_stdout_decode = r_stdout.decode('utf-8')
    lines = r_stdout_decode.split('\n')

    return lines

def get_temp_sensor():
    lines = read_tempreture_file()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_tempreture_file()

    equal_pos = lines[1].find('t=')
    if equal_pos != -1:
        temp_str = lines[1][equal_pos + 2:]
        temp = float(temp_str) / magnification

        return temp

def read_cpu_temp():
    cmd = 'vcgencmd measure_temp'
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    r_stdout, r_stderr = result.communicate()
    lines = r_stdout.split('\n')
    
    return lines

def get_cpu_temp():
    lines = read_cpu_temp()

    equal_pos_start = lines[0].find('temp=')
    equal_pos_end = lines[0].find('\'C')
    if equal_pos_start != -1 and equal_pos_end != -1:
        temp_str = lines[0][equal_pos_start + 5 : equal_pos_end]
        temp = float(temp_str)

        return temp

if __name__ == '__main__':

    cpu_temp = get_cpu_temp()
    sensor_temp = get_temp_sensor()

    print(cpu_temp, sensor_temp)
