[CmdletBinding(DefaultParameterSetName = 'Run')]
param(
    [Parameter(Mandatory, ParameterSetName = 'Run')]
    [ValidateSet('params', 'maps', 'text', 'item-text', 'hks', 'animations', 'sfx', 'events', 'talk', 'models', 'textures')]
    [string]$Scope,
    [Parameter(ParameterSetName = 'Run')]
    [ValidateSet('editor', 'repo')]
    [string]$Source = 'editor',
    [Parameter(ParameterSetName = 'Run')]
    [ValidateSet('main', 'textures')]
    [string]$Package = 'main',
    [string]$Profile,
    [switch]$StageOnly,
    [Parameter(ParameterSetName = 'Run')]
    [string]$Version,
    [Parameter(ParameterSetName = 'Run')]
    [string]$Qualification,
    [Parameter(Mandatory, ParameterSetName = 'Resume')]
    [string]$Receipt,
    [ValidateRange(1, 600)]
    [int]$WaitSeconds = 120
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $PSScriptRoot 'propagate_workflow.py'
$pythonCommand = Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1
if ($PSCmdlet.ParameterSetName -eq 'Resume') {
    $runnerArguments = @($runner, 'resume', '--receipt', $Receipt)
} else {
    if ([string]::IsNullOrWhiteSpace($Version)) {
        # Use the checked regular version; changed staged payloads require a version bump.
        $Version = & $pythonCommand.Source (Join-Path $PSScriptRoot 'release_workflow.py') target-version
        if ($LASTEXITCODE -ne 0) { throw 'Release target/changelog check failed; no propagation started.' }
    }
    if ($Scope -eq 'item-text') { $Scope = 'file:msg/engus/item_dlc02.msgbnd.dcx' }
    $runnerArguments = @($runner, 'run', '--scope', $Scope, '--from', $Source,
        '--package', $Package, '--version', $Version)
    if ($Qualification) { $runnerArguments += @('--qualification', $Qualification) }
}
$runnerArguments += @('--wait-seconds', [string]$WaitSeconds)
if ($Profile) { $runnerArguments += @('--profile', $Profile) }
if ($StageOnly) { $runnerArguments += '--stage-only' }

$logDirectory = Join-Path $repoRoot '.sovereign\propagation-logs'
New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$logPath = Join-Path $logDirectory (([Guid]::NewGuid().ToString('N')) + '.log')
Start-Transcript -LiteralPath $logPath -NoClobber | Out-Null
Write-Host "Propagation log: $logPath"
Push-Location -LiteralPath $repoRoot
try {
    & $pythonCommand.Source @runnerArguments | Out-Host
    $resultCode = $LASTEXITCODE
    if ($resultCode -eq 2) {
        Write-Host 'Vortex will continue queued finalization when ready. Use -Receipt <printed receipt> with the original profile/stage-only options to refresh local results.'
    }
    exit $resultCode
} finally {
    Pop-Location
    Stop-Transcript | Out-Null
}
