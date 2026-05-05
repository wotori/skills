#!/usr/bin/env bash
set -euo pipefail

target="${1:-$(pwd)}"
quality="${MP3_QUALITY:-2}"
overwrite="${OVERWRITE:-0}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg is not installed." >&2
  echo "macOS: brew install ffmpeg" >&2
  echo "Ubuntu/Debian: sudo apt-get update && sudo apt-get install ffmpeg" >&2
  echo "Fedora/RHEL: sudo dnf install ffmpeg" >&2
  exit 1
fi

if [[ ! -e "$target" ]]; then
  echo "Error: path does not exist: $target" >&2
  exit 1
fi

convert_one() {
  local input="$1"
  local output="${input%.*}.mp3"
  local tmp="${output}.tmp"

  if [[ -e "$output" && "$overwrite" != "1" ]]; then
    echo "skip: $output already exists"
    return
  fi

  echo "convert: $input -> $output"
  rm -f "$tmp"
  ffmpeg -hide_banner -loglevel warning -stats \
    -y \
    -i "$input" \
    -map 0:a:0 \
    -map_metadata 0 \
    -vn \
    -codec:a libmp3lame \
    -q:a "$quality" \
    -id3v2_version 3 \
    "$tmp"
  mv "$tmp" "$output"
}

if [[ -f "$target" ]]; then
  case "${target,,}" in
    *.flac|*.wav|*.aiff|*.aif|*.ape|*.wv|*.m4a) convert_one "$target" ;;
    *) echo "Error: unsupported extension: $target" >&2; exit 1 ;;
  esac
else
  while IFS= read -r -d '' file; do
    convert_one "$file"
  done < <(find "$target" -type f \( \
    -iname '*.flac' -o \
    -iname '*.wav' -o \
    -iname '*.aiff' -o \
    -iname '*.aif' -o \
    -iname '*.ape' -o \
    -iname '*.wv' -o \
    -iname '*.m4a' \
  \) -print0 | sort -z)
fi
