
import os
import shutil

path = r'E:\weihai_braintumor\weihai\xueguan\niidata'

target_path = 'E:\python\monai\data1/2/'
def mycopyfile(srcfile,dstpath):                       # 复制函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.copy(srcfile, dstpath + fname)          # 复制文件
        print ("copy %s -> %s"%(srcfile, dstpath + fname))





for i in os.listdir(path):
    t1c = os.path.join(path,i)
    for t in os.listdir(t1c):
        if t.split('_')[1].split('.')[0] =='t1c':
            mycopyfile(os.path.join(t1c, t),target_path)




