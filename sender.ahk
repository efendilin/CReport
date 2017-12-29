;
; AutoHotkey Version: 1.x
; Language:       English
; Platform:       Win9x/NT
; Author:         A.N.Other <myemail@nowhere.com>
;
; Script Function:
;	Template script (you can customize this template by editing "ShellNew\Template.ahk" in your Windows folder)
;

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

sleep, 50
stdout := FileOpen("*", "r")  
Text := stdout.read()
;Text := Clipboard
Text_array := StrSplit(Text, "IamSep")

IfWinNotExist, UniReport
{
	MsgBox, The UniReport is not exist
	return
}
WinGetTitle, TITLE, UniReport
StringGetPos, pos, TITLE, ID
If pos = -1
{
	MsgBox, You are not in edit windows
	Return
}
StringMid, PID, TITLE, pos + 6, 8
IfEqual, PID,,return
test := PID - Text_array[6]

If test = 0
{
	if Text_array[1]{
		ControlSetText, TMemo2, % Text_array[1], UniReport
	}
	if Text_array[2]{
		ControlSetText, TMemo3, % Text_array[2], UniReport
	}
	if Text_array[3]{
		ControlSetText, TMemo4, % Text_array[3], UniReport
	}
	if Text_array[4]{
		ControlSetText, Edit3, % Text_array[4], UniReport
	}
	if Text_array[5]{
		ControlSetText, Edit2, % Text_array[5], UniReport
	}
}else
{
	MsgBox, You past to wrong guy !!!!
}


