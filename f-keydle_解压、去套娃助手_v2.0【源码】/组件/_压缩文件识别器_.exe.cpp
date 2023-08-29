#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h> 
//#include <windows.h>

#define	HEAD_ZONE_SIZE				512
#define	TAR_CHECKSUM_START_OFFSET	0x93
#define	TAR_CHECKSUM_END_OFFSET		0x9a

unsigned int read_in_count=0;
unsigned char global_file_buf[HEAD_ZONE_SIZE+1];

//各类文件名的特征
const struct special_character
{
	unsigned char keyword[50];
	unsigned int  file_offset;
	unsigned int  byte_num;
}
/*压缩文件的直接特征*/
zip ={"\x50\x4b",0,2},								*pzip = &zip,
gz  ={"\x1f\x8b\x08",0,3},							*pgz  = &gz,
_7z ={"\x37\x7a\xbc\xaf\x27\x1c",0,6},				*p7z  = &_7z,
rar ={"\x52\x61\x72\x21\x1a\x07",0,6},				*prar = &rar,
tar ={"\x75\x73\x74\x61\x72",0x101,5},			    *ptar = &tar,
bz2 ={"\x42\x5a\x68",0,3},						    *pbz2 = &bz2,
xz  ={"\xfd\x37\x7a\x58\x5a",0,5},					*pxz  = &xz,
//下面zpaq的两个特征只能在zpaq未加密时才有效 
zpaq_1={"7kSt",0,4},								*pzpaq_1 = &zpaq_1,
zpaq_2={"zPQ",0,3},									*pzpaq_2 = &zpaq_2,

/*其中zip需要避开的*/
office_1={"[Content_Types].xml",0x1e,19},			*poffice_1 = &office_1,
office_2={"docProps",0x1e,8},						*poffice_2 = &office_2,
office_3={"_rels",0x1e,5},							*poffice_3 = &office_3,
apk_1={"AndroidManifest.xml",0x1e,19},				*papk_1 = &apk_1,
apk_2={"META-INF",0x1e,8},							*papk_2 = &apk_2,
/*感觉下面这些有点激进了，暂时备用 
apk_3={"classes",0x1e,7},							*papk_3 = &apk_3,
apk_4={"classes",0xa2,7},							*papk_4 = &apk_4,
apk_5={"assets",0xa2,6},							*papk_5 = &apk_5,
*/
epub ={"mimetype",0x1e,8},							*pepub  = &epub//, 
;
 

//特征匹配函数 
int match(const struct special_character *pst)
{
	if ( read_in_count < (pst->file_offset)+(pst->byte_num) ) return 0;
	
	for (unsigned int i = (pst->file_offset) , j=0 , c = (pst->byte_num);
	     c>0;
		 i++,j++,c--)
	{
		if ( global_file_buf[i] != (pst->keyword)[j] ) return 0;
	}
	return 1;
}

//无符号八进制字符串转换为对应的数字 
unsigned long long U_Ochar_to_num(unsigned char *str)
{
	unsigned long long buf=0,sum=0;
	int real_char_length;
	unsigned char real_char[9];
	unsigned char *prc=real_char,*src=str;//8+1
	
	//提取非零部分 
	for (int c=8;
	     c>0;
	     c--)
	{
		if ( /* (*src) && */ (*src)>=0x30 && (*src)<=0x37 )
		{
			(*prc) = (*src);
			prc++;
		}
		src++;
	}
	real_char_length = prc - real_char;
	
	for (prc = real_char;//复位
	     real_char_length>0;
	     real_char_length--,prc++)
	{
		buf  =  (*prc)-0x30;//ANSI码转换成数字 
		buf <<= (3*(real_char_length-1));//(*2) == (<<1)，8=2^3，加权求和转换八进制字符串到数字
		sum += buf;
	}
	
	return sum;
}

//TAR校验和函数
int tar_checksum(unsigned char *buf_zone)
{
	//读入小于512字节，肯定不是tar文件 
	if (read_in_count < HEAD_ZONE_SIZE) return 0;
	
	//单元求和 
	unsigned long long compare,sum=256;//最后的256先加上了
	unsigned int i,j;
	for (i=0;i<TAR_CHECKSUM_START_OFFSET;i++)   {sum += buf_zone[i];} 
	for (i=TAR_CHECKSUM_END_OFFSET+1;i<512;i++) {sum += buf_zone[i];}
	
	//读取checksum字符段（八进制字符），然后转为数字
	unsigned char src_buf[9];//8+1
	for (i=TAR_CHECKSUM_START_OFFSET,j=0;
	     i<=TAR_CHECKSUM_END_OFFSET;
		 i++,j++)
	{
		src_buf[j] = buf_zone[i];
	}
	src_buf[j] = '\0';
	
	compare=U_Ochar_to_num(src_buf);
	//printf("%X\n",sum);printf("%X\n",compare);
	if (sum == compare || sum-0x20 == compare/*减0x20属于7zip软件的情况*/ || sum+0x20 == compare/*又发现一个新的情况*/) return 1; else return 0;
}




/* ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆ */

/* =====================================================【主函数】============================================================= */

/* ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆ */
int main(int argc,char *argv[])
{	
	int ret=0xff;
	if (argc<2) {/*printf("缺少文件路径\n"); fflush(stdout);*/ return ret;} 
	
	char ext[_MAX_EXT]={'\x00'},file_name[_MAX_FNAME]={'\x00'};
	//受保护的扩展名列表
	const char protected_ext_list[][20]=
	{
		".apk",".epub",".xps",".jar",".wmz",
		".kmz",".kwd",".odt",
		".odp",".ott",".oxps",".sxc",".sxd",
		".sxi",".sxw",".sxc",
		".xpt",".xpi",
		"【END_MARK】"
	};


	_splitpath(argv[1],NULL,NULL,file_name,ext);
	strlwr(ext);//if ((*ext)=='\x00') printf("扩展名为空");
	for (int i=0 ; strcmp(protected_ext_list[i],"【END_MARK】") ; i++)
	{
		if (!strcmp(protected_ext_list[i],ext)) return 1;//如果是上面保护的扩展名，就不继续分析文件二进制了 
	}


	//尝试读取文件头部前512字节进入内存
	FILE *fp;
	fp = fopen(argv[1],"rb");
	if (fp==NULL) return 1;
	read_in_count=fread(global_file_buf,sizeof(char),HEAD_ZONE_SIZE,fp);
	//printf("%d\n",read_in_count);
	fclose(fp);
	//if (count < HEAD_ZONE_SIZE) return -2;
	
	
	//开始匹配 
	if      (	match(prar)	)
	{
		//printf("【%s】为rar文件\n",argv[1]);
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
		//printf("【%s】为zip文件\n",argv[1]);
		ret=0;
	}
	
	
	else if (	match(p7z)	)
	{
		//printf("【%s】为7z文件\n",argv[1]);
		ret=0;
	}
	
	else if (	!strcmp(ext,".tar") || match(ptar) || tar_checksum(global_file_buf)	)
	{
		//printf("【%s】为tar文件\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pgz)	)
	{
		//printf("【%s】为gz文件\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pbz2)	)
	{
		//printf("【%s】为bz2类文件\n",argv[1]);
		ret=0;
	}
	
	else if (	match(pxz)	)
	{
		//printf("【%s】为xz文件\n",argv[1]);
		ret=0;
	}
	
	else if (	!strcmp(ext,".zpaq")	||
				match(pzpaq_1)	|| match(pzpaq_2)	)
	{
		//printf("【%s】为zpaq文件\n",argv[1]);
		ret=0;
	}
	
	else
	{
		//printf("【%s】不是常见的压缩文件\n",argv[1]);
		ret=2;
	}
	
	//fflush(stdout);
	return ret;
}
