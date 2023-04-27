import json
import websocket
import ssl

def on_open(ws):
    print("WebSocket подключен")

def on_message(ws, message):
    raw_data = json.loads(message)
    
    if 'data' not in raw_data:
        print("Необработанное сообщение:", raw_data)
        return

    data = raw_data['data']
    symbol = data['s']
    bids = data['b']
    asks = data['a']

    print(f"Обновление стакана заявок для {symbol}:")

    print("Лучшие заявки на покупку:")
    for bid in bids[:1]:
        print(f"Цена: {bid[0]}, объем: {bid[1]}")

    print("\nЛучшие заявки на продажу:")
    for ask in asks[:1]:
        print(f"Цена: {ask[0]}, объем: {ask[1]}")

    print("\n")

def on_error(ws, error):
    print(f"WebSocket ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket отключен. Код закрытия: {close_status_code}, Сообщение: {close_msg}")

def main():
    symbols = ["btcusdt", "xrpusdt", "etcusdt", "ltcusdt", "eosusdt", "solusdt", "nearusdt", "maticusdt"]

    streams = "/".join([f"{symbol.lower()}@depth5" for symbol in symbols])
    websocket_url = f"wss://fstream.binance.com/stream?streams={streams}"

    ws = websocket.WebSocketApp(
        websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == "__main__":
    main()

