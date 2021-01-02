import requests
from urllib import parse
import json,re,csv,time,os
import pandas as pd
from Python import sentiment_analysis as sa
import jieba
import collections
import webbrowser
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.charts import Gauge
headers = {
        'User-Agent': 'Mozilla/4.-1 (X10; Linux x85_63) AppleWebKit/536.35 (KHTML, like Gecko) Chrome/60.-1.3162.99 Safari/536.35'}

#训练集获取
def Get_train(appid):
    flag = 0
    with open('reviews/pos.txt', "w+") as f:  # 训练集可持续化，读取上次写文件名，这次接着来
        total_reviews_ups = f.read()
    if total_reviews_ups == '':
        total_reviews_up = 0
    else:
        total_reviews_up = int(total_reviews_ups)
    with open('reviews/neg.txt', "w+") as f:  # 训练集可持续化
        total_reviews_downs = f.read()
    if total_reviews_downs == '':
        total_reviews_down = 0
    else:
        total_reviews_down = int(total_reviews_downs)
    for a in range(0,2):
        if flag == 0:
            url = 'https://store.steampowered.com/appreviews/%s?json=1&language=schinese&num_per_page=100'%appid
            page = requests.get(url, headers=headers).text.encode('utf-8')
            Content = json.loads(page)
            RecNum = Content['query_summary']['total_reviews']  #简中评论总条数
            cursor = parse.quote(Content['cursor']) # 将cursor 进行 url编码
            Pagenum = RecNum//100    #评论页数 每页100条
            print('共'+ str(Pagenum) +'页评论')
            print('正在进行第1页评论爬取')
            for b in range(0, len(Content['reviews'])):
                if Content['reviews'][b]['voted_up'] == True:
                    one_review = Content['reviews'][b]['review']
                    one_review_over = re.compile('\[h1]|\[/h1]|\n|\t|\[b]|\[/b]', re.I).sub('', one_review)
                    with open(r'C:\Users\Aris\AppData\Local\Programs\Python\Python38\Lib\site-packages\pyhanlp\static\data\test\reviews/推荐/pos.' + str(total_reviews_up) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(one_review_over)
                    total_reviews_up += 1
                elif Content['reviews'][b]['voted_up'] == False:
                    one_review = Content['reviews'][b]['review']
                    one_review_over = re.compile('\[h1]|\[/h1]|\n|\t|\[b]|\[/b]', re.I).sub('', one_review)
                    with open(r'C:\Users\Aris\AppData\Local\Programs\Python\Python38\Lib\site-packages\pyhanlp\static\data\test\reviews/不推荐/neg.' + str(total_reviews_down) + '.txt', 'w', encoding='utf-8') as f:
                        f.write(one_review_over)
                    total_reviews_down += 1
            with open('reviews/pos.txt', 'w+', encoding='utf-8') as f:
                f.write(str(total_reviews_up))
            with open('reviews/neg.txt', 'w+', encoding='utf-8') as f:
                f.write(str(total_reviews_down))
            print(total_reviews_up)
            print(total_reviews_down)
            flag = 1
        elif flag == 1:
            for c in range(2, 50): #爬取页数
                url = 'https://store.steampowered.com/appreviews/%s?json=1&language=schinese&num_per_page=100&cursor=%s' %(appid, cursor)
                page = requests.get(url, headers=headers).text.encode('utf-8')
                Content = json.loads(page)
                cursor = parse.quote(Content['cursor']) # 将cursor 进行 url编码
                print('正在进行第' + str(c) + '页评论爬取')
                for b in range(0, len(Content['reviews'])):
                    if Content['reviews'][b]['voted_up'] == True:
                        one_review = Content['reviews'][b]['review']
                        one_review_over = re.compile('\[h1]|\[/h1]|\n|\t|\[b]|\[/b]', re.I).sub('', one_review)
                        with open(r'C:\Users\Aris\AppData\Local\Programs\Python\Python38\Lib\site-packages\pyhanlp\static\data\test\reviews/推荐/pos.' + str(total_reviews_up) + '.txt', 'w', encoding='utf-8') as f:
                            f.write(one_review_over)
                        total_reviews_up += 1
                        with open('reviews/pos.txt', 'w+', encoding='utf-8') as f:
                            f.write(str(total_reviews_up))
                    elif Content['reviews'][b]['voted_up'] == False:
                        one_review = Content['reviews'][b]['review']
                        one_review_over = re.compile('\[h1]|\[/h1]|\n|\t|\[b]|\[/b]', re.I).sub('', one_review)
                        with open(r'C:\Users\Aris\AppData\Local\Programs\Python\Python38\Lib\site-packages\pyhanlp\static\data\test\reviews/不推荐/neg.' + str(total_reviews_down) + '.txt', 'w',encoding='utf-8') as f:
                            f.write(one_review_over)
                        total_reviews_down += 1
                        with open('reviews/neg.txt', 'w+', encoding='utf-8') as f:
                            f.write(str(total_reviews_down))
                print(total_reviews_up,total_reviews_down)
        print('pos共' + str(total_reviews_up) + '条数据，neg共' + str(total_reviews_down) + '条数据')

# 评论爬取
def Get_review(appid):
    pice = 0
    flag = 0
    for a in range(0,2):
        if flag == 0:
            url = 'https://store.steampowered.com/appreviews/%s?json=1&language=schinese&num_per_page=100'%appid
            page = requests.get(url, headers=headers).text.encode('utf-8')
            Content = json.loads(page)
            RecNum = Content['query_summary']['total_reviews']  #简中评论总条数
            cursor = parse.quote(Content['cursor']) # 将cursor 进行 url编码
            Pagenum = RecNum//100    #评论页数 每页100条
            print('共'+ str(Pagenum) +'页评论')
            print('正在进行第1页评论爬取')
            total_reviews = []
            for b in range(0,len(Content['reviews'])):
                one_review = Content['reviews'][b]['review']
                one_review_over = re.compile('\n',re.I).sub('',one_review)  #正则处理单条评论
                #one_review_over = re.compile('[b]',re.I).sub('',one_review_over)
                #one_review_over = re.compile('[/b]',re.I).sub('',one_review_over)
                total_reviews.append(one_review_over)  #将评论加入总评论列表
            print('第1页评论爬取完成')
            # print(total_reviews)
            #写入csv
            with open('reviews.csv', 'a+', encoding='utf-8', newline='') as f:
                for i in total_reviews:
                    pice += 1
                    writer = csv.writer(f)
                    writer.writerow([i])
                print('成功写入' + str(pice) + '条')
            time.sleep(1)
            flag = 1
        elif flag == 1:
            for c in range(2,Pagenum-2):  #爬取页数
                url = 'https://store.steampowered.com/appreviews/%s?json=1&language=schinese&num_per_page=100&cursor=%s' %(appid,cursor)
                page = requests.get(url, headers=headers).text.encode('utf-8')
                Content = json.loads(page)
                cursor = parse.quote(Content['cursor']) # 将cursor 进行 url编码
                print('正在进行第'+ str(c) +'页评论爬取')
                try:
                    total_reviews = []
                    for b in range(0,len(Content['reviews'])):
                        one_review = Content['reviews'][b]['review']
                        one_review_over = re.compile('\n', re.I).sub('', one_review)        #正则处理单条评论
                        total_reviews.append(one_review_over)  # 将评论加入总评论列表
                    print('第' + str(c) + '页评论爬取完成')
                    # print(total_reviews)
                    # 写入csv
                    with open('reviews.csv', 'a+', encoding='utf-8', newline='') as f:
                        for i in total_reviews:
                            pice += 1
                            writer = csv.writer(f)
                            writer.writerow([i])
                        print('成功写入' + str(pice) + '条')
                    time.sleep(1)
                except:
                    print('第' + str(c) + '页评论爬取完成')
                    #print(total_reviews)
                    # 写入csv
                    with open('reviews.csv', 'a+', encoding='utf-8', newline='') as f:
                        for i in total_reviews:
                            pice += 1
                            writer = csv.writer(f)
                            writer.writerow([i])
                        print('成功写入' + str(pice) + '条')
    print('评论爬取完成并成功写入reviews.csv，共'+ str(pice) +'条数据')

# 评论处理 去重
def Clear_review():
    frame = pd.read_csv('reviews.csv', engine='python')
    print('处理前数量' + str(len(frame)))
    data = frame.drop_duplicates(keep='first', inplace=False)
    data.to_csv('reviews_over.csv', encoding='utf8',index=None)
    frame2 = pd.read_csv('reviews_over.csv', engine='python')
    print('处理后数量' + str(len(frame2)))
    # subset: column label or sequence of labels, optional    用来指定特定的列，默认所有列
    # keep: {‘first’, ‘last’, False}, default ‘first’ 删除重复项并保留第一次出现的项
    # inplace: boolean, default False 是直接在原来数据上修改还是保留一个副本
    # 数据存入txt
    # text = ''
    # reviews = pd.read_csv('reviews_over.csv', engine='python', header=None, encoding='utf-8')  # pd读取处理完的评论
    # for xxx in range(0, len(reviews)):
    #     text = text + reviews[0][xxx]+ '\n'
    # with open('reviews_over.txt', 'w', encoding='UTF-8') as f:  # 设置文件对象
    #     f.write(text)  # 将字符串写入文件中
# 训练
def Training():
    classifier = sa.NaiveBayesClassifier()  # 创建分类器，更高级的功能请参考IClassifier的接口定义
    classifier.train(sa.chn_senti_corp)  # 训练后的模型支持持久化，下次就不必训练了
    return classifier

# 应用模型对爬取的评论进行分析
def Predict(classifier):
    reviews = pd.read_csv('reviews_over.csv', engine='python', header=None, encoding='utf-8') #pd读取处理完的评论
    for xx in range(0,len(reviews)):
        sa.predict(classifier,reviews[0][xx])
    print('有'+str(sa.pos)+'人,'+str(sa.pos/(sa.pos+sa.neg))+'%,''的人推荐购买这个游戏,'+str(sa.neg)+'人,'+str(sa.neg/(sa.pos+sa.neg))+'%的人不推荐购买这个游戏,')
    if sa.pos > sa.neg:
        print('总之，这个游戏买就对了，绝对不亏！')
    else:
        print('买前请三思，推荐度仅为'+str(sa.pos/(sa.pos+sa.neg))+'%')



#可视化
def Pycharts():
    file = open('reviews_over.txt', 'r', encoding='UTF-8')  # 路径自定义
    text = file.read()
    file.close()
    cut_text = " ".join(jieba.cut(text))
    words = cut_text.split()
    words1 = [re.sub("[\，\。\！\；\？\、\”\“]", '', word) for word in words]  # 去掉标点符号
    #停用词 自定义词典
    jieba.load_userdict("dict.txt")
    stopwords_file = "stopwords.txt"
    stop_f = open(stopwords_file, "r", encoding='utf-8')
    stop_words = list()
    for line in stop_f.readlines():
        line = line.strip()
        if not len(line):
            continue
        stop_words.append(line)
    stop_f.close
    DIY_stopwords = ['一个','没有','说','玩','做','里','中','-','⣿','','感','spoiler','2','点','完','·','\\','4','走','一款',"'",'会','没',',','游戏','帧']
    for line in range(0,len(DIY_stopwords)):
        stop_words.append(DIY_stopwords[line])
    words2 = [word for word in words1 if word not in stop_words] #停用词
    wordcounts = collections.Counter(words2).most_common(200)
    #print(wordcounts)

    #词云
    cloud = (
        WordCloud(opts.InitOpts(width="100%", height="950px"))
            .add("词频统计", wordcounts, word_size_range=[20, 300], )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="词频统计", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
            .render("html/wordcloud_diamond.html")
    )

    gauge = (
        Gauge(init_opts=opts.InitOpts(width="500px", height="500px"))
                    .add(series_name="推荐指数", data_pair=[["推荐率", sa.pos/(sa.pos+sa.neg)]])
                    .set_global_opts(
                    legend_opts=opts.LegendOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{a} <br/>{b} : {c}%"),
                )
                    .set_series_opts(
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(
                            color=[[0.3, "#67e0e3"], [0.7, "#37a2da"], [1, "#fd666d"]], width=30
                        )
                    )
                )
                    .render("html/gauge_change_color.html")
    )

    webbrowser.open('file:///F:/Project/WorkSpace/2077CommentAnalyze/Python/html/index.html')







if __name__ == '__main__':
    Get_train(1174180)
    #Get_review(1091500) # 评论爬取
    #Clear_review()  # 去重
    # 进行推荐度分析：
    #classifier = Training()
    #Predict(classifier)
    #Pycharts() #生成可视化图表



