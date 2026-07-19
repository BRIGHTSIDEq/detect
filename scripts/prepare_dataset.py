from pathlib import Path
for s in ['train','val','test']:
    (Path('data/processed/yolo/images')/s).mkdir(parents=True,exist_ok=True); (Path('data/processed/yolo/labels')/s).mkdir(parents=True,exist_ok=True)
print('Структура YOLO создана')
