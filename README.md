# Retrograde ephemeris

Exact times of every planetary retrograde station, shadow boundary and Sun conjunction, to the minute in UTC, computed from NASA JPL's DE421 ephemeris.

- **Eight planets, 2024–2030:** Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto: [`data/retrogrades.json`](data/retrogrades.json)
- **Mercury, 1900–2050:** all 476 retrograde cycles: [`data/mercury-1900-2050.json`](data/mercury-1900-2050.json)
- **The script that generates them:** [`tools/retrogrades.py`](tools/retrogrades.py) (Python, [Skyfield](https://rhodesmill.org/skyfield/))

This is the dataset behind [cazimi.live](https://cazimi.live), its [JSON API](https://cazimi.live/methodology#api), its MCP server and the iPhone app [Mercury Retrograde: Cazimi](https://apps.apple.com/us/app/cazimi-mercury-retrograde/id6760207689). It is astronomy timing, not a horoscope.

## What each moment means

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

## Live API and MCP server

The same numbers are served without a key, CORS open, rebuilt daily at 00:05 UTC:

```sh
curl https://cazimi.live/v1/planets/today.json      # which planets are retrograde today
curl https://cazimi.live/v1/mercury/next.json       # next Mercury retrograde
curl https://cazimi.live/v1/mars/cycles.json        # every Mars cycle
```

AI assistants can use the read-only MCP server at `https://cazimi.live/api/mcp` (Streamable HTTP, no auth, eight tools). It is published in the official MCP Registry as `live.cazimi/retrogrades` ([`server.json`](server.json)). In Claude: Settings → Connectors → Add custom connector → paste the URL.

## Regenerate

```sh
pip install -r requirements.txt
# years from, years to, planets, output file; downloads de421.bsp (17 MB) on first run
python tools/retrogrades.py 2025 2030 mercury,venus,mars,jupiter,saturn,uranus,neptune,pluto out.json
```

DE421 covers 1900–2050, which bounds the Mercury table. A full eight-planet run takes a few minutes.

## Licence and citation

Data (`data/`): [CC BY 4.0](LICENSE-DATA). Code (`tools/`): [MIT](LICENSE). If you publish these times, credit **Cazimi** with a link to https://cazimi.live. Citation metadata: [`CITATION.cff`](CITATION.cff).

Spotted a time that disagrees with your own software? Open an issue with the planet, the moment and your source.
