/*		encoding: GB 2312

Compiled On:                   VMware Workstation 15 Pro (15.5.6 build-16341506)
Client Operating System:       Windows 7 32bit [6.1.7601]
IDE:							DEV-C++ (5.11)

*/


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h> 
//#include <windows.h>

#define	HEAD_ZONE_SIZE				512
#define	TAR_CHECKSUM_START_OFFSET	0x93
#define	TAR_CHECKSUM_END_OFFSET		0x9a

unsigned int _read_in_count_ = 0;
unsigned char _file_buf_main_[HEAD_ZONE_SIZE+1] = {'\0'};
char _file_buf_for_iso_[3][6] = {'\0'};/*��CD001����ʶ����5+1������ƫ�Ƶ�ַ*/

//�����ļ���������
const struct special_character
{
	unsigned char keyword[50];
	unsigned int  file_offset;
	unsigned int  byte_num;
}
/*ѹ���ļ���ֱ������*/
zip ={"\x50\x4b",0,2},								*pzip = &zip,
gz  ={"\x1f\x8b\x08",0,3},							*pgz  = &gz,
_7z ={"\x37\x7a\xbc\xaf\x27\x1c",0,6},				*p7z  = &_7z,
rar ={"\x52\x61\x72\x21\x1a\x07",0,6},				*prar = &rar,
tar ={"\x75\x73\x74\x61\x72",0x101,5},			    *ptar = &tar,
bz2 ={"\x42\x5a\x68",0,3},						    *pbz2 = &bz2,
xz  ={"\xfd\x37\x7a\x58\x5a",0,5},					*pxz  = &xz,
wim ={"\x4d\x53\x57\x49\x4d",0,5},					*pwim = &wim,
//����zpaq����������ֻ����zpaqδ����ʱ����Ч 
zpaq_1={"7kSt",0,4},								*pzpaq_1 = &zpaq_1,
zpaq_2={"zPQ",0,3},									*pzpaq_2 = &zpaq_2,

/*����zip��Ҫ�ܿ���*/
office_1={"[Content_Types].xml",0x1e,19},			*poffice_1 = &office_1,
office_2={"docProps",0x1e,8},						*poffice_2 = &office_2,
office_3={"_rels",0x1e,5},							*poffice_3 = &office_3,
apk_1={"AndroidManifest.xml",0x1e,19},				*papk_1 = &apk_1,
apk_2={"META-INF",0x1e,8},							*papk_2 = &apk_2,
/*�о�������Щ�е㼤���ˣ���ʱ���� 
apk_3={"classes",0x1e,7},							*papk_3 = &apk_3,
apk_4={"classes",0xa2,7},							*papk_4 = &apk_4,
apk_5={"assets",0xa2,6},							*papk_5 = &apk_5,
*/
epub ={"mimetype",0x1e,8},							*pepub  = &epub//, 
;
 

//����ƥ�亯������ǰ512�ֽڡ�_file_buf_main_���еģ�
int match(const struct special_character *pst)
{
	if ( _read_in_count_ < (pst->file_offset)+(pst->byte_num) ) return 0;
	
	for (unsigned int i = (pst->file_offset) , j=0 , c = (pst->byte_num);
	     c>0;
		 i++,j++,c--)
	{
		if ( _file_buf_main_[i] != (pst->keyword)[j] ) return 0;
	}
	return 1;
}

//isoƥ�亯��
int match_iso()
{
	/*
	for (char i = 0; i < 3; i++)
	{
		
		printf("%d��",i);
		for (char j=0;j<6;j++)
		{
			printf("%x ",_file_buf_for_iso_[i][j]);
		}
		printf("\n");
		
	}
	*/
	for (char i = 0; i < 3; i++)
	{
		if ( !memcmp(_file_buf_for_iso_[i],"CD001",5) ) return 1;
	}

	return 0;	
}


//�޷��Ű˽����ַ���ת��Ϊ��Ӧ������ 
unsigned int U_Ochar_to_num(unsigned char *str)
{
	unsigned int buf=0,sum=0;
	int real_char_length;
	unsigned char real_char[9]={'\0'};//8+1
	unsigned char *dest=real_char,*src=str;
	
	//��ȡ���㲿�� 
	for (char c=8;
	     c>0;
	     c--)
	{
		if ( /* (*src) && */ (*src)>=0x30 && (*src)<=0x37 )
		{
			(*dest) = (*src);
			dest++;
		}
		src++;
	}
	real_char_length = dest - real_char;
	
	for (dest = real_char;//��λ
	     real_char_length>0;
	     real_char_length--,dest++)
	{
		buf  =  (*dest)-0x30;//ANSI��ת�������� 
		buf <<= (3*(real_char_length-1));//(*2) == (<<1)��8=2^3����Ȩ���ת���˽����ַ���������
		sum += buf;
	}
	
	return sum;
}

//TARУ��ͺ���
int tar_checksum()
{
	//����С��512�ֽڣ��϶�����tar�ļ� 
	if (_read_in_count_ < HEAD_ZONE_SIZE) return 0;
	
	//��Ԫ��� 
	unsigned int compare,sum=256;//����256�ȼ�����
	unsigned int i,j;
	for (i=0;i<TAR_CHECKSUM_START_OFFSET;i++)   {sum += _file_buf_main_[i];} 
	for (i=TAR_CHECKSUM_END_OFFSET+1;i<512;i++) {sum += _file_buf_main_[i];}
	
	//��ȡchecksum�ַ��Σ��˽����ַ�����Ȼ��תΪ����
	unsigned char src_buf[9];//8+1
	for (i=TAR_CHECKSUM_START_OFFSET,j=0;
	     i<=TAR_CHECKSUM_END_OFFSET;
		 i++,j++)
	{
		src_buf[j] = _file_buf_main_[i];
	}
	src_buf[j] = '\0';
	
	compare=U_Ochar_to_num(src_buf);
	//printf("%X\n",sum);printf("%X\n",compare);
	if (sum      == compare 
	 || sum-0x20 == compare/*��0x20����7zip��������*/ 
	 || sum+0x20 == compare/*�ַ���һ���µ����*/) return 1; else return 0;
}




/* ��������������������������������������������������������������� */

/* ================================================����������======================================================== */

/* ��������������������������������������������������������������� */
int main(int argc,char *argv[])
{	
	int ret=0xff;
	if (argc<2) {/*printf("ȱ���ļ�·��\n"); fflush(stdout);*/ return ret;} 
	
	//�����չ��
	char ext[_MAX_EXT]={'\0'};
	_splitpath(argv[1],NULL,NULL,NULL,ext);
	strlwr(ext);//��չ��תСд


	//�ܱ�������չ���б�
	const char protected_ext_list[][20]=
	{
		".apk",".epub",".xps",".jar",".wmz",
		".kmz",".kwd",".odt",
		".odp",".ott",".oxps",".sxc",".sxd",
		".sxi",".sxw",".sxc",
		".xpt",".xpi",
		"��END_MARK��"
	};

	for (int i=0 ; strcmp(protected_ext_list[i],"��END_MARK��") ; i++)
	{
		if (!strcmp(ext,protected_ext_list[i])) return 3;//��������汣������չ�����Ͳ����������ļ��������� 
	}



	//���Զ�ȡ�ļ�ͷ��ǰ512�ֽڽ����ڴ�
	FILE *fp;
	fp = fopen(argv[1],"rb");
	if (fp==NULL) return 1;

	_read_in_count_=fread(_file_buf_main_,sizeof(char),HEAD_ZONE_SIZE,fp);
	//printf("%d\n",_read_in_count_);

	//���Զ�ȡiso�ļ���־������������CD001����offset��0x8001��0x8801��0x9001��
	if ( !fseek(fp,0x8001L,SEEK_SET) ) { fread(_file_buf_for_iso_[0],sizeof(char),5,fp); }

	if ( !fseek(fp,0x8801L,SEEK_SET) ) { fread(_file_buf_for_iso_[1],sizeof(char),5,fp); }

	if ( !fseek(fp,0x9001L,SEEK_SET) ) { fread(_file_buf_for_iso_[2],sizeof(char),5,fp); }


	//���뻺�������ļ����ò����ˣ��ص�
	fclose(fp);
	//if (count < HEAD_ZONE_SIZE) return -2;
	
	
	//��ʼƥ�� 
	if      (	match(prar)	)
	{
		//printf("��%s��Ϊrar�ļ�\n",argv[1]);
		ret=0;
	}
	
	
	else if ( 
				match(pzip) &&
	        	!(
						match(poffice_1)	||	match(poffice_2)	||	match(poffice_3)
					||	match(papk_1) 		||	match(papk_2)		/*||	match(papk_3)		||	match(papk_4)	||	match(papk_5)*/
					||	match(pepub)
				 )
	        )
	{
		//printf("��%s��Ϊzip�ļ�\n",argv[1]);
		ret=0;
	}
	
	
	else if (	match(p7z)	)
	{
		//printf("��%s��Ϊ7z�ļ�\n",argv[1]);
		ret=0;
	}
	
	else if (	!strcmp(ext,".tar") || match(ptar) || tar_checksum()	)
	{
		//printf("��%s��Ϊtar�ļ�\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pgz)	)
	{
		//printf("��%s��Ϊgz�ļ�\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pbz2)	)
	{
		//printf("��%s��Ϊbz2���ļ�\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pxz)	)
	{
		//printf("��%s��Ϊxz�ļ�\n",argv[1]);
		ret=0;
	}
	
	else if (	match_iso()	)
	{
		//printf("��%s��Ϊiso�ļ�\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pwim)	)
	{
		//printf("��%s��Ϊwim�ļ�\n",argv[1]);
		ret=0;
	}

	else if (	!strcmp(ext,".zpaq")	||
				match(pzpaq_1)	|| match(pzpaq_2)	)
	{
		//printf("��%s��Ϊzpaq�ļ�\n",argv[1]);
		ret=0;
	}
	
	else
	{
		//printf("��%s�����ǳ�����ѹ���ļ�\n",argv[1]);
		ret=2;
	}
	
	//fflush(stdout);
	return ret;
}
