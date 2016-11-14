import requests
from bs4 import BeautifulSoup
import bs4

html = requests.get("http://www.feixunwangluo.com/page/testss.html")
# print(html.text)
with open("html.txt", 'w', encoding='utf-8') as f:
    f.write(html.text)

soup = BeautifulSoup(open('html.txt'))
# print(soup.prettify()) # display all
# print(soup.find_all("div", attrs={"class": "testvpnitem"}))
# print(soup.find_all("div", class_="testvpnitem"))
tags1 = soup.find_all("div", attrs={"class": "testvpnitem"})
for testtag in tags1:
    i=1
    for t in testtag.descendants:
        if type(t) == bs4.element.NavigableString:
            print(t.string+"-----"+str(i))
            i+=1
        #print(str(type(t)) + ":" + str(t))
    # for tag in testtag.descendants:
    #     if tag.name == 'span':
    #         print(tag.string)
print(type(tags1[0]))
soup2=BeautifulSoup(str(tags1[0]))
print(soup2.prettify())