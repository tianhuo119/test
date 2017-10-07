#!/usr/bin/env python
# encoding: utf-8
import time,requests,urllib.request,urllib.error,urllib.parse,json,re
from lxml import etree
import pandas as pd
import sys
import importlib
importlib.reload(sys)

def getPage(url):#获取链接中的网页内容
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    try:
        request = urllib.request.Request(url = url, headers = headers)
        response = urllib.request.urlopen(request, timeout = 5)
        page = response.read().decode('utf-8')
        return page
    except (urllib.error.URLError,Exception) as e:
        if hasattr(e, 'reason'):
            print(('抓取失败，具体原因：', e.reason))
            request = urllib.request.Request(url = url, headers = headers)
            response = urllib.request.urlopen(request,timeout = 5)
            page = response.read().decode('utf-8')
            return page

def getList():
    place = input('请输入想搜索的区域、类型(如北京、热门景点等)：')
    placename=place
    place = urllib.parse.quote(place)
    url = 'http://piao.qunar.com/ticket/list.htm?keyword='+str(place)+'&region=&from=mps_search_suggest={}'
    print(url)
    i = 1
    sightlist = []
    while i<300:
        page = getPage(url.format(i))
        selector = etree.HTML(page)
        print('正在爬取第' + str(i) + '页景点信息')
        i+=1
        informations = selector.xpath('//div[@class="result_list"]/div')
        for inf in informations: #获取必要信息
            sight_name = inf.xpath('./div/div/h3/a/text()')[0]
            sight_level = inf.xpath('.//span[@class="level"]/text()')
            if len(sight_level):
                sight_level = sight_level[0].replace('景区','')
            else:
                sight_level = 0
            sight_area = inf.xpath('.//span[@class="area"]/a/text()')[0]
            sight_hot = inf.xpath('.//span[@class="product_star_level"]//span/text()')[0].replace('热度 ','')
            sight_add = inf.xpath('.//p[@class="address color999"]/span/text()')[0]
            sight_add = re.sub('地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$','',str(sight_add))
            sight_slogen = inf.xpath('.//div[@class="intro color999"]/text()')
			#sight_slogen = inf.xpath('.//div[@class="intro color999"]/text()')[0]
            sight_price = inf.xpath('.//span[@class="sight_item_price"]/em/text()')
            if len(sight_price):
                sight_price = sight_price[0]
            else:
                i = 0
                break
            sight_soldnum = inf.xpath('.//span[@class="hot_num"]/text()')[0]
            sight_url = inf.xpath('.//h3/a[@class="name"]/@href')[0]
            sightlist.append([sight_name,sight_level,sight_area,float(sight_price),int(sight_soldnum),float(sight_hot),sight_add.replace('地址：',''),sight_slogen,sight_url])
        time.sleep(3)
    return sightlist,place,placename

def listToExcel(list,name):
	df = pd.DataFrame(list,columns=['景点名称','级别','所在区域','起步价','销售量','热度','地址','标语','详情网址'])
	df.to_excel(name + '景点信息.xlsx')

def getBaiduGeo(sightlist,name):
	ak = 'vgbxuVuuliaBA8p40WnuQFts'
	headers = {
	'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
	}
	list = sightlist
	bjsonlist = []
	ejsonlist1 = []
	ejsonlist2 = []
	num = 1
	for l in list:
		try:
			try:
				try:
					address = l[6]
					url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address  + '&output=json&ak=' + ak
					json_data = requests.get(url = url).json()
					json_geo = json_data['result']['location']
				except KeyError as e:
					address = l[0]
					url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address  + '&output=json&ak=' + ak
					json_data = requests.get(url = url).json()
					json_geo = json_data['result']['location']
			except KeyError as e:
					address = l[2]
					url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address  + '&output=json&ak=' + ak
					json_data = requests.get(url = url).json()
					json_geo = json_data['result']['location']
		except KeyError as e:
			continue
		json_geo['count'] = l[4]/100
		bjsonlist.append(json_geo)
		ejson1 = {l[0] : [json_geo['lng'],json_geo['lat']]}
		ejsonlist1 = dict(ejsonlist1,**ejson1)
		ejson2 = {'name' : l[0],'value' : l[4]/100}
		ejsonlist2.append(ejson2)
		print(('正在生成第' + str(num) + '个景点的经纬度'))
		num +=1
	bjsonlist =json.dumps(bjsonlist)
	ejsonlist1 = json.dumps(ejsonlist1,ensure_ascii=False)
	ejsonlist2 = json.dumps(ejsonlist2,ensure_ascii=False)
	with open('./points.json',"w") as f:
		f.write(bjsonlist)
	with open('./geoCoordMap.json',"w") as f:
		f.write(ejsonlist1)
	with open('./data.json',"w") as f:
		f.write(ejsonlist2)

def main():
	sightlist,place,placename = getList()
	listToExcel(sightlist,placename)
	getBaiduGeo(sightlist,placename)

if __name__=='__main__':
	main()