from __future__ import unicode_literals
# -*- coding:utf-8 -*-
# 2017-09-20 22:27:30
__author__ = 'kddr'

import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, re, time, sys, json
import importlib
import sqlite3
importlib.reload(sys)
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

executorThread = ThreadPoolExecutor(max_workers=10)  # 线程池

# 获取html
def get_ResponseHtml(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf8')
    return response


# bs对象
def bs_obj(responseHtml):
    # BeautifulSoup对象
    bs_obj = BeautifulSoup(responseHtml, 'lxml')
    return bs_obj


def get_html_obj(url):
    return bs_obj(get_ResponseHtml(url))


# 获取id97单个电影的详情
def get_id97_movie_info(movie):
    aTag = movie.find_all('a')
    name = aTag[1].string  # 电影名称
    detailUrl = aTag[1].get('href')  # 详情页
    imgUrl = movie.find_all('img')[0].get('data-original')  # 图片地址
    if len(movie.find_all('span'))>0:
        quality = movie.find_all('span')[0].string  # 视频质量
    else:
        quality=""
    movieID = detailUrl.split('/')[-1].split('.')[0]  # 电影id
    mark = movie.find_all('em')[0].string.split()[1].split('分')[0]  # 评分
    tags = []  # 标签
    for i in range(2, len(aTag)):
        tags.append(aTag[i].string)
    tags = ','.join(tags)
    # 电影详情爬取
    detailObj = get_html_obj(detailUrl)
    movieTitle = detailObj.find_all('h1')[0].text.split('(')[0]
    movieYear = detailObj.find_all('h1')[0].text.split('(')[1].split(')')[0]
    lastFresh = detailObj.find_all('em')[0].text.split('：')[1]
    tbodys = detailObj.find_all('tbody')
    introduce = detailObj.find_all(class_='movie-introduce')[0].text.strip()
    # 第一个body为详情
    detailName = []
    detailValue = []
    for tr in tbodys[0].find_all('tr'):
        tds = tr.find_all('td')
        detailName.append(tds[0].text)
        detailValue.append(tds[1].text.strip(' 显示全部'))
    # 在线播放
    onlineBtn = detailObj.find_all(class_="online-play-btn")
    onlineUrl = 'null'
    if (len(onlineBtn) != 0):
        onlineUrl = detailObj.find_all(class_="online-play-btn")[0].get('href')
    # 迅雷下载数量
    normalDown = detailObj.find_all(href="#normalDown")[0].text.split()[1]
    # 超清下载数量
    sourceDown = detailObj.find_all(href="#sourceDown")[0].text.split()[1]
    resourceIDs = detailObj.find_all(mid=movieID)
    sourceDownIds = []  # 资源ID  资源页面 http://www.id97.com/res/5298908.html
    normalDownIds = []#http://www.id97.com/res/5296361.html
    if normalDown != '0':
        for i in range(0, int(normalDown)):
            normalDownIds.append(resourceIDs[i].get('id').split('_')[1])
    if sourceDown != '0' and normalDown>=sourceDown:
        for j in range(int(normalDown), int(normalDown) + int(sourceDown)):
            sourceDownIds.append(resourceIDs[j].get('id').split('_')[1])
    #sourceDownIds='"'+sourceDownIds+'"'
    sourceDownIds = ",".join(sourceDownIds)
    normalDownIds = ",".join(normalDownIds)
    #normalDownIds ='"'+normalDownIds+'"'
    # 电影详情list
    basicName = ['movieID', 'name', 'detalilUrl', 'imgUrl', 'quality', 'mark', 'tags', 'movieTitle', 'movieYear',
                 'lastFresh', 'onlineUrl', 'normalDown', 'sourceDown', 'introduce']
    basicValue = [movieID, name, detailUrl, imgUrl, quality, mark, tags, movieTitle, movieYear, lastFresh, onlineUrl,
                  normalDownIds, sourceDownIds, introduce]
    basicName.extend(detailName)
    basicValue.extend(detailValue)
    basicValue = list(map(format_name, basicValue))
    result = json.dumps(dict(list(zip(basicName, basicValue))), ensure_ascii=False)
    write_movies_to_sqlite3(result)
# 用' / '分割的信息，map用这方法转换为list
def format_name(lst):
    try:
        if ' / ' in lst:
            result = lst.split(' / ')
            return result
        else:
            return lst
    except Exception as e:
        print(('format_name', e))
        return list(map(format_name, lst))


# 开始获取id97的电影
def get_id97_movies(page, url):
    # 获取html bs对象
    bsObj = get_html_obj(url)
    movies = bsObj.find_all(class_="movie-item-in")
    for index, movie in enumerate(movies):
        print((page, '----', index))
        get_id97_movie_info(movie)


# 写入数据库
def write_movies_to_sqlite3(movie):
    #result = json.dumps(dict(list(movie)), ensure_ascii=False)
    movie = json.loads(movie)
    #print(movie)
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur=conn.cursor()
        #try:
        #    cur.execute('CREATE TABLE IF NOT EXISTS mydb(movieID VARCHAR(30), name VARCHAR(200),detalilUrl VARCHAR(200),imgUrl VARCHAR(200),quality VARCHAR(200),mark VARCHAR(200),tags VARCHAR(200),movieTitle VARCHAR(200),movieYear VARCHAR(200),lastFresh VARCHAR(200),onlineUrl VARCHAR(200),normalDown VARCHAR(200),sourceDown VARCHAR(200),introduce VARCHAR(200))')
        #except:
        #   print('Create fail')
        sql_insert="INSERT INTO mydb VALUES (:movieID,:name,:detalilUrl,:imgUrl,:quality,:mark,:tags,:movieTitle,:movieYear,:lastFresh,:onlineUrl,:normalDown,:sourceDown,:introduce)"
        cur.execute(sql_insert, movie)
        conn.commit()
        conn.close()
    except Exception as e:
         print ('----error----', e)

if __name__ == '__main__':
    basicUrl = 'http://www.id97.com/movie/?page='
    # 获取html bs对象
    bsObj = get_html_obj(basicUrl + '1')
    # 获取页码数
    allPage = bsObj.find_all("a", text='末页')
    page = allPage[0].get('href').split('=')[1]
    urls = [basicUrl + str(i + 1) for i in range(0, 2)]
    for index, url in enumerate(urls):
        try:
            get_id97_movies(str(index + 1), url)
            executorThread.submit(get_id97_movies, str(index + 1), url)
        except Exception as e:
            print(e)
            continue
