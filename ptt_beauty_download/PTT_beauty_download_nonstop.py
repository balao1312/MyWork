import re, pathlib, requests, sys, time, datetime
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

cookies = {'over18': '1'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}
url = 'https://www.ptt.cc/bbs/beauty/index.html'

path = pathlib.Path.cwd().joinpath('beauty')
if not pathlib.Path.exists(path):
    pathlib.Path.mkdir(path)

who = '5' #input('搜尋主題：正妹=1，帥哥=2，神人=3，廣告=4，全部=5。 請輸入選擇 ： ')
who_dict = {'1':'正妹', '2':'帥哥', '3':'神人', '4':'廣告', '5':''}
who = who_dict[who]
pages = 5 #int(input('請問想要爬幾頁(一頁大約10篇文章) : '))
keywords = '' #input('有要加入關鍵字嗎？(沒有請直接enter) : ')
pushleast = '' #input('請問要過濾推文數大於多少？(不過濾請直接enter) : ')
pushleast = 0 if pushleast == '' else int(pushleast)

print('資料將會放在 {} '.format(path))
print('\n開始處理...\n')

# 傳line
def lineNotifyMessage(token, msg):
    headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/x-www-form-urlencoded"
                }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

token = '2unn268Rs1CkJ5JWGApbmwCPEB9qwSldVV5NNmukbFo'
# message = 'new session start'
# lineNotifyMessage(token, message)

total_cycle = 0
while 1:
    t1 = time.time()
    # for notice
    new_article_count = 0
    new_article_titles = []
    all_new_article_content = ''

    url = 'https://www.ptt.cc/bbs/beauty/index.html'
    for m in range(pages):
        res = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(res.text, 'lxml')
        titles = soup.select('div[class="title"] a')

        for tt in titles:
            author = ''
            article_time = ''
            article_title = tt.text.replace('/', ' ')
            if not who in article_title:
                print(f'\t{tt.text} \n\t\t不屬於搜尋類別')
                continue
            if not bool(re.search(keywords, article_title, re.IGNORECASE)):
                print(f'\t{tt.text} \n\t\t不含關鍵字')
                continue
            if bool(re.search('肉特', article_title)):
                print('幹不要再肉特了')
                continue

            article_url = 'https://www.ptt.cc' + tt['href']
            article_res = requests.get(article_url, headers=headers, cookies=cookies)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')

            try:
                author = article_soup.select('span[class="article-meta-value"]')[0].text
                article_time = article_soup.select('span[class="article-meta-value"]')[3].text
            except IndexError as e:
                print(e)
                print(article_url, ' 格式不符抓取設定')

            article_url = 'https://www.ptt.cc' + tt['href']
            article_res = requests.get(article_url, headers=headers, cookies=cookies)
            article_soup = BeautifulSoup(article_res.text, 'lxml')

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
            no_ext_img_url_pattern = re.compile(r'https://imgur.com/.*[^/\.]', re.IGNORECASE)
            no_ext_img_url_pattern_special = re.compile(r'https://imgur.com/a/.*[^\.]', re.IGNORECASE)
            article_content = ''

            # 計算每篇文章的圖片總數量
            for each_line in article_soup.text.split('--')[0].split('\n'):
                if bool(img_url_pattern.search(each_line)) or bool(no_ext_img_url_pattern.search(each_line)):
                    count += 1

                # 去掉空行
                if each_line.strip() != '':
                    article_content += each_line + '\n'

            # 預覽內容跳過沒意義的行
            main_content = "\n".join(list(filter(None, article_content.split("\n")[8:])))
            article_content = f'{article_title}\n{article_time}\n\n{main_content}'

            if count == 0:
                print(f'\t文章內沒有imgur圖片')
                continue

            # 圖片處理下載
            pic_url=''
            for each_line in article_soup.text.split('--')[0].split('\n'):
                if bool(img_url_pattern.search(each_line)) or bool(no_ext_img_url_pattern.search(each_line)):
                    folder_path = path.joinpath(article_title.replace(':', '').strip())
                    if not folder_path.exists():
                        folder_path.mkdir()

                        # for notice
                        new_article_count += 1
                        new_article_titles.append(article_title)
                        all_new_article_content += str(new_article_count) + ' :' + article_content + '\n\n'

                    if img_url_pattern.search(each_line):
                        pic_url = img_url_pattern.search(each_line).group(0)

                    # 點進去代碼跟最後圖片不一樣的 還得另外 soup 一次
                    elif no_ext_img_url_pattern_special.search(each_line):
                        extra_url = no_ext_img_url_pattern_special.search(each_line).group(0)
                        extra_res = requests.get(extra_url)
                        aa = BeautifulSoup(extra_res.text, 'lxml')
                        try:
                            aa = aa.select('div[class="post-images"]')[0]
                        except IndexError as e:
                            print(f'{e}:\n出錯網址：\n{each_line}')
                            continue
                        pic_code = aa.select('div', class_='post-image-container')[0]['id']
                        # print(pic_code)
                        pic_url = f'https://i.imgur.com/{pic_code}.jpg'
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
                        print('oops, something is going wrong!')
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

    # 暫改 stdout 去寫 log檔
    sys.stdout = open('log.txt', 'a')
    if total_cycle == 0 : print()
    print(f'runCycles = {total_cycle}\t{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : new article count = {new_article_count}')
    sys.stdout = sys.__stdout__

    # 如果有新文章
    if new_article_count > 0:
        title_list_str = ''
        for title in new_article_titles:
            if title != new_article_titles[-1]:
                title_list_str += title + ', '
            else:
                title_list_str += title

        # 傳Line
        message = f'{new_article_count} New article(s) : {title_list_str}\n{all_new_article_content}'
        lineNotifyMessage(token, message)
        print('Line message sent !')

        sys.stdout = open('new_article_note.txt','a')
        print(message)
        sys.stdout = sys.__stdout__
    t2 = time.time()
    print(f'{t2-t1:.2f} s')
    print('enter sleep 600s')
    total_cycle += 1
    time.sleep(600)