# This script generates a Python client for a specified module using OpenAPI specs.
# It uses the `openapi-python-client` tool to generate the client code and `ruff` for linting.
# The output will be placed in the `heimdall_api_client` directory.
# Usage:
#   .\generate-module-client.ps1 -Module <ModuleName> [-version <Version>]
param (
    [Parameter(Mandatory = $true)]
    [string]$Module,
    [Parameter(Mandatory = $false)]
    [string]$version = "v1"
)

$ErrorActionPreference = "Stop"

# Base URL to OpenAPI specs
$baseSpecUrl = "https://external-api.heimdallcloud.com/openapi"
$specFileName = "openapi.yaml" # Using the YAML format for OpenAPI spec
$specUrl = "$baseSpecUrl/$Module/$version/$specFileName" 
$specDir = "/specs/$Module"
$specPath = "$specDir/$specFileName"

# Generated output folder and target destination
$generatedFolder = "${Module}_client"
$targetPath = "../heimdall_api_client"

# Check if openapi-python-client is installed
python -m openapi_python_client --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing 'openapi-python-client'..."
    python -m pip install openapi-python-client
}
else {
    Write-Host "'openapi-python-client' is already installed."
}

# Check if ruff is installed for linting
python -m ruff --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing 'ruff'..."
    python -m pip install ruff
}
else {
    Write-Host "'ruff' is already installed."
}

# Ensure specs/<module>/ directory exists
if (!(Test-Path $specDir)) {
    New-Item -ItemType Directory -Force -Path $specDir | Out-Null
}
else {
    Remove-Item -Recurse -Force "$specDir/*" -ErrorAction Silently
}

# Download the OpenAPI spec
Write-Host "Downloading OpenAPI spec from $specUrl to $specPath..."
Invoke-WebRequest -Uri $specUrl -OutFile $specPath

# Generate the client
Write-Host "Generating client for module '$Module'..."
python -m openapi_python_client generate `
    --path $specPath --overwrite --output-path $generatedFolder --config openapi_python_client_config.yaml

# Remove the generated README, .gitignore, and pyproject.toml files
Write-Host "Cleaning up generated files in..."
Remove-Item -Path "$generatedFolder/README.md" -ErrorAction SilentlyContinue
Remove-Item -Path "$generatedFolder/.gitignore" -ErrorAction SilentlyContinue
Remove-Item -Path "$generatedFolder/pyproject.toml" -ErrorAction SilentlyContinue

# Remove the generated client folder if it exists
$existingClientPath = Join-Path -Path $targetPath -ChildPath "${Module}_api_client"
if (Test-Path $existingClientPath) {
    Write-Host "Removing existing client at $existingClientPath..."
    Remove-Item -Recurse -Force $existingClientPath
}

# Move generated client to heimdall_api_client
$clientCodePath = Join-Path -Path $generatedFolder -ChildPath "${Module}_api_client"
Write-Host "Moving generated client at $clientCodePath to $targetPath..."
Move-Item $clientCodePath $targetPath
Remove-Item -Recurse -Force $generatedFolder

# Clean up the specs folder and remove the folder
Write-Host "Cleaning up specs directory..."
Remove-Item -Recurse -Force $specDir

Write-Host "Done. Module '$Module' client is ready at $targetPath"