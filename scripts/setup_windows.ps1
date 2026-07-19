py -3.12 -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements-lock.txt
python - <<'PY'
import torch; print('CUDA:', torch.cuda.is_available())
PY
