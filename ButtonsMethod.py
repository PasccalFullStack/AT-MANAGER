__author__ = 'Pascal COSTA'
__website__ = 'www.pascalcosta.fr'
__creationDate__ = '2024-02-05'
__license__ = 'free'

class ButtonsMethod():
    def __init__(
            self,
            new_data_value,
            active_ret_carr,
            active_ret_line,
            send_data,
            ret_carr,
            ret_line
        ):
        super(ButtonsMethod, self).__init__()
        self.new_data_value = new_data_value
        self.active_ret_carr = active_ret_carr
        self.active_ret_line = active_ret_line
        self.send_data = send_data
        self.ret_carr = ret_carr
        self.ret_line = ret_line
        self.enabled_button_style = (
                'font-size: 16px;'
                'background-color: lightgreen;'
                'color: black;'
            )
        self.disabled_button_style = (
                'font-size: 16px;'
                'background-color: #FC7F7F;'
                'color: black;'
            )
        
    def send_AT(self):
        self.text_in_prepa = 'AT'
        self.new_data_value.setPlainText('AT')
        self.send_data()

    def send_ATNAME(self):
        self.text_in_prepa = 'AT+NAME?'
        self.new_data_value.setPlainText('AT+NAME?')
        self.send_data()

    def send_ATADDR(self):
        self.text_in_prepa = 'AT+ADDR?'
        self.new_data_value.setPlainText('AT+ADDR?')
        self.send_data()

    def send_ATVERSION(self):
        self.text_in_prepa = 'AT+VERSION?'
        self.new_data_value.setPlainText('AT+VERSION?')
        self.send_data()

    def send_ATUART(self):
        self.text_in_prepa = 'AT+UART?'
        self.new_data_value.setPlainText('AT+UART?')
        self.send_data()

    def send_ATPSWD(self):
        self.text_in_prepa = 'AT+PSWD?'
        self.new_data_value.setPlainText('AT+PSWD?')
        self.send_data()

    def write_ATNAME(self):
        self.new_data_value.setPlainText('AT+NAME=')

    def write_ATUART(self):
        self.new_data_value.setPlainText('AT+UART=')

    def write_ATPSWD(self):
        self.new_data_value.setPlainText('AT+PSWD=')

    def write_RESET(self):
        self.new_data_value.clear()
        
    def set_carr(self):
        self.ret_carr = not self.ret_carr
        if self.ret_carr:
            self.active_ret_carr.setStyleSheet(
                self.enabled_button_style
            )
        else:
            self.active_ret_carr.setStyleSheet(
                self.disabled_button_style
                )
        return self.ret_carr

    def set_line(self):
        self.ret_line = not self.ret_line
        if self.ret_line:
            self.active_ret_line.setStyleSheet(
                self.enabled_button_style
            )
        else:
            self.active_ret_line.setStyleSheet(
                self.disabled_button_style
            )
        return self.ret_line