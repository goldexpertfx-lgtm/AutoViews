import requests
import time
import random
from bs4 import BeautifulSoup
import re

# Final Configuration for your Trading Channel
CHANNEL_USERNAME = "Gold_Expert_Fx77"

def clean_proxy_list(raw_proxies):
    """Proxies ko format karne aur clean karne ke liye"""
    cleaned = []
    for proxy in raw_proxies:
        proxy = proxy.strip()
        if proxy and not proxy.startswith('#'):
            # Agar sirf IP:Port ho to format sahi karein
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', proxy):
                cleaned.append(proxy)
    return list(set(cleaned))

def get_high_quality_free_proxies():
    """5 alag premium quality free proxy sources ka pool"""
    print("🔄 Fetching fresh proxies from 5 premium backup sources...")
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
            # Render context mein headers lagana zaroori hai taake APIs block na karein
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                lines = response.text.splitlines()
                proxies.extend(lines)
        except Exception as e:
            print(f"⚠️ Source down, skipping: {url.split('/')[2]}")
            continue
            
    cleaned_pool = clean_proxy_list(proxies)
    print(f"🔥 Total Live Proxies Loaded into Pool: {len(cleaned_pool)}")
    return cleaned_pool

def get_recent_post_ids():
    """Pichli 4 posts ki live IDs fetch karne ke liye"""
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        r = requests.get(url, headers=headers, timeout=12)
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
        print(f"❌ Error connecting to Telegram Web View: {e}")
    return []

def hit_view_with_headers(post_id, proxy):
    """Telegram views page par hit karne ka real browser technique"""
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
    
    # Real looking headers ka rotation
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': f'https://t.me/s/{CHANNEL_USERNAME}',
        'Connection': 'close'
    }
    
    try:
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=4)
        # Telegram hit count karne ke liye page par 'views' class lazmi honi chahiye
        if r.status_code == 200 and "views" in r.text:
            return True
    except:
        pass
    return False

def run_trading_ecosystem_cycle():
    """Ecosystem loop: New post ko fast aur old posts ko 1700-2000 views tak hit karega"""
    post_ids = get_recent_post_ids()
    if not post_ids:
        print("❌ Telegram preview page respond nahi kar raha. Retrying next cycle.")
        return

    proxies = get_high_quality_free_proxies()
    if not proxies or len(proxies) < 50:
        print("❌ Working proxies nahi milien. Proxy scrapers blocked.")
        return

    print(f"🎯 Target Posts detected for Boosting: {post_ids}")
    
    # Pichli posts par cycle chalana
    for post_id in post_ids:
        is_latest = (post_id == post_ids[-1])
        
        # Agar latest post hai to 600-850 views ka target, puraniyo par extra top-up taake 2K ho sakein
        target = random.randint(600, 850) if is_latest else random.randint(250, 450)
        
        successful_views = 0
        random.shuffle(proxies)
        
        print(f"⚡ Starting push for Post ID: {post_id} (Target: {target} Views)")
        
        for proxy in proxies:
            if successful_views >= target:
                break
                
            if hit_view_with_headers(post_id, proxy):
                successful_views += 1
                
                # Render logs ko clean aur interactive rakhne ke liye
                if successful_views % 50 == 0:
                    print(f" -> Post {post_id}: [{successful_views}/{target}] Delivered successfully.")
                
                # Trading curve delay (Latest post fast, older posts slow)
                if is_latest:
                    time.sleep(random.uniform(1.5, 3.5)) # Fast rush for VIP signals
                else:
                    time.sleep(random.uniform(4.0, 8.0)) # Gradual drop for old posts
                    
        print(f"✅ Finished Loop for Post {post_id}. Total Added in this wave: {successful_views}")

def main():
    print("======================================================")
    print("🚀 PREMIUM TELEGRAM TRADING VIEW ENGINE ACTIVE ON RENDER")
    print(f"📈 Channel: @{CHANNEL_USERNAME} | Plan: Premium Continuous")
    print("======================================================")
    
    while True:
        try:
            run_trading_ecosystem_cycle()
        except Exception as global_error:
            print(f"⚠️ Runtime warning encountered: {global_error}")
            
        # Har 12 se 15 minute ke baad naya checker run hoga
        sleep_time = random.randint(720, 900)
        print(f"💤 Wave complete. Keeping Render active, sleeping for {sleep_time // 60} minutes...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
    
