import requests
import bs4

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

all = []


'''
attributes = {
    "bgcolor": "black",
    "cellspacing": "1",
    "cellpadding": "1",
    "align": "center",
    "width": "80%"
}


for i in range(1, 51):
    url = f"http://www.world-diplomacy-database.com/php/ranking/ranking_class.php?TRI=1&PAGE={i}&id_ranking=3"
    response = requests.get(url, headers={"User-Agent": user_agent})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', attrs=attributes)
    all.append(table)

with open("diplomacy.html", "w") as f:
    f.write("<html><body>")
    for table in all:
        f.write(str(table))
    f.write("</body></html>")
'''

attributes = {
    "align": "center",
    "bgcolor": "black",
    "cellpadding": "1",
    "cellspacing": "1",
    "width": "80%"
}

for i in range(1, 75):
    url = f"http://www.world-diplomacy-database.com/php/ranking/ranking_class.php?TRI=1&PAGE={i}&id_ranking=2"
    response = requests.get(url, headers={"User-Agent": user_agent})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', attrs=attributes)
    all.append(table)

with open("diplomacy.html", "w") as f:
    f.write("<html><body>")
    for table in all:
        f.write(str(table))
    f.write("</body></html>")