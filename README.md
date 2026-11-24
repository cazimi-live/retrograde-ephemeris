# Retrograde ephemeris

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24011806.svg)](https://doi.org/10.5281/zenodo.24011806)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Cazimi MCP connector](https://glama.ai/mcp/connectors/live.cazimi/retrogrades/badges/score.svg)](https://glama.ai/mcp/connectors/live.cazimi/retrogrades)

**The exact minute (UTC) of every planetary retrograde station, shadow boundary and Sun conjunction, computed from NASA JPL's DE421 ephemeris.** Mercury to Pluto for 2024–2030, and every Mercury retrograde from 1900 to 2050. Open data you can cite, from [Cazimi](https://cazimi.live). It is astronomy timing, not a horoscope.

```sh
curl https://cazimi.live/v1/planets/today.json   # which planets are retrograde today (live, no key)
```

| File | What it holds |
|---|---|
| [`data/retrogrades.json`](data/retrogrades.json) | Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto: every retrograde 2024–2030 |
| [`data/mercury-1900-2050.json`](data/mercury-1900-2050.json) | Mercury: all 476 retrograde cycles 1900–2050 |
| [`tools/retrogrades.py`](tools/retrogrades.py) | The script that generates both files (Python, [Skyfield](https://rhodesmill.org/skyfield/)) |
| [`tools/sidereal.py`](tools/sidereal.py) | Adds the sidereal (Vedic, Lahiri) signs, degrees and nakshatras |
| [`examples/`](examples) | Print the next Mercury retrograde in [Python](examples/python/next_mercury_retrograde.py) (stdlib only) or [JavaScript](examples/javascript/next-mercury-retrograde.mjs) (Node 18+) |
| [`CITATION.cff`](CITATION.cff) | Citation metadata (GitHub's "Cite this repository" button) |

**Live API · iCal · MCP · web:** [JSON API and MCP server](https://cazimi.live/methodology#api) · [retrograde calendar feed (iCal)](https://cazimi.live/retrograde-calendar) · [accuracy, checked against JPL Horizons](https://cazimi.live/accuracy) · [Mercury retrograde 2027 dates](https://cazimi.live/mercury-retrograde-2027) · [cazimi.live](https://cazimi.live)

## Cite this dataset

APA:

> Rachytskyy, M. (2026). *Planetary retrograde stations, shadows and cazimi, 2024–2030 (Mercury 1900–2050), from JPL DE421* (Version 2026.11.06) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24011806

BibTeX:

```bibtex
@dataset{rachytskyy_2026_retrograde_ephemeris,
  author    = {Rachytskyy, Max},
  title     = {Planetary retrograde stations, shadows and cazimi, 2024--2030 (Mercury 1900--2050), from {JPL} {DE421}},
  year      = {2026},
  publisher = {Zenodo},
  version   = {2026.11.06},
  doi       = {10.5281/zenodo.24011806},
  url       = {https://doi.org/10.5281/zenodo.24011806}
}
```

On a web page, a plain credit is enough: "Retrograde times: [Cazimi](https://cazimi.live), from JPL DE421."

## Quick start

```sh
git clone https://github.com/cazimi-live/retrograde-ephemeris
cd retrograde-ephemeris
python examples/python/next_mercury_retrograde.py
node examples/javascript/next-mercury-retrograde.mjs
```

```text
Mercury next retrograde, in Pisces
  pre-shadow begins   2027-01-25T18:58Z
  station retrograde  2027-02-09T17:36Z  5°59′ Pisces
  cazimi (Sun)        2027-02-18T16:39Z  29°48′ Aquarius
  station direct      2027-03-03T12:32Z  20°55′ Aquarius
  post-shadow ends    2027-03-23T14:58Z
```

Pass a date (`2031-06-01`) to ask as of another day. To read a file straight from GitHub without cloning: `https://raw.githubusercontent.com/cazimi-live/retrograde-ephemeris/main/data/retrogrades.json`.

## File format

`data/retrogrades.json` is `{"generatedAt", "source", "script", "planets": {"mercury": [cycle, ...], "venus": [...], ...}, "ayanamsa"}`. `data/mercury-1900-2050.json` is `{"mercury": [cycle, ...], "ayanamsa"}`. Cycles are in time order; each cycle is one retrograde, with the fields below. `source` states the exact method. `ayanamsa` lists the Lahiri ayanamsa on 1 January of each year.

### What each moment means

All positions are apparent geocentric ecliptic longitude of date, as seen from Earth's centre. Full method: [cazimi.live/methodology](https://cazimi.live/methodology).

| Field | Meaning |
|---|---|
| `retro` | Station retrograde: the minute the planet's ecliptic longitude rate turns negative |
| `direct` | Station direct: the minute it turns positive again |
| `pre` | Pre-shadow start: the last time before `retro` that the planet, still direct, reaches the degree of the direct station |
| `post` | Post-shadow end: the first time after `direct` that the planet passes the degree of the retrograde station |
| `cazimi` | Mercury and Venus: conjunction with the Sun inside the retrograde (inferior conjunction) |
| `cazimiWindow` | Start and end of the traditional 17′ cazimi window |
| `opposition` | Mars to Pluto: the minute the planet is 180° from the Sun, inside the retrograde |
| `*Degree` | Position at that moment, in degrees and arcminutes of a tropical sign |
| `sign` | Sign at the retrograde station |
| `sidereal` | The same moments in the sidereal (Vedic, Jyotish) zodiac, Lahiri ayanamsa: `sign`, `*Degree`, `*Lon` (decimal degrees) and `*Nakshatra` (`name`, `number` 1–27, `pada` 1–4) |

Times are ISO 8601 UTC rounded to the nearest minute, for example `2027-02-09T17:36Z`.

Example, the Mercury retrograde of February 2027:

```json
{
  "sign": "Pisces",
  "pre": "2027-01-25T18:58Z",
  "retro": "2027-02-09T17:36Z", "retroDegree": "5°59′ Pisces",
  "cazimi": "2027-02-18T16:39Z", "cazimiDegree": "29°48′ Aquarius",
  "cazimiWindow": ["2027-02-18T13:28Z", "2027-02-18T19:50Z"],
  "direct": "2027-03-03T12:32Z", "directDegree": "20°55′ Aquarius",
  "post": "2027-03-23T14:58Z"
}
```

## Sidereal (Vedic) zodiac

Retrograde timing is the same in both zodiacs: a station is the minute the planet's apparent motion reverses, whatever the frame. Only the sign and degree differ. Every cycle carries a `sidereal` block, and each file has an `ayanamsa` table (1 January of each year). The ayanamsa is Lahiri (Chitrapaksha), as Swiss Ephemeris defines `SE_SIDM_LAHIRI`: 23°15′00.658″ at 1956-03-21 0h TT, carried by IAU 2006 general precession, plus nutation in longitude so it matches the apparent longitude of date. Sidereal = tropical − ayanamsa (about 24°14′ in 2027). Code: [`tools/sidereal.py`](tools/sidereal.py).

```json
"sidereal": {
  "sign": "Aquarius",
  "retroDegree": "11°45′ Aquarius", "retroNakshatra": {"name": "Shatabhisha", "number": 24, "pada": 2},
  "cazimiDegree": "5°33′ Aquarius",
  "directDegree": "26°41′ Capricorn", "directNakshatra": {"name": "Dhanishta", "number": 23, "pada": 2}
}
```

## Live API, calendar and MCP server

The same numbers are served by [cazimi.live](https://cazimi.live) without a key, CORS open, rebuilt daily at 00:05 UTC ([API docs](https://cazimi.live/methodology#api)):

```sh
curl https://cazimi.live/v1/planets/today.json      # which planets are retrograde today
curl https://cazimi.live/v1/mercury/next.json       # next Mercury retrograde
curl https://cazimi.live/v1/mars/cycles.json        # every Mars cycle
```

Calendar feed for Google, Apple or Outlook: `https://cazimi.live/v1/calendar/retrogrades.ics`, or one planet at a time ([how to subscribe](https://cazimi.live/retrograde-calendar)).

AI assistants can use the read-only MCP server at `https://cazimi.live/api/mcp` (Streamable HTTP, no auth). It is published in the official MCP Registry as `live.cazimi/retrogrades` ([`server.json`](server.json)). In Claude, add it from the connector directory: [Cazimi Mercury Retrograde](https://claude.ai/directory/cazimi-mercury-retrograde). Listed on Glama: [live.cazimi/retrogrades](https://glama.ai/mcp/connectors/live.cazimi/retrogrades). On iPhone: [Mercury Retrograde: Cazimi](https://apps.apple.com/us/app/cazimi-mercury-retrograde/id6760207689).

## Accuracy

Every station is the minute the planet's apparent longitude rate changes sign in JPL DE421, found by root-finding, not read off a daily table. The published times are checked against JPL Horizons: [cazimi.live/accuracy](https://cazimi.live/accuracy). Spotted a time that disagrees with your own software? [Open an issue](https://github.com/cazimi-live/retrograde-ephemeris/issues/new/choose) with the planet, the moment and your source.

## Regenerate

```sh
pip install -r requirements.txt
# years from, years to, planets, output file; downloads de421.bsp (17 MB) on first run
python tools/retrogrades.py 2025 2030 mercury,venus,mars,jupiter,saturn,uranus,neptune,pluto out.json
```

DE421 covers 1900–2050, which bounds the Mercury table. A full eight-planet run takes a few minutes. To add or refresh only the sidereal blocks in existing files: `python tools/sidereal.py data/retrogrades.json data/mercury-1900-2050.json`.

## Licence

Data (`data/`): [CC BY 4.0](LICENSE-DATA). Code (`tools/`, `examples/`): [MIT](LICENSE). If you publish these times, credit **Cazimi** with a link to https://cazimi.live, or cite the DOI above.
