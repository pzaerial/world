# fishing.py
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

# Customizable Knobs
WATER_TYPE = "SALTWATER" # SALTWATER or FRESHWATER. Inventory should have no more than one row of each. 
CASTING_TIME = 0.000 # Time holding left click before casting. 1.500 or 0.000 common options.
BASE_REELING_TIME = 1.500 # Base amount we reel in for each time.
ADDITIONAL_REELING_TIME = 0.015 # Additional reeling time for each iteration. Scales linearly.
MAX_REELS_BEFORE_CONTINUING = 25 #When reeling in, stop after this many pulls, as the fish has probably gotten away.
MAX_TIME_BEFORE_CONTINUING = 3.000 # When reeling in each time, stop after pulling for this long, as the line has probably broken.

# Ignore PyAutoGUI failsafe.
pyautogui.FAILSAFE = False

def main():
	print("INFO: Initializing...")
	getWindow()
	window_ref.activate()
	resetUI()
	time.sleep(1.500)
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

# Operates on a finite state machine representing the phases of fishing.
# 0: Starting state
# 1: Waiting for fish to be hooked.
# 2: Waiting for fish hooked icon to dissapear, meaning we can start reeling.
# 3: Reeling rod and waiting for reeling to finish.
# 4: Clear actions to get ready for next iteration.
def gameLoop():
	global window_ref, isRunning
	centerX = window_ref.left + (window_ref.width/2)
	centerY = window_ref.top + (window_ref.height/2)

	state = 0
	while True:
		window_is_active = window_ref.isActive
		if(window_is_active == False):
			print("INFO: Game Window not in focus. Breaking from loop.")
			return

		if state == 0:
			print("INFO: Getting rod out.")
			pyautogui.press('f3')
			time.sleep(1.500)

			print("INFO: Equipping bait.")
			pyautogui.press('r')
			time.sleep(1.500)
			if WATER_TYPE == "SALTWATER":
				win32api.SetCursorPos((1180, 600))
			else:
				win32api.SetCursorPos((1180, 450))
			time.sleep(0.100)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
			time.sleep(0.500)
			win32api.SetCursorPos((1500, 825))
			time.sleep(0.100)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
			time.sleep(3.000)

			print("INFO: Casting rod.")
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
			time.sleep(CASTING_TIME)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
			time.sleep(3.000)

			state = 1
		elif state == 1:
			if isLineCasted() == True:
				continue
			else:
				print("INFO: Fishing waiting icon went away.")

				state = 2
		elif state == 2:
			if isLineCasted() == False:
				print("INFO: Got something hooked!")
				time.sleep(0.050)
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
				time.sleep(1.000)

				state = 3
		elif state == 3:
			print("INFO: Starting to reel in...")
			keepReeling = True
			isKeyDown = False
			lastReelStartTime = 0
			reelTimes = 0
			while keepReeling == True:
				window_is_active = window_ref.isActive
				if(window_is_active == False):
					print("INFO: Game Window not in focus. Breaking from loop.")
					return

				if isF3PromptVisible() or reelTimes > MAX_REELS_BEFORE_CONTINUING:
					print("INFO: Finished reeling.")
					keepReeling = False
					continue

				if isKeyDown == True:
					now = time.time()
					elapsedTime = now - lastReelStartTime
					if elapsedTime > BASE_REELING_TIME + (reelTimes * ADDITIONAL_REELING_TIME):
						print("INFO: Waiting for line tension to go down.")
						win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
						isKeyDown = False
						slackWaitStart = time.time()
						elapsedTime = 0
						while True: 
							window_is_active = window_ref.isActive
							if(window_is_active == False):
								print("INFO: Game Window not in focus. Breaking from loop.")
								return

							if isF3PromptVisible():
								print("INFO: The hooked object escaped.")
								break

							elapsedTime = time.time() - slackWaitStart
							if isLineSlack() or elapsedTime > MAX_TIME_BEFORE_CONTINUING:
								break
				else:
					print("INFO: Reeling...")
					lastReelStartTime = time.time()
					win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
					isKeyDown = True
					reelTimes = reelTimes + 1

			state = 4
		elif state == 4:
			print("INFO: Unclicking mouse.")
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

			print("INFO: Exiting fishing mode.")
			time.sleep(2.000)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
			time.sleep(0.0100)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
			time.sleep(0.0097)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
			time.sleep(0.0100)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
			time.sleep(0.0089)

			print("INFO: Doing anti-AFK detection movement.")
			sleepAmt = random.random() * 0.025 + 0.010
			time.sleep(1.000)
			pyautogui.keyDown('a');
			time.sleep(sleepAmt)
			pyautogui.keyUp('a');
			time.sleep(0.500)
			pyautogui.keyDown('d');
			time.sleep(sleepAmt)
			pyautogui.keyUp('d');
			time.sleep(3.000)

			state = 0
		else:
			state = 0


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

def isLineCasted():
	img = pyautogui.locateOnScreen("fishing.png")
	if img is None:
		return False
	return True

def isF3PromptVisible():
	img = pyautogui.locateOnScreen("F3Prompt.png")
	img2 = pyautogui.locateOnScreen("F3Prompt2.png")
	if img is not None or img2 is not None:
		return True
	return False

def isLineSlack():
	img1 = pyautogui.locateOnScreen("fishinglowtension.png")
	img2 = pyautogui.locateOnScreen("fishinglowtension2.png")
	if img1 is not None or img2 is not None:
		return True
	return False

## Script style handler
if __name__ == '__main__':
		main()