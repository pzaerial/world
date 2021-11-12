SetWorkingDir,%A_ScriptDir%

^c:: break++
^x::

; Define finite state maching for the fishing loop.
; 0: Starting state.
; 1: Waiting for fish to be hooked.
; 2: Waiting for fish hooked icon to dissapear, meaning we can start reeling.
; 3: Reeling rod & waiting for reeling to be finished.
; 4: Taking actions to clear and get ready for next iteration.
state := 0

break := -1
lastReelTime := 0

while break < 0 {

	if(state = 0) {
		CastRod()
		state := 1
	} else if (state = 1) {
		if(IsFishHooked() = 1){
			state := 2
		}
	} else if (state = 2) {
		if(IsFishHooked() = 0){
			sleep 50
   	   	 	MouseClick, left
   	   	 	sleep 100
   	   	 	state := 3
		}
	} else if (state = 3) {
		ReelRod()
		state := 4
	} else if (state = 4) {
		DoCleanupActions()
		state := 0
	} else {
		state := 0
	}
}


CastRod() {
	; Enter Fishing Mode
	Send, {F3}
	sleep 1500

	; Enter Bait Select Screen
	Send, r
	sleep 1500

	; Select First Bait Option
	MouseClick, left, 1180, 450
	sleep 100
	MouseClick, left, 1500, 825
	sleep 3000

	; Cast Fishing Rod
	MouseClick, left,,, 1, 0, D
	;sleep 250
	MouseClick, left,,, 1, 0, U
}

IsFishHooked() {
	ImageSearch, OutputVarX, OutputVarY, 0, 0, A_ScreenWidth, A_ScreenHeight, fishing.PNG
    if(OutputVarX > 0){
   	    return 1
   	} else {
   	    return 0
   	}
}

ReelRod() {
	keepReeling := 1
	isKeyDown := 0
	lastReelStartTime := 0
	reelTimes := 0
	while(keepReeling = 1){
		if(IsF3PromptVisible() = 1 or reelTimes > 25){
			keepReeling := 0
			continue 
		}
		if(isKeyDown = 1){
			curTime := A_TickCount
			elapsedTime := curTime - lastReelStartTime
			if(elapsedTime > 1500 + (reelTimes * 15)) {
				MouseClick, left,,, 1, 0, U
				isKeyDown := 0
				WaitForSlackLine()
			}
		} else {
			curTime := A_TickCount
			lastReelStartTime := curTime
			MouseClick, left,,, 1, 0, D
			isKeyDown := 1
			reelTimes := reelTimes + 1
		}
	}
}

WaitForSlackLine() {

	startTime := A_TickCount
	elapsedtime := 0
	Loop {
		elapsedTime := A_TickCount - startTime
		if(IsLineSlack() = 1 or elapsedTime > 3000){
			return 	
		}
	}
}

IsLineSlack() {
	ImageSearch, lowTensionX1, lowTensionY1, 0, 0, A_ScreenWidth, A_ScreenHeight, fishinglowtension.PNG
	ImageSearch, lowTensionX2, lowTensionY2, 0, 0, A_ScreenWidth, A_ScreenHeight, fishinglowtension2.PNG
    if(lowTensionX1 > 0 or lowTensionX2 > 0){
   	    return 1
   	} else {
   	    return 0
   	}
}

IsF3PromptVisible() {
	ImageSearch, OutputVarX, OutputVarY, 0, 0, A_ScreenWidth, A_ScreenHeight, F3Prompt.PNG
    if(OutputVarX > 0){
   	    return 1
   	} else {
   	    return 0
   	}
}

DoCleanupActions() {
	; Unclick Mouse
	MouseClick, left,,, 1, 0, U

	; Exit Fishing Mode
	sleep, 3005
	MouseClick, right
	sleep, 100
	MouseClick, right
	sleep, 97
	MouseClick, right
	sleep, 105
	MouseClick, right
	sleep, 89

	; afk kick prevention with wasd
	Random, fwdBackSleepTime1, 50, 100
	Random, leftRightSleepTime1, 25, 75
	Random, fwdBackSleepTime2, 50, 100
	Random, leftRightSleepTime2, 25, 75
	Send, {w down}
	sleep fwdBackSleepTime1
	Send, {d down}
	sleep leftRightSleepTime1
	Send, {w up}
	sleep fwdBackSleepTime2
	Send, {d up}
	sleep leftRightSleepTime2
	Send, {s down}
	sleep fwdBackSleepTime1
	Send, {a down}
	sleep leftRightSleepTime1
	Send, {s up}
	sleep fwdBackSleepTime2
	Send, {a up}
	sleep leftRightSleepTime2

	sleep, 2000 
}
