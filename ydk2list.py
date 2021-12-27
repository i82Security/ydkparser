import re
import requests
import io  
import sys 
import json
import urllib
from bs4 import BeautifulSoup
import sqlite3
import time
import fitz
from PIL import ImageDraw,ImageFont
from PIL import Image 
import random
import numpy as np
#import cv2
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') 

class cardDict(dict):
 
	def __missing__(self,key):
		#print("调用了 User的__missing__方法")
		return False
 
	def __getitem__(self, item):
		# print("调用User 类的 __getitem__方法")
		return super(cardDict, self).__getitem__(item)
 
	def get(self, k, d=None):
	# print("调用User 类的 get 方法")
		return super(cardDict, self).get(k, d)
 
	def appendCard(self,k):
		if self[k]:
			self[k] = self[k] +1
		else:
			self[k] = 1
class ydkParser(object):
	"""docstring for ydkParser"""
	def __init__(self,path):
		super(ydkParser).__init__()
		self.path = path
		self.mainEffectDeck =  cardDict()
		self.mainSpellDeck = cardDict()
		self.mainTrapDeck = cardDict()
		self.extraDeck = cardDict()
		self.sideDeck = cardDict()
	def parser(self):
		conn = sqlite3.connect("cards.db")
		c = conn.cursor()
		with open(self.path) as f:
			lines = f.readlines()
			mainBegin = False
			exBegin = False
			sideBegin = False
			for line in lines:
				if line.find("#created") != -1:
					continue
				if line.find("#main") != -1:
					mainBegin = True
					continue
				if line.find("#extra") != -1:
					mainBegin = False
					exBegin = True
					continue
				if line.find("side") != -1:
					mainBegin = False
					exBegin = False
					sideBegin = True
					continue
				sql = "select * from datas where id = {cardid}".format(cardid=line.replace("\n", ""))
				#print(sql)
				l = c.execute(sql)
				for card in l:
					cid = card[0]
					cname = card[1]
					jname = card[2]
					ctype = card[3]
					if mainBegin:
						if ctype == 0 or ctype == 1 or ctype == 2:
							self.mainEffectDeck.appendCard(jname)
							continue
						if ctype == 7:
							self.mainSpellDeck.appendCard(jname)
							continue
						if ctype == 8:
							self.mainTrapDeck.appendCard(jname)
							continue
					if exBegin:
						self.extraDeck.appendCard(jname)
						continue
					if sideBegin:
						self.sideDeck.appendCard(jname)
						continue
		return None
	def reportResult(self):
		print("怪兽")
		for jname in self.mainEffectDeck.keys():
			print(jname,self.mainEffectDeck[jname])	
		print("魔法")
		for jname in self.mainSpellDeck.keys():
			print(jname,self.mainSpellDeck[jname])
		print("陷阱")
		for jname in self.mainTrapDeck.keys():
			print(jname,self.mainTrapDeck[jname])
		print("额外")
		for jname in self.extraDeck.keys():
			print(jname,self.extraDeck[jname])
		print("Side")
		for jname in self.sideDeck.keys():
			print(jname,self.sideDeck[jname])
	def drawCardName(self,path,outpath):
		self.im = Image.open(path)#生成空白图像
		self.im = self.im.convert("RGB")
		draw = ImageDraw.Draw(self.im)
		basex= 1000
		basey= 2000
		font = ImageFont.truetype('simhei.ttf',48)
		t = 0
		for c in self.mainEffectDeck.keys():
			draw.text((basex,basey+t*150),c.replace("・","·"),font=font,fill= (0,0,0),direction=None )
			draw.text((780,basey+t*150),str(self.mainEffectDeck[c]),font=font,fill= (0,0,0),direction=None )
			t = t+1
		t= 0
		for c in self.mainSpellDeck.keys():
			draw.text((2650,basey+t*150),c.replace("・","·"),font=font,fill= (0,0,0),direction=None )
			draw.text((2450,basey+t*150),str(self.mainSpellDeck[c]),font=font,fill= (0,0,0),direction=None )
			t = t+1
		t= 0
		for c in self.mainTrapDeck.keys():
			draw.text((4350,basey+t*150),c.replace("・","·"),font=font,fill= (0,0,0),direction=None )
			draw.text((4050,basey+t*150),str(self.mainTrapDeck[c]),font=font,fill= (0,0,0),direction=None )
			t = t+1
		t=0
		for c in self.extraDeck.keys():
			draw.text((basex,5400+t*150),c.replace("・","·"),font=font,fill= (0,0,0),direction=None )
			draw.text((780,5400+t*150),str(self.extraDeck[c]),font=font,fill= (0,0,0),direction=None )
			t = t+1
		t=0
		for c in self.sideDeck.keys():
			draw.text((2650,5400+t*150),c.replace("・","·"),font=font,fill= (0,0,0),direction=None )
			draw.text((2450,5400+t*150),str(self.sideDeck[c]),font=font,fill= (0,0,0),direction=None )
			t = t+1
		del draw
		self.im.save(outpath)

if __name__ == '__main__':
	impath = "D:\YGOPro_Setup_2020-12-01\YGOPro\\1.png"
	outpath ="D:\YGOPro_Setup_2020-12-01\YGOPro\\out.png"
	pdfpath = "D:\YGOPro_Setup_2020-12-01\YGOPro\\list.pdf"
	p = ydkParser("D:\YGOPro_Setup_2020-12-01\YGOPro\\deck\\test.ydk")
	#p.pdf_images(pdfpath,"D:\YGOPro_Setup_2020-12-01\YGOPro\\",5,5,0)
	p.parser()
	p.reportResult()
	p.drawCardName(impath, outpath)
	print("Pass")
	#doc = fitz.open(pdfpath)
	#page = doc.load_page(0)
	#p = fitz.Point(100,100)
	#rc = page.insert_text(p,"中文",fontname = "helv",fontsize =12,rotate=0)
	#doc.save("D:\YGOPro_Setup_2020-12-01\YGOPro\\out.pdf")
	#print(p.mainEffectDeck)
	#print(p.mainSpellDeck)
	#print(p.mainTrapDeck)