import requests
import time
import random
from bs4 import BeautifulSoup

CHANNEL_USERNAME = "https://t.me/Gold_Expert_Fx77"

def get_free_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url)
        if response.status_code == 200: return response.text.splitlines()
    except: return []

def get_recent_post_ids():
    # Yeh function pichli 4 posts ki IDs nikalega taake purani posts bhi boost hoti rahein
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            # Pichli 4 posts ki IDs return karega
            ids = [int(p.get('data-post').split('/')[-1]) for p in posts[-4:] if p.get('data-post')]
            return ids
    except Exception as e:
        print(f"Error fetching recent posts: {e}")
    return []

def hit_view(post_id, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=4)
        if r.status_code == 200 and "views" in r.text: return True
    except: pass
    return False

def boost_channel_ecosystem():
    post_ids = get_recent_post_ids()
    if not post_ids: return

    proxies = get_free_proxies()
    if not proxies: return

    print(f"🔄 Ecosystem Boost Active for Posts: {post_ids}")
    
    # Har post ke liye alag random target (New wali par zyada, puraniyon par extra jump)
    # Is tarah daily/yesterday views 1700-2000 easily touch kar mien ge
    for post_id in post_ids:
        # Agar sab se latest post hai to 600-850, baki pichli posts par extra add-on views
        is_latest = (post_id == post_ids[-1])
        target = random.randint(600, 850) if is_latest else random.randint(200, 400)
        
        successful = 0
        random.shuffle(proxies) # Proxies ko mix karna taake har post ko different IPs milein
        
        for proxy in proxies[:target]: # Loop limit based on target
            if hit_view(post_id, proxy):
                successful += 1
                # Natural gap based on post age
                time.sleep(random.uniform(2, 5) if is_latest else random.uniform(5, 10))
                
        print(f"✅ Post {post_id} boosted with {successful} views.")

def main():
    print("🚀 Advanced Ecosystem Trading Bot Active on Render Premium...")
    while True:
        boost_channel_ecosystem()
        # Har 15 se 20 mint baad poore channel ka circle lagaye gaa
        print("💤 Cycle complete. Waiting 15 minutes for next organic wave...")
        time.sleep(900) 

if __name__ == "__main__":
    main()
        
