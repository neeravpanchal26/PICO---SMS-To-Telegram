from machine import UART, Pin
import time
import ujson


class UARTCommunicator:
    def __init__(self, config_file_path='config.json'):
        with open(config_file_path) as config_file:
            self.config_json = ujson.load(config_file)
        self.uart = UART(
            0, baudrate=self.config_json['BAUDRATE'], bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

        time.sleep(10)
        response = self._exe_command('AT\r\n')
        response += self._exe_command('ATE\r\n')
        response += self._exe_command('ATI\r\n')
        response += self._exe_command('AT+CIMI\r\n')
        response += self._exe_command('AT+CNUM\r\n')
        response += self._exe_command('AT+COPS?\r\n')
        self.send_telegram_message(response)

        while True:
            sms_response = self.read_sms()
            sms_messages = sms_response.decode('utf-8').split('+CMGL: ')[1:]
            print(sms_messages)
            for sms_message in sms_messages:
                message_lines = sms_message.split('\r\n')
                timestamp = message_lines[0].split(',')[4].replace('"', '')
                message = message_lines[1]
                formatted_message = "<b>Time: </b>{}\r\n<b>Message: </b>{}".format(
                    timestamp, message)
                self.send_telegram_message(formatted_message)
                sms_index = message_lines[0].split(',')[0]
                self.uart.write(
                    'AT+CMGD={}\r\n'.format(sms_index))
                time.sleep(1)
            self._exe_command('AT+CMGD=1,4\r\n')
            time.sleep(10)

    def _exe_command(self, command):
        self.uart.write(command)
        time.sleep(2)
        response = self.uart.read()
        print(response.decode('utf-8'))
        return response

    def send_telegram_message(self, message):
        payload = {
            "chat_id": self.config_json['CHAT_ID'],
            "text": message,
            "parse_mode": "HTML"
        }
        json_data = ujson.dumps(payload)
        data_length = len(json_data)

        uart_commands = [
            'AT+HTTPINIT\r\n',
            'AT+HTTPPARA="URL","https://api.telegram.org/bot' +
            self.config_json['BOT_TOKEN'] + '/sendMessage"\r\n',
            'AT+HTTPPARA="CONTENT","application/json"\r\n',
            'AT+HTTPDATA={},10000\r\n'.format(data_length),
            json_data,
            'AT+HTTPACTION=1\r\n',
            'AT+HTTPHEAD\r\n',
            'AT+HTTPTERM\r\n'
        ]

        for command in uart_commands:
            self._exe_command(command)

    def read_sms(self):
        self._exe_command('AT+CMGF=1\r\n')
        return self._exe_command('AT+CMGL="REC UNREAD"\r\n')


if __name__ == "__main__":
    UARTCommunicator()

