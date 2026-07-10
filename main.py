import requests
import time
import random
from bs4 import BeautifulSoup

# Apne channel ka username bina '@' ke yahan likhein
CHANNEL_USERNAME = "https://t.me/Gold_Expert_Fx77" 

def get_free_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
    except:
        return []

def get_latest_post_id():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            return int(posts[-1].get('data-post').split('/')[-1])
    except Exception as e:
        print(f"Channel check karne mein error: {e}")
    return None

def send_views_gradually(post_id):
    # Phase 1: Pehle 1 ghante mein ~300 views
    phase1_target = random.randint(280, 320)
    # Phase 2: Agle 3 ghantoun mein mazeed ~300 views (Total 4 ghante mein 500-700)
    phase2_target = random.randint(220, 380)
    
    total_target = phase1_target + phase2_target
    print(f"🔥 New Post {post_id} Detected! Planning {total_target} views over 4 hours...")
    
    proxies = get_free_proxies()
    if not proxies:
        print("❌ Proxies nahi milien.")
        return

    successful_views = 0
    proxy_index = 0

    # --- PHASE 1: Target ~300 views in 1 Hour (3600 seconds) ---
    # 3600 / 300 = ~12 seconds delay per view
    print(f"⏳ Phase 1 Started: Sending {phase1_target} views in the first hour...")
    while successful_views < phase1_target and proxy_index < len(proxies):
        proxy = proxies[proxy_index]
        proxy_index += 1
        
        if hit_view(post_id, proxy):
            successful_views += 1
            if successful_views % 30 == 0:
                print(f"📈 [Phase 1] Views: {successful_views}/{total_target}")
            # Natural delay: 10 se 14 seconds ka random gap
            time.sleep(random.uniform(10, 14))
        else:
            time.sleep(1) # Agar proxy kharab ho to foran agli check kare

    # --- PHASE 2: Target Remaining views in next 3 Hours (10800 seconds) ---
    # 10800 / 300 = ~36 seconds delay per view
    print(f"⏳ Phase 2 Started: Sending remaining views slowly over the next 3 hours...")
    while successful_views < total_target:
        # Nayi proxies fetch karna agar purani khatam ho jayein
        if proxy_index >= len(proxies):
            proxies = get_free_proxies()
            proxy_index = 0
            if not proxies:
                print("❌ No more proxies available. Ending task.")
                break

        proxy = proxies[proxy_index]
        proxy_index += 1
        
        if hit_view(post_id, proxy):
            successful_views += 1
            if successful_views % 30 == 0:
                print(f"📈 [Phase 2] Views: {successful_views}/{total_target}")
            # Lamba delay: 30 se 42 seconds ka random gap taake speed slow ho jaye
            time.sleep(random.uniform(30, 42))
        else:
            time.sleep(1)

    print(f"✅ 4-Hour Schedule Complete! Total {successful_views} views delivered naturally.")

def hit_view(post_id, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=5)
        if r.status_code == 200 and "views" in r.text:
            return True
    except:
        pass
    return False

def main():
    print("🚀 Natural Speed Telegram Auto-View Bot Started on Render...")
    last_checked_id = get_latest_post_id()
    
    while True:
        current_id = get_latest_post_id()
        if current_id and current_id > last_checked_id:
            # Yeh function ab poore 4 ghante background mein chalega views dene ke liye
            send_views_gradually(current_id)
            last_checked_id = current_id
        
        # Har 30 seconds baad check karega new post ke liye
        time.sleep(30)

if __name__ == "__main__":
    main()
    
