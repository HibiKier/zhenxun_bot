import requests
from util.user_agent import get_user_agent
from bs4 import BeautifulSoup
from time import sleep
import threading
import os
from configs.path_config import IMAGE_PATH

lock = threading.Lock()

url = "https://search.bilibili.com/article"
# path = IMAGE_PATH + "setu/"

index = 1
THREAD_SUM_REMAINDER = 2    # 越小线程越多


class bilibiliThread (threading.Thread):
    def __init__(self, threadId, url_list, path, nolist):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.url_list = url_list
        self.path = path
        self.nolist = nolist
    def run(self):
        print("开始线程<><><><><><><><><> " + self.threadId)
        thread_get_url(self.threadId, self.url_list, self.path, self.nolist)


def get_bilibili_img(name, path, nolist=None):
    global index
    index = get_dirfile_len(path)
    print("index===", index)
    threadId = 1
    params = {
        'keyword': name,
        'page': '1'
    }
    res = requests.get(url, headers=get_user_agent(), params=params)
    sleep(8)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.text)
    try:
        total_page = soup.find_all('button', {'class': 'pagination-btn'})[-1].text.strip()
        print("1 try")
    except:
        try:
            total_page = soup.find_all('button', {'class': 'pagination-btn num-btn'})[-1].text.strip()
            print("2 try")
        except:
            total_page = 1
            print("3 except")
    print(total_page)
    url_list = []
    for page in range(1, int(total_page)+1):
        url_r = "https://search.bilibili.com/article?keyword=" + name + "&page=" + str(page)
        url_list.append(url_r)
        if page % THREAD_SUM_REMAINDER == 0:
            print('-----> ' + str(page) + " =======>", url_list)
            # _thread.start_new_thread(thread_get_url, (url_list, path,))
            bilibiliThread(str(threadId), url_list, path, nolist).start()
            threadId += 1
            sleep(0.5)
            url_list = []
    if url_list:
        print("=========================最后一个线程启动========================= url数量: ", len(url_list))
        bilibiliThread(str(threadId), url_list, path, nolist).start()


def thread_get_url(threadId, url_list, path, nolist):
    for url in url_list:
        res = requests.get(url, headers=get_user_agent())
        sleep(2)
        soup = BeautifulSoup(res.text, 'lxml')
        alist = soup.find_all('a', {'class': 'poster'})
        img_content_page = []
        # print(alist)
        for a in alist:
            if nolist != None:
                if a.get('href') not in nolist:
                    img_content_page.append("https://" + a.get('href')[2:])
            else:
                img_content_page.append("https://" + a.get('href')[2:])
        pic_url = []
        for img_content in img_content_page:
            print("开始获取---------->", img_content)
            res = requests.get(img_content, headers=get_user_agent())
            sleep(2)
            soup = BeautifulSoup(res.text, 'lxml')
            figure_ls = soup.body.find_all('figure')
            # print(figure_ls)
            for figure in figure_ls:
                try:
                    _ = figure.img.attrs['class']
                except:
                    data_src = figure.img.attrs['data-src']
                    pic_url.append('https:' + data_src)
            print("线程 " + threadId + " 获取完毕------>  开始存储")
            for url in pic_url:
                print("线程 " + threadId + "正在存储---------------->", url)
                res = requests.get(url, headers=get_user_agent())
                save_img(res.content, path, threadId)
            pic_url = []
    print("线程 " + threadId + " ---------------->执行完毕")


def save_img(img, path, threadId):
    global index
    try:
        lock.acquire()
        img_index = index
    finally:
        lock.release()
    try:
        with open(path + str(img_index) + ".jpg", 'wb') as f:
            f.write(img)
        lock.acquire()
        index += 1
    except:
        print("线程 " + threadId + "存储失败-------->" + str(img_index) + ".jpg")
    finally:
        lock.release()


def get_dirfile_len(path):
    return len(os.listdir(path))


if __name__ == '__main__':
    # url = "https://search.bilibili.com" \
    #       "/article?keyword=%23%E4%BB%8A%E6%97%A5%E4%BB%BD%E7%9A%84%E5%8F%AF%E7%88%B1%" \
    #       "E5%B0%8F%E8%90%9D%E8%8E%89%EF%BC%8C%E8%BF%9B%E6%9D%A5%E7%9C%8B%E7%9C%8B%EF%BC%8C%E" \
    #       "6%8F%90%E7%A5%9E%E9%86%92%E8%84%91%EF%BC%81"
    # res = requests.get(url, headers=get_user_agent())
    # sleep(2)
    # soup = BeautifulSoup(res.text, 'lxml')
    # alist = soup.find_all('button', {'class': 'pagination-btn num-btn'})
    # total_page = soup.find_all('button', {'class': 'pagination-btn num-btn'})[-1].text.strip()
    # print(total_page)
    get_bilibili_img("精选动漫壁纸手机电脑壁纸&动漫游戏专题", IMAGE_PATH + "bizhi/")