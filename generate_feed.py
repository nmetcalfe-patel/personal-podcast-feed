#!/usr/bin/env python3
"""
Rebuilds feed.xml from episodes.json.

Run standalone if you've hand-edited episodes.json:
    python generate_feed.py

Normally called automatically by publish_episode.py after it adds a new episode.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "episodes.json"
FEED_OUT = HERE / "feed.xml"

PAGES_BASE = "https://nmetcalfe-patel.github.io/personal-podcast-feed"

CHANNEL_TITLE = "Personal Podcast"
CHANNEL_DESCRIPTION = (
    "A self-tuning personal news podcast, hosted by Priya (tech & AI), "
    "Jim (business & economy) and Nell (politics & the world) — plus a shorter "
    "personal digest and on-demand deep dives."
)
CHANNEL_LANGUAGE = "en-gb"
CHANNEL_AUTHOR = "Priya, Jim & Nell"
CHANNEL_CATEGORY = "News"

SHOW_LABELS = {
    "main": "Main",
    "digest": "Digest",
    "followup": "Deep Dive",
}


def load_episodes() -> list[dict]:
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def parse_pub_date(raw: str) -> datetime:
    # episodes.json stores ISO8601; be lenient about a bare date (no time/offset).
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return datetime.fromisoformat(raw + "T06:00:00+00:00")


def build_item(ep: dict) -> str:
    dt = parse_pub_date(ep["pub_date"])
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    pub_rfc2822 = format_datetime(dt)

    label = SHOW_LABELS.get(ep.get("show", ""), "")
    title = f"[{label}] {ep['title']}" if label else ep["title"]
    audio_url = f"{PAGES_BASE}/episodes/{ep['filename']}"

    return f"""    <item>
      <title>{escape(title)}</title>
      <description>{escape(ep.get('description', ''))}</description>
      <pubDate>{pub_rfc2822}</pubDate>
      <guid isPermaLink="false">{escape(ep['guid'])}</guid>
      <enclosure url="{escape(audio_url)}" length="{ep.get('file_size_bytes', 0)}" type="audio/mpeg" />
      <itunes:duration>{ep.get('duration_seconds', 0)}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>"""


def build_feed(episodes: list[dict]) -> str:
    episodes_sorted = sorted(episodes, key=lambda e: parse_pub_date(e["pub_date"]), reverse=True)
    items = "\n".join(build_item(ep) for ep in episodes_sorted)
    now_rfc2822 = format_datetime(datetime.now(timezone.utc))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(CHANNEL_TITLE)}</title>
    <link>{PAGES_BASE}</link>
    <atom:link href="{PAGES_BASE}/feed.xml" rel="self" type="application/rss+xml" />
    <description>{escape(CHANNEL_DESCRIPTION)}</description>
    <language>{CHANNEL_LANGUAGE}</language>
    <lastBuildDate>{now_rfc2822}</lastBuildDate>
    <itunes:author>{escape(CHANNEL_AUTHOR)}</itunes:author>
    <itunes:category text="{CHANNEL_CATEGORY}" />
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>episodic</itunes:type>
{items}
  </channel>
</rss>
"""


def main():
    episodes = load_episodes()
    feed_xml = build_feed(episodes)
    FEED_OUT.write_text(feed_xml, encoding="utf-8")
    print(f"WROTE {FEED_OUT} ({len(episodes)} episodes)")


if __name__ == "__main__":
    main()
