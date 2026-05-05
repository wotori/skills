#!/usr/bin/env python3
"""Split a CUE album and transcode tracks to high-quality MP3."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def sanitize_filename(value: str, limit: int = 140) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip()
    value = re.sub(r"\s+", " ", value)
    return (value or "Untitled")[:limit].rstrip(". ")


def parse_time(value: str) -> float:
    minutes, seconds, frames = [int(part) for part in value.split(":")]
    return minutes * 60 + seconds + frames / 75.0


def ffmpeg_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def parse_cue(cue_path: Path) -> Tuple[Dict[str, str], List[Dict[str, object]]]:
    album: Dict[str, str] = {}
    tracks: List[Dict[str, object]] = []
    current_file: Optional[str] = None

    for raw_line in cue_path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        file_match = re.match(r'FILE\s+"(.+?)"', line, re.IGNORECASE)
        if file_match:
            current_file = file_match.group(1)
            continue

        track_match = re.match(r"TRACK\s+(\d+)\s+AUDIO", line, re.IGNORECASE)
        if track_match:
            tracks.append(
                {
                    "num": int(track_match.group(1)),
                    "file": current_file,
                    "title": "",
                    "performer": album.get("performer", ""),
                    "start": None,
                }
            )
            continue

        quoted_match = re.match(r'(TITLE|PERFORMER)\s+"(.+)"', line, re.IGNORECASE)
        if quoted_match:
            key = quoted_match.group(1).lower()
            value = quoted_match.group(2)
            if tracks:
                tracks[-1][key] = value
            else:
                album[key] = value
            continue

        index_match = re.match(r"INDEX\s+01\s+(\d{2}:\d{2}:\d{2})", line, re.IGNORECASE)
        if index_match and tracks:
            tracks[-1]["start"] = parse_time(index_match.group(1))

    return album, tracks


def run_ffmpeg(
    input_file: Path,
    output_file: Path,
    track: Dict[str, object],
    next_track: Optional[Dict[str, object]],
    album: Dict[str, str],
    cover: Optional[Path],
    quality: int,
    overwrite: bool,
) -> None:
    start = track.get("start")
    if start is None:
        raise ValueError(f"track {track['num']} has no INDEX 01")

    duration = None
    if next_track and next_track.get("file") == track.get("file") and next_track.get("start") is not None:
        duration = float(next_track["start"]) - float(start)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-stats",
        "-y" if overwrite else "-n",
        "-i",
        str(input_file),
        "-ss",
        ffmpeg_time(float(start)),
    ]
    if duration and duration > 0:
        cmd.extend(["-t", f"{duration:.3f}"])

    if cover:
        cmd.extend(["-i", str(cover), "-map", "0:a:0", "-map", "1:v:0", "-c:v", "copy"])
    else:
        cmd.extend(["-map", "0:a:0"])

    title = str(track.get("title") or f"Track {track['num']:02d}")
    artist = str(track.get("performer") or album.get("performer") or "")

    cmd.extend(
        [
            "-codec:a",
            "libmp3lame",
            "-q:a",
            str(quality),
            "-id3v2_version",
            "3",
            "-metadata",
            f"title={title}",
            "-metadata",
            f"track={track['num']}",
        ]
    )
    if album.get("title"):
        cmd.extend(["-metadata", f"album={album['title']}"])
    if artist:
        cmd.extend(["-metadata", f"artist={artist}", "-metadata", f"album_artist={artist}"])
    if cover:
        cmd.extend(["-metadata:s:v", "title=Album cover", "-metadata:s:v", "comment=Cover (front)"])

    tmp_output = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_output.unlink(missing_ok=True)
    cmd.append(str(tmp_output))

    subprocess.run(cmd, check=True)
    tmp_output.replace(output_file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a CUE album and transcode tracks to MP3.")
    parser.add_argument("cue", type=Path, help="Path to .cue file")
    parser.add_argument("--output", type=Path, default=None, help="Output directory; default: cue_dir/tracks")
    parser.add_argument("--quality", type=int, default=2, choices=range(0, 10), help="LAME VBR quality, 0 best/largest, 9 smallest")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing MP3 files")
    args = parser.parse_args()

    cue_path = args.cue.expanduser().resolve()
    output_dir = (args.output or cue_path.parent / "tracks").expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    album, tracks = parse_cue(cue_path)
    if not tracks:
        raise SystemExit(f"No audio tracks found in {cue_path}")

    cover = cue_path.parent / "cover.jpg"
    if not cover.exists():
        cover = None

    for index, track in enumerate(tracks):
        source_name = track.get("file")
        if not source_name:
            print(f"skip: track {track['num']} has no FILE entry")
            continue

        input_file = cue_path.parent / str(source_name)
        if not input_file.exists():
            print(f"skip: missing source file: {input_file}")
            continue

        title = str(track.get("title") or f"Track {track['num']:02d}")
        output_name = f"{int(track['num']):02d} - {sanitize_filename(title)}.mp3"
        output_file = output_dir / output_name

        if output_file.exists() and not args.overwrite:
            print(f"skip: {output_file} already exists")
            continue

        print(f"convert: {input_file.name} [{track['num']:02d}] -> {output_file.name}")
        next_track = tracks[index + 1] if index + 1 < len(tracks) else None
        run_ffmpeg(input_file, output_file, track, next_track, album, cover, args.quality, args.overwrite)


if __name__ == "__main__":
    main()
