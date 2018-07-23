# coding=utf-8
"""
created on:2018/7/6
author:DilicelSten
target:计算文档的主题分散度
finished on:2018/7/6
"""
import os


def run_topic():
    """
    通过Familia模型计算主题个数和主题分散度
    :return: {id:[主题数，主题分散度]}
    """
    familia_path = "/media/iiip/数据/duanduan/Familia-master/python"
    run_command = "sh run_lda_infer_demo.sh"
    os.system('cd ' + familia_path + '&& ' + run_command)


if __name__ == '__main__':
    run_topic()