<#
.SYNOPSIS
    Checks the local prerequisites for building and testing both SDKs.

.DESCRIPTION
    Installs nothing and writes no files: missing tools are reported with install hints.
    Also reports whether the integration-test credentials are present in
    $env:HEIMDALL_CLIENT_ID / $env:HEIMDALL_CLIENT_SECRET, without printing their values.
    Exit code 1 when a required tool is missing.

.EXAMPLE
    ./scripts/check-prerequisites.ps1
#>
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSAvoidUsingWriteHost', '', Justification = 'Interactive status output that must not enter the pipeline')]
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$script:missing = 0

function Write-Ok([string]$Name) { Write-Host "  ok       $Name" }
function Write-Missing([string]$Name, [string]$Hint) {
    Write-Host "  MISSING  $Name" -ForegroundColor Red
    Write-Host "           hint: $Hint"
    $script:missing++
}
function Write-Warn([string]$Name, [string]$Hint) {
    Write-Host "  warning  $Name" -ForegroundColor Yellow
    Write-Host "           hint: $Hint"
}
function Test-Command([string]$Name) { [bool](Get-Command $Name -ErrorAction SilentlyContinue) }

Write-Host 'Checking prerequisites'

# .NET: projects target net10.0; CI uses dotnet-version 10.0.x
$sdk = if (Test-Command dotnet) { dotnet --list-sdks 2>$null | Where-Object { $_ -match '^10\.' } | Select-Object -Last 1 }
if ($sdk) { Write-Ok ".NET SDK 10 ($(($sdk -split ' ')[0]))" }
else { Write-Missing '.NET SDK 10.x' 'https://dotnet.microsoft.com/download/dotnet/10.0' }

# Python: pyproject requires-python >=3.11
$python = @('python3', 'python') | Where-Object { Test-Command $_ } | Select-Object -First 1
$pythonOk = $false
if ($python) {
    & $python -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>$null
    $pythonOk = ($LASTEXITCODE -eq 0)
}
if ($pythonOk) { Write-Ok "Python >= 3.11 ($(& $python -c 'import platform; print(platform.python_version())'))" }
else { Write-Missing 'Python >= 3.11' 'https://www.python.org/downloads/' }

# Poetry: pyproject uses the PEP 621 [project] table, supported from Poetry 2.0
if (Test-Command poetry) {
    $poetryVersion = [regex]::Match((poetry --version 2>$null), '\d+\.\d+(\.\d+)?').Value
    if ($poetryVersion -and [version]$poetryVersion -ge [version]'2.0') { Write-Ok "Poetry >= 2.0 ($poetryVersion)" }
    else { Write-Missing "Poetry >= 2.0 (found: $poetryVersion)" 'poetry self update  (or: pipx upgrade poetry)' }
}
else { Write-Missing 'Poetry >= 2.0' 'https://python-poetry.org/docs/#installation  (or: pipx install poetry)' }

# PowerShell 7: only needed to regenerate the Python clients
if ($PSVersionTable.PSVersion.Major -ge 7) { Write-Ok "PowerShell ($($PSVersionTable.PSVersion))" }
else { Write-Warn 'PowerShell 7 (pwsh) - only needed for python/scripts/generate-module-client.ps1' 'https://learn.microsoft.com/powershell/scripting/install/installing-powershell' }

Write-Host 'Checking integration-test credentials'
foreach ($name in 'HEIMDALL_CLIENT_ID', 'HEIMDALL_CLIENT_SECRET') {
    # Only the presence is checked; the value is never read into output.
    if ([string]::IsNullOrEmpty([Environment]::GetEnvironmentVariable($name))) {
        Write-Warn "$name is not set - only needed for integration tests" 'set these to credentials for a Heimdall API client; contact Heimdall Power to obtain API access'
    }
    else { Write-Ok "$name is set (hidden)" }
}

if ($script:missing -gt 0) {
    Write-Host "$($script:missing) required tool(s) missing - see hints above."
    exit 1
}
