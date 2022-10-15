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


def check_dir(input_dir_path,output_dir_path):
    for filename_ori in os.listdir(input_dir_path):
        filename= input_dir_path + filename_ori
        if os.path.isfile(filename):
            ed=filename.split('.')[2]
            # print(ed)
            if ed in ['jpg','JPG']:
                year,month,day,hour,minitus,second=get_create_time(filename)
                if year!=None:
                    move_dir=output_dir_path+year+'_'+month+'/'
                    if not os.path.exists(move_dir):
                        os.mkdir(move_dir)
                    print(filename,'  ---  ',move_dir+filename_ori)
                    shutil.move(filename,move_dir+filename_ori)
                else:
                    print(filename,"           !!!!!!!!!!!!!!!!!!!!!!!!!")
            elif ed in ['MOV','mov','mp4','MP4']:
                pass
                # print('mov ',filename)
            elif ed in []:
                pass
            else:
                pass
                # print('unknow ',filename)
        else:
            check_dir(filename+'/',output_dir_path)

def main():
    input_file_path='./input_files/'
    output_file_path='./output_files/'
    check_dir(input_dir_path=input_file_path,output_dir_path=output_file_path)





if __name__ == '__main__':
    main()