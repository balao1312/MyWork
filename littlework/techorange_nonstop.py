import requests
from bs4 import BeautifulSoup
import json
import pprint
import csv
import smtplib
from email.mime.text import MIMEText
import pickle, time

url = 'https://buzzorange.com/techorange/wp-admin/admin-ajax.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

ss = requests.session()
# 生成 post data  換頁需要
data_str = '''MIME Type: application/x-www-form-urlencoded; charset=UTF-8
action: fm_ajax_load_more
nonce: aadb1a53f7
page: 1'''

# 用生成式直接建字典
data = {i.split(': ')[0]: i.split(': ')[1] for i in data_str.split('\n')}

# 這網站不用cookie
# cookies_string = '''ClientID=3fc634b94729401fb3da089a13b4e585; _td=045bdd71-4e28-4c24-a848-a05aa3b76b12; __asc=108008461718ecaeeb6acba10e6; __auc=567251681718afc03d5112506f2; _fbp=fb.1.1587174704869.599352767; _ga=GA1.2.1226458808.1587174704; _gid=GA1.2.389082915.1587174704; _ss_pp_id=3e2c23c94c0f7385acb1586083632631; privacy_notice=1; AWSELB=F36D0F791E0088A8882B14A22BEB2618B7B242A79E17A8C0C9F671AD27C43898A846D44D6A5E8033CA89B107BFDC19F8C85F5AA9D2450BA07E63AFA309222955104E52534D; AWSELBCORS=F36D0F791E0088A8882B14A22BEB2618B7B242A79E17A8C0C9F671AD27C43898A846D44D6A5E8033CA89B107BFDC19F8C85F5AA9D2450BA07E63AFA309222955104E52534D; PHPSESSID=92cj63klird760n812gqs0d94g; __cfduid=d4867009169acd3e7f62cd5a6270bf5ac1586112426'''
# cookies={}
# for cc in cookies_string.split('; '):
#         ss.cookies[cc.split('=')[0]] = cc.split('=')[1]

pages = 2  # int(input('input pages : '))

while 1:
    try:
        with open('techorange_data', 'rb') as f:
            all_article = pickle.load(f)
    except:
        all_article = {}
    new_article_count = 0
    new_article_titles = []
    all_new_article_content = ''
    for m in range(pages):
        res = ss.post(url, headers=headers, data=data)
        # print(res.text)
        jdata = json.loads(res.text)
        # pprint.pprint(jdata)
        html = jdata['data']  # 判斷data標籤中的內容為 html 格式
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        titles = soup.select('h4[class="entry-title"] a')
        # print(titles)

        # if m == 0 and titles:
        #     with open('./techorange.csv', 'w') as f:
        #         csv_writer = csv.writer(f)
        #         datatitle = ['文章標題', '文章網址', '文章內容']
        #         csv_writer.writerow(datatitle)

        for tt in titles:
            article_title = tt.text
            article_url = tt['href']
            print(article_title)
            print(article_url)
            print()

            # 有新文章
            if article_title not in all_article:
                all_article[article_title] = article_url

                new_article_count += 1
                new_article_titles.append(article_title)
                all_new_article_content += f'{str(new_article_count)} :\n{article_title}\n{article_url}\n\n'

            # 取文章內容
            # article_res = ss.post(article_url, headers=headers, data=data)
            # soup = BeautifulSoup(article_res.text, 'html.parser')
            # print(soup.prettify())
            # article_contents = soup.select('div.fb-quotable p')

            # 想取文章時間 未確定
            # article_times = soup.select('time[class="entry-date published updated"]')
            # print(article_times[0].text)

            # 文章內容 結合成字串
            # sss = article_times[0].text + '\n'
            # for article_content in article_contents:
            #     #print(article_content.text)
            #     sss += article_content.text
            # print(sss)

        #     # with open('./techorange.csv','a',encoding='utf_8_sig') as f:
        #     #    csv.writer(f).writerow([article_title, article_url])

        data['page'] = 1 + m

    # 送出 email
    if new_article_count > 0:
        gmail_user = 'balao1312@gmail.com'
        gmail_password = 'ikjzinovbusndzpt'

        msg = MIMEText(all_new_article_content)
        msg['Subject'] = f'New {new_article_count} Article from TechOrange : {new_article_titles}'
        msg['From'] = gmail_user
        msg['To'] = 'balao1014@hotmail.com'

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()

        print('Email sent!')

    with open('techorange_data', 'wb') as f:
        pickle.dump(all_article, f)

    print('enter sleep')
    time.sleep(600)

# print(json.dumps(soup_json, indent=2, ensure_ascii=False))
