# nuclear_inplay_bot_2025.py - TELEGRAM VERSION
import requests, time, json, numpy as np, pandas as pd
from datetime import datetime
from scipy.stats import poisson
import threading
from bs4 import BeautifulSoup

# === CONFIG (Railway will override these with your variables) ===
API_FOOTBALL_KEY = "YOUR_API_FOOTBALL_KEY"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
CHECK_INTERVAL = 30

def send_telegram(msg):
    if TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_TOKEN":
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
        except: pass

def get_live_fixtures():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-apisports-key': API_FOOTBALL_KEY}
    r = requests.get(url, headers=headers, timeout=15)
    return r.json().get('response', []) if r.status_code == 200 else []

print("NUCLEAR TELEGRAM BOT STARTING...")
send_telegram("NUCLEAR BOT ONLINE\nScanning every live match on Earth...")

while True:
    try:
        fixtures = get_live_fixtures()
        live = [f for f in fixtures if f['fixture']['status']['elapsed'] and 10 <= f['fixture']['status']['elapsed'] <= 89]
        
        if live:
            msg = f"Live Games: {len(live)}\n\n"
            for fix in live[:7]:
                h = fix['teams']['home']['name']
                a = fix['teams']['away']['name']
                score = f"{fix['goals']['home'] or 0}–{fix['goals']['away'] or 0}"
                minute = fix['fixture']['status']['elapsed']
                msg += f"<b>{h} vs {a}</b>\n   {score}  ({minute}')\n\n"
            send_telegram(msg.strip())
        else:
            print(f"{datetime.now().strftime('%H:%M')} – No live games", end='\r')
            
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        send_telegram(f"Error: {e}")
        time.sleep(60)
