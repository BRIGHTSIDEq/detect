from pathlib import Path
Path('artifacts/reports').mkdir(parents=True, exist_ok=True)
Path('artifacts/reports/model_benchmark.md').write_text('# Короткий benchmark моделей\n\nПосле запуска с данными сюда записываются mAP, latency, VRAM и размер. Кандидаты: YOLO11n, YOLOv8n, SSD Lite MobileNetV3.\n', encoding='utf-8')
