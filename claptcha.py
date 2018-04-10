# -*- utf-8 -*-

from PIL import Image
import pytesseract
from utils import Util

class Claptcha:
	
	def __init__(self):
		self.util = Util()

	def start(self):
		# for x in range(1,6):
		# 	image = self.util.loadImage()
		# 	image.save('images/%d.png'%x)
		
		image = Image.open('images/1.png')
		# # code = pytesseract.image_to_string(image)
		# # print(code)
		cuts = self.util.vertical(image,10)
		w,h = image.size
		print(cuts)
		for i,n in enumerate(cuts,1):
			temp = image.crop([n[0],0,n[1],h])
			temp.save("cut%s.png" %i)




def main():
	claptcha = Claptcha()
	claptcha.start()

if __name__ == '__main__':
	main()
		