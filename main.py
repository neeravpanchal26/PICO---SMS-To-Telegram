import A7670C
import time
import ujson


class Main:
    def __init__(self, config_file_path='config.json'):
        with open(config_file_path) as config_file:
            self.config_json = ujson.load(config_file)

        self.simcom = A7670C.A7670C(
            self.config_json['UART_INTERFACE'],
            self.config_json['BAUDRATE'],
            self.config_json['TX_PIN'],
            self.config_json['RX_PIN'])

        while True:
            self.simcom.Check_and_start()
            self.simcom.Network_checking()

            self.simcom.Send_command('AT+CMGF=1', 'OK')
            self.simcom.uart.write(bytearray(b'AT+CMGL="REC UNREAD"\r\n'))
            sms_response = self.simcom.wait_resp_info()
            sms_messages = sms_response.decode('utf-8').split('+CMGL: ')[1:]
            print(sms_messages)

            for sms_message in sms_messages:
                message_lines = sms_message.split('\r\n')
                timestamp = message_lines[0].split(',')[4].replace('"', '')
                message = message_lines[1]

                payload = {
                    "chat_id": self.config_json['CHAT_ID'],
                    "text": "<b>Time: </b>{}\r\n<b>Message: </b>{}".format(
                        timestamp, message),
                    "parse_mode": "HTML"
                }

                self.simcom.post_http(self.config_json['APN'], 'https://api.telegram.org/bot' +
                                      self.config_json['BOT_TOKEN'] + '/sendMessage', 'application/json', payload)

                sms_index = message_lines[0].split(',')[0]
                self.simcom.Send_command('AT+CMGD={}'.format(sms_index), 'OK')

            self.simcom.Send_command('AT+CMGD=1,4', 'OK')
            time.sleep(10)


if __name__ == "__main__":
    Main()
