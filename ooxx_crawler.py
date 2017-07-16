import urllib.request as url_request
import urllib.parse as url_parse
import urllib.robotparser as robotparser
from bs4 import BeautifulSoup

import sqlite3

import time
import random
import os
import re

'''
    Note(TODO):
        1. load last access page num, then continue crawl
        2. write to sqlite3 db
            1.file_name : unique key
            2.publish_time
            3.author
            4.oo_num
            5.xx_num
            6.tucao_num
            7.pic_text
            8.[comments key words of this pic] 
            9.[text_info_in_this_pic]
        3. if page(cur_page_num) == page(cur_page_num + 1) : no new pages
        
        
'''
def get_links(html):
    """ return a list of links from html
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def download(url, user_agent='wswp', num_retries=2):
    print('Downloading:{}'.format(url))
    headers = {'User-agent': user_agent if user_agent else 'wsap'}
    request = url_request.Request(url, headers=headers)
    try:
        html = url_request.urlopen(request).read()
    except url_request.HTTPError as e:
        print('Download error:{}'.format(e.reason))
        html = None
        if hasattr(e, 'code') and 500 <= e.code <= 600:
            return download(url, user_agent, num_retries - 1)

    return html

def ooxx_crawler(seed_url, robots_parser=None, user_agent='wsap'):
    """
    :param seed_url: crawl from the seed_url, following links
    :param link_regex: matched by link_regex 
    :return: list of urls
    """
    cur_page_url = seed_url
    pic_seen = set()

    # 1. download the page html
    # 2. extract pic url of this page
    # 3. download the pics
    # 4. goto next page
    random.seed(time.time())

    if not os.path.exists('./ooxx/'):
        os.mkdir('./ooxx/')
        print('Hell I create a new dir with python...')
    while cur_page_url != None:
        html = download(cur_page_url, user_agent)
        soup = BeautifulSoup(html, 'html.parser')
        #img_urls = soup.find_all('img', {'src': re.compile(r'.*sinaimg.*')})
        img_urls = soup.find_all('a', text='[查看原图]')

        for img_url in img_urls:
            cur_url = url_parse.urljoin('http://', img_url['href'])
            img_name = cur_url.split('/')[-1]
            img = download(cur_url)

            with open('./ooxx/' + img_name, 'wb') as img_file:
                img_file.write(img)

            time.sleep(random.randrange(2, 5))

        #get the next page url
        cur_page_url = None


if __name__ == '__main__':
    ooxx_crawler(r'http://jandan.net/ooxx')






