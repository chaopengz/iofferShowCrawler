# coding:utf-8
import re
import urllib
import urllib2
import json
from urllib import urlencode
import requests
from requests.exceptions import ConnectionError
import time


def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    html = urllib2.urlopen(request, timeout=50).read()
    return html


def get_item(pattern, content):
    try:
        result = re.compile(pattern, re.S).findall(content)[0]
    except Exception:
        result = ""
    return result.replace(',', ' ').replace('，', ' ').replace('\n', '')


def get_results(html):
    result = []
    match_str = r'div class="ui-block-b"><p align="center" data-theme="a">(.*?)</div>'
    patten_url = re.compile(match_str, re.S)
    contents = patten_url.findall(html)

    if len(contents) != 8:
        return result
    pattern_1 = r'<a.*?>(.*?)<'
    pattern_2 = r'(.*?)<'

    kind = get_item(pattern_1, contents[0])
    name = get_item(pattern_1, contents[1])
    job = get_item(pattern_1, contents[2])
    place = get_item(pattern_1, contents[3])
    salary = get_item(pattern_2, contents[4])
    credit = get_item(pattern_1, contents[5])
    time = get_item(pattern_2, contents[6])
    note = get_item(pattern_2, contents[7])

    result.append(kind)
    result.append(name)
    result.append(job)
    result.append(place)
    result.append(salary)
    result.append(credit)
    result.append(time)
    result.append(note)

    return result


def get_w_str(offer_id):
    baseurl = 'https://www.ioffershow.com/offerdetail/'
    url = baseurl + offer_id
    html = get_html(url)
    result = get_results(html)
    w_str = ",".join(result)
    return w_str


if __name__ == '__main__':
    fw = open('./ioffershow.txt', 'w')
    ids = range(1, 4280)
    for offer_id in ids:
        w_str = get_w_str(str(offer_id))
        if w_str == "":
            continue
        w_str = str(offer_id) + ',' + w_str + '\n'
        print(w_str)
        fw.write(w_str)
        time.sleep(1)
    fw.close()
