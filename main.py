import requests
import time
import random
from bs4 import BeautifulSoup
import re

CHANNEL_USERNAME = "Gold_Expert_Fx77" # Testing channel name

def clean_proxy_list(raw_proxies):
    cleaned = []
    for proxy in raw_proxies:
        proxy = proxy.strip()
        if proxy and not proxy.startswith('#'):
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', proxy):
                cleaned.append(proxy)
    return list(set(cleaned))

def get_high_quality_free_proxies():
    print("🔄 Fetching fresh proxies pool...", flush=True)
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
    ]
    for url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                proxies.extend(response.text.splitlines())
        except:
            continue
    return clean_proxy_list(proxies)

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            return [int(p.get('data-post').split('/')[-1]) for p in posts[-4:] if p.get('data-post')]
    except Exception as e:
        print(f"❌ Error fetching posts: {e}", flush=True)
    return []

def hit_view(post_id, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': f'https://t.me/s/{CHANNEL_USERNAME}'
    }
    try:
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=3)
        if r.status_code == 200 and "views" in r.text:
            return True
    except:
        pass
    return False

def main():
    print("======================================================", flush=True)
    print("🚀 PRIORITY TRADING ENGINE ACTIVE ON RENDER PREMIUM", flush=True)
    print(f"📈 Target Channel: @{CHANNEL_USERNAME}", flush=True)
    print("======================================================", flush=True)
    
    # Pehle round mein posts map taiyar karna
    post_ids = get_recent_post_ids()
    last_known_latest_id = post_ids[-1] if post_ids else 0
    
    # Base targets setup
    # Key: post_id, Value: [current_views_sent, max_target_needed]
    views_tracker = {}
    
    while True:
        # 1. Har round ke start mein check karein ke koi nayi post to nahi aayi?
        current_posts = get_recent_post_ids()
        if not current_posts:
            time.sleep(15)
            continue
            
        latest_post_id = current_posts[-1]
        
        # 🚨 ALERT: Agar nayi post detect ho jaye!
        if latest_post_id > last_known_latest_id:
            print(f"🚨 ALERT: New Trading Signal Detected! (ID: {latest_post_id})", flush=True)
            print("⚡ Pausing old tasks. Shifting 100% focus to New Post!", flush=True)
            last_known_latest_id = latest_post_id
            
            # Nayi post ko highest priority target dena (600-850 views)
            views_tracker[latest_post_id] = [0, random.randint(600, 850)]
            
            # --- INSTANT RUSH LOOP FOR NEW POST ---
            proxies = get_high_quality_free_proxies()
            random.shuffle(proxies)
            
            print(f"🔥 Phase 1 (Signal Rush): Sending fast views to {latest_post_id}...", flush=True)
            for proxy in proxies:
                if views_tracker[latest_post_id][0] >= views_tracker[latest_post_id][1]:
                    break # Target complete
                    
                if hit_view(latest_post_id, proxy):
                    views_tracker[latest_post_id][0] += 1
                    if views_tracker[latest_post_id][0] % 50 == 0:
                        print(f"💥 New Post {latest_post_id} -> Live Views: {views_tracker[latest_post_id][0]}/{views_tracker[latest_post_id][1]}", flush=True)
                    time.sleep(random.uniform(1.5, 3.5)) # Fast delivery gap
            
            print(f"✅ Phase 1 Done for New Post {latest_post_id}. Shifting back to multi-tasking.", flush=True)

        # 2. SLOW BACKGROUND WAVE (For all recent 4 posts)
        # Tracker update for older posts if not exists
        for pid in current_posts:
            if pid not in views_tracker:
                # Purani posts ka ultimate target 1700-2000 views tak le kar jana hai
                views_tracker[pid] = [0, random.randint(1700, 2000)]
        
        proxies = get_high_quality_free_proxies()
        random.shuffle(proxies)
        
        print("💤 Running Background Top-up for all posts (Slow & Organic)...", flush=True)
        
        # Ek cycle mein har post par thode thode views dalna
        for pid in current_posts:
            # Agar target poora ho chuka hai to skip karein
            if views_tracker[pid][0] >= views_tracker[pid][1]:
                continue
                
            # Har post par is round mein sirf 15-20 views bhejna aur phir agli post par switch hona
            sub_target = 20
            views_sent_this_round = 0
            
            for proxy in proxies:
                if views_sent_this_round >= sub_target or views_tracker[pid][0] >= views_tracker[pid][1]:
                    break
                    
                if hit_view(pid, proxy):
                    views_tracker[pid][0] += 1
                    views_sent_this_round += 1
                    time.sleep(random.uniform(8.0, 15.0)) # Slow top-up gap
            
            print(f" -> Post {pid} updated. Total Progress: {views_tracker[pid][0]} Views", flush=True)
            
        print("⏳ Fast scanning for any new updates in 15 seconds...", flush=True)
        time.sleep(15)

if __name__ == "__main__":
    main()
                
