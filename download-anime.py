import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import bs4 as bs
import requests
import urllib.request
import sys
import os
import time


# site = sys.argv[1]
site = "9anime"
site = "https://"+site+".is/"
dic = {"op" : "one-piece.ov8","dbs" : "dragon-ball-super.7jly","boruto":"boruto-naruto-next-generations.97vm"}

manga = sys.argv[1]        # change here
episode_no = sys.argv[2]    	# change-here

anime= dic[manga]
site = site + "watch/" + anime

print(site)

#driver = webdriver.Firefox(executable_path="/home/akash/drivers/geckodriver")
driver = webdriver.Chrome(executable_path="/home/akash/drivers/chromedriver")
driver.get(site)

soup = bs.BeautifulSoup(requests.get(site).content,"lxml")
#print(soup.prettify())

for x in driver.find_elements_by_xpath("//span[contains(@class,'tab')]"):
    if x.text == 'OpenLoad':
        x.click()

shift = int(episode_no) // 50
str_shift = str(shift)
print(shift)

driver.execute_script("window.scrollBy(0,200)")
# browser.execute_script("window.scrollBy(0,10000)")

try:
	eps = soup.find('div',class_='range')
	for ep in eps.find_all('span'):
	    if ep['data-range-id'] == str(shift):
	        eps_range = ep.text

	x = driver.find_elements_by_xpath("//span[contains(@data-range-id,str_shift)]")
	x = [i for i in x if i.text == eps_range][0]
	x.click()

except Exception as e:
	print(str(e))

for ul in driver.find_elements_by_tag_name('ul'):
    if ul.get_attribute('data-range-id') == str(shift):
        for links in ul.find_elements_by_tag_name('a'):
            if links.get_attribute('data-base') == episode_no:
                url = links.get_attribute('href')
                break
                
driver.get(url)

x = driver.find_element_by_xpath("//div[contains(@class,'cover')]")
x.click()

time.sleep(2)

for i in range(3):
    x = driver.find_element_by_xpath("//div[contains(@id,'player')]")
    #button = x.find_element_by_tag_name('button')
    click = x.find_element_by_tag_name('iframe')
    src = click.get_attribute('src')
    click.click()
    time.sleep(1)

print(src)


#driver1 = webdriver.Firefox(executable_path="/home/akash/drivers/geckodriver")
driver1 = webdriver.Chrome(executable_path="/home/akash/drivers/chromedriver")
driver1.get(src)

x = driver1.find_element_by_tag_name('div')
x.click()

src = driver1.find_element_by_tag_name('video').get_attribute('src')
print(src)

driver.close()
driver1.close()


root = '.'
last_percent_reported = None

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def download_progress_hook(count, blockSize, totalSize):
    global last_percent_reported
    percent = int(count*blockSize * 100 / totalSize)
    
    if last_percent_reported != percent:
        if percent % 5 == 0:
            sys.stdout.write("%s%%" % percent)
            sys.stdout.flush()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
        last_percent_reported = percent

urllib.request.urlretrieve(src,"%s.mp4"%os.path.join(root,manga),reporthook=download_progress_hook)
