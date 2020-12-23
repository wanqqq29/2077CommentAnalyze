# -*- coding: utf-8 -*-
import requests
from lxml import etree
from urllib.parse import urlencode
import re
from requests.exceptions import ConnectionError
from multiprocessing import Pool
import jieba
from pprint import pprint
from wordcloud import WordCloud
import csv
from collections import Counter
import matplotlib.pyplot as plt
import itertools
import os


def get_page_index(page, offset):
    error_url = []
    target = 'http://steamcommunity.com/app/1091500/homecontent/?'
    headers = {'User-Agent': 'Mozilla/4.-1 (X10; Linux x85_63) AppleWebKit/536.35 (KHTML, like Gecko) Chrome/60.-1.3162.99 Safari/536.35'}
    query_data = {
        'numperpage': 10,
        'appid': 577800,
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


# 获取评论内容
def get_reviews(data):
    html_text = etree.HTML(data)
    reviews_text = html_text.xpath('//div[@class="apphub_CardTextContent"]/text()')
    print(reviews_text)
    return reviews_text


# 清理大量的空列表, 评论中的空格
def data_clean(data):
    clean_data = []
    regex = re.compile(r'[\r\t\n]')
    for li in data:
        cleaned = regex.sub('', li)
        clean_data.append(cleaned)
    return [item for item in clean_data if item]


def save_local(data):
    with open(os.path.join('data', 'revies.txt'), 'w+') as f:
        f.writelines(data)
    f.close()


def reviews_counter():
    jieba.load_userdict("./data/user_dict.txt")
    tokens = []
    stop_words = []
    # 网上找到的中文停词库
    stop_words_list = ['data/stop_words/ baidu_stopword.txt',
                       'data/stop_words/zhs_stopword.txt',
                       'data/stop_words/hagongzh_stopword.txt']
    for file_path in stop_words_list:
        with open(os.path.join(os.path.dirname(__file__), file_path)) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                stop_words.append(line)
            stop_words.append(' ')

    comments = open(os.path.join('data', 'revies.txt'), encoding='utf-8').read()
    seg_lst = jieba.cut(comments, cut_all=False)
    counter = dict()
    for seg in seg_lst:
        if seg not in stop_words:
            tokens.append(seg)
    for token in tokens:
        counter[token] = counter.get(token, 1) + 1
    counter_sort = sorted(counter.items(), key=lambda value: value[1], reverse=True)
    pprint(counter_sort)
    file_path = os.path.join("data", "reviews_word_counter.csv")
    with open(file_path, 'w+', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(counter_sort)


def gen_word_cloud():
    """
    生成词云
    """
    counter = {}
    file_path = os.path.join('data', 'reviews_word_counter.csv')
    with open(file_path, 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in  f_csv:
            counter[row[0]] = counter.get(row[0], int(row[1]))
        pprint(counter)
    file_path = os.path.join('data', 'msyh.ttf')
    wordcloud = WordCloud(font_path=file_path, height=600, width=1200, max_words=400, max_font_size=200).generate_from_frequencies(counter)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    file_path = os.path.join('data', 'wordcloud.jpg')
    wordcloud.to_file(file_path)


def recomment_counter(data):
    reviews_header = {}
    hours = []
    html_text = etree.HTML(data)
    recommendation = html_text.xpath('//div[@class="vote_header"]//div[@class="title"]/text()')
    game_hour = html_text.xpath('//div[@class="vote_header"]//div[@class="hours"]/text()')
    for hour in game_hour:
        hour= re.findall(r'\d*\.\d+', hour)
        hours.append(hour)
    hours = list(itertools.chain.from_iterable(hours))
    for i, item in enumerate(hours):
        reviews_header[item] = recommendation[i]

    with open(os.path.join('data', 'review_header.csv'), 'a', encoding='utf-8') as f:
        w = csv.writer(f)
        for key, value in reviews_header.items():
            w.writerow([key, value])
    f.close()


def counter_recomment():
    counter = {}
    with open(os.path.join('data', 'review_header.csv'), 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if row[1] == '推荐':
                counter['推荐'] = counter.get('推荐', 1) + 1
            else:
                counter['不推荐'] = counter.get('不推荐', 1) + 1
    return counter





def draw_charts(data):
    labels = "recommended", "Not recommended"
    size1 = int(data['推荐']) / int(int(data['推荐']) + int(data['不推荐']))
    size2 = int(data['不推荐']) / int(int(data['推荐']) + int(data['不推荐']))
    sizes = [size1, size2]
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, autopct='%1.2f%%', labels=labels, shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()


def main(page):
    #result = []
    #for page in range(1, 346):
    offset = (page-1) * 10
    html = get_page_index(page, offset)
    #reviews = get_reviews(html)
    #cleaned = data_clean(reviews)
    #result.append(cleaned)
    #res = itertools.chain.from_iterable(result)
    print('保存' + str(page) + '页中……')
    #save_local(list(res))
    recomment_counter(html)


if __name__ == '__main__':
    #pages = [page for page in range(1, 346)]
    #with Pool(5) as p:
    #    p.map(main, pages)
    #main()
    gen_word_cloud()
    #reviews_counter()
    #rep = get_page_index(2, 10)
    #print(rep)
    #header = get_reviews(rep)
    #print(header)
    #recomment_counter(rep)
    #data = counter_recomment()
    #draw_charts(data)
