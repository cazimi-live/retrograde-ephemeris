"""Sidereal (Vedic) zodiac for the retrograde data, Lahiri (Chitrapaksha) ayanamsa.

Ayanamsa definition (the one Swiss Ephemeris calls SE_SIDM_LAHIRI, from the Indian
Calendar Reform Committee): 23°15′00.658″ at 1956-03-21 0h TT, carried by IAU 2006
general precession in longitude, plus nutation in longitude so it matches the apparent
ecliptic longitude of date that tools/retrogrades.py writes. Sidereal = tropical − ayanamsa.

Event times never change between zodiacs; only the sign, degree and nakshatra do.

Usage: python tools/sidereal.py data/retrogrades.json [data/mercury-1900-2050.json ...]
adds a "sidereal" block to every cycle (recomputed at the stored minute) and a top-level
"ayanamsa" table, in place.
"""
import json, sys
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from skyfield.nutationlib import iau2000a_radians

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
NAKSHATRAS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
              "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
              "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
T0_JD, AYAN_T0 = 2435553.5, 23.250182778 - 0.004658035
DEFINITION = ("Lahiri (Chitrapaksha): 23°15′00.658″ at 1956-03-21 0h TT, IAU 2006 general precession in longitude, "
              "plus nutation in longitude (true ayanamsa, matches apparent longitude of date); sidereal = tropical − ayanamsa")

def _pA(jd_tt):  # IAU 2006 general precession in longitude, arcsec
    T = (jd_tt - 2451545.0) / 36525
    return 5028.796195*T + 1.1054348*T**2 + 0.00007964*T**3 - 0.000023857*T**4 - 0.0000000383*T**5

def ayanamsa(t, true=True):
    a = AYAN_T0 + (_pA(t.tt) - _pA(T0_JD)) / 3600
    if true:
        dpsi, _ = iau2000a_radians(t)
        a += dpsi * 57.29577951308232
    return a

def fmt_deg(l):
    s = int(l // 30); d = l - s*30; m = int(round((d - int(d))*60)); dd = int(d)
    if m == 60: dd += 1; m = 0
    if dd == 30: dd = 0; s = (s + 1) % 12
    return f"{dd}°{m:02d}′ {SIGNS[s]}"

def nakshatra(l):
    i = int(l // (360/27)); pada = int((l - i*360/27) // (360/108)) + 1
    return {"name": NAKSHATRAS[i], "number": i + 1, "pada": pada}

_ts = _eph = None
def _load():
    global _ts, _eph
    if _ts is None: _ts, _eph = load.timescale(), load('de421.bsp')
    return _ts, _eph

def lon_tropical(body, t):
    ts, eph = _load()
    _, lo, _ = eph['earth'].at(t).observe(body).apparent().frame_latlon(ecliptic_frame)
    return lo.degrees % 360

def sidereal_block(body, c, t_of):
    """t_of(iso) -> skyfield Time. Returns the sidereal block for one cycle dict."""
    out = {}
    for key in ("retro", "direct", "cazimi", "opposition"):
        if not c.get(key): continue
        t = t_of(c[key]); l = (lon_tropical(body, t) - ayanamsa(t)) % 360
        if key == "retro": out["sign"] = SIGNS[int(l // 30)]
        out[key + "Degree"] = fmt_deg(l)
        out[key + "Lon"] = round(l, 4)
        out[key + "Nakshatra"] = nakshatra(l)
    return out

def ayanamsa_table(y0, y1):
    ts, _ = _load()
    return {f"{y}-01-01": round(ayanamsa(ts.utc(y, 1, 1)), 6) for y in range(y0, y1 + 1)}

PLANETS = {'mercury': 'mercury', 'venus': 'venus', 'mars': 'mars', 'jupiter': 'jupiter barycenter', 'saturn': 'saturn barycenter',
           'uranus': 'uranus barycenter', 'neptune': 'neptune barycenter', 'pluto': 'pluto barycenter'}

def enrich(path):
    ts, eph = _load()
    d = json.load(open(path))
    planets = d["planets"] if "planets" in d else d
    t_of = lambda s: ts.utc(int(s[0:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))
    for name, cycles in planets.items():
        body = eph[PLANETS[name]]
        for c in cycles: c["sidereal"] = sidereal_block(body, c, t_of)
        print(path, name, len(cycles), file=sys.stderr)
    years = [int(c["retro"][:4]) for cs in planets.values() for c in cs]
    table = {"system": "Lahiri", "definition": DEFINITION, "yearly": ayanamsa_table(min(years), max(years) + 1)}
    if "planets" in d:
        d["ayanamsa"] = table
        d["source"] = d["source"].split(" | sidereal:")[0] + " | sidereal: " + DEFINITION
    else:
        d = {"ayanamsa": table, **d}
    json.dump(d, open(path, "w"), indent=1)

if __name__ == "__main__":
    for p in sys.argv[1:]: enrich(p)
