[CmdletBinding()]
param([switch]$Save, [switch]$LoginOnly, [string]$BackupPath = "", [switch]$Setup)
$ErrorActionPreference = "Stop"
$arguments = @((Join-Path $PSScriptRoot 'nexus_workflow.py'), 'descriptions')
if ($Save) { $arguments += '--save' }
if ($LoginOnly) { $arguments += '--login' }
if ($BackupPath) { $arguments += @('--backup', $BackupPath) }
if ($Setup) { $arguments += '--setup' }
& python @arguments
exit $LASTEXITCODE
