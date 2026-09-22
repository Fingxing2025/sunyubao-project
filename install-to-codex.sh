#!/usr/bin/env bash

set -euo pipefail

VERSION_DIR="${1:-codex-pet}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$ROOT_DIR/$VERSION_DIR"
DEST_DIR="${SUNYU_PET_DEST:-$HOME/.codex/pets/sunyu-baobao}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "错误：未找到版本目录 $SOURCE_DIR"
  echo "可用版本：codex-pet / codex-pet-smooth / codex-pet-gait-fix / codex-pet-fluid / codex-pet-foot-forward"
  exit 1
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

ZIP_FILE="$(find "$SOURCE_DIR" -maxdepth 1 -type f -name '*.zip' -print -quit)"
if [[ -n "$ZIP_FILE" ]]; then
  echo "已检测到安装包：$ZIP_FILE"
  unzip -q "$ZIP_FILE" -d "$TMP_DIR"
  PET_JSON="$(find "$TMP_DIR" -type f -name pet.json -print -quit)"
  if [[ -z "$PET_JSON" ]]; then
    echo "错误：安装包内未找到 pet.json"
    exit 1
  fi
  SRC_DIR="$(dirname "$PET_JSON")"
else
  SRC_DIR="$SOURCE_DIR/final"
  if [[ ! -d "$SRC_DIR" ]]; then
    echo "错误：版本目录下既无 zip 安装包，也无 final 目录"
    exit 1
  fi
fi

if [[ ! -f "$SRC_DIR/pet.json" || ! -f "$SRC_DIR/spritesheet.webp" ]]; then
  echo "错误：安装源必须同时包含 pet.json 和 spritesheet.webp"
  exit 1
fi

mkdir -p "$(dirname "$DEST_DIR")"
if [[ -e "$DEST_DIR" ]]; then
  BACKUP_DIR="${DEST_DIR}.backup-$(date +%Y%m%d-%H%M%S)"
  mv "$DEST_DIR" "$BACKUP_DIR"
  echo "已备份现有桌宠：$BACKUP_DIR"
fi

mkdir -p "$DEST_DIR"
cp "$SRC_DIR/pet.json" "$SRC_DIR/spritesheet.webp" "$DEST_DIR/"
echo "安装完成：$DEST_DIR"
echo "请在 Codex 设置中刷新宠物列表并重新选择“Sunyu Baobao”。"
