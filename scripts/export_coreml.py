from ultralytics import YOLO
from pathlib import Path
import json,yaml,shutil
cfg=yaml.safe_load(Path('configs/export.yaml').read_text(encoding='utf-8'))
classes=yaml.safe_load(Path('configs/classes.yaml').read_text(encoding='utf-8'))['classes']
model=YOLO(cfg['checkpoint'])
out=model.export(format='coreml', imgsz=cfg['image_size'], half=cfg['half'], nms=cfg['nms'])
Path('artifacts/coreml').mkdir(parents=True, exist_ok=True)
Path(cfg['metadata']).write_text(json.dumps(classes,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
