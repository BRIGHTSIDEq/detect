from pathlib import Path
Path('data/raw').mkdir(parents=True, exist_ok=True)
print('Скачайте COCO через Ultralytics и Open Images под выбранные классы: python scripts/prepare_dataset.py --source open-images')
