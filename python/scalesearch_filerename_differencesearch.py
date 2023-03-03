import cv2
import os
import shutil
import np

def rename(org_path, idx, re_path):
    new_path = re_path
    file_name = str(idx)
    file_name = file_name.zfill(5)
    file_name = file_name+".jpg"
    new_path = os.path.join(new_path, file_name)
    shutil.copyfile(org_path, new_path)
    return 0

def scale_select(source_path, new_path, height, width):
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

def change_name(source_path):
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
    idx = 0
    for root,dir,files in os.walk(source_path,topdown=True):
        files2 = files
        new_files =files
        for file in files:              #files是一个列表，我们的想法是创建files2，这个files里面不包含已经搜索的file和相同的不同命名的file，并且找到相同的file第二层循环不能终止，因为可能存在多个一样的，将唯一的一个复制到新文件夹中
            files2 = files2.remove(file)
            for file2 in files2:
                file_name = file
                file_path = os.path.join(source_path, file_name)
                file2_name = file2
                file2_path = os.path.join(source_path, file2_name)
                img1 = cv2.imread(file_path)    
                img2 = cv2.imread(file2_path)
                difference = cv2.subtract(img1, img2)
                result = not np.any(difference)
                if result==True:
                    new_files.remove(file2)
                else:
                    continue
    
    return new_files

def select_diff_file(source_path, file_list, new_path):
    idx = 0
    for file in file_list:
        idx = idx+1
        file_path = os.path.join(source_path, file)
        rename(source_path, idx, new_path)
    
    return 0





if __name__  ==  "__main__":
    std_height = 500
    std_width = 500
    source_path = "F:/Tank/oringinal/tank"
    re_path = "F:/Tank/selected500/tank"
    #scale_select(source_path, re_path, std_height, std_width)
    indiff_path = "F:/Tank/indiff/tank"
    indiff_list = select_diff(source_path)
    select_diff_file(source_path, indiff_list, indiff_path)
    