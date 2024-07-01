# Binance Futures WebSocket Trade Monitor

This Python script connects to the Binance Futures WebSocket to monitor trades and determine whether buyers or sellers are more powerful based on trade volumes. The script calculates the average buy and sell volumes and the number of large trades to provide insights into market dynamics.

## Features

- Connects to Binance Futures WebSocket for real-time trade data.
- Monitors trade volumes to determine buyer and seller power.
- Automatically reconnects if the WebSocket connection is lost.
- Configurable parameters for minimum volume and window size for trade monitoring.

## Requirements

- Python 3.7+
- `websockets` library
- `aiohttp` library
- `numpy` library
