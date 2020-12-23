import requests
from lxml import etree
import re

burp0_url = "https://steamcommunity.com:443/app/1091500/homecontent/?userreviewscursor=AoIFP%2FTju8AAAAB95r%2B4Ag%3D%3D&userreviewsoffset=20&p=1&workshopitemspage=3&readytouseitemspage=3&mtxitemspage=3&itemspage=3&screenshotspage=3&videospage=3&artpage=3&allguidepage=3&webguidepage=3&integratedguidepage=3&discussionspage=3&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=1091500&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=default&searchText=&forceanon=1"
burp0_cookies = {"steamCountry": "HK%7C01b1b474dc118b08a61c746c53f5b7c8", "sessionid": "06abdbe835771b114114e465", "recentlyVisitedAppHubs": "1091500", "timezoneOffset": "28800,0", "_ga": "GA1.2.1685764198.1608514170", "_gid": "GA1.2.1921152134.1608514170", "app_impressions": "1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|440@2_100100_100101_100106|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_|1091500@2_9_100010_"}
burp0_headers = {"Connection": "close", "Accept": "text/javascript, text/html, application/xml, text/xml, */*", "X-Prototype-Version": "1.7", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://steamcommunity.com/app/1091500/reviews/?browsefilter=toprated&snr=1_5_100010_", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "If-Modified-Since": "Mon, 21 Dec 2020 08:28:00 GMT"}
TotalFbr = [] #所有发布人
TotalDate = [] #所有发布时间
TotalReview = [] #所有评论

page = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).text

page = re.compile(',',re.I).sub('',page)
page = re.compile('<br>',re.I).sub('',page)
Xpage = etree.HTML(page)

# Fbr = Xpage.xpath('.//div[@class="apphub_friend_block"]/div/a[1]/text()') # 提取发布人
# for a in range(0,len(Fbr)):
#     TotalFbr.append(Fbr[a])
# print(len(TotalFbr))
# print(TotalFbr)
#
# Date = Xpage.xpath('.//div[@class="date_posted"]/text()') # 提取发布时间
# for b in range(0,len(Date)):
#     TotalDate.append(Date[b])
# print(len(TotalDate))
# print(TotalDate)

Review = Xpage.xpath('.//*[@class="apphub_CardTextContent"]/text()')# 提取评论
for c in range(0,len(Review)): #对评论进行清理
    Review1 = list(map(lambda x : re.sub("\n?", '', x), Review))
    Review1 = list(map(lambda x : re.sub("\r?", '', x), Review1))
    Review1 = list(map(lambda x : re.sub("\t?", '', x), Review1))
    if len(Review1[c]) != 0:
        TotalReview.append(Review1[c])
print(len(TotalReview))
print(TotalReview)
