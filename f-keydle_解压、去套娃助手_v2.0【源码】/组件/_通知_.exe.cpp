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
//VC��QT���벻���ڴ���ѡ��
//���ʹ��Dev-C++����Ҫ�ڱ���ǰ�򿪡�������ѡ�--����������/�Ż���--����������--������������̨���ڡ���ѡ��yes��

int main(int argc,char *argv[])
{
	int choice = -1;
	if (argv[1]) choice = atoi(argv[1]);
	
	switch(choice)
	{
		case 0:
			MessageBox(
				NULL,
				(LPCTSTR)"�������",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONINFORMATION | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť������Ϣ��ͼ�ꡢ�ö���ǰ̨
			);
			break;

		case 1:
			MessageBox(
				NULL,
				(LPCTSTR)"·�������ڣ������ԣ�",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;

		case 2:
			MessageBox(
				NULL,
				(LPCTSTR)"��ȡ�������÷�������\n\
							���顰���ý�ѹ���������ɾ��ָ���ļ�.txt���е�4���ߣ�\n\
							���߳����������á�",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;
		
		case 3:
			MessageBox(
				NULL,
				(LPCTSTR)"ת�������ļ�д��ʱ��������\n\
							���ִ���һ�㲻���ܷ�����",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;

		case 4:
			MessageBox(
				NULL,
				(LPCTSTR)"������origin_path�����ݳ���",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND//��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;

		case 5:
			MessageBox(
				NULL,
				(LPCTSTR)"��Ҫ�����ļ��У��������ļ�\n\
							������",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;

		case 6:
			MessageBox(
				NULL,
				(LPCTSTR)"��ȡ��ɾ���ļ�����ʱ��������\n\
							���顰���ý�ѹ���������ɾ��ָ���ļ�.txt���е�4���ߣ�\n\
							���߳����������á�",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;

		case 7:
			MessageBox(
				NULL,
				(LPCTSTR)"ת�ƴ�ɾ���ļ��б�д��ʱ��������\n\
							���ִ���һ�㲻���ܷ�����",//�ı�
				(LPCTSTR)"f_keydle",//����
				MB_OK | MB_ICONERROR | MB_TOPMOST | MB_SETFOREGROUND //��ȷ������ť��������ͼ�ꡢ�ö���ǰ̨
			);
			break;
	}

	return 0;
}
