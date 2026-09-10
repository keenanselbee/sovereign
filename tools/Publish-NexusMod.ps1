[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$ArchivePath, [switch]$Publish)
$ErrorActionPreference = "Stop"
$arguments = @((Join-Path $PSScriptRoot 'nexus_publish.py'), '--archive', $ArchivePath)
if ($Publish) { $arguments += '--publish' }
& python @arguments
exit $LASTEXITCODE
