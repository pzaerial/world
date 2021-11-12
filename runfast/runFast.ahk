^c:: break++
Send {w up}
return

^x::
break := -1
Send {w down}
last := A_TickCount
Random, delay, 2400, 3000
while break < 0 {
	time := A_TickCount
	diff := time - last
	if (diff > delay) {
		Send {LShift}
		Random, delay, 100, 125
		Sleep delay
		Send x
		Send {w up}
		Random, delay, 10, 50
		Sleep delay
		Send {w down}
		last := A_TickCount
		Random, delay, 2400, 3000
	}
}
