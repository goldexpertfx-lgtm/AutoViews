import requests
import time
import random
from bs4 import BeautifulSoup
import re
import sys

CHANNEL_USERNAME = "Gold_Expert_Fx77"

def clean_proxy_list(raw_proxies):
    cleaned = []
    for proxy in raw_proxies:
        proxy = proxy.strip()
        if proxy and not proxy.startswith('#'):
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', proxy):
                cleaned.append(proxy)
    return list(set(cleaned))

def get_high_quality_free_proxies():
    print("🔄 Fetching fresh proxies from 5 premium backup sources...", flush=True)
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http"
    ]
    
    for url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=6)
            if response.status_code == 200:
                proxies.extend(response.text.splitlines())
        except:
            continue
            
    cleaned_pool = clean_proxy_list(proxies)
    print(f"🔥 Total Live Proxies Loaded into Pool: {len(cleaned_pool)}", flush=True)
    return cleaned_pool

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            ids = []
            for p in posts[-4:]:
                data_post = p.get('data-post')
                if data_post and '/' in data_post:
                    ids.append(int(data_post.split('/')[-1]))
            return ids
    except Exception as e:
        print(f"❌ Error connecting to Telegram: {e}", flush=True)
    return []

def hit_view_with_headers(post_id, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://t.me/s/{CHANNEL_USERNAME}',
        'Connection': 'close'
    }
    try:
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=3)
        if r.status_code == 200 and "views" in r.text:
            return True
    except:
        pass
    return False

def run_trading_ecosystem_cycle():
    post_ids = get_recent_post_ids()
    if not post_ids:
        print("❌ Telegram preview page respond nahi kar raha.", flush=True)
        return

    proxies = get_high_quality_free_proxies()
    if not proxies or len(proxies) < 10:
        print("❌ Working proxies nahi milien.", flush=True)
        return

    print(f"🎯 Target Posts detected for Boosting: {post_ids}", flush=True)
    
    for post_id in post_ids:
        is_latest = (post_id == post_ids[-1])
        target = random.randint(600, 850) if is_latest else random.randint(250, 450)
        successful_views = 0
        random.shuffle(proxies)
        
        print(f"⚡ Starting push for Post ID: {post_id} (Target: {target} Views)", flush=True)
        
        for proxy in proxies:
            if successful_views >= target:
                break
                
            if hit_view_with_headers(post_id, proxy):
                successful_views += 1
                if successful_views % 20 == 0:
                    print(f" -> Post {post_id}: [{successful_views}/{target}] Delivered successfully.", flush=True)
                
                if is_latest:
                    time.sleep(random.uniform(1.5, 3.5))
                else:
                    time.sleep(random.uniform(4.0, 7.0))
                    
        print(f"✅ Finished Loop for Post {post_id}. Total: {successful_views}", flush=True)

def main():
    print("======================================================", flush=True)
    print("🚀 PREMIUM TELEGRAM TRADING VIEW ENGINE ACTIVE ON RENDER", flush=True)
    print(f"📈 Channel: @{CHANNEL_USERNAME}", flush=True)
    print("======================================================", flush=True)
    
    while True:
        run_trading_ecosystem_cycle()
        # Pehle cycle ke baad 12-15 mint sleep karega
        sleep_time = random.randint(720, 900)
        print(f"💤 Wave complete. Next wave in {sleep_time // 60} minutes...", flush=True)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
    
