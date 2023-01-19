import sys

#from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import *
#pyqtSignal, QThread, QObject, QTimer

class SerialWork(QObject):
    def __init__(self):
        super().__init__()

#    def init(self):
        self.com = QSerialPort()
        self.com.setPortName('/dev/pts/4')
        self.com.setBaudRate(115200)

        if self.com.open(QSerialPort.ReadWrite) == False:
            return

        self.readtimer = QTimer()
        self.readtimer.timeout.connect(self.readData)
        self.readtimer.start(100)

    def readData(self):
        revData = self.com.readAll()
        revData = bytes(revData)
        if len(revData) > 0:
            print('%d read' % len(revData))

class PyQt_Serial(QObject):
    def __init__(self):
        super().__init__()

        self.serialthread = QThread()
        self.serialwork = SerialWork()
        self.serialwork.moveToThread(self.serialthread)
        self.serialthread.started.connect(self.serialwork.init)

        self.serialthread.start()

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    win = SerialWork()
#    win = PyQt_Serial()
#    win.show()
    sys.exit(app.exec_())
