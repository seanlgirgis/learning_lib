# env_setter.ps1
# 1. Ensure the local Python path is prioritized in this session
$env:Path = "C:\pyver\py312;" + $env:Path

# 2. Define the Virtual Environment path
$venvPath = "C:\py_venv\learning_lib_venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

# 3. Check and Activate
if (Test-Path $activateScript) {
    # Set execution policy for this session only to allow the script to run
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
    
    & $activateScript
    Write-Host "--- AWS Developer Environment ---" -ForegroundColor Yellow
    Write-Host "Status: Virtual environment activated" -ForegroundColor Green
    Write-Host "Venv Path: $venvPath" -ForegroundColor Gray
    Write-Host "Python: $(Get-Command python | Select-Object -ExpandProperty Source)" -ForegroundColor Cyan
}
else {
    Write-Host "Error: Activation script not found at $activateScript" -ForegroundColor Red
}