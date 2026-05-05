---
name: lossless-to-mp3
description: Convert lossless audio albums and tracks such as FLAC, ALAC, WAV, AIFF, APE, and WavPack to high-quality MP3 with much smaller file size, preserving metadata when possible, placing MP3 files next to originals, and splitting CUE albums into named MP3 tracks.
---

# Lossless to MP3

Use this skill when the user wants to transcode lossless music to MP3 while keeping quality high and file size meaningfully smaller than the source. Prefer deterministic local tools over ad hoc commands.

## Quality Policy

- Default to LAME VBR `-q:a 2`: transparent or near-transparent for most music, usually far smaller than FLAC/WAV/AIFF.
- Use `-q:a 0` only when the user explicitly asks for maximum MP3 quality and accepts larger files.
- Do not use low fixed bitrates unless the user asks for very small files.
- Preserve source files. Write MP3 outputs beside the original file, or for CUE albums into an adjacent `tracks/` directory.
- Skip existing MP3 files unless the user explicitly asks to overwrite.

## Dependencies

Check first:

```bash
ffmpeg -version
python3 --version
```

Install on macOS:

```bash
brew install ffmpeg
```

Install on Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install ffmpeg python3
```

Install on Fedora/RHEL:

```bash
sudo dnf install ffmpeg python3
```

Optional metadata editing beyond ffmpeg:

```bash
python3 -m pip install mutagen
```

If macOS Python reports an externally managed environment, use a virtual environment or:

```bash
python3 -m pip install --break-system-packages mutagen
```

## Fast Workflow

1. Inspect the target path and identify whether it is ordinary lossless files or a CUE album.
2. Verify `ffmpeg` exists. If not, tell the user the exact install command for their OS.
3. For ordinary files, run:

```bash
bash scripts/convert_lossless_to_mp3.sh "/path/to/music"
```

4. For one CUE sheet with one or more referenced lossless files, run:

```bash
python3 scripts/cue_to_mp3.py "/path/to/album/album.cue"
```

5. Verify output count, file names, and sample metadata with `ffprobe`.

## Ordinary Lossless Files

Use `scripts/convert_lossless_to_mp3.sh` for `.flac`, `.wav`, `.aiff`, `.aif`, `.ape`, `.wv`, and likely ALAC `.m4a` files. It writes:

```text
Song.flac -> Song.mp3
```

Useful options:

```bash
MP3_QUALITY=0 bash scripts/convert_lossless_to_mp3.sh "/path/to/music"
OVERWRITE=1 bash scripts/convert_lossless_to_mp3.sh "/path/to/music"
```

## CUE Albums

Use `scripts/cue_to_mp3.py` when an album folder contains `.cue` plus one or more referenced lossless files. It writes MP3s to:

```text
Album Folder/tracks/01 - Track Title.mp3
```

The script reads common CUE fields: `FILE`, `TRACK`, `TITLE`, `PERFORMER`, and `INDEX 01`. It embeds track title, track number, album title, artist, and `cover.jpg` when present.

Example:

```bash
python3 scripts/cue_to_mp3.py "/Music/Album/album.cue" --quality 2
python3 scripts/cue_to_mp3.py "/Music/Album/album.cue" --quality 0 --overwrite
```

## TXT Metadata Pattern From Existing Code

If the album has a simple metadata `.txt`, follow this existing convention:

- First line: album title.
- Last line: artist; discard text after the first comma for the artist name.
- Ignore `Side ...` and `Сторона ...` lines.
- Lines containing `BWV` without a track number are work titles.
- Lines without `BWV` and without a track number are work groups.
- Track lines are `NN - Track Title`.
- Rename MP3 files as `NN - Full Title.mp3` after metadata is applied.

If the repository also includes `set_metadata_from_txt.py`, prefer using it for that specific TXT format:

```bash
python3 src/set_metadata_from_txt.py "/path/to/album/tracks" "/path/to/album/metadata.txt" "1972"
```

## Verification

After conversion, run:

```bash
find "/path/to/music" -name "*.mp3" -type f | sort
ffprobe -hide_banner "/path/to/music/example.mp3"
```

Confirm:

- MP3 files exist beside originals or under `tracks/` for CUE albums.
- Originals still exist.
- MP3 sizes are smaller than source lossless files.
- Tags and file names are readable.
