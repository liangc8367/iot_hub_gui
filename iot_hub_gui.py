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
 
    def query_pressure(self, interval_seconds):
        c = self._conn.cursor()
        
        query_stmt = "select datetime(tm, 'localtime'), avg(pressure) from sensor_data group by (strftime('%%s', tm)/(%d))" % interval_seconds
        c.execute(query_stmt)
        pressure_data = c.fetchall()
        # convert the list of tuples to two lists
        tm, pressure = zip(*pressure_data)
        tm1 = list(tm)
        pressure1 = list(pressure)
        c.close()       
        return tm1, pressure1 
 
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
#         data = [random.random() for i in range(25)]
        # group by 60 second interval
        tm, pressure = self._iotHub.query_pressure(1200)
        ax = self.figure.add_subplot(111)
#         ax.plot(data, 'r-')
        ax.plot_date(tm, pressure, 'r-', xdate=True) #(tm, pressure, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.figure.autofmt_xdate()
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