# -*- utf-8 -*-

import pytesseract
import requests
from PIL import Image
from io import BytesIO
import random

class Util:

	def __init__(self):
		pass

	def loadImage(self):
		r = random.random()
		url = "http://ssp.qingtingfm.com/index.php?w=200&h=100&r=login%sCaptcha&random=%s" %('%2F',str(r))
		print(url)
		response = requests.get(url)
		image = Image.open(BytesIO(response.content))
		image = self.binarizing(image,150)
		image = self.depoint(image)
		# image = self.udepoint(image)
		return image
		
	def binarizing(self,img,threshold):  
		'''传入image对象进行灰度、二值处理'''
		img = img.convert('L') #转灰度
		pixdata = img.load()
		w,h = img.size
		#遍历所有像素，大于阈值的为黑色
		for y in range(h):
			for x in range(w):
				if pixdata[x,y] < threshold:
					pixdata[x,y] = 0
				else:
					pixdata[x,y] = 255
		return img

	def vertical(self,img,threshold): #投影法分割字符
		"""传入二值化后的图片进行垂直投影"""
		pixdata = img.load()
		w,h = img.size
		ver_list = []
		#开始投影 
		for x in range(w):
			black = 0
			for y in range(h):
				if pixdata[x,y] == 0:
					black += 1
			ver_list.append(black)
		#判断边界
		l,r = 0,0
		flag = False
		cuts = []
		for i,count in enumerate(ver_list):
			if flag is False and count >threshold:
				l = i
				flag = True
			if flag and count == threshold:
				r = i-1
				flag = False
				cuts.append((l,r))
		return cuts

	def depoint(self,img): #降噪
		pixdata = img.load()
		w,h = img.size
		for y in range(1,h-1):
			for x in range(1,w-1):
				count = 0
				if pixdata[x,y-1] > 245:
					count = count +1
				if pixdata[x,y+1] > 245:
					count = count +1
				if pixdata[x-1,y] > 245:
					count = count +1
				if pixdata[x+1,y] > 245:
					count = count +1
				if pixdata[x-1,y-1] > 245:
					count = count +1
				if pixdata[x-1,y+1] > 245:
					count = count +1
				if pixdata[x+1,y-1] > 245:
					count = count +1
				if pixdata[x+1,y+1] > 245:
					count = count +1
				if count >4:
					pixdata[x,y] = 255
		return img

	def udepoint(self,img): #字体补全
		pixdata = img.load()
		w,h = img.size
		for y in range(1,h-1):
			for x in range(1,w-1):
				count = 0
				if pixdata[x,y-1] < 10:
					count = count +1
				if pixdata[x,y+1] < 10:
					count = count +1
				if pixdata[x-1,y] < 10:
					count = count +1
				if pixdata[x+1,y] < 10:
					count = count +1
				if pixdata[x-1,y-1] < 10:
					count = count +1
				if pixdata[x-1,y+1] < 10:
					count = count +1
				if pixdata[x+1,y-1] < 10:
					count = count +1
				if pixdata[x+1,y+1] < 10:
					count = count +1
				if count >4:
					pixdata[x,y] = 0
		return img