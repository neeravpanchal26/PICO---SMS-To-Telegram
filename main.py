from machine import UART, Pin
import time
import ujson

with open('config.json') as config_file:
    config_json = ujson.load(config_file)

# Configure UART
uart = UART(0, baudrate=config_json['BAUDRATE'], tx=Pin(0), rx=Pin(1))


def send_telegram_message(message):
    payload = {
        "chat_id": config_json['CHAT_ID'],
        "text": message,
        "parse_mode": "HTML"
    }
    json_data = ujson.dumps(payload)
    data_length = len(json_data)

    uart.write('AT+CSQ\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+CREG?\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+CGDCONT=1,"IP","'+config_json['APN']+'"\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+CGACT=1,1\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+HTTPINIT\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+HTTPPARA="URL","https://api.telegram.org/bot' +
               config_json['BOT_TOKEN']+'/sendMessage"\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+HTTPPARA="CONTENT","application/json"\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+HTTPDATA={},10000\r\n'.format(data_length))
    time.sleep(2)
    uart.write(json_data)
    time.sleep(2)
    print(response)

    uart.write('AT+HTTPACTION=1\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+HTTPHEAD\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)

    uart.write('AT+HTTPTERM\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)


def read_sms():
    uart.write('AT+CMGF=1\r\n')
    time.sleep(1)
    uart.write('AT+CMGL="REC UNREAD"\r\n')
    time.sleep(2)
    response = uart.read()
    return response


while True:
    sms_response = read_sms()
    sms_messages = sms_response.decode('utf-8').split('+CMGL: ')[1:]
    print(sms_messages)
    for sms_message in sms_messages:
        message_lines = sms_message.split('\r\n')
        number = message_lines[0].split(',')[2].replace('"', '')
        timestamp = message_lines[0].split(',')[4].replace('"', '')
        message = message_lines[1]
        formatted_message = "<b>From:</b> {}\n<b>Time:</b> {}\n<b>Message:</b> {}".format(
            number, timestamp, message)
        send_telegram_message(formatted_message)
        sms_index = message_lines[0].split(',')[0]
        uart.write('AT+CMGD={}\r\n'.format(sms_index))
        time.sleep(1)
    uart.write('AT+CMGD=1,4\r\n')
    time.sleep(2)
    response = uart.read()
    print(response)
    time.sleep(10)
