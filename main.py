import telebot
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

# ⚠️ Apna Bot Token yahan dalein
BOT_TOKEN = "7818601229:AAHzgOQYaAulQ_GsB8YdZbzjWLW_a48Y974"
bot = telebot.TeleBot(BOT_TOKEN)

# ULTRA HIGH-SPEED PAID HTTP ROTATING ENGINE
PROXY_URL = "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/"
PROXY_DICT = {
    "http": PROXY_URL,
    "https": PROXY_URL
}

def hit_view_worker(channel_info):
    channel_username, message_id, is_private = channel_info
    
    # Base URL switching logic based on privacy status
    if is_private:
        clean_id = str(channel_username).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{message_id}?embed=1"
    else:
        clean_username = str(channel_username).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
        
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(534,603)}.{random.randint(1,50)} (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': f'https://t.me/s/{str(channel_username).replace("@","")}' if not is_private else 'https://t.me/',
        'Connection': 'keep-alive'
    }
    
    try:
        # Step 1: Fire to main embed endpoint
        r = requests.get(embed_url, proxies=PROXY_DICT, headers=headers, timeout=5)
        
        # Step 2: Extract base telegram context token if needed
        if r.status_code == 200 and "views" in r.text:
            if "data-view" in r.text:
                # Force extract view token session if telegram requests verification
                try:
                    token = r.text.split('data-view="')[1].split('"')[0]
                    ajax_url = f"https://t.me/v/?v={token}"
                    requests.get(ajax_url, proxies=PROXY_DICT, headers=headers, timeout=3)
                except:
                    pass
            return True
    except:
        pass
    return False

def fire_fast_views(channel_username, message_id, target_views, is_private=False, threads=40):
    success_count = 0
    channel_info = (channel_username, message_id, is_private)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # We overshoot the loop to bypass high proxy failure/drop rates
        futures = [executor.submit(hit_view_worker, channel_info) for _ in range(target_views * 3)]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= target_views:
                    break
    return success_count

@bot.channel_post_handler(func=lambda message: True)
def handle_new_post(message):
    chat_id = message.chat.id
    message_id = message.message_id
    channel_name = message.chat.username or message.chat.title
    
    # Determine privacy protocol
    is_private = True if message.chat.username is None else False
    target_identifier = chat_id if is_private else message.chat.username
    
    print(f"🚨 BOT TRIGGERED: New post in [{channel_name}] (ID: {message_id}) | Private: {is_private}", flush=True)
    print("⚡ Pumping force views via Smart Token Fallback...", flush=True)
    
    # Phase 1: Heavy Instant Boost
    sent = fire_fast_views(target_identifier, message_id, 150, is_private=is_private, threads=45)
    print(f"💥 Session 1 Complete: Delivered {sent} views to {channel_name}.", flush=True)
    
    # Phase 2: Smooth Balancing (Drip-feed over 10 seconds)
    time.sleep(5)
    sent_secondary = fire_fast_views(target_identifier, message_id, 200, is_private=is_private, threads=25)
    print(f"📈 Session 2 Complete: Added +{sent_secondary} drip views.", flush=True)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v4.0 (Smart Token Fallback LIVE)", flush=True)
    print("======================================================", flush=True)
    
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            print(f"⚠️ Glitch detected: {e}. Re-booting socket...", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
            
