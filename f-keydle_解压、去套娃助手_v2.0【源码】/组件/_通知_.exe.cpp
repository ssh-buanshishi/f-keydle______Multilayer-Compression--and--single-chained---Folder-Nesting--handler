/*		encoding: GB 2312

Compiled On:                   VMware Workstation 15 Pro (15.5.6 build-16341506)
Client Operating System:       Windows 7 32bit [6.1.7601]
IDE:							DEV-C++ (5.11)

*/


#include <string.h>
#include <stdlib.h>
#include <windows.h> 
#include <winuser.h>

#pragma comment(linker, "/subsystem:"windows" /entry:"mainCRTStartup"")
//VC、QT编译不弹黑窗的选项
//如果使用Dev-C++，则要在编译前打开“编译器选项”--“代码生成/优化”--“连接器”--“不产生控制台窗口”，选择“yes”

int main(int argc,char *argv[])
{
	int choice = -1;
	if (argv[1]) choice = atoi(argv[1]);
	
	switch(choice)
	{
		case 0:
			MessageBox(
				NULL,
				(LPCTSTR)"处理结束",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONINFORMATION | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“信息”图标、置顶、前台
			);
			break;

		case 1:
			MessageBox(
				NULL,
				(LPCTSTR)"路径不存在，请重试！",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“出错”图标、置顶、前台
			);
			break;

		case 2:
			MessageBox(
				NULL,
				(LPCTSTR)"读取密码配置发生错误，\n\
							请检查“配置解压密码和配置删除指定文件.txt”中的4条线，\n\
							或者尝试重置配置。",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“出错”图标、置顶、前台
			);
			break;
		
		case 3:
			MessageBox(
				NULL,
				(LPCTSTR)"转移密码文件写入时发生错误，\n\
							这种错误一般不可能发生。",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“出错”图标、置顶、前台
			);
			break;

		case 4:
			MessageBox(
				NULL,
				(LPCTSTR)"参数“origin_path”传递出错",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND//“确定”按钮、“出错”图标、置顶、前台
			);
			break;

		case 5:
			MessageBox(
				NULL,
				(LPCTSTR)"需要接受文件夹，而不是文件\n\
							请重试",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“出错”图标、置顶、前台
			);
			break;

		case 6:
			MessageBox(
				NULL,
				(LPCTSTR)"读取待删除文件配置时发生错误，\n\
							请检查“配置解压密码和配置删除指定文件.txt”中的4条线，\n\
							或者尝试重置配置。",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“出错”图标、置顶、前台
			);
			break;

		case 7:
			MessageBox(
				NULL,
				(LPCTSTR)"转移待删除文件列表写入时发生错误，\n\
							这种错误一般不可能发生。",//文本
				(LPCTSTR)"f_keydle",//标题
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //“确定”按钮、“出错”图标、置顶、前台
			);
			break;
	}

	return 0;
}
