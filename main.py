import telebot
import requests
import time
import random
import re
from concurrent.futures import ThreadPoolExecutor

# ⚠️ Apna Bot Token yahan dalein
BOT_TOKEN = "8385538981:AAFiFcdmvuSUr7G_JqWt67fy2EMkkiCmwdU"
bot = telebot.TeleBot(BOT_TOKEN)

# ULTRA HIGH-SPEED PAID HTTP ROTATING ENGINE
PROXY_URL = "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/"
PROXY_DICT = {"http": PROXY_URL, "https": PROXY_URL}

channel_configs = {}
delivered_views_tracker = {}

def get_channel_subscriber_count(chat_id):
    try:
        count = bot.get_chat_member_count(chat_id)
        return count if count > 0 else 1000
    except:
        return 5000  # Fallback baseline

def hit_view_worker(channel_info):
    channel_username, message_id, is_private = channel_info
    
    if is_private:
        clean_id = str(channel_username).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{message_id}?embed=1"
    else:
        clean_username = str(channel_username).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
        
    session = requests.Session()
    session.proxies = PROXY_DICT
    
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120,126)}.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': embed_url,
        'Connection': 'keep-alive'
    }
    
    try:
        # Step 1: Fire base request to catch Telegram cookies & token
        r = session.get(embed_url, headers=headers, timeout=7)
        if r.status_code == 200 and "views" in r.text:
            
            # Extracting the precise view token via regex
            token_match = re.search(r'data-view="([^"]+)"', r.text)
            if token_match:
                token = token_match.group(1)
                ajax_url = f"https://t.me/v/?v={token}"
                
                # Step 2: Injecting required Telegram sub-headers to trick internal validation
                ajax_headers = headers.copy()
                ajax_headers.update({
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': '*/*',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin'
                })
                
                # Step 3: Triggering the final dynamic view credit endpoint
                res = session.get(ajax_url, headers=ajax_headers, timeout=5)
                if res.status_code == 200 and (res.text == "true" or res.text == ""):
                    return True
    except:
        pass
    return False

def fire_percentage_chunk(target_identifier, message_id, is_private, volume, worker_threads=20):
    if volume <= 0:
        return 0
    channel_info = (target_identifier, message_id, is_private)
    success_count = 0
    
    # We increase pool factor slightly to ensure targeted hits clear the proxy gateway
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = [executor.submit(hit_view_worker, channel_info) for _ in range(int(volume * 5))]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= volume:
                    break
    return success_count

@bot.channel_post_handler(func=lambda message: True)
def handle_incoming_signal(message):
    chat_id = message.chat.id
    message_id = message.message_id
    is_private = True if message.chat.username is None else False
    target_identifier = chat_id if is_private else message.chat.username
    
    sub_count = get_channel_subscriber_count(chat_id)
    daily_target_percent = random.uniform(10.0, 15.0) / 100.0
    total_target_views = max(15, int(sub_count * daily_target_percent))
    
    channel_configs[chat_id] = {
        'target_identifier': target_identifier,
        'is_private': is_private,
        'sub_count': sub_count,
        'latest_id': message_id
    }
    
    print(f"📡 [NEW POST] Subs: {sub_count} | Target: {total_target_views} views", flush=True)
    
    # ⏳ 10s Fast Burst
    p1_volume = max(3, int(total_target_views * 0.008))
    sent_p1 = fire_percentage_chunk(target_identifier, message_id, is_private, p1_volume, worker_threads=12)
    print(f"⏱️ [10s Burst] Pushed (+{sent_p1} views)", flush=True)
    time.sleep(12)
    
    # ⏳ 30s Scale-up
    p2_volume = max(4, int(total_target_views * 0.015))
    sent_p2 = fire_percentage_chunk(target_identifier, message_id, is_private, p2_volume, worker_threads=18)
    print(f"⏱️ [30s Scale] Pushed (+{sent_p2} views)", flush=True)
    
    track_key = f"{chat_id}_{message_id}"
    delivered_views_tracker[track_key] = sent_p1 + sent_p2

def night_and_grid_audit_loop():
    while True:
        try:
            for chat_id, config in list(channel_configs.items()):
                latest_id = config['latest_id']
                sub_count = config['sub_count']
                target_id = config['target_identifier']
                is_private = config['is_private']
                
                for msg_id in range(max(1, latest_id - 4), latest_id + 1):
                    track_key = f"{chat_id}_{msg_id}"
                    
                    if msg_id == latest_id:
                        target_ratio = random.uniform(10.0, 15.0) / 100.0
                    else:
                        target_ratio = random.uniform(20.0, 25.0) / 100.0
                        
                    calculated_cap = max(20, int(sub_count * target_ratio))
                    current_done = delivered_views_tracker.get(track_key, 0)
                    
                    if current_done >= calculated_cap:
                        continue
                        
                    chunk_size = random.randint(25, 50)
                    if current_done + chunk_size > calculated_cap:
                        chunk_size = calculated_cap - current_done
                        
                    sent = fire_percentage_chunk(target_id, msg_id, is_private, chunk_size, worker_threads=15)
                    delivered_views_tracker[track_key] = current_done + sent
                    print(f"📊 [Grid Sync] Msg {msg_id} -> Status: [{delivered_views_tracker[track_key]}/{calculated_cap}]", flush=True)
                    time.sleep(4)
        except Exception as e:
            print(f"⚠️ Grid error: {e}", flush=True)
        time.sleep(20)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v7.0 (Session-Emulated Core Live)", flush=True)
    print("======================================================", flush=True)
    
    try:
        bot.remove_webhook()
        time.sleep(2)
        bot.set_webhook(url="https://localhost/fake-webhook-to-kill-polling")
        print("🧹 Dynamic anti-conflict patch maintained.", flush=True)
    except Exception as e:
        print(f"⚠️ Session reset note: {e}", flush=True)

    import threading
    audit_thread = threading.Thread(target=night_and_grid_audit_loop, daemon=True)
    audit_thread.start()
    
    while True:
        try:
            updates = bot.get_updates(offset=-1, timeout=10)
            if updates:
                bot.process_new_updates(updates)
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    main()
    
