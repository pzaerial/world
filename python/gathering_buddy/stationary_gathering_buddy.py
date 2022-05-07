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
from PIL import Image, ImageEnhance

WINDOW_NAME = "New World"
window_ref = None ## Reference to the window.
window_searchable_region = None ## Region used for image searching.

TIME_BETWEEN_ITEM_PICKUP_PRESSES = 10.000
TIME_BETWEEN_ITEM_PICKUP_PRESSES_CAP = 30.000
ITEM_PICKUP_KEY = 'f'
TIME_BETWEEN_ANTI_AFK_MOVEMENTS = 300.000

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

def gameLoop():
	global window_ref
	centerX = window_ref.left + (window_ref.width/2)
	centerY = window_ref.top + (window_ref.height/2)

	lastAntiAfk = time.time()
	lastF = time.time()
	while True:
		window_is_active = window_ref.isActive
		if(window_is_active == False):
			print("INFO: Game Window not in focus. Breaking from loop.")
			return

		if isPlayerDead() == True:
			print("INFO: Player is dead. Stopping program....")
			return

		if isPlayerMenuOpen() == True:
			print("INFO: Player menu is open. Closing it...")
			pyautogui.press('escape')	
			time.sleep(1)
			toggleRunning()
			time.sleep(2)
			continue

		now = time.time()

		if(now - lastF > TIME_BETWEEN_ITEM_PICKUP_PRESSES or now - lastF > TIME_BETWEEN_ITEM_PICKUP_PRESSES_CAP):
			pyautogui.press(ITEM_PICKUP_KEY)
			lastF = time.time()

		if(isHarvesting() == True):
			continue

		if(now - lastAntiAfk > TIME_BETWEEN_ANTI_AFK_MOVEMENTS):
			print("INFO: Doing anti-afk moves...")
			antiAfk()
			lastAntiAfk = time.time()

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

def isHarvesting():
	img = pyautogui.locateOnScreen("yellowWeaponLock.png")
	if img is None:
		return True
	return False

def isPlayerDead():
	img = pyautogui.locateOnScreen("respawn_button.png")
	if img is None:
		return False
	return True

def isPlayerMenuOpen():
	img = pyautogui.locateOnScreen("store_button.png")
	if img is None:
		return False
	return True

def antiAfk():
	sleepAmt = random.random() * 0.025 + 0.010
	pyautogui.keyDown('a');
	time.sleep(sleepAmt)
	pyautogui.keyUp('a');
	time.sleep(0.500)
	pyautogui.keyDown('d');
	time.sleep(sleepAmt)
	pyautogui.keyUp('d');

## Script style handler
if __name__ == '__main__':
		main()