SetWorkingDir,%A_ScriptDir%

^c:: break++
^x::

break := -1
itors := 0

last := A_TickCount

while break < 0 {
	;Press F to Pick Up
	;if(IsPressFPromptVisible()){
	;	Random, sleepTime, 505, 1000
	;	sleep %sleepTime%
	;	Send, f
	;}

	;Alternate Press F
	Random, sleepTime, 505, 1000
	sleep %sleepTime%
	Send, f

	now := A_TickCount
	elapsedTime := now - last
	last := now
	Random, sleepTime, 250000, 500000
	if(elapsedTime > sleepTime){
		AfkPrevention()
	}

	itors := itors + 1
}


IsPressFPromptVisible() {
   	ImageSearch, fx, fy, 0, 0, A_ScreenWidth, A_ScreenHeight, pressFPrompt.PNG
   	if(fx){
   	    return 1
   	} else {
   		return 0
   	}
}

AfkPrevention() {
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
}
