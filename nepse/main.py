from bs4 import BeautifulSoup


with open("index.html", "r", encoding="utf-8") as file:
    html_content = file.read()


soup = BeautifulSoup(html_content, "html5lib")


print(soup.title.text)


ul = soup.find('ul', id="nepseticker")


label = ul.find('li')

for item in label.find_all('a'):
    print(item.attrs['href'])