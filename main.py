import yfinance as yf
import pandas_ta as ta
import requests
import time

# بياناتك
TOKEN = "8721841884:AAEf944fZYf7ESHnGIzFRchyD_VaduyjflY"
CHAT_ID = "8238827370"

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

print("🚀 البوت بدأ العمل الآن...")
send_signal("✅ تم تشغيل البوت بنجاح على GitHub Actions!")

while True:
    try:
        data = yf.download(tickers='EURUSD=X', period='1d', interval='1m', progress=False)
        if not data.empty:
            df = data.copy()
            df['rsi'] = ta.rsi(df['Close'], length=14)
            df['ema200'] = ta.ema(df['Close'], length=200)
            
            last_price = df['Close'].iloc[-1]
            if last_price > df['ema200'].iloc[-1] and df['rsi'].iloc[-1] < 35:
                send_signal(f"🟢 *شراء (CALL)*\nالسعر: {last_price:.5f}")
                time.sleep(120)
            elif last_price < df['ema200'].iloc[-1] and df['rsi'].iloc[-1] > 65:
                send_signal(f"🔴 *بيع (PUT)*\nالسعر: {last_price:.5f}")
                time.sleep(120)
        time.sleep(30)
    except:
        time.sleep(10)
