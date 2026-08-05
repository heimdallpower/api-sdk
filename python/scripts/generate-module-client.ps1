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
$specDir = "./specs/$Module"
$specPath = "$specDir/$specFileName"

# Generated output folder and target destination
$generatedFolder = "${Module}_client"
$targetPath = "../heimdall_api_client"

# Check if openapi-python-client is installed
$requiredVersion = "0.28.3"  # Pin the version here

# Ensure correct version of openapi-python-client is installed
$installedVersion = python -m openapi_python_client --version 2>$null
if ($LASTEXITCODE -ne 0 -or $installedVersion -notmatch [regex]::Escape($requiredVersion)) {
    Write-Host "Installing 'openapi-python-client' version $requiredVersion..."
    python -m pip install "openapi-python-client==$requiredVersion" --quiet
} else {
    Write-Host "'openapi-python-client' $requiredVersion is already installed."
}

# Warn if a newer version is available on PyPI
try {
    $pypiInfo = Invoke-RestMethod -Uri "https://pypi.org/pypi/openapi-python-client/json" -ErrorAction Stop
    $latestVersion = $pypiInfo.info.version
    if ($latestVersion -ne $requiredVersion) {
        Write-Host "WARNING: A newer version of 'openapi-python-client' is available ($latestVersion). Currently pinned to $requiredVersion. Edit in 'generate-module-client.ps1'" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Could not check PyPI for latest 'openapi-python-client' version." -ForegroundColor DarkYellow
}

# Ensure ruff is available to the interpreter that runs the generator.
# openapi-python-client formats its output via the post_hooks in
# openapi_python_client_config.yaml, which call 'python -m ruff'. Probing the
# module (not the 'ruff' executable) is what those hooks actually need: pip
# installs ruff.exe into a Scripts directory that is often not on PATH, and the
# generator only warns when a hook fails, leaving the output unformatted.
python -m ruff --version 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing 'ruff'..."
    python -m pip install ruff --quiet
    python -m ruff --version 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "'python -m ruff' is still unavailable after install; generated code would be left unformatted."
    }
}
else {
    Write-Host "'ruff' is already installed."
}

# Ensure specs/<module>/ directory exists
if (!(Test-Path $specDir)) {
    New-Item -ItemType Directory -Force -Path $specDir | Out-Null
}
else {
    Remove-Item -Recurse -Force "$specDir/*" -ErrorAction SilentlyContinue
}

# Download the OpenAPI spec
Write-Host "Downloading OpenAPI spec from $specUrl to $specPath..."
Invoke-WebRequest -Uri $specUrl -OutFile $specPath

# Generate the client
Write-Host "Generating client for module '$Module'..."
python -m openapi_python_client generate `
    --path $specPath --overwrite --output-path $generatedFolder --config openapi_python_client_config.yaml

# Verify the post_hooks actually formatted the output. A hook failure is only a
# warning to the generator, and unformatted code shows up as a diff touching
# every file in the package rather than just the endpoints that changed.
# Runs before the metadata cleanup below so ruff resolves the same config the
# post_hooks used: the generated project's own pyproject.toml.
Write-Host "Verifying generated code is formatted..."
python -m ruff format --check $generatedFolder | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Generated code is not formatted: the post_hooks in openapi_python_client_config.yaml did not run. Aborting rather than producing a whole-package diff."
}

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
