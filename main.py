import requests
import base64
import random
import hashlib
import tkinter
import pyautogui
import io

APPID = ''
PAS = ''
ACCESS_TOKEN = ''


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
        print(response.json())
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
        print(res.json())
        test = res.json()['trans_result'][0]['dst']
    return test


def solve():
    global text_frame
    #text_frame.insert(tkinter.END, '2333')
    LW = 810
    LH = 1171
    RW = 1900
    RH = 1253
    img = pyautogui.screenshot(region=(LW, LH, RW - LW, RH - LH))
    tmp = io.BytesIO()
    img.save(tmp, format='png')
    img = tmp.getvalue()
    print(img)
    pstr = get_test_from_pic(img, ACCESS_TOKEN)
    enstr = translate(pstr, APPID, PAS)
    text_frame.delete(0.0, tkinter.END)
    text_frame.insert(tkinter.END, pstr)
    text_frame.insert(tkinter.END, '\n\n')
    text_frame.insert(tkinter.END, enstr)
    pass


# f = open('d://QQ截图20200708215349.jpg', 'rb')
# print(f.read())
'''

pstr = get_test_from_pic(f.read(), ACCESS_TOKEN)
enstr = translate(pstr, APPID, PAS)
print(pstr, enstr)
'''
frame = tkinter.Tk()
text_frame = tkinter.Text(frame)
text_frame.pack()
b = tkinter.Button(frame, text='翻译', command=solve)
b.pack()
frame.mainloop()
'''
app = wx.App(False)
s = wx.ScreenDC()
s.Pen = wx.Pen("#FF0000")
s.DrawLine(60,60,1200,1200)
'''
