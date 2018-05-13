''' GUI for IOT Hub
revision
2018-05-12, liangc, initial version
'''

import os
import sys
import sqlite3 
import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



sqlite_file = "iot_sensor_data.db"

class IoTHubApp(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'IoT Hub'
        self.width = 640
        self.height = 400
        self._conn = sqlite3.connect(sqlite_file)
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)
 
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(500,0)
        button.resize(140,100)
 
        self.show()
 
    def query(self, timeslice):
        ''' query table with timeslice '''
        c = self._conn.cursor()
        
        query_stmt = "select datetime(tm, 'localtime'), avg(pressure), avg(temp), avg(cpu_temp), avg(rssi), avg(humidity), avg(battery_volt) " \
                    "from sensor_data group by (strftime('%%s', tm)/(%d)) order by tm asc" % timeslice
        c.execute(query_stmt)
        query_result = c.fetchall()
        # convert the list of tuples to two lists
        t_tm, t_pressure, t_temp, t_cpu_temp, t_rssi, t_humidity, t_batt_volt= zip(*query_result)
        tm = list(t_tm)
        pressure = list(t_pressure)
        temp = list(t_temp)
        cpu_temp = list(t_cpu_temp)
        rssi = list(t_rssi)
        humidity = list(t_humidity)
        batt_volt = list(t_batt_volt)
        c.close()       
        return tm, pressure, temp, cpu_temp, rssi, humidity, batt_volt
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self._iotHub = parent
        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        tm, pressure, temp, cpu_temp, rssi, humidity, batt_volt = self._iotHub.query(1200)
        
        # layout of plots: 2x2
        color = 'tab:red'
        ax_pressure = self.figure.add_subplot(221) #Pos=1
        ax_pressure.set_ylabel('Pressure', color = color)
        ax_pressure.tick_params(axis='y', labelcolor = color)
        ax_pressure.plot_date(tm, pressure, 'r-', xdate=True) #(tm, pressure, 'r-')

        #ax_pressure.set_title('Pressure')
        color = 'tab:blue'
        ax_humidity = ax_pressure.twinx()
        ax_humidity.set_ylabel('Humidity', color = color)
        ax_humidity.tick_params(axis='y', labelcolor = color)
        ax_humidity.plot_date(tm, humidity, 'b-', xdate=True)
        
        # room temperature and cpu temperature
        ax_temp = self.figure.add_subplot(222)
        ax_temp.set_ylabel('Degree(C)', color = color)
        ax_temp.tick_params(axis='y', labelcolor = color)
        ax_temp.plot_date(tm, temp, 'r-', xdate=True, label='temp') #(tm, pressure, 'r-')
        ax_temp.plot_date(tm, cpu_temp, 'b-', xdate=True, label='cpu temp') #(tm, pressure, 'r-')
        #ax_temp.set_title('Temperature')
        # Now add the legend with some customizations.
        legend = ax_temp.legend(loc='upper center', shadow=True)
        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        
        # rssi and battery volt
        color = 'tab:red'
        ax_rssi = self.figure.add_subplot(212)
        ax_rssi.set_ylabel('RSSI', color = color)
        ax_rssi.tick_params(axis='y', labelcolor = color)
        ax_rssi.plot_date(tm, rssi, 'r-', xdate=True) #(tm, pressure, 'r-')
        
        color = 'tab:blue'
        ax_batt_volt = ax_rssi.twinx()
        ax_batt_volt.set_ylabel('Battery Volt', color = color)
        ax_batt_volt.tick_params(axis='y', labelcolor = color)
        ax_batt_volt.plot_date(tm, batt_volt, 'b-', xdate=True)
                        
        self.figure.autofmt_xdate()
        self.figure.tight_layout()
        self.draw()
        
def main2():
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
    app = QApplication(sys.argv)
    ex = IoTHubApp()
    sys.exit(app.exec_())