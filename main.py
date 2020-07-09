import requests
import base64
import random
import hashlib
import tkinter
import pyautogui
import io
import tkinter.messagebox
import configparser

APPID = ''
PAS = ''
ACCESS_TOKEN = ''
SELECT_LEFT_POINT = False
SELECT_RIGHT_POINT = False
POINT = [810, 1171, 1900, 1253]


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
              'from': 'auto',
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
    img = pyautogui.screenshot(region=(LW, LH, RW - LW, RH - LH))
    tmp = io.BytesIO()
    img.save(tmp, format='png')
    img.save('2333.png')
    img = tmp.getvalue()
    # print(img)
    pstr = get_test_from_pic(img, ACCESS_TOKEN)
    enstr = translate(pstr, APPID, PAS)
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

    # print(event, event.keysym)
    if SELECT_RIGHT_POINT:
        POINT[2], POINT[3] = event.x_root, event.y_root
        SELECT_RIGHT_POINT = False
        tkinter.messagebox.showinfo('右下角定位成功', 'x %d, y %d' % (event.x_root, event.y_root))
        pass
    elif SELECT_LEFT_POINT:
        POINT[0], POINT[1] = event.x_root, event.y_root
        SELECT_LEFT_POINT = False
        tkinter.messagebox.showinfo('左上角定位成功', 'x %d, y %d' % (event.x_root, event.y_root))
        pass


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


def translate_key(event):
    # print(event)
    if event.char == 't':
        solve()


if __name__ == '__main__':
    # load config
    cfp = configparser.ConfigParser()
    cfp.read('sgt.ini')
    APPID = cfp.get('sgt', 'APPID')
    PAS = cfp.get('sgt', 'PAS')
    ACCESS_TOKEN = cfp.get('sgt', 'ACCESS_TOKEN')
    WIDTH = cfp.get('sgt', 'WIDTH')
    HEIGHT = cfp.get('sgt', 'HEIGHT')
    # build frame
    frame = tkinter.Tk()
    frame.geometry('%dx%d' % (int(WIDTH), int(HEIGHT)))
    text_frame = tkinter.Text(frame)
    b = tkinter.Button(frame, text='翻译', command=solve)
    select_left_point_button = tkinter.Button(frame, text='左上角定位', command=select_left_point)
    select_right_point_button = tkinter.Button(frame, text='右下角定位', command=select_right_point)
    text_frame.config(state=tkinter.DISABLED)
    select_left_point_button.pack()
    select_right_point_button.pack()
    text_frame.pack()
    b.pack()
    frame.title('Simple galgame translator')
    frame.bind('<Control-Key>', get_key_info)
    frame.bind('<Key>', translate_key)
    frame.mainloop()
