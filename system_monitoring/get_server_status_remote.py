import subprocess, requests, time, datetime


def lineNotifyMessage(line_token, msg):
    line_headers = {
        "Authorization": "Bearer " + line_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=line_headers, params=payload)
    return r.status_code

def get_server_status(server):
    server_name = server['name']
    server_ip = server['ip']
    server_user = server['user']

    cmd = f'scp {server_user}@{server_ip}:~/monitoring/logs/resources_log ./logs/{server_name}_resources_log'

    subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT)

    with open(f'logs/{server_name}_resources_log', 'r') as f:
        data = f.read()

    status = data.split('\n')[-2]
    checktime = status.split('|')[0]
    cpu = status.split('|')[1]
    mem = status.split('|')[2]
    disk = status.split('|')[3]
    swap = status.split('|')[4]

    msg = f'server : {server_name}\nchecktime : {checktime}\ncpu load : {cpu}\nmem usage : {mem}\nstorage usage : {disk}\n' \
          f'swap usage : {swap}\n'

    print(msg)

    if float(cpu.split(', ')[-1]) > 1.0 or float(mem.split(',')[0][:-1]) > 90.0 or \
            float(disk.split(',')[0][:-1]) > 90.0:
        try:
            msg = f"\nMBM server heavy loading !! \nstatus : \n{msg}"
            lineNotifyMessage(token, msg)
        except:
            print('line server failed')

    return msg


if __name__ == '__main__':
    token = '2unn268Rs1CkJ5JWGApbmwCPEB9qwSldVV5NNmukbFo'
    servers_to_check = [
        {'name': 'MBM', 'ip': '172.104.68.207', 'user': 'balao1312'},
        {'name': 'Linode', 'ip': '172.105.202.99', 'user': 'balao1312'}
    ]
    
    while 1:
        notify_msg = ''
        for each in servers_to_check:
            notify_msg += get_server_status(each) + '\n'

        if datetime.datetime.now().strftime('%M') == '00':
            try:
                lineNotifyMessage(token, notify_msg[:-1])
            except:
                print('line server failed')
        time.sleep(60)

