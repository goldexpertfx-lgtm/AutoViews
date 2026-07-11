import telebot
import requests
import time
import random
import re
from concurrent.futures import ThreadPoolExecutor

BOT_TOKEN = "8385538981:AAFiFcdmvuSUr7G_JqWt67fy2EMkkiCmwdU"
bot = telebot.TeleBot(BOT_TOKEN)

# 🚀 Apni Premium Rotating Proxy ka details yahan set karein
PREMIUM_PROXY = "http://USER:PASSWORD@ROTATING-ENDPOINT.com:8000"
PROXY_DICT = {"http": PREMIUM_PROXY, "https": PREMIUM_PROXY}

channel_configs = {}
delivered_views_tracker = {}
active_threads = {}

def get_channel_subscriber_count(chat_id):
    try:
        count = bot.get_chat_member_count(chat_id)
        return count if count > 0 else 1000
    except:
        return random.randint(950, 1100)

def verify_post_exists(channel_username, message_id, is_private):
    """Detects if a post is deleted to instantly stop hitting"""
    if is_private or str(channel_username).startswith("-100"):
        clean_id = str(channel_username).replace("-100", "")
        url = f"https://t.me/c/{clean_id}/{message_id}"
    else:
        clean_username = str(channel_username).replace("@", "")
        url = f"https://t.me/{clean_username}/{message_id}"
    try:
        r = requests.head(url, timeout=3)
        if r.status_code == 404:
            return False
    except:
        pass
    return True

def hit_view_worker(channel_info):
    channel_username, message_id, is_private = channel_info
    
    # Live Check: Agar post delete ho chuki hai toh worker stop
    if not verify_post_exists(channel_username, message_id, is_private):
        return "DELETED"

    if is_private or str(channel_username).startswith("-100"):
        clean_id = str(channel_username).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{message_id}?embed=1"
    else:
        clean_username = str(channel_username).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
        
    session = requests.Session()
    session.proxies = PROXY_DICT
    
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(124,126)}.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }
    
    try:
        r = session.get(embed_url, headers=headers, timeout=5)
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
                res = session.get(f"https://t.me/v/?v={token}", headers=ajax_headers, timeout=4)
                if res.status_code == 200:
                    return "SUCCESS"
    except:
        pass
    return "FAILED"

def execute_drip_feed(target_id, message_id, is_private, total_needed, pool_key):
    channel_info = (target_id, message_id, is_private)
    
    # ⏱️ Phase 1: Pehle 10 Seconds mein bilkul normal 0.5% views
    p1_vol = max(1, int(total_needed * 0.005))
    fire_chunk(channel_info, p1_vol)
    time.sleep(random.randint(8, 12))
    
    # ⏱️ Phase 2: Agle 15-30 Seconds mein mazeed 1% views
    if not verify_post_exists(target_id, message_id, is_private): return
    p2_vol = max(1, int(total_needed * 0.01))
    fire_chunk(channel_info, p2_vol)
    time.sleep(random.randint(15, 25))
    
    # ⏱️ Phase 3: Baqi bache hue 10%-14% views natural smooth scheduling ke sath
    remaining = total_needed - (p1_vol + p2_vol)
    while remaining > 0:
        if not verify_post_exists(target_id, message_id, is_private):
            print(f"🛑 [STOPPED] Post {message_id} deleted by user. Target cancelled.", flush=True)
            break
            
        chunk = random.randint(2, 7)
        if chunk > remaining: chunk = remaining
        
        delivered = fire_chunk(channel_info, chunk)
        delivered_views_tracker[pool_key] = delivered_views_tracker.get(pool_key, 0) + delivered
        remaining -= chunk
        
        # Random interval between hits to mimic real users scrolling
        time.sleep(random.uniform(5.0, 15.0))

def fire_chunk(channel_info, volume):
    success = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(hit_view_worker, channel_info) for _ in range(volume * 2)]
        for fut in futures:
            res = fut.result()
            if res == "DELETED":
                return success
            if res == "SUCCESS":
                success += 1
                if success >= volume: break
    return success

@bot.channel_post_handler(func=lambda message: True)
def handle_live_signals(message):
    chat_id = message.chat.id
    message_id = message.message_id
    is_private = True if message.chat.username is None else False
    target_id = chat_id if is_private else message.chat.username
    
    sub_count = get_channel_subscriber_count(chat_id)
    
    # Dynamic Scaling Matrix (Bilkul professional proportion)
    daily_ratio = random.uniform(10.0, 15.0) / 100.0
    total_target = int(sub_count * daily_ratio)
    if total_target < 1: total_target = 1
    
    pool_key = f"{chat_id}_{message_id}"
    delivered_views_tracker[pool_key] = 0
    
    channel_configs[chat_id] = {
        'target_id': target_id,
        'is_private': is_private,
        'sub_count': sub_count,
        'latest_id': message_id
    }
    
    print(f"📡 [SMART ENGINE v15] Channel Subs: {sub_count} -> Target Set: {total_target} Views (Proportional)", flush=True)
    
    # Multi-threaded async scheduling for human emulation
    import threading
    t = threading.Thread(target=execute_drip_feed, args=(target_id, message_id, is_private, total_target, pool_key))
    t.start()

def night_audit_and_yesterday_sync_loop():
    while True:
        try:
            current_hour = time.localtime().tm_hour
            # 🌙 Raat 12 baje se subah 7 baje tak activity slow or steady rakhein
            is_night = True if (current_hour >= 0 or current_hour <= 7) else False
            
            for chat_id, config in list(channel_configs.items()):
                latest_id = config['latest_id']
                sub_count = config['sub_count']
                target_id = config['target_id']
                is_private = config['is_private']
                
                # Yesterday & Active grid scanning (Last 3 posts check)
                for msg_id in range(max(1, latest_id - 3), latest_id + 1):
                    pool_key = f"{chat_id}_{msg_id}"
                    
                    # Target assignment based on age of the post
                    if msg_id == latest_id:
                        ratio = random.uniform(10, 15) / 100.0 # Current day ratio
                    else:
                        ratio = random.uniform(20, 25) / 100.0 # Yesterday's boost ratio
                        
                    calculated_cap = int(sub_count * ratio)
                    current_done = delivered_views_tracker.get(pool_key, 0)
                    
                    if current_done >= calculated_cap:
                        continue
                        
                    if is_night:
                        # Raat ke waqt extra slow drip taaki pattern natural lage
                        chunk_size = random.randint(1, 3)
                        time_wait = random.randint(30, 60)
                    else:
                        chunk_size = random.randint(5, 12)
                        time_wait = random.randint(10, 20)
                        
                    if verify_post_exists(target_id, msg_id, is_private):
                        sent = fire_chunk((target_id, msg_id, is_private), chunk_size)
                        delivered_views_tracker[pool_key] = current_done + sent
                        print(f"📊 [Routine Sync] Msg {msg_id} Status: [{delivered_views_tracker[pool_key]}/{calculated_cap}]", flush=True)
                    
                    time.sleep(time_wait)
        except:
            pass
        time.sleep(40)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v15.0 (Smart Human Emulation Live)", flush=True)
    print("======================================================", flush=True)
    
    try:
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url="https://localhost/fake-webhook-to-kill-polling")
    except:
        pass

    import threading
    audit_thread = threading.Thread(target=night_audit_and_yesterday_sync_loop, daemon=True)
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
    
