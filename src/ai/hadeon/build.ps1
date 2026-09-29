param(
    [Parameter(Mandatory = $true)][string]$TemplateBinder,
    [Parameter(Mandatory = $true)][string]$LuaCompiler,
    [Parameter(Mandatory = $true)][string]$WitchyBND,
    [Parameter(Mandatory = $true)][string]$OutputDirectory,
    [string]$ScratchDirectory = (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path '.codex-temp\hadeon-ai-build')
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$tempRoot = [IO.Path]::GetFullPath((Join-Path $repoRoot '.codex-temp'))
$outputPath = [IO.Path]::GetFullPath($OutputDirectory)
$scratchPath = [IO.Path]::GetFullPath($ScratchDirectory)
foreach ($path in @($outputPath, $scratchPath)) {
    if (-not $path.StartsWith($tempRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Build output and scratch must be under $tempRoot."
    }
}
if (Test-Path -LiteralPath $outputPath) {
    throw "OutputDirectory already exists: $outputPath"
}

foreach ($path in @($TemplateBinder, $LuaCompiler, $WitchyBND)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required input is missing: $path"
    }
}
if ([IO.Path]::GetFileName($TemplateBinder) -ne '010000_logic.luabnd.dcx') {
    throw 'TemplateBinder must be the native 010000_logic.luabnd.dcx.'
}
$witchyConfig = Join-Path (Split-Path -Parent $WitchyBND) 'appsettings.json'
if (-not (Test-Path -LiteralPath $witchyConfig -PathType Leaf) -or
    (Get-Content -LiteralPath $witchyConfig -Raw | ConvertFrom-Json).Recursive -ne $false) {
    throw 'WitchyBND Recursive must be false in its current appsettings.json.'
}
$source = Join-Path $PSScriptRoot '250090_logic.lua'
$guardPaths = @($TemplateBinder, $LuaCompiler, $WitchyBND, $witchyConfig, $source)
$inputHashes = @{}
foreach ($path in $guardPaths) {
    $inputHashes[$path] = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
}

$compilerVersion = (& $LuaCompiler -v 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0 -or $compilerVersion -notmatch 'Lua 5\.0\.2') {
    throw 'LuaCompiler must be a working Lua 5.0.2 compiler.'
}

$work = Join-Path $ScratchDirectory ([guid]::NewGuid().ToString('N'))
$candidate = Join-Path $work 'candidate'
New-Item -ItemType Directory -Force -Path $work, $candidate | Out-Null
$templateCopy = Join-Path $work '010000_logic.luabnd.dcx'
Copy-Item -LiteralPath $TemplateBinder -Destination $templateCopy

& $WitchyBND --silent --bnd --unpack $templateCopy
if ($LASTEXITCODE -ne 0) { throw 'Could not unpack native logic binder.' }
$unpacked = Join-Path $work '010000_logic-luabnd-dcx'
foreach ($name in @('010000_logic.lua', '010000_logic.luagnl', '010000_logic.luainfo', '_witchy-bnd4.xml')) {
    if (-not (Test-Path -LiteralPath (Join-Path $unpacked $name) -PathType Leaf)) {
        throw "Native binder is missing $name."
    }
}

$compiled = Join-Path $candidate '250090_logic.lua'
& $LuaCompiler -s -o $compiled $source
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $compiled -PathType Leaf)) {
    throw 'Lua 5.0.2 compilation failed.'
}
$nativeHeader = [IO.File]::ReadAllBytes((Join-Path $unpacked '010000_logic.lua'))
$builtHeader = [IO.File]::ReadAllBytes($compiled)
if ($nativeHeader.Length -lt 14 -or $builtHeader.Length -lt 14 -or
    -not [Linq.Enumerable]::SequenceEqual([byte[]]$nativeHeader[0..13], [byte[]]$builtHeader[0..13])) {
    throw 'Compiled Lua header does not match the native 64-bit Lua 5.0 format.'
}

foreach ($extension in @('luagnl', 'luainfo')) {
    $nativeMember = Join-Path $unpacked "010000_logic.$extension"
    & $WitchyBND --silent --unpack $nativeMember
    if ($LASTEXITCODE -ne 0) { throw "Could not decode native $extension metadata." }
    $xmlPath = Join-Path $unpacked "010000_logic.$extension.xml"
    [xml]$metadata = Get-Content -LiteralPath $xmlPath -Raw
    $metadata.SelectSingleNode("/$extension/filename").InnerText = "250090_logic.$extension"
    if ($extension -eq 'luagnl') {
        foreach ($node in $metadata.SelectNodes('/luagnl/globals/global')) {
            $node.InnerText = $node.InnerText.Replace('common10000', 'Hadeon250090')
        }
    } else {
        $goal = $metadata.SelectSingleNode('/luainfo/goals/goal')
        if ($goal.id -ne '10000') { throw 'Unexpected template logic goal ID.' }
        $goal.SetAttribute('id', '250090')
        $goal.name = 'Hadeon250090_Logic'
        $goal.logicinterruptname = 'Hadeon250090_Interupt'
    }
    $newXmlPath = Join-Path $candidate "250090_logic.$extension.xml"
    $metadata.Save($newXmlPath)
    & $WitchyBND --silent --repack $newXmlPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath (Join-Path $candidate "250090_logic.$extension") -PathType Leaf)) {
        throw "Could not rebuild $extension metadata."
    }
}

[xml]$manifest = Get-Content -LiteralPath (Join-Path $unpacked '_witchy-bnd4.xml') -Raw
$originalFiles = @($manifest.SelectNodes('/bnd4/files/file'))
if ($originalFiles.Count -ne 3 -or
    [string]::Join(',', @($originalFiles | ForEach-Object { $_.id })) -ne '1000,1000000,1000001') {
    throw 'Unexpected native binder member IDs.'
}
$manifest.bnd4.filename = '250090_logic.luabnd.dcx'
$manifest.bnd4.root = $manifest.bnd4.root.Replace('010000_logic', '250090_logic')
foreach ($file in $manifest.SelectNodes('/bnd4/files/file')) {
    $file.path = $file.path.Replace('010000_logic', '250090_logic')
}
$manifest.Save((Join-Path $candidate '_witchy-bnd4.xml'))
& $WitchyBND --silent --bnd --repack $candidate
if ($LASTEXITCODE -ne 0) { throw 'Could not repack Hadeon logic binder.' }
$builtBinder = Join-Path $work '250090_logic.luabnd.dcx'
if (-not (Test-Path -LiteralPath $builtBinder -PathType Leaf)) {
    throw 'WitchyBND did not produce the expected binder.'
}
foreach ($path in $guardPaths) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash -ne $inputHashes[$path]) {
        throw "Build input changed during compilation: $path"
    }
}
$receipt = [ordered]@{
    outputSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $builtBinder).Hash
    inputSha256 = $inputHashes
    memberSha256 = [ordered]@{
        lua = (Get-FileHash -Algorithm SHA256 -LiteralPath $compiled).Hash
        luagnl = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $candidate '250090_logic.luagnl')).Hash
        luainfo = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $candidate '250090_logic.luainfo')).Hash
    }
    memberIds = @(1000, 1000000, 1000001)
    logicGoalId = 250090
    commandSpeech = 1900
    commandParked = 1901
}
$receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $work 'receipt.json') -Encoding UTF8
New-Item -ItemType Directory -Path $outputPath | Out-Null
$output = Join-Path $outputPath '250090_logic.luabnd.dcx'
Copy-Item -LiteralPath $builtBinder -Destination $output
Write-Output "Built $output"
Write-Output "Scratch evidence: $work"
Write-Output "SHA256: $((Get-FileHash -Algorithm SHA256 -LiteralPath $output).Hash)"
