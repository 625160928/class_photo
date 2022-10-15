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

def main():
    input_file_path='./input_files/'
    for filename in os.listdir(input_file_path):
        if os.path.isfile(filename):
            year,month,day,hour,minitus,second=get_create_time(filename)
            print(year,month,day,hour,minitus,second)
        else:


if __name__ == '__main__':
    main()