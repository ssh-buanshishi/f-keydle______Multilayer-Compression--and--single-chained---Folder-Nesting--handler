# -*- coding: UTF-8 -*-

import os,sys
import argparse
import re
#import csv
import subprocess
#import win32clipboard as wcb
#import win32con
#import time

#def pause():
    #os.system("pause")
    #return

def monitor_on():
    os.chdir(currentPath)
    os.system("start \"【指定的标题】\" \"_解压成功失败检测器_.exe\"")
    os.chdir(targetPath)
    return

def monitor_off():
    ret=subprocess.run("taskkill /im \"_解压成功失败检测器_.exe\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
    if ret:
        ret=subprocess.run("taskkill /f /im \"_解压成功失败检测器_.exe\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
        if not ret:
            os.chdir(currentPath)
            os.system("start \"【指定的标题】\" /WAIT _刷新任务栏_.exe")
    os.chdir(targetPath)
    return

def transfer_password():
    readed_passwords = []
    try:
        file = open(_config_file_,mode="r",encoding="utf-8")
        buf = [a.replace("\n","") for a in file.readlines()]
        content = [a for a in buf if a]
        file.close

        switch = False
        for index in range(len(content)):
            buf = content[index]
            if buf == "------------------------ 密码起始线 ------------------------":
                start_line = index
                switch = True
            elif buf == "------------------------ 密码终止线 ------------------------":
                end_line = index
                break
            elif switch:
                readed_passwords.append(buf)
        if not (start_line and end_line): #“and(start_line < end_line)”不需要，因为如果end_line在前，不可能得到start_line
            raise Exception()
    except:
        os.chdir(currentPath)
        os.system("cd.>密码读取失败.txt")
        return False

    #未指定密码的情况，蒙一个最常用的，
    if not readed_passwords:
        readed_passwords.append("123456")

    try:
        file = open(_password_file_,mode="w",encoding="utf-8")
        file.writelines([(a+"\n") for a in readed_passwords])
        file.close()
        return True
    except:
        os.chdir(currentPath)
        os.system("cd.>密码目的地写入失败.txt")
        return False

def transfer_rm_list():
    readed_rm_list = []
    try:
        file = open(_config_file_,mode="r",encoding="utf-8")
        buf = [a.replace("\n","") for a in file.readlines()]
        content = [a for a in buf if a]
        file.close

        switch = False
        for index in range(len(content)):
            buf = content[index]
            if buf == "-------------------- 删除指定文件起始线 --------------------":
                start_line = index
                switch = True
            elif buf == "-------------------- 删除指定文件终止线 --------------------":
                end_line = index
                break
            elif switch:
                readed_rm_list.append(buf)
        if not (start_line and end_line): #“and(start_line < end_line)”不需要，因为如果end_line在前，不可能得到start_line
            raise Exception()
    except:
        os.chdir(targetPath)
        os.system("cd.>_rm_list_.txt")
        return False

    try:
        file = open(_rm_list_file_,mode="w",encoding="utf-8")
        if readed_rm_list:
            file.writelines([(a+"\n") for a in readed_rm_list])
        file.close()
    except:
        os.chdir(targetPath)
        os.system("cd.>_rm_list_.txt")
        return False
    return True



def get_remove_list():
    readed_remove_list = []
    if os.path.exists(_rm_list_file_):
        file = open(_rm_list_file_,mode="r",encoding="utf-8")
        buf = [a.replace("\n","") for a in file.readlines()]
        readed_remove_list = [a for a in buf if a]
        file.close
    else:    
        try:
            file = open(_config_file_,mode="r",encoding="utf-8")
            buf = [a.replace("\n","") for a in file.readlines()]
            content = [a for a in buf if a]
            file.close

            switch = False
            for index in range(len(content)):
                buf = content[index]
                if buf == "-------------------- 删除指定文件起始线 --------------------":
                    start_line = index
                    switch = True
                elif buf == "-------------------- 删除指定文件终止线 --------------------":
                    end_line = index
                    break
                elif switch:
                    readed_remove_list.append(buf)
            if not (start_line and end_line): #“and(start_line < end_line)”不需要，因为如果end_line在前，不可能得到start_line
                raise Exception()
        except:
            readed_remove_list.clear()

    return readed_remove_list

def delete_specific_files(recursion):
    remove_list = get_remove_list()
    os.chdir(targetPath)
    if remove_list:
        for file in remove_list:
            if recursion == True:
                os.system("del /f /s /q " + "\""+file+"\"")
            else:
                #递归为否的情况下，保护批处理自身不被删
                os.system("for \u0025i in (" + "\""+file+"\"" + ") do (if \"%~xi\" NEQ \".bat\" (del /f /q \"%~nxi\"))")
    return



def get_files():
    os.chdir(targetPath)
    return [element for element in os.listdir() if os.path.isfile(element)]

def get_password_list():
    try:
        #os.chdir(targetPath)
        file = open(_password_file_,mode="r",encoding="utf-8")
        buf = [a.replace("\n","") for a in file.readlines()]
        content = [a for a in buf if a]
        file.close
    except:
        content = []
    return content



def transfer_curpath_for_detector():
    os.chdir(_detector_path_)
    file = open("_current_path_.txt",mode="w",encoding="utf-8")
    file.writelines([targetPath+"\n"])
    file.close
    os.chdir(targetPath)

def clean_barrier():
    os.chdir(targetPath)
    #去除扩展名中的多余字符（为了防止资源被和谐）产生的干扰
    for text in _origin_file_list_:
        split = os.path.splitext(text)
        name = split[0]
        ext = split[1]
        ext = ext.replace(".","",1)#去掉点

        if ext == "【_解压失败_】":
            continue

        #受保护的文件扩展名（小写），里面含有非字母数字成分
        protected_ext_list=["search-ms","linux_amd64_asm","dvr-ms"]

        state = 0
        for i in protected_ext_list:
            if ext.lower() == i:
                state = 1
                break
        #如有，则不进行下去了，换下一个文件名
        if state == 1:
            continue

        result = ""
        char_counted_in = 0

        if name and ext:
            for char in ext:
                #收纳正常字母数字
                if ('0' <= char <= '9') or ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                    result += char
                    char_counted_in += 1
                #转换全角字母数字
                elif ('０' <= char <= '９') or ('Ａ' <= char <= 'Ｚ') or ('ａ' <= char <= 'ｚ'):
                    result += chr(ord(char) - 65248)
                    char_counted_in += 1
            result = result.lower()
            name = name.replace("\u00a0","\u0020")#替换不间断空格
            name = name.replace("\u3000","\u0020")#替换全角空格
            if (name+"."+result) != text:
                num = 1
                if char_counted_in > 0:
                    new_fname = name+"."+result
                    while (os.path.exists(new_fname)):
                        new_fname = name + "(" + str(num).zfill(5) + ")" +"."+result
                        num += 1
                    os.rename(text,new_fname)
                else:
                    new_fname = name
                    while (os.path.exists(new_fname)):
                        new_fname = name + "(" + str(num).zfill(5) + ")"
                        num += 1
                    os.rename(text,new_fname)

        #以点开头，只有扩展名的情况（例如文件名为：".zip"，这也是允许的）
        elif re.match('^[.][^.]+$',text):
            for char in text:
                #收纳正常字母数字
                if ('0' <= char <= '9') or ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                    result += char
                    char_counted_in += 1
                #转换全角字母数字
                elif ('０' <= char <= '９') or ('Ａ' <= char <= 'Ｚ') or ('ａ' <= char <= 'ｚ'):
                    result += chr(ord(char) - 65248)
                    char_counted_in += 1
            result = result.lower()
            result = result.replace("\u00a0","\u0020")#替换不间断空格
            result = result.replace("\u3000","\u0020")#替换全角空格
            if result != text:
                num = 1
                if char_counted_in > 0:
                    new_fname = "无名文件"+"."+result
                    while (os.path.exists(new_fname)):
                        new_fname = "无名文件" + "(" + str(num).zfill(5) + ")" +"."+result
                        num += 1
                    os.rename(text,new_fname)
                else:
                    new_fname = "无名文件"+"."+"未知类型"
                    while (os.path.exists(new_fname)):
                        new_fname = "无名文件" + "(" + str(num).zfill(5) + ")" +"."+"未知类型"
                        num += 1
                    os.rename(text,new_fname)
    #无返回值
    return



def get_rar_sep_vol_fname(input_string):
    buf = input_string
    buf = os.path.splitext(buf)[0]
    buf = os.path.splitext(buf)[0]
    return buf

def get_other_sep_vol_fname(input_string):
    buf = input_string
    buf = os.path.splitext(buf)[0]
    return buf

def get_sep_vol_fgroup(mode):
    #分配pattern
    if mode == "rar":
        pattern = r".+[.]part\d+[.]rar$"
    elif mode == "zip":
        pattern = r".+[.]z\d+$|.+[.]zip$"
    elif mode == "zipx":
        pattern = r".+[.]zx\d+$|.+[.]zipx$"
    elif mode == "001":
        pattern = r".+[.]\d+$"
    elif mode == "rar_old":
        pattern = r".+[.]r\d+$"
    else:
        return []   #类型错误

    filter_1 = [element for element in _origin_file_list_ if re.match(pattern,element)]
    filter_2 = []
    filter_3 = []
    if filter_1:

        filter_1.sort()
        #print(filter_1)

        list_buf = []
        #竖起第一组文件的“标杆”beginner
        if mode == "rar":
            beginner = get_rar_sep_vol_fname(filter_1[0])
        else:
            beginner = get_other_sep_vol_fname(filter_1[0])
        
        for pointer in range(len(filter_1)):
            str_buf_1 = filter_1[pointer]                       #str_buf_1：完整文件名
            if mode == "rar":
                str_buf_2 = get_rar_sep_vol_fname(str_buf_1)    #str_buf_2：去掉".partXXX.rar"后的真实文件名
            else:
                str_buf_2 = get_other_sep_vol_fname(str_buf_1)
            
            if str_buf_2 == beginner:
                list_buf.append(str_buf_1)
            else:
                filter_2.append([element for element in list_buf])      #文件名变化，此时一组相同文件的list_buf已装完，添加进二维数组filter_2
                #一定是得这样写，不然append(buf_list)添加进二维数组的就是list_buf这个对象，而不是其中的成员
                #，list_buf一变，之前添加进二维数组里的元素也跟着变

                list_buf.clear()                                        #重置list_buf
                list_buf.append(str_buf_1)                              #list_buf装入新一组文件的第一个
                beginner = str_buf_2                                    #更换下一组文件的“标杆”
        filter_2.append([element for element in list_buf])              #还有最后一组文件未在循环中装入最终的filter_2，这一句补上

        filter_3 = [element for element in filter_2 if len(element)>1]
    #返回
    return filter_3



def extracted_successfully():
    #解压失败成功检测器留在“组件”目录
    os.chdir(currentPath)
    ret=subprocess.run("find \"release_error_\" \"_checker_record_.txt\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
    os.system("cd.>_checker_record_.txt")
    if ret:
        return True
    else:
        return False

def is_compressed(file):
    os.chdir(targetPath)
    ret=subprocess.run("_压缩文件识别器_.exe " + "\""+file+"\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
    if not ret:
        return True
    elif ret == 1:
        new_fname = "_t_a_r_g_e_t_.bin"
        os.rename(file,new_fname)
        ret=subprocess.run("_压缩文件识别器_.exe " + "\""+new_fname+"\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
        os.rename(new_fname,file)
        if not ret:
            return True
        else:
            return False
    else:
        return False

#另一种可行的方法，不过还是舍弃了
#def paste_commmand_and_run(file,password):
    #os.chdir(currentPath)
    #os.system("start \"【标题】\" _命令粘贴助手_.exe")

    #command = "cls&&echo 【解压窗口，勿关】&&start \"titile\" /wait " + "\""+_bandizip_+"\"" +" x -aou -p:" +"\""+password+"\""+ " -target:auto "+"\""+file+"\""+"&&exit"
    #wcb.OpenClipboard()
    #wcb.EmptyClipboard()
    #wcb.SetClipboardData(win32con.CF_UNICODETEXT, command)
    #wcb.CloseClipboard()
    
    #time.sleep(0.25)
    #os.system("start \"【解压窗口，勿关】\" /D "+"\""+targetPath+"\""+" /WAIT cmd_2.exe")
    #return
    



def extract_single_file(file):
    status = False
    try:
        for password in _password_list_:
            os.chdir(_detector_path_)
            os.system("start \"【无标题】\" /min /wait detector.exe r .\\_current_path_.txt _folder_names_record_.txt")
            
            #下面是另一种可行的方法，不过还是舍弃了
            #paste_commmand_and_run(file,password)
            
            os.chdir(targetPath)
            os.system("start \"titile\" /wait " + "\""+_bandizip_+"\"" +" x -aou -p:" +"\""+password+"\""+ " -target:auto "+"\""+file+"\"")
        
            if extracted_successfully():
                status = True
                break
            else:
                os.chdir(_detector_path_)
                os.system("start \"【无标题】\" /min /wait detector.exe d .\\_current_path_.txt _folder_names_record_.txt")
    except:
        os.chdir(targetPath)
        return status
    
    os.chdir(targetPath)
    return status



def mark(fname):
    buf = fname.replace(".","【_dot_】")
    buf = "【_解压失败_】"+buf+"【_解压失败_】.【_解压失败_】"
    return buf


def protect_mark(fname):
    buf = fname.replace(".","【_dot_】")
    buf = "【_保护_】"+buf+"【_保护_】.【_保护_】"
    return buf

def extract_single_fgroup_list(fg_list,mode):
    if mode == "zip":
        entry = -1
    else:
        entry = 0
    
    for group in fg_list:
        ret = extract_single_file(group[entry])
        os.chdir(targetPath)
        if ret:
            for file in group:
                os.remove(file)
        else:
            for file in group:
                os.rename(file,mark(file))
    
    return


def extra_sep_vol_files():
    for pattern in ["rar","zip","zipx","001","rar_old"]:
        buf_list = get_sep_vol_fgroup(pattern)
        if buf_list:
            extract_single_fgroup_list(buf_list,pattern)
    return

def extra_single_files():
    for file in _origin_file_list_:
        ext_buf = os.path.splitext(file)[1]
        if ((ext_buf == ".【_解压失败_】") or (file == "_origin_path_.txt") or (file == "_password_.txt") or (file == "_rm_list_.txt")
                or (file == "_child_excuter_1.bat") or (file == "_folder_names_record_.txt") or (file == "_压缩文件识别器_.exe")):
            continue
        elif is_compressed(file):
            ret = extract_single_file(file)
            os.chdir(targetPath)
            if ret:
                os.remove(file)
            else:
                os.rename(file,mark(file))
    return



def protect_mark_single_files():
    os.chdir(targetPath)
    for file in _origin_file_list_:
        ext_buf = os.path.splitext(file)[1]
        if ((ext_buf == ".【_保护_】") or (file == "_origin_path_.txt") or (file == "_rm_list_.txt")
                or (file == "_child_excuter_4.bat") or (file == "_压缩文件识别器_.exe")):
            continue
        elif is_compressed(file):
            os.rename(file,protect_mark(file))
    return


def protect_mark_single_fgroup_list(fg_list):
    os.chdir(targetPath)
    for group in fg_list:
        for file in group:
            os.rename(file,protect_mark(file))
    return


def protect_mark_sep_vol_fgroups():
    for pattern in ["rar","zip","zipx","001","rar_old"]:
        buf_list = get_sep_vol_fgroup(pattern)
        if buf_list:
            protect_mark_single_fgroup_list(buf_list)
    return




parser = argparse.ArgumentParser()
parser.add_argument("mode",type=int)
parser.add_argument("path",type=str)
args = parser.parse_args()

os.chdir("..")
#记录当前目录
currentPath = os.getcwd()
#记录目标目录
targetPath  = args.path

#配置各项信息
_bandizip_       = currentPath+"\\"+"BandizipPro_portable"+"\\"+"Bandizip.exe"
#_zip_identifier_ = currentPath+"\\"+"_压缩文件识别器_.exe"
_config_file_    = currentPath+"\\"+"配置解压密码和配置删除指定文件.txt"
#_detector_       = currentPath+"\\"+"detector"+"\\"+"detector.exe"
_detector_path_  = currentPath+"\\"+"detector"
_password_file_  = targetPath +"\\"+"_password_.txt"
_rm_list_file_   = targetPath +"\\"+"_rm_list_.txt"

_mode_ = args.mode
if _mode_ == 0:
    transfer_password()
    transfer_rm_list()
    sys.exit(0)

elif _mode_ == 2:
    delete_specific_files(True)
    sys.exit(0)

elif _mode_ == 3:
    delete_specific_files(False)
    sys.exit(0)

elif _mode_ == 4:
    transfer_rm_list()
    sys.exit(0)

elif _mode_ == 5:
    #获取文件列表
    _origin_file_list_ = get_files()
    if not _origin_file_list_:
        sys.exit(0)
    
    protect_mark_sep_vol_fgroups()
    #刷新文件列表
    _origin_file_list_ = get_files()

    protect_mark_single_files()

    sys.exit(0)

elif _mode_ == 1:
    #获取文件列表
    _origin_file_list_ = get_files()
    if not _origin_file_list_:
        sys.exit(0)
    
    #打开“_解压成功失败检测器_.exe”
    monitor_on()

    #准备密码列表
    _password_list_ = get_password_list()
    #传送当前压缩文件所在位置给detector
    transfer_curpath_for_detector()
    #去除扩展名中的多余字符（为了防止资源被和谐）产生的干扰
    clean_barrier()


    #刷新文件列表
    _origin_file_list_ = get_files()
    #先尝试解压分卷压缩文件
    extra_sep_vol_files()
    #刷新文件列表
    _origin_file_list_ = get_files()
    #再解决剩下来的单个文件
    extra_single_files()

    #关闭“_解压成功失败检测器_.exe”
    monitor_off()
    
    sys.exit(0)

else:
    sys.exit(0)
