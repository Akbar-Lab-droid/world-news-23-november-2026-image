# The World in One Page — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Akbar-Lab-Droid/world-news-23-november-2026-image/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Akbar-Lab-Droid/world-news-23-november-2026-image/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A single 1024×1024 broadsheet image summing up the world news of
**Monday 23 November 2026** — 60 verified stories in one page.

## The front page

- **Hero:** COP31 collapses without a deal in Antalya — the longest COP in
  history and the first outright failure since Copenhagen 2009. The final
  draft never mentioned "fossil fuels"; the EU and others rejected it.
- **Secondary:** Democrats win at least 258 US House seats (largest majority
  since 1992); Iran strikes Bahrain as tankers are hit in Hormuz; a Russian
  corvette is reported destroyed off Libya.
- **Grid:** 56 more stories in 8 sections — War & Diplomacy, Climate &
  Environment, US & World Politics, Economy & Markets, Technology & AI,
  Disaster, Transport & Aid, Sport, and Culture & More.

Every story was verified against wire and major-outlet reporting
(AP, Reuters, AFP, CNN, Al Jazeera, Yonhap, NDTV, The Hindu, Times of India,
CNA, Nikkei Asia, Le Monde) on 23 November 2026.

## Run

Requires Python 3 and Pillow, plus the Liberation fonts (present on most
Linux systems).

```bash
python3 main.py        # renders /output/entry.png (1024x1024, < 1 MiB)
```

The render is fully deterministic — no randomness, no clock, no network —
so running it twice produces a byte-identical PNG (same SHA-256).

## Files

- `draw.py` — the whole page: layout, text and all 60 stories, written from
  scratch for this edition. Prints a warning count; a clean run prints 0.
- `main.py` — entry point; creates `/output` if needed and writes
  `/output/entry.png`.
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
