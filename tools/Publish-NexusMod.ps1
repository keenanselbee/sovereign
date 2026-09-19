[CmdletBinding()]
param([Parameter(Mandatory = $true)][string]$ArchivePath, [switch]$Publish,
      [ValidateSet('main', 'textures')][string]$Package = 'main',
      [string]$TexturesArchivePath, [switch]$Resume)
$ErrorActionPreference = "Stop"
$arguments = @((Join-Path $PSScriptRoot 'nexus_publish.py'), '--archive', $ArchivePath)
$arguments += @('--package', $Package)
if ($TexturesArchivePath) { $arguments += @('--textures-archive', $TexturesArchivePath) }
if ($Resume) { $arguments += '--resume' }
if ($Publish) { $arguments += '--publish' }
& python @arguments
exit $LASTEXITCODE
