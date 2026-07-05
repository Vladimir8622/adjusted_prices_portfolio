import os
import time
import requests
import pandas as pd
import io  # для работы с текстовыми данными

# -----------------------------
# 1. Получаем список всех инструментов MOEX
# -----------------------------
response = requests.get("https://api.okama.io/api/namespaces/MOEX", timeout=30)
response.raise_for_status()
data = response.json()
tickers = pd.DataFrame(data)

print(f"Найдено {len(tickers)} инструментов на MOEX")

# Преобразуем: первая строка – заголовки
tickers.columns = tickers.iloc[0].tolist()
tickers = tickers[1:].reset_index(drop=True)

# -----------------------------
# 2. Фильтруем только акции (Common Stock)
# -----------------------------
tickers = tickers[tickers['type'] == 'Common Stock']
names = tickers['symbol'].to_list()
print(f"Найдено акций: {len(names)}")
print(names[:10])  # покажем первые 10

# -----------------------------
# 3. Переменные для дат (пока абсурдно большие)
# -----------------------------
first_date = "1900-01-01"
last_date  = "2100-01-01"
period = "d"  # дневные данные

# -----------------------------
# 4. Создаём папку для сохранения
# -----------------------------
os.makedirs("data/moex", exist_ok=True)

# -----------------------------
# 5. Загружаем adjusted‑close для каждого тикера
# -----------------------------
for ticker in names:
    symbol = ticker
    url = f"https://api.okama.io/api/ts/adjusted_close/{symbol}"
    params = {
        "first_date": first_date,
        "last_date":  last_date,
        "period":     period
    }
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        
        # Сохраняем полученный CSV в файл
        file_path = f"data/moex/{ticker}.csv"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        
        print(f"✅ Загружено: {ticker}")
    except Exception as e:
        print(f"❌ Ошибка для {ticker}: {e}")
    
    time.sleep(1)  # пауза, чтобы не перегружать API

print("🎉 Все файлы сохранены в data/moex/")