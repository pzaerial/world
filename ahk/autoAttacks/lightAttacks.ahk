^c:: break++
^x::

break := -1
Random, attackSleepTime, 700, 800
sleepUntil := 0

while break < 0 {
    curTime := A_TickCount
    if(curtime > sleepUntil) {
        MouseClick, left
		Random, attackSleepTime, 700, 800
        sleepUntil := curTime + attackSleepTime
    }
}