import telebot
import requests
import time
import random
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
        
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(118,124)}.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    try:
        r = requests.get(embed_url, proxies=PROXY_DICT, headers=headers, timeout=5)
        if r.status_code == 200 and "views" in r.text and "Post not found" not in r.text:
            if 'data-view="' in r.text:
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

def fire_percentage_chunk(target_identifier, message_id, is_private, volume, worker_threads=20):
    if volume <= 0:
        return 0
    channel_info = (target_identifier, message_id, is_private)
    success_count = 0
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = [executor.submit(hit_view_worker, channel_info) for _ in range(int(volume * 4))]
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
    
    print(f"📡 [NEW POST DETECTED] Subs: {sub_count} | Target: {total_target_views} views", flush=True)
    
    # ⏳ 10s Stamp (0.5%)
    p1_volume = max(2, int(total_target_views * 0.005))
    sent_p1 = fire_percentage_chunk(target_identifier, message_id, is_private, p1_volume, worker_threads=10)
    print(f"⏱️ [10s Stamp] Pushed burst (+{sent_p1} views)", flush=True)
    time.sleep(15)
    
    # ⏳ 30s Stamp (1%)
    p2_volume = max(3, int(total_target_views * 0.01))
    sent_p2 = fire_percentage_chunk(target_identifier, message_id, is_private, p2_volume, worker_threads=15)
    print(f"⏱️ [30s Stamp] Pushed momentum (+{sent_p2} views)", flush=True)
    
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
                        
                    chunk_size = random.randint(20, 45)
                    if current_done + chunk_size > calculated_cap:
                        chunk_size = calculated_cap - current_done
                        
                    sent = fire_percentage_chunk(target_id, msg_id, is_private, chunk_size, worker_threads=15)
                    delivered_views_tracker[track_key] = current_done + sent
                    print(f"📊 [Grid Sync] Msg {msg_id} -> Status: [{delivered_views_tracker[track_key]}/{calculated_cap}]", flush=True)
                    time.sleep(3)
        except Exception as e:
            print(f"⚠️ Grid error: {e}", flush=True)
        time.sleep(15)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v6.0 (Zero-Polling Anti-Conflict LIVE)", flush=True)
    print("======================================================", flush=True)
    
    # FORCED RESET: Removing previous webhooks and clearing old stuck polling logs
    try:
        bot.remove_webhook()
        time.sleep(2)
        # Setting a fake webhook fixes conflict 409 forever by shutting down internal polling mechanics
        bot.set_webhook(url="https://localhost/fake-webhook-to-kill-polling")
        print("🧹 Successfully applied dynamic anti-conflict block.", flush=True)
    except Exception as e:
        print(f"⚠️ Session reset note: {e}", flush=True)

    import threading
    audit_thread = threading.Thread(target=night_and_grid_audit_loop, daemon=True)
    audit_thread.start()
    
    # Keeps script running seamlessly without any crash-prone loop
    while True:
        try:
            # We fetch updates manually inside a try-catch pattern to protect the server runtime
            updates = bot.get_updates(offset=-1, timeout=10)
            if updates:
                bot.process_new_updates(updates)
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    main()
    
