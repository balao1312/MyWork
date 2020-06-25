# -*- coding: UTF-8 -*-
import pathlib, requests
from bs4 import BeautifulSoup
from my_wordcloud_v2 import my_wordcloud

def get_article():
    cookies = {'over18': '1'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.132 Safari/537.36'}

    while 1:
        section = input('請問內容來自什麼版 : ')
        res = requests.get(f'https://www.ptt.cc/bbs/{section}/index.html', headers=headers, cookies=cookies)
        if res.status_code == 200:
            break
        else:
            print('版名有誤請重新輸入')
    pages = int(input('請問樣本想要取幾頁 : '))

    path = pathlib.Path.cwd()

    url = f'https://www.ptt.cc/bbs/{section}/index.html'

    print('\n開始處理...')

    filename = f'{section}_{pages}.txt'
    if path.joinpath(filename).exists():
        path.joinpath(filename).unlink()

    for m in range(pages):
        res = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div[class="title"] a')

        for tt in titles:
            # reset
            article_content = ''

            article_title = tt.text
            article_url = 'https://www.ptt.cc' + tt['href']

            article_res = requests.get(article_url, headers=headers, cookies=cookies)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')

            #單篇文章
            article_content += article_title
            article_content += '\n'.join(article_soup.select('div[id="main-content"]')[0].text.split('--')[0].split('\n')[1:])

            comment_lines = article_soup.select('div[id="main-content"]')[0].text.split('--')[-1]
            #print(comment_lines)
            for anyy in comment_lines.split('\n')[3:-1]:
                #print(anyy)
                try:
                    comment = anyy.split(':')[1][:-9]
                except IndexError as e:
                    #print(e,'發生在',anyy)
                    continue
                #print(comment)
                article_content += f'\n{comment}'

            with open(path.joinpath(filename), 'a', encoding= 'utf-8') as f:
                f.write(article_content)

        url = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
        print('已處理 {} 頁'.format(m+1))
    return filename

def main():
    filename = get_article()
    my_wordcloud(filename)


if __name__ == '__main__':
    main()