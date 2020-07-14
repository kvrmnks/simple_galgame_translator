### 简单的orc+翻译功能
旨在帮助不懂日语并且打不开vnr的孩子们阅读galgame生肉(
#### 一些api
* “百度智能云”的“文字识别”中的“通用文字识别” https://cloud.baidu.com/doc/OCR/s/Mk3h7ycqx
* “百度翻译开放平台”的“通用翻译”https://api.fanyi.baidu.com/product/11

#### 使用指南
1. 填全sgt.ini中的APPID, PAS, ACCESS_TOKEN, 分别为两个api中的参数
2. 可以按按钮选择左上角与右下角来定位要翻译的区域
3. 可以按t来进行翻译，但要保持这个程序的焦点，于是只能用滑轮来翻galgame的页了，~~或许以后会改吧~~ 改了改了可以改快捷键了


#### 需要另外安装的模块的支持
1. request 用来调用api
2. tkinter GUI
3. pyautogui 截图处理
4. pynput 对鼠标动作的监听

#### 演示
咕了咕了

#### 更新日志

* 2020-7-14 加入切换翻译快捷键, 加入ocr区域以及相关设置的离线存储, 加入翻页自动翻页功能