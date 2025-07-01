import os
import random
import shutil
from sklearn.model_selection import KFold
import re
import argparse

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='YOLO数据集交叉验证划分工具')
    parser.add_argument('--image_dir', type=str, required=True, 
                       help='图片文件夹路径')
    parser.add_argument('--label_dir', type=str, required=True,
                       help='标签文件夹路径')
    parser.add_argument('--output_dir', type=str, default='yolo_cv_folds',
                       help='输出目录路径 (默认: yolo_cv_folds)')
    parser.add_argument('--num_folds', type=int, default=5,
                       help='交叉验证折数 (默认: 5)')
    parser.add_argument('--seed', type=int, default=42,
                       help='随机种子 (默认: 42)')
    return parser.parse_args()

def extract_group_id(filename):
    """从文件名中提取组ID"""
    # 移除文件扩展名
    base_name = os.path.splitext(filename)[0]
    
    # 常见增强模式匹配 (根据实际情况调整)
    patterns = [
        r'(.+?)_(flip|rotate|rot|rot90|bright|contrast|crop|blur|noise|trans|shift|scale|mirror)$',
        r'(.+?)_(aug\d+)$',
        r'(.+?)_(\d+)$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, base_name)
        if match:
            return match.group(1)  # 返回基础文件名作为组ID
    
    # 如果没有匹配增强模式，则认为是原图
    return base_name

def main():
    args = parse_arguments()
    
    # 设置随机种子
    random.seed(args.seed)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 步骤1: 收集所有图片并分组
    image_files = [f for f in os.listdir(args.image_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    groups = {}
    for img in image_files:
        group_id = extract_group_id(img)
        if group_id not in groups:
            groups[group_id] = []
        groups[group_id].append(img)
    
    print(f"发现 {len(groups)} 个图片组, 共 {len(image_files)} 张图片")
    print(f"平均每组 {len(image_files)/len(groups):.1f} 张图片")

    # 步骤2: 准备交叉验证划分
    group_ids = list(groups.keys())
    random.shuffle(group_ids)  # 随机打乱组顺序
    
    # 初始化K折交叉验证
    kf = KFold(n_splits=args.num_folds, shuffle=True, random_state=args.seed)
    
    # 步骤3: 创建交叉验证目录结构
    for fold in range(args.num_folds):
        fold_dir = os.path.join(args.output_dir, f"fold_{fold+1}")
        os.makedirs(os.path.join(fold_dir, "train", "images"), exist_ok=True)
        os.makedirs(os.path.join(fold_dir, "train", "labels"), exist_ok=True)
        os.makedirs(os.path.join(fold_dir, "val", "images"), exist_ok=True)
        os.makedirs(os.path.join(fold_dir, "val", "labels"), exist_ok=True)
    
    # 步骤4: 执行K折划分并复制文件
    fold_details = []
    for fold, (train_idx, val_idx) in enumerate(kf.split(group_ids)):
        print(f"\n正在处理 Fold {fold+1}/{args.num_folds}")
        
        # 获取当前fold的训练组和验证组
        train_groups = [group_ids[i] for i in train_idx]
        val_groups = [group_ids[i] for i in val_idx]
        
        print(f"  训练组: {len(train_groups)} 组")
        print(f"  验证组: {len(val_groups)} 组")
        
        fold_dir = os.path.join(args.output_dir, f"fold_{fold+1}")
        
        # 复制训练集图片和标签
        train_img_count = 0
        for group in train_groups:
            for img in groups[group]:
                # 复制图片
                src_img = os.path.join(args.image_dir, img)
                dst_img = os.path.join(fold_dir, "train", "images", img)
                shutil.copy2(src_img, dst_img)
                
                # 复制对应的标签文件
                label_name = os.path.splitext(img)[0] + ".txt"
                src_label = os.path.join(args.label_dir, label_name)
                
                if os.path.exists(src_label):
                    dst_label = os.path.join(fold_dir, "train", "labels", label_name)
                    shutil.copy2(src_label, dst_label)
                else:
                    print(f"  警告: 缺少标签文件 {src_label}")
                
                train_img_count += 1
        
        # 复制验证集图片和标签
        val_img_count = 0
        for group in val_groups:
            for img in groups[group]:
                # 复制图片
                src_img = os.path.join(args.image_dir, img)
                dst_img = os.path.join(fold_dir, "val", "images", img)
                shutil.copy2(src_img, dst_img)
                
                # 复制对应的标签文件
                label_name = os.path.splitext(img)[0] + ".txt"
                src_label = os.path.join(args.label_dir, label_name)
                
                if os.path.exists(src_label):
                    dst_label = os.path.join(fold_dir, "val", "labels", label_name)
                    shutil.copy2(src_label, dst_label)
                else:
                    print(f"  警告: 缺少标签文件 {src_label}")
                
                val_img_count += 1
        
        print(f"  训练图片: {train_img_count} 张, 验证图片: {val_img_count} 张")
        fold_details.append({
            "fold": fold+1,
            "train_groups": len(train_groups),
            "val_groups": len(val_groups),
            "train_images": train_img_count,
            "val_images": val_img_count
        })
    
    # 步骤5: 创建YOLO训练用的配置文件
    class_names = []  # 这里需要替换为您的实际类别
    
    for fold in range(args.num_folds):
        fold_dir = os.path.join(args.output_dir, f"fold_{fold+1}")
        config_content = f"""# YOLO 数据集配置文件 (Fold {fold+1})
train: {os.path.abspath(os.path.join(fold_dir, "train/images"))}
val: {os.path.abspath(os.path.join(fold_dir, "val/images"))}

# 类别数量
nc: {len(class_names)}

# 类别名称
names: {class_names}
"""
        with open(os.path.join(fold_dir, "dataset.yaml"), "w") as f:
            f.write(config_content)
    
    # 生成汇总报告
    print("\n" + "="*50)
    print("交叉验证划分完成！")
    print(f"结果已保存到: {os.path.abspath(args.output_dir)}")
    print(f"总组数: {len(groups)} | 总图片数: {len(image_files)}")
    print("-"*50)
    for detail in fold_details:
        print(f"Fold {detail['fold']}:")
        print(f"  训练组: {detail['train_groups']} ({detail['train_groups']/len(groups)*100:.1f}%)")
        print(f"  验证组: {detail['val_groups']} ({detail['val_groups']/len(groups)*100:.1f}%)")
        print(f"  训练图片: {detail['train_images']} 张")
        print(f"  验证图片: {detail['val_images']} 张")
        print("-"*50)
    
    # 生成使用说明
    print("\n使用说明:")
    print(f"1. 每个fold的目录结构:")
    print("   fold_X/")
    print("   ├── dataset.yaml    # YOLO配置文件")
    print("   ├── train/          # 训练集")
    print("   │   ├── images/     # 训练图片")
    print("   │   └── labels/     # 训练标签")
    print("   └── val/            # 验证集")
    print("       ├── images/     # 验证图片")
    print("       └── labels/     # 验证标签")
    print("\n2. 训练命令示例:")
    print(f"   yolo train data=fold_1/dataset.yaml model=yolov11s.pt epochs=100 imgsz=640")

if __name__ == "__main__":
    main()