# coding=utf-8
"""
created on:2018/7/4
author:DilicelSten
target:对数据进行处理
finished on:2018/7/4
"""
import pandas as pd
from pyltp import SentenceSplitter


def sen_split(document):
    """
    利用pytltp对文档进行分句
    :param document: 整篇文档
    :return: 文档句子列表，文档句子分段
    """
    sents = SentenceSplitter.split(document)
    result = '\n'.join(sents)
    return sents, result


def train_sen(train_path, valid_path):
    """
    对训练样本提取并分句
    :param train_path: 训练样本路径
    :param valid_path: 验证样本路径
    :return:写入文件训练srilm模型
    """
    train = pd.read_csv(train_path, sep='\t')
    valid = pd.read_csv(valid_path, sep='\t')
    result = ""
    t_contents = train.content
    v_contents = valid.content
    for t_index, t_content in enumerate(t_contents):  # 迭代器处理
        print t_content
        for t_each in sen_split(t_content)[0]:
            if len(t_each) < 40: continue
            result += t_each + '\n'
    for v_index, v_content in enumerate(v_contents):
        print v_content
        for v_each in sen_split(v_content)[0]:
            if len(v_each) < 40: continue
            result += v_each + '\n'
    with open("../data/train_sen.txt", 'w') as f:
        f.write(result)


def read_split_file(file_path):
    """
    读取文本内容，得到已经分词分句的文档
    :param file_path: 文件路径
    :return: 样本字典dict = {"id":"content"}，标签，id列表
    """
    sample_dict = {}
    num_dict = {}
    # label_dict = {}
    sample = pd.read_csv(file_path, sep='\t')
    ids, contents = sample.id, sample.content
    for num, d_id in enumerate(ids):
        num_dict[num] = d_id
    # for num1, label in enumerate(labels):
    #     label_dict[num_dict[num1]] = label
    for index, content in enumerate(contents):
        sents = sen_split(content)[0]
        sample_dict[num_dict[index]] = sents
    return sample_dict, ids


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


def write_file(file_path):
    """
    将分词分句好的文档按句写进文件便于SRILM模型的计算
    :param file_path: 文档路径
    :return: 写入的文件，以及id列表
    """
    sample_dict = read_split_file(file_path)[0]
    ids = read_split_file(file_path)[1]
    con = ""
    id_list = []
    sen_list = []
    for each in sample_dict:
        print each
        for i in range(len(sample_dict[each])):
            if sample_dict[each][i] == '': continue
            if len(sample_dict[each][i]) < 20:
                print sample_dict[each][i]
                # continue
            id_list.append(each)
            sen_list.append(sample_dict[each][i])
            con += sample_dict[each][i] + '\n'
    with open(file_path.replace("csv", "txt"), 'w') as f:
        f.write(con)
    return id_list, ids


if __name__ == '__main__':
    tr_path = "../data/train.csv"
    # va_path = '../data/validation.csv'
    # train_sen(tr_path, va_path)
    # length = 0
    # path = "../data/test.csv"
    # test_dict = read_test(path)[0]
    # for each in test_dict:
    #     length += len(test_dict[each])
    # print length
    # test_sen(path)
    # with open("../data/first_result.ppl",'r') as f:
    #     content = f.read()
    # ppl = re.findall("ppl= (.*?) ppl1=",content)
    # for each in ppl:
    #     print each
    # read_document(path)