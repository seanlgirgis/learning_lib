# start-pyspark-jupyter.ps1
# Simple script to run Jupyter + PySpark container with proper volume mount on Windows/PowerShell

# === CONFIG ===
$image = "quay.io/jupyter/pyspark-notebook:latest"
$localNotebooksFolder = "notebooks"   # subfolder in current dir - will be created if missing
$containerWorkDir = "/home/jovyan/work/notebooks"

# === MAIN ===

# Create the notebooks folder if it doesn't exist
if (-not (Test-Path $localNotebooksFolder)) {
    New-Item -ItemType Directory -Path $localNotebooksFolder | Out-Null
    Write-Host "Created local folder: $localNotebooksFolder"
}

# Get current directory in a safe way (full path, forward slashes for Docker)
$currentDir = $PWD.Path.Replace('\', '/')

# Build the host path for volume (forward slashes, quoted)
$hostPath = "${currentDir}/${localNotebooksFolder}"
$volumeArg = "${hostPath}:${containerWorkDir}"

Write-Host "Starting Jupyter + PySpark container..."
Write-Host "Image:          $image"
Write-Host "Volume mount:   $volumeArg"
Write-Host "Jupyter will be at: http://127.0.0.1:8888 (copy token from logs)"
Write-Host ""

# Run the container
# Use double quotes around volume, line continuation with backtick `
docker run -it --rm `
    -p 8888:8888 `
    -p 4040:4040 `
    -v "$volumeArg" `
    $image