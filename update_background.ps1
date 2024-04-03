$ArtworkFolder = ".\artwork"

if (-Not (Test-Path -Path $ArtworkFolder)) {
    Write-Host "Artwork folder not found: $ArtworkFolder"
    exit
}

$RandomImage = Get-ChildItem -Path $ArtworkFolder -File | Get-Random

if ($null -eq $RandomImage) {
    Write-Host "No images found in the artwork folder."
    exit
}

$ScreenResolution = "1920x1080"

$TimeStamp = Get-Date -Format "yyyyMMddHHmmss"
$ResizedImage = ".\temp\resized_image_$TimeStamp.jpg"

magick convert "$($RandomImage.FullName)" -resize "$ScreenResolution>" "$ResizedImage"

if (-Not (Test-Path -Path $ResizedImage)) {
    Write-Host "Failed to create resized image."
    exit
}

$BGcolour = magick convert "$ResizedImage" -format "%[pixel:p{0,0}]" info:

$BGcolourImage = ".\temp\bg_colour_$TimeStamp.jpg"
magick convert -size "$ScreenResolution" "xc:$BGcolour" $BGcolourImage

magick convert $BGcolourImage $ResizedImage -gravity center -composite $ResizedImage

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@
$Prefix = Get-Location
$ResizedImagePath = $ResizedImage.Replace('.\', '\artwork\')
$ResizedImagePath = Join-Path -Path $Prefix -ChildPath $ResizedImage
[Wallpaper]::SystemParametersInfo(20, 0, $ResizedImagePath, 3)

Remove-Item -Path ".\temp\*" -Recurse -Force