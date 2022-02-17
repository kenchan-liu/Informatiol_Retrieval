import itertools
import random
from CleanData import *
import torch
save_dir = os.path.join("data", "save")
voc, pairs = loadPrepareData(corpus, corpus_name, datafile, save_dir)

def indexesFromSentence(voc, sentence):
    return [voc.word2index[word] for word in sentence.split(' ')] + [end]



def Sen2Index(voc, sentence):
    return [voc.word2index[word] for word in sentence.split(' ')] + [end]


# zip 对数据进行合并了，相当于行列转置了
def zeroPadding(l, fillvalue=normal):
    return list(itertools.zip_longest(*l, fillvalue=fillvalue))


# 记录 PAD_token的位置为0， 其他的为1
def binaryMatrix(line):
    m = []
    for i, seq in enumerate(line):
        m.append([])
        for token in seq:
            if token == normal:
                m[i].append(0)
            else:
                m[i].append(1)
    return m


# 返回填充前（加入结束index EOS_token做标记）的长度 和 填充后的输入序列张量
def inputVar(l, voc):
    indexes_batch = [Sen2Index(voc, sentence) for sentence in l]
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    padVar = torch.LongTensor(padList)
    return padVar, lengths
##把输入的单词转换成tensor，并且返回padding之后的长度


# 返回填充前（加入结束index EOS_token做标记）最长的一个长度 和 填充后的输入序列张量, 和 填充后的标记 mask
def outputVar(l, voc):
    indexes_batch = [Sen2Index(voc, sentence) for sentence in l]
    max_target_len = max([len(indexes) for indexes in indexes_batch])
    padList = zeroPadding(indexes_batch)
    mask = binaryMatrix(padList)
    mask = torch.ByteTensor(mask)
    padVar = torch.LongTensor(padList)
    return padVar, mask, max_target_len
##类似上面的，把输出转换tensor


# 返回给定batch对的所有项目
def batch2TrainData(voc, pair_batch):
    pair_batch.sort(key=lambda x: len(x[0].split(" ")), reverse=True)
    input_batch, output_batch = [], []
    for pair in pair_batch:
        input_batch.append(pair[0])
        output_batch.append(pair[1])
    input, lengths = inputVar(input_batch, voc)
    output, mask, max_target_len = outputVar(output_batch, voc)
    return input, lengths, output, mask, max_target_len


# 验证例子
if __name__ == '__main__':
    small_batch_size = 5
    voc, pairs = loadPrepareData(corpus, corpus_name, datafile, save_dir)
    input_variable, lengths, target_variable, mask, max_target_len = batch2TrainData(voc, [random.choice(pairs) for _ in range(small_batch_size)])
    print("input_variable:", input_variable)
    print("lengths:", lengths)
    print("target_variable:", target_variable)
    print("mask:", mask)
    print("max_target_len:", max_target_len)
