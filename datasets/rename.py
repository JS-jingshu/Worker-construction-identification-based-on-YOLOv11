import os
import glob

def rename_jpg_files(folder_path):
    # 获取所有jpg文件（不区分大小写）
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    jpg_files += glob.glob(os.path.join(folder_path, '*.JPG'))
    
    # 按创建时间排序
    jpg_files.sort(key=os.path.getctime)
    
    # 打印找到的文件列表
    print(f"找到 {len(jpg_files)} 个JPG文件:")
    for i, f in enumerate(jpg_files, 1):
        print(f"{i}. {os.path.basename(f)}")
    
    # 计数器初始化
    count = 1
    
    # 创建新的文件列表（避免在重命名过程中改变源列表）
    new_files = []
    
    # 先处理所有重命名操作
    for file_path in jpg_files:
        # 确保文件仍然存在
        if not os.path.exists(file_path):
            print(f"警告: 文件 {os.path.basename(file_path)} 不存在，跳过")
            continue
            
        # 构建新文件名
        new_name = f"worker_{count}.jpg"
        new_path = os.path.join(folder_path, new_name)
        
        # 处理文件名冲突
        while os.path.exists(new_path):
            count += 1
            new_name = f"worker_{count}.jpg"
            new_path = os.path.join(folder_path, new_name)
        
        # 重命名文件
        try:
            os.rename(file_path, new_path)
            print(f"重命名: {os.path.basename(file_path)} -> {new_name}")
            new_files.append(new_path)
            count += 1
        except Exception as e:
            print(f"重命名 {os.path.basename(file_path)} 时出错: {str(e)}")

if __name__ == "__main__":
    # 用户输入文件夹路径
    target_folder = input("请输入文件夹路径: ").strip()
    
    # 检查路径是否存在
    if not os.path.isdir(target_folder):
        print("错误：指定的路径不是一个有效的文件夹！")
    else:
        rename_jpg_files(target_folder)
        print("\n所有JPG文件重命名完成！")