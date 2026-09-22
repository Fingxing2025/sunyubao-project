param(
    [string]$Version = "codex-pet",
    [string]$Destination = ""
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Join-Path $repoRoot $Version

if (-not (Test-Path -Path $sourceDir -PathType Container)) {
  Write-Error "错误：未找到版本目录: $sourceDir`
可用版本: codex-pet / codex-pet-smooth / codex-pet-gait-fix / codex-pet-fluid / codex-pet-foot-forward"
  exit 1
}

$destRoot = if ($Destination) {
  $Destination
} else {
  Join-Path $env:USERPROFILE '.codex\pets\sunyu-baobao'
}
$zipFile = Get-ChildItem -Path $sourceDir -Filter *.zip -File | Select-Object -First 1
$tmpDir = Join-Path $env:TEMP ([guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null

try {
  if ($zipFile) {
    Write-Output "已检测到安装包：$($zipFile.FullName)"
    Expand-Archive -Path $zipFile.FullName -DestinationPath $tmpDir -Force

    $petJson = Get-ChildItem -Path $tmpDir -Filter pet.json -Recurse -File | Select-Object -First 1
    if (-not $petJson) {
      Write-Error '错误：安装包内未找到 pet.json'
      exit 1
    }
    $sourceInstallDir = $petJson.DirectoryName
  } else {
    $sourceInstallDir = Join-Path $sourceDir 'final'
    if (-not (Test-Path -Path $sourceInstallDir -PathType Container)) {
      Write-Error '错误：版本目录下既无 zip 安装包，也无 final 目录'
      exit 1
    }
    Write-Output '未检测到 zip，使用 final 目录直接安装。'
  }

  $sourcePetJson = Join-Path $sourceInstallDir 'pet.json'
  $sourceSpritesheet = Join-Path $sourceInstallDir 'spritesheet.webp'
  if (-not (Test-Path -Path $sourcePetJson -PathType Leaf) -or
      -not (Test-Path -Path $sourceSpritesheet -PathType Leaf)) {
    Write-Error '错误：安装源必须同时包含 pet.json 和 spritesheet.webp'
    exit 1
  }

  if (Test-Path -Path $destRoot) {
    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backupRoot = "$destRoot.backup-$timestamp"
    Move-Item -Path $destRoot -Destination $backupRoot
    Write-Output "已备份现有桌宠：$backupRoot"
  }
  New-Item -ItemType Directory -Path $destRoot -Force | Out-Null
  Copy-Item -Path $sourcePetJson, $sourceSpritesheet -Destination $destRoot -Force
  Write-Output "安装完成：$destRoot"
  Write-Output '请在 Codex 设置中刷新宠物列表并重新选择“Sunyu Baobao”。'
} finally {
  if (Test-Path -Path $tmpDir) {
    Remove-Item -Recurse -Force -Path $tmpDir
  }
}
