# SMS TO Telegram Channel.

A brief description of the project goes here.

## Overview

This project utilizes Raspberry Pi Pico and SIMCOM A7670C Board to achieve a specific functionality (describe briefly what the project does). The code provided in `main.py` and `A7670C.py` enables the communication between the Raspberry Pi Pico and the SIMCOM A7670C Board using UART communication. The project is designed to (briefly describe the main purpose or functionality of the project).

## Devices Used

- Raspberry Pi Pico - [Raspberry Pi Pico Product Page](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- SIMCOM A7670C Board - [SIMCOM A7670C Product Page](https://www.graylogix.in/product/sim-a7670c-4g-lte-ttl-modem)

## Prerequisites

Make sure you have the following components before running the code:

- Raspberry Pi Pico
- SIMCOM A7670C Board
- `config.json` file containing necessary configuration parameters (ignored by .gitignore)

## How to Use

1. **Setup**

   - Connect Raspberry Pi Pico and SIMCOM A7670C Board according to the provided documentation.
   - Ensure `config.json` file is properly configured with the required parameters.

2. **Running the Code**
   - Upload `main.py` and `A7670C.py` to your Raspberry Pi Pico.
   - Run `main.py` on your Raspberry Pi Pico.

## Configuration

The `config.json` file contains the following parameters:

- `BOT_TOKEN`: Telegram bot token used for communication.
- `CHAT_ID`: Chat ID of the recipient for Telegram messages.
- `BAUDRATE`: Baud rate for UART communication.
- `UART_INTERFACE`: UART interface used for communication.
- `TX_PIN`: Pin number for transmitting data.
- `RX_PIN`: Pin number for receiving data.
- `APN`: Access Point Name for mobile network connection.

## Code Explanation

The `main.py` file contains the main logic of the project. It initializes communication with the SIMCOM A7670C Board, checks for unread SMS messages, sends the messages to a Telegram chat, and deletes the read messages.

The `A7670C.py` file contains the class `A7670C` that handles communication with the SIMCOM A7670C Board using UART.

## Important Notes

- Make sure to handle sensitive information such as API tokens and access credentials securely.
- Ensure proper connections between Raspberry Pi Pico and SIMCOM A7670C Board to avoid communication issues.
- Refer to the official documentation of Raspberry Pi Pico and SIMCOM A7670C Board for detailed setup and troubleshooting.
