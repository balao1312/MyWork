import datetime
import subprocess
import time
import pathlib

log_dir = pathlib.Path.cwd().joinpath('log')
if not log_dir.exists():
    log_dir.mkdir()

while 1:
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    cmd = 'uptime'
    result = subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT).decode('utf8')
    # print(result)
    cpu_status = list(filter(None, result.split(' ')))
    cpu_load = f'{cpu_status[-3]} {cpu_status[-2]} {cpu_status[-1][:-2]}'
    #print(cpu_load)

    # print(cpu_load)

    cmd = 'free'
    result = subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT).decode('utf8')
    # print(result)
    mem_status = result.split('\n')[1].split(' ')
    mem_status = list(filter(None, mem_status))
    mem_total = mem_status[1]
    mem_available = mem_status[6]
    mem_used = mem_status[2]
    # print(mem_status)
    mem_usage = round((int(mem_used) / int(mem_total))*100, 1)
    mem_total = round((int(mem_total) / 1024 / 1024), 0)
    # print(mem_total, mem_available)

    cmd = 'df -h'
    result = subprocess.check_output([cmd], timeout=10, shell=True, stderr=subprocess.STDOUT).decode('utf8')
    # print(result)
    storage_status = result.split('\n')[3].split(' ')
    storage_total = list(filter(None, storage_status))[1]
    sotrage_usage = list(filter(None, storage_status))[4]
    # print(storage)

    with open(log_dir.joinpath('resources_log'), 'a') as f:
        f.write(f'{now_time}|{cpu_load}|{mem_usage}%, {mem_total}G|{sotrage_usage}, {storage_total}\n')

    time.sleep(60)
