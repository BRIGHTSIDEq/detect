from .boxes import BoundingBox, Detection, DetectionGroup

class GroupingConfig:
    """Хранит пороги группировки."""
    def __init__(self, min_iou_to_merge:float=0.02, max_center_distance_ratio:float=1.75, max_gap_ratio:float=0.65, size_similarity_min:float=0.25, confidence_weight:str='area'):
        self.min_iou_to_merge=min_iou_to_merge; self.max_center_distance_ratio=max_center_distance_ratio; self.max_gap_ratio=max_gap_ratio; self.size_similarity_min=size_similarity_min; self.confidence_weight=confidence_weight

def should_merge(a:Detection,b:Detection,cfg:GroupingConfig)->bool:
    """Проверяет, относятся ли две рамки к одной визуальной группе."""
    if a.class_id!=b.class_id: return False
    size=min(a.box.area,b.box.area)/max(a.box.area,b.box.area) if max(a.box.area,b.box.area)>0 else 0
    if size < cfg.size_similarity_min: return False
    if a.box.iou(b.box)>=cfg.min_iou_to_merge: return True
    ac,bc=a.box.center,b.box.center
    center=((ac[0]-bc[0])**2+(ac[1]-bc[1])**2)**0.5
    scale=((a.box.width+a.box.height+b.box.width+b.box.height)/4) or 1
    gap=a.box.gap(b.box)
    return center/scale<=cfg.max_center_distance_ratio and gap/scale<=cfg.max_gap_ratio

def group_detections(detections:list[Detection], cfg:GroupingConfig|None=None)->list[DetectionGroup]:
    """Группирует соседние детекции одного класса."""
    cfg=cfg or GroupingConfig(); n=len(detections); parent=list(range(n))
    def find(x:int)->int:
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a:int,b:int)->None:
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for i in range(n):
        for j in range(i+1,n):
            if should_merge(detections[i],detections[j],cfg): union(i,j)
    buckets={}
    for i,d in enumerate(detections): buckets.setdefault(find(i),[]).append(d)
    groups=[]
    for items in buckets.values():
        box=items[0].box
        for d in items[1:]: box=box.union(d.box)
        weights=[max(d.box.area,1e-6) for d in items]
        conf=sum(d.confidence*w for d,w in zip(items,weights))/sum(weights)
        groups.append(DetectionGroup(items[0].class_id,items[0].class_name,conf,box,tuple(items)))
    return sorted(groups,key=lambda g:(g.class_id,g.box.x,g.box.y))
