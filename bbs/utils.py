import time

def log(*args, **kwargs):
    format = "%H/%M/%S"
    value = time.localtime(int(time.time()))
    dt = time.strftime(format,value)
    with open('log.txt','a',encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

accept_file_type = ['jpg', 'gif', 'png']
user_img_director =r'user_img'