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
;	ImageSearch, promptX, promptY, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolSkinningKnifeOrichalcum.PNG
;	if(promptX <= 0){
;		MsgBox, prompt is not there anymore
;	}
;	ImageSearch, promptX, promptY, 0, 0, A_ScreenWidth, A_ScreenHeight, yellowWeaponLock.PNG
;	if(promptX <= 0){
;		MsgBox, Yellow lock prompt is not there
;	}
;	return


	; press f for item pickup.
	Random, sleepTime, 50, 100
	sleep %sleepTime%
	Send, f

	; if harvesting tool is being used, wait until it has stopped being used 
	gatheredThisItor := 0
	while IsUiInGatheringMode() == 1 {
		Send, {w up}
		isWalking := 0
		gatheredThisItor := 1
		Sleep 50 
	}

	; start walking if not walking, or after some time has passed.
	now := A_TickCount
	elapsedTime := now - timeOfLastWPress
	if ((gatheredThisItor == 1 and isWalking == 0) or elapsedTime > 5000) {
		Send, {w down}
		isWalking := 1
		timeOfLastWPress := now
	}

	itors := itors + 1

}

;Gathers when part of UI dissapears while starting a mining/collecting action.
IsUiInGatheringMode() {
	ImageSearch, promptX, promptY, 0, 0, A_ScreenWidth, A_ScreenHeight, yellowWeaponLock.PNG
	if(promptX <= 0){
		return 1
	}
	return 0
}


;old implementation, unused
IsGatheringToolBeingUsed() {
	;ImageSearch, axeXStone, axeYStone, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolLoggingAxeStone.PNG
	;ImageSearch, pickaxeXStone, pickaxeYStone, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolPickaxeStone.PNG
	;ImageSearch, knifeXStone, knifeYStone, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolSkinningKnifeStone.PNG

	;ImageSearch, sickleXOrichalcum, sickleYOrichalcum, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolHarvestingSickleOrichalcum.PNG
	;ImageSearch, axeXOrichalcum, axeYOrichalcum, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolLoggingAxeOrichalcum.PNG
	;ImageSearch, pickaxeXOrichalcum, pickaxeYOrichalcum, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolPickaxeOrichalcum.PNG
	;ImageSearch, knifeXOrichalcum, knifeYOrichalcum, 0, 0, A_ScreenWidth, A_ScreenHeight, gatheringToolSkinningKnifeOrichalcum.PNG

	;if(axeXStone or pickaxeXStone or knifeXStone or sickleXOrichalcum or axeXOrichalcum or pickaxeXOrichalcum or knifeXOrichalcum){
   	;    return 1
   	;} else {
   	;	return 0
   	;}


   	ImageSearch, promptX, promptY, 0, 0, A_ScreenWidth, A_ScreenHeight, weaponXPrompt.PNG
   	if(promptX){
   	    return 0
   	} else {
   		return 1
   	}
}
