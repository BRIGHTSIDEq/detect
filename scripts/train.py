from ultralytics import YOLO
from pathlib import Path
import yaml, torch

def main():
    cfg=yaml.safe_load(Path('configs/train.yaml').read_text(encoding='utf-8'))
    model=YOLO(cfg['model'])
    try:
        model.train(data='configs/data.yaml', imgsz=cfg['image_size'], epochs=cfg['epochs'], batch=cfg['batch_size'], workers=cfg['workers'], amp=cfg['amp'], patience=cfg['patience'], project=cfg['project'])
    except RuntimeError as e:
        if 'out of memory' in str(e).lower() and torch.cuda.is_available():
            torch.cuda.empty_cache(); cfg['batch_size']=max(cfg['min_batch_size'], cfg['batch_size']//2); model.train(data='configs/data.yaml', imgsz=cfg['image_size'], epochs=cfg['epochs'], batch=cfg['batch_size'], workers=0, amp=True, project=cfg['project'])
        else: raise
if __name__=='__main__': main()
