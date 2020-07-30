# 定时任务demo


from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
from multiprocessing import Process, Queue


# 这个提示虽然可以用，但不够好用, 还会消失..
def mac_time():
    cur_format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    time_title = "报警时间"
    content = cur_format_time

    # display notification "Lorem ipsum dolor sit amet" with title "Title"
    cmd = 'display notification  \"' + content + '\" with title \"' + time_title + '\"'
    print(cmd)
    call(["osascript", "-e", cmd])


# 看得出background_scheduler 自己维护循环，虽然够用，但不是那么好,总感觉有点奇怪, 但是这个也许可以写在 单独的进程里，就不干扰我做事了
def run_background_scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(mac_time, 'interval', minutes=15, start_date='2020-07-19 18:15:00', end_date='2020-07-19 21:00:00')
    scheduler.add_job(mac_time, 'interval', minutes=2)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


if __name__ == "__main__":
    process = Process(target=run_background_scheduler())
    process.start()
