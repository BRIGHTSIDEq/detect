from dataclasses import dataclass

@dataclass(frozen=True)
class BoundingBox:
    """Хранит рамку в нормализованных координатах."""
    x: float; y: float; width: float; height: float
    @property
    def x2(self) -> float: return self.x + self.width
    @property
    def y2(self) -> float: return self.y + self.height
    @property
    def area(self) -> float: return max(0.0,self.width)*max(0.0,self.height)
    @property
    def center(self) -> tuple[float,float]: return (self.x+self.width/2,self.y+self.height/2)
    def union(self, other: 'BoundingBox') -> 'BoundingBox':
        x1,y1=min(self.x,other.x),min(self.y,other.y); x2,y2=max(self.x2,other.x2),max(self.y2,other.y2)
        return BoundingBox(x1,y1,x2-x1,y2-y1)
    def iou(self, other: 'BoundingBox') -> float:
        ix1,iy1=max(self.x,other.x),max(self.y,other.y); ix2,iy2=min(self.x2,other.x2),min(self.y2,other.y2)
        inter=max(0.0,ix2-ix1)*max(0.0,iy2-iy1); den=self.area+other.area-inter
        return inter/den if den else 0.0
    def gap(self, other: 'BoundingBox') -> float:
        dx=max(other.x-self.x2,self.x-other.x2,0.0); dy=max(other.y-self.y2,self.y-other.y2,0.0)
        return (dx*dx+dy*dy)**0.5

@dataclass(frozen=True)
class Detection:
    """Описывает исходную детекцию."""
    class_id:int; class_name:str; confidence:float; box:BoundingBox

@dataclass(frozen=True)
class DetectionGroup:
    """Описывает объединённую группу детекций."""
    class_id:int; class_name:str; confidence:float; box:BoundingBox; detections:tuple[Detection,...]
    @property
    def count(self)->int: return len(self.detections)
