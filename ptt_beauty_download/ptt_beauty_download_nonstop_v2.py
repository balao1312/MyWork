import re, pathlib, requests, sys, time, datetime, concurrent.futures
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def lineNotifyMessage(line_token, msg):
    line_headers = {
        "Authorization": "Bearer " + line_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=line_headers, params=payload)
    return r.status_code


def helper(arg):
    pic_url = arg[0]
    folder_path = arg[1]
    return pic_download(pic_url, folder_path)

def pic_download(pic_url,folder_path):
    file_path = folder_path.joinpath(pic_url.split('/')[-1])
    try:
        pic = requests.get(pic_url, timeout=10)
    except Exception as e :
        print(f'oops, something is going wrong!\n{e}')
        return
    with open(file_path, 'wb') as p:
        p.write(pic.content)
    return 1        # 1= 成功下載未載過的圖片


def ptt_beauty_download():
    cookies = {'over18': '1'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.132 Safari/537.36'}

    pages = 5 # 每個 round 搜幾頁

    path = pathlib.Path.cwd().joinpath('beauty')
    if not pathlib.Path.exists(path):
        pathlib.Path.mkdir(path)

    print('資料將會放在 {} '.format(path))
    print('\n開始處理...\n')

    # 傳line
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
                article_title = tt.text.replace('/', ' ')
                if bool(re.search('肉特', article_title)):
                    print(f'處理文章 ： {tt.text}\n----幹不要再肉特文章了')
                    continue

                article_url = 'https://www.ptt.cc' + tt['href']
                article_res = requests.get(article_url, headers=headers, cookies=cookies)
                article_soup = BeautifulSoup(article_res.text, 'lxml')

                try:
                    article_time = article_soup.select('span[class="article-meta-value"]')[3].text
                except IndexError as e:
                    print(e)
                    print(article_url, ' 格式不符抓取設定')

                print(f'處理文章 ： {tt.text}')

                img_url_pattern = re.compile(r'(http).*(jpg|png|jpeg|gif)', re.IGNORECASE)
                no_ext_img_url_pattern = re.compile(r'https?://imgur.com/.*', re.IGNORECASE)
                no_ext_img_url_pattern_special = re.compile(r'https?://imgur.com/a/.*', re.IGNORECASE)

                article_content = article_soup.text.split('--')[0]
                filter_content = ''
                count = 0
                done = 0
                # 計算每篇文章的圖片總數量
                for each_line in article_content.split('\n'):
                    if bool(img_url_pattern.search(each_line)) or bool(no_ext_img_url_pattern.search(each_line)):
                        count += 1

                    # 去掉空行
                    if each_line.strip() != '':
                        filter_content += each_line + '\n'
                print('圖片數:',count)
                # 沒imgur圖片就跳下一篇文章
                if count == 0:
                    print(f'\t文章內沒有imgur圖片')
                    continue

                # 預覽內容跳過沒意義的行
                temp = "\n".join(list(filter(None, filter_content.split("\n")[8:])))
                filter_content = f'{article_title}\n{article_time}\n\n{temp}'

                # 圖片處理下載
                folder_path = path.joinpath(article_title.replace(':', '').strip())
                pic_urls = []
                for each_line in article_content.split('\n'):
                    # 找文章內是圖片網址的行
                    if bool(img_url_pattern.search(each_line)) or bool(no_ext_img_url_pattern.search(each_line)):
                        if not folder_path.exists():
                            folder_path.mkdir()

                            # for notice
                            new_article_count += 1
                            new_article_titles.append(article_title)
                            all_new_article_content += str(new_article_count) + ' :' + filter_content + '\n\n'

                        # 3種網址型態
                        if img_url_pattern.search(each_line):
                            pic_urls.append(img_url_pattern.search(each_line).group(0))
                        # 點進去代碼跟最後圖片不一樣的 還得另外 soup 一次
                        elif no_ext_img_url_pattern_special.search(each_line):
                            print('遇到要跳轉的imgur網頁')
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
                            pic_urls.append(f'https://i.imgur.com/{pic_code}.jpg')
                        else:
                            pic_code = no_ext_img_url_pattern.search(each_line).group(0).split('/')[-1]
                            pic_urls.append(f'https://i.imgur.com/{pic_code}.jpg')

                # 判斷有無下載過，有的話 done +1 然後從 list裡刪除，要刪除要從後面刪，不然索引值會變動然後出錯
                for i in range(len(pic_urls)-1,-1,-1):
                    file_path = folder_path.joinpath(pic_urls[i].split('/')[-1])
                    if file_path.exists():
                        done +=1
                        del pic_urls[i]

                if pic_urls :
                    folder_path_arg = [folder_path]
                    arguments_to_send = [(a,b) for a in pic_urls for b in folder_path_arg]
                    with concurrent.futures.ProcessPoolExecutor() as executor:
                        results = executor.map(helper, arguments_to_send)

                        for result in results:
                            if result == 1:
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
        print(f'runCycles = {total_cycle}\t{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : '
              f'new article count = {new_article_count}')
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

def main():
    ptt_beauty_download()

if __name__ == '__main__':
    main()