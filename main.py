import requests
import base64
import random
import hashlib
import tkinter
import pyautogui
import io
import tkinter.messagebox
import configparser
import time
from pynput import mouse
import _thread

APPID = ''
PAS = ''
ACCESS_TOKEN = ''
SELECT_LEFT_POINT = False
SELECT_RIGHT_POINT = False
POINT = []
KEY = ''


def get_test_from_pic(pic_binary, ACCESS_TOKEN):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    img = base64.b64encode(pic_binary)
    params = {"image": img, 'language_type': 'JAP', 'detect_language': 'true'}
    access_token = ACCESS_TOKEN
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    text = ''
    if response:
        # print(response.json())
        js = response.json()['words_result']
        for x in js:
            text = text + ' ' + x['words']
    return text


def translate(text, APPID, PAS):
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    salt = str(random.randint(32768, 65536))
    params = {'q': text,
              'from': 'jp',
              'to': 'zh',
              'appid': APPID,
              'salt': salt,
              'sign': hashlib.md5((APPID + text + salt + PAS).encode()).hexdigest()
              }
    res = requests.post(url, data=params, headers=headers)
    test = ''
    if res:
        # print(res.json())
        test = res.json()['trans_result'][0]['dst']
    return test


def solve():
    global text_frame
    global POINT
    # print(POINT)
    LW, LH, RW, RH = tuple(POINT)
    # print(datetime.datetime.now())

    img = pyautogui.screenshot(region=(LW, LH, RW - LW, RH - LH))
    tmp = io.BytesIO()
    img.save(tmp, format='png')
    # img.save('2333.png')
    img = tmp.getvalue()
    # print(img)
    # print(datetime.datetime.now())

    pstr = get_test_from_pic(img, ACCESS_TOKEN)
    if pstr == '':
        return 
    # print(datetime.datetime.now())
    enstr = translate(pstr, APPID, PAS)
    # print(datetime.datetime.now())

    text_frame.config(state=tkinter.NORMAL)
    text_frame.delete(0.0, tkinter.END)
    text_frame.insert(tkinter.END, pstr)
    text_frame.insert(tkinter.END, '\n\n')
    text_frame.insert(tkinter.END, enstr)
    text_frame.config(state=tkinter.DISABLED)
    pass


def get_key_info(event):
    global POINT
    global SELECT_LEFT_POINT
    global SELECT_RIGHT_POINT
    global cfp

    # print(event, event.keysym)
    if SELECT_RIGHT_POINT:
        POINT[2], POINT[3] = event.x_root, event.y_root
        SELECT_RIGHT_POINT = False
        tkinter.messagebox.showinfo('右下角定位成功', 'x %d, y %d' % (event.x_root, event.y_root))
        cfp.set('sgt', 'BX', str(event.x_root))
        cfp.set('sgt', 'BY', str(event.y_root))
    elif SELECT_LEFT_POINT:
        POINT[0], POINT[1] = event.x_root, event.y_root
        SELECT_LEFT_POINT = False
        tkinter.messagebox.showinfo('左上角定位成功', 'x %d, y %d' % (event.x_root, event.y_root))
        cfp.set('sgt', 'AX', str(event.x_root))
        cfp.set('sgt', 'AY', str(event.y_root))
    cfp.write(open('sgt.ini', 'w'))


def select_left_point():
    global SELECT_LEFT_POINT
    global SELECT_RIGHT_POINT

    SELECT_RIGHT_POINT = False
    if SELECT_LEFT_POINT:
        tkinter.messagebox.showinfo('提示', '左上角定位终止')
        SELECT_LEFT_POINT = False
    else:
        tkinter.messagebox.showinfo('提示', '开始左上角定位，请将鼠标移至左上角按下Ctrl+C')
        SELECT_LEFT_POINT = True


def select_right_point():
    global SELECT_LEFT_POINT
    global SELECT_RIGHT_POINT

    SELECT_LEFT_POINT = False
    if SELECT_RIGHT_POINT:
        tkinter.messagebox.showinfo('提示', '右下角定位终止')
        SELECT_RIGHT_POINT = False
    else:
        tkinter.messagebox.showinfo('提示', '开始右下角定位，请将鼠标移至左上角按下Ctrl+C')
        SELECT_RIGHT_POINT = True


CHANGE_FLAG = False

def delay_solve(delay):
    time.sleep(delay)
    solve()

def on_scroll(x, y, dx, dy):
    global WHEEL_FLAG
    if dy < 0 and WHEEL_FLAG == 1:
        _thread.start_new_thread(delay_solve,(0.2,))


def new_thread():
    while True:
        with mouse.Listener(on_scroll=on_scroll) as listener:
            listener.join()


def translate_key(event):
    global KEY
    global CHANGE_FLAG
    global text_frame
    global cfp
    if CHANGE_FLAG:
        KEY = str(event.char)
        tkinter.messagebox.showinfo('提示', '翻译快捷键设置为' + str(KEY))
        cfp.set('sgt', 'KEY', KEY)
        CHANGE_FLAG = False
        cfp.write(open('sgt.ini', 'w'))
    elif event.char == str(KEY):
        _thread.start_new_thread(delay_solve,(0.5,))


def translate_key_changed():
    global CHANGE_FLAG
    tkinter.messagebox.showinfo('提示', '按下要设置的快捷键')
    CHANGE_FLAG = True


WHEEL_FLAG = 0


def wheel_switch():
    global WHEEL_FLAG
    global cfp
    if WHEEL_FLAG == 1:
        tkinter.messagebox.showinfo('提示', '已关闭滚轮翻译')
        WHEEL_FLAG = 0
    else:
        tkinter.messagebox.showinfo('提示', '已开启滚轮翻译')
        WHEEL_FLAG = 1
    cfp.set('sgt', 'wheel', str(WHEEL_FLAG))
    cfp.write(open('sgt.ini', 'w'))

def no_delay_solve():
    _thread.start_new_thread(delay_solve,(0,))

if __name__ == '__main__':
    # load config
    cfp = configparser.ConfigParser()
    cfp.read('sgt.ini')
    APPID = cfp.get('sgt', 'APPID')
    PAS = cfp.get('sgt', 'PAS')
    ACCESS_TOKEN = cfp.get('sgt', 'ACCESS_TOKEN')
    WIDTH = cfp.get('sgt', 'WIDTH')
    HEIGHT = cfp.get('sgt', 'HEIGHT')
    KEY = cfp.get('sgt', 'KEY')
    POINT = [int(cfp.get('sgt', 'AX')), int(cfp.get('sgt', 'AY')), int(cfp.get('sgt', 'BX')), int(cfp.get('sgt', 'BY'))]
    WHEEL_FLAG = int(cfp.get('sgt', 'wheel'))

    _thread.start_new_thread(new_thread, ())

    # build frame
    frame = tkinter.Tk()
    frame.geometry('%dx%d' % (int(WIDTH), int(HEIGHT)))

    text_frame = tkinter.Text(frame)
    b = tkinter.Button(frame, text='翻译', command=no_delay_solve)
    select_left_point_button = tkinter.Button(frame, text='左上角定位', command=select_left_point)
    select_right_point_button = tkinter.Button(frame, text='右下角定位', command=select_right_point)
    select_key = tkinter.Button(frame, text='调整翻译快捷键', command=translate_key_changed)
    select_wheel = tkinter.Button(frame, text='滚轮翻译', command=wheel_switch)
    text_frame.config(state=tkinter.DISABLED)
    select_left_point_button.pack()
    select_right_point_button.pack()
    select_key.pack()
    select_wheel.pack()
    text_frame.pack()
    b.pack()
    frame.title('Simple galgame translator')
    frame.bind('<Control-Key>', get_key_info)
    frame.bind('<Key>', translate_key)
    frame.mainloop()
