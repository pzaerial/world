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
import mss
import numpy as np
import cv2
import pytesseract
from PIL import Image, ImageEnhance

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

def gameLoop():
	global window_ref, isRunning
	centerX = window_ref.left + (window_ref.width/2)
	centerY = window_ref.top + (window_ref.height/2)

	lastTurn = time.time()
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

		# ## Bounding Box Navigation
		# ## [Max X, Min X, Max Y, Min Y]
		# boundingBox = [8000, 7750.0, 4090.0, 3965.0]
		# position = getLocation()
		# if position is not None:
		# 	xPos = position[0]
		# 	yPos = position[1]
		# 	xCorrection = 0
		# 	yCorrection = 0
		# 	if xPos > boundingBox[0]:
		# 		xCorrection = boundingBox[0] - xPos
		# 	elif xPos < boundingBox[1]:
		# 		xCorrection = xPos - boundingBox[1]
		# 	if yPos > boundingBox[2]:
		# 		yCorrection = boundingBox[2] - yPos
		# 	elif yPos < boundingBox[3]:
		# 		yCorrection = yPos - boundingBox[3]

		# 	# Correct using 90 degree turning first to fix one aspect at a time.
		# 	if xCorrection > 0:
		# 		print("INFO: Player has left bounding box in the -X direction. Need to move EAST (+X direction). X Correction: " + str(xCorrection))
		# 	elif xCorrection < 0:
		# 		print("INFO: Player has left bounding box in the +X direction. Need to move WEST (-X direction). X Correction: " + str(xCorrection))
		# 	elif yCorrection > 0:
		# 		print("INFO: Player has left bounding box in the -Y direction. Need to move NORTH (+Y direction). Y Correction: " + str(yCorrection))
		# 	elif yCorrection < 0:
		# 		print("INFO: Player has left bounding box in the +Y direction. Need to move SOUTH (-Y direction). Y Correction: " + str(yCorrection))
		# 	else:
		# 		print("INFO: Player is inside bounding box.")
		# else:
		# 	print("INFO: Got None from location data.")



		## Live loop.
		if(isHarvesting() == True):
			if isRunning is True:
				print("INFO: Stopped running to harvest something.")
				pyautogui.keyUp('w')
				isRunning = False
				pyautogui.press('f')
			continue

		now = time.time()

		if(isRunning == False):
			toggleRunning()

		# Implementation 1: Square
		# if(now - lastTurn > 60.000):
		# 	turn90Degrees()
		# 	lastTurn = time.time()

		# Implementation 2: Triangle
		# if(now - lastTurn > 60.000):
		# 	turn120Degrees()
		# 	lastTurn = time.time()

		# Implementation 3: Back and Forth (With variation)
		# if(now - lastTurn > 60.000):
		# 	turnBackAndForth()
		# 	lastTurn = time.time()

		# Implementation 4: Run in a long rectangle, starting along the bottom left going along a long side. (facing "north")
		if now - lastTurn > 60.000 and (facing_direction == "NORTH" or facing_direction == "SOUTH"):
			turn90Degrees()
			lastTurn = time.time()
		elif now-lastTurn > 10.000 and (facing_direction == "EAST" or facing_direction == "WEST"):
			turn90Degrees()
			lastTurn = time.time()

		if(now - lastF > 0.020):
			pyautogui.press('f')
			lastF = time.time()

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

def toggleRunning():
	global isRunning
	if(isRunning == False):
		print("INFO: Starting to run.")
		pyautogui.keyDown('w')
		isRunning = True
	else:
		print("INFO: Stopping running.")
		pyautogui.keyUp('w')
		isRunning = False


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


def getLocation():
	global tesseract_cmd, window_ref
	with mss.mss() as sct:
		screenshot_region = {
			"mon":1,
			"top":20,
			"left":window_ref.width - 270,
			"width":275,
			"height":17
		}

		## Get base image
		sct_img = sct.grab(screenshot_region)
		mss.tools.to_png(sct_img.rgb, sct_img.size, output='tmpLocationPicture.png')
		# print("DEBUG: Pytesseract read from the screenshot: " + pytesseract.image_to_string('tmpLocationPicture.png'))

		##Enhance image for contrast //THIS WORKED BEST ON contrast_in.enhance(2)
		pil_img = Image.open('tmpLocationPicture.png')
		contrast_in = ImageEnhance.Contrast(pil_img)
		contrast_out = contrast_in.enhance(8)
		contrast_out.save('tmpContrastLocationPicture.png')
		# print("DEBUG: Pytesseract read from the high contrast image: " + pytesseract.image_to_string('tmpContrastLocationPicture.png'))

		# ## Binarize image according to threshold, This is a good practice but doesn't seem to do better than the others in daytime.
		# threshold = 175
		# bin_img = Image.open("tmpLocationPicture.png")
		# greyscale_img = bin_img.convert('L') #greyscale
		# binarized_img = greyscale_img.point( lambda p: 255 if p > threshold else 0 ) #binarization
		# bin_out = binarized_img.convert('1') #to mono
		# bin_out.save("tmpBinarizedLocationPicture.png")
		# print("DEBUG: Pytesseract read from the contrast + black and white image: " + pytesseract.image_to_string('tmpBWLocationPicture.png'))

		# ## Convert image to B&W //THIS IS WORSE THAN THE CONTRAST ONE.
		# bw_img = Image.open('tmpContrastLocationPicture.png')
		# bw_in = ImageEnhance.Color(bw_img)
		# bw_out = bw_in.enhance(0)
		# bw_out.save('tmpBWLocationPicture.png')
		# # print("DEBUG: Pytesseract read from the contrast + black and white image: " + pytesseract.image_to_string('tmpBWLocationPicture.png'))

	tess_string = pytesseract.image_to_string('tmpContrastLocationPicture.png')
	return parseLocationData(tess_string)

def parseLocationData(loc):
	## Step 1: Is the string enclosed in square brackets, return string with brackets + remaining whitespace clipped.
	leftBracketPos = loc.find('[')
	rightBracketPos = loc.find(']')
	if leftBracketPos == -1 or rightBracketPos == -1:
		return None
	loc = loc[leftBracketPos+1:rightBracketPos]
	# print("DEBUG: Sliced string: " + loc)
	loc = loc.replace(" ", "")
	# print("DEBUG: No whitespace string: " + loc)

	## Step 2: Tesseract distinguishes between numbers well, but not between commas and periods. 
	## Break into an array and build numbers back up, knowing that we have a whole number and decimal component, alternating. Verify each of the 6 parts is numeric only.
	arr = re.split(r'[,.]', loc)
	# print("DEBUG: Location array: " + str(arr))
	if len(arr) != 6:
			# print("DEBUG: Location parts array did not tokenize into 6 parts.")
			return None
	for a in arr:
		if not a.isnumeric():
			# print("DEBUG: One or more location components was not fully numeric: " + a)
			return None

	## Step 3: Concatenate into decimal strings and return as a triple.
	x = arr[0] + "." + arr[1]
	y = arr[2] + "." + arr[3]
	z = arr[4] + "." + arr[5]
	location = (float(x), float(y), float(z))
	print("DEBUG: Location: " + str(location))
	return location


def turn90Degrees():
	global facing_direction, window_ref, bearing
	centerX = int(window_ref.left + (window_ref.width/2))
	centerY = int(window_ref.top + (window_ref.height/2))
	if(facing_direction == "NORTH"):
		print("INFO: Turning EAST.")
		newX = int(centerX + 5500)
		bearing = newX
		win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,newX,centerY)
		facing_direction = "EAST"
	elif(facing_direction == "EAST"):
		print("INFO: Turning SOUTH.")
		newX = int(centerX + 11000)
		bearing = newX
		win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,newX,centerY)
		facing_direction = "SOUTH"
	elif(facing_direction == "SOUTH"):
		print("INFO: Turning WEST.")
		newX = int(centerX - 5500)
		bearing = newX
		win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,newX,centerY)
		facing_direction = "WEST"
	elif(facing_direction == "WEST"):
		print("INFO: Turning NORTH.")
		bearing = centerX
		win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,centerX,centerY)
		facing_direction = "NORTH"
	else:
		facing_direction = "NORTH"

def turn120Degrees():
	global window_ref, bearing
	print("INFO: Turning {} units.", 7500)
	centerY = int(window_ref.top + (window_ref.height/2))
	newX = int(bearing + 7500)
	bearing = int(newX)
	win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,newX,centerY)

def turnBackAndForth():
	global window_ref, backAndForthState
	centerX = int(window_ref.left + (window_ref.width/2))
	centerY = int(window_ref.top + (window_ref.height/2))

	if(backAndForthState == 0):
		print("INFO: Turning around.")
		variation = (random.random() * 300) - 150
		newX = int(centerX + 11000 + variation)
		win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,newX,centerY)
		backAndForthState = 1
	elif(backAndForthState == 1):
		print("INFO: Turning around.")
		variation = (random.random() * 300) - 150
		newX = int(centerX + variation)
		win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,newX,centerY)
		backAndForthState = 0
	else:
		backAndForthState = 0

## Script style handler
if __name__ == '__main__':
		main()