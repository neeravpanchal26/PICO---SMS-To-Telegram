import machine
import time
import urequests

# Configure UART for communication with SIM800L
uart = machine.UART(0, baudrate=9600, tx=0, rx=1)  # Pico GP0 (TX) to SIM800L RX, Pico GP1 (RX) to SIM800L TX

# Initialize SIM800L
def init_sim800l():
    uart.write("AT\r\n")
    response = uart.read()
    if b'OK' in response:
        print("SIM800L initialized successfully.")
    else:
        print("SIM800L initialization failed.")
        return False

# Read SMS
def read_sms():
    uart.write("AT+CMGF=1\r\n")  # Set SMS text mode
    time.sleep(1)
    uart.write("AT+CMGL=\"REC UNREAD\"\r\n")  # List unread messages
    response = uart.read()
    return response

# Send SMS content to Telegram bot
def send_to_telegram_bot(message):
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = urequests.post(url, json=payload, timeout=30)  # Adjust the timeout as needed
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except Exception as e:
        print("Error sending message to Telegram:", str(e))
        return False

# Mark SMS as read
def mark_sms_as_read():
    uart.write("AT+CMGDA=\"DEL READ\"\r\n")
    time.sleep(1)

# Main loop
def main():
    init_sim800l()
    
    while True:
        sms_data = read_sms()
        if sms_data:
            # Extract SMS content from response
            # You need to parse the response according to the AT command response format
            sms_content = ...  # Extract the SMS content
            
            if sms_content:
                if send_to_telegram_bot(sms_content):
                    print("SMS forwarded to Telegram bot.")
                    mark_sms_as_read()
                else:
                    print("Failed to forward SMS to Telegram bot.")
            
        time.sleep(30)  # Delay before checking for new SMS messages

if __name__ == "__main__":
    main()
