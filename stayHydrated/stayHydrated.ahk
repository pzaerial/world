^c:: break++
^x::

break := -1

msBetweenFPresses := 1800
msBetweenAfkPrevention := 240000

lastPress := A_TickCount
lastAfkPrevention := A_TickCount

sleep 1000
windowTitle=New World
WinActivate %windowTitle%
sleep 1000


while break < 0 {
	now := A_TickCount

	;Press F at a certain interval to pick up water.
	if(now - lastPress > msBetweenFPresses){
		Send, f
		lastPress := now
	}

	;Move at a certain interval to prevent being kicked for inactivity
	if(now - lastAfkPrevention > msBetweenAfkPrevention) {
		AfkPrevention()
		lastAfkPrevention := now
	}
}


AfkPrevention() {
	;Let any current actions finish
	Sleep, msBetweenFPress

	Random, sleepTime, 50, 100

	Send, {d down}
	sleep sleepTime
	Send, {d up}
	sleep 500
	Send, {a down}
	sleep sleepTime
	Send, {a up}
}
