import requests, pprint, pandas
from bs4 import BeautifulSoup

ss = requests.session()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}
pages = 10      # 總頁數
current_page = 1
for m in range(pages):
    url = f'https://newhouse.591.com.tw/home/housing/search?rid=1&page={current_page + m}&sid='
    res = ss.get(url, headers=headers).json()

    for anyy in res['data']['items']:
        # pprint.pprint(anyy)
        # print(len(res['data']['items']))  #20筆

        # 把每筆物件的標籤整合為一個字串  不然印成csv會變多列
        tag_str=''
        for anyyy in anyy['tag']:
            tag_str += anyyy + ' '
        anyy['tag'] = tag_str

        # bid = 細項網址
        anyy['bid'] = 'https://newhouse.591.com.tw/home/housing/detail?hid=' + str(anyy['hid'])

        # 去除不重要的欄位
        if 'video_pic' in anyy:
            del anyy['video_pic']
        if 'event_show_url' in anyy:
            del anyy['event_show_url']
        if 'event_click_url' in anyy:
            del anyy['event_click_url']
        if 'event_show' in anyy:
            del anyy['event_show']
        if 'event_click' in anyy:
            del anyy['event_click']
        if 'cover' in anyy:
            del anyy['cover']
        if 'native_orderno' in anyy:
            del anyy['native_orderno']
        if 'is_video' in anyy:
            del anyy['is_video']
        if 'isvip' in anyy:
            del anyy['isvip']

        pprint.pprint(anyy)

        # 建立 dataframe
        tt = pandas.DataFrame.from_dict(anyy,orient='index').T

        # 第一頁第一筆時重開檔案，其它時候 append 上去
        if anyy == res['data']['items'][0] and m == 0:
            tt.to_csv('591.csv', mode='w', encoding='utf-8-sig', index=False)
        else:
            tt.to_csv('591.csv', mode='a', encoding='utf-8-sig', header=False, index=False)
