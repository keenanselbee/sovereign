[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('params', 'maps', 'text', 'item-text', 'hks', 'animations', 'sfx', 'events', 'talk', 'models', 'textures')]
    [string]$Scope,
    [ValidateSet('editor', 'repo')]
    [string]$Source = 'editor',
    [string]$Qualification
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $PSScriptRoot 'propagate_workflow.py'
$pythonCommand = Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1
$runtimeScope = if ($Scope -eq 'item-text') { 'file:msg/engus/item_dlc02.msgbnd.dcx' } else { $Scope }
$runnerArguments = @($runner, 'sync', '--scope', $runtimeScope, '--from', $Source)
if ($Qualification) { $runnerArguments += @('--qualification', $Qualification) }

$logDirectory = Join-Path $repoRoot '.sovereign\propagation-logs'
New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$logPath = Join-Path $logDirectory (([Guid]::NewGuid().ToString('N')) + '.log')
Start-Transcript -LiteralPath $logPath -NoClobber | Out-Null
Write-Host "Propagation log: $logPath"
Push-Location -LiteralPath $repoRoot
try {
    & $pythonCommand.Source @runnerArguments | Out-Host
    $resultCode = $LASTEXITCODE
    exit $resultCode
} finally {
    Pop-Location
    Stop-Transcript | Out-Null
}
