from ultralytics import YOLO
model=YOLO('artifacts/checkpoints/best.pt')
model.val(data='configs/data.yaml', plots=True, project='artifacts/reports')
