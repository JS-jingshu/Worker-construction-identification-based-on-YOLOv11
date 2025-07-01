import os
import random
import shutil


def select_and_copy_files(image_dir, txt_dir, exclude_image_dirs, output_image_dir, output_txt_dir, num_to_select):
    # 创建输出文件夹
    for dir_path in [output_image_dir, output_txt_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # 获取所有图片和文本文件列表，并确保它们有相同的名称
    image_files = set(f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f)))
    txt_files = set(f for f in os.listdir(txt_dir) if os.path.isfile(os.path.join(txt_dir, f)) and f.endswith('.txt'))

    # 确保图片文件名与文本文件名（去掉扩展名后）匹配
    matching_files = {os.path.splitext(img)[0] for img in image_files}.intersection(
        {os.path.splitext(txt)[0] for txt in txt_files})

    # 初始化过滤后的文件集为所有匹配文件
    filtered_files = matching_files

    # 定义一个函数来获取要排除的文件集合
    def get_exclude_files(exclude_dir):
        if exclude_dir and os.path.exists(exclude_dir) and os.listdir(exclude_dir):
            return set(f for f in os.listdir(exclude_dir) if os.path.isfile(os.path.join(exclude_dir, f)))
        return set()

    # 获取要排除的文件集合
    exclude_files_set = set()
    for exclude_dir in exclude_image_dirs:
        exclude_files_set |= get_exclude_files(exclude_dir)

    # 进行文件排除操作
    if exclude_files_set:
        filtered_files = filtered_files - {os.path.splitext(img)[0] for img in exclude_files_set}

    # 如果可选文件少于要选择的数量，给出警告并调整选择数量
    if len(filtered_files) < num_to_select:
        print(f"Warning: Only {len(filtered_files)} files available to select from.")
        num_to_select = len(filtered_files)

    # 随机选择指定数量的文件
    selected_files = random.sample(list(filtered_files), num_to_select)

    # 复制选中的图片和文本文件到新文件夹
    for file_base_name in selected_files:
        # 查找对应的图片文件扩展名
        image_extension = next((ext for ext in ['.jpg', '.jpeg', '.png', '.bmp']
                                if os.path.exists(os.path.join(image_dir, file_base_name + ext))), None)
        if image_extension is None:
            print(f"Warning: No image found for base name {file_base_name}")
            continue

        image_file = os.path.join(image_dir, file_base_name + image_extension)
        txt_file = os.path.join(txt_dir, file_base_name + '.txt')

        shutil.copy(image_file, output_image_directory)
        shutil.copy(txt_file, output_txt_directory)


# 使用函数处理文件
image_directory = 'Original Images/augmentation Panama/images'  # 图片文件夹路径
txt_directory = 'Original Images/augmentation Panama/labels'  # 文本文件夹路径
exclude_image_directories = ['/Volumes/Elements/yolo/yolov8-main/augmentation_datasets2/banana/images/train',
                             '/Volumes/Elements/yolo/yolov8-main/augmentation_datasets2/banana/images/val']  # 要排除的图片文件夹路径列表，可以包含空字符串表示不做排除
output_image_directory = '/Volumes/Elements/yolo/yolov8-main/augmentation_datasets2/banana/images/test'  # 输出图片文件夹路径
output_txt_directory = '/Volumes/Elements/yolo/yolov8-main/augmentation_datasets2/banana/labels/test'  # 输出文本文件夹路径
number_of_files_to_select = 82  # 指定要选择的文件数量

select_and_copy_files(image_directory, txt_directory, exclude_image_directories, output_image_directory,
                      output_txt_directory, number_of_files_to_select)
