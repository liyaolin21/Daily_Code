import cv2
import os
import shutil
import numpy as np

def rename(org_path, idx, re_path):  #该函数将单个图片按照索引命名并复制到目标目录下
    new_path = re_path
    file_name = str(idx)
    file_name = file_name.zfill(5)
    file_name = file_name+".jpg"
    new_path = os.path.join(new_path, file_name)
    shutil.copyfile(org_path, new_path)
    return 0

def scale_select(source_path, new_path, height, width):     #该函数可以选取特定长宽的图片，并按照顺序命名它们放到指定目录下
    std_height = height
    std_width = width
    idx=0
    for root,dir,files in os.walk(source_path,topdown=True):
        for file in files:
            file_name = file
            file_path = os.path.join(source_path,file_name)
            img = cv2.imread(file_path)
            if(img.shape[0]>=std_width and img.shape[1]>=std_height):
                idx = idx+1
                rename(file_path,idx,new_path)
    return 0

def change_name(source_path):                   #该函数直接将源目录下的文件重新命名
    idx = 0
    for root,dir,files in os.walk(source_path,topdown=True):
        for file in files:
            idx = idx+1
            file_path = os.path.join(source_path,file)
            new_name = str(idx)
            new_name = new_name.zfill(5)+".jpg"
            new_path = os.path.join(source_path,new_name)
            os.rename(file_path,new_path)

def select_diff(source_path):           #本函数的表述是：在一个列表中剔除所用的相同元素，只保留唯一的一个
    files2 = []
    new_files = []
    #idx = 0
    for root,dir,files in os.walk(source_path,topdown=True):
        files2 = files.copy()
        new_files =files.copy()
        for file in files:              #files是一个列表，我们的想法是创建files2，这个files里面不包含已经搜索的file和相同的不同命名的file，并且找到相同的file第二层循环不能终止，因为可能存在多个一样的，将唯一的一个复制到新文件夹中
            files2.remove(file)
            print("==>  Searching the same image of {}:".format(file))
            for file2 in files2:
                file_name = file
                file_path = os.path.join(source_path, file_name)
                file2_name = file2
                file2_path = os.path.join(source_path, file2_name)
                img1 = cv2.imread(file_path)    
                img2 = cv2.imread(file2_path)
                if img1.shape == img2.shape:
                    print("{}'s shape is the same as {}".format(file2, file))
                    difference = cv2.subtract(img1, img2)
                    result = not np.any(difference)
                    if result==True:
                        print("** {} is the same as {}".format(file2, file))
                        new_files.remove(file2)
                    else:
                        continue
                else:
                    continue
    
    return new_files

def select_diff_file(source_path, file_list, new_path):     #根据提供的列表，提出相同的图片并重新放到指定的目录下
    idx = 0
    for file in file_list:
        idx = idx+1
        file_path = os.path.join(source_path, file)
        rename(file_path, idx, new_path)
    
    return 0

def norm_chitst(img_path, channel):
    img = cv2.imread(img_path)
    H = cv2.calcHist([img], [channel], None, [256], [0, 256])
    H = cv2.normalize(H, H, 0, 1, cv2.NORM_MINMAX, -1)
    return H

def count_similarity(H1, H2):
    simliarity = cv2.compareHist(H1, H2, 0)
    return simliarity

def avg_similarity(img1_path, img2_path):
    sum_similarity = 0
    for channel in range(0,3):
        sum_similarity = count_similarity(norm_chitst(img1_path,channel),norm_chitst(img2_path,channel))+sum_similarity
    avg_sim = sum_similarity/3.0
    return avg_sim

def select_sim(source_path, similar_metric):
    files2 = []
    new_files = []
    #idx = 0
    for root,dir,files in os.walk(source_path,topdown=True):
        files2 = files.copy()
        new_files =files.copy()
        for file in files:
            if file in new_files:             
                files2.remove(file)
                print("==>  Searching the similar image of {}:".format(file))
                for file2 in files2:
                    if file2 in new_files:
                        file_path = os.path.join(source_path, file)
                        file2_path = os.path.join(source_path, file2)
                        similarity = avg_similarity(file_path,file2_path)
                        #print("THe similarity of {} and {} is {}".format(file2, file,similarity))
                        if similarity>=similar_metric:
                            print("****** {} is similar to {} with similarity of {}".format(file2, file,similarity))
                            new_files.remove(file2)
                        else:
                            continue
                    else:
                        continue
            else:
                continue
        
        return new_files





if __name__  ==  "__main__":
    std_height = 500
    std_width = 500
    unsim_path = "F:/Tank/unsim/tank/"
    shutil.rmtree(unsim_path)
    os.mkdir(unsim_path)
    similarity_metric = 0.90
    source_path = "F:/Tank/oringinal/tank/"
    re_path = "F:/Tank/selected500/tank/"
    #scale_select(source_path, re_path, std_height, std_width)
    unsim_list = select_sim(source_path,similarity_metric)
    print("umsimilar list got")
    select_diff_file(source_path, unsim_list, unsim_path)
    