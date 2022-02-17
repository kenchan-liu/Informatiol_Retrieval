import unicodedata
import os
import re

# 默认词向量
normal = 0  # Used for padding short sentences
start = 1  # Start-of-sentence token
end = 2  # End-of-sentence token
corpus = "cornell movie-dialogs corpus"
corpus_name = os.path.join("F://Chat-Bot//data//", corpus)
datafile = "F://Chat-Bot//data//cornell movie-dialogs corpus//formattedlines.txt"

class Voc:
    def __init__(self, name):
        self.name = name
        self.index2word = {normal: "p", start: "s", end: "e"}
        self.word2index = {}
        self.word2count = {}

        self.num_words = 3  #开始结束符号
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1


    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

MAX_LENGTH = 10  # 最长句子长度
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def normalizeS(s):
    s = s.lower()
    s = re.sub('[@#$\&%*\^]','',s)
    return s


# 如果对 'p' 中的两个句子都低于 MAX_LENGTH 阈值，则返回True
def filterPair(p):
    # Input sequences need to preserve the last word for EOS token
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH


# 过滤满足条件的 pairs 对话
def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

# 使用上面定义的函数，返回一个填充的voc对象和对列表
def loadPrepareData(corpus, corpus_name, datafile, save_dir):
    print("Start preparing training data ...")
    print("Reading lines...")
    # Read the file and split into lines
    lines = open(datafile, encoding='utf-8').read().strip().split('\n')
    # Split every line into pairs and normalize
    pairs = [[normalizeS(s) for s in l.split('\t')] for l in lines]
    voc = Voc(corpus_name)
    print("Read {!s} sentence pairs".format(len(pairs)))
    pairs = filterPairs(pairs)
    print("Trimmed to {!s} sentence pairs".format(len(pairs)))
    print("Counting words...")
    for pair in pairs:
        voc.addSentence(pair[0])
        voc.addSentence(pair[1])
    print("Counted words:", voc.num_words)
    return voc, pairs

def trimRareWords(voc, pairs, MIN_COUNT):
    # 修剪来自voc的MIN_COUNT下使用的单词
    # Filter out pairs with trimmed words
    keep_pairs = []
    for pair in pairs:
        input_sentence = pair[0]
        output_sentence = pair[1]
        keep_input = True
        keep_output = True
        for word in input_sentence.split(' '):
            if word not in voc.word2index:
                keep_input = False
                break
        for word in output_sentence.split(' '):
            if word not in voc.word2index:
                keep_output = False
                break

        # 只保留输入或输出句子中不包含修剪单词的对
        if keep_input and keep_output:
            keep_pairs.append(pair)

    print("Trimmed from {} pairs to {}, {:.4f} of total".format(len(pairs), len(keep_pairs),
                                                                len(keep_pairs) / len(pairs)))
    return keep_pairs


if __name__ == '__main__':
    # 加载/组装voc和对
    save_dir = os.path.join("data", "save")
    voc, pairs = loadPrepareData(corpus, corpus_name, datafile, save_dir)
    # 打印一些对进行验证
    print("\npairs:")
    for pair in pairs[:10]:
        print(pair)
    MIN_COUNT = 3  # 修剪的最小字数阈值




