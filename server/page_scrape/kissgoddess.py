
import coloredlogs
import csv
import time
import random
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from page_scrape.models import Post
import requests
import logging

originUrl = 'https://kissgoddess.com'
galleryUrl = 'https://kissgoddess.com/gallery/'
source = 'kissgoddess'

coloredlogs.install()
logging.info("It works!")


def scrapeEachPost(url, thumbnail):
    postFoundInDB = Post.objects(url=url, source=source)
    if ~(len(postFoundInDB) == 0):
        print('Scrape url:', url)

        time.sleep(2)
        html = BeautifulSoup(requests.get(
            url, verify=False).text, 'html.parser')
        title = html.find("img", {"id": "bigImg"}).get('alt')

        firstImageUrl = html.find("img", {"id": "bigImg"}).get(
            'src').replace('//', 'https://')
        imageUrl = firstImageUrl.split('/000.')
        print('First image url:', imageUrl)
        bot = 0
        top = 100
        while ((top-bot) > 1):
            num = int((top+bot)/2)
            numStr = ('0000' + str(num))[-3:]

            indexUrl = imageUrl[0]+'/'+numStr+'.'+imageUrl[1]
            print(indexUrl)
            if (requests.get(indexUrl).status_code == 200):
                bot = num
                print('num', num)
            else:
                top = num


def scrapeListofAlbum():
    html = BeautifulSoup(requests.get(
        galleryUrl, verify=False).text, 'html.parser')
    postListHtml = html.find(class_='td-related-row')
    # logging.info(postListHtml)

    for postHtml in postListHtml:
        # logging.info(postHtml)

        if isinstance(postHtml.find('a'), Tag):
            postUrl = originUrl + postHtml.find('a').get('href')
            print(postUrl)
            # thumbnail = postHtml.find('a').find('img').get('src').replace('//','https://')

        # if postUrl:
        #     scrapeEachPost(postUrl,thumbnail)


scrapeListofAlbum()
