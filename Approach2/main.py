import requests
from bs4 import BeautifulSoup
import json
import time
import lxml
import random

def get_random_proxy(proxy_file):
    with open(proxy_file, 'r') as f:
        proxies = f.readlines()
        proxies = [proxy.strip() for proxy in proxies]

    return random.choice(proxies)

def extract_json(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    script_tag = soup.find('body').get_text()
    start = script_tag.find('{')
    end = script_tag.rfind('}') + 1
    json_data = script_tag[start:end]
    return json.loads(json_data)


proxy_file = 'proxy.txt'
user_handle = "vashuvats1"
base_url = f"https://www.codechef.com/recent/user?page={{}}&user_handle={user_handle}"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
headers = {
    "User-Agent": user_agent
}


response = requests.get(base_url.format(0),headers=headers)

data = extract_json(response.text)

max_page = data.get('max_page', 1)
print(max_page)
all_data = []

for page in range(max_page):
    random_proxy = get_random_proxy(proxy_file)
    proxies = {
        "http": random_proxy,
        "https": random_proxy
    }
    response = requests.get(base_url.format(page), proxies=proxies,headers=headers)

    fetched_data = extract_json(response.text)
    
    if 'content' in fetched_data :
        html_content = fetched_data['content']
        page_soup = BeautifulSoup(html_content, 'lxml')
        table = page_soup.select_one(".dataTable")    
        if table:
            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    problem = row.select_one("td:nth-child(2) a").text if row.select_one("td:nth-child(2) a") else None
                    result = row.select_one("td:nth-child(3) span")['title'] if row.select_one("td:nth-child(3) span") else None

                    if problem and result:
                        all_data.append({"Problem Name": problem, "Status": result})
        else:
            print(f"Table not found on page {page}")
    else:
        print(f"No content found on page {page}")
        break  

print(all_data)

