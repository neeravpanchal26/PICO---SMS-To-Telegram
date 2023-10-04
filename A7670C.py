from machine import UART, Pin
import utime
import ujson


class A7670C:
    def __init__(self, interface, baudrate, tx, rx):
        self.uart = UART(interface, baudrate=baudrate, bits=8,
                         parity=None, stop=1, tx=Pin(tx), rx=Pin(rx))

    def wait_resp_info(self, timeout=3000):
        prvmills = utime.ticks_ms()
        info = b""
        while (utime.ticks_ms()-prvmills) < timeout:
            if self.uart.any():
                info = b"".join([info, self.uart.read(1)])
        print(info.decode())
        return info

    def Send_command(self, cmd, back, timeout=2000):
        rec_buff = b''
        self.uart.write((cmd+'\r\n').encode())
        prvmills = utime.ticks_ms()
        while (utime.ticks_ms()-prvmills) < timeout:
            if self.uart.any():
                rec_buff = b"".join([rec_buff, self.uart.read(1)])
        if rec_buff != '':
            if back not in rec_buff.decode():
                print(cmd + ' back:\t' + rec_buff.decode())
                return 0
            else:
                print(rec_buff.decode())
                return 1
        else:
            print(cmd + ' no response')

    def Send_command_wait_resp(self, cmd, back, timeout=2000):
        rec_buff = b''
        self.uart.write((cmd + '\r\n').encode())
        prvmills = utime.ticks_ms()
        while (utime.ticks_ms() - prvmills) < timeout:
            if self.uart.any():
                rec_buff = b"".join([rec_buff, self.uart.read(1)])
        if rec_buff != '':
            if back not in rec_buff.decode():
                print(cmd + ' back:\t' + rec_buff.decode())
            else:
                print(rec_buff.decode())
        else:
            print(cmd + ' no response')
        return rec_buff

    def Check_and_start(self):
        while True:
            self.uart.write(bytearray(b'ATE1\r\n'))
            utime.sleep(2)
            self.uart.write(bytearray(b'AT\r\n'))
            rec_temp = self.wait_resp_info()
            if 'OK' in rec_temp.decode():
                print('Pico 4G is ready\r\n' + rec_temp.decode())
                break
            else:
                power = Pin(1, Pin.OUT)
                power.value(1)
                utime.sleep(4)
                power.value(0)
                print('Pico 4G is starting up, please wait...\r\n')
                utime.sleep(4)

    def Network_checking(self):
        for i in range(1, 3):
            print(i)
            if self.Send_command("AT+CGREG?", "0,1") == 1:
                print('A7670C-4G is online\r\n')
                break
            else:
                print('A7670C-4G is offline, please wait...\r\n')
                self.Send_command("AT+CNMP=38", "OK")
                self.Send_command("AT+CMNB=1", "OK")
                self.Send_command("AT+CFUN=1", "OK")
                self.Send_command("AT+CGATT=1", "OK")
                self.Send_command('AT+CGDCONT=1,"IP","JioNet"', "OK")
                self.Send_command('AT+CGEREP=2,1', "OK")
                utime.sleep(2)
                continue

    def post_http(self, apn, post_server, content_type, payload):
        json_data = ujson.dumps(payload)
        data_length = len(json_data)
        self.Check_and_start()
        self.Network_checking()
        self.Send_command('AT+CGDCONT=1,"IP","'+apn+'"', "OK")
        self.Send_command('AT+HTTPINIT', 'OK')
        self.Send_command('AT+HTTPPARA="URL","' + post_server + '"', 'OK')
        self.Send_command('AT+HTTPPARA="CONTENT","' + content_type + '"', 'OK')
        if self.Send_command('AT+HTTPDATA={},8000'.format(data_length), 'DOWNLOAD', 3000):
            self.uart.write(json_data)
            utime.sleep(5)
            rec_buff = self.wait_resp_info()
            if 'OK' in rec_buff.decode():
                print("UART data is read!\n")
            if self.Send_command('AT+HTTPACTION=1', '200', 8000):
                print("POST successfully!\n")
            else:
                print("POST failed\n")
            self.Send_command('AT+HTTPTERM', 'OK')
        else:
            print("failed，please try again!\n")
