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
        except subprocess.TimeoutExpired:
            print(f'cant reach {service_name}, retrying ...')
            count += 1
            if count == 3:
                return {service_name: 'dead'}
            continue


if __name__ == '__main__':

    print('Start Monitoring all server ...')
    token = '2unn268Rs1CkJ5JWGApbmwCPEB9qwSldVV5NNmukbFo'

    # 定義有哪些 server 要監控
    servers_to_check = [
        {'ip': '172.105.202.99', 'port': 9092, 'service_name': 'kafka'},
        {'ip': '172.105.202.99', 'port': 6379, 'service_name': 'redis'},
        {'ip': '172.105.202.99', 'port': 3306, 'service_name': 'MySQL'},
        {'ip': '172.104.68.207', 'port': 22, 'service_name': 'MBM_vm'},
        {'ip': '172.104.68.207', 'port': 5432, 'service_name': 'PostgreSQL'}
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
                    msg = f'[{now_time}] Oops !! {service} is dead !!\n'
                    try:
                        lineNotifyMessage(token, msg)
                    except:
                        print('!! Problem with line server')

                    print(f'[{now_time}] Oops !! {service} is dead !!\n')
                    open('./logs/server_status_log', 'a').write(f'\n[{now_time}] {service} is down')

            print(f'[{now_time}] server_status : {server_status}\n')
            print('=' * 80)
            open('./logs/server_status_log', 'a').write(f'[{now_time}] server_status : {server_status}\n')

        # 每小時送一次狀態給 line
        if datetime.datetime.now().strftime('%M') == '00':

            if 'dead' not in server_status.values():

                try:
                    lineNotifyMessage(token, f'[{now_time}] All server working fine\n')
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

