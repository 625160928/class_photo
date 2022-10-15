import os
import exifread
import random
import time
import shutil


def getExif(filename):
  FIELD = 'EXIF DateTimeOriginal'
  fd = open(filename, 'rb')
  tags = exifread.process_file(fd)
  fd.close()
  if FIELD in tags:
    k1=str(tags[FIELD]).split(" ")
    k2=k1[0].split(":")
    print('k2  ',k2)


    new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
    tot = 1
    while os.path.exists(new_name):
      new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + '_' + str(tot) + os.path.splitext(filename)[1]
      tot += 1
    new_name2 = new_name.split(".")[0] + '__' +filename
    print('new name 2',new_name2)
    os.rename(filename, new_name2)
  else:
    print('No {} found'.format(FIELD))

def get_create_time(filename):
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


def check_dir(input_dir_path,output_dir_path,move=False):
    cannot_move=[]
    for filename_ori in os.listdir(input_dir_path):
        filename= input_dir_path + filename_ori
        if os.path.isfile(filename):
            try:
                year, month, day, hour, minitus, second = get_create_time(filename)
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
            except:
                cannot_move.append(filename)

        else:
            cannot_move=cannot_move+check_dir(filename+'/',output_dir_path,move=move)

    return cannot_move
def main():
    input_file_path='D:/Program Files (x86)/文档整理/unkown/'
    output_file_path='D:/Program Files (x86)/文档整理/输出/'

    input_file_path=input_file_path.replace('\\','/')
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)
    ans=check_dir(input_dir_path=input_file_path,output_dir_path=output_file_path,move=False)


    for path in ans:
        print(path)


    # print(os.listdir(input_file_path))



    # f='E:/兴趣开发/照片备份/ip 相片/2013_12/IMG_0821_696645203.JPG'
    # mtime = time.ctime(os.path.getmtime(f))
    # ctime = time.ctime(os.path.getctime(f))
    # print("Last modified : %s, last created time: %s" % (mtime, ctime))


if __name__ == '__main__':
    main()