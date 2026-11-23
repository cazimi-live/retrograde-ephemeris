"""Print the next (or current) Mercury retrograde from the dataset.

Standard library only. Run from anywhere:

    python examples/python/next_mercury_retrograde.py
    python examples/python/next_mercury_retrograde.py 2031-06-01   # as of another date

Data: Cazimi retrograde ephemeris (JPL DE421), CC BY 4.0,
https://doi.org/10.5281/zenodo.24011806 and https://cazimi.live
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "mercury-1900-2050.json"


def parse(t):
    # Times look like "2027-02-09T17:36Z": UTC, to the minute.
    return datetime.strptime(t, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)


def main():
    now = datetime.now(timezone.utc)
    if len(sys.argv) > 1:
        now = datetime.fromisoformat(sys.argv[1]).replace(tzinfo=timezone.utc)

    with open(DATA, encoding="utf-8") as f:
        cycles = json.load(f)["mercury"]

    # The first cycle whose station direct is still ahead: current or next.
    cycle = next((c for c in cycles if parse(c["direct"]) > now), None)
    if cycle is None:
        print("No Mercury retrograde after that date in this file (it ends in 2050).")
        return

    state = "now retrograde" if parse(cycle["retro"]) <= now else "next retrograde"
    print(f"Mercury {state}, in {cycle['sign']}")
    print(f"  pre-shadow begins   {cycle['pre']}")
    print(f"  station retrograde  {cycle['retro']}  {cycle['retroDegree']}")
    print(f"  cazimi (Sun)        {cycle['cazimi']}  {cycle['cazimiDegree']}")
    print(f"  station direct      {cycle['direct']}  {cycle['directDegree']}")
    print(f"  post-shadow ends    {cycle['post']}")
    print("Source: Cazimi retrograde ephemeris, https://cazimi.live")


if __name__ == "__main__":
    main()
