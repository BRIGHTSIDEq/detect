from pathlib import Path
import yaml

def load_yaml(path: Path) -> dict:
    """Загружает YAML-конфигурацию."""
    if not path.exists(): raise FileNotFoundError(f"Файл конфигурации не найден: {path}")
    with path.open('r',encoding='utf-8') as f: return yaml.safe_load(f) or {}

def load_classes(path: Path) -> list[dict]:
    """Загружает и проверяет список классов."""
    data=load_yaml(path); classes=data.get('classes',[])
    names=[c.get('name') for c in classes]
    if len(names)!=len(set(names)): raise ValueError('Найдены повторяющиеся классы')
    return classes
