import asyncio
import websockets
import json
from collections import deque
import numpy as np
import datetime

# Set your parameters here
MINIMUM_VOLUME = 10
WINDOW_SIZE = 1000  # Number of recent trades to consider
RECONNECT_DELAY = 5  # Delay in seconds before attempting to reconnect

# Global variables
buy_volumes = deque(maxlen=WINDOW_SIZE)
sell_volumes = deque(maxlen=WINDOW_SIZE)

def check_power():
    avg_buy_volume = np.mean(buy_volumes) if buy_volumes else 0
    avg_sell_volume = np.mean(sell_volumes) if sell_volumes else 0
    num_big_buyers = sum(v >= MINIMUM_VOLUME for v in buy_volumes)
    num_big_sellers = sum(v >= MINIMUM_VOLUME for v in sell_volumes)

    if avg_buy_volume > avg_sell_volume and num_big_buyers > num_big_sellers:
        print(datetime.datetime.now())
        print("Buyers are more powerful")
    elif avg_buy_volume < avg_sell_volume and num_big_buyers < num_big_sellers:
        print(datetime.datetime.now())
        print("Sellers are more powerful")

async def handle_socket():
    uri = "wss://fstream.binance.com/ws/btcusdt@trade"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket")
                while True:
                    data = await websocket.recv()
                    trade = json.loads(data)
                    trade_volume = float(trade['q'])
                    is_buyer_maker = trade['m']

                    if is_buyer_maker:
                        sell_volumes.append(trade_volume)
                    else:
                        buy_volumes.append(trade_volume)

                    check_power()
        except (websockets.ConnectionClosed, websockets.InvalidStatusCode) as e:
            print(f"Connection error: {e}. Reconnecting in {RECONNECT_DELAY} seconds...")
            await asyncio.sleep(RECONNECT_DELAY)
        except Exception as e:
            print(f"Unexpected error: {e}. Reconnecting in {RECONNECT_DELAY} seconds...")
            await asyncio.sleep(RECONNECT_DELAY)

async def main():
    await handle_socket()

if __name__ == "__main__":
    asyncio.run(main())
