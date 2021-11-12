^c:: break++
^x::

break := -1
Random, attackSleepTime, 1500, 2000
Random, waitSleepTime, 500, 750
sleepUntil := 0
chargeAttackUntil := 0
mouseDown := 0

while break < 0 {
    curTime := A_TickCount
    if (mouseDown == 0) {
        if(curtime > sleepUntil) {
            MouseClick, left,,, 1, 0, D
            Random, attackSleepTime, 1500, 2000
            chargeAttackUntil := curTime + attackSleepTime
            mouseDown := 1
        }
    } else {
        if(curtime > chargeAttackUntil) {
            MouseClick, left,,, 1, 0, U
            Random, waitSleepTime, 500, 750
            sleepUntil := curTime + waitSleepTime
            mouseDown := 0
        }
    }
}