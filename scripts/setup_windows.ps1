$ErrorActionPreference = "Stop"
Write-Host "Object Lens: Windows setup" -ForegroundColor Green

$pythonLauncher = "py"
$pythonArgs = @("-3.12")
try {
    & $pythonLauncher @pythonArgs --version | Out-Host
} catch {
    $pythonLauncher = "python"
    $pythonArgs = @()
    & $pythonLauncher --version | Out-Host
}

if (!(Test-Path ".venv")) {
    & $pythonLauncher @pythonArgs -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements-lock.txt
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('CUDA device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'not available')"
Write-Host "Готово. Для проверки запустите: .\scripts\one_click.ps1" -ForegroundColor Green
