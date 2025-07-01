from ultralytics import YOLO

if __name__ == '__main__':

    # Load a model
    model = YOLO(model=r'runs\detect\train2\weights\best.pt')  
    model.predict(source=r'detect.jpg',
                  save=True,
                  show=True,
                  )
