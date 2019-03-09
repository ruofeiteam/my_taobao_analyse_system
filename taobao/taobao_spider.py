import re
import requests
import json


# from Model.models import Spider
# from django.shortcuts import render

# rate.taobao.com/detailCommon.htm?auctionNumId=584067666712  总体评价
def Comment_Spider(taobao_id):
    parmar = {'auctionNumId': taobao_id}
    taobao_detailCommon_url = r"https://rate.taobao.com/detailCommon.htm"
    r = requests.get(taobao_detailCommon_url, params=parmar)

    spider_detail_common = r.text
    r.close()

    return (spider_detail_common)


# rate.taobao.com/feedRateList.htm?auctionNumId=584067666712&currentPageNum=180&pageSize=100 每个评论
def One_Page_Spider(taobao_id, page_num, page_size="1000"):
    parmar = {'auctionNumId': taobao_id, 'currentPageNum': page_num, 'pageSize': page_size}
    cookies = dict(
        x5sec='7b22726174656d616e616765723b32223a223631306230393455676639663036366363623562316139383134753963616132434e61436a755146454a47642b4c65373937717a5767453d227d')
    taobao_one_page_url = r"https://rate.taobao.com/feedRateList.htm"
    r = requests.get(taobao_one_page_url, params=parmar, cookies=cookies)

    spider_one_page_common = r.text
    r.close()

    return (spider_one_page_common)


def All_Spider(taobao_id):
    detail_comment = Comment_Spider(taobao_id)

    list_content = []

    for page_num in range(1,200):
        content = One_Page_Spider(taobao_id, page_num)
        all_content = re.findall(r"\]\,\"content\"\:\"(.+?)\"", content)
        for one_content in all_content:
            list_content.append(one_content)


    # print(json.dumps(list_content, ensure_ascii=False))
    # print(len(list_content))

    #存入spider数据库  #明日计划/增加线程池/增加数据库表（类似CMD5，读入id存在直接返回，不存在加入线程池加入数据库，等下次使用或邮件告知）
    return ("spider is done")


All_Spider("575384751046")