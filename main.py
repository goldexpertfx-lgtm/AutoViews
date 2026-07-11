import telebot
import requests
import time
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask

# 🚀 Built-in Web Server Render ke liye taaki bot live rahe
app = Flask('')

@app.route('/')
def home():
    return "👑 ENTERPRISE TRADING VIEW ENGINE v17.1 IS LIVE ON RENDER"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

BOT_TOKEN = "8385538981:AAFiFcdmvuSUr7G_JqWt67fy2EMkkiCmwdU"
bot = telebot.TeleBot(BOT_TOKEN)

active_channels = {}
processed_posts = {}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
]

def get_real_sub_count(chat_id):
    try:
        count = bot.get_chat_member_count(chat_id)
        return count if count > 0 else 100
    except:
        return random.randint(95, 125)

def is_post_alive(target, msg_id, is_private):
    if is_private or str(target).startswith("-100"):
        clean_id = str(target).replace("-100", "")
        url = f"https://t.me/c/{clean_id}/{msg_id}"
    else:
        clean_username = str(target).replace("@", "")
        url = f"https://t.me/{clean_username}/{msg_id}"
    try:
        r = requests.head(url, timeout=2)
        return r.status_code != 404
    except:
        return True

def fire_free_simulation_view(target, msg_id, is_private):
    if not is_post_alive(target, msg_id, is_private):
        return "DELETED"
        
    if is_private or str(target).startswith("-100"):
        clean_id = str(target).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{msg_id}?embed=1"
    else:
        clean_username = str(target).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{msg_id}?embed=1"

    session = requests.Session()
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    try:
        r = session.get(embed_url, headers=headers, timeout=4)
        if r.status_code == 200:
            token_match = re.search(r'data-view="([^"]+)"', r.text)
            if token_match:
                token = token_match.group(1)
                ajax_headers = {
                    'User-Agent': headers['User-Agent'],
                    'Referer': embed_url,
                    'X-Requested-With': 'XMLHttpRequest'
                }
                res = session.get(f"https://t.me/v/?v={token}", headers=ajax_headers, timeout=4)
                if res.status_code == 200:
                    return "SUCCESS"
    except:
        pass
    return "FAILED"

def deliver_simulated_chunk(target, msg_id, is_private, size):
    success = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fire_free_simulation_view, target, msg_id, is_private) for _ in range(size * 2)]
        for fut in futures:
            res = fut.result()
            if res == "DELETED": return "STOP"
            if res == "SUCCESS":
                success += 1
                if success >= size: break
    return success

def human_speed_drip_pipeline(target, msg_id, is_private, total_target, post_key):
    if not is_post_alive(target, msg_id, is_private): return

    # ⏱️ 0-10 Secs Burst (0.5%)
    p1_vol = max(1, int(total_target * 0.005))
    res = deliver_simulated_chunk(target, msg_id, is_private, p1_vol)
    if res == "STOP": return
    processed_posts[post_key] = processed_posts.get(post_key, 0) + (res if isinstance(res, int) else p1_vol)
    time.sleep(random.uniform(8.0, 12.0))
    
    # ⏱️ 15-30 Secs Wave (1.0%)
    if not is_post_alive(target, msg_id, is_private): return
    p2_vol = max(1, int(total_target * 0.01))
    res = deliver_simulated_chunk(target, msg_id, is_private, p2_vol)
    if res == "STOP": return
    processed_posts[post_key] = processed_posts.get(post_key, 0) + (res if isinstance(res, int) else p2_vol)
    
    # ⏱️ Rest Drip
    remaining = total_target - processed_posts[post_key]
    while remaining > 0:
        if not is_post_alive(target, msg_id, is_private): break
        chunk = random.randint(1, 4)
        if chunk > remaining: chunk = remaining
        res = deliver_simulated_chunk(target, msg_id, is_private, chunk)
        if res == "STOP": break
        processed_posts[post_key] = processed_posts.get(post_key, 0) + res
        remaining -= res
        time.sleep(random.uniform(10.0, 30.0))

@bot.channel_post_handler(func=lambda message: True)
def monitor_incoming_posts(message):
    chat_id = message.chat.id
    msg_id = message.message_id
    is_private = True if message.chat.username is None else False
    target = chat_id if is_private else message.chat.username
    
    sub_count = get_real_sub_count(chat_id)
    active_channels[chat_id] = {
        'target': target,
        'is_private': is_private,
        'subs': sub_count,
        'last_msg_id': msg_id
    }
    
    ratio = random.uniform(10.5, 14.5) / 100.0
    total_target = int(sub_count * ratio)
    if total_target < 1: total_target = 1
    
    post_key = f"{chat_id}_{msg_id}"
    processed_posts[post_key] = 0
    
    print(f"🎯 [Render Live] Target: {total_target} Views Locked.")
    t = threading.Thread(target=human_speed_drip_pipeline, args=(target, msg_id, is_private, total_target, post_key))
    t.start()

def global_night_audit_and_yesterday_sync():
    while True:
        try:
            current_hour = time.localtime().tm_hour
            is_market_sleep = True if (current_hour >= 0 and current_hour <= 7) else False
            
            for chat_id, meta in list(active_channels.items()):
                last_id = meta['last_msg_id']
                subs = meta['subs']
                target = meta['target']
                is_private = meta['is_private']
                
                for historical_id in range(max(1, last_id - 3), last_id + 1):
                    key = f"{chat_id}_{historical_id}"
                    cap_ratio = random.uniform(10.0, 15.0) / 100.0 if historical_id == last_id else random.uniform(20.0, 25.0) / 100.0
                    max_allowed_views = int(subs * cap_ratio)
                    current_views = processed_posts.get(key, 0)
                    
                    if current_views >= max_allowed_views: continue
                    chunk = random.randint(1, 2) if is_market_sleep else random.randint(2, 5)
                    delay = random.randint(60, 120) if is_market_sleep else random.randint(25, 50)
                        
                    if is_post_alive(target, historical_id, is_private):
                        res = deliver_simulated_chunk(target, historical_id, is_private, chunk)
                        if res != "STOP": processed_posts[key] = current_views + res
                    time.sleep(delay)
        except: pass
        time.sleep(60)

def main():
    # Web server ko alag thread mein start karna Render ke liye
    ws_thread = threading.Thread(target=run_web_server, daemon=True)
    ws_thread.start()

    try:
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url="https://localhost/fake-webhook-render")
    except: pass

    audit_worker = threading.Thread(target=global_night_audit_and_yesterday_sync, daemon=True)
    audit_worker.start()
    
    while True:
        try:
            updates = bot.get_updates(offset=-1, timeout=12)
            if updates: bot.process_new_updates(updates)
        except: pass
        time.sleep(2)

if __name__ == "__main__":
    main()
                
