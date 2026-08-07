#!/usr/bin/env python3
"""
North Africa organic-export map for the LinkedIn visual.

Geometry : Natural Earth 1:50m admin-0 countries (public domain).
           Morocco is rendered as a single continuous territory: the MAR and
           ESH features are dissolved with a geometric union so no internal
           boundary is drawn and the southern coastline runs unbroken to
           Lagouira.
Projection: Albers equal-area conic, standard parallels 21°N / 37°N,
           central meridian 10°E — a standard choice for a band this wide.
"""

import json
import math
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

# ------------------------------------------------------------------ config --
W, H = 1200, 1200                      # LinkedIn square
MAP_BOX = (58, 196, 1084, 600)         # x, y, w, h of the map panel

LON0, LAT1, LAT2, LAT0 = 10.0, 21.0, 37.0, 28.0
VIEW = dict(lon_min=-19.0, lon_max=38.0, lat_min=18.5, lat_max=44.5)

MAGHREB = {                            # the four TRACES rows in the post
    "Morocco":  dict(producers=215, exporters=218),
    "Algeria":  dict(producers=31,  exporters=26),
    "Tunisia":  dict(producers=535, exporters=254),
    "Egypt":    dict(producers=279, exporters=244),
}
CONTEXT = ["Libya", "Mauritania", "Mali", "Niger", "Chad", "Sudan"]
EU27 = ["Spain", "Portugal", "France", "Italy", "Greece", "Malta", "Cyprus",
        "Slovenia", "Croatia", "Austria", "Germany", "Belgium", "Netherlands",
        "Luxembourg", "Czechia", "Slovakia", "Poland", "Hungary", "Romania",
        "Bulgaria", "Ireland", "Denmark", "Sweden", "Finland", "Estonia",
        "Latvia", "Lithuania"]
NON_EU = ["United Kingdom", "Switzerland", "Turkey", "Albania", "Serbia",
          "Montenegro", "Bosnia and Herz.", "Kosovo", "North Macedonia",
          "Ukraine", "Moldova", "Belarus", "N. Cyprus", "Syria", "Lebanon",
          "Israel", "Palestine", "Jordan", "Saudi Arabia", "Iraq", "Norway",
          "Andorra", "Monaco", "San Marino", "Gibraltar", "Kuwait"]

# palette — matches the report's chrome and the validated categorical set
INK, MUTED, RULE = "#0b0b0b", "#8b8a84", "#dedcd4"
BRAND, BRAND_D = "#1f7a5e", "#0f3d31"
SEA, LAND, LAND_E = "#eef2f2", "#e4e2da", "#dfe4ea"
STROKE = "#ffffff"

# ------------------------------------------------------------- projection --
r1, r2, r0, l0 = map(math.radians, (LAT1, LAT2, LAT0, LON0))
_n = 0.5 * (math.sin(r1) + math.sin(r2))
_C = math.cos(r1) ** 2 + 2 * _n * math.sin(r1)
_rho0 = math.sqrt(_C - 2 * _n * math.sin(r0)) / _n


def albers(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    q = _C - 2 * _n * math.sin(phi)
    rho = math.sqrt(max(q, 1e-9)) / _n
    th = _n * (lam - l0)
    return rho * math.sin(th), _rho0 - rho * math.cos(th)


_c = [albers(lo, la) for lo in (VIEW["lon_min"], VIEW["lon_max"])
      for la in (VIEW["lat_min"], VIEW["lat_max"])]
_c += [albers(lo, VIEW["lat_min"]) for lo in range(-19, 39, 3)]
_c += [albers(lo, VIEW["lat_max"]) for lo in range(-19, 39, 3)]
X0, X1 = min(p[0] for p in _c), max(p[0] for p in _c)
Y0, Y1 = min(p[1] for p in _c), max(p[1] for p in _c)
MX, MY, MW, MH = MAP_BOX
_s = min(MW / (X1 - X0), MH / (Y1 - Y0))
_ox = MX + (MW - (X1 - X0) * _s) / 2
_oy = MY + (MH - (Y1 - Y0) * _s) / 2


def pt(lon, lat):
    x, y = albers(lon, lat)
    return (_ox + (x - X0) * _s, _oy + (Y1 - y) * _s)


def path_of(geom, prec=1):
    """Shapely geometry -> SVG path data, dropping negligible islands."""
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for poly in polys:
        if poly.area < 0.05:
            continue
        for ring in [poly.exterior] + list(poly.interiors):
            cs = list(ring.coords)
            if len(cs) < 4:
                continue
            d = []
            last = None
            for lon, lat in cs:
                x, y = pt(lon, lat)
                x, y = round(x, prec), round(y, prec)
                if last and abs(x - last[0]) < 0.35 and abs(y - last[1]) < 0.35:
                    continue
                d.append(f"{'M' if not d else 'L'}{x} {y}")
                last = (x, y)
            if len(d) > 3:
                out.append(" ".join(d) + "Z")
    return " ".join(out)


# ------------------------------------------------------------------- data --
feats = json.load(open("ne50.geojson"))["features"]


def by_name(*names):
    got = []
    for f in feats:
        p = f["properties"]
        nm = p.get("NAME") or p.get("name")
        if nm in names:
            got.append(shape(f["geometry"]))
    return got


# Morocco as one territory — dissolve the MAR/ESH boundary.
morocco = unary_union(by_name("Morocco", "W. Sahara")).buffer(0.02).buffer(-0.02)

shapes = {"Morocco": morocco}
for n in ("Algeria", "Tunisia", "Egypt"):
    shapes[n] = unary_union(by_name(n))
context = unary_union(by_name(*CONTEXT))
eu27 = unary_union(by_name(*EU27))
noneu = unary_union(by_name(*NON_EU))

if __name__ == "__main__":
    parts = {
        "eu27": path_of(eu27),
        "noneu": path_of(noneu),
        "context": path_of(context),
        **{k.lower(): path_of(v) for k, v in shapes.items()},
    }
    json.dump({"paths": parts,
               "anchors": {n: pt(*c) for n, c in {
                   "Morocco": (-7.6, 31.4), "Algeria": (2.8, 28.2),
                   "Tunisia": (9.6, 34.4), "Egypt": (29.5, 26.6),
                   "Libya": (17.5, 27.0), "Mauritania": (-10.5, 20.5),
                   "EU": (-2.0, 41.6), "Agadir": (-9.6, 30.42),
                   "MoroccoDot": (-8.2, 31.7), "EgyptIn": (29.8, 26.4),
                   "AlgeriaIn": (2.5, 27.6),
                   "TangerMed": (-5.5, 35.9), "Casablanca": (-7.6, 33.57),
               }.items()},
               "box": MAP_BOX, "size": [W, H], "maghreb": MAGHREB},
              open("map.json", "w"))
    tot = sum(len(v) for v in parts.values())
    print(f"paths built, {tot/1024:.0f} KB of path data")
    print("morocco bounds (lon/lat):",
          [round(v, 2) for v in morocco.bounds])
