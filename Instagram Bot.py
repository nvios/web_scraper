#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
import pandas as pd
import getpass


psw = getpass.getpass(prompt= 'Insert your Instagram password: ', stream=None)
    

webdriver = webdriver.Chrome('/Users/luca/Downloads/chromedriver')
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('myemail@company.com')
password = webdriver.find_element_by_name('password')
password.send_keys(psw)

button_login = webdriver.find_element_by_xpath("//button[@type='submit']")
button_login.click()
sleep(3)

notnow = webdriver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']") 
notnow.click()

hashtag_list = ['travel', 'nature', 'sunset', 'drone', 'streetphotography', 'architecture']

try:
    old_list = pd.read_csv ('users_followed_list.csv').squeeze().tolist()
except:
    old_list = []
   
new_list = old_list
followed = 0
likes = 0
comments = 0

for tag in range(len(hashtag_list)):
    webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    first_thumbnail.click()
    sleep(randint(1,2))    
    
    try:    
        for x in range(20):
            username = webdriver.find_element_by_xpath("//a[@class='FPmhX notranslate nJAzx']").text
            print (username)
            
            if username not in new_list:
                # If we already follow, do not unfollow
                if webdriver.find_element_by_xpath("//button[@class='oW_lN _0mzm- sqdOP yWX7d        ']").text == 'Follow':
                    #webdriver.find_element_by_xpath("//button[@class='oW_lN _0mzm- sqdOP yWX7d        ']").click()
                    new_list.append(username)
                    followed += 1
    
                    # Liking the picture
                    button_like = webdriver.find_element_by_xpath("//button[@class='dCJp8 afkep _0mzm-']")
                    button_like.click()
                    likes += 1
                    sleep(randint(2,8))
    
                    # Comments and tracker
                    comm_prob = randint(1,10)
                    print('{}_{}: {}'.format(hashtag_list[tag], x,comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        webdriver.find_element_by_xpath("//span[@class='glyphsSpriteComment__outline__24__grey_9 u-__7']").click()
                        comment_box = webdriver.find_element_by_xpath("//textarea[@class='Ypffh']")
    
                        if (comm_prob == 7):
                            comment_box.send_keys('Really nice!')
                            sleep(1)
                        elif (comm_prob == 8):
                            comment_box.send_keys('Very nice pic :)')
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys('Nice gallery!')
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys('Cool pic! ;)')
                            sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(3,8))
    
                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(1,6))
            else:
                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(1,4))  
    except:
        continue

csv = open('users_followed_list.csv', 'w')
csv.write('Followed\n')
for i in range (len(new_list)):
    csv.write(new_list[i] + '\n')
csv.close()

print('Followed {} people.'.format(followed))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
