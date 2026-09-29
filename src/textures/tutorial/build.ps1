param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,
    [Parameter(Mandatory = $true)]
    [string]$WitchyBnd,
    [Parameter(Mandatory = $true)]
    [string]$Texconv
)

$ErrorActionPreference = 'Stop'
$repository = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$baseline = Join-Path $repository 'packages\textures\mod\menu\hi'
$artworks = @(
    @{ Name = 'MENU_Tuto_00016'; Image = 'deflection.png' },
    @{ Name = 'MENU_Tuto_00018'; Image = 'ultimate.png' }
)
$qualifiedBaselines = @(
    @{
        Header = 'CECC321945A93DADCB9925B31D058CB7074F56DC42513408D9C6F12D563D7241'
        Data = '015BD0BFC48B50ABCABEA656F720D672DC10A364398D59283EDA5C770200B14F'
        Target = 'B0617794B187558AB73AF528D1985D528D660DA80691010BEAE27C8E682D0A13'
    },
    @{
        Header = '4FD01F5ED33EC29BB7C37E51E34765467C7FF84FF09DDE390F1714B627ED4D22'
        Data = 'CE8EF7371ED16015FB309AE23C4A1B61194220EB3ABDA80CC54863F9751149CF'
        Target = 'C6CF6FC701FC548174472EAE5FDFDA49ED39FF2D0D12985947F3D5D8901E0759'
    },
    @{
        Header = 'E4707D8DDA184947736961ACEEF4E339A298F6141792118E43A742E0D583A862'
        Data = 'F864DFE0D10D134D1566132FC7DFB76FA11469C5C07BDF41AA4FC3183F2939CD'
        Target = '2B5ACD7ACCA092451D8F086E689C91278EEFBF78FE08713D39F29344CE460FD7'
    },
    @{
        Header = '835888BD7BE39FD84BF04770B9631B0A0F5B22EC2AADA48812633069CEAC791C'
        Data = '0B140C323FA65FC079EB6B88006F444ECF7B35480BB959DB114E30990E4D1AFE'
        Target = 'DB5303C7EAC4988BB92A837F31DEBD2EBAE979FEC011F82BB58060DD94161847'
    }
)

if ((Test-Path -LiteralPath $OutputDirectory) -and (Get-ChildItem -LiteralPath $OutputDirectory -Force | Select-Object -First 1)) {
    throw 'OutputDirectory must be empty so an earlier candidate cannot be overwritten.'
}
$headerHash = (Get-FileHash -LiteralPath (Join-Path $baseline '00_solo.tpfbhd')).Hash
$dataHash = (Get-FileHash -LiteralPath (Join-Path $baseline '00_solo.tpfbdt')).Hash
$qualified = $qualifiedBaselines | Where-Object { $_.Header -ceq $headerHash -and $_.Data -ceq $dataHash } | Select-Object -First 1
if (-not $qualified) { throw 'The texture-pair baseline changed; requalify the archive before rebuilding.' }

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $baseline '00_solo.tpfbhd') -Destination $OutputDirectory
Copy-Item -LiteralPath (Join-Path $baseline '00_solo.tpfbdt') -Destination $OutputDirectory
$archive = Join-Path $OutputDirectory '00_solo.tpfbhd'
& $WitchyBnd --silent --bnd --unpack $archive
if ($LASTEXITCODE -ne 0) { throw 'WitchyBND failed to unpack the texture pair.' }

foreach ($art in $artworks) {
    $artwork = Join-Path $PSScriptRoot $art.Image
    $member = Join-Path $OutputDirectory ('00_solo-tpfbhd\' + $art.Name + '.tpf.dcx')
    if ($art.Name -eq 'MENU_Tuto_00016' -and (Get-FileHash -LiteralPath $member).Hash -cne $qualified.Target) {
        throw 'The tutorial member does not match the qualified texture-pair baseline.'
    }
    & $WitchyBnd --silent --unpack $member
    if ($LASTEXITCODE -ne 0) { throw 'WitchyBND failed to unpack the tutorial TPF.' }
    $texture = Join-Path $OutputDirectory ('00_solo-tpfbhd\' + $art.Name + '-tpf-dcx\' + $art.Name + '.dds')
    $original = [IO.File]::ReadAllBytes($texture)

    & $Texconv -nologo -nogpu -bcmax -f BC7_UNORM -m 1 -w 544 -h 336 -if CUBIC -o $OutputDirectory -y $artwork
    if ($LASTEXITCODE -ne 0) { throw 'texconv failed to encode the approved artwork.' }
    $encoded = [IO.File]::ReadAllBytes((Join-Path $OutputDirectory ([IO.Path]::GetFileNameWithoutExtension($art.Image) + '.DDS')))
    if ($original.Length -ne 182932 -or $encoded.Length -ne $original.Length -or
        [BitConverter]::ToInt32($original, 128) -ne 98 -or [BitConverter]::ToInt32($encoded, 128) -ne 98 -or
        [BitConverter]::ToInt32($original, 16) -ne 544 -or [BitConverter]::ToInt32($original, 12) -ne 336 -or
        [BitConverter]::ToInt32($encoded, 16) -ne 544 -or [BitConverter]::ToInt32($encoded, 12) -ne 336) {
        throw 'The original and encoded DDS formats do not match the qualified 544x336 BC7 layout.'
    }
    # texconv sets a one-mip header flag that the original DDS omits. Retain every
    # original header byte; only the BC7 blocks carry the new tutorial artwork.
    [Array]::Copy($original, $encoded, 148)
    [IO.File]::WriteAllBytes($texture, $encoded)

    & $WitchyBnd --silent --repack (Split-Path $texture)
    if ($LASTEXITCODE -ne 0) { throw 'WitchyBND failed to repack the tutorial TPF.' }
}
& $WitchyBnd --silent --bnd --repack (Join-Path $OutputDirectory '00_solo-tpfbhd')
if ($LASTEXITCODE -ne 0) { throw 'WitchyBND failed to repack the texture pair.' }

Get-FileHash -LiteralPath (Join-Path $OutputDirectory '00_solo.tpfbhd'), (Join-Path $OutputDirectory '00_solo.tpfbdt') |
    Select-Object Path, Hash
