#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pyhanlp import *

import zipfile
import os
from pyhanlp.static import download, remove_file, HANLP_DATA_PATH


def test_data_path():
    """
    获取测试数据路径，位于$root/data/test，根目录由配置文件指定。
    :return:
    """
    data_path = os.path.join(HANLP_DATA_PATH, 'test')
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    return data_path


## 验证是否存在语料库，如果没有自动下载
def ensure_data(data_name, data_url):
    root_path = test_data_path()
    dest_path = os.path.join(root_path, data_name)
    if os.path.exists(dest_path):
        return dest_path

    if data_url.endswith('.zip'):
        dest_path += '.zip'
    download(data_url, dest_path)
    if data_url.endswith('.zip'):
        with zipfile.ZipFile(dest_path, "r") as archive:
            archive.extractall(root_path)
        remove_file(dest_path)
        dest_path = dest_path[:-len('.zip')]
    return dest_path


chn_senti_corp = ensure_data("reviews", "http://file.hankcs.com/corpus/ChnSentiCorp.zip")
#chn_senti_corp = ensure_data("reviews", "http://file.hankcs.com/corpus/ChnSentiCorp.zip")

## ===============================================
## 以下开始 情感分析


IClassifier = JClass('com.hankcs.hanlp.classification.classifiers.IClassifier')
NaiveBayesClassifier = JClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')

neg = 0
pos = 0

def predict(classifier, text):
    global neg
    global pos
    #print("《%s》 情感极性是 【%s】" % (text, classifier.classify(text)))
    #print(classifier.classify(text))
    if classifier.classify(text) == '不推荐':
        neg += 1
    elif classifier.classify(text) == '推荐':
        pos += 1
    global textaaa
    textaaa = classifier.classify(text)


if __name__ == '__main__':
    classifier = NaiveBayesClassifier()
    #  创建分类器，更高级的功能请参考IClassifier的接口定义
    classifier.train(chn_senti_corp)
    #  训练后的模型支持持久化，下次就不必训练了
    #predict(classifier, "(''垃圾''")