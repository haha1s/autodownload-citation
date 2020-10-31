#!/usr/bin/env python
# coding: utf-8
#根据文献题目从百度学术下载格式化的引文
# usage:  python path/to/bdduxtuu.python  path/to/yourinputfile
import os
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import sys
import re
#os.chdir(r'C:\Users\Acer\Desktop\lalal')

inputfile = sys.argv[1]
bx = webdriver.Chrome()
bx.implicitly_wait(3)
bx.get('https://xueshu.baidu.com/')
bx.maximize_window()
#登陆检查

try:
    bx.find_element_by_id('lb').click()
except:
    print("已经登录")
else:
    print("正在登录......")
while True:
    try:
        xbxi = bx.find_element_by_id('imsg')
       
    except:
        time.sleep(3)
    else:
        print("登陆成功")
        break
        
#得到作者信息 多结果页面 与下载到得引用文章手动看一下是否相同
def get_zv1():
    sc_info = bx.find_element_by_xpath("(//div[@class='sc_info'])[1]").text
    zove = re.sub("[\s,(...))]","",sc_info)
    title = bx.find_element_by_xpath('//div[@id="1"]//h3/a').text
    print(zove + "-" + title)

#得到作者信息 单独页面
def get_zv2():
    zove = bx.find_element_by_xpath('//p[@class="author_text"]').text
    title = bx.find_element_by_xpath('//div[@class="main-info"]//h3/a').text
    year = bx.find_element_by_xpath('//div[@class="year_wr"]/p[2]').text
    print(zove + "-"+ title + "-" + year)

#dowdload
def downwx():
    bx.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]').click() #点击引用数量
    time.sleep(5) #wait umtil contens appear
    ac = ActionChains(bx)
    ac.move_to_element(bx.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[1]')).perform() #move to 导出至
    time.sleep(1)     #等待选项出现，
    bx.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/ul/li[4]/a').click() #点击下载得格式
    bx.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/a[1]').click() #清空列表
    bx.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/i').click() #close this window


with open(inputfile,'r') as cjwx:
    ck = cjwx.readlines()

num = 0
for line in ck:
    bx.find_element_by_id('kw').clear()
    bx.find_element_by_id('kw').send_keys(line)
    while True:
        try:
            uull = bx.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/span').get_attribute('innerHTML')
        except:
            break
        else:
            if int(uull) == 30:#单次最大批量引用数30个
                downwx()
            break

    while True:
        try:
            bx.find_element_by_xpath('(//a[@class="sc_batch"])[1]').click()
            num += 1
            #第一个出现的批量引用包含多个结果页面和一个单独结果页面
            #bx.find_element_by_xpath("//div[@id='1']//a[@class='sc_batch']").click()
            #用带有id的绝对xpath路径，当非常匹配时跳转到文献单独页面，不能点击批量引用了
        except:
                try:
                    bx.find_element_by_xpath('(//a[@class="sc_batch batched"])[1]')
                    #第一个是否被点击
                except:
                    print("文献: "+line.strip()+" 未发现")
                    break
                else:
                    print("已点击批量引用")
                    break
                print("批量引用无法点击")
                break
        else:
            print("="*40)
            print(line)
            try:
                get_zv1()
            except:
                get_zv2()
            break
        #当查找不到文献时，查找不到引用数量,每次成功点击后查看已经批量引用得数字，也可判断所有情况后查找
#for loop stop , download the current wfxm
downwx()
print(str(num) + "个文献引文被查找到并下载")
bx.quit()
