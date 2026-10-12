# -*- coding: utf-8 -*-
"""Save a snapshot of the Israel Airports Authority flight board (data.gov.il).

The public dataset only holds a rolling window of a few days, so history has
to be collected. Each run writes one gzipped JSON file to data/raw, named by
the UTC time of the run so local and cloud runs never collide.

Run:  python collect.py
"""
import gzip
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RESOURCE_ID = "e83f763b-b7d7-479e-b172-ae981ddc6de5"
API = "https://data.gov.il/api/3/action/datastore_search"
PAGE = 5000
OUT_DIR = Path(__file__).parent / "data" / "raw"


def fetch_all():
    records, offset = [], 0
    while True:
        url = f"{API}?resource_id={RESOURCE_ID}&limit={PAGE}&offset={offset}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.load(resp)["result"]
        records.extend(result["records"])
        offset += PAGE
        if offset >= result["total"]:
            return records


def main():
    records = fetch_all()
    if not records:
        raise SystemExit("no records returned")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"flights_{datetime.now(timezone.utc):%Y-%m-%dT%H%M}Z.json.gz"
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)
    times = sorted(r["CHSTOL"] for r in records)
    line = f"{len(records)} flights, {times[0]} to {times[-1]} -> {out.name}"
    with open(OUT_DIR.parent / "collect.log", "a", encoding="utf-8") as log:
        log.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
