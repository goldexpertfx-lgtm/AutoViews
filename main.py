import requests
import time
import random
from bs4 import BeautifulSoup

CHANNEL_USERNAME = "Gold_Expert_Fx77"

def get_free_proxies():
    # 3 alag sources se proxies jama karne ka backup system
    proxies = []
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                lines = response.text.splitlines()
                proxies.extend(lines)
        except:
            continue
            
    # Duplicate IPs remove karna
    proxies = list(set(proxies))
    print(f"Total Scraped Proxies for Pool: {len(proxies)}")
    return proxies

def get_recent_post_ids():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    try:
        # User-Agent lagana zaroori hai taake Telegram block na kare
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.find_all('div', class_='tgme_widget_message')
        if posts:
            ids = [int(p.get('data-post').split('/')[-1]) for p in posts[-4:] if p.get('data-post')]
            return ids
    except Exception as e:
        print(f"Error fetching recent posts: {e}")
    return []

def hit_view(post_id, proxy):
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        embed_url = f"https://t.me/{CHANNEL_USERNAME}/{post_id}?embed=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'https://t.me/s/{CHANNEL_USERNAME}'
        }
        # Connection foran close karne ke liye timeout kam rakha hai
        r = requests.get(embed_url, proxies=proxy_dict, headers=headers, timeout=3)
        if r.status_code == 200 and "views" in r.text: 
            return True
    except: 
        pass
    return False

def boost_channel_ecosystem():
    post_ids = get_recent_post_ids()
    if not post_ids: 
        print("❌ Posts nahi milien. Link ya Content Protection check karein.")
        return

    proxies = get_free_proxies()
    if not proxies or len(proxies) < 10:
        print("❌ Working proxies pool empty.")
        return

    print(f"🔄 Ecosystem Boost Active for Posts: {post_ids}")
    
    for post_id in post_ids:
        is_latest = (post_id == post_ids[-1])
        target = random.randint(600, 850) if is_latest else random.randint(200, 400)
        
        successful = 0
        random.shuffle(proxies)
        
        # Sirf working proxies ko filter karne ke liye loop
        for proxy in proxies:
            if successful >= target:
                break
                
            if hit_view(post_id, proxy):
                successful += 1
                if successful % 20 == 0:
                    print(f"Post {post_id} -> Views Delivered: {successful}/{target}")
                time.sleep(random.uniform(2, 5) if is_latest else random.uniform(5, 10))
                
        print(f"✅ Post {post_id} cycle complete. Delivered: {successful}")

def main():
    print("🚀 Advanced Ecosystem Trading Bot Active on Render Premium...")
    while True:
        boost_channel_ecosystem()
        print("ZL Cycle complete. Waiting 15 minutes...")
        time.sleep(900) 

if __name__ == "__main__":
    main()
    
