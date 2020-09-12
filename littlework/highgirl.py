import re
import os
import requests
from bs4 import BeautifulSoup
import json
import pprint

ss = requests.session()
# cookies_string='''sails.sid4=s%3Agl8P9fcg0ThF-zM7yGsK_N_a4FpVf6yi.LKWA7TpyNapcTs2emaXs45%2BNUKHYgZZgUJhdLp9CtH0; _ga=GA1.2.1504423313.1584926401; _gid=GA1.2.854934376.1584926401'''
# for cc in cookies_string.split(';'):
#         ss.cookies[cc.split('=')[0]] = cc.split('=')[1]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}
url = 'https://meteor.today/beautycampaign/get_candidates'
res = ss.get(url, headers=headers)
# print(res.text)
jdata = json.loads(res.text)
# pprint.pprint(jdata)

if not os.path.exists('./highgirl'):
    os.mkdir('./highgirl')
path = './highgirl'
for eachone in jdata['result']:
    print(eachone['name'])
    for i in range(1, 4):
        pp = 'img_' + str(i)
        pic = requests.get(eachone[pp])
        with open(path + '/' + eachone['name'] + '_' + str(i) + '.jpeg', 'wb') as f:
            f.write(pic.content)

print('done')
