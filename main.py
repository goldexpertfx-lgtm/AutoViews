import requests
import time
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

CHANNEL_USERNAME = "Gold_Expert_Fx77" 

PROXY_URL = "http://qkhaljvp:zadw5l3s9igx@p.webshare.io:80/"
PROXY_DICT = {
    "http": PROXY_URL,
    "https": PROXY_URL
}

# Persistent memory pools
channel_history_tracker = {}
target_caps_tracker = {}

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(530,600)}.36',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        r = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            return [int(p.get('data-post').split('/')[-1]) for p in posts[-5:] if p.get('data-post')]
    except Exception as e:
        print(f"❌ Error scanning channel: {e}", flush=True)
    return []

def hit_view_worker(post_id):
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(530,600)}.36',
        'Referer': f'https://t.me/s/{CHANNEL_USERNAME}',
        'Connection': 'close'
    }
    try:
        r = requests.get(embed_url, proxies=PROXY_DICT, headers=headers, timeout=4)
        if r.status_code == 200 and "views" in r.text:
            return True
    except:
        pass
    return False

def fire_fast_views(post_id, target_views, threads=40):
    success_count = 0
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(hit_view_worker, post_id) for _ in range(target_views * 2)]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= target_views:
                    break
    return success_count

def main():
    print("======================================================", flush=True)
    print("💎 PREMIUM HTTP ROTATING ENGINE v3.1 LIVE", flush=True)
    print(f"📈 Target Channel: @{CHANNEL_USERNAME}", flush=True)
    print("======================================================", flush=True)
    
    post_ids = get_recent_post_ids()
    last_known_latest_id = post_ids[-1] if post_ids else 0
    
    while True:
        current_posts = get_recent_post_ids()
        if not current_posts:
            time.sleep(10)
            continue
            
        latest_id = current_posts[-1]
        
        if latest_id > last_known_latest_id:
            print(f"🚨 NEW SIGNAL DETECTED: Post ID {latest_id}", flush=True)
            last_known_latest_id = latest_id
            
            sent_instant = fire_fast_views(latest_id, 60, threads=45)
            channel_history_tracker[latest_id] = channel_history_tracker.get(latest_id, 0) + sent_instant
            print(f"💥 Delivered {sent_instant} instant views to New Post.", flush=True)
            continue
            
        print("📊 Balancing Channel Grid...", flush=True)
        for pid in current_posts:
            is_latest = (pid == latest_id)
            
            # Set permanent cap for the session so it doesn't shuffle every 10 seconds
            if pid not in target_caps_tracker:
                target_caps_tracker[pid] = random.randint(650, 850) if is_latest else random.randint(1700, 2100)
                
            ultimate_target = target_caps_tracker[pid]
            current_sent = channel_history_tracker.get(pid, 0)
            
            if current_sent >= ultimate_target:
                continue
                
            chunk = random.randint(30, 60)
            sent = fire_fast_views(pid, chunk, threads=15)
            channel_history_tracker[pid] = current_sent + sent
            
            print(f" -> Post {pid}: Added +{sent} Views. Status [{channel_history_tracker[pid]}/{ultimate_target}]", flush=True)
            time.sleep(3)
            
        print("⏳ Cycle complete. Re-checking in 10s...", flush=True)
        time.sleep(10)

if __name__ == "__main__":
    main()
                
