import telebot
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

# ⚠️ Apna Bot Token yahan dalein jo BotFather se milega
BOT_TOKEN = "7818601229:AAHzgOQYaAulQ_GsB8YdZbzjWLW_a48Y974"
bot = telebot.TeleBot(BOT_TOKEN)

# ULTRA HIGH-SPEED PAID HTTP ROTATING ENGINE
PROXY_URL = "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/"
PROXY_DICT = {
    "http": PROXY_URL,
    "https": PROXY_URL
}

# Channels ko track karne ke liye memory pool
channel_history_tracker = {}

def hit_view_worker(channel_username, message_id):
    """Paid Premium Request Fire Unit"""
    # Agar channel private hai to username '-100xxxxxx' form mein hota hai, uski link alag banti hai
    clean_username = str(channel_username).replace("-100", "c/") if str(channel_username).startswith("-100") else channel_username
    
    embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(530,600)}.36',
        'Connection': 'close'
    }
    try:
        r = requests.get(embed_url, proxies=PROXY_DICT, headers=headers, timeout=4)
        if r.status_code == 200 and "views" in r.text:
            return True
    except:
        pass
    return False

def fire_fast_views(channel_username, message_id, target_views, threads=35):
    """Parallel Thread Processing"""
    success_count = 0
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(hit_view_worker, channel_username, message_id) for _ in range(target_views * 2)]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= target_views:
                    break
    return success_count

# 🚨 TRIGGER: Bot jis channel mein bhi admin hoga, wahan nayi post aate hi yeh function automatic chalaiga
@bot.channel_post_handler(func=lambda message: True)
def handle_new_post(message):
    chat_id = message.chat.id
    message_id = message.message_id
    channel_name = message.chat.username or message.chat.title
    
    print(f"🚨 NEW POST DETECTED via Bot in [{channel_name}] (ID: {message_id})", flush=True)
    print("⚡ Launching Premium Bot Blast...", flush=True)
    
    # Target structure allocation
    target_username = message.chat.username if message.chat.username else message.chat.id
    
    # Phase 1: Instant Views Delivery
    sent = fire_fast_views(target_username, message_id, 70, threads=40)
    print(f"💥 Delivered {sent} views instantly to {channel_name} post {message_id}.", flush=True)
    
    # Background momentum loops (Optional balancing)
    time.sleep(2)
    fire_fast_views(target_username, message_id, 150, threads=15)

def main():
    print("======================================================", flush=True)
    print("🤖 MULTI-CHANNEL SMART TELEGRAM BOT ENGINE LIVE", flush=True)
    print("🛡️ Private Channels & Multi-User Support Enabled")
    print("======================================================", flush=True)
    
    # Bot polling start (Render par hamesha live rahega aur events sunta rahega)
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            print(f"⚠️ Bot network glitch, restarting socket... Error: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
    
