import requests
import urllib
import json
# 百度Al情感倾向分析
def sentiment_classify(text):
    """
    获取文本的感情偏向（消极 or 积极 or 中立）
    参数：
    text:str 本文
    """
    # 读config.ini文件
    # dir_now = os.path.dirname(__file__)
    # conf = configparser.ConfigParser()
    # conf.read(dir_now + '/config.ini')
    raw = {"text": "内容"}
    raw['text'] = text
    data = json.dumps(raw).encode('utf-8')
    # AT = conf.get('baidu', 'AT')
    # host = conf.get('baidu', 'host') + AT
    AT = "24.b21366821456eacb43fd4fde910579f6.2592000.1558952204.282335-15834712"
    host = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + AT
    request = urllib.request.Request(url=host, data=data)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    rdata = json.loads(content)
    # print("百度Al返回" + str(rdata))
    return rdata