# Raspberry Pi Pico GSM SMS Receiver

This project demonstrates how to receive SMS messages using a Raspberry Pi Pico and a GSM module. The code provided here allows you to interact with a GSM module (A7670C) and receive SMS messages. The received messages are then sent to a specified Telegram chat using the Telegram Bot API.

## Prerequisites
- [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [GSM Board (A7670C)](https://www.graylogix.in/product/sim-a7670c-4g-lte-ttl-modem)

## Configuration
Create a `config.json` file in the project directory with the following content (replace the placeholder values with actual values, omit confidential values):

```json
{
	"BOT_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
	"CHAT_ID": "YOUR_TELEGRAM_CHAT_ID",
	"BAUDRATE": 115200,
	"UART_INTERFACE": 0,
	"TX_PIN": 0,
	"RX_PIN": 1,
	"APN": "YOUR_APN_NAME"
}
```

- `BOT_TOKEN`: Your Telegram Bot token obtained from the BotFather.
- `CHAT_ID`: The chat ID of the Telegram chat where you want to receive SMS notifications.
- `BAUDRATE`: Baud rate for UART communication with the GSM module (e.g., 115200).
- `UART_INTERFACE`: UART interface number on the Raspberry Pi Pico (e.g., 0 for UART0).
- `TX_PIN`: GPIO pin used for transmitting data to the GSM module.
- `RX_PIN`: GPIO pin used for receiving data from the GSM module.
- `APN`: Access Point Name for your mobile network provider (e.g., "JioNet" for Jio network).

## How it Works
1. The `A7670C.py` module provides a Python class `A7670C` that communicates with the GSM module via UART. It includes methods to execute AT commands, perform HTTP POST requests, and handle GSM responses.

2. The `main.py` script initializes the GSM module and continuously checks for unread SMS messages. When a new SMS is received, it is formatted and sent to the specified Telegram chat using the Telegram Bot API.

## Setup
1. Connect the Raspberry Pi Pico to the GSM module (A7670C) using appropriate wiring for UART communication (TX, RX pins).
2. Configure the `config.json` file with the necessary parameters as described above.

## Usage
`main.py` script to start the SMS receiver. The script will continuously check for new SMS messages and send them to the specified Telegram chat in real-time.

**Note:** Ensure that you have internet connectivity and the necessary permissions for sending SMS and accessing the Telegram API.

Feel free to contribute and open issues if you encounter any problems. Happy coding!
