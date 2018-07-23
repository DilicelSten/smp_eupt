# coding=utf8
"""
created on:2018/7/6
author:DilicelSten
target:利用Familia开源工具计算主题分散度
finished on:2018/7/6
"""
import numpy as np
import sys
from familia_wrapper import InferenceEngineWrapper
import pandas as pd
import csv

if sys.version_info < (3, 0):
    input = raw_input


def read_whole_file(file_path):
    """
    读取文本内容，得到完整的文档内容
    :param file_path: 文件路径
    :return: 样本字典dict = {"id":"content"}
    """
    test_dict = {}
    num_dict = {}
    sample = pd.read_csv(file_path, sep='\t')
    ids, contents = sample.id, sample.content
    for num, d_id in enumerate(ids):
        num_dict[num] = d_id
    for index, content in enumerate(contents):
        document = content.replace(" ", "")
        test_dict[num_dict[index]] = document
    return test_dict


def calc_ent(x):
    """
    计算主题分布的信息熵
    :param x:主题分布列表
    :return:
    """
    ent = 0.0
    p = np.array(x)
    logp = np.log2(p)
    ent -= p * logp
    result = np.sum(ent)
    return result


def cal_topic(tp_list):
    """
    通过Familia模型计算出主题分布计算阈值主题个数以及主题分布的交叉熵
    :param tp_list:主题分布列表
    :return:列表【主题个数，交叉熵】
    """
    result = []
    tp_num = 0
    values = []
    for each in tp_list:
        values.append(each[1])
        if each[1] > 0.05:
            tp_num += 1
    ent = calc_ent(values)
    result.append(tp_num)
    result.append(ent)
    return result


if __name__ == '__main__':
    path = '/media/iiip/数据/duanduan/data/validation.csv'
    documents = read_whole_file(path)
    if len(sys.argv) < 3:
        sys.stderr.write("Usage:python {} {} {}\n".format(
            sys.argv[0], "model_dir", "conf_file"))
        exit(-1)
    # 获取参数
    model_dir = sys.argv[1]
    conf_file = sys.argv[2]
    # 创建InferenceEngineWrapper对象
    inference_engine_wrapper = InferenceEngineWrapper(model_dir, conf_file)
    topic_result = {}
    for key in documents:
        print key
        seg_list = inference_engine_wrapper.tokenize(documents[key])
        # 进行推断
        topic_dist = inference_engine_wrapper.lda_infer(seg_list)
        topic_result[key] = cal_topic(topic_dist)
    file = open(path.replace(".csv", "_topic.csv"), 'w')
    writer = csv.writer(file)
    for each in topic_result:
        writer.writerow([each, topic_result[each][0], topic_result[each][1]])
    file.close()
    # return topic_result

