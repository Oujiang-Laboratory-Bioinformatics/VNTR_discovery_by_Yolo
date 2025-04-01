import os
import sys

def get_fa_files(directory):
 
    fa_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.fa'):
            fa_files.append(filename)
    return fa_files

def compare_and_clean(folder1, folder2):
   

    files1 = get_fa_files(folder1)
    files2 = get_fa_files(folder2)
    common_files = set(files1) & set(files2)
    for filename in files1:
        if filename not in common_files:
            file_path = os.path.join(folder1, filename)
            os.remove(file_path)
            print(f"删除文件 {file_path}")
    
    for filename in files2:
        if filename not in common_files:
            file_path = os.path.join(folder2, filename)
            os.remove(file_path)
            print(f"删除文件 {file_path}")

if __name__ == "__main__":
 
    if len(sys.argv) != 3:
        print("用法: python3 compareAndclean.py <文件夹1路径> <文件夹2路径>")
        sys.exit(1)
    
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    
    if not os.path.exists(folder1):
        print(f"文件夹 {folder1} 不存在。")
        sys.exit(1)
    
    if not os.path.exists(folder2):
        print(f"文件夹 {folder2} 不存在。")
        sys.exit(1)
    
    compare_and_clean(folder1, folder2)
