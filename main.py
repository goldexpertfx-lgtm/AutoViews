import telebot
import requests
import time
import random
import re
from concurrent.futures import ThreadPoolExecutor

# ⚠️ Apna Bot Token yahan dalein
BOT_TOKEN = "8385538981:AAFiFcdmvuSUr7G_JqWt67fy2EMkkiCmwdU"
bot = telebot.TeleBot(BOT_TOKEN)

# Fallback Backups: Agar paid proxy block ho, toh yeh public pool se automatically live IPs uthayega
fallback_proxies = []

def refresh_public_proxy_pool():
    global fallback_proxies
    try:
        # Fetching fresh socks4/http proxies dynamically
        res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all", timeout=10)
        if res.status_code == 200 and len(res.text) > 100:
            fallback_proxies = [p.strip() for p in res.text.split("\n") if p.strip()]
            print(f"🔄 [PROXY REFRESH] Loaded {len(fallback_proxies)} fresh public backup IPs.", flush=True)
    except Exception as e:
        print(f"⚠️ Proxy Scraper Note: {e}", flush=True)

# Initial proxy setup
refresh_public_proxy_pool()

channel_configs = {}
delivered_views_tracker = {}

def get_channel_subscriber_count(chat_id):
    try:
        count = bot.get_chat_member_count(chat_id)
        return count if count > 0 else 1000
    except:
        return 5000

def hit_view_worker(channel_info):
    global fallback_proxies
    channel_username, message_id, is_private = channel_info
    
    if is_private:
        clean_id = str(channel_username).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{message_id}?embed=1"
    else:
        clean_username = str(channel_username).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
        
    session = requests.Session()
    
    # SYSTEM SELECTION: Decides whether to route through primary or dynamic fallback pool
    if fallback_proxies and random.random() > 0.3:
        p_ip = random.choice(fallback_proxies)
        session.proxies = {"http": f"http://{p_ip}", "https": f"http://{p_ip}"}
    else:
        # Default Webshare
        session.proxies = {"http": "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/", "https": "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/"}
    
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(122,126)}.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': embed_url,
        'Connection': 'keep-alive'
    }
    
    try:
        r = session.get(embed_url, headers=headers, timeout=6)
        if r.status_code == 200 and "views" in r.text:
            token_match = re.search(r'data-view="([^"]+)"', r.text)
            if token_match:
                token = token_match.group(1)
                ajax_url = f"https://t.me/v/?v={token}"
                
                ajax_headers = headers.copy()
                ajax_headers.update({
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': '*/*',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin'
                })
                
                res = session.get(ajax_url, headers=ajax_headers, timeout=4)
                if res.status_code == 200:
                    return True
            else:
                # Debugging line to capture signature mismatch
                print("🔍 [DEBUG] Token signature not found in HTML payload.", flush=True)
    except Exception as e:
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
    
    print(f"📡 [NEW POST DETECTED] Subs: {sub_count} | Target: {total_target_views}", flush=True)
    
    p1_volume = max(3, int(total_target_views * 0.01))
    sent_p1 = fire_percentage_chunk(target_identifier, message_id, is_private, p1_volume, worker_threads=15)
    print(f"⏱️ [10s Burst] Pushed (+{sent_p1} views)", flush=True)
    
    track_key = f"{chat_id}_{message_id}"
    delivered_views_tracker[track_key] = sent_p1

def night_and_grid_audit_loop():
    proxy_timer = 0
    while True:
        try:
            proxy_timer += 1
            if proxy_timer >= 15:  # Every ~5 minutes, refresh the fallback pool
                refresh_public_proxy_pool()
                proxy_timer = 0
                
            for chat_id, config in list(channel_configs.items()):
                latest_id = config['latest_id']
                sub_count = config['sub_count']
                target_id = config['target_identifier']
                is_private = config['is_private']
                
                for msg_id in range(max(1, latest_id - 2), latest_id + 1):
                    track_key = f"{chat_id}_{msg_id}"
                    calculated_cap = max(20, int(sub_count * (random.uniform(10, 15) / 100.0)))
                    current_done = delivered_views_tracker.get(track_key, 0)
                    
                    if current_done >= calculated_cap:
                        continue
                        
                    chunk_size = random.randint(15, 30)
                    sent = fire_percentage_chunk(target_id, msg_id, is_private, chunk_size, worker_threads=10)
                    delivered_views_tracker[track_key] = current_done + sent
                    print(f"📊 [Grid Sync] Msg {msg_id} -> Status: [{delivered_views_tracker[track_key]}/{calculated_cap}]", flush=True)
                    time.sleep(5)
        except Exception as e:
            print(f"⚠️ Grid loop error: {e}", flush=True)
        time.sleep(20)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v8.0 (Dynamic Proxy Core Live)", flush=True)
    print("======================================================", flush=True)
    
    try:
        bot.remove_webhook()
        time.sleep(2)
        bot.set_webhook(url="https://localhost/fake-webhook-to-kill-polling")
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
        
