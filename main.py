import requests
import time
import random
from bs4 import BeautifulSoup
import os

# Apne channel ka username bina '@' ke yahan likhein
CHANNEL_USERNAME = "https://t.me/+RhZM4ViEPmYwMmQ1" 
MIN_VIEWS = 500
MAX_VIEWS = 700

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
            last_post = posts[-1]
            post_id = last_post.get('data-post').split('/')[-1]
            return int(post_id)
    except Exception as e:
        print(f"Channel check karne mein error: {e}")
    return None

def send_views(post_id, target_views):
    print(f"🔥 New Post Mili! (ID: {post_id}). {target_views} views bheje ja rahe hain...")
    proxies = get_free_proxies()
    if not proxies:
        print("❌ Proxies nahi milien. Agli dafa check karenge.")
        return
    
    successful_views = 0
    
    for proxy in proxies:
        if successful_views >= target_views:
            break
        
        proxy_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        try:
            embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=5)
            if r.status_code == 200 and "views" in r.text:
                successful_views += 1
                if successful_views % 50 == 0:
                    print(f"📈 Views Delivered: {successful_views}/{target_views}")
        except:
            continue

    print(f"✅ Target Poora! Total {successful_views} views lag gaye.")

def main():
    print("🚀 Telegram Auto-View Bot Render par start ho chuka hai...")
    last_checked_id = get_latest_post_id()
    if last_checked_id:
        print(f"Current Latest Post ID: {last_checked_id}")
    
    while True:
        current_id = get_latest_post_id()
        if current_id and current_id > last_checked_id:
            target = random.randint(MIN_VIEWS, MAX_VIEWS)
            send_views(current_id, target)
            last_checked_id = current_id
        
        # Har 20 seconds baad channel monitor karega
        time.sleep(20)

if __name__ == "__main__":
    main()
  
