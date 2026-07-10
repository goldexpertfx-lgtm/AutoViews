import telebot
import requests
import time
import random
import math
from concurrent.futures import ThreadPoolExecutor

# ⚠️ Apna Bot Token yahan dalein
BOT_TOKEN = "7818601229:AAHzgOQYaAulQ_GsB8YdZbzjWLW_a48Y974"
bot = telebot.TeleBot(BOT_TOKEN)

# ULTRA HIGH-SPEED PAID HTTP ROTATING ENGINE
PROXY_URL = "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/"
PROXY_DICT = {"http": PROXY_URL, "https": PROXY_URL}

# Global database to mimic organic memory
channel_configs = {}  # Stores dynamic subscriber limits and randomized formulas
delivered_views_tracker = {}  # TRACKS exact delivery per message_id to prevent over-pumping

def get_channel_subscriber_count(chat_id):
    """Fetches total subscribers dynamically to calculate the 10-15% limits"""
    try:
        count = bot.get_chat_member_count(chat_id)
        return count if count > 0 else 100  # Default fallback if restricted
    except Exception as e:
        print(f"⚠️ Error fetching subscriber count for {chat_id}: {e}", flush=True)
        return 500  # Safe average baseline

def hit_view_worker(channel_info):
    channel_username, message_id, is_private = channel_info
    if is_private:
        clean_id = str(channel_username).replace("-100", "")
        embed_url = f"https://t.me/c/{clean_id}/{message_id}?embed=1"
    else:
        clean_username = str(channel_username).replace("@", "")
        embed_url = f"https://t.me/{clean_username}/{message_id}?embed=1"
        
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(534,603)}.{random.randint(1,50)} (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': f'https://t.me/s/{str(channel_username).replace("@","")}' if not is_private else 'https://t.me/',
        'Connection': 'keep-alive'
    }
    try:
        r = requests.get(embed_url, proxies=PROXY_DICT, headers=headers, timeout=4)
        if r.status_code == 200 and "views" in r.text and "Post not found" not in r.text:
            return True
    except:
        pass
    return False

def fire_percentage_chunk(target_identifier, message_id, is_private, volume, worker_threads=15):
    """Fires targeted view bursts using dynamic thread allocation"""
    if volume <= 0:
        return 0
    channel_info = (target_identifier, message_id, is_private)
    success_count = 0
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = [executor.submit(hit_view_worker, channel_info) for _ in range(int(volume * 2.5))]
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
    
    # 🌟 Step 1: Calculate Real-time Channel Strength
    sub_count = get_channel_subscriber_count(chat_id)
    
    # Randomize targets so posts never look identical (e.g. one gets 11%, other gets 14%)
    daily_target_percent = random.uniform(10.0, 15.0) / 100.0
    total_target_views = max(10, int(sub_count * daily_target_percent))
    
    # Save parameters for background audits
    channel_configs[chat_id] = {
        'target_identifier': target_identifier,
        'is_private': is_private,
        'sub_count': sub_count,
        'latest_id': message_id
    }
    
    print(f"📡 [NEW POST] Channel: {message.chat.title} | Subs: {sub_count} | Target Base: {total_target_views} views", flush=True)
    
    # ⏳ Step 2: Phase 1 -> 0.5% views inside first 10 seconds
    p1_volume = max(1, int(total_target_views * 0.005))
    sent_p1 = fire_percentage_chunk(target_identifier, message_id, is_private, p1_volume, worker_threads=5)
    print(f"⏱️ [10s Stamp] Pushed 0.5% burst (+{sent_p1} views)", flush=True)
    time.sleep(12)
    
    # ⏳ Step 3: Phase 2 -> 1% views inside 15-30 seconds
    p2_volume = max(1, int(total_target_views * 0.01))
    sent_p2 = fire_percentage_chunk(target_identifier, message_id, is_private, p2_volume, worker_threads=8)
    print(f"⏱️ [30s Stamp] Pushed 1.0% momentum (+{sent_p2} views)", flush=True)
    
    # Update global memory
    track_key = f"{chat_id}_{message_id}"
    delivered_views_tracker[track_key] = sent_p1 + sent_p2

def night_and_grid_audit_loop():
    """Background loop that executes slower drip-feeding and runs deep channel audits at night"""
    while True:
        try:
            current_hour = time.localtime().tm_hour
            # 🌙 Night mode runs between 11 PM and 6 AM (Slower, stealth processing)
            is_night_mode = current_hour >= 23 or current_hour < 6
            
            if is_night_mode:
                print("🌙 Night Audit Active: Processing stealth baseline adjustments...", flush=True)
                sleep_interval = 25  # Lower proxy frequency to keep channel looking completely organic
            else:
                sleep_interval = 12  # Standard active hours grid balancing

            for chat_id, config in list(channel_configs.items()):
                latest_id = config['latest_id']
                sub_count = config['sub_count']
                target_id = config['target_identifier']
                is_private = config['is_private']
                
                # Check recent trailing grid of past 4 messages (including yesterday's posts)
                for msg_id in range(max(1, latest_id - 4), latest_id + 1):
                    track_key = f"{chat_id}_{msg_id}"
                    
                    # Determine dynamic target bounds based on post age
                    if msg_id == latest_id:
                        # Today's active post: 10% - 15%
                        target_ratio = random.uniform(10.0, 15.0) / 100.0
                    else:
                        # Yesterday's trailing posts: Scales up to 20% - 25% organically
                        target_ratio = random.uniform(20.0, 25.0) / 100.0
                        
                    calculated_cap = max(15, int(sub_count * target_ratio))
                    current_done = delivered_views_tracker.get(track_key, 0)
                    
                    if current_done >= calculated_cap:
                        continue
                        
                    # Drip feed a small chunk (e.g. 2-5% of missing views at a time)
                    chunk_size = random.randint(15, 35)
                    if current_done + chunk_size > calculated_cap:
                        chunk_size = calculated_cap - current_done
                        
                    # Trigger chunk fire (Checks for deletion happens seamlessly during worker handshakes)
                    sent = fire_percentage_chunk(target_id, msg_id, is_private, chunk_size, worker_threads=10)
                    delivered_views_tracker[track_key] = current_done + sent
                    
                    print(f"📊 [Grid Sync] Channel ID {chat_id} | Msg {msg_id} -> Status: [{delivered_views_tracker[track_key]}/{calculated_cap}]", flush=True)
                    time.sleep(4)
                    
        except Exception as e:
            print(f"⚠️ Grid audit engine hiccup: {e}", flush=True)
            
        time.sleep(sleep_interval)

def main():
    print("======================================================", flush=True)
    print("🤖 ULTRA BOT ENGINE v5.0 (Dynamic Organic Scaler Live)", flush=True)
    print("📈 Automatic Subscriber Percentage Matrix Active")
    print("======================================================", flush=True)
    
    # Launch the Background Matrix Thread for Drip Feeding & Night Auditing
    import threading
    audit_thread = threading.Thread(target=night_and_grid_audit_loop, daemon=True)
    audit_thread.start()
    
    # Start Telegram Long Polling
    while True:
        try:
            bot.infinity_polling(timeout=25, long_polling_timeout=15)
        except Exception as e:
            print(f"⚠️ Bot network glitch, restarting socket... Error: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
    
