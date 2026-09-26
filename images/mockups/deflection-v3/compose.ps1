Add-Type -AssemblyName System.Drawing
$assetRoot = $PSScriptRoot
$scene = [System.Drawing.Bitmap]::FromFile((Join-Path $assetRoot 'scene.png'))
$panel = [System.Drawing.Bitmap]::FromFile((Join-Path $assetRoot 'panel-background.png'))
$icon = [System.Drawing.Bitmap]::FromFile((Join-Path $assetRoot 'icon.png'))
$canvas = New-Object System.Drawing.Bitmap($scene.Width, $scene.Height)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.DrawImageUnscaled($scene, 0, 0)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.DrawImage($panel, [System.Drawing.Rectangle]::new(1120, 728, 420, 221))
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::Half
$graphics.DrawImage($icon, [System.Drawing.Rectangle]::new(1270, 778, 120, 120))
$canvas.Save((Join-Path $assetRoot 'mockup.png'), [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$canvas.Dispose()
$scene.Dispose()
$panel.Dispose()
$icon.Dispose()
