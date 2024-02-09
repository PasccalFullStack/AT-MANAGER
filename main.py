__author__ = 'Pascal COSTA'
__website__ = 'www.pascalcosta.fr'
__creationDate__ = '2024-02-05'
__license__ = 'free'

import sys, os, serial, serial.tools.list_ports
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from SerialReader import SerialReader
from ButtonsMethod import ButtonsMethod

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll
    myappid = 'AT-MANAGER'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class qt(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('ATmanag.ui', self)
    
        self.ret_carr = self.ret_line = False
        self.buts = ButtonsMethod(
            self.new_data_value,
            self.active_ret_carr,
            self.active_ret_line,
            self.send_data,
            self.ret_carr,
            self.ret_line
        )
        self.thread = None
        self.serialReader = None
        self.start_com.clicked.connect(self.start_loop)
        self.stop_com.clicked.connect(self.stop_loop)
        self.send_but.clicked.connect(self.send_data)
        self.baudrate_selector.currentIndexChanged.connect(self.get_baudrate)
        self.active_ret_carr.clicked.connect(self.change_ret_carr)
        self.active_ret_line.clicked.connect(self.change_ret_line)
        self.send_at.clicked.connect(self.buts.send_AT)
        self.send_at_name.clicked.connect(self.buts.send_ATNAME)
        self.send_at_addr.clicked.connect(self.buts.send_ATADDR)
        self.send_at_version.clicked.connect(self.buts.send_ATVERSION)
        self.send_at_uart.clicked.connect(self.buts.send_ATUART)
        self.send_at_password.clicked.connect(self.buts.send_ATPSWD)
        self.write_at_name.clicked.connect(self.buts.write_ATNAME)
        self.write_at_uart.clicked.connect(self.buts.write_ATUART)
        self.write_at_pswd.clicked.connect(self.buts.write_ATPSWD)
        self.write_reset.clicked.connect(self.buts.write_RESET)
        self.port = 'none'
        self.baudrate = 9600
        self.ser = False
        self.text_in_prepa = ''
    
    def change_ret_carr(self):
        self.ret_carr = self.buts.set_carr()
    
    def change_ret_line(self):
        self.ret_line = self.buts.set_line()
    
    def get_baudrate(self):
        self.baudrate = int(self.baudrate_selector.currentText())

    def search_port_com(self):
        for p in serial.tools.list_ports.comports():
            if 'CP21' in p.description:
                self.port = p.device
                self.connection_status_label.setText("CONNECTED!")
                self.start_com.setStyleSheet(
                    'font-size: 14px;'
                    'color: black;'
                    'background-color: lightgreen;'
                )
                self.stop_com.setStyleSheet(
                    'font-size: 14px;'
                    'color: black;'
                    'background-color: grey;'
                )
                self.connection_status_label.setStyleSheet(
                    'font-size: 20px;'
                    'color: lightgreen;'
                    'background-color: black;'
                )
                tp = str(datetime.now())
                self.receive_box.setText(
                    tp[11:-7] + \
                    " >>> Connected to " + self.port + \
                    ", baudrate = " + str(self.baudrate) + " bauds"
                )
            else:
                self.port = 'NONE'

        self.port_com_label.setText(self.port)

    def start_loop(self):
        self.search_port_com()
        try:
            mytext = "\n"
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.ser.write(mytext.encode())
        except:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("COM Port Error!")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No port COM available")
            msgBox.exec()
            self.init_connection()
            return

        self.serialReader = SerialReader(self.ser)
        self.thread = QThread()
        self.serialReader.moveToThread(self.thread)
        self.thread.started.connect(self.serialReader.work)
        self.serialReader.intReady.connect(self.emit_data)
        self.serialReader.finished.connect(self.thread.quit)
        self.serialReader.finished.connect(self.serialReader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def stop_loop(self):
        if self.ser.isOpen():
            self.ser.close()
            self.serialReader.working = False
            self.init_connection()
            self.port = 'none'
            
    def init_connection(self):
        self.connection_status_label.setText("Not Connected")
        self.start_com.setStyleSheet(
            'font-size: 14px;'
            'color: black;'
            'background-color: grey;'
        )
        self.stop_com.setStyleSheet(
            'font-size: 14px;'
            'color: black;'
            'background-color: #F66D62;'
        )
        self.connection_status_label.setStyleSheet(
            'font-size: 20px;'
            'color: red;'
            'background-color: black;'
        )
        self.port_com_label.setText('COM ???')

    def send_data(self):
        message = self.new_data_value.toPlainText()
        if self.text_in_prepa != '':
            message = self.text_in_prepa
        if self.ret_carr:
            message += "\r"
        if self.ret_line:
            message += "\n"
        self.emit_data('Send : ' + message +  "\n")
        try:
            self.ser.write(message.encode())
            self.new_data_value.clear()
            self.text_in_prepa = ''
        except:
            self.emit_data('Erreur, envoi impossible!' + "\n")

    def emit_data(self, i):
        if i != '':
            tp = str(datetime.now())
            cursor = QtGui.QTextCursor(self.receive_box.document())
            self.receive_box.setTextCursor(cursor)
            self.receive_box.insertPlainText(
                tp[11:-7] + ' >>> ' + "{}".format(i))


def run():
    app = QApplication(sys.argv)
    widget = qt()
    widget.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'favicon.ico')))
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
