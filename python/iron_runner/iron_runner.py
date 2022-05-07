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
SLEEP_TIME_BETWEEN_ACTIONS=0.500
window_ref = None ## Reference to the window.
window_searchable_region = None ## Region used for image searching.
isRunning = False

def main():
	print("INFO: Initializing...")
	getWindow()
	window_ref.activate()
	resetUI()
	gameLoop()


def getWindow():
	global window_ref, window_searchable_region
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
		return
	raise OSError("This game window reference could not be found.")


## Resets the UI in case any elements have been expanded.
## Algorithm is to hit Escape a few times then click in the middle.
def resetUI():
	global window_ref
	time.sleep(1)
	for i in range(1,3):
		pyautogui.press('escape')
		time.sleep(1)
	print("INFO: Successfully reset game UI.")

## Main Game Loop
## TAS Iron Route Runner from Everfall to Monarch's Bluffs. Uses state to go through a series of steps.
## Precondition is looking exactly West from the West gate of everfall in between the 2 lamp posts.
def gameLoop():
	global isRunning
	
	directive_index = 0
	directives = [
		["forward", 13.000],
		["forwardleft", 1.000],
		["forward", 10.000],
		["forwardleft", 5.000],
		["forward", 2.000],
		["forwardleft", 5.000],
		["forward", 2.000],
		["forwardleft", 3.000],
		["forward", 2.000],
		["forwardleft", 3.000],
		["forward", 17.000],
		["forwardleft", 5.000],
		["forward", 3.000],
		["forwardleft", 4.000],
		["forward", 7.000],
		["forwardright", 7.000],
		["forward", 3.000],
		["forwardright", 7.000],
		["forward", 1.000],

		["pressf", 6.000],
		["forward", 1.000],
		["pressf", 9.000],
		["forwardleft", 10.000],
		["left", 3.250],
		["pressf", 6.000],
		["left", 1.000],
		["pressf", 9.000],
		["right", 5.000],
		["forwardright", 9.500],
		["pressf", 9.000],
		["forwardright", 1.000],
		["pressf", 6.000],

		["forwardleft", 10.000],
		["left", 5.250],
		["pressf", 6.000],
		["left", 1],
		["pressf", 9.000],

	]

	currentAction = None
	currentActionFinishTime = None
	actionInProgress = False

	go = True
	while go == True:
		#Check for lost window focus
		window_is_active = window_ref.isActive
		if(window_is_active == False):
			print("INFO: Game Window not in focus. Breaking from loop.")
			return

		#Start New Action if none in progress
		if actionInProgress is False:
			now = time.time()
			currentAction = directives[directive_index][0]
			currentActionFinishTime = time.time() + directives[directive_index][1]
			actionInProgress = True
			print("INFO: Performing action [{}] for [{}] seconds.".format(currentAction, directives[directive_index][1]))

			if currentAction == "forward":
				pyautogui.keyDown('w')
			elif currentAction == "backward":
				pyautogui.keyDown('s')
			elif currentAction == "left":
				pyautogui.keyDown('a')
			elif currentAction == "right":
				pyautogui.keyDown('d')
			elif currentAction == "forwardleft":
				pyautogui.keyDown('w')
				pyautogui.keyDown('a')
			elif currentAction == "forwardright":
				pyautogui.keyDown('w')
				pyautogui.keyDown('d')
			elif currentAction == "backwardleft":
				pyautogui.keyDown('s')
				pyautogui.keyDown('a')
			elif currentAction == "backwardright":
				pyautogui.keyDown('s')
				pyautogui.keyDown('d')
			elif currentAction == "pressf":
				pyautogui.press('f')

		#Finish actions if expired
		elif time.time() >= currentActionFinishTime:
			print("INFO: Finished action [{}] after [{}] seconds.".format(currentAction, directives[directive_index][1]))

			if currentAction == "forward":
				pyautogui.keyUp('w')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "backward":
				pyautogui.keyUp('s')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "left":
				pyautogui.keyUp('a')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "right":
				pyautogui.keyUp('d')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "forwardleft":
				pyautogui.keyUp('w')
				pyautogui.keyUp('a')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "forwardright":
				pyautogui.keyUp('w')
				pyautogui.keyUp('d')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "backwardleft":
				pyautogui.keyUp('s')
				pyautogui.keyUp('a')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "backwardright":
				pyautogui.keyUp('s')
				pyautogui.keyUp('d')
				time.sleep(SLEEP_TIME_BETWEEN_ACTIONS)
			elif currentAction == "pressf":
				pass

			currentAction = None
			currentActionFinishTime = None
			actionInProgress = False

			#Increment directive_index
			directive_index = directive_index + 1
			if directive_index >= len(directives):
				directive_index = 0
				exit()

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

## Script style handler
if __name__ == '__main__':
		main()