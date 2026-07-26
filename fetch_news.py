import urllib.request
import xml.etree.ElementTree as ET
import json
import html

# مصادر أخبار الذكاء الاصطناعي (RSS Feeds)
RSS_URLS = [
    "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=ar&gl=EG&ceid=EG:ar", # أخبار جوجل بالتحليل العربي
    "https://techcrunch.com/category/artificial-intelligence/feed/" # تك كرنش العالمي
]

def fetch_ai_news():
    articles = []
    
    for url in RSS_URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            xml_data = urllib.request.urlopen(req).read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item')[:5]:  # يجيب أحدث 5 أخبار من كل مصدر
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else '#'
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                articles.append({
                    "title": html.unescape(title),
                    "link": link,
                    "date": pub_date[:16] if pub_date else ''
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    # حفظ الأخبار في ملف json ليقرأه الموقع
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        print("News updated successfully!")

if __name__ == "__main__":
    fetch_ai_news()
