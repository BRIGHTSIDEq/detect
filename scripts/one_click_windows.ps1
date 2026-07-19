param(
    [switch]$RealDataset,
    [int]$MaxSamplesPerSplit = 400
)
$ErrorActionPreference = "Stop"
Write-Host "Object Lens: one-click bootstrap for Windows" -ForegroundColor Green
if (!(Test-Path ".venv")) {
    py -3.12 -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements-lock.txt
if ($RealDataset) {
    pip install fiftyone
    python scripts/download_datasets.py --preset open-images --max-samples-per-split $MaxSamplesPerSplit
} else {
    python scripts/download_datasets.py --preset coco8
}
python scripts/prepare_dataset.py
pytest -q
python scripts/benchmark.py
if ($RealDataset) {
    Write-Host "Open Images скачан. Можно запускать обучение: python scripts/train.py" -ForegroundColor Green
} else {
    Write-Host "Готово. Проверочный pipeline работает. Для реального датасета: .\scripts\one_click_windows.ps1 -RealDataset" -ForegroundColor Green
}
