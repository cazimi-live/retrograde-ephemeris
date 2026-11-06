import json, sys, datetime as dt
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

ts = load.timescale()
eph = load('de421.bsp')
earth, sun = eph['earth'], eph['sun']
PLANETS = {'mercury': 'mercury', 'venus': 'venus', 'mars': 'mars', 'jupiter': 'jupiter barycenter', 'saturn': 'saturn barycenter', 'uranus': 'uranus barycenter', 'neptune': 'neptune barycenter', 'pluto': 'pluto barycenter'}
SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

def lon(body, t):
    lat, lo, _ = earth.at(t).observe(body).apparent().frame_latlon(ecliptic_frame)
    return lo.degrees % 360

def speed(body, t):  # deg/day via central difference of 1 minute
    h = 1/1440/2
    a = lon(body, ts.tt_jd(t.tt - h)); b = lon(body, ts.tt_jd(t.tt + h))
    d = (b - a + 540) % 360 - 180
    return d / (2*h)

def bisect(f, t0, t1, iters=40):  # f changes sign between t0,t1
    f0 = f(t0)
    for _ in range(iters):
        tm = ts.tt_jd((t0.tt + t1.tt)/2)
        fm = f(tm)
        if (fm < 0) == (f0 < 0): t0, f0 = tm, fm
        else: t1 = tm
    return ts.tt_jd((t0.tt + t1.tt)/2)

def iso(t):
    d = t.utc_datetime().replace(second=0, microsecond=0, tzinfo=None)
    # round to nearest minute
    d2 = t.utc_datetime()
    if d2.second >= 30: d = d + dt.timedelta(minutes=1)
    return d.strftime('%Y-%m-%dT%H:%MZ')

def fmt_deg(l):
    s = int(l // 30); d = l - s*30; m = int(round((d - int(d))*60)); dd = int(d)
    if m == 60: dd += 1; m = 0
    return f"{dd}°{m:02d}′ {SIGNS[s]}"

def crossing(body, target, t_from, t_to, step=0.25):
    """first time in [t_from,t_to] when lon(body) crosses target going forward"""
    f = lambda t: ((lon(body, t) - target + 180) % 360) - 180
    if t_from.tt < EPH_MIN.tt: t_from = EPH_MIN
    t = t_from; prev = f(t)
    while t.tt < t_to.tt:
        tn = ts.tt_jd(t.tt + step); cur = f(tn)
        if prev < 0 <= cur or (prev <= 0 < cur): return bisect(f, t, tn)
        t, prev = tn, cur
    return None

out = {}
Y0, Y1 = int(sys.argv[1]), int(sys.argv[2]); EPH_MIN = ts.utc(1899, 8, 1)
start, end = ts.tt_jd(max(ts.utc(Y0 - 1, 8, 1).tt, ts.utc(1899, 12, 1).tt)), ts.utc(Y1 + 1, 6, 1)
for name, key in [(n, PLANETS[n]) for n in sys.argv[3].split(',')]:
    body = eph[key]
    # find station times: speed sign changes, sample every 0.5 day
    t = start; sp = speed(body, t); stations = []
    while t.tt < end.tt:
        tn = ts.tt_jd(t.tt + 0.5); spn = speed(body, tn)
        if (sp < 0) != (spn < 0):
            tt = bisect(lambda x: speed(body, x), t, tn)
            stations.append((tt, 'retro' if spn < 0 else 'direct'))
        t, sp = tn, spn
    cycles = []
    for i, (tt, kind) in enumerate(stations):
        if kind != 'retro' or i + 1 >= len(stations): continue
        td, _ = stations[i+1]
        lr, ld = lon(body, tt), lon(body, td)
        # pre-shadow: last crossing of ld before tt; post-shadow: first crossing of lr after td
        pre = crossing(body, ld, ts.tt_jd(tt.tt - 120), tt)
        post = crossing(body, lr, td, ts.tt_jd(td.tt + 120))
        c = {"sign": SIGNS[int(lr // 30)], "retro": iso(tt), "retroDegree": fmt_deg(lr), "direct": iso(td), "directDegree": fmt_deg(ld),
             "pre": iso(pre) if pre is not None else None, "post": iso(post) if post is not None else None}
        # conjunction/opposition with the Sun inside the retrograde
        f = lambda x: ((lon(body, x) - lon(sun, x) + 180) % 360) - 180
        g = lambda x: ((lon(body, x) - lon(sun, x)) % 360) - 180
        for fn, label in ((f, 'cazimi'), (g, 'opposition')):
            a = tt; fa = fn(a); found = None
            while a.tt < td.tt:
                b = ts.tt_jd(min(a.tt + 0.5, td.tt)); fb = fn(b)
                if (fa < 0) != (fb < 0) and abs(fa) < 90: found = bisect(fn, a, b); break
                a, fa = b, fb
            if found is not None:
                c[label] = iso(found); c[label + "Degree"] = fmt_deg(lon(body, found))
                if label == 'cazimi':
                    # 17 arcmin window
                    w = lambda x: abs(((lon(body, x) - lon(sun, x) + 180) % 360) - 180) - 17/60
                    s0 = bisect(w, ts.tt_jd(found.tt - 2), found); s1 = bisect(w, found, ts.tt_jd(found.tt + 2))
                    c["cazimiWindow"] = [iso(s0), iso(s1)]
        if (c["post"] or c["direct"]) >= f"{Y0}-01-01" and c["retro"] < f"{Y1 + 1}-01-01": cycles.append(c)
    out[name] = cycles
    print(name, len(cycles), file=sys.stderr)
json.dump(out, open(sys.argv[4], 'w'), indent=1)
