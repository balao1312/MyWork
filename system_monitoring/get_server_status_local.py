import subprocess, requests, time
import pathlib
import datetime


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
    log_path = pathlib.Path.cwd().joinpath('log').joinpath('resources_log')

    while 1:
        with open(log_path, 'r') as f:
            data = f.read()

        status = data.split('\n')[-2]
        checktime = status.split('|')[0]
        cpu = status.split('|')[1]
        mem = status.split('|')[2]
        disk = status.split('|')[3]
        swap = status.split('|')[4]

        # for screen output
        msg = f'server : linode\nchecktime : {checktime}\ncpu load : {cpu}\nmem usage : {mem}\nstorage usage : {disk}\n' \
              f'swap usage : {swap}'
        print(msg)

        if float(cpu.split(', ')[-1]) > 1.0 or float(mem.split(',')[0][:-1]) > 90.0 or \
                float(disk.split(',')[0][:-1]) > 90.0:
            try:
                msg = f"\nlinode server heavy loading !! \nstatus : \n{msg}"
                lineNotifyMessage(token, msg)
            except:
                print('line server failed')

        if datetime.datetime.now().strftime('%M') == '00':
            try:
                lineNotifyMessage(token, msg)
            except:
                print('!! Problem with line server')

        time.sleep(60)
