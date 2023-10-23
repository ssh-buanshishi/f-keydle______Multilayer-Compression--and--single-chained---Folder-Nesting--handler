#include <QTextStream>
#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QSet>
//#include <QDebug>

//把dirName目录下的所有目录名记录到dirName/recordFileName中，utf-8编码
void RecordDir(const QString &dirName, const QString &recordFileName);

//对照dirName/recordFileName中的目录信息，删除没有的目录
void DeleteDir(const QString &dirName, const QString &recordFileName);

//从dirNameFile中获取一个目录路径
QString GetDirPath(const QString &dirNameFile);

//命令行使用格式为：.exe 命令(r/R/d/D) 目录路径文件 记录文件
int main(int argc, char* argv[])
{
//#if (QT_VERSION < QT_VERSION_CHECK(5,0,0))  //判断QT版本
//    #if _MSC_VER  //判断是否为MSVC编译器
//        QTextCodec *codec = QTextCodec::codecForName("gbk");    //获取GBK编解码器
//    #else
//        QTextCodec *codec = QTextCodec::codecForName("utf-8");  //获取UTF8编解码器
//    #endif
//        QTextCodec::setCodecForLocale(codec);
//        QTextCodec::setCodecForCStrings(codec);
//        QTextCodec::setCodecForTr(codec);
//#else
//    QTextCodec *codec = QTextCodec::codecForName("utf-8");
//    QTextCodec::setCodecForLocale(codec);
//#endif

    //确保是有4个参数
    if(argc != 4) return -1;

    //确保命令参数为单字符
    if(strlen(argv[1]) != 1) return -1;

    //取出命令
    char command = argv[1][0];
    //提取出目录名和记录文件名
    QString dirPath = GetDirPath(argv[2]);
    QString recordFileName = QString::fromLocal8Bit(argv[3]);

    //判断要操作的目录是否为空路径
    if(dirPath.isEmpty()) return -1;

//    qDebug() << "dirPath = " << dirPath;
//    qDebug() << "reocrdFileName = " << recordFileName;


    //判断命令
    //删除
    if(command  == 'd' || command  == 'D')
    {
        DeleteDir(dirPath, recordFileName);
    }
    //记录
    else if(command  == 'r' || command  == 'R')
    {
        RecordDir(dirPath, recordFileName);
    }
    else
    {
        return -1;
    }

    return 0;
}


QString GetDirPath(const QString &dirNameFile)
{
    QFileInfo fileInfo(dirNameFile);
    if(!fileInfo.exists() || !fileInfo.isFile())
    {
//        qDebug() << "dirNameFile error!";
        return QString();
    }

    //打开记录文件
    QFile file(dirNameFile);
    if(!file.open(QFile::ReadOnly))
    {
        return QString();
    }

    QTextStream inStream(&file);
    //设置编码格式为UTF-8
    inStream.setCodec("UTF-8");

    //读取不限制长度的一行
    return inStream.readLine();
}


void RecordDir(const QString &dirName, const QString &recordFileName)
{
    QFileInfo fileInfo(dirName);
    //判断是否存在和是否为目录
    if(!fileInfo.exists() || !fileInfo.isDir())
    {
        return;
    }

    //拼接记录文件绝对路径
    QString recordFilePath = QString("%1\\%2").arg(fileInfo.absoluteFilePath(), recordFileName);

    //打开记录文件
    QFile recordFile(recordFilePath);
    if(recordFile.open(QFile::WriteOnly))
    {
        //获取所有的子目录名
        QDir dir(dirName);
        QStringList childDirList = dir.entryList(QDir::Dirs);

        QTextStream outStream(&recordFile);
        //设置编码格式为UTF-8
        outStream.setCodec("UTF-8");
        for(int i = 0; i < childDirList.size(); i++)
        {
            outStream << childDirList.at(i).toUtf8() << Qt::endl;
        }
    }
}


void DeleteDir(const QString &dirName, const QString &recordFileName)
{
    QFileInfo fileInfo(dirName);
    //判断是否存在和是否为目录
    if(!fileInfo.exists() || !fileInfo.isDir())
    {
        return;
    }

    //拼接记录文件绝对路径
    QString recordFilePath = QString("%1\\%2").arg(fileInfo.absoluteFilePath(), recordFileName);

    //打开记录文件
    QFile recordFile(recordFilePath);
    if(!recordFile.open(QFile::ReadOnly))
    {
        return;
    }

    //先读取记录文件
    QSet<QString> oldDirNames;
    QTextStream inStream(&recordFile);
    //设置编码格式为UTF-8
    inStream.setCodec("UTF-8");

    //从记录文件中记取所有的目录
    while(1)
    {
        QString line = inStream.readLine(1024);
        if(line.isEmpty()) break;
        oldDirNames.insert(line);
    }

    //如果老的记录文件上空的则不再进行删除操作
    if(oldDirNames.isEmpty())
    {
        return;
    }

    //获取当前目录中的所有目录信息
    QDir dir(dirName);
    QFileInfoList childDirsInfoList = dir.entryInfoList(QDir::Dirs);
    for(int i = 0; i < childDirsInfoList.size(); i++)
    {
        //在老的目录记录中查找，如果没有找到则删除
        if(oldDirNames.find(childDirsInfoList.at(i).fileName()) == oldDirNames.end())
        {
            //删除目录
            QDir(childDirsInfoList.at(i).absoluteFilePath()).removeRecursively();
        }
    }

//    recordFile.remove();
}
