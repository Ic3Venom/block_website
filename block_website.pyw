
import os
import csv
from datetime import datetime as dt
from time import sleep

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
times_path = os.path.dirname(__file__) + r"/time.txt"
sites_path = os.path.dirname(__file__) + r"/website_list.csv"
redirect = "127.0.0.1"
times = []

while True:
    with open(sites_path, 'r') as sites_file:
        website_list = list(csv.reader(sites_file))[0]

    with open(times_path) as time_file:
        times = []
        time_file.readline()  # skip the file documentation
        times.append(int(time_file.readline().split(" ")[2]))
        times.append(int(time_file.readline().split(" ")[2]))

    try:
        if (times[0] <= dt.now().hour and dt.now().hour < times[1]):
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in website_list:
                    if website not in content:
                        file.write("\n" + redirect + " " + website)
        else:
            with open(hosts_path, "r+") as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in website_list):
                        file.write(line)
                file.truncate()
    except PermissionError:
        os.system("echo ERROR: file \"" + os.path.dirname(__file__) +
                  "\\block.bat\" does not have permission")
        os.system("echo        to access your hosts file.")
        os.system("echo - Restart the batch file in admin mode and try again.")
        os.system('pause')
        exit(1)

    sleep(60)