"""The loot roll of the column loot-containers.md, rewritten from scratch: same behaviour, none of the game's code.

The sample table is a cut-down military crate: its component table and its small side slots. The two big
slots of the real crate (one of 96 workbench level 2 items at 40%, one workbench upgrade at 5%) are left out.

    python3 content/columns/loot-containers.py            # 100,000 crates with seed 1, the numbers quoted in the column
    python3 content/columns/loot-containers.py 500000 7   # other counts and seeds
"""
import collections
import random
import sys

# A table either lists weighted sub-tables (one is picked) or items (all are given).
# Sub-tables: name -> [(weight, sub-table name)]
TABLES = {
    "Components": [(120, "SmgBody"), (80, "RifleBody"), (100, "TechParts"), (100, "Pipes"), (100, "TurretParts"),
                   (100, "HighQualityMetal")],
    "TurretParts": [(55, "Computer"), (45, "Camera"), (5, "AutoTurret")],
}
# Items: name -> [(item, amount, max amount)]. A max that is not above the amount means "always the amount".
ITEMS = {
    "SmgBody": [("smgbody", 1, 1)],
    "RifleBody": [("riflebody", 1, 1)],
    "TechParts": [("techparts", 2, 4)],
    "Pipes": [("metalpipe", 5, 6)],
    "HighQualityMetal": [("metal.refined", 15, 25)],
    "Computer": [("targeting.computer", 1, 0)],
    "Camera": [("cctv.camera", 1, 0)],
    "AutoTurret": [("autoturret", 1, -1)],
    "SupplySignal": [("supply.signal", 1, 0)],
    "Backpack": [("largebackpack", 1, 1)],
    "ArmorInsert": [("clothing.mod.armorinsert_metal", 1, 1)],
    "BlueprintPage": [("blueprintpage", 1, 0)],
    "HeavyFuse": [("fuse.highgrade", 1, 1)],
}
# The crate: (table, number of tries, chance of each try), rolled top to bottom when the crate appears.
SLOTS = [("Components", 1, 1.0), ("SupplySignal", 1, 0.01), ("Backpack", 1, 0.05), ("ArmorInsert", 1, 0.05),
         ("BlueprintPage", 1, 0.10), ("HeavyFuse", 1, 0.06)]
SCRAP = 8


def roll_amount(amount: float, maximum: float, rng: random.Random) -> int:
    """A real number between amount and maximum, cut down to a whole number: the maximum itself never comes out."""
    if maximum > 0 and maximum > amount:
        return max(1, int(rng.uniform(amount, maximum)))
    return max(1, int(amount))


def spawn(table: str, rng: random.Random, box: collections.Counter) -> None:
    """Walk the tree from one table: pick one sub-table by weight until a table of items is reached."""
    subs = TABLES.get(table)
    if subs:
        left = sum(weight for weight, _ in subs)
        pick = rng.randrange(left)              # a whole number from 0 to total - 1
        for weight, name in subs:
            left -= weight
            if pick >= left:
                spawn(name, rng, box)
                return
    for item, amount, maximum in ITEMS.get(table, []):
        box[item] += roll_amount(amount, maximum, rng)


def fill(rng: random.Random) -> collections.Counter:
    """One crate. Nothing about who opens it, when or where comes in: only the tables and random numbers."""
    box: collections.Counter = collections.Counter()
    for table, tries, chance in SLOTS:
        for _ in range(tries):
            if rng.random() <= chance:
                spawn(table, rng, box)
    box["scrap"] += SCRAP
    return box


def chance_per_call(table: str) -> dict[str, float]:
    """Exact chance that one walk from this table gives each item."""
    subs = TABLES.get(table)
    if not subs:
        return {item: 1.0 for item, _, _ in ITEMS.get(table, [])}
    total = sum(weight for weight, _ in subs)
    out: dict[str, float] = collections.defaultdict(float)
    for weight, name in subs:
        for item, p in chance_per_call(name).items():
            out[item] += weight / total * p
    return dict(out)


def chance_per_box() -> dict[str, float]:
    """Exact chance of at least one per crate: 1 - product over the tries of (1 - chance x chance per walk)."""
    miss: dict[str, float] = collections.defaultdict(lambda: 1.0)
    for table, tries, chance in SLOTS:
        for item, p in chance_per_call(table).items():
            miss[item] *= (1 - chance * p) ** tries
    return {"scrap": 1.0, **{item: 1 - m for item, m in miss.items()}}


def main() -> None:
    boxes = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    seen: collections.Counter = collections.Counter()
    amounts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for _ in range(boxes):
        for item, amount in fill(rng).items():
            seen[item] += 1
            amounts[item][amount] += 1
    print(f"crates={boxes}")
    for item, p in sorted(chance_per_box().items(), key=lambda kv: -kv[1]):
        low, high = min(amounts[item], default=0), max(amounts[item], default=0)
        print(f"{item:<32} computed {p:7.2%}  seen {seen[item] / boxes:7.2%}  amount {low}-{high}")
    tech = amounts["techparts"]
    print("techparts (2 to 4 in the table): " + ", ".join(f"{n} x {tech[n] / sum(tech.values()):.1%}" for n in (2, 3, 4)))


if __name__ == "__main__":
    main()
