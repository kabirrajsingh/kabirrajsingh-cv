#!/usr/bin/env python3
"""Pull the latest uploads from a YouTube channel's public RSS feed and
write them to a Jekyll data file. No API key needed - YouTube exposes
this feed for any channel at a stable, unauthenticated URL. Run on a
schedule by .github/workflows/update-videos.yml.
"""

import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCxafUUNVFXJ7wAMKE-rmgMw"  # Kabir Raj Singh
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
MAX_VIDEOS = 4
OUTPUT_PATH = pathlib.Path(__file__).resolve().parent.parent / "_data" / "videos.json"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def fetch_videos():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        root = ET.fromstring(resp.read())

    videos = []
    for entry in root.findall("atom:entry", NS)[:MAX_VIDEOS]:
        video_id = entry.find("yt:videoId", NS).text
        videos.append({
            "id": video_id,
            "title": entry.find("atom:title", NS).text,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "published": entry.find("atom:published", NS).text,
            "thumbnail": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
        })
    return videos


def main():
    videos = fetch_videos()
    OUTPUT_PATH.write_text(json.dumps(videos, indent=2) + "\n")


if __name__ == "__main__":
    main()
