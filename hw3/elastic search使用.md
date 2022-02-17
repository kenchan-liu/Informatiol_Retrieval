# elastic search使用

### 索引构建

使用elastic search的python接口，读取enron的邮件数据集，将每个邮件的内容读取出来，使用json的格式来包装数据内容，将数据建立起映射的形式，建立索引，将数据传送到es数据库对应的索引中。代码如下：

~~~python
import os
for root, dirs, files in os.walk("f://enronmail/maildir", topdown=False):
    i=1
    for name in files:
        try:
            with open(os.path.join(root, name),encoding='utf-8') as f:
                messageid=f.readline()
                Time=f.readline()
                for j in range(2):
                    f.readline()
                Theme = f.readline()
                for j in range(3):
                    f.readline()
                Sender=f.readline()
                if len(Sender.split(":"))>1:
                    Sender=Sender.split(":")[1]
                Reciver=f.readline()
                if len(Reciver.split(":"))>1:
                    Reciver=Reciver.split(":")[1]
                CC=f.readline()
                f.readline()
                f.readline()
                f.readline()
                File=f.readline()
                if len(File.split(":"))>1:
                    File=File.split(":")[1]
                doc = {
                    'head':{
                        'messageid':messageid,
                        'Time':Time,
                        'Sender':Sender,
                        'Reciver':Reciver,
                        'CC':CC,
                    },
                    'Theme' : Theme,
                    'File':File,
                    'Text': f.read()
                }
        except UnicodeDecodeError:
            print("decodeError")
        res = es.index(index="estest-index", id=i, document=doc)
        i+=1
    print(res['result'])
~~~

这里索引构建的形式是包括了该邮件的messageid，发送时间，发送人和接收人还有cc群组，以上的几个数据用json包装起来作为head，接下来包括了邮件的标题、邮件的附件名和邮件的文本内容，将以上的几个数据用json格式包装作为doc传入，每一条数据传入的时候，id自增作为索引的id传入elasticsearch数据库。

这里读取文件的过程中，因为有一个字段对应多行内容的，因此我们需要进行判断，连续读取多行内容然后拼接。还有需要注意的一点是，因为直接读取有时候会报错，因为编码形式的问题，因此使用了错误处理跳过了报错的文件。

### 检索功能

使用**res = es.get(index="estest-index", id=1)**来查找索引中某个特定id的数据内容。

然后使用**res['_source']**可以查看内容详情。

使用elastic的query可以用来进行特定形式的查找了。

在网站：[查询表达式 | Elasticsearch: 权威指南 | Elastic](https://www.elastic.co/guide/cn/elasticsearch/guide/current/query-dsl-intro.html)中可以找到查询语句的具体写法。

~~~sql
{
    "query": {
        "match_all": {}
    }
}
~~~

用如上的语句可以查到每一条数据。

写在python的api里面是这样的。

~~~python
es.search(index="estest-index", query={
   "match_all":{}
   })
~~~

普通的检索字段的形式如下

~~~sql
{
    QUERY_NAME: {
        ARGUMENT: VALUE,
        ARGUMENT: VALUE,...
    }
}
~~~

在这个索引的字段检索的具体写法示例如下：

~~~python
es.search(index="estest-index", query={
    "match":{"head.Sender":"allen"}
   })
~~~

这里就表示字段head的Sender子字段中包含allen的可以被检索出来，这是模糊索引。

~~~python
res = es.search(index="estest-index", query={"match": {'Text' :'futures contract' }})

~~~

比如上面的模糊索引，就会返回text中和futures、contract相关的所有数据，比如futures如何如何，或者contract如何如何。

~~~python
res = es.search(index="estest-index", query={"match_phrase": {'Text' :'futures contract' }})
~~~

如果是这样的使用match_phrase的就是精确索引了，这会匹配所有包含”futures contract“的数据（必须连续）

![image-20211118220904622](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211118220904622.png)

结果部分展示如上图。

还可以使用合并查询语句完成一些更加复杂的操作，就像一些简单的组合块，这些组合块可以彼此之间合并组成更复杂的查询。这些语句可以是如下形式：

~~~sql
{
    "bool": {
        "must":     { "match": { "tweet": "elasticsearch" }},
        "must_not": { "match": { "name":  "mary" }},
        "should":   { "match": { "tweet": "full text" }},
        "filter":   { "range": { "age" : { "gt" : 30 }} }
    }
}

~~~

还可以使用multi_match的方法进行检索

~~~sql
{
    "multi_match": {
        "query":                "Quick brown fox",
        "type":                 "best_fields", 
        "fields":               [ "title", "body" ],
        "tie_breaker":          0.3,
    }
}

~~~

上面的意思是对下面的两个字段进行query内容的查询（这里query的内容是quick brown fox，也就是需要查询这个内容），而字段范围是title和body，也就是需要在title和body域里面查询这个query的内容。

模糊查询fuzzy。将你需要输入的查询内容，用一个（"fuzzy":）包含起来，这样就在匹配的时候就不会精准匹配你需要的那个单词了，比如说我们要查找contract，这就不会在向量空间中匹配每个contract的词语，而是把比如contracts，contrcts这种相似度较高的词语也当作同样的词语进行向量空间的计算。

~~~python
"fuzzy": {
      "head.Sender": {
        "value": "allen"
      }
    }


~~~

上图的模糊搜索中，就不会强行找所有allen发送的邮件，因为有可能他叫allan，这个名字也差不多。

 Bool查询由一个或者多个子句组成，每个子句都有特定的类型。

**must**

返回的文档必须满足must子句的条件，并且参与计算分值

**filter**

返回的文档必须满足filter子句的条件。但是不会像Must一样，参与计算分值

**should**

返回的文档可能满足should子句的条件。在一个Bool查询中，如果没有must或者filter，有一个或者多个should子句，那么只要满足一个就可以返回。`minimum_should_match`参数定义了至少满足几个子句。

~~~python
        "bool": {
            "must not": [
                {"match": {
                        "head.messageid": "1231515"
                        
                    }},
                    {"match": {
                        "Sender": "Bailey"
                    }},
            ]
        }
    

~~~



## es原理以及功能探索

es的match查询使用了向量空间的原理，在返回值的时候可以看到它会给出一个score数值，根据score数值的高低来返回查询结果的优先程度。在es构建索引的时候，他已经给每个字段文档分词完成。match给出了一个query，去和每个检索的字段域去计算余弦距离。这需要先用tf-idf去计算每个单词在不同文档的权重。

![image-20211119144631907](https://i.loli.net/2021/11/19/TMLncD7NYdVJ2A9.png)

然后用朴素的余弦距离公式来进行分数计算，计算的时候需要乘上权重，也就是上面得到的tfidf。

![image-20211119145235720](https://i.loli.net/2021/11/19/wvjuR2gMIfCdhbP.png)

最后例子中得到的结果如图，按照分数从大到小排列就是我们需要得到的结果。

![image-20211119145452754](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211119145452754.png)

拿这次的enron邮件数据集举例，我们输入一个match的query比方说"oil contracts"，然后他就会拿这个oil contracts作为一个query去和每个字段域的内容匹配，计算余弦相似性。这个例子里面就是要把oil的tfidf权重计算，然后计算contracts的tfidf，计算完成之后，直接按照余弦相似性的公式得到分数。

在每一次查询的返回值中，最前面有这样一段内容，其中的max_score就代表了这里查询得到的分数。最高分无疑就是这个max score，后面的查询结果也会带有这样的内容，而maxscore就被替换为了score单词。

~~~python
'took': 35, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 15, 'relation': 'eq'}, 'max_score': 6.9701686, 
~~~

![image-20211119150301668](https://i.loli.net/2021/11/19/ojgxurUJncA4kIR.png)

查询结果的一部分内容展示如上图所示。

**1	**	情感分析

如果我们要在enron数据集中做一些工作，比如说情感分析，那么我们可以找出表示一个特定情感的单词集合，比如说表示生气的单词有：angry annoyed vexation mad 等等，把这些单词作为query输入，然后使用match去查询，这里查询的字段域是text，也就是邮件正文中的内容。

如果我们要分析失落的情感，那我们需要先做一个失落情感的单词集合，比如upset，disappointed，down，blue等等，然后把这些单词作为match的query输入，查看向量空间中相似性高的text集合。

**2** 		垃圾邮件

如果我们要判断垃圾邮件，我们首先需要知道垃圾邮件有哪些特征，比如垃圾邮件一半都会存在一个advertisement，那我们可以将这个advertisement作为查询的query去进行查询。这里我们可以使用es一些更加复杂的查询，比如说fuzzy查询，也可以使用bool查询，来将各种各样的条件组合在一起，比如说一般重要的公务邮件会有一个提示，比如说significant 或者 vital之类的，我们在bool查询中可以要求这些是不能被包含的，使用must not语句。

## es功能探索之图形界面

elastic search官方提供了一个图形界面，类似于mysql的workbench，不同的是它是web版本的。我们需要下载kibana来使用它。

其主页如图：

![image-20211119153206367](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211119153206367.png)

可以查看es在主机的状态。

![image-20211119153742395](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211119153742395.png)

首先，我们可以在这里输入query，可以不使用python的api接口。

![image-20211119153144773](https://i.loli.net/2021/11/19/tq4Glk7V2ji9EYX.png)

在这个工具的网页里面，我们可以找到index management页面。

![image-20211119153552917](https://i.loli.net/2021/11/19/AcGDYp1PTyUkKM4.png)

这里我们可以看到我们已经在es数据库中构建的各种索引。

而索引的各个字段也可以在这里直观地查看出来。

![image-20211119153852873](https://i.loli.net/2021/11/19/U9k64KJPvf8EdLs.png)

kibana还有一个很强的功能是discovery，可以查看各个字段内容的分布，比如下图这样：

![image-20211119164339243](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211119164339243.png)

这里可以看到收件人出现最多的就是SARA SHACKLETON，

甚至还有直接可视化统计的功能：

![image-20211119164653550](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211119164653550.png)

邮件主题可以看到，因为没有切分re：字符，这是表示回复邮件的，

![image-20211119164754137](C:\Users\kentl\AppData\Roaming\Typora\typora-user-images\image-20211119164754137.png)

但是刨除那些普遍出现的字段，我们也可以看到巴西的金融交易是邮件集合中比较重要的主题。

