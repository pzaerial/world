# gathering_buddy.py
# @author pZ_aeriaL

# Standard libraries
import random
import time
import win32api
import win32con
import re

## Special libraries, installed via pip
import pyautogui

WINDOW_NAME = "New World"
window_ref = None ## Reference to the window.
window_searchable_region = None ## Region used for image searching.
facing_direction = "NORTH"
isRunning = False
bearing = 0
backAndForthState = 0

## Either do this or add "C:\Program Files (x86)\Tesseract-OCR" to path. I did both.
tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def main():
	print("INFO: Initializing...")
	getWindow()
	window_ref.activate()
	resetUI()
	gameLoop()


def getWindow():
	global window_ref, window_searchable_region, bearing
	windows = pyautogui.getWindowsWithTitle(WINDOW_NAME);
	if windows is None:
		raise OSError("No game window references were found.")
	foundWindow = False
	for window in windows:
		if window.title == WINDOW_NAME:
			window_ref = window
			foundWindow = True
	if foundWindow:
		print("INFO: Successfully grabbed game window.")
		window_searchable_region = (window_ref.left, window_ref.top, window_ref.width, window_ref.height)
		centerX = window_ref.left + (window_ref.width/2)
		bearing = centerX
		return
	raise OSError("This game window reference could not be found.")

## Resets the UI in case any elements have been expanded.
## Algorithm is to hit Escape a few times then click in the middle.
def resetUI():
	global window_ref
	centerX = window_ref.left + (window_ref.width/2)
	centerY = window_ref.top + (window_ref.height/2)
	for i in range(1,2):
		time.sleep(.1)
		pyautogui.press('escape')
	pyautogui.moveTo(centerX, centerY)
	time.sleep(.1)
	pyautogui.click()
	time.sleep(.1)
	print("INFO: Successfully reset game UI.")

def gameLoop():
	global window_ref

	time.sleep(1)
	pyautogui.press('f')
	time.sleep(1)

	pyautogui.click(x=550, y=150)
	time.sleep(3)

	while True:
		# First Owned Item
		checkWindowFocus()
		pyautogui.click(x=400, y=350)
		time.sleep(3)

		# First Buy Order
		checkWindowFocus()
		pyautogui.click(x=1700, y=625)
		time.sleep(3)

		# Max Quantity
		checkWindowFocus()
		pyautogui.click(x=1627, y=638)
		time.sleep(0.250)

		# Sell Now
		checkWindowFocus()
		pyautogui.click(x=1150, y=850)
		time.sleep(0.250)

def checkWindowFocus():
	window_is_active = window_ref.isActive
	if(window_is_active == False):
		print("INFO: Game Window not in focus. Breaking from loop.")
		exit()

## Script style handler
if __name__ == '__main__':
		main()