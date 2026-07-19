from pathlib import Path
from object_recognition.configuration.config import load_classes

def test_classes_unique():
    classes=load_classes(Path('configs/classes.yaml'))
    assert len(classes)>=50
    assert len({c['name'] for c in classes})==len(classes)
