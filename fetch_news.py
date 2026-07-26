import urllib.request
import xml.etree.ElementTree as ET
import json
import html
import re

RSS_URLS = [
    "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=ar&gl=EG&ceid=EG:ar",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]

def get_og_image(article_url):
    """سحب الصورة الأصلية للمقال من الرابط مباشرة"""
    try:
        req = urllib.request.Request(article_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html_content = urllib.request.urlopen(req, timeout=4).read().decode('utf-8', errors='ignore')
        
        # البحث عن صورة og:image في صفحة الخبر الأصلية
        match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html_content)
        if not match:
            match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html_content)
            
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def fetch_ai_news():
    articles = []
    
    for url in RSS_URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            xml_data = urllib.request.urlopen(req).read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else '#'
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # جلب الصورة الأصلية من رابط المقال
                original_img = get_og_image(link)
                if not original_img:
                    original_img = "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=800&q=80"
                
                articles.append({
                    "title": html.unescape(title),
                    "link": link,
                    "date": pub_date[:16] if pub_date else '',
                    "image": original_img
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        print("News with ORIGINAL images updated successfully!")

if __name__ == "__main__":
    fetch_ai_news()
