# Sample.py
from flask import Flask, render_template, url_for, request, redirect
from elasticsearch.client import Elasticsearch
from datetime import datetime

es = Elasticsearch()
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/redirect', methods=['POST'])
def direct_new():
    username = request.form['username']
    password = request.form['password']
    name_find = es.search(index="searchaccount-index",query={"bool": {
            "must": [{
                "term": {
                    "name": username
                }
            }, {
                "term": {
                    "password": password
                }
            }]
        }})
    if name_find['hits']['hits'] == []:
        return  redirect(url_for('search'))
    else:
        return redirect(url_for('adv_search', username=username))


@app.route('/search_in/<searching>', methods=['POST', 'GET'])
def search_in(searching):
    """
    i = es.search(index="searchaccount-index", query={"match": {"name": username}})['hits']['hits'][0]['_id']
    tmp = es.get(index="searchaccount-index", id=int(i))['_source']
    tmp['history'] = tmp['history'] + str(datetime.now()) + ' ' + str(searching)
    es.index(index="searchaccount-index", id=int(i), document=tmp)
    """
    res = es.search(index="newstore-index", query={"function_score":{"query":{"match": {"content": str(searching)},"field_value_factor":{"field":"influe"}}}})
    if len(res['hits']['hits']) >= 3:
        ret1 = res['hits']['hits'][0]['_source']['content']
        ret10 = "<p>{}</p>".format(ret1)
        ret11 = res['hits']['hits'][0]['_source']['url'][0]
        ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
        ret2 = res['hits']['hits'][1]['_source']['content']
        ret20 = "<p>{}</p>".format(ret2)
        ret22 = res['hits']['hits'][1]['_source']['url'][0]
        ret22 = "<a href=\"{}\">新闻二</a>".format(ret22)
        ret3 = res['hits']['hits'][2]['_source']['content']
        ret30 = "<p>{}</p>".format(ret3)
        ret33 = res['hits']['hits'][2]['_source']['url'][0]
        ret33 = "<a href=\"{}\">新闻三</a>".format(ret33)
        return '<h1 style="text-align:center">{}</h1>  {}{}{}{}{}{}'.format(
            'This is what you want:', ret10, ret11, ret20, ret22, ret30, ret33)
    elif 2 <= len(res['hits']['hits']) < 3:
        ret1 = res['hits']['hits'][0]['_source']['content']
        ret10 = "<p>{}</p>".format(ret1)
        ret11 = res['hits']['hits'][0]['_source']['url'][0]
        ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
        ret2 = res['hits']['hits'][1]['_source']['content']
        ret20 = "<p>{}</p>".format(ret1)
        ret22 = res['hits']['hits'][1]['_source']['url'][0]
        ret22 = "<a href=\"{}\">新闻二</a>".format(ret11)
        return '<h1 style="text-align:center">{}</h1>  {}{}{}{}'.format(
            'This is what you want:', ret10, ret11, ret20, ret22)
    elif 1 <= len(res['hits']['hits']) < 2:
        ret1 = res['hits']['hits'][0]['_source']['content']
        ret10 = "<p>{}</p>".format(ret1)
        ret11 = res['hits']['hits'][0]['_source']['url'][0]
        ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
        return '<h1 style="text-align:center">{}</h1>  {}{}'.format(
            'This is what you want:', ret10, ret11)
    else:
        return redirect(url_for('error'))


@app.route('/adsearch_in/<string:key>', methods=['POST', 'GET'])
def adsearch_in(key):
    keys = str(key).split('?')
    print(keys)
    key1 = keys[0]
    key2 = keys[1]
    html = keys[2]
    username = keys[3]
    option = keys[3]
    if option == "phrase":
        i = es.search(index="searchaccount-index", query={"match": {"name": username}})['hits']['hits'][0]['_id']
        tmp = es.get(index="searchaccount-index", id=int(i))['_source']
        tmp['history'] = tmp['history'] + str(datetime.now()) + ' ' + str(key1)+' '+str(key2) + ' ' + str(html)
        es.index(index="searchaccount-index", id=int(i), document=tmp)
        res = es.search(index="newstore-index", query={
            "bool": {
                "must": [
                    {"match_phrase": {
                        "content": key1
                    }}
                ],
                "should": [{
                    "match": {
                        "url": html}
                }, {
                    "match": {
                        "content": key2
                    }
                }
                ]
            }})
        if len(res['hits']['hits']) >= 3:
            ret1 = res['hits']['hits'][0]['_source']['content']
            ret10 = "<p>{}</p>".format(ret1)
            ret11 = res['hits']['hits'][0]['_source']['url'][0]
            ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
            ret2 = res['hits']['hits'][1]['_source']['content']
            ret20 = "<p>{}</p>".format(ret2)
            ret22 = res['hits']['hits'][1]['_source']['url'][0]
            ret22 = "<a href=\"{}\">新闻二</a>".format(ret22)
            ret3 = res['hits']['hits'][2]['_source']['content']
            ret30 = "<p>{}</p>".format(ret3)
            ret33 = res['hits']['hits'][2]['_source']['url'][0]
            ret33 = "<a href=\"{}\">新闻三</a>".format(ret33)
            return '<h1 style="text-align:center">{}</h1>  {}{}{}{}{}{}'.format(
                'This is what you want:', ret10, ret11, ret20, ret22, ret30, ret33)
        elif 2 <= len(res['hits']['hits']) < 3:
            ret1 = res['hits']['hits'][0]['_source']['content']
            ret10 = "<p>{}</p>".format(ret1)
            ret11 = res['hits']['hits'][0]['_source']['url'][0]
            ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
            ret2 = res['hits']['hits'][1]['_source']['content']
            ret20 = "<p>{}</p>".format(ret1)
            ret22 = res['hits']['hits'][1]['_source']['url'][0]
            ret22 = "<a href=\"{}\">新闻二</a>".format(ret11)
            return '<h1 style="text-align:center">{}</h1>  {}{}{}{}'.format(
                'This is what you want:', ret10, ret11, ret20, ret22)
        elif 1 <= len(res['hits']['hits']) < 2:
            ret1 = res['hits']['hits'][0]['_source']['content']
            ret10 = "<p>{}</p>".format(ret1)
            ret11 = res['hits']['hits'][0]['_source']['url'][0]
            ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
            return '<h1 style="text-align:center">{}</h1>  {}{}'.format(
                'This is what you want:', ret10, ret11)
        else:
            return redirect(url_for('error'))
    else:
        i = es.search(index="searchaccount-index", query={"match": {"name": username}})['hits']['hits'][0]['_id']
        tmp = es.get(index="searchaccount-index", id=int(i))['_source']
        tmp['history'] = tmp['history'] + str(datetime.now()) + ' ' + str(key1) + ' ' + str(key2) + ' ' + str(html)
        es.index(index="searchaccount-index", id=int(i), document=tmp)
        res = es.search(index="newstore-index", query={
            "bool": {
                "must": [
                    {"match": {
                        "content": key1
                    }}
                ],
                "should": [{
                    "match": {
                        "url": html}
                }, {
                    "match": {
                        "content": key2
                    }
                }
                ]
            }})
        if len(res['hits']['hits']) >= 3:
            ret1 = res['hits']['hits'][0]['_source']['content']
            ret10 = "<p>{}</p>".format(ret1)
            ret11 = res['hits']['hits'][0]['_source']['url'][0]
            ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
            ret2 = res['hits']['hits'][1]['_source']['content']
            ret20 = "<p>{}</p>".format(ret2)
            ret22 = res['hits']['hits'][1]['_source']['url'][0]
            ret22 = "<a href=\"{}\">新闻二</a>".format(ret22)
            ret3 = res['hits']['hits'][2]['_source']['content']
            ret30 = "<p>{}</p>".format(ret3)
            ret33 = res['hits']['hits'][2]['_source']['url'][0]
            ret33 = "<a href=\"{}\">新闻三</a>".format(ret33)
            return '<h1 style="text-align:center">{}</h1>  {}{}{}{}{}{}'.format(
                'This is what you want:', ret10, ret11, ret20, ret22, ret30, ret33)
        elif 2 <= len(res['hits']['hits']) < 3:
            ret1 = res['hits']['hits'][0]['_source']['content']
            ret10 = "<p>{}</p>".format(ret1)
            ret11 = res['hits']['hits'][0]['_source']['url'][0]
            ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
            ret2 = res['hits']['hits'][1]['_source']['content']
            ret20 = "<p>{}</p>".format(ret1)
            ret22 = res['hits']['hits'][1]['_source']['url'][0]
            ret22 = "<a href=\"{}\">新闻二</a>".format(ret11)
            return '<h1 style="text-align:center">{}</h1>  {}{}{}{}'.format(
                'This is what you want:', ret10, ret11, ret20, ret22)
        elif 1 <= len(res['hits']['hits']) < 2:
            ret1 = res['hits']['hits'][0]['_source']['content']
            ret10 = "<p>{}</p>".format(ret1)
            ret11 = res['hits']['hits'][0]['_source']['url'][0]
            ret11 = "<a href=\"{}\">新闻一</a>".format(ret11)
            return '<h1 style="text-align:center">{}</h1>  {}{}'.format(
                'This is what you want:', ret10, ret11)
        else:
            return redirect(url_for('error'))


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/adv_search')
def adv_search():
    return render_template('search2.html')


@app.route('/adv_search/redirect', methods=['POST'])
def redirect2():
    key1 = request.form['key1']
    key2 = request.form['key2']
    html = request.form['html']
    username = request.form['username']
    data = request.form.get('options')
    return redirect(url_for('adsearch_in', key=str(key1)+"?"+str(key2)+"?"+str(html)+"?"+str(username)+"?"+str(data)))


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/search/redirect', methods=['POST'])
def redirect_to_new_url():
    """
    username = request.form['username']
    return redirect(url_for('user', username=username))
    """
    searching = request.form['search']
    return redirect(url_for('search_in', searching=searching))




if __name__ == '__main__':
    app.run()
