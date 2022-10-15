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
    print(k2)


    new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
    tot = 1
    while os.path.exists(new_name):
      new_name = str(tags[FIELD]).replace(':', '').replace(' ', '_') + '_' + str(tot) + os.path.splitext(filename)[1]
      tot += 1
    new_name2 = new_name.split(".")[0] + '__' +filename
    print(new_name2)
    os.rename(filename, new_name2)
  else:
    print('No {} found'.format(FIELD))


for filename in os.listdir('.'):
  if os.path.isfile(filename):
    getExif(filename)