"""The rankings of the column buff-ranking.md: the strongest teas and pies, tried in every combination with the rules
of the Buff Planner (scripts/consume_calc.py, content/research/farming/consumable-effects.md).

    python3 content/columns/buff-ranking.py            # the tables of the column, in Japanese
    python3 content/columns/buff-ranking.py en         # in English
    python3 content/columns/buff-ranking.py check      # the tables in the column (both languages) are these

Four ways to compare, each in its own table:
- gather: value x time of one tea (or pie) with no bear pie, a bear pie or a rich bear pie eaten at the same time
- window: the average bonus over 15, 30 and 60 minutes when the same tea (and pie) is had again as soon as it ends
- fight: the effects that help in a fight (max health, healing speed, clotting, radiation), the strongest of each, and
  whether they can all work at once (one of a kind each)
- cost: value x time per base ingredient, following the recipes of the mixing table and the cooking workbench down to
  what is not made (berries, cream, meat ...)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import consume_calc as cc  # noqa: E402

GATHER = ["Ore_Yield", "Wood_Yield", "Scrap_Yield", "Harvesting"]
FIGHT = ["Max_Health", "MetabolismBooster", "Clotting", "Radiation_Resistance"]
PIES = [None, "pie.bear", "pie.bear.rich"]
WINDOWS = [15, 30, 60]
TOP = 5
TYPE_NAMES = {"Ore_Yield": ("鉱石", "Ore"), "Wood_Yield": ("木", "Wood"), "Scrap_Yield": ("スクラップ", "Scrap"),
              "Harvesting": ("採集 (動物と魚)", "Harvesting (animals, fish)"), "Max_Health": ("最大体力", "Max health"),
              "MetabolismBooster": ("体力の戻り", "Healing speed"), "Clotting": ("止血", "Clotting"),
              "Radiation_Resistance": ("放射線のダメージ", "Radiation damage")}
WORDS = {"ja": {"none": "なし", "item": "お茶・パイ", "pie": "熊肉パイ", "peak": "効き目", "time": "続く時間", "score": "値 × 時間",
                "avg": "平均", "drinks": "使う数", "kind": "効果", "best": "いちばん強い", "longest": "いちばん長い",
                "per": "材料 1 つあたり", "base": "材料", "min": "{m} 分", "rank": "順位", "uses": "{n} 回使う"},
         "en": {"none": "none", "item": "Tea or pie", "pie": "Bear Pie", "peak": "Effect", "time": "Lasts", "score": "Value × time",
                "avg": "Average", "drinks": "Used", "kind": "Effect", "best": "Strongest", "longest": "Longest",
                "per": "Per ingredient", "base": "Ingredients", "min": "{m} min", "rank": "Rank", "uses": "{n} uses"}}


def load() -> tuple[dict, dict, dict]:
    items = cc.newest_items()
    names = yaml.safe_load((ROOT / "rules" / "item-names-ja.yml").read_text(encoding="utf-8"))["names"]
    return items, names, cc.newest_recipes()


def buffs(items: dict) -> list[str]:
    """The items with a timed effect a player gets (the teas and pies of the Buff Planner)."""
    return [sn for sn, it in items.items() if sn not in cc.UNOBTAINABLE
            and any(m["type"] not in cc.NOT_ON_PLAYER for m in ((it.get("stats") or {}).get("consume") or {}).get("modifiers") or [])]


def mods(items: dict, sn: str) -> dict[str, tuple[float, float]]:
    return {m["type"]: (m["value"], m["duration"]) for m in items[sn]["stats"]["consume"]["modifiers"] if m["type"] not in cc.NOT_ON_PLAYER}


def area(sim: dict, type_: str, until: float | None = None) -> float:
    """value x seconds of a type in a simulation, up to `until` seconds if given."""
    return sum(s["v"] * (min(s["b"], until) - s["a"] if until else s["b"] - s["a"])
               for s in sim["segs"].get(type_, []) if until is None or s["a"] < until)


def gather(items: dict, made: dict) -> dict[str, list[dict]]:
    out = {}
    for t in GATHER:
        rows = []
        for sn in buffs(items):
            if t not in mods(items, sn) or sn.startswith("pie.bear") or sn not in made:
                continue
            for pie in PIES:
                eats = [(0, sn)] + ([(0, pie)] if pie else [])
                sim = cc.simulate(items, eats)
                segs = sim["segs"][t]
                rows.append({"item": sn, "pie": pie, "peak": max(s["v"] for s in segs), "time": segs[-1]["b"],
                             "score": area(sim, t) / 60})
        rows.sort(key=lambda r: (-r["score"], -r["peak"], r["item"], str(r["pie"])))
        out[t] = rows
    return out


def window(items: dict, made: dict) -> dict[str, dict[int, list[dict]]]:
    """For each gathering kind and window, the best ways when the tea (and pie) is had again as soon as it ends."""
    out = {}
    for t in GATHER:
        out[t] = {}
        for w in WINDOWS:
            rows = []
            for sn in buffs(items):
                if t not in mods(items, sn) or sn.startswith("pie.bear") or sn not in made:
                    continue
                for pie in PIES:
                    eats = [(0, sn)] + ([(0, pie)] if pie else [])
                    while True:   # have again what runs out first (all that end then), and work it out once more
                        sim = cc.simulate(items, eats)
                        last = {x: j for j, (_u, x) in enumerate(eats)}   # the latest row of each item
                        ends = [(sim["row_ends"][j], x) for x, j in last.items() if sim["row_ends"].get(j, w * 60) < w * 60]
                        if not ends:
                            break
                        first = min(e for e, _x in ends)
                        eats += [(e, x) for e, x in ends if abs(e - first) < 1e-9]
                    rows.append({"item": sn, "pie": pie, "avg": area(sim, t, w * 60) / (w * 60),
                                 "drinks": sum(1 for _t0, s in eats if s == sn), "pies": sum(1 for _t0, s in eats if s == pie)})
            rows.sort(key=lambda r: (-r["avg"], r["drinks"] + r["pies"], r["item"], str(r["pie"])))
            out[t][w] = rows
    return out


def fight(items: dict, made: dict) -> dict[str, list[dict]]:
    out = {}
    for t in FIGHT:
        rows = [{"item": sn, "value": mods(items, sn)[t][0], "time": mods(items, sn)[t][1]}
                for sn in buffs(items) if t in mods(items, sn) and sn in made]
        rows.sort(key=lambda r: (-r["value"], -r["time"], r["item"]))
        out[t] = rows
    return out


def cost(items: dict, made: dict) -> dict[str, list[dict]]:
    out = {}
    for t in GATHER + ["Max_Health"]:
        rows = []
        for sn in buffs(items):
            if t not in mods(items, sn) or sn not in made:
                continue
            v, d = mods(items, sn)[t]
            b = cc.base_ingredients(made, sn)
            n = sum(b.values())
            rows.append({"item": sn, "base": b, "n": n, "score": v * 100 * d / 60, "per": v * 100 * d / 60 / float(n)})
        rows.sort(key=lambda r: (-r["per"], r["item"]))
        out[t] = rows
    return out


def fmt_pct(v: float, t: str) -> str:
    if t == "Radiation_Resistance":
        return f"−{round(v * 100)}%"
    if t == "MetabolismBooster":
        return f"×{1 + v:g}"
    if t == "Clotting":
        return f"{v:g}"
    return f"+{round(v * 1000) / 10:g}%"


def tables(lang: str) -> dict[str, str]:
    """The Markdown tables of the column by name: gather-<kind>, window-<kind>, fight, cost-<kind>."""
    items, names, made = load()
    w = WORDS[lang]
    nm = (lambda sn: names[sn]) if lang == "ja" else (lambda sn: items[sn]["name"])
    mins = lambda s: w["min"].format(m=f"{s / 60:g}")  # noqa: E731

    def icon(sn: str) -> str:
        """The colour icon of a tea (by its first effect), a pie (the basic and the rich share one) or an ingredient."""
        if sn in items and not sn.startswith("pie.") and mods(items, sn):
            return f"{{ci:{next(iter(mods(items, sn)))}}}"
        return f"{{ci:{sn.removesuffix('.rich')}}}"

    def link(sn: str, pie: str | None = None, label: str | None = None) -> str:
        """The item with its icon, opening the Buff Planner with it (and the bear pie) eaten at second 0."""
        e = f"{sn}:0" + (f",{pie}:0" if pie else "")
        return f"{icon(sn)}[{label or nm(sn)}](../tools/buff.html?e={e})"
    out = {}
    for t, rows in gather(items, made).items():
        lines = [f"| {w['rank']} | {w['item']} | {w['pie']} | {w['peak']} | {w['time']} | {w['score']} |", "|---|---|---|---|---|---|"]
        for k, r in enumerate(rows[:TOP], 1):
            lines.append(f"| {k} | {link(r['item'], r['pie'])} | {icon(r['pie']) + nm(r['pie']) if r['pie'] else w['none']} | {fmt_pct(r['peak'], t)} | {mins(r['time'])} | {r['score'] * 100:,.0f} |")
        out[f"gather-{t}"] = "\n".join(lines)
    for t, by in window(items, made).items():
        lines = [f"| {w['rank']} | " + " | ".join(f"{mins(m * 60)}" for m in WINDOWS) + " |", "|---|" + "---|" * len(WINDOWS)]
        for k in range(3):
            cells = []
            for m in WINDOWS:
                r = by[m][k]
                label = nm(r["item"]) + (f" + {nm(r['pie'])}" if r["pie"] else "")
                cells.append(f"{link(r['item'], r['pie'], label)} ({w['avg']} {fmt_pct(r['avg'], t)}, {w['uses'].format(n=r['drinks'] + r['pies'])})")
            lines.append(f"| {k + 1} | " + " | ".join(cells) + " |")
        out[f"window-{t}"] = "\n".join(lines)
    lines = [f"| {w['kind']} | {w['best']} | {w['longest']} |", "|---|---|---|"]
    for t, rows in fight(items, made).items():
        strong = rows[0]
        long = max(rows, key=lambda r: (r["time"], r["value"]))
        lines.append(f"| {TYPE_NAMES[t][0 if lang == 'ja' else 1]} | {link(strong['item'])} ({fmt_pct(strong['value'], t)}, {mins(strong['time'])}) "
                     f"| {link(long['item'])} ({fmt_pct(long['value'], t)}, {mins(long['time'])}) |")
    out["fight"] = "\n".join(lines)
    for t, rows in cost(items, made).items():
        lines = [f"| {w['rank']} | {w['item']} | {w['score']} | {w['base']} | {w['per']} |", "|---|---|---|---|---|"]
        for k, r in enumerate(rows[:TOP], 1):
            parts = ", ".join(f"{icon(b)}{nm(b) if b in names or lang == 'en' else b} {float(n):g}" for b, n in sorted(r["base"].items(), key=lambda x: (-x[1], x[0])))
            lines.append(f"| {k} | {link(r['item'])} | {r['score']:,.0f} | {parts} | {r['per']:,.1f} |")
        out[f"cost-{t}"] = "\n".join(lines)
    return out


def check() -> int:
    bad = []
    for lang, path in [("ja", ROOT / "content" / "columns" / "buff-ranking.md"), ("en", ROOT / "content" / "columns" / "en" / "buff-ranking.md")]:
        text = path.read_text(encoding="utf-8")
        for name, table in tables(lang).items():
            m = re.search(rf"<!-- table:{re.escape(name)} -->\n(.*?)\n<!-- /table -->", text, re.S)
            if not m:
                bad.append(f"{path.name} ({lang}): no table {name}")
            elif m.group(1).strip() != table:
                bad.append(f"{path.name} ({lang}): the table {name} is not what the program gives")
    for line in bad:
        print("NG " + line, file=sys.stderr)
    if not bad:
        print(f"OK buff ranking: {len(tables('ja'))} tables in each language match the program")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        sys.exit(check())
    for name, table in tables(sys.argv[1] if sys.argv[1:] else "ja").items():
        print(f"<!-- table:{name} -->\n{table}\n<!-- /table -->\n")
