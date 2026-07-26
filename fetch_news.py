import urllib.request
import xml.etree.ElementTree as ET
import json
import html
import re

RSS_URLS = [
    "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=ar&gl=EG&ceid=EG:ar",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]

def extract_image(item, raw_xml_str):
    # Search for media:content or enclosure image url
    media = item.find('{http://search.yahoo.com/mrss/}content')
    if media is not None and 'url' in media.attrib:
        return media.attrib['url']
    
    enclosure = item.find('enclosure')
    if enclosure is not None and 'url' in enclosure.attrib:
        return enclosure.attrib['url']
        
    # Search inside description using regex
    desc = item.find('description')
    if desc is not None and desc.text:
        img_match = re.search(r'src=["\'](https?://[^"\']+\.(?:jpg|jpeg|png|webp))["\']', desc.text)
        if img_match:
            return img_match.group(1)
            
    # Default fallback AI tech image
    return "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=800&q=80"

def fetch_ai_news():
    articles = []
    
    for url in RSS_URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            xml_data = urllib.request.urlopen(req).read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall('.//item')[:6]:
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else '#'
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                img_url = extract_image(item, str(xml_data))
                
                articles.append({
                    "title": html.unescape(title),
                    "link": link,
                    "date": pub_date[:16] if pub_date else '',
                    "image": img_url
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
        print("News with images updated successfully!")

if __name__ == "__main__":
    fetch_ai_news()
