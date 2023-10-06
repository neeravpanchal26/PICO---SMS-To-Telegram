from machine import UART, Pin
from time import sleep
import ujson


class A7600X:
    def __init__(self, interface, baudrate, txpin, rxpin):
        self.uart = UART(interface,
                         baudrate=baudrate,
                         bits=8,
                         parity=None,
                         stop=1,
                         tx=Pin(txpin),
                         rx=Pin(rxpin))

    def _exe_command(self, command):
        self.uart.write(command+'\r\n')
        sleep(2)
        response = self.uart.read()
        print(response.decode('utf-8'))
        return response

    def _http_post(self, url, type, data):
        json_data = ujson.dumps(data)
        data_length = len(json_data)

        uart_commands = [
            'AT+HTTPINIT',
            'AT+HTTPPARA="URL","' + url + '"',
            'AT+HTTPPARA="CONTENT","' + type + '"',
            'AT+HTTPDATA={},10000'.format(data_length),
            json_data,
            'AT+HTTPACTION=1',
            'AT+HTTPHEAD',
            'AT+HTTPTERM'
        ]

        for command in uart_commands:
            self._exe_command(command)
