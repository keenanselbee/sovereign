[CmdletBinding()]
param([switch]$SkipBrowser)
$ErrorActionPreference = "Stop"
$arguments = @((Join-Path $PSScriptRoot 'nexus_workflow.py'), 'audit')
if ($SkipBrowser) { $arguments += '--skip-browser' }
& python @arguments
exit $LASTEXITCODE
