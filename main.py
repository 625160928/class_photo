import os
import exifread
import random
import time
import shutil

import datetime
import warnings
warnings.filterwarnings("ignore")
def cmp_file(f1, f2):
    st1 = os.stat(f1)
    st2 = os.stat(f2)

    # 比较文件大小
    if st1.st_size != st2.st_size:
        return False

    bufsize = 8*1024
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)  # 读取指定大小的数据进行比较
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True

def get_photo_create_time(filename):
  FIELD = 'EXIF DateTimeOriginal'
  year=None
  month=None
  day=None
  hour=None
  minitus=None
  second=None
  # print(filename)
  fd = open(filename, 'rb')
  tags = exifread.process_file(fd)
  # for k in tags:
  #     print(k,tags[k])
  # print(tags)
  fd.close()
  if FIELD in tags:
      k1=str(tags[FIELD]).split(" ")
      k2=k1[0].split(':')
      k3=k1[1].split(':')
      year=k2[0]
      month=k2[1]
      day=k2[2]
      hour=k3[0]
      minitus=k3[1]
      second=k3[2]



  return year,month,day,hour,minitus,second

def get_file_time(filename):
    year = None
    month = None
    day = None
    hour = None
    minitus = None
    second = None

    t = os.path.getmtime(filename)
    str_t=str(datetime.datetime.fromtimestamp(t))
    k1 = str_t.split(" ")
    k2 = k1[0].split('-')
    k3 = k1[1].split(':')


    year = k2[0]
    month = k2[1]
    day = k2[2]
    hour = k3[0]
    minitus = k3[1]
    second = k3[2].split('.')[0]

    return year,month,day,hour,minitus,second

def class_file_all(input_dir_path, output_dir_path, move=False):
    cannot_move=[]
    for filename_ori in os.listdir(input_dir_path):
        filename= input_dir_path + filename_ori
        if os.path.isfile(filename):
            year, month, day, hour, minitus, second = get_file_time_all( filename)

            if year != None:
                move_dir = output_dir_path + year + '_' + month + '/'
                if not os.path.exists(move_dir):
                    os.mkdir(move_dir)
                if move:
                    if not os.path.exists(move_dir + filename_ori):
                        fin_path=move_dir + filename_ori
                    else:
                        fin_path=move_dir + str(time.time()) + filename_ori
                    print(filename,'  move to  ',fin_path)
                    shutil.move(filename, fin_path)
            else:
                    move_dir =output_dir_path+'unkown/'
                    if not os.path.exists(move_dir):
                        os.mkdir(move_dir)

                    if move:
                        if not os.path.exists(move_dir+filename_ori):
                            fin_path=move_dir+filename_ori
                        else:
                            fin_path=move_dir+str(time.time())+filename_ori
                        shutil.move(filename,fin_path)
                        print(filename,' to unkown')
        else:
            cannot_move= cannot_move + class_file_all(filename + '/', output_dir_path, move=move)

    return cannot_move


def get_file_time_all( filename):
    year = None
    month = None
    day = None
    hour = None
    minitus = None
    second = None
    try:
        year, month, day, hour, minitus, second = get_photo_create_time(filename)
    except:
        year, month, day, hour, minitus, second = get_file_time(filename)
    if year==None:
        year, month, day, hour, minitus, second = get_file_time(filename)

    # print(filename, year, month, day, hour, minitus, second)
    return year, month, day, hour, minitus, second


def move_same_file_all(input_dir_path, output_dir_path, move=False):
    check_file_list=[]
    for filename_ori in os.listdir(input_dir_path):
        filename= input_dir_path + filename_ori
        if os.path.isfile(filename):
            check_file_list.append(filename_ori)
        else:
            move_same_file_all(filename + '/', output_dir_path, move)
    len1=len(check_file_list)
    unique=[]
    del_list=[]
    while check_file_list!=[]:
        ck=check_file_list[0]
        check_file_list.remove(ck)
        unique.append(ck)
        rec_to_del=[]
        if len(check_file_list)>0:
            for i in check_file_list:
                if cmp_file(input_dir_path+ck,input_dir_path+i)==True:
                    rec_to_del.append(i)
                    del_list.append(i)
            for i in rec_to_del:
                check_file_list.remove(i)

    print('===================================')
    print(input_dir_path)
    print(len1,len(unique),len(del_list),len1==len(unique)+len(del_list))


    if move:
        move_dir = output_dir_path + 'unkown/'
        if not os.path.exists(move_dir):
            os.mkdir(move_dir)
        for filename_ori in del_list:
            filename= input_dir_path + filename_ori
            if not os.path.exists(move_dir + filename_ori):
                fin_path = move_dir + filename_ori
            else:
                fin_path = move_dir + str(time.time()) + filename_ori
            shutil.move(filename, fin_path)
            print(filename, ' to unkown')

def get_file_path_list(dir_path):
    file_list=[]
    for i, j, k in os.walk(dir_path):
        # print(i, j, k)
        if k!=[]:
            for file_name in k:
                file_list.append(i+'/'+file_name)
    return file_list


def move_in_file_all(input_dir_path, output_dir_path, move=False):
    move_in_number=0
    exist_number=0

    input_file_list=get_file_path_list(input_dir_path)
    all_number=len(input_file_list)

    for filename in input_file_list:
        just_name=filename.split('/')[-1]
        #确认文件的移动位置
        year, month, day, hour, minitus, second = get_file_time_all( filename)
        if year !=None and month!=None:
            file_to_path=output_dir_path+year+'_'+month+'/'
        else:
            file_to_path=output_dir_path+'unknown/'

        if not os.path.exists(file_to_path):
            os.mkdir(file_to_path)
        # print(filename,file_to_path)

        #判断文件是否已经存在
        check_file_list=get_file_path_list(file_to_path)
        need_move=True
        for ck in check_file_list:
            if cmp_file(ck,filename)==True:
                exist_number+=1
                need_move=False
                break
        if need_move==False:
            file_to_path = output_dir_path + 'copy/'
            if not os.path.exists(file_to_path):
                os.mkdir(file_to_path)

        file_to_path+=just_name

        if not os.path.exists(file_to_path ):
            fin_path = file_to_path

        else:
            k=file_to_path.split('/')
            if len(k)!=1:
                head=''
                for i in range(len(k)-1):
                    head+=k[i]+'/'

                tail=k[-1]
                # print(head,tail,'=======',k)
                fin_path = head + str(time.time()) +'_'+ tail
            else:
                break

        print(need_move,filename, '  move to  ', fin_path)

        if move:
            #只有不存在的文件才需要移动
            # if need_move :
            move_in_number+=1
            shutil.move(filename, fin_path)
            print(filename, '  move to  ', fin_path)


    print(all_number,move_in_number,exist_number)



def find_eq_file(input_dir_path, check_dir_path):
    move_in_number=0
    exist_number=0
    ans=[]
    input_file_list=get_file_path_list(input_dir_path)
    all_number=len(input_file_list)

    for filename in input_file_list:
        tmp_eq=''
        just_name=filename.split('/')[-1]
        #确认文件的移动位置
        year, month, day, hour, minitus, second = get_file_time_all( filename)
        if year !=None and month!=None:
            file_to_path= check_dir_path + year + '_' + month + '/'
        else:
            file_to_path= check_dir_path + 'unknown/'

        # print(filename,file_to_path)

        #判断文件是否已经存在
        check_file_list=get_file_path_list(file_to_path)
        for ck in check_file_list:
            if cmp_file(ck,filename)==True:
                tmp_eq=ck
                break
        if tmp_eq=='':
            print(filename,' ======= ',tmp_eq,' ================= ',year , month )
            ans.append([filename,' ======= ',tmp_eq,' ================= ',year , month])
    return ans



def main():
    input_file_path='D:/Program Files (x86)/文档整理/copy/'
    output_file_path='D:/Program Files (x86)/文档整理/输出/'

    input_file_path=input_file_path.replace('\\','/')
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)

    # ans=move_file_all(input_dir_path=input_file_path, output_dir_path=output_file_path, move=True)
    # move_same_file_all(input_dir_path=input_file_path, output_dir_path=output_file_path, move=True)
    # move_in_file_all(input_dir_path=input_file_path, output_dir_path=output_file_path, move=True)
    ans=find_eq_file(input_dir_path=input_file_path, check_dir_path=output_file_path)

    # print(get_file_time_all('D:/Program Files (x86)/文档整理/copy//2019_01_16_08_55_IMG_1610.MOV'))
    # print(get_file_time('D:/Program Files (x86)/文档整理/copy//2019_01_16_08_55_IMG_1610.MOV'))
    # for i in ans:
    #     print(i)
    # print('========')
    # print(len(ans))
if __name__ == '__main__':
    main()