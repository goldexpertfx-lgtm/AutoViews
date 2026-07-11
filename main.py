import telebot
import requests
import time
import random
import re
from concurrent.futures import ThreadPoolExecutor

BOT_TOKEN = "8385538981:AAFiFcdmvuSUr7G_JqWt67fy2EMkkiCmwdU"
bot = telebot.TeleBot(BOT_TOKEN)

# Dynamic Proxy Pool
GLOBAL_PROXIES = []
channel_configs = {}
delivered_views_tracker = {}

def fetch_fresh_public_proxies():
    """Internet se fresh HTTP/HTTPS proxies auto-scrape karne ka engine"""
    global GLOBAL_PROXIES
    proxy_urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.proxy-list.download/api/v1/get?type=http"
    ]
    new_pool = []
    for url in proxy_urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                extracted = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}\b', r.text)
                new_pool.extend(extracted)
        except:
            pass
    
    if new_pool:
        GLOBAL_PROXIES = list(set(new_pool)) # Duplicate remove lines
        print(f"🔄 [DYNAMIC PROXY ENGINE] Loaded {len(GLOBAL_PROXIES)} fresh public pipelines.", flush=True)
    else:
        print("⚠️ Proxy source down, retrying next loop...", flush=True)

def get_channel_subscriber_count(chat_id):
    try:
        count = bot.get_chat_member_count(chat_id)
        return count if count > 0 else 1000
    except:
        return 10430

def hit_view_worker(channel_info):
    global GLOBAL_PROXIES
    if not GLOBAL_PROXIES:
        return False
        
    channel_username, message_id, is_private = channel_info
    
    if is_private or str(channel_username).startswith("-100"):
        clean_id = str(channel_username).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{message_id}?embed=1"
    else:
        clean_username = str(channel_username).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
        
    # Pool se random proxy pick karein
    selected_proxy = random.choice(GLOBAL_PROXIES)
    proxies = {"http": f"http://{selected_proxy}", "https": f"http://{selected_proxy}"}
    
    session = requests.Session()
    session.proxies = proxies
    
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(124,126)}.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }
    
    try:
        r = session.get(embed_url, headers=headers, timeout=3)
        if r.status_code == 200:
            token_match = re.search(r'data-view="([^"]+)"', r.text)
            if token_match:
                token = token_match.group(1)
                
                ajax_headers = {
                    'User-Agent': headers['User-Agent'],
                    'Accept': '*/*',
                    'Referer': embed_url,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive'
                }
                
                res = session.get(f"https://t.me/v/?v={token}", headers=ajax_headers, timeout=3)
                if res.status_code == 200:
                    return True
    except:
        # Agar koi public proxy bad respond kare toh use pool se drop kar sakte hain temporarily
        pass
    return False

def fire_percentage_chunk(target_identifier, message_id, is_private, volume, worker_threads=60):
    if volume <= 0:
        return 0
    channel_info = (target_identifier, message_id, is_private)
    success_count = 0
    
    # Public proxies ka success rate low hota hai isliye multi-firing 6x rakhi hai
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = [executor.submit(hit_view_worker, channel_info) for _ in range(int(volume * 6))]
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
    trading_target_percent = random.uniform(32.0, 42.0) / 100.0
    total_target_views = int(sub_count * trading_target_percent)
    
    channel_configs[chat_id] = {
        'target_identifier': target_identifier,
        'is_private': is_private,
        'sub_count': sub_count,
        'latest_id': message_id
    }
    
    print(f"📡 [TRADING MODE AUTO] New Post. Target: {total_target_views} Views", flush=True)
    
    p1_volume = int(total_target_views * 0.35)
    sent_p1 = fire_percentage_chunk(target_identifier, message_id, is_private, p1_volume, worker_threads=80)
    print(f"⚡ [Auto Burst] Initial success: (+{sent_p1} views)", flush=True)
    
    track_key = f"{chat_id}_{message_id}"
    delivered_views_tracker[track_key] = sent_p1

def proxy_refresher_loop():
    while True:
        fetch_fresh_public_proxies()
        time.sleep(60) # Har 60 seconds baad fresh list load hogi

def night_and_grid_audit_loop():
    while True:
        try:
            for chat_id, config in list(channel_configs.items()):
                latest_id = config['latest_id']
                sub_count = config['sub_count']
                target_id = config['target_identifier']
                is_private = config['is_private']
                
                for msg_id in range(max(1, latest_id - 2), latest_id + 1):
                    track_key = f"{chat_id}_{msg_id}"
                    calculated_cap = int(sub_count * (random.uniform(35, 45) / 100.0))
                    current_done = delivered_views_tracker.get(track_key, 0)
                    
                    if current_done >= calculated_cap:
                        continue
                        
                    chunk_size = random.randint(30, 60)
                    sent = fire_percentage_chunk(target_id, msg_id, is_private, chunk_size, worker_threads=40)
                    delivered_views_tracker[track_key] = current_done + sent
                    print(f"📊 [Grid Sync] Msg {msg_id} status: [{delivered_views_tracker[track_key]}/{calculated_cap}]", flush=True)
                    time.sleep(3)
        except Exception as e:
            pass
        time.sleep(20)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v12.0 (Auto Scraper Integration)", flush=True)
    print("======================================================", flush=True)
    
    try:
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url="https://localhost/fake-webhook-to-kill-polling")
    except:
        pass

    import threading
    # Thread 1: Proxy Refresh Engine
    refresher_thread = threading.Thread(target=proxy_refresher_loop, daemon=True)
    refresher_thread.start()
    
    # Thread 2: Background Grid Audit
    audit_thread = threading.Thread(target=night_and_grid_audit_loop, daemon=True)
    audit_thread.start()
    
    time.sleep(5) # Initial proxies load hone ka wait karein
    
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
