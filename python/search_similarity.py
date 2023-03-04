import cv2
import os
import shutil
import numpy as np

def norm_chitst(img_path):
    img = cv2.imread(img_path)
    H = cv2.calcHist([img], [1], None, [256], [0, 256])
    H = cv2.normalize(H, H, 0, 1, cv2.NORM_MINMAX, -1)
    return H

def count_similarity(H1, H2):
    simliarity = cv2.compareHist(H1, H2, 0)

    return simliarity

def select_sim(source_path, similar_metric):
    files2 = []
    new_files = []
    #idx = 0
    for root,dir,files in os.walk(source_path,topdown=True):
        files2 = files.copy()
        new_files =files.copy()
        for file in files:             
            files.remove(file)
            print("==>  Searching the similar image of {}:".format(file))
            for file2 in files:
                file_path = os.path.join(source_path, file)
                file2_path = os.path.join(source_path, file2)
                similarity = count_similarity(norm_chitst(file_path),norm_chitst(file2_path))
                print("THe similarity of {} and {} is {}".format(file2, file,similarity))
                if similarity>=similar_metric:
                    print("** {} is similar to {} with similarity of {}".format(file2, file,similarity))
                    files.remove(file2)
                else:
                    continue
                
        return files

def select_diff_file(source_path, file_list, new_path):     #根据提供的列表，提出相同的图片并重新放到指定的目录下
    idx = 0
    for file in file_list:
        idx = idx+1
        file_path = os.path.join(source_path, file)
        rename(file_path, idx, new_path)

def rename(org_path, idx, re_path):  #该函数将单个图片按照索引命名并复制到目标目录下
    new_path = re_path
    file_name = str(idx)
    file_name = file_name.zfill(5)
    file_name = file_name+".jpg"
    new_path = os.path.join(new_path, file_name)
    shutil.copyfile(org_path, new_path)
    return 0

if __name__  ==  "__main__":
    similarity_metric = 0.8
    source_path = "F:/Tank/oringinal/tank/"
    re_path = "F:/Tank/selected500/tank/"
    #scale_select(source_path, re_path, std_height, std_width)
    indiff_path = "F:/Tank/unsim/tank/"
    indiff_list = select_sim(re_path,similarity_metric)
    print("umsimilar list got")
    select_diff_file(re_path, indiff_list, indiff_path)