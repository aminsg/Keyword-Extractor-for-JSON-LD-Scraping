import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# خواندن لینک‌ها از فایل links.txt
def read_links(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

# تابع برای استخراج کلمه کلیدی از JSON-LD
def extract_keywords_from_json_ld(soup):
    json_ld_script = soup.find("script", {"type": "application/ld+json"})
    keywords_json_ld = None
    if json_ld_script:
        try:
            json_data = json.loads(json_ld_script.string)
            # جستجو برای کلمه کلیدی در ساختار JSON
            for item in json_data["@graph"]:
                if "keywords" in item:
                    keywords_json_ld = item["keywords"]
                    break
        except json.JSONDecodeError:
            keywords_json_ld = None
    return keywords_json_ld

# تابع برای استخراج اطلاعات
def extract_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # استخراج کلمه کلیدی از JSON-LD
    keywords_json_ld = extract_keywords_from_json_ld(soup)
    
    return keywords_json_ld

# ذخیره اطلاعات در فایل متنی
def save_to_file(output_file, urls):
    with open(output_file, "w", encoding="utf-8") as file:
        for i, url in enumerate(tqdm(urls, desc="Processing", unit="link")):
            keywords_json_ld = extract_info(url)
            file.write(f"URL: {url}\nKeywords (JSON-LD): {keywords_json_ld if keywords_json_ld else 'کلمه کلیدی JSON-LD یافت نشد'}\n\n")

# خواندن لینک‌ها از فایل links.txt
urls = read_links("links.txt")

# ذخیره نتایج در output.txt
save_to_file("output.txt", urls)
