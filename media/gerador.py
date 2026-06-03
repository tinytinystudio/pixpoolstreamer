#!/usr/bin/env python3
import argparse
import base64
from pathlib import Path


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fullscreen WebP Player</title>
  <style>
    html, body {{
      margin: 0;
      width: 100%;
      height: 100%;
      background: black;
      overflow: hidden;
    }}

    .player {{
      width: 100vw;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: black;
    }}

    img {{
      width: 100vw;
      height: 100vh;
      object-fit: contain;
      background: black;
    }}
  </style>
</head>
<body>
  <div class="player">
    <img src="data:image/webp;base64,{base64_data}" alt="WebP animation" />
  </div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate a self-contained fullscreen HTML page for an animated WebP."
    )
    parser.add_argument("video_file", help="Path to the .webp file")
    parser.add_argument("output_html", help="Output HTML file name")

    args = parser.parse_args()

    video_path = Path(args.video_file)
    output_path = Path(args.output_html)

    if not video_path.exists():
        raise FileNotFoundError(f"File not found: {video_path}")

    if video_path.suffix.lower() != ".webp":
        raise ValueError("Input file must be a .webp file")

    encoded = base64.b64encode(video_path.read_bytes()).decode("ascii")

    html = HTML_TEMPLATE.format(base64_data=encoded)

    output_path.write_text(html, encoding="utf-8")

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()