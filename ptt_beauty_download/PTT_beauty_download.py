import re, pathlib, requests, sys
from bs4 import BeautifulSoup

cookies = {'over18': '1'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}
url = 'https://www.ptt.cc/bbs/beauty/index.html'

path = pathlib.Path.cwd().joinpath('beauty')
if not pathlib.Path.exists(path):
    pathlib.Path.mkdir(path)

who = input('搜尋主題：正妹=1，帥哥=2，神人=3，廣告=4，全部=5。 請輸入選擇 ： ')
who_dict = {'1':'正妹', '2':'帥哥', '3':'神人', '4':'廣告', '5':''}
who = who_dict[who]
pages = int(input('請問想要爬幾頁(一頁大約10篇文章) : '))
keywords = input('有要加入關鍵字嗎？(沒有請直接enter) : ')
pushleast = input('請問要過濾推文數大於多少？(不過濾請直接enter) : ')
pushleast = 0 if pushleast == '' else int(pushleast)

# 同時印在 terminal 跟寫入 log檔
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.flush()  # 每次寫入後更新 清空暫存

    def flush(self):
        self.log.flush()

sys.stdout = Logger('log.txt')

print('資料將會放在 {} '.format(path))
print('\n開始處理...\n')
for m in range(pages):
    res = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('div[class="title"] a')

    for tt in titles:
        article_title = tt.text.replace('/', ' ')
        if not who in article_title:
            print(f'\t{tt.text} \n\t\t不屬於搜尋類別')
            continue
        if not bool(re.search(keywords, article_title, re.IGNORECASE)):
            print(f'\t{tt.text} \n\t\t不含關鍵字')
            continue

        article_url = 'https://www.ptt.cc' + tt['href']
        article_res = requests.get(article_url, headers=headers, cookies=cookies)
        article_soup = BeautifulSoup(article_res.text, 'html.parser')

        push = 0
        each_comment_line = article_soup.text.split('--\n')[-1].strip().split('\n')
        for ss in each_comment_line:
            if ss:
                if list(ss)[0] == '推': push += 1
        if pushleast != 0 and push < pushleast:
            print(f'\t{tt.text} \n\t\t推文數太少')
            continue

        if keywords == '':
            print(f'處理文章 ： {tt.text}')
        else:
            print(f'！！找到符合文章 : {tt.text}')

        count = 0
        done = 0
        img_url_pattern = re.compile(r'(http).*(jpg|png|jpeg|gif)', re.IGNORECASE)
        no_ext_img_url_pattern = re.compile(r'https://imgur.com/.*[^\.]', re.IGNORECASE)

        # 計算每篇文章的圖片總數量
        for each_line in article_soup.text.split('--')[0].split('\n'):
            if bool(img_url_pattern.search(each_line)) or bool(no_ext_img_url_pattern.search(each_line)):
                count += 1
        if count == 0:
            print(f'\t文章內沒有imgur圖片')
            continue

        pic_url=''
        for each_line in article_soup.text.split('--')[0].split('\n'):
            if bool(img_url_pattern.search(each_line)) or bool(no_ext_img_url_pattern.search(each_line)):
                folder_path = path.joinpath(article_title)
                if not folder_path.exists():
                    folder_path.mkdir()

                if img_url_pattern.search(each_line):
                    pic_url = img_url_pattern.search(each_line).group(0)
                else:
                    pic_code = no_ext_img_url_pattern.search(each_line).group(0).split('/')[-1]
                    pic_url = f'https://i.imgur.com/{pic_code}.jpg'

                file_path = folder_path.joinpath(pic_url.split('/')[-1])
                if file_path.exists():
                    done += 1
                    continue

                try:
                    pic = requests.get(pic_url, timeout=10)
                except :
                    print('oops, something is not responding')
                    continue
                with open(file_path, 'wb') as p:
                    p.write(pic.content)
                    done += 1
                    print(f'抓抓  {done} / {count}')
        print('--已收藏')

    url = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
    print('=========================')
    print(f'已處理了 {m+1} / {pages} 頁')
    print('=========================')

sys.stdout = sys.__stdout__