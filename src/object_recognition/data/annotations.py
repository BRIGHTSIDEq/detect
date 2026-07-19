from dataclasses import dataclass
from pathlib import Path
from PIL import Image

@dataclass(frozen=True)
class Annotation:
    """Хранит аннотацию в формате YOLO."""
    class_id:int; x_center:float; y_center:float; width:float; height:float

def find_corrupt_images(paths:list[Path])->list[Path]:
    """Находит повреждённые изображения."""
    bad=[]
    for p in paths:
        try:
            with Image.open(p) as img: img.verify()
        except Exception:
            bad.append(p)
    return bad

def coco_bbox_to_yolo(class_id:int,bbox:list[float],image_width:int,image_height:int)->Annotation:
    """Преобразует COCO bbox в нормализованный YOLO bbox."""
    x,y,w,h=bbox
    return Annotation(class_id,(x+w/2)/image_width,(y+h/2)/image_height,w/image_width,h/image_height)
