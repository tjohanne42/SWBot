"""
import pyautogui
import win32gui

def screenshot(window_title=None):
	if window_title:
		hwnd = win32gui.FindWindow(None, window_title)
		if hwnd:
			win32gui.SetForegroundWindow(hwnd)
			x, y, x1, y1 = win32gui.GetClientRect(hwnd)
			x, y = win32gui.ClientToScreen(hwnd, (x, y))
			x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
			im = pyautogui.screenshot(region=(x, y, x1, y1))
			return im
		else:
			print('Window not found!')
	else:
		im = pyautogui.screenshot()
		return im


im = screenshot('Calculatrice')
if im:
	im.show()
"""
"""

import win32gui
import win32ui
import win32con

def background_screenshot(hwnd, width, height):
	wDC = win32gui.GetWindowDC(hwnd)
	dcObj = win32ui.CreateDCFromHandle(wDC)
	cDC=dcObj.CreateCompatibleDC()
	dataBitMap = win32ui.CreateBitmap()
	dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
	cDC.SelectObject(dataBitMap)
	cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
	dataBitMap.SaveBitmapFile(cDC, 'screenshot.bmp')
	dcObj.DeleteDC()
	cDC.DeleteDC()
	win32gui.ReleaseDC(hwnd, wDC)
	win32gui.DeleteObject(dataBitMap.GetHandle())

hwnd = win32gui.FindWindow(None, 'Calculatrice')
background_screenshot(hwnd, 1920, 1080)
"""

import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import atexit

class Screenshot(object):
	def __init__(self):
		self.left, self.top, self.right, self.bot = False, False, False, False
		atexit.register(self.clean)

	def screenshot(self, windowname, save=False):
		self.hwnd = win32gui.FindWindow(None, windowname)
		if self.hwnd == 0:
			print(f"Window '{windowname}' not found.")
			return False
		# Change the line below depending on whether you want the whole window
		# or just the client area. 
		#tmpleft, tmptop, tmpright, tmpbot = win32gui.GetClientRect(self.hwnd)
		tmpleft, tmptop, tmpright, tmpbot = win32gui.GetWindowRect(self.hwnd)
		if (self.left, self.top, self.right, self.bot) != (tmpleft, tmptop, tmpright, tmpbot):
			try:
				self.saveDC.DeleteDC()
				self.mfcDC.DeleteDC()
			except:
				pass
			(self.left, self.top, self.right, self.bot) = (tmpleft, tmptop, tmpright, tmpbot)
			self.w = self.right - self.left
			self.h = self.bot - self.top
			hwndDC = win32gui.GetWindowDC(self.hwnd)
			self.mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
			self.saveDC = self.mfcDC.CreateCompatibleDC()
		saveBitMap = win32ui.CreateBitmap()
		saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
		self.saveDC.SelectObject(saveBitMap)
		# Change the line below depending on whether you want the whole window
		# or just the client area. 
		#result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
		result = windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), 0)
		bmpinfo = saveBitMap.GetInfo()
		bmpstr = saveBitMap.GetBitmapBits(True)
		img = Image.frombuffer(
			"RGB",
			(bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
			bmpstr, "raw", "BGRX", 0, 1)
		if type(save) == str and result == 1:
			img.save(save)
		win32gui.DeleteObject(saveBitMap.GetHandle())
		return img

	def clean(self):
		try:
			self.saveDC.DeleteDC()
			self.mfcDC.DeleteDC()
		except:
			pass
