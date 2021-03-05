import pygame as pg
import music_player as mp
import time
import screenshot
import atexit
import PIL
import concurrent.futures
import pyautogui
import random
import win32gui

def img_pixelMatchesColor(img, coord, rgb, tolerence=0):
	x = 0
	for i in rgb:
		if img.getpixel(coord)[x] < rgb[x] - tolerence or img.getpixel(coord)[x] > rgb[x] + tolerence:
			return False
		x = x + 1
	return True

def delay(ms, randmax):
	timer = int(time.time() * 1000)
	tmp = timer + ms + random.randint(0, randmax)
	while int(time.time() * 1000) < tmp:
		ms = ms + 1

def click(coord):
	try:
		pyautogui.moveTo(random.randint(coord[0], coord[0] + coord[2]), random.randint(coord[1], coord[1] + coord[3]), random.randint(15, 30) / 100)
		pyautogui.mouseDown()
		delay(50, 100)
		pyautogui.mouseUp()
	except:
		pass

class SWBot(object):
	def __init__(self):
		self.init_pygame()
		atexit.register(pg.quit)
		self.screenshot = screenshot.Screenshot()
		self.init_variables()
		f1 = concurrent.futures.ThreadPoolExecutor().submit(self.screen_analyse, 4000)
		#self.screen_analyse(5000)
		#self.test(5000)
		#f1 = concurrent.futures.ThreadPoolExecutor().submit(self.test, 5000)

	def init_pygame(self):
		pg.init()
		icon_surface = pg.image.load("icon.ico")
		pg.display.set_icon(icon_surface)
		pg.display.set_caption("SWBot")
		self.screen = pg.display.set_mode((800, 600))

	def init_variables(self):
		self.launched = True
		self.fps = 30
		self.nox_launched = False
		self.sw_pics_end_fight = 	{
									"defeated" : PIL.Image.open("sw_pics/defeated.png"),
									"ok_rta" : PIL.Image.open("sw_pics/ok_rta.png"),
									"victory" : PIL.Image.open("sw_pics/victory.png")
									}
		self.resized_sw_pics_end_fight = [False] * len(self.sw_pics_end_fight)
		self.sw_pics =	{
						"go" : PIL.Image.open("sw_pics/go.png"),
						"ok" : PIL.Image.open("sw_pics/ok.png"),
						"preparation" : PIL.Image.open("sw_pics/preparation.png"),
						"suivant" : PIL.Image.open("sw_pics/suivant.png"),
						"treasure" : PIL.Image.open("sw_pics/treasure.png"),
						}
		self.resized_sw_pics = [False] * len(self.sw_pics)
		self.confidence = 0.7
		self.last_img_size = [0, 0]
		self.clock = pg.time.Clock()

	def display(self):
		mx, my = pg.mouse.get_pos()
		self.screen.fill((60, 70, 90))
		pg.display.flip()

	def screen_analyse(self, ms):
		mx, my = pg.mouse.get_pos()
		self.curr_window = win32gui.GetForegroundWindow()
		while self.launched:
			timer = time.time() * 1000
			img = self.screenshot.screenshot("NoxPlayer")
			if img != False:
				debug_timer = time.time()
				if img.size[0] != self.last_img_size[0] or img.size[1] != self.last_img_size[1]:
					self.nox_launched = True
					# BORDURE NOX : TOP = 32 BOT = 2
					# COULEUR BORDURE : (13, 16, 48) (blue)
					x = 0
					y = 33
					while x < img.size[0] and img_pixelMatchesColor(img, (x, y), (13, 16, 48), 0):
						x += 1
					result = x
					x = 1
					while x < img.size[0] and img_pixelMatchesColor(img, (img.size[0] - x, y), (13, 16, 48), 0):
						x += 1
					result += x - 1
					self.px, self.py = (img.size[0] - result) / 1788, (img.size[1] - 34) / 1006
					self.last_img_size[0] = img.size[0]
					self.last_img_size[1] = img.size[1]
				print(f"time to calculate border {time.time() - debug_timer} m")
				debug_timer_resize = 0
				debug_count_resize = 0
				debug_timer_locate = 0
				debug_count_locate = 0
				x = 0
				for key, value in self.sw_pics_end_fight.items():
					if self.resized_sw_pics_end_fight[x] == False \
					or self.resized_sw_pics_end_fight[x].size[0] != (int(value.size[0] * self.px)) \
					or self.resized_sw_pics_end_fight[x].size[1] != (int(value.size[1] * self.py)):
						debug_timer = time.time()
						self.resized_sw_pics_end_fight[x] = value.resize((int(value.size[0] * self.px), int(value.size[1] * self.py)))
						debug_timer_resize += time.time() - debug_timer
						debug_count_resize += 1
					debug_timer = time.time()
					locate = pyautogui.locate(self.resized_sw_pics_end_fight[x], img, grayscale=True, confidence=self.confidence)
					debug_timer_locate += time.time() - debug_timer
					debug_count_locate += 1
					#locate = pyautogui.locate(value, img, grayscale=True, confidence=self.confidence + 0.2)
					if locate:
						print(f"button '{key}' found")
						break
					x = x + 1
				x = 0
				for key, value in self.sw_pics.items():
					if self.resized_sw_pics[x] == False \
					or self.resized_sw_pics[x].size[0] != (int(value.size[0] * self.px)) \
					or self.resized_sw_pics[x].size[1] != (int(value.size[1] * self.py)):
						debug_timer = time.time()
						self.resized_sw_pics[x] = value.resize((int(value.size[0] * self.px), int(value.size[1] * self.py)))
						debug_timer_resize += time.time() - debug_timer
						debug_count_resize += 1
					debug_timer = time.time()
					locate = pyautogui.locate(self.resized_sw_pics[x], img, grayscale=True, confidence=self.confidence)
					debug_timer_locate += time.time() - debug_timer
					debug_count_locate += 1
					if locate:
						print(f"button '{key}' found")
						break
					x = x + 1
						#if key == "victory" or key == "defeated":
							#mx, my = pg.mouse.get_pos()
							#self.curr_window = win32gui.GetForegroundWindow()
						#win32gui.SetForegroundWindow(self.screenshot.hwnd)
						#if key == "defeated" or key == "victory":
						#	click((self.screenshot.left + locate[0], self.screenshot.top + int(locate[1] + img.size[1] / 2), 
						#		locate[2], locate[3]))
						#else:
						#	click((self.screenshot.left + locate[0], self.screenshot.top + locate[1], locate[2], locate[3]))
						#	if key == "go":
						#		win32gui.SetForegroundWindow(self.curr_window)
						#		pyautogui.moveTo(mx, my)
				if debug_count_locate:
					print(f"Locate Timer :\t{debug_timer_locate} {debug_count_locate} = {debug_timer_locate / debug_count_locate} / locate")
				if debug_count_resize:
					print(f"Resize Timer :\t{debug_timer_resize} {debug_count_resize} = {debug_timer_resize / debug_count_resize} / resize")
				print("-" * 11 + "\n")
			else:
				self.nox_launched = False
			while time.time() * 1000 - timer < ms:
				sleep_time = (ms - (time.time() * 1000 - timer)) / 1000
				if sleep_time > 500:
					sleep_time = 500
				time.sleep(sleep_time / 1000)
				if not self.launched:
					exit()

swbot = SWBot()

while swbot.launched:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			swbot.launched = False
		elif event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				tmp = time.time()
				img = swbot.screenshot.screenshot("NoxPlayer")
				print(time.time() - tmp, 's')

	swbot.display()
	swbot.clock.tick(swbot.fps)
