from pathlib import Path
import hashlib, random

def image_hash(path:Path)->str:
    """Вычисляет хэш изображения."""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def deterministic_split(items:list[Path], seed:int=42, ratios:tuple[float,float,float]=(0.8,0.1,0.1))->dict[str,list[Path]]:
    """Создаёт воспроизводимое разбиение."""
    rng=random.Random(seed); data=items[:]; rng.shuffle(data); n=len(data); a=int(n*ratios[0]); b=a+int(n*ratios[1])
    return {'train':data[:a],'val':data[a:b],'test':data[b:]}

def has_leakage(splits:dict[str,list[Path]])->bool:
    """Проверяет утечку одинаковых файлов между выборками."""
    seen={}
    for name,paths in splits.items():
        for p in paths:
            h=image_hash(p)
            if h in seen and seen[h]!=name: return True
            seen[h]=name
    return False
