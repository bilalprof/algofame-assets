#!/usr/bin/env python3
"""
Build the Morocco Organic Market Report PDF.

    python3 build.py            # -> ../Morocco-Organic-Market-Report-2026.pdf

Reads the open datasets in ../../data/, renders every figure and table from
them (so the PDF can never drift from the data), substitutes the fragments
into report.html and prints to PDF via WeasyPrint.

Dependencies: weasyprint, pyphen.
"""

import csv
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import charts as C  # noqa: E402

SRC = Path(__file__).parent
DATA = (SRC / ".." / "data").resolve()
OUT = (SRC / ".." / "Morocco-Organic-Market-Report-2026.pdf").resolve()


def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s):
    if s is None:
        return None
    s = str(s).strip().replace(" ", "")
    if s == "" or s.lower() in ("n.s.", "n/a", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def signed(v, dp=1, unit=" %"):
    """Signed number with a typographic minus (U+2212), not an ASCII hyphen."""
    if v is None:
        return "&ndash;"
    return f"{v:+.{dp}f}{unit}".replace("-", "\u2212")


def grade_badge(g):
    g = (g or "").strip()
    if g in ("A", "B", "C", "D"):
        return f'<span class="gr gr-{g}">{g}</span>'
    return '<span class="gr gr-none">&ndash;</span>'


# ===========================================================================
# fragments
# ===========================================================================

def fig_morocco_area(rows):
    """Certified organic cultivated land, Morocco. One series -> one colour."""
    pts = [(r["year"], num(r["cultivated_ha"])) for r in rows if num(r["cultivated_ha"])]
    labels = [p[0] for p in pts]
    vals = [p[1] for p in pts]
    svg = C.linechart(
        [{"name": "Cultivated organic land", "values": vals, "colour": C.BRAND}],
        labels, y_min=0, y_max=20000, height=48, y_ticks=4, unit=" ha",
        y_fmt=lambda v: f"{v/1000:.0f}k", area=True, pad_l=13,
    )
    return svg


def tbl_morocco_area(rows):
    out = ['<table class="compact"><thead><tr>'
           '<th>Reference year</th><th class="num">Cultivated (ha)</th>'
           '<th class="num">In conversion</th><th class="num">Wild collection</th>'
           '<th>Basis</th><th style="width:8mm">Ev.</th></tr></thead><tbody>']
    for r in rows:
        f = lambda k: (C.nb(num(r[k])) if num(r[k]) else "&ndash;")  # noqa: E731
        out.append(
            f'<tr><td class="num">{esc(r["year"])}</td><td class="num">{f("cultivated_ha")}</td>'
            f'<td class="num">{f("in_conversion_ha")}</td><td class="num">{f("wild_collection_ha")}</td>'
            f'<td>{esc(r["basis"])}</td><td>{grade_badge(r["grade"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def fig_africa_top(rows):
    """Top African countries by certified organic agricultural land."""
    have = [(r["country"], num(r["organic_ag_land_ha"]), r["land_data_year"])
            for r in rows if num(r["organic_ag_land_ha"])]
    have.sort(key=lambda t: -t[1])
    bars = [(f'{c} <span style="color:#898781">({y})</span>', v) for c, v, y in have]
    return C.hbar(bars, highlight=[b[0] for b in bars if b[0].startswith("Morocco")][0],
                  label_w="44mm", val_w="22mm")


def tbl_africa(rows):
    out = ['<table class="compact"><thead><tr>'
           '<th style="width:7mm" class="num">#</th><th>Country</th>'
           '<th class="num">Organic land (ha)</th><th class="num">Yr</th>'
           '<th class="num">Producers</th><th class="num">Yr</th>'
           '<th class="num">Wild coll. (ha)</th>'
           '<th>Flagship organic products</th><th style="width:8mm">Ev.</th>'
           "</tr></thead><tbody>"]
    withdata = [r for r in rows if num(r["organic_ag_land_ha"])]
    withdata.sort(key=lambda r: -num(r["organic_ag_land_ha"]))
    others = [r for r in rows if not num(r["organic_ag_land_ha"])]
    others.sort(key=lambda r: (r["flagship_organic_products"] == "no data reported",
                               r["country"]))
    i = 0
    for r in withdata + others:
        ranked = num(r["organic_ag_land_ha"]) is not None
        if ranked:
            i += 1
        hi = ' class="hi"' if r["country"] == "Morocco" else ""
        g = lambda k: (C.nb(num(r[k])) if num(r[k]) else '<span class="nil">&ndash;</span>')  # noqa
        yr = lambda k: (esc(r[k]) if r[k] and r[k] != "n.s." else '<span class="nil">&ndash;</span>')  # noqa
        out.append(
            f'<tr{hi}><td class="num rank">{i if ranked else ""}</td>'
            f'<td>{esc(r["country"])}</td>'
            f'<td class="num">{g("organic_ag_land_ha")}</td><td class="num">{yr("land_data_year")}</td>'
            f'<td class="num">{g("producers")}</td><td class="num">{yr("producers_year")}</td>'
            f'<td class="num">{g("wild_collection_ha")}</td>'
            f'<td>{esc(r["flagship_organic_products"])}</td>'
            f'<td>{grade_badge(r["grade"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def fig_eu_imports(rows):
    labels = [r["year"] for r in rows]
    vals = [num(r["total_tonnes"]) / 1e6 for r in rows]
    return C.linechart(
        [{"name": "EU organic agri-food imports", "values": vals, "colour": C.PALETTE[0]}],
        labels, y_min=0, y_max=3.2, height=46, y_ticks=4, dp=2, unit=" Mt",
        y_fmt=lambda v: f"{v:.1f}", area=True, pad_l=11,
    )


def tbl_eu_imports(rows):
    out = ['<table class="compact"><thead><tr><th>Year</th>'
           '<th class="num">Total organic imports (t)</th><th class="num">Change</th>'
           '<th style="width:8mm">Ev.</th><th>Note</th></tr></thead><tbody>']
    for r in rows:
        chs = signed(num(r["pct_change"]))
        out.append(f'<tr><td class="num">{esc(r["year"])}</td>'
                   f'<td class="num">{C.nb(num(r["total_tonnes"]))}</td>'
                   f'<td class="num">{chs}</td><td>{grade_badge(r["grade"])}</td>'
                   f'<td>{esc(r["note"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def fig_preparations(rows):
    bars = [(r["country"], num(r["tonnes_2024"])) for r in rows]
    return C.hbar(bars, highlight="Morocco", label_w="30mm", val_w="20mm", unit=" t")


def tbl_preparations(rows):
    out = ['<table><thead><tr><th class="num" style="width:7mm">#</th><th>Supplier</th>'
           '<th class="num">2024 (t)</th><th class="num">Share of category</th>'
           '<th class="num">Change on 2023</th><th style="width:8mm">Ev.</th>'
           "</tr></thead><tbody>"]
    for r in rows:
        hi = ' class="hi"' if r["country"] == "Morocco" else ""
        ys = signed(num(r["yoy_pct"]))
        out.append(f'<tr{hi}><td class="num rank">{esc(r["rank"])}</td><td>{esc(r["country"])}</td>'
                   f'<td class="num">{C.nb(num(r["tonnes_2024"]))}</td>'
                   f'<td class="num">{num(r["share_pct"]):.1f} %</td>'
                   f'<td class="num">{ys}</td><td>{grade_badge(r["grade"])}</td></tr>')
    out.append('<tr class="total"><td></td><td>Category total, all origins</td>'
               '<td class="num">130 708</td><td class="num">100.0 %</td>'
               '<td class="num">+7.6 %</td><td></td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_suppliers(rows):
    out = ['<table><thead><tr><th class="num" style="width:7mm">#</th><th>Origin</th>'
           '<th class="num">2024 (t)</th><th class="num">2023 (t)</th>'
           '<th class="num">Change</th><th class="num">Share of EU total</th>'
           '<th style="width:8mm">Ev.</th></tr></thead><tbody>']
    for r in rows:
        a, b = num(r["tonnes_2024"]), num(r["tonnes_2023"])
        ch = (a - b) / b * 100
        out.append(f'<tr><td class="num rank">{esc(r["rank"])}</td><td>{esc(r["country"])}</td>'
                   f'<td class="num">{C.nb(a)}</td><td class="num">{C.nb(b)}</td>'
                   f'<td class="num">{signed(ch)}</td>'
                   f'<td class="num">{num(r["share_pct_calc"]):.2f} %</td>'
                   f'<td>{grade_badge(r["grade"])}</td></tr>')
    out.append('<tr class="hi"><td class="num rank">&ndash;</td><td>Morocco '
               '<span style="font-weight:400">(all organic categories)</span></td>'
               '<td class="num" colspan="4">not published in any retrievable table</td>'
               '<td></td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_africa_exports(rows):
    out = ['<table class="compact"><thead><tr><th>Origin</th><th class="num">Year</th>'
           '<th class="num">Tonnes</th><th class="num">Rank</th>'
           '<th>Basis / category</th><th style="width:8mm">Ev.</th>'
           "</tr></thead><tbody>"]
    for r in rows:
        hi = ' class="hi"' if r["country"] == "Morocco" else (
            ' class="total"' if "total" in r["country"] else "")
        rk = esc(r["eu_rank"]) if r["eu_rank"] else "&ndash;"
        out.append(f'<tr{hi}><td>{esc(r["country"])}</td><td class="num">{esc(r["year"])}</td>'
                   f'<td class="num">{C.nb(num(r["tonnes"]))}</td><td class="num">{rk}</td>'
                   f'<td>{esc(r["category"])}</td><td>{grade_badge(r["grade"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_operators(rows, status):
    out = ['<table class="compact"><thead><tr><th>Operator</th><th>Location</th>'
           '<th>Legal form</th><th>Organic range</th><th>Certification evidence</th>'
           '<th>EU</th></tr></thead><tbody>']
    n = 0
    for r in rows:
        if not r["verification"].startswith(status):
            continue
        n += 1
        out.append(
            f'<tr><td><b>{esc(r["name"])}</b></td><td>{esc(r["city_region"])}</td>'
            f'<td>{esc(r["type"])}</td><td>{esc(r["products"])}</td>'
            f'<td>{esc(r["certifications"])}</td><td>{esc(r["eu_market"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out), n


def tbl_timeline(rows):
    out = ['<table class="compact"><thead><tr><th style="width:20mm">Date</th>'
           '<th>Event</th><th style="width:44mm">Instrument</th>'
           '<th>Consequence for Morocco</th></tr></thead><tbody>']
    for r in rows:
        key = r["date"] in ("2025-01-01", "2024-12-31")
        cls = ' class="hi"' if key else ""
        out.append(f'<tr{cls}><td class="num">{esc(r["date"])}</td><td>{esc(r["event"])}</td>'
                   f'<td>{esc(r["instrument"])}</td>'
                   f'<td>{esc(r["relevance_to_morocco"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_retail(rows):
    out = ['<table class="compact"><thead><tr><th>Market</th>'
           '<th class="num">Retail value (bn EUR)</th><th class="num">Year</th>'
           '<th class="num">Growth</th><th>Note</th></tr></thead><tbody>']
    for r in rows:
        gs = signed(num(r["growth_pct"]))
        out.append(f'<tr><td>{esc(r["market"])}</td>'
                   f'<td class="num">{num(r["value_bn_eur"]):.1f}</td>'
                   f'<td class="num">{esc(r["data_year"])}</td><td class="num">{gs}</td>'
                   f'<td>{esc(r["note"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_targets(rows):
    out = ['<table class="compact"><thead><tr><th>Programme</th><th class="num">Period</th>'
           '<th class="num">Budget (bn MAD)</th><th class="num">Area target (ha)</th>'
           '<th class="num">Output (t)</th><th class="num">Exports (t)</th>'
           '<th>Outcome</th></tr></thead><tbody>']
    for r in rows:
        g = lambda k: (C.nb(num(r[k])) if num(r[k]) else "&ndash;")  # noqa: E731
        b = num(r["budget_mad_bn"])
        bs = f"{b:.2f}" if b else "&ndash;"
        out.append(f'<tr><td><b>{esc(r["programme"])}</b></td>'
                   f'<td class="num">{esc(r["period"])}</td>'
                   f'<td class="num">{bs}</td>'
                   f'<td class="num">{g("target_area_ha")}</td>'
                   f'<td class="num">{g("target_production_t")}</td>'
                   f'<td class="num">{g("target_exports_t")}</td>'
                   f'<td>{esc(r["outcome"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_cjeu(rows):
    out = ['<table class="compact"><thead><tr><th style="width:52mm">Case</th>'
           '<th class="num" style="width:20mm">Date</th><th>Subject</th>'
           '<th>Holding</th></tr></thead><tbody>']
    for r in rows:
        out.append(f'<tr><td><b>{esc(r["case"])}</b></td><td class="num">{esc(r["date"])}</td>'
                   f'<td>{esc(r["subject"])}</td><td>{esc(r["holding"])}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def tbl_sources(rows):
    out = ['<div class="sources"><table class="compact srcs"><thead><tr>'
           '<th style="width:12mm">Ref</th><th>Title</th><th style="width:40mm">Publisher</th>'
           '<th class="num" style="width:11mm">Year</th><th style="width:18mm">Tier</th>'
           "</tr></thead><tbody>"]
    for r in rows:
        out.append(f'<tr><td class="mono">{esc(r["ref"])}</td>'
                   f'<td>{esc(r["title"])}<span class="u">{esc(r["url"])}</span></td>'
                   f'<td>{esc(r["publisher"])}</td><td class="num">{esc(r["year"])}</td>'
                   f'<td>{esc(r["tier"])}</td></tr>')
    out.append("</tbody></table></div>")
    return "\n".join(out)


# ===========================================================================
# assemble
# ===========================================================================

def main():
    area = load("morocco_area_series.csv")
    africa = load("africa_organic_land.csv")
    imports = load("eu_organic_imports.csv")
    suppliers = load("eu_top_suppliers_2024.csv")
    preps = load("eu_fruitveg_preparations_2024.csv")
    afx = load("africa_eu_organic_exports.csv")
    ops = load("morocco_organic_operators.csv")
    timeline = load("eu_regulatory_timeline.csv")
    retail = load("eu_organic_retail.csv")
    targets = load("morocco_targets.csv")
    cjeu = load("cjeu_western_sahara.csv")
    sources = load("sources.csv")

    op_v, n_v = tbl_operators(ops, "Verified")
    op_p, n_p = tbl_operators(ops, "Partial")
    op_r, n_r = tbl_operators(ops, "Register-only")

    n_africa_data = len([r for r in africa if num(r["organic_ag_land_ha"])])

    frag = {
        "FIG_MOROCCO_AREA": fig_morocco_area(area),
        "TBL_MOROCCO_AREA": tbl_morocco_area(area),
        "FIG_AFRICA_TOP": fig_africa_top(africa),
        "TBL_AFRICA": tbl_africa(africa),
        "FIG_EU_IMPORTS": fig_eu_imports(imports),
        "TBL_EU_IMPORTS": tbl_eu_imports(imports),
        "FIG_PREPARATIONS": fig_preparations(preps),
        "TBL_PREPARATIONS": tbl_preparations(preps),
        "TBL_SUPPLIERS": tbl_suppliers(suppliers),
        "TBL_AFRICA_EXPORTS": tbl_africa_exports(afx),
        "TBL_OPERATORS_VERIFIED": op_v,
        "TBL_OPERATORS_PARTIAL": op_p,
        "TBL_OPERATORS_REGISTER": op_r,
        "TBL_TIMELINE": tbl_timeline(timeline),
        "TBL_RETAIL": tbl_retail(retail),
        "TBL_TARGETS": tbl_targets(targets),
        "TBL_CJEU": tbl_cjeu(cjeu),
        "TBL_SOURCES": tbl_sources(sources),
        "N_VERIFIED": str(n_v),
        "N_PARTIAL": str(n_p),
        "N_REGISTER": str(n_r),
        "N_OPERATORS": str(n_v + n_p + n_r),
        "N_AFRICA_DATA": str(n_africa_data),
        "N_SOURCES": str(len(sources)),
    }

    html = (SRC / "report.html").read_text(encoding="utf-8")
    missing = set(re.findall(r"\{\{(\w+)\}\}", html)) - set(frag)
    if missing:
        raise SystemExit(f"Unfilled tokens in report.html: {sorted(missing)}")
    for k, v in frag.items():
        html = html.replace("{{" + k + "}}", v)

    rendered = SRC / "report.rendered.html"
    rendered.write_text(html, encoding="utf-8")

    from weasyprint import HTML
    HTML(str(rendered), base_url=str(SRC)).write_pdf(str(OUT))
    print(f"wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"operators: {n_v} verified / {n_p} partial / {n_r} register-only")
    print(f"african countries with a land figure: {n_africa_data} of {len(africa)}")


if __name__ == "__main__":
    main()
