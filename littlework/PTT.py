# -*- coding: UTF-8 -*-
import re, os, pathlib, datetime, requests
from bs4 import BeautifulSoup

cookies = {'over18': '1'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

while 1:
    section = input('請問想要爬什麼版 : ')
    res = requests.get('https://www.ptt.cc/bbs/{}/index.html'.format(section), headers=headers, cookies=cookies)
    if res.status_code == 200:
        break
    else:
        print('版名有誤請重新輸入')
pages = int(input('請問想要爬幾頁 : '))
pushleast = input('請問要過濾推文數大於多少？ : ')
keyword = input('請輸入要過濾內容的關鍵字(不需要的話請直接enter) ： ')
foldername = f'{section}_{str(datetime.date.today())}'

pushleast = 0 if pushleast == '' else int(pushleast)
path = pathlib.Path.cwd().joinpath(foldername)
if not pathlib.Path.exists(path):
    pathlib.Path.mkdir(path)

url = 'https://www.ptt.cc/bbs/{}/index.html'.format(section)

print(f'資料將會放在 {path} ')
print('\n開始處理...')
for m in range(pages):
    res = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('div[class="title"] a')

    for tt in titles:
        # reset
        author = ''
        datetime = ''
        article_content = ''
        push = 0
        boo = 0
        arrow = 0

        article_title = tt.text
        article_url = 'https://www.ptt.cc' + tt['href']

        article_res = requests.get(article_url, headers=headers, cookies=cookies)
        article_soup = BeautifulSoup(article_res.text, 'html.parser')

        #單篇文章
        article_content = article_soup.select('div[id="main-content"]')[0].text
        try:
            author = article_soup.select('span[class="article-meta-value"]')[0].text
            datetime = article_soup.select('span[class="article-meta-value"]')[3].text
        except IndexError as e:
            print(e)
            print(article_url,' 格式不符抓取設定')

        each_comment_line = article_content.split('--\n')[-1].strip().split('\n')
        for ss in each_comment_line:
            if ss:
                if list(ss)[0] == '推': push += 1
                if list(ss)[0] == '噓': boo += 1
                if list(ss)[0] == '→': arrow += 1

        article_content += '\n----------------------------------------------\n'
        article_content += '作者 ： ' + author + '\n'
        article_content += '時間 ： ' + datetime + '\n'
        article_content += '標題 ： ' + article_title + '\n'
        article_content += '推 ： ' + str(push) + '\n'
        article_content += '噓 ： ' + str(boo) + '\n'
        article_content += '→ ： ' + str(arrow) + '\n'

        filename = article_title.replace('/', '').replace('?', '').replace(':', '') + '.txt'

        if bool(re.search(keyword, article_content, re.IGNORECASE)):
            if pushleast == 0 or push > pushleast :
                with open(path.joinpath(filename), 'w', encoding= 'utf-8') as f:
                    f.write(article_content)

    url = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
    print('已處理 {} 頁'.format(m+1))
