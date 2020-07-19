import subprocess, requests, time, datetime


def lineNotifyMessage(line_token, msg):
    line_headers = {
        "Authorization": "Bearer " + line_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=line_headers, params=payload)
    return r.status_code


def check_server(ip, port, service_name):
    cmd = f'nc -vz {ip} {port} -w 3'
    print(f'==> Checking {service_name} on {ip}:{port}')

    count = 0
    while 1:
        try:
            subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT)
            return {service_name: 'alive'}
        except:
            count += 1
            if count == 3:
                return {service_name: 'dead'}
            continue


if __name__ == '__main__':

    print('Start Monitoring all server ...')
    token = '2unn268Rs1CkJ5JWGApbmwCPEB9qwSldVV5NNmukbFo'

    # 定義有哪些 server 要監控
    servers_to_check = [
        {'ip': '35.194.137.72', 'port': 9092, 'service_name': 'kafka'},
        {'ip': '35.194.137.72', 'port': 6379, 'service_name': 'redis'},
        {'ip': '34.80.186.211', 'port': 3306, 'service_name': 'MySQL_GCP'},
        {'ip': '1.tcp.jp.ngrok.io', 'port': 23879, 'service_name': 'MySQL_local'},
        {'ip': '1.tcp.jp.ngrok.io', 'port': 23853, 'service_name': 'Hadoop_HDFS'},
        {'ip': '35.194.191.163', 'port': 9200, 'service_name': 'Elasticsearch'},
        {'ip': '35.194.191.163', 'port': 5601, 'service_name': 'Kibana'}

    ]

    server_status = {}

    while 1:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # 每五分鐘檢查有沒有server死掉，有就回報
        if datetime.datetime.now().minute % 5 == 0:
            for each in servers_to_check:
                server_status.update(check_server(each['ip'], each['port'], each['service_name']))

            for service, status in server_status.items():
                if status == 'dead':
                    msg = f'\n[{now_time}] Oops !! {service} is dead !!'
                    try:
                        lineNotifyMessage(token, msg)
                    except:
                        print('!! Problem with line server')

                    print(f'\n[{now_time}] Oops !! {service} is dead !!')
                    open('server_status_log', 'a').write(f'\n[{now_time}] {service} is down')

            print(f'\n[{now_time}] server_status : {server_status}')
            print('=' * 80)
            open('server_status_log', 'a').write(f'\n[{now_time}] server_status : {server_status}')

        # 每小時送一次狀態給 line
        if datetime.datetime.now().strftime('%M') == '00':

            if not 'dead' in server_status.values():

                try:
                    lineNotifyMessage(token, f'\n[{now_time}] All server working fine')
                except:
                    print('!! Problem with line server')

        time.sleep(60)

    # test
    # for each in servers_to_check:
    #     server_status.update(check_server(each['ip'], each['port'], each['service_name']))
    # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    #
    # print(f'\n[{now_time}] server_status : {server_status}')
    # msg = f'\n[{now_time}] server_status : \n{server_status}\n'
    # for service, status in server_status.items():
    #     msg += f'{service} status : {status}\n'
    # lineNotifyMessage(token, msg)
