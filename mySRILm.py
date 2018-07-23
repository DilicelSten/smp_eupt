# coding=utf-8
"""
created on:2018/7/4
author:DilicelSten
target:使用语言模型计算文档困惑度(修改版)
finished on:2018/7/6
"""
import os
import data_process
import re
import numpy as np


root = "cd ~"  # 返回根目录
srilm_path = "/home/iiip/Downloads/duanduan/srilm/srilm-1.7.1/bin/i686-m64"  # srilm存放路径
export = "export PATH="+srilm_path+":"+srilm_path+":$PATH"  # 设置环境变量


def cal_feature(p_list):
    """
    计算ppl的4个特征并以列表的形式返回
    :param p_list: 每篇文档ppl数值列表
    :return: 结果列表[极差\最差\最差top3均值（小于3则为最差）\最好\ppl方差]
    """
    result = []
    p_arr = np.array(p_list)
    range_ppl = np.max(p_arr) - np.min(p_arr)
    bad_ppl = np.max(p_arr)
    if len(p_list) < 3:
        mean_ppl = bad_ppl
    else:
        mean_ppl = np.mean(p_list[-3:])
    best_ppl = np.min(p_arr)
    variance_ppl = np.var(p_arr)
    result.append(range_ppl)
    result.append(bad_ppl)
    result.append(mean_ppl)
    result.append(best_ppl)
    result.append(variance_ppl)
    return result


def train_model(txt_path, count_path, lm_path):
    """
    调用Linux命令训练srilm模型
    :param txt_path:训练样本TXT路径
    :param count_path: 存放count文件路径
    :param lm_path: 存放模型路径
    :return:
    """
    os.system(root + '&&' + export + '&& ngram-count -text '+txt_path+' -order 3 -write '+count_path)
    os.system(root + '&&' + export + '&& ngram-count -read '+count_path+' -order 3 -lm '+lm_path+' -interpolate -kndiscount')


def cal_ppl(file_path, lm):
    """
    计算每篇文档ppl的极差作为特征输入
    :param lm: srilm模型的存放路径
    :param file_path:要处理的文档路径
    :return:测试样本ppl_dict = {"id","ppl"}
    """
    id_list, ids = data_process.write_file(file_path)
    ppl_list = []
    os.system(root + '&&' + export + '&& ngram -ppl '+file_path.replace("csv", "txt")+' -order 3 -lm '+lm+' -debug 1 > /media/iiip/数据/duanduan/data/result.ppl')
    with open('/media/iiip/数据/duanduan/data/result.ppl', 'r') as fr:
        text = fr.read()
    for num in re.findall("ppl= (.*?) ppl1=", text)[:-1]:
        ppl_list.append(float(num))
    print len(id_list)
    print len(ppl_list)
    return id_list, ppl_list, ids


def cal_final(file_path, l_path):
    """
    计算每篇文档的ppl极差，并写入文件
    :param file_path: 文件路径
    :param l_path: 训练模型路径
    :return: {id：ppl}
    """
    result = {}
    id_list, ppl_list, ids = cal_ppl(file_path, l_path)
    for each in ids:
        print each
        each_list = []
        for i in range(len(id_list)):
            if id_list[i] == each:
                each_list.append(ppl_list[i])
        each_list.sort()
        if len(each_list) == 0: continue
        print each_list
        result[each] = cal_feature(each_list)
    return result

