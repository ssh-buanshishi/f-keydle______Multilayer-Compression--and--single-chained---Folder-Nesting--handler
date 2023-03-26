#Requires AutoHotkey v2.0
SetControlDelay 0
SetWinDelay 0
; 编码设置为UTF-8，用以适应特殊符号
FileEncoding("UTF-8")
; 将当前目录的绝对路径写入【_current_path_.txt】
FileAppend A_WorkingDir, A_WorkingDir "\_current_path_.txt"
; 编码设置为ANSI，用以适应.bat批处理搜索此程序记录下的“release_error_”时的需要。
FileEncoding("")
; 输出解压错误信号的txt位置在当前目录的【_checker_record_.txt】
output_file := A_WorkingDir "\_checker_record_.txt"
; 变量tmp用以存放抓取到的bandizip输出的解压报告，初始化为"_none_"
tmp := "_none_"
; 下面是两个解压错误信息关键字
target_string_1 := "错误"
target_string_2 := "error"

; 整个解压过程需要解压N个文件，一直开在那监视bandizip的动作比较好，结束时由批处理结束进程。
Loop
{
    ; 检测到bandizip启动
    if WinActive("ahk_exe Bandizip.exe")
    {
        ; 这里让你输密码说明失败了，因为密码在批处理中已经分配好了。
        if WinExist("输入密码") or WinExist("Enter Password")
        {
            try
            {
                ; 将失败信号记录到txt（写文件命令在前面，这样关闭bandizip以后批处理就不会因为此程序还没写入错误信息出错）
                FileAppend "release_error_", output_file
                ; 激活密码输入窗口，并点击“取消”（"Button2"控件）按钮关闭密码输入窗口
                WinActive("输入密码")
                WinActive("Enter Password")
                ControlClick "Button2"
                ; 略微延迟一点实际，再激活仅剩的解压进度信息窗口，点击“关闭”（"Button2"控件）关掉它。
                Sleep 10
                WinActive("ahk_exe Bandizip.exe")
                ControlClick "Button2"
                ; 错误已经处理，不需要读取
                tmp := "_none_"
            }

        }
        else
        {
            ; 如果没有跳出密码输入窗口，尝试抓取bandizip输出的解压报告（在"RICHEDIT50W1"控件里）
            ; 如果控件没有跳出来（catch any的部分），给一个“空”的值，下面instr就不会因为变量没赋值而报错。
            Try
            {
                tmp := ControlGetText("RICHEDIT50W1")
            } catch Any {
                tmp := "_none_"
            }   
        }
    }
    else
    {
        ; bandizip没启动时，tmp维持重置状态。
        tmp := "_none_"
    }

    ; 如果抓到的解压报告里搜索到“错误”或“error”，说明解压失败
    if InStr(tmp,target_string_1) or InStr(tmp,target_string_2)
    {
        ; 及时重置变量，防止下一次循环误判
        tmp := "_none_"
        Try
        {
            ; 将失败信号记录到txt（写文件命令在前面，这样关闭bandizip以后批处理就不会因为此程序还没写入错误信息出错）
            FileAppend "release_error_", output_file
            ; 激活解压进度信息窗口，点击“关闭”（"Button2"控件）关掉它。
            WinActive("ahk_exe Bandizip.exe")
            ControlClick "Button2"
        }
    }
}