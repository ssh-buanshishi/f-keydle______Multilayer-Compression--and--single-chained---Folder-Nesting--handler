#Requires AutoHotkey v2.0

try {
    ; 一定要先切换焦点到桌面，这样获得的屏幕大小才是真实的
    ControlFocus "SysListView321","Program Manager","FolderView"
    ; 获取当前鼠标位置，方便最后复原
    MouseGetPos &x_oringin, &y_oringin
    ; 设置X坐标移动终点为屏幕最右边
    x_target := A_ScreenWidth
    ; 从屏幕底部中间开始
    p1_x := A_ScreenWidth/2
    ; 设置距离底部高度5像素
    p1_y := A_ScreenHeight - 5
} catch Any {
    p1_x := 0
    p1_y := 0
    x_target := 0
}

; 一直向右移动鼠标光标，因为正好悬停经过右下角任务栏，所以能更新任务栏
; 用loop循环，这样能看清效果，看到鼠标向右移动的过程；直接一条命令怕直接点到点，中间一点轨迹也没有。
Loop
{
    try {
        ; 先“移”后“自加”，一开始会运动到屏幕底部中间，距离底部高度5像素的位置上，
        ; 之后一直往右移，每次移50个像素，等待1ms，继续下一次移动，直到移到最右边。
        ; 这些参数都是测试过后凑好的。
        MouseMove p1_x, p1_y, 0
        p1_x := p1_x + 50
        Sleep 1
    } catch Any {
        p1_x := p1_x + 50
        Sleep 1
    }
}
Until p1_x > x_target

try {
    ; 鼠标位置复原
    MouseMove x_oringin, y_oringin, 0
}
; 退出程序
exitapp
