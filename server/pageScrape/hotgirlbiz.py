
import coloredlogs
import csv
import uuid
import os
import time
import random
import json
import imghdr
from PIL import Image
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from pageScrape.models import Album, ModelInfo
import requests
import logging
import mongoengine
import pageScrape
from slugify import slugify
from sexybaby.commons import dataLogging, downloadAndSaveToS3, deleteTempPath, getLongId, getShortId, debug
from sexybaby.aws import deleteAwsS3Dir, uploadToAws
import logging
logger = logging.getLogger(__name__)

originUrl = 'https://hotgirl.biz'
source = 'hotgirlbiz'

coloredlogs.install()


def albumScrapeListofAlbum(pageUrl):
    """Scrape the gallery page and return list of album
    Args:
        pageUrl: Url of the pages contain all album.
    Returns:
        List of album obj
    """

    html = BeautifulSoup(requests.get(
        pageUrl,
        verify=True
    ).text, 'html.parser')

    albumLiHtml = html.find_all(class_='latestPost')

    albumLi = []
    for albumHtml in albumLiHtml:

        albumUrl = albumHtml.find('a').get('href')
        imageUrl = albumHtml.find_all(
            class_='featured-thumbnail')[0].find('img').get('data-lazy-src')

        if (albumUrl and imageUrl):
            album = {
                'albumSourceUrl': albumUrl,
                'albumThumbnail': {
                    'imgSourceUrl': imageUrl
                }
            }

            albumLi.append(album)

    return albumLi


def albumScrapeAllImageInAlbum(album):
    """Scrape all images in album and return list of image object
    Args:
        url(str): url of album

    Returns:
        Object of image contain title and images scraped
    """
    albumInDB = Album.objects(
        albumSourceUrl=album['albumSourceUrl'], albumSource=source)

    if not (len(albumInDB) == 0):
        dataLogging(albumInDB[0], '')
        return

    debug('Scrape images in url: %s' % (album['albumSourceUrl']))

    html = BeautifulSoup(requests.get(
        album['albumSourceUrl'],
        verify=True).text, 'html.parser')

    album['albumSource'] = source

    album['albumDisplayTitle'] = html.find(
        class_='single_post').find(class_='single-title').contents[0]

    album['albumTitle'] = slugify(
        album['albumDisplayTitle'], to_lower=True)

    album['albumSourceCreatedDate'] = html.find(
        class_='single_post').find(class_='thetime').find('span').contents[0]
    print(album['albumSourceCreatedDate'])
    album['albumTags'] = []
    tagsHtml = html.find(
        class_='single_post').find(class_='tags').find_all('a')
    for tagHtml in tagsHtml:
        album['albumTags'].append(tagHtml.contents[0])

    album['albumCategories'] = []
    categoriesText = html.find(
        class_='single_post').find(class_='thecategory').contents[0]
    album['albumCategories'] = (categoriesText.split(','))

    album['albumId'] = getLongId()

    thumbnailImageUrl = album['albumThumbnail']['imgSourceUrl']
    imgPath = 'album/' + album['albumId']
    imgExtension = thumbnailImageUrl.split(
        '.')[len(thumbnailImageUrl.split('.')) - 1]
    imgFile = getShortId() + '.' + imgExtension
    imgTempFilePath = '/tmp/' + imgPath + '/' + imgFile

    uploaded = downloadAndSaveToS3(
        thumbnailImageUrl, imgPath, imgFile)

    imgOpened = Image.open(imgTempFilePath)

    if uploaded:
        imgObj = {}
        imgObj['imgNo'] = '001'
        imgObj['imgWidth'] = imgOpened.size[0]
        imgObj['imgHeight'] = imgOpened.size[1]
        imgObj['imgSize'] = os.path.getsize(imgTempFilePath)
        imgObj['imgType'] = imghdr.what(imgTempFilePath)
        imgObj['imgSourceUrl'] = thumbnailImageUrl
        imgObj['imgStorePath'] = imgPath + '/' + imgFile
        imgObj['imgExtension'] = imgExtension
        album['albumThumbnail'] = imgObj

    album['albumImages'] = []
    imagesHtml = html.find(
        class_='post-single-content').find(class_='thecontent').find('p').find_all('a')
    for imageHtml in imagesHtml:
        imgUrl = imageHtml.get('href')
        if (imgUrl):
            imgPath = 'album/' + album['albumId']
            imgExtension = imgUrl.split('.')[len(imgUrl.split('.')) - 1]
            imgFile = getShortId() + '.' + imgExtension
            imgTempFilePath = '/tmp/' + imgPath + '/' + imgFile

            uploaded = downloadAndSaveToS3(
                imgUrl, imgPath, imgFile)

            imgOpened = Image.open(imgTempFilePath)

            if uploaded:
                imgObj = {}
                imgObj['imgNo'] = format(len(album['albumImages']) + 1, '03d')
                imgObj['imgWidth'] = imgOpened.size[0]
                imgObj['imgHeight'] = imgOpened.size[1]
                imgObj['imgSize'] = os.path.getsize(imgTempFilePath)
                imgObj['imgType'] = imghdr.what(imgTempFilePath)
                imgObj['imgSourceUrl'] = imgUrl
                imgObj['imgStorePath'] = imgPath + '/' + imgFile
                imgObj['imgExtension'] = imgExtension
                album['albumImages'].append(imgObj)

    deleteTempPath('album/' + album['albumId'])

    print(album)

    try:
        Album(**album).save()

    except:
        logger.error('Cannot save to DB:' + album['albumSourceUrl'])
        debug('Delete album ' + album['albumId'])
        deleteAwsS3Dir('album/' + album['albumId'])


def scrapeEachPage():
    pageUrl = originUrl + '/page/1'
    albumObjLi = albumScrapeListofAlbum(pageUrl)
    print(albumObjLi)
    for album in albumObjLi:
        if (album['albumSourceUrl'] != 'https://hotgirl.biz/huayang-vol-279-yue-er-yue/'):
            continue

        albumScrapeAllImageInAlbum(album)


def main():
    logging.info('Start to scrape: %s' % (source))
    album = {
        'albumSourceUrl': 'https://hotgirl.biz/youmei-vol-414-baby-sitters-honey/',
        'albumThumbnail': {
            'imgSourceUrl': 'https://hotgirl.biz/wp-content/uploads/2020/11/0-09142032.jpg'
        }
    }
    # albumScrapeAllImageInAlbum(album)

    scrapeEachPage()
