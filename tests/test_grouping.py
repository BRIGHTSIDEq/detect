from object_recognition.grouping.boxes import BoundingBox, Detection
from object_recognition.grouping.grouping import group_detections

def d(cls,x): return Detection(cls,'apple' if cls==0 else 'orange',0.9,BoundingBox(x,0.1,0.1,0.1))
def test_three_near_apples_merge():
    g=group_detections([d(0,0.1),d(0,0.19),d(0,0.28)])
    assert len(g)==1 and g[0].count==3 and round(g[0].box.width,2)==0.28
def test_far_apples_do_not_merge(): assert len(group_detections([d(0,0.1),d(0,0.8)]))==2
def test_different_classes_do_not_merge(): assert len(group_detections([d(0,0.1),d(1,0.12)]))==2
