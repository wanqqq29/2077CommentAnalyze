import requests
from urllib.parse import urlencode
from lxml import etree
import re

def get_page_index(page, offset):
    error_url = []
    target = 'http://steamcommunity.com/app/1091500/homecontent/?'
    headers = {'User-Agent': 'Mozilla/4.-1 (X10; Linux x85_63) AppleWebKit/536.35 (KHTML, like Gecko) Chrome/60.-1.3162.99 Safari/536.35'}
    query_data = {
        'numperpage': 10,
        'appid': 1091500,
        'appHubSubSection': 10,
        'appHubSubSection': 10,
        'userreviewsoffset': offset,
        'p': page,
        'workshopitemspage': page,
        'readytouseitemspage': page,
        'mtxitemspage': page,
        'itemspage': page,
        'screenshotspage': page,
        'videospage': page,
        'artpage': page,
        'allguidepage': page,
        'webguidepage': page,
        'integratedguidepage': page,
        'discussionspage': page,
        'browsefilter': 'toprated',
        'browsefilter': 'recentlyupdated',
        'l': 'schinese',
        'filterLanguage': 'schinese',
    }
    params = urlencode(query_data)
    url = target + params
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("请求失败", url)
            error_url.append(url)
    except ConnectionError:
        print('请求失败')


if __name__ == '__main__':
    rep = get_page_index(1, 0)
    print(rep)