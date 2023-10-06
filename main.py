import A7600X
from time import sleep
import ujson


class Main:
    def __init__(self, config_file_path='config.json'):
        with open(config_file_path) as config_file:
            self.config_json = ujson.load(config_file)

        self.gsm = A7600X.A7600X(self.config_json['UART_INTERFACE'],
                                 self.config_json['BAUDRATE'],
                                 self.config_json['TX_PIN'],
                                 self.config_json['RX_PIN'])

        self.telegram_url = 'https://api.telegram.org/bot' + \
            self.config_json['BOT_TOKEN'] + '/sendMessage'
        self.http_type = 'application/json'

        sleep(10)
        response = self.gsm._exe_command('AT')
        response += self.gsm._exe_command('ATE')
        response += self.gsm._exe_command('ATI')
        response += self.gsm._exe_command('AT+CIMI')
        response += self.gsm._exe_command('AT+CNUM')
        response += self.gsm._exe_command('AT+COPS?')
        response += self.gsm._exe_command('AT+CPIN?')
        self.gsm._http_post(
            self.telegram_url,
            self.http_type,
            self._telegram_payload(response))

        while True:
            self.gsm._exe_command('AT+CMGF=1')
            sms_response = self.gsm._exe_command('AT+CMGL="REC UNREAD"')
            sms_messages = sms_response.decode('utf-8').split('+CMGL: ')[1:]
            print(sms_messages)
            for sms_message in sms_messages:
                message_lines = sms_message.split('\r\n')
                timestamp = message_lines[0].split(',')[4].replace('"', '')
                message = message_lines[1]
                formatted_message = "<b>Time: </b>{}\r\n<b>Message: </b>{}".format(
                    timestamp, message)
                self.gsm._http_post(
                    self.telegram_url,
                    self.http_type,
                    self._telegram_payload(formatted_message))
                sms_index = message_lines[0].split(',')[0]
                self.gsm._exe_command('AT+CMGD={}'.format(sms_index))
                sleep(1)
            self.gsm._exe_command('AT+CMGD=1,4')
            sleep(10)

    def _telegram_payload(self, message):
        payload = {
            "chat_id": self.config_json['CHAT_ID'],
            "text": message,
            "parse_mode": "HTML"
        }
        return payload


if __name__ == "__main__":
    Main()
