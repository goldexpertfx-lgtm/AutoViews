import requests
import time
import random
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

CHANNEL_USERNAME = "Gold_Expert_Fx77" # Real channel ke liye badal kar "Gold_Expert_Fx" kar dein

def clean_proxy_list(raw_proxies):
    cleaned = []
    for proxy in raw_proxies:
        proxy = proxy.strip()
        if proxy and not proxy.startswith('#'):
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', proxy):
                cleaned.append(proxy)
    return list(set(cleaned))

def get_ultra_proxy_pool():
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=4000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    ]
    for url in urls:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=4)
            if r.status_code == 200: proxies.extend(r.text.splitlines())
        except: continue
    return clean_proxy_list(proxies)

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=6)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            return [int(p.get('data-post').split('/')[-1]) for p in posts[-5:] if p.get('data-post')]
    except: pass
    return []

def hit_view_worker(post_id, proxy):
    """Single fast worker for threading"""
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    try:
        r = requests.get(embed_url, proxies=proxy_dict, headers={'User-Agent': 'Mozilla/5.0'}, timeout=2.5)
        if r.status_code == 200 and "views" in r.text:
            return True
    except: pass
    return False

def fire_fast_views(post_id, target_views, proxy_pool):
    """ThreadPoolExecutor to force views instantly within seconds"""
    random.shuffle(proxy_pool)
    success_count = 0
    
    # 50 Parallel threads aik sath fire hongi bullet speed ki tarah
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(hit_view_worker, post_id, proxy) for proxy in proxy_pool[:target_views * 3]]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= target_views:
                    break
    return success_count

def main():
    print("======================================================", flush=True)
    print("⚡ HYPER-DRIVE 50-THREAD TRADING ENGINE LIVE ON RENDER", flush=True)
    print(f"📈 Monitoring Channel: @{CHANNEL_USERNAME}", flush=True)
    print("======================================================", flush=True)
    
    post_ids = get_recent_post_ids()
    last_known_latest_id = post_ids[-1] if post_ids else 0
    channel_history_tracker = {} # Har post ka permanent views counter
    
    while True:
        current_posts = get_recent_post_ids()
        if not current_posts:
            time.sleep(5)
            continue
            
        latest_id = current_posts[-1]
        
        # 🚨 TRIGGER: Nayi Post Detect Hote Hi Instant Attack!
        if latest_id > last_known_latest_id:
            print(f"🚨 NEW SIGNAL DETECTED (ID: {latest_id})! Launching Instant 50-Thread Blast...", flush=True)
            last_known_latest_id = latest_id
            
            # Fresh proxies for instant delivery
            pool = get_ultra_proxy_pool()
            
            # Immediate target: 150 views within first 3-5 minutes
            sent = fire_fast_views(latest_id, 160, pool)
            print(f"💥 Instant Blast Complete! Delivered {sent} views to New Post {latest_id} within seconds.", flush=True)
            channel_history_tracker[latest_id] = sent
            continue # Skip normal routine to stay safe
            
        # 💤 NORMAL ECOSYSTEM MANAGEMENT (Yesterday & Past Posts)
        print("📊 Managing Full Channel Ecosystem (New, Old & Yesterday Posts)...", flush=True)
        pool = get_ultra_proxy_pool()
        
        for pid in current_posts:
            is_latest = (pid == latest_id)
            
            # Dynamic Target Setting
            if is_latest:
                ultimate_target = random.randint(650, 850) # Today's normal limit
            else:
                ultimate_target = random.randint(1700, 2100) # Yesterday / Old post premium layout
                
            current_sent = channel_history_tracker.get(pid, 0)
            
            if current_sent >= ultimate_target:
                continue
                
            # Slow incremental push for ecosystem stability
            chunk_target = random.randint(30, 60)
            sent = fire_fast_views(pid, chunk_target, pool)
            channel_history_tracker[pid] = current_sent + sent
            print(f" -> Post {pid}: Total Views Level reached [{channel_history_tracker[pid]}/{ultimate_target}]", flush=True)
            time.sleep(random.uniform(5, 10)) # Natural resting gap between posts
            
        print("⏳ Scan cycle done. Re-checking for new signals in 10 seconds...", flush=True)
        time.sleep(10)

if __name__ == "__main__":
    main()
    
