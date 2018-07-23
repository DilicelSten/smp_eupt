# coding=utf-8
"""
created on:2018/7/6
author:DilicelSten
target:对原始向量进行归一化处理
finished on:2018/7/7
"""
import numpy as np
import csv
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
"""
13维特征：id,features
1.语义困惑度
2.主题困惑度
3.句子特征
4.标点符号
读取原始向量并且尝试3种归一化方法
"""
header = ['id', 'ppl_range', 'ppl_worst', 'ppl_mean3', 'ppl_best', 'ppl_variance', 'topic_num', 'topic_shan', 'sen_num', 'len_mean', 'ico1', 'ico2', 'ico3', 'ico4']

methods = ['min_max', 'normalize', 'standard']
sample = ['test_result.csv', 'train_result.csv', 'validation_result.csv']


def sta_method(lst):
    """
    标准化
    :param lst: 原始向量
    :return:
    """
    arr = np.array(lst)
    ss = StandardScaler()
    result = ss.fit_transform(arr)
    return result


def minmax_method(lst):
    """
    最大最小
    :param lst:原始向量
    :return:
    """
    arr = np.array(lst)
    mm = MinMaxScaler()
    result = mm.fit_transform(arr)
    return result


def process_result(file_path):
    """
    读取结果向量并且进行归一化写入
    :param file_path:原始文件路径
    :return:
    """
    for each in sample:
        new_vector = []
        path = file_path + each
        with open(path, 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                line = line.strip('\r\n')
                term = line.split(",")
                d_id = term[0]
                vector = []
                for i in range(1, len(term)):
                    vector.append(float(term[i]))
                nor_result = minmax_method(vector)
                result = nor_result.tolist()
                result.insert(0, d_id)
                new_vector.append(result)
        file = open(file_path.replace("original", "min_max")+each, 'w')
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        data = []
        for each in new_vector:
            dic = dict(map(lambda x, y: [x, y], header, each))
            data.append(dic)
        writer.writerows(data)


if __name__ == '__main__':
    file_dir = '/media/iiip/数据/duanduan/data/result/original/'
    process_result(file_dir)