from PIL import Image
from selenium import webdriver

import cv2
import pytesseract
import requests
import time

import os


driver = webdriver.Firefox(executable_path='~/geckodriver')

driver.get('https://test.com')

time.sleep(4)

driver.save_screenshot("image.png")
image = driver.find_element_by_tag_name("iframe")
# crop image
width = image.location['x'] + image.size['width']
height = image.location['y']+ image.size['height']
print("width : ", width)
print("height : ", height)
im = Image.open('image.png')
im = im.crop((image.location['x'], image.location['y'], int(width), int(height)))
im.save('element.png', dpi=(300, 300))


img = cv2.imread('element.png')
gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blr = cv2.GaussianBlur(gry, (3, 3), 0)
thr = cv2.threshold(blr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
cv2.imwrite('element.png',thr)

txt = pytesseract.image_to_string('element.png')
print(txt)



# Fill The Form
txtCaptcha = driver.find_element_by_id("txtCaptcha")
txtCaptcha.send_keys(txt[:7])

txtBusinessName = driver.find_element_by_id("txtBusinessName")
txtBusinessName.send_keys("Blue") # INSERT THE COMPANY NAME



btn = driver.find_element_by_id("btnSearch")
btn.click()

time.sleep(10)

driver.quit()
