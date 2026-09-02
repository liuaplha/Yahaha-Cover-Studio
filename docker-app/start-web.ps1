$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectDir ".venv\Scripts\python.exe"
$dataDir = Join-Path $projectDir "data"

if (-not (Test-Path $python)) {
    throw "未找到 Python 虚拟环境。请先在 docker-app 目录执行依赖安装步骤。"
}

$env:YAHAA_DATA_DIR = $dataDir
& $python -m uvicorn app.main:app --host 127.0.0.1 --port 8899 --no-access-log
