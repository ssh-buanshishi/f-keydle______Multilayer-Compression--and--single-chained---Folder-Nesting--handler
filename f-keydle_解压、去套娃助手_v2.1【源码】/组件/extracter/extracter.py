# -*- coding: UTF-8 -*-

#Compiled On:                   VMware Workstation 15 Pro (15.5.6 build-16341506)
#Client Operating System:       Windows 7 32bit [6.1.7601]
#Python Version:                python 3.8.6(32bit)
#Nuitka Version:                2.2.2


import os,sys
import argparse
import re
import subprocess


#打开“解压成功失败检测器”
def monitor_on() -> None:
    os.chdir(_currentPath_)
    os.system("start \"【指定的标题】\" \"_解压成功失败检测器_.exe\"")

    #无返回值
    return


#关闭“解压成功失败检测器”
def monitor_off() -> None:
    #先尝试正常发送结束信号给“_解压成功失败检测器_.exe”
    ret=subprocess.run("taskkill /im \"_解压成功失败检测器_.exe\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode

    #如果返回不为零，说明正常结束失败
    if ret:
        #尝试强制结束
        os.system("taskkill /f /im \"_解压成功失败检测器_.exe\"")
        #如果强制结束，桌面右下角会残留图标，需要刷新任务栏以去除，防止相同的图标堆积起来
        os.chdir(_currentPath_)
        os.system("start \"【指定的标题】\" /WAIT _刷新任务栏_.exe")

    #无返回值
    return





#将配置文件中的密码单独读出，然后逐行写入到目标目录的一个单独存放密码的文件里，
#这样解压的时候就可以省掉直接从配置文件里筛选出密码所在区域的那部分时间。
def transfer_password() -> None:
    readed_passwords = []
    file = None
    try:
        #os.chdir(_currentPath_)
        file = open(_config_file_,mode="r",encoding="utf-8")
        content = [a for a in \
                   [a.replace("\n","") for a in file.readlines()] \
                   if a] #读取文件，去除空行和换行符
        file.close


        switch = False
        for buf in content:
            if buf == "------------------------ 密码起始线 ------------------------":
                start_line = True
                switch = True
            elif buf == "------------------------ 密码终止线 ------------------------":
                end_line = True
                #switch = False
                break
            elif switch:
                readed_passwords.append(buf)
        
        #如果有一个变量没有被定义，下面这行空表达式就会报错，“终止线”在前，“起始线”就会未定义
        start_line and end_line

    except:
        if file:
            try:
                file.close
            except:
                None
        os.chdir(_currentPath_)
        os.system("cd.>密码读取失败.txt")   #写一个空白文件方便批处理判断是否出错
        #无返回值
        return

    try:
        #os.chdir(_targetPath_)
        if readed_passwords:
            file = open(_password_file_,mode="w",encoding="utf-8")
            file.writelines([(a+"\n") for a in readed_passwords])
            file.close()
    except:
        if file:
            try:
                file.close
            except:
                None

        #os.chdir(_targetPath_)
        if os.path.exists(_password_file_):
            os.remove(_password_file_)

        os.chdir(_currentPath_)
        os.system("cd.>密码目的地写入失败.txt")   #写一个空白文件方便批处理判断是否出错
        #无返回值
        return
    
    #无返回值
    return





#将配置文件中的待删除文件列表单独读出，然后逐行写入到目标目录的一个单独存放删除文件列表的文件里，
#这样删除文件的时候就可以省掉直接从配置文件里筛选出删除文件列表所在区域的那部分时间。
def transfer_rm_list() -> None:
    readed_rm_list = []
    file = None
    try:
        #os.chdir(_currentPath_)
        file = open(_config_file_,mode="r",encoding="utf-8")
        content = [a for a in \
                   [a.replace("\n","") for a in file.readlines()] \
                   if a] #读取文件，去除空行和换行符
        file.close


        switch = False
        for buf in content:
            if buf == "-------------------- 删除指定文件起始线 --------------------":
                start_line = True
                switch = True
            elif buf == "-------------------- 删除指定文件终止线 --------------------":
                end_line = True
                #switch = False
                break
            elif switch:
                 readed_rm_list.append(buf)
        
        #如果有一个变量没有被定义，下面这行空表达式就会报错，“终止线”在前，“起始线”就会未定义
        start_line and end_line
    except:
        if file:
            try:
                file.close
            except:
                None
        
        os.chdir(_currentPath_)
        os.system("cd.>删除列表读取失败.txt")   #写一个空白文件方便批处理判断是否出错
        #无返回值
        return


    try:    
        #os.chdir(_targetPath_)
        if readed_rm_list:
            file = open(_rm_list_file_,mode="w",encoding="utf-8")
            file.writelines([(a+"\n") for a in readed_rm_list])
            file.close()

    except:
        if file:
            try:
                file.close
            except:
                None

        #os.chdir(_targetPath_)
        if os.path.exists(_rm_list_file_):
            os.remove(_rm_list_file_)

        
        os.chdir(_currentPath_)
        os.system("cd.>删除列表写入失败.txt")   #写一个空白文件方便批处理判断是否出错
        #无返回值
        return

    #无返回值
    return





#获取待删除文件列表
def get_remove_list() -> list:
    readed_remove_list = []
    file = None
    try:
        #运行“03-删除指定文件【不保护压缩文件】.bat”时（模式2）没有且不需要transfer_rm_list()，
        #加上运行“03-xx”时只需要读一次配置文件，所以要设置从配置文件里直接读取的第二选项。
        if os.path.exists(_rm_list_file_):
            #os.chdir(_targetPath_)
            file = open(_rm_list_file_,mode="r",encoding="utf-8")
            readed_remove_list = [a for a in \
                                  [a.replace("\n","") for a in file.readlines()] \
                                  if a]  #读取文件，去除空行和换行符
            file.close
        elif _mode_ == 2:
            #os.chdir(_currentPath_)
            file = open(_config_file_,mode="r",encoding="utf-8")
            content = [a for a in \
                       [a.replace("\n","") for a in file.readlines()] \
                       if a] #读取文件，去除空行和换行符
            file.close

            switch = False
            for buf in content:
                if buf == "-------------------- 删除指定文件起始线 --------------------":
                    start_line = True
                    switch = True
                elif buf == "-------------------- 删除指定文件终止线 --------------------":
                    end_line = True
                    #switch = False
                    break
                elif switch:
                    readed_remove_list.append(buf)
        
            #如果有一个变量没有被定义，下面这行空表达式就会报错，“终止线”在前，“起始线”就会未定义
            start_line and end_line

    except:
        if file:
            try:
                file.close
            except:
                None
        readed_remove_list.clear()

    return readed_remove_list


#删除指定文件
def delete_specific_files(recursion:bool) -> None:
    remove_list = get_remove_list()
    if remove_list:
        os.chdir(_targetPath_)
        if recursion:
            for file in remove_list:
                os.system("del /f /s /q " + "\""+file+"\"")
        #递归为否的情况下（运行“04-xxx.bat”时），保护批处理自身不被删
        else:
            for file in remove_list:
                os.system("for \u0025i in (" + "\""+file+"\"" + ") do (if \"\u0025i\" NEQ \"_child_excuter_4.bat\" (del /f /q \"\u0025i\"))")
    #无返回值
    return




#文件过滤器
def pass_file_filter(file:str) -> bool:
    #过滤掉非文件的文件夹
    if (not os.path.isfile(file)):
        return False
    else:
        ext = (os.path.splitext(file)[1]).replace(".","",1)#扩展名去掉点
        #过滤掉打上标记的
        if (ext == "【_过滤标记_】"):
            return False
        #过滤掉可能出现的程序文件
        for excluded_file in ["_child_excuter_1.bat","_child_excuter_4.bat","_password_.txt",
                              "_rm_list_.txt","_folder_names_record_.txt"]:
            if (file == excluded_file):
                return False

    return True

#得到目标目录下的所有文件的列表，并填入“_origin_file_list_”
def get_files() -> None:
    #声明全局变量“_origin_file_list_”，之后才能给“_origin_file_list_”赋值；
    #引用或读取全局变量时就可以直接写变量名。
    global _origin_file_list_

    os.chdir(_targetPath_)
    _origin_file_list_ = [element for element in os.listdir() if pass_file_filter(element)]

    #无返回值
    return

#程序内部刷新文件列表，去除列表中被“删除”后的“None”值
def internal_refresh_origin_file_list() -> None:
    global _origin_file_list_
    _origin_file_list_ = [file for file in _origin_file_list_ if file]
    
    #无返回值
    return




#从转移到目标目录下的单独存放密码的文件中获取密码列表
def get_password_list() -> None:
    global _password_list_

    file = None
    try:
        #os.chdir(_targetPath_)
        if os.path.exists(_password_file_):
            file = open(_password_file_,mode="r",encoding="utf-8")
            _password_list_ = [a for a in \
                               [a.replace("\n","") for a in file.readlines()] \
                               if a]  #读取文件，去除空行和换行符
            file.close
    except:
        if file:
            try:
                file.close
            except:
                None
        _password_list_.clear()

    #没读取到或出错时，蒙一个最常用的，为了省时间，情愿先只尝试一个，之后解压失败重来
    if not _password_list_:
        _password_list_.append("123456")
    
    #无返回值
    return




#detector.exe需要接收文本文件的路径作为参数，读取文本文件中的目标路径，每次调用解压操作前要提前准备好
def transfer_targetpath_for_detector() -> None:
    os.chdir(_detector_path_)
    file = open("_target_path_.txt",mode="w",encoding="utf-8")
    file.writelines([_targetPath_+"\n"])
    file.close
    #无返回值
    return




#去除扩展名中的多余字符（为了防止资源被和谐）产生的干扰
def clean_barrier() -> None:
    global _origin_file_list_
    unexpected_disappear_file_num = 0

    os.chdir(_targetPath_)

    #创建文件列表进行循环时的同步索引，循环到哪个值index对应的就是它的索引，方便修改
    index = -1
    for text in _origin_file_list_:
        index += 1

        split = os.path.splitext(text)
        name = split[0]
        ext = (split[1]).replace(".","",1)#去掉点

        state = False
        #下面的列表里是受保护的文件扩展名（小写），里面含有非字母数字成分，
        #“.未知类型”为程序自身产生的，但是一轮操作过后，要么消失，要么被打上过滤标记，所以这里不用包括在内。
        for i in ["search-ms","linux_amd64_asm","dvr-ms"]:
            if ext.lower() == i:
                state = True
                break
        if state:
            continue

        result = ""
        char_counted_in = 0

        #拥有文件名+扩展名两个完整部分的文件
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

            #当处理过后的文件名发生变化时重命名，过滤掉没变化的
            if (name+"."+result) != text:
                num = 1
                if char_counted_in > 0:
                    new_fname = name+"."+result
                    #一旦发现文件名被占用，自动分配一个新名字，防止冲突
                    while (os.path.exists(new_fname)):
                        new_fname = name + "(" + str(num).zfill(5) + ")" +"."+result
                        num += 1
                else:
                    #形如“xxx.zip.001.删除文字”的就能转换成“xxx.zip.001”，如果再往后面加“.未知类型”就不合适了
                    new_fname = name
                    #一旦发现文件名被占用，自动分配一个新名字，防止冲突
                    while (os.path.exists(new_fname)):
                        new_fname = name + "(" + str(num).zfill(5) + ")"
                        num += 1

                #检查文件是否还存在，防止中途有程序干扰文件夹
                if os.path.exists(text):
                    os.rename(text,new_fname)
                    #同步替换掉列表里的文件名
                    _origin_file_list_[index] = new_fname
                else:
                    unexpected_disappear_file_num += 1
                    _origin_file_list_[index] = None

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
            #因为“\u00a0”、“\u3000”上面不会被收入result，所以这里不需要
            #result = result.replace("\u00a0","\u0020")#替换不间断空格
            #result = result.replace("\u3000","\u0020")#替换全角空格
            
            #因为是无名文件，需要加个文件名，所以肯定要重命名
            num = 1
            if char_counted_in > 0:
                new_fname = "无名文件"+"."+result
                #一旦发现文件名被占用，自动分配一个新名字，防止冲突
                while (os.path.exists(new_fname)):
                    new_fname = "无名文件" + "(" + str(num).zfill(5) + ")" +"."+result
                    num += 1
            else:
                new_fname = "无名文件"+"."+"未知类型"
                #一旦发现文件名被占用，自动分配一个新名字，防止冲突
                while (os.path.exists(new_fname)):
                    new_fname = "无名文件" + "(" + str(num).zfill(5) + ")" +"."+"未知类型"
                    num += 1

            #检查文件是否还存在，防止中途有程序干扰文件夹
            if os.path.exists(text):
                os.rename(text,new_fname)
                #同步替换掉列表里的文件名
                _origin_file_list_[index] = new_fname
            else:
                unexpected_disappear_file_num += 1
                _origin_file_list_[index] = None

    if unexpected_disappear_file_num > 0:
        internal_refresh_origin_file_list()

    #无返回值
    return




#对rar、2345好压型分卷去掉最后两个“.”后的内容得到真实分卷文件名
def get_rar_2345_sep_vol_fname(input_string:str) -> str:
    return (os.path.splitext
            (os.path.splitext(input_string)[0])
            [0])

#对其他型分卷去掉最后一个“.”后的内容得到真实分卷文件名
def get_other_sep_vol_fname(input_string:str) -> str:
    return (os.path.splitext
            (input_string)
            [0])

#获取由一个类型的分卷文件组（同组中文件名相同）组成的分卷文件列表
def get_a_list_of_one_type_of_sep_vol_file_groups(mode:str) -> list:
    #分配匹配某一类分卷压缩包的特征，用于下面的匹配
    if mode == "rar":
        pattern = r".+[.]part\d+[.]rar$"
        #rar分卷的特点为“xxx.part[若干数字组成的编号].rar”，如“文件.part001.rar”
    elif mode == "zip":
        pattern = r".+[.]z\d+$|.+[.]zip$"
        #zip分卷的特点为有若干个形如“xxx.z[若干数字组成的编号]”，如“文件.z01”；
        #此外同组分卷文件中还有一个“.zip”文件，如“文件.zip”
    elif mode == "zipx":
        pattern = r".+[.]zx\d+$|.+[.]zipx$"
        #zipx分卷的特点为有若干个形如“xxx.zx[若干数字组成的编号]”，如“文件.zx01”；
        #此外同组分卷文件中还有一个“.zipx”文件，如“文件.zipx”
    elif mode == "001":
        pattern = r".+[.]\d+$"
        #001分卷的特点为“xxx.[7z或zip等等，甚至可以没有].[若干数字组成的编号]”，如“文件.7z.001”、“文件.zip.001”、“文件.001”
    elif mode == "rar_old":
        pattern = r".+[.]r\d+$"
        #老版rar分卷的特点为“xxx.r[若干数字组成的编号]”，如“文件.r01”
    elif mode == "hao_ziper":
        pattern = r".+[.]haozip\d+[.]zip$|.+[.]haozip\d+[.]7z$"
        #2345好压的分卷（“生成论坛专用分卷”模式）特点为“xxx.haozip[若干数字组成的编号].[zip/7z]”，如“文件.haozip01.zip”
    else:
        return []   #类型错误

    #filter_1筛选出所有匹配某个分卷类型的压缩包文件和在原文件列表中对应的索引，格式：[文件名,索引]
    filter_1 = []
    index = -1
    for file in _origin_file_list_:
        index += 1
        if re.match(pattern,file):
            filter_1.append([file,index])

    if filter_1:
        #按文件名对筛选出的分卷压缩包数据“[文件名,索引]”进行排序
        filter_1.sort(key=lambda element: element[0])
        #print(filter_1)

        #filter_2将filter_1中的压缩包分为若干个解压小组（分卷压缩包开头部分的文件名相同是一组），方便解压
        filter_2 = []
        list_buf = []
        #竖起第一组文件的“比较标杆”beginner
        if (mode == "rar") or (mode == "hao_ziper"):
            beginner = get_rar_2345_sep_vol_fname(filter_1[0][0])
        else:
            beginner = get_other_sep_vol_fname(filter_1[0][0])

        for element in filter_1:
            full_name = element[0]                              #full_name：完整文件名
            if (mode == "rar") or (mode == "hao_ziper"):
                real_name = get_rar_2345_sep_vol_fname(full_name)    #real_name：去掉".partXXX.rar"（最后2个点）之后的真实文件名
            else:
                real_name = get_other_sep_vol_fname(full_name)  #real_name：去掉".z01"等（最后1个点）之后的真实文件名
            
            if real_name == beginner:
                list_buf.append([a for a in element])      #真实文件名相同，说明是同一组分卷文件，装入放有同组分卷文件的list_buf
            else:
                #文件名变化，此时一组文件名相同的分卷文件（也可能是单个zip或
                #zipx文件）和对应索引已装进list_buf，添加进二维数组filter_2
                filter_2.append([a for a in list_buf])
                #一定是得这样写，不然append(buf_list)添加进二维数组的就是list_buf这个对象，而不是其中的成员
                #，list_buf一变，之前添加进二维数组里的元素也跟着变

                list_buf.clear()                                        #重置list_buf
                list_buf.append([a for a in element])                   #list_buf装入新一组文件的第一个
                beginner = real_name                                    #更换下一组文件的“比较标杆”
        filter_2.append([a for a in list_buf])      #还有最后一组文件未在循环中装入最终的filter_2，这一句补上

        filter_3 = [element for element in filter_2 if len(element)>1]
        #一开始的匹配可能漏进来了单个的.zip或.zipx文件，所以这里要去掉一组中只有一个文件的压缩包，也就是单个压缩包（非分卷压缩包）

        return filter_3

    else:
        return []




#检测解压是否成功
def extracted_successfully() -> bool:
    #解压失败成功检测器留在“组件”目录
    os.chdir(_currentPath_)
    #在“_checker_record_.txt”查找是否有失败标记
    ret=subprocess.run("find \"release_error_\" \"_checker_record_.txt\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
    #及时清除文本，为下一次解压准备
    os.system("cd.>_checker_record_.txt")
    #返回为非0，说明没有“find”命令没有找到失败标记，解压成功；反之失败
    if ret:
        return True
    else:
        return False


#检测是否为压缩文件
def is_compressed(file:str) -> bool:
    os.chdir(_targetPath_)
    ret=subprocess.run("\""+_zip_identifier_+"\"" + " " + "\""+file+"\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
    #如果是压缩文件，返回0
    if not ret:
        return True
    #返回1，说明路径有问题，将文件重命名后进行重新检查
    elif ret == 1:
        #检查文件是否存在
        if os.path.exists(file):
            new_fname = "_t_a_r_g_e_t_.bin"
            os.rename(file,new_fname)
            ret=subprocess.run("\""+_zip_identifier_+"\"" + " " + "\""+new_fname+"\"",stdout=None, stderr=None,
                   shell=False,creationflags=subprocess.CREATE_NO_WINDOW).returncode
            os.rename(new_fname,file)   #重命名并检测完成后，恢复原文件名
            #重命名过后返回0，文件本身还是压缩文件
            if not ret:
                return True
            #返回其他值说明不是压缩文件
            else:
                return False
        #不存在返回假
        else:
            return False
    #返回其他值说明不是压缩文件
    else:
        return False




#解压单个文件
def extract_a_single_file(file:str) -> bool:
    global _try_extra_file_count_
    #每尝试解压一个文件（组），说明这个文件已经判定为压缩文件，对批处理跳出循环起重要参考作用
    _try_extra_file_count_ += 1

    #初始化解压成功状态
    status = False
    try:
        #依次尝试密码
        for password in _password_list_:
            #解压前先用detector.exe记录下（r）当前目录下所有文件夹名称的列表
            os.chdir(_detector_path_)
            os.system("start \"【无标题】\" /min /wait detector.exe r \".\\_target_path_.txt\" \"_folder_names_record_.txt\"")

            #调用Bandizip进行解压，需要等到程序退出，用“start "【指定窗口标题】" /wait ……”
            os.chdir(_targetPath_)
            os.system("start \"titile\" /wait " + "\""+_bandizip_+"\"" + " x -aou -p:" + "\""+password+"\"" + " -target:auto " + "\""+file+"\"")

            if extracted_successfully():
                status = True
                break   #解压成功后就不用继续尝试下去了
            else:
                #失败后，可能会多出一个文件夹（最多为1个文件夹），里面是解压失败的文件，通过detector.exe删除（d）多出的文件夹
                os.chdir(_detector_path_)
                os.system("start \"【无标题】\" /min /wait detector.exe d \".\\_target_path_.txt\" \"_folder_names_record_.txt\"")
    except:
        return status
    #返回解压成功状态
    return status


#生成解压失败的文件、安全删除模式下需要保护的文件的保护标记（统一为1个，少一个在过滤时的判断条件）
def mark(fname:str) -> str:
    return ("【_过滤标记_】" + fname.replace(".","【_dot_】") + "【_过滤标记_】.【_过滤标记_】")


#解压由一个类型的分卷文件组（同组中文件名相同）组成的分卷文件列表
def extract_a_list_of_one_type_of_sep_file_groups(fg_list:list , mode:str) -> None:
    #if (not fg_list) or (not mode):
        #return
    
    global _origin_file_list_

    #同组分卷压缩文件解压时要找到一个“入口”文件，向压缩软件传递“入口”文件的文件名进行解压
    #如果是zip类分卷，“入口”文件排在同组最后，其他类型的分卷的“入口”文件排在第一个
    if mode == "zip":
        entry = -1
    else:
        entry = 0
    
    for group in fg_list:
        #返回的是解压是否成功（布尔值）
        ret = extract_a_single_file(group[entry][0])
        os.chdir(_targetPath_)

        if ret:
            for element in group:
                filename = element[0]
                index    = element[1]

                if os.path.exists(filename):
                    os.remove(filename) #成功就删除整个分卷文件组里的文件

                _origin_file_list_[index] = None #根据每个文件携带的索引“删除”_origin_file_list_里的对应文件名记录
        else:
            for element in group:
                filename = element[0]
                index    = element[1]

                if os.path.exists(filename):
                    os.rename(filename,mark(filename)) #失败就给整个分卷文件组里的文件打上标记

                _origin_file_list_[index] = None #根据每个文件携带的索引“删除”_origin_file_list_里的对应文件名记录

    internal_refresh_origin_file_list()

    #无返回值
    return



#####       之前一版在解压操作的代码中，需要多次刷新目标目录的文件列表，对于文件较多的场景下，时间和性能开销估计较大，
#####   而且获取到的列表是没有经过过滤的，之后的多个操作进行循环和过滤时都会额外增加时间。
#####   所以，这一次优化方向就是：只需要获取一次文件列表，同时在第一次获取的时候就对文件进行过滤，
#####   进行clean_barrier()，在外部对文件重命名的同时，在程序内部更新_origin_file_list_，修改已经改名的文件的数据；
#####   进行分卷文件解压或保护标记时，每处理一组文件，就把这组文件的数据从_origin_file_list_“删除”，
#####   这样之后解压或保护标记单个压缩文件时，_origin_file_list_中的元素数量就会减少，从而减少循环时间。
#####   进行到单个压缩文件时，后续就没有对文件的相关操作了，所以就不用从_origin_file_list_“删除”对应记录了。



#解压分卷压缩文件
def extra_sep_vol_files() -> None:
    #依次搜索各个类型的分卷文件，搜索一个类型后马上解压这个类型的分卷文件
    for pattern in ["rar","zip","zipx","001","rar_old","hao_ziper"]:
        buf_list = get_a_list_of_one_type_of_sep_vol_file_groups(pattern)
        if buf_list:
            extract_a_list_of_one_type_of_sep_file_groups(buf_list,pattern)
    #无返回值
    return


#确保压缩包文件名不与压缩包内的文件夹名称产生冲突，在没有扩展名的情况下，给文件加上标记
def secure_file_name(fname:str) -> str:
    if re.match(r".*[.].*",fname):
        return fname
    else:
        try:
            os.chdir(_targetPath_)
            new_name = fname + ".UnknownedZipFile"

            num = 0
            while (os.path.exists(new_name)):
                num += 1
                new_name = fname + "(" +str(num).zfill(5)+ ")" + ".UnknownedZipFile"

            os.rename(fname,new_name)
            return new_name
        except:
            return fname


#解压单独的压缩文件
def extra_single_files() -> None:
    os.chdir(_targetPath_)
    for file in _origin_file_list_:
        #is_compressed()能确定文件在解压前是否存在
        if is_compressed(file):
            #避免无扩展名压缩包文件在解压时，因为包中存在相同名字的文件夹而发生错误
            file = secure_file_name(file)
            #返回的是解压是否成功（布尔值）
            ret = extract_a_single_file(file)
            os.chdir(_targetPath_)
            if ret:
                os.remove(file) #成功就删除文件
            else:
                os.rename(file,mark(file))  #失败就打上标记
        else:
            if os.path.exists(file):
                os.rename(file,mark(file))  #不是压缩文件也打上标记，下一次就能在程序一开始就过滤掉这些文件
    #无返回值
    return



#在安全删除模式下，给受保护的单个压缩文件打保护标记
def protect_mark_single_files() -> None:
    os.chdir(_targetPath_)
    for file in _origin_file_list_:
        if is_compressed(file):#is_compressed()能确定文件是否存在
            os.rename(file,mark(file))
    #无返回值
    return


#在安全删除模式下，给单个类型的分卷文件打保护标记
def protect_mark_a_list_of_one_type_of_sep_vol_file_groups(fg_list:list) -> None:
    #if not fg_list:
        #return

    global _origin_file_list_

    os.chdir(_targetPath_)
    for group in fg_list:
        for element in group:
            filename = element[0]
            index    = element[1]

            if os.path.exists(filename):
                os.rename(filename,mark(filename))

            #同步“删除”在原文件列表中的记录，因为已经打上标记了，下一步给单个压缩包打标记不需要这些记录了
            _origin_file_list_[index] = None

    internal_refresh_origin_file_list()

    #无返回值
    return


#在安全删除模式下，给受保护的分卷压缩文件打保护标记
def protect_mark_sep_vol_files() -> None:
    #依次搜索各个类型的分卷文件，搜索一个类型后马上给这个类型的分卷文件打标记
    for pattern in ["rar","zip","zipx","001","rar_old","hao_ziper"]:
        buf_list = get_a_list_of_one_type_of_sep_vol_file_groups(pattern)
        if buf_list:
            protect_mark_a_list_of_one_type_of_sep_vol_file_groups(buf_list)
    #无返回值
    return


#给文件解除标记
def demark_files() -> None:
    global _origin_file_list_

    os.chdir(_targetPath_)
    _origin_file_list_ = [element for element in os.listdir() if os.path.isfile(element)]

    for file in _origin_file_list_:
        new_name = file

        if re.match(r".+【_过滤标记_】$",file):
            new_name = file.replace(".【_过滤标记_】","").replace("【_过滤标记_】","").replace("【_dot_】",".").replace(".UnknownedZipFile","")
        #下面两个是老版本的
        elif re.match(r".+【_解压失败_】$",file):
            new_name = file.replace(".【_解压失败_】","").replace("【_解压失败_】","").replace("【_dot_】",".")
        elif re.match(r".+【_保护_】$",file):
            new_name = file.replace(".【_保护_】","").replace("【_保护_】","").replace("【_dot_】",".")

        if (new_name != file):
            try:
                os.rename(file,new_name)
            except:
                None

    #无返回值
    return
    



'''
        ........       .......                    .....                                                       
        =@@@@@@@.     ,@@@@@@@                    =@@@@                                                       
        =@@@@@@@^     /@@@@@@@                    =@@@@                                                       
        =@@@@@@@@.   =@@@@@@@@      .]]]]]]`              .]]]`  ,]]]].                                       
        =@@@@=@@@^   @@@@=@@@@    /@@@@@@@@@@@.   =@@@@   =@@@@/@@@@@@@@`                                     
        =@@@@.@@@@. =@@@^=@@@@   /@@@/` .,@@@@^   =@@@@   =@@@@@/. ,@@@@@.                                    
        =@@@@.=@@@\ @@@@.=@@@@          ,]/@@@@   =@@@@   =@@@@^    =@@@@.         ,]]]]]]]]]]]]]]]]]]]`      
        =@@@@. @@@@/@@@^ =@@@@    ,@@@@@@@@@@@@   =@@@@   =@@@@.    =@@@@.         \@@@@@@@@@@@@@@@@@@@@.     
        =@@@@. =@@@@@@@. =@@@@  .@@@@@/[`.=@@@/   =@@@@   =@@@@.    =@@@@.                           =@@^     
        =@@@@.  @@@@@@^  =@@@@  =@@@@`   ,@@@@\   =@@@@   =@@@@.    =@@@@.                           =@@^     
        =@@@@.  =@@@@@.  =@@@@   \@@@@@@@@@@@@@   =@@@@   =@@@@.    =@@@@.                        @@@@@@@@@@  
        ,@@@@.   @@@@/   =@@@@    ,\@@@@[` \@@@^  =@@@O   ,@@@@.    ,@@@@.                        ,@@@@@@@@`  
                                                                                                   =@@@@@@^   
                                                                                                    @@@@@@    
                                                                                                    .@@@@^    
                                                                                                     =@@/     
                                                                                                      \@.     
                                                                                                       `      
'''




#解析传过来的参数
parser = argparse.ArgumentParser()
parser.add_argument("mode",type=int)
parser.add_argument("path",type=str)
args = parser.parse_args()

#进入上一级的“组件”文件夹，方便定位
os.chdir("..")
#记录当前目录（“组件”文件夹的绝对路径）
_currentPath_ = os.getcwd()
#记录目标目录
_targetPath_  = args.path

#配置各项信息
_bandizip_       = _currentPath_+"\\"+"BandizipPro_portable"+"\\"+"Bandizip.exe"
_detector_path_  = _currentPath_+"\\"+"detector"
_zip_identifier_ = _currentPath_+"\\"+"_压缩文件识别器_.exe"
_config_file_    = _currentPath_+"\\"+"配置解压密码和配置删除指定文件.txt"
_password_file_  = _targetPath_ +"\\"+"_password_.txt"
_rm_list_file_   = _targetPath_ +"\\"+"_rm_list_.txt"
_origin_file_list_ = []
_password_list_    = []
_try_extra_file_count_ = 0



_mode_ = args.mode
#模式0：解压（01-解多层压缩+解文件夹套娃.bat）前准备
if _mode_ == 0:
    transfer_password()
    sys.exit(0)

#模式2：运行“03-删除指定文件【不保护压缩文件】.bat”时调用，以【递归】方式删除目标目录下的指定文件
elif _mode_ == 2:
    delete_specific_files(True)
    sys.exit(0)

#模式3：运行“04-xxx.bat”时调用，以【非递归】方式删除目标目录下的指定文件
elif _mode_ == 3:
    delete_specific_files(False)
    sys.exit(0)

#模式4：运行“04-删除指定文件【保护压缩文件】.bat”时调用，提取并转移要删除文件的列表，为删除文件做准备
elif _mode_ == 4:
    transfer_rm_list()
    sys.exit(0)

#模式5：运行“04-删除指定文件【保护压缩文件】.bat”时调用，给压缩文件打上保护标记
elif _mode_ == 5:
    #获取文件列表
    get_files()
    if not _origin_file_list_:
        sys.exit(1)#这里虽然没什么实际的用处，但方便调试
    
    #给分卷压缩文件打上保护标记
    protect_mark_sep_vol_files()#internal_refresh_origin_file_list()

    #给单个压缩文件打上保护标记
    protect_mark_single_files()

    sys.exit(0)

#模式6：给文件解除标记
elif _mode_ == 6:
    demark_files()
    sys.exit(0)

#模式1：解压（01-解多层压缩+解文件夹套娃.bat）
elif _mode_ == 1:
    #获取文件列表
    get_files()
    #没有有效文件，说明原来就没有文件或只有解压失败的文件，返回1让批处理跳出循环
    if not _origin_file_list_:
        sys.exit(1)
    
    #准备密码列表
    get_password_list()
    #传送当前压缩文件所在目录给detector
    transfer_targetpath_for_detector()

    #打开“解压成功失败检测器”
    monitor_on()

    #去除扩展名中的多余字符（为了防止资源被和谐）产生的干扰
    clean_barrier()#在出意外时：internal_refresh_origin_file_list()


    #先尝试解压分卷压缩文件
    extra_sep_vol_files()#internal_refresh_origin_file_list()

    #再解决剩下来的单个文件
    extra_single_files()

    #关闭“解压成功失败检测器”
    monitor_off()
    
    #判断解压文件尝试的次数，如果没有压缩文件，尝试次数为0（每个/组文件解压前先判定了是否为压缩文件），返回1让批处理跳出循环
    #尝试次数不为0，说明
    if _try_extra_file_count_ > 0:
        sys.exit(0)
    else:
        sys.exit(1)
    

else:
    sys.exit(0)



#######################################    代码回收站    #######################################
#import csv
#import win32clipboard as wcb
#import win32con
#import time

#def pause():
    #os.system("pause")
    #return

#另一种可行的方法，不过还是舍弃了
#def paste_commmand_and_run(file,password):
    #os.chdir(_currentPath_)
    #os.system("start \"【标题】\" _命令粘贴助手_.exe")

    #command = "cls&&echo 【解压窗口，勿关】&&start \"titile\" /wait " + "\""+_bandizip_+"\"" +" x -aou -p:" +"\""+password+"\""+ " -target:auto "+"\""+file+"\""+"&&exit"
    #wcb.OpenClipboard()
    #wcb.EmptyClipboard()
    #wcb.SetClipboardData(win32con.CF_UNICODETEXT, command)
    #wcb.CloseClipboard()
    
    #time.sleep(0.25)
    #os.system("start \"【解压窗口，勿关】\" /D "+"\""+_targetPath_+"\""+" /WAIT cmd_2.exe")
    #return
