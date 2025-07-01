import torch
import warnings
from functools import partial
from ultralytics import YOLO
from ultralytics.nn.tasks import DetectionModel

# 修复 1: 安全覆盖 torch.load
original_torch_load = torch.load
def custom_torch_load(*args, **kwargs):
    kwargs["weights_only"] = False  # 强制设置 weights_only=False
    return original_torch_load(*args, **kwargs)
torch.load = custom_torch_load

# 修复 2: 允许 DetectionModel 类
torch.serialization.add_safe_globals([DetectionModel])

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # 方式 1: 从 YAML 配置文件初始化模型结构（无预训练权重）
    # model = YOLO(r"ultralytics\cfg\models\11\yolo11n.yaml")
    
    # 方式 2: 加载预训练权重（需确保路径正确）
    model = YOLO("yolo11n.pt")
    
    # 训练配置
    model.train(
        data=r"datasets\Cross_validation\fold_5\dataset.yaml",
        cache=False,
        imgsz=640,
        epochs=300,
        batch=64,
        close_mosaic=10,
        workers=8,
        patience=50,
        device="0",
        optimizer="SGD",
    )