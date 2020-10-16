python3 -u check_server.py >/dev/null 2>>errorlog &
python3 -u logging_usage.py >/dev/null 2>>errorlog &
python3 -u get_server_status_remote.py >/dev/null 2>>errorlog &
python3 -u keep_heroku_awake.py >/dev/null 2>>errorlog &
