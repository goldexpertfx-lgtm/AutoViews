import requests
import time
import random
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

# Aap ka naya testing channel username (Real par shift karte waqt badal lena)
CHANNEL_USERNAME = "Gold_Expert_Fx77" 

def clean_proxy_list(raw_proxies):
    cleaned = []
    for proxy in raw_proxies:
        proxy = proxy.strip()
        if proxy and not proxy.startswith('#'):
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', proxy):
                cleaned.append(proxy)
    return list(set(cleaned))

def get_ultra_proxy_pool():
    """6 alag top-rated sources se data nikalne ke liye optimized proxy scraper"""
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3500&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/Anonym0usWork3r/proxy-list/main/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http"
    ]
    for url in urls:
        try:
            # Random browser signatures taake scraper block na ho
            headers = {'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) User-{random.randint(1,100)}'}
            r = requests.get(url, headers=headers, timeout=4)
            if r.status_code == 200: 
                proxies.extend(r.text.splitlines())
        except: 
            continue
    return clean_proxy_list(proxies)

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            return [int(p.get('data-post').split('/')[-1]) for p in posts[-5:] if p.get('data-post')]
    except: 
        pass
    return []

def hit_view_worker(post_id, proxy):
    """Instant single request handler with stealth headers"""
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    
    # Fake browser signatures to mimic mobile/desktop traders
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': f'https://t.me/s/{CHANNEL_USERNAME}',
        'Connection': 'close'
    }
    try:
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=2.0)
        if r.status_code == 200 and "views" in r.text:
            return True
    except: 
        pass
    return False

def fire_fast_views(post_id, target_views, proxy_pool, workers_count=60):
    """Parallel processing pool - Ek sath 60 requests fire karega lightning speed ke liye"""
    random.shuffle(proxy_pool)
    success_count = 0
    
    # Workers badha kar 60 kar diye hain taake 10-15 seconds ka boost target achieve ho sake
    with ThreadPoolExecutor(max_workers=workers_count) as executor:
        futures = [executor.submit(hit_view_worker, post_id, proxy) for proxy in proxy_pool[:target_views * 4]]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= target_views:
                    break
    return success_count

def main():
    print("======================================================", flush=True)
    print("⚡ HYPER-DRIVE PRIORITIZED TRADING ENGINE v3 LIVE", flush=True)
    print(f"📈 Monitoring Channel: @{CHANNEL_USERNAME}", flush=True)
    print("======================================================", flush=True)
    
    post_ids = get_recent_post_ids()
    last_known_latest_id = post_ids[-1] if post_ids else 0
    channel_history_tracker = {} 
    
    while True:
        current_posts = get_recent_post_ids()
        if not current_posts:
            time.sleep(5)
            continue
            
        latest_id = current_posts[-1]
        
        # 🚨 TRIGGER: Nayi Post/Signal Aate Hi Sub Kuch Chhor Kar Instant Attack!
        if latest_id > last_known_latest_id:
            print(f"🚨 NEW SIGNAL DETECTED (ID: {latest_id})!", flush=True)
            print("⚡ Launching Instant 60-Thread Priority Blast for Trader Rush...", flush=True)
            last_known_latest_id = latest_id
            
            pool = get_ultra_proxy_pool()
            
            # Phase A: Shuruati 10-15 seconds ka blast (40-50 views target)
            sent_instant = fire_fast_views(latest_id, 55, pool, workers_count=60)
            print(f"💥 Instant 15s Wave Complete! Delivered {sent_instant} views.", flush=True)
            
            # Phase B: Agle 3-5 mints mein 150 views tak punch karna
            print("⏳ Maintaining momentum... Pushing to 150 views target.", flush=True)
            time.sleep(5)
            pool_two = get_ultra_proxy_pool()
            sent_momentum = fire_fast_views(latest_id, 100, pool_two, workers_count=30)
            
            channel_history_tracker[latest_id] = sent_instant + sent_momentum
            print(f"✅ Fast Signal Setup Complete for Post {latest_id}.", flush=True)
            continue 
            
        # 💤 NORMAL SYSTEM (Yesterday Posts, Old Posts aur Today's Target Cooldown)
        print("📊 Balancing Channel Ecosystem (New, Old & Yesterday Posts)...", flush=True)
        pool = get_ultra_proxy_pool()
        
        for pid in current_posts:
            is_latest = (pid == latest_id)
            
            # Targets control framework
            if is_latest:
                ultimate_target = random.randint(650, 850) # Aaj ka final scale
            else:
                ultimate_target = random.randint(1700, 2100) # Yesterday/Older post structure
                
            current_sent = channel_history_tracker.get(pid, 0)
            
            if current_sent >= ultimate_target:
                continue
                
            # Slow and stable continuous injection for deep timeline
            chunk_target = random.randint(35, 70)
            sent = fire_fast_views(pid, chunk_target, pool, workers_count=20)
            channel_history_tracker[pid] = current_sent + sent
            print(f" -> Post {pid}: Overall Views Status [{channel_history_tracker[pid]}/{ultimate_target}]", flush=True)
            time.sleep(random.uniform(4, 8)) 
            
        print("⏳ Scan cycle complete. Watching for fresh breakout signals in 10 seconds...", flush=True)
        time.sleep(10)

if __name__ == "__main__":
    main()
            
