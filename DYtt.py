import requests
import re
from bs4 import BeautifulSoup
import os


class Movie(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        re = requests.get(url)
        re.encoding = "gbk"
        sp = BeautifulSoup(re.text, 'html.parser')
        self.content = sp.find('div', attrs={'id': 'Zoom'})
        self.n = 1

    def get_img(self):
        img_t = self.content.find_all('img')
        img = []
        for each in img_t:
          img.append(each.get('src'))
        return img

    def get_info(self):
        info_sp = self.content.find('p')
        info = re.sub('◎', '\n◎', info_sp.text)
        return info

    def get_magnet(self):
        mg = self.content.find('a').get('href')
        return mg

    def FindDouBanpf(self):
        p = self.content.find('p')
        try:
            db = re.findall(re.compile(r'豆瓣评分\u3000\d.\d'), p.text)
            pf = re.findall(re.compile(r'\d.\d'), db[0])
            return (float(pf[0]))
        except:
            return 0.0


    def testexist(self, path):
        if os.path.exists(path):
            if self.n != 1:
                path = path[:-3]
            path = path + '(' + str(self.n) + ')'
            self.n += 1
            return self.testexist(path)
        else:
            return path


    def download(self):
        test = 'G:\\dyttDownload\\最新电影\\'+self.name
        path = self.testexist(test)
        os.makedirs(path)
        print('正在下载......'+self.name+'......')
        with open(path+'\\information.txt', 'w', encoding='utf-8') as file:
            file.write(self.get_info())
        with open(path + '\\magnet.txt', 'w', encoding='utf-8') as file:
            file.write(self.get_magnet())
        for k in self.get_img():
            re = requests.get(k)
            pa = path+'\\img1.jpg'
            if os.path.exists(pa):
                pa = path+'\\img2.jpg'
            with open(pa, 'wb') as file:
                file.write(re.content)
        with open(path+ '\\豆瓣评分：'+str(self.FindDouBanpf())+'.txt','w') as file:
            file.write('豆瓣评分：'+str(self.FindDouBanpf()))
        print('......下载完成......')


def GetMovie(sp):
    cont = sp.find('div', attrs={'class':'co_content8'})
    ul = cont.find('ul')
    movie = ul.find_all('a')
    name = []
    url = []
    for each in movie:
        try:
            name_p = re.search(re.compile(r"《.*》"), each.text).group(0)
            na = re.sub('/', 'or', name_p)
            name.append(na)
            url.append('http://dytt8.net' + each.get('href'))
        except AttributeError:
            pass
    return name, url


for j in range(50):
    url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_'+str(j+1)+'.html'
    r = requests.get(url)
    r.encoding = "gb2312"
    sp = BeautifulSoup(r.text, 'html.parser')
    print('......page'+str(j+1)+'开始下载......')
    try:
        name, url = GetMovie(sp)
        error_name = []
        error_url = []
        for i in range(len(name)):
            try:
                mo = Movie(name[i], url[i])
                mo.download()
            except:
                error_name.append(name[i])
                error_name.append(url[i])
                print(name[i] + '......下载失败！')
        print('......page' + str(j + 1) + '下载完成......')
    except:
        print('......page' + str(j + 1) + '下载失败......')
