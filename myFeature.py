# coding=utf-8
"""
created on:2018/7/6
author:DilicelSten
target:确定每个特征并且完成整个流程
finished on:2018/7/7
"""
import data_process
import mySRILM
import numpy as np
import csv

"""
特征说明：
1.语义困惑度衡量
（1）ppl极差
（2）ppl最差
（3）ppl最差top3均值（小于3则为最差）
（4）ppl最好
（5）ppl方差
2.主题困惑度衡量
（6）主题分布超过0.05的个数
（7）主题分布信息熵
3.句子长短
（8）句子个数
（9）句子长度均值
4.标点符号
（10）。。
（11），。/。，
（12）>>>>/]
（13）……
"""

header = ['id', 'ppl_range', 'ppl_worst', 'ppl_mean3', 'ppl_best', 'ppl_variance', 'topic_num', 'topic_shan', 'sen_num', 'len_mean', 'ico1', 'ico2', 'ico3', 'ico4']


def get_ppl(file_path):
    """
    计算该文件所有文档的ppl特征
    :param file_path: 文件路径
    :return:ppl特征列表【极差\最差\最差top3均值（小于3则为最差）\最好\ppl方差】
    """
    lm_path = '/media/iiip/数据/duanduan/data/train_sen.lm'
    ppl_dict = mySRILM.cal_final(file_path, lm_path)
    return ppl_dict


def get_topic(file_path):
    """
    获取主题的两个特征
    :param file_path:文档路径
    :return:
    """
    topic_dict = {}
    with open(file_path.replace(".csv", "_topic.csv"), 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip('\r\n')
        result = []
        d_id, topic1, topic2 = line.split(',')
        result.append(float(topic1))
        result.append(float(topic2))
        topic_dict[int(d_id)] = result
    return topic_dict


def get_sen_icon(file_path):
    """
    获取文本长短以及标点符号的特征
    :param file_path: 文件路径
    :return: {id:[句子个数\句子长度均值\。。\，。/。，\>>>>/]\……]}
    """
    result = {}
    content = data_process.read_whole_file(file_path)
    for key in content:
        i1, i2, i3, i4 = 0, 0, 0, 0
        si_list = []
        sents = data_process.sen_split(content[key])[0]
        length = len(sents)
        sents_ls = []
        for i in range(length):
            sents_ls.append(len(sents[i]))
        len_mean = np.mean(sents_ls)
        if "。。" in content[key]:
            i1 = 1
        if "，。" in content[key]:
            i2 = 1
        if "。，" in content[key]:
            i2 = 1
        if ">>>>" in content[key]:
            i3 = 1
        if "……" in content[key]:
            i4 = 1
        si_list.append(length)
        si_list.append(len_mean)
        si_list.append(i1)
        si_list.append(i2)
        si_list.append(i3)
        si_list.append(i4)
        result[key] = si_list
    return result


def merge(file_path):
    """
    将多个特征列表进行融合并归一化形成最终结果文档
    :param file_path: 文件路径
    :return:写入结果文件
    """
    result = {}
    ids = data_process.read_split_file(file_path)[1]
    ppl = get_ppl(file_path)
    topic = get_topic(file_path)
    sen_icon = get_sen_icon(file_path)
    for key in ids:
        print ppl[key]
        print topic[key]
        print sen_icon[key]
        merge_lt = ppl[key] + topic[key] + sen_icon[key]
        merge_lt.insert(0, key)
        result[key] = merge_lt
    file = open(file_path.replace(".csv", "_result.csv"), 'w')
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    data = []
    for each in result:
        dic = dict(map(lambda x, y: [x, y], header, result[each]))
        data.append(dic)
    writer.writerows(data)


if __name__ == '__main__':
    test = '/media/iiip/数据/duanduan/data/test.csv'
    merge(test)
    train = '/media/iiip/数据/duanduan/data/train.csv'
    merge(train)
    validation = '/media/iiip/数据/duanduan/data/validation.csv'
    merge(validation)







