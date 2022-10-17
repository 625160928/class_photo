import os
import exifread
import random
import time
import shutil

import datetime

def del_str_null(input_str):
    ans=input_str
    while ans[0]==' ':
        ans=ans[1:]
    while ans[-1]==' ':
        ans=ans[:len(ans)-1]
    return ans


def main():
    file_path='./log.txt'
    with open(file_path, encoding='utf-8') as file_obj:
        for line_row in file_obj:
            if line_row=='':
                continue
            if 'File format not recognized.' in line_row:
                continue
            if ' move to ' in line_row:
                line=line_row.replace('\\','/')
                k=line.split(' move to ')
                # ori_name=
                ori_path=k[0].replace('\n','')
                ori_path=del_str_null(ori_path)
                ori_name=ori_path.split('/')[-1]
                new_path=k[1].replace('\n','')
                new_path=del_str_null(new_path)

                new_path_base=new_path.split('/')
                new_path_base_str=''
                for i in range(len(new_path_base)-1):
                    new_path_base_str+=new_path_base[i]+'/'
                # new_path_base_str='D:\Program Files (x86)\文档整理\输出/unknown/'
                # print(ori_name,new_path,new_path_base_str)
                new_name_path=new_path_base_str+ori_name
                # print(new_path,'----',new_path[-1],new_name_path[0],'---------',new_name_path)

                if os.path.exists(new_path):
                    shutil.move(new_path, new_name_path)
                # print(ori_name)
if __name__ == '__main__':
    main()
    # print(del_str_null('  D:/Program Files (x86)/文档整理/输出/unknown/1665994744.3736293.png '))