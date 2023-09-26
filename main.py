# %%
import utils
from config import username, password
import requests
import random
import re
import time


ss = utils.login(username, password)

# %%
main_resp = ss.get('http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=list')

access_urls = re.findall('setAction=viewAssess&sid=(.*?)&lid=(.*?)&templateFlag=0',
            main_resp.text)
for i, (sid, lid) in enumerate(access_urls):
    access_urls[i] = f'http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=viewAssess&sid={sid}&lid={lid}&templateFlag=0'
    print(access_urls[i])
    

# %%
# url = access_urls[0]  # test, use the fist
for url in access_urls:

    # %%
    resp = ss.get(url)
    resp.encoding = resp.apparent_encoding
    # html = etree.HTML(resp.text)
    # form = html.xpath('//*[@id="answerForm"]')[0]

    # %%
    # assess_id = form.xpath('input/@value')[0]
    # print(assess_id)

    # %%
    assess_id = re.findall('<input name="assess_id" type="hidden" value="(.*?)"', resp.text)[0]
    # print(assess_id)

    # %%
    scores = '_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0__'
    percents = '_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0'
    # 常量
    # templateFlag = '0'
    # keyword = 'null'
    # teacherId = ''
    # setAction = 'answerStudent'

    # %%
    problem_ids = re.findall('<input name="problem_id" type="hidden" value="(.*?)" perc=', resp.text)
    # for problem_id in problem_ids:
        # print(problem_id)

    # %%
    answer_values = []
    for problem_id in problem_ids[:-2]:
        answer_value = re.findall(f'<input type="radio" name="problem{problem_id}" value="(.*?)" score="5.0"', resp.text)[0]
        answer_values.append(answer_value)
        # print(answer_value)

    # %%
    answer_values.append('老师讲课条理清晰')  # 17题问题：你认为该课程哪个方面你最满意？
    answer_values.append('无')  # 18题问题：你认为该课程哪个方面最需要改进？

    # %%
    answer = '_' + '_'.join(answer_values)
    id = '_' + '_'.join(problem_ids)

    # %%
    log_id = re.findall('<input type="hidden" name="logId" value="(.*?)"', resp.text)[0]
    # print(log_id)

    # %%
    form = {
        'answer': answer,
        'scores': scores,
        'percents': percents,
        'assess_id': assess_id,
        'templateFlag': '0',
        't': random.random(),
        'keyword': 'null',
        'id': id,
        'teacherId': '',
        'logId': log_id,
        'setAction': 'answerStudent'
    }
    # for i in form.items():
    #     print(i)

    # %%
    time.sleep(61)  # 少于1分钟后端报错，提交失败（操你妈逼还防脚本是吧他妈的）
    ss.headers.update({'Referer': resp.url})
    res = ss.post(url='http://jwc.swjtu.edu.cn/vatuu/AssessAction',
            data=form)

    # %%
    # print(res.text)
    if '操作成功' in res.text:
        print('评价成功')
        continue

    print(f'评价失败：{res.url}')
    print(res.text)

# %%



