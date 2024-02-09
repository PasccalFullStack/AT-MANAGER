__author__ = 'Pascal COSTA'
__website__ = 'www.pascalcosta.fr'
__creationDate__ = '2024-02-05'
__license__ = 'free'

import time
from PyQt5.QtCore import *

class SerialReader(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    def __init__(self, ser):
        super(SerialReader, self).__init__()
        self.working = True
        self.ser = ser

    def work(self):
        while self.working:
            if self.ser.isOpen():
                try:
                    line = self.ser.readline().decode('utf-8')
                except:
                    pass
            else:
                line = ''

            if line != '':
                time.sleep(0.1)
                self.intReady.emit(line)

        self.finished.emit()