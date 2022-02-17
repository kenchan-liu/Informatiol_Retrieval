# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch
from torch.jit import script, trace
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import csv
import codecs
from io import open
import itertools
import math

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")



def loadATA(fileName, fileName2, linefields, convfields):
    lines = {}
    f = open(fileName, 'r', encoding='iso-8859-1')

    #加载句子
    for line in f:
        values = line.split(" +++$+++ ")
        # Extract fields
        lineObj = {}
        for i, field in enumerate(linefields):
            lineObj[field] = values[i]
        lines[lineObj['lineID']] = lineObj

    conversations = []

    #加载对话信息
    with open(fileName2, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            convObj = {}
            for i, field in enumerate(convfields):
                convObj[field] = values[i]
            # Convert string to list (convObj["utteranceIDs"] == "['L598485', 'L598486', ...]")
            lineIds = eval(convObj["utteranceIDs"])
            # Reassemble lines
            convObj["lines"] = []
            for lineId in lineIds:

                #和上面所构建的句子信息对应合并
                convObj["lines"].append(lines[lineId])
            conversations.append(convObj)

    qa_pairs = []
    for conversation in conversations:
        # 遍历所有的对话
        for i in range(len(conversation["lines"]) - 1):
            #构建问答对
            inputLine = conversation["lines"][i]["text"].strip()
            targetLine = conversation["lines"][i+1]["text"].strip()
            if inputLine and targetLine:
                qa_pairs.append([inputLine, targetLine])
    return qa_pairs



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    datafile = "F://Chat-Bot//data//cornell movie-dialogs corpus//formattedlines.txt"

    delimiter = '\t'

    delimiter = str(codecs.decode(delimiter, "unicode_escape"))

    # 初始化行dict，对话列表和字段ID
    lines = {}
    conversations = []
    MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]
    MOVIE_CONVERSATIONS_FIELDS = ["character1ID", "character2ID", "movieID", "utteranceIDs"]

    # 加载行和进程对话
    QAP = loadATA("F://Chat-Bot//data//cornell movie-dialogs corpus//movie_lines.txt"
                  ,"F://Chat-Bot//data//cornell movie-dialogs corpus//movie_conversations.txt", MOVIE_LINES_FIELDS , MOVIE_CONVERSATIONS_FIELDS)

    # 写入新的csv文件
    print("\nWriting newly formatted file...")
    with open(datafile, 'w', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile, delimiter=delimiter, lineterminator='\n')
        for pair in QAP:
            writer.writerow(pair)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
