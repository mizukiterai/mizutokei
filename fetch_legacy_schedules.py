#!/usr/bin/env python3
"""
Fetch vessel schedules for the 15 "legacy" carriers from the server-rendered
HTML schedule site at https://www.toyoshingo.com/{slug}/index.php and normalize
them into the same schema as vessel_schedules.csv.

Produces:
  - vessel_schedules_legacy.csv  (15 legacy carriers)
  - vessel_schedules_all.csv     (union of vessel_schedules.csv + legacy)

No third-party deps: uses urllib + html.parser + regex (Shift_JIS pages).
"""

import csv
import html as htmllib
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://www.toyoshingo.com"
HERE = os.path.dirname(os.path.abspath(__file__))

# slug -> full display carrier name (matches vessel_schedules.csv where applicable)
CARRIER_NAMES = {
    "ckline": "CK LINE CO., LTD.",
    "cmacgm": "CMA CGM S.A.",
    "cosco": "COSCO SHIPPING LINES CO., LTD.",
    "hapag": "HAPAG-LLOYD AG",
    "heunga": "HEUNG A LINE CO., LTD.",
    "hmm": "HMM CO., LTD.",
    "namsung": "NAMSUNG SHIPPING CO., LTD.",
    "pancon": "PAN CONTINENTAL SHIPPING CO., LTD.",
    "smc": "SHANDONG MARINE CORPORATION",
    "hasco": "SHANGHAI HAI HUA SHIPPING CO., LTD.",
    "sinokor": "SINOKOR MERCHANT MARINE CO., LTD.",
    "starocean": "STAROCEAN MARINE CO., LTD.",
    "tslines": "T.S.LINES LTD.",
    "tclc": "TAICANG CONTAINER LINES CO., LTD.",
    "yangming": "YANG MING MARINE TRANSPORT CORPORATION",
}

SLUGS = list(CARRIER_NAMES.keys())

COLUMNS = [
    "carrier", "carrier_slug", "port", "port_code", "locode", "vessel",
    "call_sign", "service", "direction", "import_voyage", "export_voyage",
    "proforma_ETA", "proforma_ETD", "arrival_date", "arrival_time",
    "berthing_date", "berthing_time", "sailing_date", "sailing_time",
]


def fetch(url, retries=4):
    """Fetch a URL, return decoded (shift_jis) text. Exponential backoff."""
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (schedule-aggregator)"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
            return raw.decode("shift_jis", "replace")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            last = e
            wait = 0.5 * (2 ** attempt)
            sys.stderr.write(f"  retry {attempt+1} for {url}: {e} (wait {wait}s)\n")
            time.sleep(wait)
    raise RuntimeError(f"failed to fetch {url}: {last}")


def harvest_ports_weeks(html):
    """From a carrier index page, return (port_area_pairs, weeks).

    port_area_pairs: list of (port_code, area_or_None) for every navigable port.
    weeks: sorted list of week numbers from the week selector.
    """
    pairs = {}  # port_code -> area (area may be None)
    # handles both '&amp;' (most carriers) and bare '&' (tslines), and an empty
    # week value (tslines nav links use 'week=' with no number).
    for m in re.finditer(
        r"index\.php\?port=(\d+)&(?:amp;)?week=\d*(?:&(?:amp;)?area=(\w+))?", html
    ):
        port = m.group(1)
        area = m.group(2)
        # keep first/any area seen for this port
        if port not in pairs or (area and not pairs[port]):
            pairs[port] = area

    weeks = set()
    wm = re.search(r'id="weekmovediv">(.*?)</div>', html, re.S)
    if wm:
        for x in re.finditer(r"week=(\d+)", wm.group(1)):
            weeks.add(int(x.group(1)))
    if not weeks:
        # No week selector on the page (e.g. tslines): the site still serves
        # WEEK -2..+2 as week=1..5, so enumerate those.
        weeks = {1, 2, 3, 4, 5}
    return pairs, sorted(weeks)


def page_port_name(html):
    """Extract English port name for the current page.

    Most carriers expose it in '<p id="pagetitle"> ... By Port : Yokohama'.
    The tslines layout instead marks the current port with
    '<div id="current">横浜<br />YOKOHAMA</div>'.
    """
    m = re.search(r'<p id="pagetitle">(.*?)</p>', html, re.S)
    if m:
        txt = htmllib.unescape(m.group(1))
        pm = re.search(r"[Bb]y\s+[Pp]ort\s*:\s*([^<\n]+)", txt)
        if pm:
            return pm.group(1).strip()
    cur = re.search(r'<div id="current">(.*?)</div>', html, re.S)
    if cur:
        # take the last (English) line of "JP<br />EN"
        parts = [clean(p) for p in re.split(r"<br\s*/?>", cur.group(1))]
        parts = [p for p in parts if p]
        if parts:
            return parts[-1]
    return ""


# field labels found inside the <dl> title attribute (label -> normalized key).
# Labels are matched case-insensitively with internal spaces removed, so e.g.
# both "Vessel Name" and "VesselName" map to the same key.
FIELD_KEYS = {
    "vesselname": "vessel",
    "voyage": "voyage",
    "service": "service",
    "arrival": "arrival",
    "berthing": "berthing",
    "sailing": "sailing",
}

TAG_RE = re.compile(r"<[^>]+>")


def clean(text):
    text = TAG_RE.sub(" ", text)
    text = htmllib.unescape(text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_dl(title_html):
    """Parse the <dl><dt>label</dt><dd>value</dd>...</dl> in a title attribute.

    Returns dict of normalized field -> raw value text (tags stripped, except we
    preserve the inner text). Handles both 'Label : value' and
    'Label</dt><dd>: value' styles.
    """
    out = {}
    for m in re.finditer(r"<dt>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", title_html, re.S):
        label = clean(m.group(1)).rstrip(":").strip().lower()
        label = label.replace(" ", "")  # "vessel name" / "vesselname" -> "vesselname"
        value = clean(m.group(2))
        # value sometimes begins with ": "
        value = re.sub(r"^:\s*", "", value)
        if label in FIELD_KEYS:
            out[FIELD_KEYS[label]] = value
    return out


def split_voyage(voy):
    """Split 'A/B' into (import, export); single -> (single, '')."""
    if not voy:
        return "", ""
    voy = voy.strip()
    if "/" in voy:
        a, b = voy.split("/", 1)
        return a.strip(), b.strip()
    return voy, ""


DATE_RE = re.compile(r"(\d{4})/(\d{2})/(\d{2})")
DT_RE = re.compile(r"(\d{4})/(\d{2})/(\d{2})(?:\s+(\d{1,2}:\d{2}))?")
MMDD_DT_RE = re.compile(r"(\d{1,2})/(\d{1,2})(?:\s+(\d{1,2}:\d{2}))?")


def split_datetime(val, default_year=2026):
    """Return (date YYYY/MM/DD, time HH:MM or '') from a value cell.

    Handles 'YYYY/MM/DD HH:MM', 'YYYY/MM/DD', 'MM/DD HH:MM', 'MM/DD'.
    Returns ('','') if no date present (e.g. --OMIT--).
    """
    if not val:
        return "", ""
    val = val.strip()
    m = DT_RE.search(val)
    if m:
        date = f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
        tm = m.group(4) or ""
        if tm and len(tm.split(":")[0]) == 1:
            tm = "0" + tm
        return date, tm
    m = MMDD_DT_RE.search(val)
    if m:
        mm = int(m.group(1)); dd = int(m.group(2))
        date = f"{default_year}/{mm:02d}/{dd:02d}"
        tm = m.group(3) or ""
        if tm and len(tm.split(":")[0]) == 1:
            tm = "0" + tm
        return date, tm
    return "", ""


# matches each schedule entry anchor and its title attribute + visible call sign
ENTRY_RE = re.compile(
    r'<a\s+href="certificate\.php\?[^"]*"\s+title="(?P<title>.*?)"\s*>(?P<body>.*?)</a>',
    re.S,
)
CALLSIGN_RE = re.compile(r"\(([^()]+)\)\s*$")


def make_row(slug, carrier, port_name, port_code, vessel, call_sign, service,
             imp, exp, a, b, s):
    """a/b/s are (date, time) tuples for arrival/berthing/sailing."""
    return {
        "carrier": carrier,
        "carrier_slug": slug,
        "port": port_name,
        "port_code": port_code,
        "locode": "",
        "vessel": vessel,
        "call_sign": call_sign,
        "service": service,
        "direction": "",
        "import_voyage": imp,
        "export_voyage": exp,
        "proforma_ETA": "",
        "proforma_ETD": "",
        "arrival_date": a[0],
        "arrival_time": a[1],
        "berthing_date": b[0],
        "berthing_time": b[1],
        "sailing_date": s[0],
        "sailing_time": s[1],
    }


def parse_entries_dl(html, slug, carrier, port_name, port_code):
    """Parse carriers whose anchors carry a title="<dl>...</dl>" attribute."""
    rows = []
    for em in ENTRY_RE.finditer(html):
        fields = parse_dl(em.group("title"))
        if not fields.get("vessel"):
            continue

        vessel_raw = fields.get("vessel", "")
        # call sign is in parentheses at end of vessel name: "NAME (CALLSIGN)"
        call_sign = ""
        cm = CALLSIGN_RE.search(vessel_raw)
        if cm:
            call_sign = cm.group(1).strip()
            vessel = vessel_raw[: cm.start()].strip()
        else:
            vessel = vessel_raw.strip()

        imp, exp = split_voyage(fields.get("voyage", ""))
        rows.append(make_row(
            slug, carrier, port_name, port_code, vessel, call_sign,
            fields.get("service", ""), imp, exp,
            split_datetime(fields.get("arrival", "")),
            split_datetime(fields.get("berthing", "")),
            split_datetime(fields.get("sailing", "")),
        ))
    return rows


# --- positional layout (e.g. tslines): anchors have no title attr; the date is
# implied by the column position within the 7-day grid, and the body holds the
# voyage(s), berthing/sailing time, abbreviation/call_sign and service code. ---
DATELINE_RE = re.compile(
    r'<div[^>]*>(\d{1,2})/(\d{1,2})\([A-Z]+\)</div>'
)
POS_CELL_RE = re.compile(
    r'<div class="nodata"></div>'
    r'|<div class="half"></div>'
    r'|<div class="omit">(?P<omit><a href="certificate\.php.*?</a>)</div>'
    r'|<div>(?P<cell><a href="certificate\.php.*?</a>)</div>',
    re.S,
)
POS_VESSEL_RE = re.compile(
    r'<span class="vesselname">(?P<vessel>.*?)</span>(?P<rest>.*?)</a>', re.S
)


def parse_entries_positional(html, slug, carrier, port_name, port_code,
                             default_year=2026):
    rows = []
    # dateline: ordered list of dates, one per grid column
    dl = re.search(r'id="dateline">(.*?)(?=<div class="oneline")', html, re.S)
    dates = []
    if dl:
        for m in DATELINE_RE.finditer(dl.group(1)):
            dates.append(
                f"{default_year}/{int(m.group(1)):02d}/{int(m.group(2)):02d}"
            )
    if not dates:
        return rows

    body = html[html.find('id="dateline"'):]
    for row in re.split(r'<div class="oneline">', body)[1:]:
        col = 0.0
        for m in POS_CELL_RE.finditer(row):
            token = m.group(0)
            anchor = m.group("cell") or m.group("omit")
            if "nodata" in token and anchor is None:
                col += 1
                continue
            if "half" in token and anchor is None:
                col += 0.5
                continue
            vm = POS_VESSEL_RE.search(anchor)
            if not vm:
                col += 1
                continue
            vessel = htmllib.unescape(clean(vm.group("vessel")))
            lines = [clean(x) for x in re.split(r"<br\s*/?>", vm.group("rest"))]
            voy = lines[0] if len(lines) > 0 else ""
            times = lines[1] if len(lines) > 1 else ""
            abbr_cs = lines[2] if len(lines) > 2 else ""
            service = lines[3] if len(lines) > 3 else ""

            imp, exp = "", ""
            if voy:
                # voyages are colon-separated here, e.g. "2624E:2624W"
                parts = re.split(r"[:/]", voy)
                imp = parts[0].strip()
                exp = parts[1].strip() if len(parts) > 1 else ""

            # call sign is after the slash in "ABBR/CALLSIGN"
            call_sign = ""
            if "/" in abbr_cs:
                call_sign = abbr_cs.split("/", 1)[1].strip()

            # times: "HH:MM:HH:MM" -> berthing time, sailing time (no dates)
            b_time = s_time = ""
            tm = re.findall(r"\d{1,2}:\d{2}", times)
            if len(tm) >= 1:
                b_time = tm[0]
            if len(tm) >= 2:
                s_time = tm[1]

            ci = int(round(col))
            ci = max(0, min(ci, len(dates) - 1))
            cell_date = dates[ci]
            # The grid column marks the berthing day; sailing may roll to next
            # day if its time is earlier than berthing time (best-effort).
            b_date = cell_date
            s_date = cell_date
            if b_time and s_time and s_time < b_time:
                d_ci = min(ci + 1, len(dates) - 1)
                s_date = dates[d_ci]

            rows.append(make_row(
                slug, carrier, port_name, port_code, vessel, call_sign,
                service, imp, exp,
                ("", ""),
                (b_date if b_time else cell_date, b_time),
                (s_date if s_time else "", s_time),
            ))
            col += 1
    return rows


# carriers that use the positional (no-title) layout
POSITIONAL_SLUGS = {"tslines"}


def parse_entries(html, slug, carrier, port_name, port_code):
    if slug in POSITIONAL_SLUGS:
        return parse_entries_positional(html, slug, carrier, port_name, port_code)
    return parse_entries_dl(html, slug, carrier, port_name, port_code)


def scrape_carrier(slug, delay=0.25):
    carrier = CARRIER_NAMES[slug]
    index_url = f"{BASE}/{slug}/index.php"
    sys.stderr.write(f"[{slug}] fetching index {index_url}\n")
    idx_html = fetch(index_url)
    pairs, weeks = harvest_ports_weeks(idx_html)
    sys.stderr.write(
        f"[{slug}] {len(pairs)} ports, weeks={weeks}\n"
    )

    all_rows = []
    ports_with_data = set()
    for port_code in sorted(pairs, key=lambda p: int(p)):
        area = pairs[port_code]
        for wk in weeks:
            url = f"{BASE}/{slug}/index.php?port={port_code}&week={wk}"
            if area:
                url += f"&area={area}"
            html = fetch(url)
            port_name = page_port_name(html) or port_code
            rows = parse_entries(html, slug, carrier, port_name, port_code)
            if rows:
                ports_with_data.add(port_code)
            all_rows.extend(rows)
            time.sleep(delay)
    return all_rows, len(pairs), ports_with_data


def write_csv(path, rows):
    # UTF-8 with BOM, quote fields containing commas (csv default QUOTE_MINIMAL)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_existing(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def dedup_exact(rows):
    """Drop exact-duplicate rows (full tuple across all columns)."""
    seen = set()
    out = []
    for r in rows:
        key = tuple(r.get(c, "") for c in COLUMNS)
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def main():
    legacy_rows = []
    summary = []
    for slug in SLUGS:
        try:
            rows, nports, ports_data = scrape_carrier(slug)
        except Exception as e:  # noqa
            sys.stderr.write(f"[{slug}] ERROR: {e}\n")
            rows, nports, ports_data = [], 0, set()
        rows = dedup_exact(rows)
        legacy_rows.extend(rows)
        summary.append((slug, len(rows), nports, len(ports_data)))
        sys.stderr.write(
            f"[{slug}] DONE rows={len(rows)} ports={nports} ports_with_data={len(ports_data)}\n"
        )

    legacy_rows = dedup_exact(legacy_rows)
    legacy_path = os.path.join(HERE, "vessel_schedules_legacy.csv")
    write_csv(legacy_path, legacy_rows)

    # Build union with existing API csv
    existing_path = os.path.join(HERE, "vessel_schedules.csv")
    existing = read_existing(existing_path)
    # normalize existing rows to dict with our columns
    existing_norm = [{c: r.get(c, "") for c in COLUMNS} for r in existing]
    all_rows = dedup_exact(existing_norm + legacy_rows)
    all_path = os.path.join(HERE, "vessel_schedules_all.csv")
    write_csv(all_path, all_rows)

    # report
    print("\n=== PER-CARRIER SUMMARY (legacy) ===")
    for slug, n, nports, pd in summary:
        print(f"{slug:12s} rows={n:5d} ports={nports:3d} ports_with_data={pd:3d}")
    print(f"\nlegacy total rows: {len(legacy_rows)}")
    print(f"existing API rows: {len(existing_norm)}")
    print(f"all total rows:    {len(all_rows)}")

    carriers_all = sorted(set(r["carrier"] for r in all_rows))
    print(f"\ndistinct carriers in all: {len(carriers_all)}")
    for c in carriers_all:
        print("  ", c)


if __name__ == "__main__":
    main()
