from object_recognition.data.annotations import coco_bbox_to_yolo
from object_recognition.evaluation.metrics import precision_recall

def test_coco_conversion():
    a=coco_bbox_to_yolo(1,[10,20,30,40],100,200)
    assert a.class_id==1 and abs(a.x_center-0.25)<1e-6

def test_metrics(): assert precision_recall(8,2,2)==(0.8,0.8)
