import requests
import time
import random
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

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
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=4)
            if r.status_code == 200: proxies.extend(r.text.splitlines())
        except: continue
    return clean_proxy_list(proxies)

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        # Har dafa browser signature tabdeel hoga taake Telegram block na kare
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500,600)}.36',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code == 429:
            print("⚠️ Telegram ne Render IP ko Temporary Limit kiya hai. Free proxies use kar raha hoon bypass ke liye...", flush=True)
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            return [int(p.get('data-post').split('/')[-1]) for p in posts[-5:] if p.get('data-post')]
    except: pass
    return []

def hit_view_worker(post_id, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://t.me/s/{CHANNEL_USERNAME}'
    }
    try:
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=2.0)
        if r.status_code == 200 and "views" in r.text:
            return True
    except: pass
    return False

def fire_fast_views(post_id, target_views, proxy_pool, workers_count=70):
    random.shuffle(proxy_pool)
    success_count = 0
    with ThreadPoolExecutor(max_workers=workers_count) as executor:
        futures = [executor.submit(hit_view_worker, post_id, proxy) for proxy in proxy_pool[:target_views * 5]]
        for fut in futures:
            if fut.result():
                success_count += 1
                if success_count >= target_views:
                    break
    return success_count

def main():
    print("======================================================", flush=True)
    print("⚡ HYPER-DRIVE PRIORITIZED TRADING ENGINE v4 (ANTI-LOCK)", flush=True)
    print("======================================================", flush=True)
    
    # Starting setup
    post_ids = get_recent_post_ids()
    if post_ids:
        last_known_latest_id = post_ids[-1]
    else:
        # Agar block ho to safe guess pichli settings se uthaye
        last_known_latest_id = 1325 
        
    channel_history_tracker = {}
    
    while True:
        current_posts = get_recent_post_ids()
        
        # Fallback mechanism: Agar telegram page response na de to last ID ko monitor karte raho auto-incremented guess se
        if not current_posts:
            print("🔗 Scanner scanning via sequential guess pipeline...", flush=True)
            current_posts = [last_known_latest_id, last_known_latest_id + 1]
            
        latest_id = current_posts[-1]
        
        if latest_id > last_known_latest_id:
            print(f"🚨 NEW SIGNAL TRIGGERED IN PIPELINE (ID: {latest_id})!", flush=True)
            last_known_latest_id = latest_id
            
            pool = get_ultra_proxy_pool()
            sent_instant = fire_fast_views(latest_id, 80, pool, workers_count=70)
            print(f"💥 Delivered {sent_instant} views instantly to New Post {latest_id}.", flush=True)
            channel_history_tracker[latest_id] = sent_instant
            continue
            
        print("📊 Updating channel matrix elements...", flush=True)
        pool = get_ultra_proxy_pool()
        
        for pid in current_posts[-3:]: # Sirf top 3 par focused rakhein taake system load kam ho
            ultimate_target = random.randint(600, 900) if pid == latest_id else random.randint(1500, 1900)
            current_sent = channel_history_tracker.get(pid, 0)
            
            if current_sent >= ultimate_target: continue
                
            sent = fire_fast_views(pid, random.randint(40, 70), pool, workers_count=35)
            channel_history_tracker[pid] = current_sent + sent
            print(f" -> Post {pid}: Overall [{channel_history_tracker[pid]}/{ultimate_target}]", flush=True)
            time.sleep(4)
            
        time.sleep(15)

if __name__ == "__main__":
    main()
        
