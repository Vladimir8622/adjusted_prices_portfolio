import okama as ok
import pandas as pd
from datetime import datetime
import time
import requests

# 1. Получаем список всех инструментов MOEX прямым HTTP-запросом

response = requests.get("https://api.okama.io/api/namespaces/MOEX", timeout=30)
response.raise_for_status()
data = response.json()
tickers = pd.DataFrame(data)

print(f"Найдено {len(tickers)} инструментов на MOEX")
# print(tickers)
tickers.columns = tickers.iloc[0].tolist()
tickers = tickers[1:].reset_index(drop=True)

# 2. Фильтруем только акции (опционально — по типу инструмента)
tickers = tickers[tickers['type'] == 'Common Stock']
print((tickers['type']=='Common Stock').all())
names = (tickers['symbol'].to_list())

print(names)
print(len(names))

# 3. Загружаем adjusted-цены для всех тикеров (пачками по N штук)
# Пример вызова
# https://api.okama.io/api/ts/adjusted_close/SBER.MOEX?period=d
# https://api.okama.io/api/ts/adjusted_close/SBER.MOEX?first_date=2026-01-01&last_date=2026-07-05&period=d
batch_size = 30
all_data = []

for i in range(0, len(tickers)):
    


    # Приводим к длинному формату (ticker, date, value)
    df_long = df.stack().reset_index()
    df_long.columns = ['date', 'ticker', 'adjusted_close']
    all_data.append(df_long)

    
    time.sleep(0.5)  # пауза, чтобы не перегружать API

# 4. Объединяем и сохраняем
result = pd.concat(all_data, ignore_index=True)

os.makedirs("data/prices", exist_ok=True)
result.to_csv("data/prices/all_adjusted_prices.csv", index = False)

print(f"Сохранено {len(result)} записей")