SetWorkingDir,%A_ScriptDir%

^c:: break++
^x::

break := -1
itors := 0

isWDown := 0
timeOfLastWPress := 0
isWalking := 0

Send, {w down}

while break < 0 {

	; for testing new pictures on updates
;	ImageSearch, sickleX, axeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolHarvestingSickleOrichalcum.PNG
;	if(sickleX > 0){
;		MsgBox, sickle being used
;	}
;	ImageSearch, axeX, axeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolLoggingAxeOrichalcum.PNG
;	if(axeX > 0){
;		MsgBox, logging axe being used
;	}
;	ImageSearch, pickaxeX, axeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolPickaxeOrichalcum.PNG
;	if(pickaxeX > 0){
;		MsgBox, pickaxe being used
;	}
;	ImageSearch, knifeX, axeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolSkinningKnifeOrichalcum.PNG
;	if(knifeX > 0){
;		MsgBox, knife being used
;	}

	; press f for item pickup.
	Random, sleepTime, 50, 100
	sleep %sleepTime%
	Send, f

	; if harvesting tool is being used, wait until it has stopped being used 
	gatheredThisItor := 0
	while IsGatheringToolBeingUsed() == 1 {
		Send, {w up}
		isWalking := 0
		gatheredThisItor := 1
		Sleep 50 
	}

	; start walking if not walking, or after some time has passed.
	now = A_TickCount
	elapsedTime := now - timeOfLastWPress
	if ((gatheredThisItor == 1 and isWalking == 0) or elapsedTime > 5000) {
		Send, {w down}
		isWalking := 1
		timeOfLastWPress := now
	}

	itors := itors + 1

}

IsGatheringToolBeingUsed() {
	ImageSearch, sickleX, sickleY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolHarvestingSickleOrichalcum.PNG
	ImageSearch, axeX, axeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolLoggingAxeOrichalcum.PNG
	ImageSearch, pickaxeX, pickaxeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolPickaxeOrichalcum.PNG
	ImageSearch, knifeX, knifeY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolSkinningKnifeOrichalcum.PNG

	if(sickleX > 0 or axeX > 0 or pickaxeX > 0 or knifeX > 0){
   	    return 1
   	} else {
   		return 0
   	}
}
