import urllib
from urllib import request
from bs4 import BeautifulSoup
file=open('proxy.txt','w')
for page in range(1,50):
    url='http://www.xicidaili.com/nn/%s'%page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    try:
        request = urllib.request.Request(url = url, headers = headers)
        response = urllib.request.urlopen(request, timeout = 5)
        #page = response.read().decode('utf-8')
    except (urllib.error.URLError,Exception) as e:
        if hasattr(e, 'reason'):
            print(url,"#####")
            print(('抓取失败，具体原因：', e.reason))
            request = urllib.request.Request(url = url, headers = headers)
            response = urllib.request.urlopen(request,timeout = 5)
            #page = response.read().decode('utf-8')
    soup=BeautifulSoup(response)

    trs = soup.find('table', {"id": "ip_list"}).findAll('tr')

    for tr in trs[1:]:
        tds=tr.findAll('td')
        ip=tds[2].text.strip()
        port=tds[3].text.strip()
        protocol=tds[6].text.strip()
        if protocol =='HTTP' or protocol=='HTTPS':
            file.write('%s=$s:%s\n'%(protocol,ip,port))
            print('%s://%s:%s'%(protocol,ip,port))