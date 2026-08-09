# Personal Podcast — Feed

This repo exists for one reason: to serve a podcast RSS feed (via GitHub Pages) so the episodes produced by the private `Personal-Podcast` project can be added to a normal podcast app.

**This repo is public** (required for free GitHub Pages) but only ever contains the finished audio, episode titles/dates/descriptions, and the generated feed — never research notes, sourcing, prompts, or the tooling that decides what gets covered. That stays in the private source repo.

## Structure
- `feed.xml` — the generated podcast RSS feed. Served at the Pages URL once Pages is enabled.
- `episodes/` — published MP3s.
- `episodes.json` — manifest the feed is generated from (title, date, description, filename, duration, size, show type).
- `generate_feed.py` — rebuilds `feed.xml` from `episodes.json`. Run after editing the manifest by hand; normally called automatically by `publish_episode.py`.
- `publish_episode.py` — takes a finished episode script (`.md` + matching `.mp3`) from the source repo, copies the audio here, extracts metadata, updates the manifest, regenerates the feed, and commits + pushes. Called as the final step of the source repo's `/episode` and `/deep-dive` skills.

## Subscribing
Add this URL to any podcast app: `https://nmetcalfe-patel.github.io/personal-podcast-feed/feed.xml`
