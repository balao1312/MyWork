import requests, csv, urllib, pathlib, time
import pandas as pd
from bs4 import BeautifulSoup
import concurrent.futures
import ssl  # mac 需要設定SSL   在使用urllib時

ssl._create_default_https_context = ssl._create_unverified_context


def one_page_scraping(url):
    cookie_string = '''__auc=e8e44726170e82e1140262dcf40; luauid=2114195893; _hjid=36896220-6ac2-4a4e-9f2a-e02131b76c69; _hp2_id.3192618648=%7B%22userId%22%3A%224093191121934740%22%2C%22pageviewId%22%3A%225912219665355168%22%2C%22sessionId%22%3A%223466139958157014%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; EPK=11b1d6296a4b858038e6e62693046b840; _hjTLDTest=1; ALGO_EXP_6019=C; _fbp=fb.2.1599043894424.1274873331; _gid=GA1.3.994276620.1599631655; AC=1599631668; R_PF=%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C202009091680364810761%2C%2C%2C; TS01f8a99d=01180e452dc96d057b5e07fac18bf071733431eac5f973a17c6210f3790dd04e4cb6c6e45975ea5604b63bff5358b3cbacc93b594bd6e2fe13f77da48f8414d84d9c4e6a3ab23276614df9ccc5d151e0399bc91851a9dfcad7a1a030bcc65b7b0fb34ff6ccb12fa14528e7a3e5618e5f07091eb99cdc33082c997c2293e261a58ac4c0edd4; JBCLOGIN.sig=3qt67ghG-ddAtNeilPH8APCQiXk; JBCLOGIN=BQbosSCPu9cJXdzaDEXO4f1ids2wJPwNt95GV9x4jJM; _uetsid=ad103f1aece69707246ad239b073ea24; _uetvid=d978c985a140a34bd95d81be22968902; COUNTER_SOURCE=AD_24676_98646%2C98647%2C98648%2C98649; bprofile_history=%5B%7B%22key%22%3A%22auxx12g%22%2C%22custName%22%3A%22%E8%8F%AF%E7%A2%A9%E9%9B%BB%E8%85%A6%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2Fauxx12g%22%7D%2C%7B%22key%22%3A%221a2x6bj8og%22%2C%22custName%22%3A%22%E6%98%93%E5%8B%9D%E8%B3%87%E8%A8%8A%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bj8og%22%7D%2C%7B%22key%22%3A%221a2x6bi0qr%22%2C%22custName%22%3A%22%E5%B7%A8%E6%80%9D%E7%A7%91%E6%8A%80%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bi0qr%22%7D%2C%7B%22key%22%3A%221a2x6bkxph%22%2C%22custName%22%3A%22%E4%BC%8A%E8%AB%BE%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bkxph%22%7D%2C%7B%22key%22%3A%221a2x6bl4fc%22%2C%22custName%22%3A%22%E5%BE%B7%E5%88%A9%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bl4fc%22%7D%2C%7B%22key%22%3A%221a2x6bi1ab%22%2C%22custName%22%3A%22%E9%81%94%E6%9A%89%E8%B3%87%E8%A8%8A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bi1ab%22%7D%2C%7B%22key%22%3A%22b8e4baw%22%2C%22custName%22%3A%22%E7%9A%93%E5%B1%95%E8%B3%87%E8%A8%8A%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2Fb8e4baw%22%7D%2C%7B%22key%22%3A%2213quahyo%22%2C%22custName%22%3A%22%E7%8E%89%E5%B1%B1%E9%8A%80%E8%A1%8C_%E7%8E%89%E5%B1%B1%E5%95%86%E6%A5%AD%E9%8A%80%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F13quahyo%22%7D%2C%7B%22key%22%3A%221xzkino%22%2C%22custName%22%3A%22%E5%9C%8B%E6%B3%B0%E4%B8%96%E8%8F%AF%E5%95%86%E6%A5%AD%E9%8A%80%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8_%E4%BA%BA%E5%8A%9B%E8%B3%87%E6%BA%90%E9%83%A8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1xzkino%22%7D%2C%7B%22key%22%3A%22asvjd8g%22%2C%22custName%22%3A%22%E7%85%99%E6%B3%A2%E5%A4%A7%E9%A3%AF%E5%BA%97%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2Fasvjd8g%22%7D%2C%7B%22key%22%3A%22b69ox5c%22%2C%22custName%22%3A%22(MyMusic%EF%BC%8C%E5%8F%B0%E7%81%A3%E5%A4%A7%E5%93%A5%E5%A4%A7%E5%AD%90%E5%85%AC%E5%8F%B8)%E5%8F%B0%E7%81%A3%E9%85%B7%E6%A8%82%E6%99%82%E4%BB%A3%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2Fb69ox5c%22%7D%5D; job_same_ab=2; _gaexp=GAX1.3.ydox8u6PTwaYoX5PSnzxXA.18578.1!JA0tMycRRhS-5EjRcXg0uA.18521.1!TR-R_HpzRVS6WpOAaNbMWA.18521.0!exRHFuUvRIOmFqAn4Hv8dQ.18574.1; _gat_UA-15276226-1=1; TS016ab800=01180e452de63b475930ba6d46100fb7c520145bc15ad564ccd776c20b30be21d4ad09186b5fa07cd3f00fd333a0a6f072008ab163ff92615de3ef04edfc9d1363a53cddac81b874e7211e856570135d2747fd29aadf5c869227bfe38d547e0977f5b1fcb9066b45f34a4878b6ee9e769ad1e1ef0895f34ae222c2eaf784e781a7d298be0ec1f2adc90fdf81a22b25caaf167c9847f4125393c6368e65f85b5597f75f5f0acf74398ab8fe7ff4d7dcb2c69bd04e2b; __asc=35038c6b17473a897cd39e2167a; _ga_W9X1GB1SVR=GS1.1.1599668094.61.1.1599668263.59; _ga_FJWMQR9J2K=GS1.1.1599668094.61.1.1599668263.0; _ga=GA1.3.1049900863.1584443298; _dc_gtm_UA-15276226-1=1; lup=2114195893.5001489413863.4623532291991.1.4640712161167; lunp=4623532291991'''

    data = {i.split('=')[0]: i.split('=')[1] for i in cookie_string.split('; ')}

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

    static_folder = pathlib.Path.cwd().joinpath('static')

    specialty_dict = {}  # 字典存技能統計
    edu_req_dict = {'高中以上': 0, '專科以上': 0, '大學以上': 0, '碩士以上': 0, '不拘': 0}  # 字典存學歷需求
    major_req_dict = {}  # 字典存科系要求
    count = 0  # 資料總筆數

    ss = requests.session()
    ss.headers[
        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    res = ss.post(url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    job_name_list = soup.select('article', class_="js-job-item")

    result_list = []
    for job in job_name_list:
        try:
            comp_name = job['data-cust-name']
            job_name = job['data-job-name']

            detail_link = 'http:' + job.select_one('a', class_='js-job-link')['href']

            # 取得細項網址
            detail_code = detail_link.split('/')[-1].split('?')[0]
            detail_link_oo = 'https://m.104.com.tw/job/' + detail_code

            # print(detail_link_oo)
            print(comp_name)
            print(job_name)
            print(detail_link)
            print(detail_link_oo)

            # ss.max_redirects = 600
            res = ss.post(detail_link_oo, timeout=10, allow_redirects=False)
            res = res.text
            # print(res)
            dfs = pd.read_html(res)
            # print(len(dfs))
            # for ii,dd in enumerate(dfs):
            #     print(ii)
            #     print(dd)
            #     print('-'*40)

            # 開始建細項list
            detail_list = [comp_name, job_name]  # 公司名稱、職缺名稱

            detail_list.append(detail_link)  # 徵才網址

            detail_list.append(dfs[1].iat[0, 1][:-5])  # 薪水區間
            detail_list.append(dfs[0].iat[1, 1][-2:])  # 工作性質
            detail_list.append(dfs[0].iat[0, 1])  # 工作地點
            detail_list.append(dfs[2].iat[3, 1])  # 管理責任
            detail_list.append(dfs[2].iat[0, 1])  # 出差外派
            detail_list.append(dfs[2].iat[1, 1])  # 上班時段
            detail_list.append(dfs[2].iat[2, 1])  # 休假制度
            detail_list.append(dfs[3].iat[1, 1])  # 可上班日
            detail_list.append(dfs[0].iat[2, 1])  # 需求人數
            detail_list.append(dfs[3].iat[0, 1])  # 接受身份
            detail_list.append(dfs[3].iat[2, 1])  # 工作經歷
            detail_list.append(dfs[3].iat[3, 1])  # 學歷要求

            # 學歷要求統計
            if '不拘' in dfs[3].iat[3, 1]:
                edu_req_dict['不拘'] += 1
            elif '高中' in dfs[3].iat[3, 1]:
                edu_req_dict['高中以上'] += 1
            elif '專科' in dfs[3].iat[3, 1]:
                edu_req_dict['專科以上'] += 1
            elif '大學' in dfs[3].iat[3, 1]:
                edu_req_dict['大學以上'] += 1
            elif '碩士' in dfs[3].iat[3, 1]:
                edu_req_dict['碩士以上'] += 1

            # 科系要求
            ffilter = (dfs[3][0] == '科系要求：')
            # print(f'科系要求: \n{dfs[3][ff]}')
            if len(dfs[3][ffilter]):
                detail_list.append(dfs[3][ffilter].iat[0, 1])
                # 科系要求統計
                majors = dfs[3][ffilter].iat[0, 1].split('、')
                for major in majors:
                    if not major in major_req_dict:
                        major_req_dict[major] = 1
                    else:
                        major_req_dict[major] += 1
            else:
                detail_list.append('不拘')

            # 語文條件
            ffilter = (dfs[3][0] == '語文條件：')
            # print(f'科系要求: \n{dfs[3][ff]}')
            if len(dfs[3][ffilter]):
                detail_list.append(dfs[3][ffilter].iat[0, 1])
            else:
                detail_list.append('不拘')

            # 擅長工具
            ffilter = (dfs[3][0] == '擅長工具：')
            # print(f'科系要求: \n{dfs[3][ff]}')
            if len(dfs[3][ffilter]):
                detail_list.append(dfs[3][ffilter].iat[0, 1])
                # 擅長工具統計
                specialtys = dfs[3][ffilter].iat[0, 1].split('、')
                for specialty in specialtys:
                    if not specialty in specialty_dict:
                        specialty_dict[specialty] = 1
                    else:
                        specialty_dict[specialty] += 1
            else:
                detail_list.append('不拘')

        except Exception as e:
            print('======================')
            print('目標不符設定 錯誤內容 ： ')
            print(e)
            print('======================')
            continue
        count += 1
        print(detail_list)
        result_list.append(detail_list)
        time.sleep(3)



    print(count)
    # print(result_list)
    result_df = pd.DataFrame(result_list)
    # result_df.to_csv('result.csv')
    return result_df

def web_scraping(keyword, pages):

    keyword_url_format = urllib.parse.quote(keyword)  # 中文字轉 url 格式

    static_folder = pathlib.Path.cwd().joinpath('static')

    # 寫入 csv 檔的標頭
    with open(static_folder.joinpath(f'104_result_{keyword}x{pages}.csv'), 'w', encoding='utf_8_sig') as csv_file:
        csv_writer = csv.writer(csv_file)
        datatitle = ['公司名稱', '職缺名稱', '徵才網址', '薪水區間', \
                     '工作性質', '工作地點', '管理責任', '出差外派', '上班時段',
                     '休假制度', '可上班日', '需求人數', '接受身份', '工作經歷', '學歷要求', \
                     '科系要求', '語文條件', '擅長工具']
        csv_writer.writerow(datatitle)

    # startpage 初始是1
    # startpage += 1
    # url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=' + keyword + '&order=15&asc=0&page=' + str(
    #     page) \
    #       + '&mode=l&jobsource=2018indexpoc'

    urls = ['https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=' + keyword_url_format + '&order=15&asc=0&page=' +
            str(page + 1) + '&mode=l&jobsource=2018indexpoc' for page in range(pages)]

    for url in urls:
        print(url)

    # total_df = pd.DataFrame()
    with concurrent.futures.ProcessPoolExecutor() as excutor:
        excutor.map(one_page_scraping, urls)

        # for result in results:
        #     total_df.append(result)

    # print(total_df)

    # # 每完成一項職缺的細項抓取 就寫入一列資料到剛剛建好標頭的csv檔 這邊開檔用 a = append
    # with open(static_folder.joinpath(f'104_result_{keyword}x{pages}.csv'), 'a',
    #           encoding='utf_8_sig') as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     csv_writer.writerow(detail_list)

        # print(f'已完成 {i + 1} / {pages} 頁')

    # 處理統計專長的字典 這行是用value排序後回傳一個新的 list, 字典.item() 可以將字典轉成含有 key & value 的 list
    # specialty_dict_sorted = sorted(specialty_dict.items(), key=lambda d: d[1], reverse=True)
    # edu_req_dict_sorted = sorted(edu_req_dict.items(), key=lambda d: d[1], reverse=True)
    # major_req_dict_sorted = sorted(major_req_dict.items(), key=lambda d: d[1], reverse=True)
    #
    # print(f'完成處理，總共有 {count} 筆資料')

    # 回傳接下來畫圖需要的變數
    # return {'specialty_dict_sorted': specialty_dict_sorted, 'edu_req_dict_sorted': edu_req_dict_sorted,
    #         'major_req_dict_sorted': major_req_dict_sorted, 'count': count}


if __name__ == '__main__':
    web_scraping('資訊工程', 3)
    # w1 = one_page_scraping('https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=資訊工程&order=15&asc=0&page=1&mode=l&jobsource=2018indexpoc')
    # w2 = one_page_scraping('https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=資訊工程&order=15&asc=0&page=2&mode=l&jobsource=2018indexpoc')
    # w3 = one_page_scraping(
    #     'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=資訊工程&order=15&asc=0&page=3&mode=l&jobsource=2018indexpoc')

    # df = w1.append(w2)
    # print(w1)
    # print(df)