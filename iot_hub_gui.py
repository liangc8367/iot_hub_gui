''' GUI for IOT Hub
revision
2018-05-12, liangc, initial version
'''

import os
import sys
import sqlite3

import matplotlib.pyplot as plt


sqlite_file = "iot_sensor_data.db"

def main():
    sys.stdout.write("Hello\n")
    # load database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    query_stmt = "select datetime(tm, 'localtime'), pressure from sensor_data order by tm asc limit 20"
    c.execute(query_stmt)
    pressure_data = c.fetchall()
    # convert the list of tuples to two lists
    tm, pressure = zip(*pressure_data)
    tm1 = list(tm)
    pressure1 = list(pressure)
    
    # plot on gui
    plt.plot(tm1, pressure1)
    plt.gcf().autofmt_xdate()
    plt.show()
    sys.stdout.write("Bye\n")
    


if __name__ == '__main__':
    main()