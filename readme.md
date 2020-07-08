### 简单的orc+翻译功能
帮助阅读galgame生肉(
#### 一些api
* “百度智能云”的“文字识别”中的“通用文字识别” https://cloud.baidu.com/doc/OCR/s/Mk3h7ycqx
* “百度翻译开放平台”的“通用翻译”https://api.fanyi.baidu.com/product/11

#### 使用指南
1. 填全main.py中的APPID, PAS, ACCESS_TOKEN, 分别为两个api中的参数
2. 调整solve方法中的LW, LH, RW, RH, 以标明截图区域，再下个版本中应该会添加手动选择区域的方法(bu hui gu bu hui gu)

#### 简单演示
![pic/1.png](pic//1.jpg)
![pic/1.png](pic//2.jpg)
