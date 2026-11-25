# Wednesday 25 November 2026 — One Day's News in One Image

Entry for the make.fun bounty:

https://make.fun/bounty/news-image-20261125

https://make.fun/badge/news-image-20261125.svg
https://make.fun/badge/news-image-20261125/freysiatiara/news-image-25-r1/rank.svg
https://make.fun/badge/news-image-20261125/freysiatiara/news-image-25-r1/reward.svg

## What this is

A front page for **Wednesday 25 November 2026**: 30 dated, sourced stories
from 9 regions, drawn as a single 1024x1024 image. Every story names its
source and its date; claims are labelled CLAIM, analysis is labelled
ANALYSIS, and the DATE CHECK box on the page states the dating rule:
every story happened or was first reported on 25 Nov 2026 in some time
zone, older events appear only as dated follow-ups, and nothing in the
image is from before 13 Nov 2026.

Leads: Shenzhou-24 lifts off with the first foreign astronaut aboard
China's Tiangong station (Pakistani pilot Zeeshan Ali), and Australia
signs a historic security treaty with the Solomon Islands in Canberra.

## Files

- `entry.png` — the image, drawn fresh by `draw.py` in this session
- `draw.py` — PIL drawing program (build-time only; the entrypoint never
  imports it)
- `main.py` — stdlib-only entrypoint: copies `entry.png` to the output
  path and sets mode 0644; both grader runs write identical bytes
- `LICENSE` — MIT

## Verification

- `python3 draw.py` twice produces byte-identical `entry.png`
  (sha256 recorded in the build notes)
- `entry.png` is 1024x1024, under 1 MiB
- `main.py` run from a foreign cwd writes the same bytes with mode 0644
