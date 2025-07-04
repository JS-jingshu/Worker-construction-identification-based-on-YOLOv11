# Worker-construction-identification-based-on-YOLOv11

## 1. 数据集预处理
- 从网上搜索相关图片并保存到本地文件夹，共30张图片
- 使用labelimg工具进行标注，保存为txt文件
![数据标注](labelimg.png)
- 因数据集较少，对数据进行扩充，使用数据增强技术（具体代码见 `datasets/augmentation.py`）

## 2. 交叉验证
扩充后的数据集共300张(含30张原图)仍较少，故进行交叉验证。  
此处采用5折交叉验证，结果如下：

| 折数 | P     | R     | mAP50 | mAP50-95 |
|:----:|:-----:|:-----:|:-----:|:--------:|
| 1    | 0.842 | 0.577 | 0.699 | 0.441    |
| 2    | 1     | 1     | 0.995 | 0.993    |
| 3    | 0.996 | 0.989 | 0.995 | 0.982    |
| 4    | 1     | 0.996 | 0.995 | 0.984    |
| 5    | 1     | 0.978 | 0.987 | 0.977    |

## 3. 模型预测
使用效果最好的第二折的训练权重进行预测，预测效果如下：

![预测效果展示](/runs/detect/predict/detect.jpg)
