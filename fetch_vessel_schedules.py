import json, time, urllib.request, urllib.error, csv, sys

B = "https://api-shipper.vessel-schedule-service.com/api/v1"
HDRS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))

# 1) carrier list
companies = fetch(f"{B}/shipping-companies")["data"]
companies = [c for c in companies if c.get("slug") != "demo"]
print(f"{len(companies)} carriers (excluding demo)", file=sys.stderr)

COLS = ["carrier","carrier_slug","port","port_code","locode","vessel",
        "call_sign","service","direction","import_voyage","export_voyage",
        "proforma_ETA","proforma_ETD","arrival_date","arrival_time",
        "berthing_date","berthing_time","sailing_date","sailing_time"]

IE = {"1":"Import","2":"Export","3":"Import/Export"}

rows = []
for c in companies:
    slug = c["slug"]; name = c["name"]
    page = 1
    got = 0
    while True:
        url = f"{B}/{slug}/voyages/tracking?per_page=200&page={page}"
        try:
            d = fetch(url)
        except Exception as e:
            print(f"  ! {slug} page {page} failed: {e}", file=sys.stderr)
            break
        data = d.get("data", [])
        for it in data:
            lp = it.get("locate_port") or {}
            rows.append({
                "carrier": name,
                "carrier_slug": slug,
                "port": lp.get("name_en") or it.get("from_port_name_E"),
                "port_code": it.get("port_code") or lp.get("port_code"),
                "locode": lp.get("locode"),
                "vessel": it.get("vessel_name"),
                "call_sign": it.get("call_sign"),
                "service": it.get("service"),
                "direction": IE.get(str(it.get("IE_flag")), it.get("IE_flag")),
                "import_voyage": it.get("import_voyage"),
                "export_voyage": it.get("export_voyage"),
                "proforma_ETA": it.get("proforma_ETA"),
                "proforma_ETD": it.get("proforma_ETD"),
                "arrival_date": it.get("arrival_date"),
                "arrival_time": it.get("arrival_time"),
                "berthing_date": it.get("berthing_date"),
                "berthing_time": it.get("berthing_time"),
                "sailing_date": it.get("sailing_date"),
                "sailing_time": it.get("sailing_time"),
            })
        got += len(data)
        last = (d.get("meta") or {}).get("last_page", page)
        if page >= last or not data:
            break
        page += 1
        time.sleep(0.3)
    print(f"  {name} ({slug}): {got} voyages", file=sys.stderr)
    time.sleep(0.3)

out = "/home/user/mizutokei/vessel_schedules.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print(f"\nTOTAL ROWS: {len(rows)} -> {out}", file=sys.stderr)
