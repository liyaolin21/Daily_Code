import requests
import re
import os
from lxml import etree
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
 
 
def get_page(num):
    img_list = []
    for i in range((num // 35) + 1):
        url = f'http://mms1.baidu.com/it/u=2971161858,522100436&fm=253&app=120&f=JPEG&fmt=auto&q=75?w=660&h=372'
        r = requests.get(url, headers=headers)#刚才复制的链接地址
        html = r.text
        html = etree.HTML(html)
        conda_list = html.xpath('//a[@class="iusc"]/@m')   #conda_list是空的，存在问题
        for j in conda_list:
            pattern = re.compile(r'"murl":"(.*?)"')
            img_url = re.findall(pattern, j)[0]
            img_list.append(img_url)
    return img_list
 
 
def download(path, img_list):
    for i in range(len(img_list)):
        img_url = img_list[i]
        idx = i+1
        idx = str(idx)
        page_idx = idx.zfill(4)
        print(f'正在爬取: {img_url}')
        img_floder = path + keyword  #爬取图片存放的位置并命名
        if not os.path.exists(img_floder):
            os.makedirs(img_floder)
        try:
            with open(f'{img_floder}/{page_idx}.jpg', 'wb') as f:
                img_content = requests.get(img_url).content
                f.write(img_content)
        except:
            continue
 
if __name__ == '__main__':
    num = 500
    keyword = 'tank'        #文件名
    path = 'F:/Tank/oringinal/'   #存放位置
    img_list = get_page(num)
    download(path, img_list)