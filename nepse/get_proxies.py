import requests
from bs4 import BeautifulSoup

url = "https://free-proxy-list.net/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

div = soup.find('div', class_='fpl-list')
table = div.find('table')

headers = [th.text.strip() for th in table.find('thead').find_all('th')]

proxy_list = []

for row in table.find('tbody').find_all('tr'):
    cells = row.find_all('td')
    if len(cells) != len(headers):
        continue
    
    row_data = {header: cell.text.strip() for header, cell in zip(headers, cells)}
    
    # Filter for proxies with HTTPS = 'yes'
    if row_data.get("Https", "").lower() == "yes":
        proxy = f"https://{row_data['IP Address']}:{row_data['Port']}"
        proxy_list.append(proxy)

# Save proxies to file
with open("proxy_list.txt", "w") as f:
    for proxy in proxy_list:
        f.write(proxy + "\n")

print(f"Saved {len(proxy_list)} HTTPS proxies to proxy_list.txt")
