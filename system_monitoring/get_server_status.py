import subprocess, requests, time


def lineNotifyMessage(line_token, msg):
    line_headers = {
        "Authorization": "Bearer " + line_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=line_headers, params=payload)
    return r.status_code


if __name__ == '__main__':
    token = '2unn268Rs1CkJ5JWGApbmwCPEB9qwSldVV5NNmukbFo'

    while 1:
        # 305
        cmd = 'scp -P 23853 hadoop_admin@1.tcp.jp.ngrok.io:~/resource_log ./305_resource_log'

        subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT)

        with open('305_resource_log', 'r') as f:
            data = f.read()

        status = data.split('\n')[-2]
        checktime = status.split('|')[0]
        cpu = status.split('|')[1]
        mem = status.split('|')[2]
        disk = status.split('|')[3]

        # for screen output
        msg = f'server : 305\nchecktime : {checktime}\ncpu load : {cpu}\nmem usage : {mem}\nstorage usage : {disk}\n'
        print(msg)

        if float(cpu.split(', ')[-1]) > 1.0 or float(mem.split(',')[0][:-1]) > 90.0 or \
                float(disk.split(',')[0][:-1]) > 90.0:
            try:
                msg = f"\n305 server heavy loading !! \nstatus : \n{msg}"
                lineNotifyMessage(token, msg)
            except:
                print('line server failed')

        # GCP
        cmd = 'scp balao1312@35.194.137.72:~/resource_log ./GCP_resource_log'

        subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT)

        with open('GCP_resource_log', 'r') as f:
            data = f.read()

        status = data.split('\n')[-2]
        checktime = status.split('|')[0]
        cpu = status.split('|')[1]
        mem = status.split('|')[2]
        disk = status.split('|')[3]

        msg = f'server : GCP\nchecktime : {checktime}\ncpu load : {cpu}\nmem usage : {mem}\nstorage usage : {disk}\n'
        print(msg)

        if float(cpu.split(', ')[-1]) > 1.0 or float(mem.split(',')[0][:-1]) > 90.0 or \
                float(disk.split(',')[0][:-1]) > 90.0:
            try:
                msg = f"\nGCP server heavy loading !! \nstatus : \n{msg}"
                lineNotifyMessage(token, msg)
            except:
                print('line server failed')

        time.sleep(300)
