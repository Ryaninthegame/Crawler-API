import time
import requests
import urllib.request as req
import bs4 
from dateutil.parser import parse

def getRequest(url):
    request = req.Request(url, headers={
        "cookie":"over18=1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    })
    while(1):
        try:
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")
            break
        except:
            print("-----------------------------sleep")
            time.sleep(10)
    return data

def imageRequest(url, stream):
    while(1):
        try:
            r = requests.get(url, stream=stream)
            break
        except:
            print("-----------------------------sleep")
            time.sleep(10)
    return r

def getSoup(url):
    data = getRequest(url)
    soup = bs4.BeautifulSoup(data, "html.parser")
    return soup

def getNextPage(soup):
    nextPage = soup.find_all('div', class_='btn-group')
    nextPage = nextPage[1].find_all('a', class_='btn wide')
    nextPage = nextPage[1].get('href')
    return r"https://www.ptt.cc/"+nextPage

def getInformation(article):
    date = article.find('div', class_='meta')
    date = date.find('div', class_='date')
    bomb = article.find('div', class_='nrec')
    mark = article.find('div', class_='meta')
    mark = mark.find('div', class_='mark')
    link = article.find('div', class_='title')
    try:
        link = r"https://www.ptt.cc/"+link.find('a').get('href')
    except:
        link = ""
    return date.text, getIntBomb(bomb.text), mark.text, link

def filter(date, bomb, bombLimit, mark, link, dateBegin, dateEnd):
    date = parse(date)
    if parse(dateBegin)<=date<=parse(dateEnd):
        if int(bomb)>bombLimit:
            if mark=="" and link !="":
                return True
    return False

def getIntBomb(bomb):
    try:
        if bomb=="爆":
            return 100
        return int(bomb)
    except:
        return 0

def getTitle(soup):
    title = soup.find_all('span', class_="article-meta-value")
    return title[2].text

def judgeDate(date, dateBegin, index):
    if index>1 and parse(date)<parse(dateBegin):
        return True
    return False

def getCandidate(dateBegin, dateEnd, bombLimit):
    index, candidate = 0, []
    url = r'https://www.ptt.cc/bbs/Beauty/index.html'
    while(1):
        index+=1
        soup = getSoup(url)
        articleSet = soup.find_all('div', class_='r-ent')
        for article in articleSet:
            date, bomb, mark, link = getInformation(article)
            if(filter(date, bomb, bombLimit, mark, link, dateBegin, dateEnd)):
                candidate.append(link)
        if judgeDate(date, dateBegin, index):
            break
        url = getNextPage(soup)
    return candidate

def getImageLink(soup):
    imageSet = []
    imageLink = soup.find('div', class_="bbs-screen bbs-content")
    imageLink = imageLink.find_all('a')
    for image in imageLink:
        image = image.text
        if 'imgur' in image:
            imageSet.append(image)
    imageLinkInPush = soup.find_all('div', class_="push")
    for image in imageLinkInPush:
        image = image.find('a')
        try:
            image = image.text
            imageSet.remove(image)
        except:
            pass
    return imageSet

def getImagePerArticle(candidate):
    dic = {}
    for url in candidate:
        soup = getSoup(url)
        title = getTitle(soup)
        imageSet = getImageLink(soup)
        dic[title] = imageSet
    return dic

def main(dateBegin, dateEnd, bombLimit):
    dic = {}
    try:
        candidate = getCandidate(dateBegin, dateEnd, bombLimit)
        content = getImagePerArticle(candidate)
        dic['state'] = 'success'
        dic['content'] = content
    except:
        dic['state'] = 'fail'
    return dic
