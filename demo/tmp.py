from datetime import date, time

time_num = '19:30:02'

time_num_tmp=time_num.zfill(8)

print(str(time_num_tmp))


my_time = time.fromisoformat('09:30:02')
my_time2 = time.fromisoformat('10:30:01')

if my_time > my_time2:
    print('true')
else:
    print('false')
