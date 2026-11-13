"""The roulette of the column wheel-myths.md, rewritten from scratch: same behaviour, none of the game's code.

    python3 content/columns/wheel-myths.py            # 100,000 spins with seed 1, the numbers quoted in the column
    python3 content/columns/wheel-myths.py 500000 7   # other counts and seeds
    python3 content/columns/wheel-myths.py old        # the wheel before 2024-05, worked out exactly (frame 1/30 s),
                                                      # with the segments where they really are and evenly spaced
    python3 content/columns/wheel-myths.py old 256    # the same with a frame of 1/256 s
"""
import collections
import math
import random
import sys

# The 25 segments in order. Each number is the multiplier paid when it wins.
SEGMENTS = [3, 1, 10, 1, 3, 1, 5, 1, 5, 3, 1, 10, 1, 3, 1, 5, 1, 3, 1, 20, 1, 3, 1, 5, 1]


def spin(source: random.Random) -> int:
    """One round: a fresh generator from a new seed, then one of the 25 segments with equal chance."""
    fresh = random.Random(source.getrandbits(32))
    return fresh.randrange(len(SEGMENTS))


def payout(bets: dict[int, int], segment: int) -> int:
    """What comes back for bets {number: amount}: the winning bet times (1 + number). The others are lost."""
    number = SEGMENTS[segment]
    return bets.get(number, 0) * (1 + number)


# Where the 25 segment markers sit on the wheel (x, z in the wheel's own frame, every marker at y 0.0627) and
# where the pointer is, read from the wheel's prefab. They are the same in the game client of 2018-12-14, 2020-11,
# 2021-08 and 2024-04 and in the server of 2026-11. The markers are not evenly spaced.
MARKERS = [(-0.3695, -0.0256), (-0.3625, 0.0663), (-0.3329, 0.1573), (-0.2834, 0.2356), (-0.2164, 0.2973),
           (-0.1349, 0.3414), (-0.0465, 0.3658), (0.0501, 0.3650), (0.1392, 0.3428), (0.2175, 0.2989),
           (0.2862, 0.2359), (0.3368, 0.1568), (0.3662, 0.0666), (0.3727, -0.0213), (0.3560, -0.1164),
           (0.3129, -0.2038), (0.2543, -0.2739), (0.1785, -0.3283), (0.0954, -0.3647), (-0.0019, -0.3763),
           (-0.0920, -0.3608), (-0.1785, -0.3284), (-0.2540, -0.2726), (-0.3143, -0.1995), (-0.3523, -0.1164)]
MARKER_Y = 0.0627
POINTER = (-1.4821, 0.063, 0.0001)
NUMBERS = (1, 3, 5, 10, 20)


def distance(segment: int, angle: float) -> float:
    """How far a segment's marker is from the pointer when the wheel is turned `angle` degrees about its up axis."""
    x, z = MARKERS[segment]
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    return math.dist((x * c + z * s, MARKER_Y, -x * s + z * c), POINTER)


def nearest(angle: float) -> int:
    """The segment that wins when the wheel rests at `angle`: the marker nearest the pointer."""
    return min(range(len(MARKERS)), key=lambda k: distance(k, angle))


def real_arcs() -> list[tuple[float, float]]:
    """Per segment, the wheel angles at which it wins: (start, width) in degrees. The edges are where the nearest
    marker changes, found by halving the interval."""
    steps = 3600
    seq = [nearest(360 * (g + 0.5) / steps) for g in range(steps)]
    edges = []
    for g in range(steps):
        a, b = seq[g], seq[(g + 1) % steps]
        if a != b:
            lo, hi = 360 * (g + 0.5) / steps, 360 * (g + 1.5) / steps
            for _ in range(50):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if distance(a, mid) < distance(b, mid) else (lo, mid)
            edges.append((lo % 360, b))
    assert len(edges) == len(MARKERS)
    arcs = {}
    for n, (start, k) in enumerate(edges):
        arcs[k] = (start, (edges[(n + 1) % len(edges)][0] - start) % 360)
    return [arcs[k] for k in range(len(MARKERS))]


def even_arcs() -> list[tuple[float, float]]:
    """The same order and direction with every segment 14.4 degrees wide, centred where segment 0 is centred."""
    start, width = real_arcs()[0]
    centre = start + width / 2
    return [((centre - SECTOR * k - SECTOR / 2) % 360, SECTOR) for k in range(len(MARKERS))]


# Before 2024-05 the wheel was not told where to stop. A spin added a random speed (7 to `top`) to the wheel at
# rest; each frame it turned min(180 x speed, 180) degrees a second and lost min(max(speed / 2, 0.1), 1) x the
# frame time of speed. It stopped wherever that took it, the segment nearest the pointer won, and the next spin
# started from there. `top` was 10 until 2023-05-03 and 16 from 2023-05-04.
SECTOR = 360 / len(SEGMENTS)
FRAME = 1 / 30   # the frame time of the server; 1/30 to 1/256 change the turn by under 2 degrees


def old_turn(speed: float, frame: float = FRAME) -> float:
    """How far one old spin turns the wheel, in degrees, from its start speed."""
    turned = 0.0
    while speed > 0:
        rate = min(180 * speed, 180)
        speed = max(0.0, speed - frame * min(max(speed / 2, 0.1), 1.0))
        turned += rate * frame
    return turned


def old_turns(top: float, frame: float, count: int = 2000) -> list[float]:
    """The turn of `count` start speeds spread evenly over 7 to `top` (the turn is read off a grid of 401 speeds)."""
    step = (top - 7) / 400
    grid = [old_turn(7 + step * i, frame) for i in range(401)]
    turns = []
    for i in range(count):
        x = (top - 7) * (i + 0.5) / count / step
        j = min(int(x), 399)
        turns.append(grid[j] + (grid[j + 1] - grid[j]) * (x - j))
    return turns


def overlap(a: float, a_width: float, b: float, b_width: float) -> float:
    """Degrees shared by two arcs of the circle that start at a and b (both in 0..360)."""
    return sum(max(0.0, min(a + a_width, b + n + b_width) - max(a, b + n)) for n in (-360, 0, 360))


def old_era(top: float, frame: float, arcs: list[tuple[float, float]]) -> dict:
    """How the old wheel's next result leans on the previous one, worked out exactly rather than simulated.
    In the long run the wheel's angle is spread evenly round the circle (adding a random turn to an angle keeps
    that spread), so after the previous segment k the angle is spread evenly over k's arc. Each start speed then
    turns it by the same amount; `step[k][j]` is the chance that segment j wins next."""
    turns = old_turns(top, frame)
    step = []
    for start, width in arcs:
        row = [0.0] * len(arcs)
        for t in turns:
            moved = (start + t) % 360
            for j, (other, other_width) in enumerate(arcs):
                row[j] += overlap(moved, width, other, other_width)
        step.append([r / (len(turns) * width) for r in row])
    share = {n: sum(w for (_, w), m in zip(arcs, SEGMENTS) if m == n) / 360 for n in NUMBERS}
    after = {n: [sum(p for p, m in zip(step[k], SEGMENTS) if m == n) * (1 + n) for k in range(len(arcs))]
             for n in NUMBERS}
    return {"turns": (turns[0], turns[-1]), "share": share, "after": after, "step": step}


def show_old(top: float, frame: float, layout: str) -> None:
    arcs = real_arcs() if layout == "real" else even_arcs()
    r = old_era(top, frame, arcs)
    lo, hi = r["turns"]
    print(f"start speed 7 to {top:g}, frame 1/{round(1 / frame)} s, segments {layout}: one spin turns {lo:.0f} to "
          f"{hi:.0f} degrees ({(hi - lo) / 360:.2f} turns of spread)")
    if layout == "even":
        # the wheel turned the positive way brings lower segment numbers to the pointer: j ahead of 0 is -j
        ahead = [r["step"][0][-j % len(SEGMENTS)] for j in range(len(SEGMENTS))]
        print("  next result, segments ahead of the previous one: "
              + " ".join(f"{j}:{a:.2%}" for j, a in enumerate(ahead)))
    else:
        print("  arc of each segment (degrees): " + " ".join(f"{k}:{w:.2f}" for k, (_, w) in enumerate(arcs)))
    for n in NUMBERS:
        back = r["after"][n]
        best = max(range(len(back)), key=back.__getitem__)
        print(f"  {n:>2}: wins {r['share'][n]:.2%}, return on 1 without looking {r['share'][n] * (1 + n):.4f}; "
              f"after the best previous segment {back[best]:.4f} (segment {best}), worst {min(back):.4f}, above 1 after "
              f"{sum(b > 1 for b in back)} of 25 segments")


# From 2024-05 the result is drawn first and the wheel is turned to -(360 / 25) x segment + 3.852 + a random
# -6 to 6 degrees. The payout follows the drawn segment; the marker nearest the pointer can be another one.
def new_look() -> None:
    """How often the marker nearest the pointer is not the paid segment: the part of the -6..6 degree spread
    around each segment's goal that falls outside that segment's arc, worked out exactly."""
    arcs = real_arcs()
    misses = [1 - overlap((-SECTOR * k + 3.852 - 6) % 360, 12, *arcs[k]) / 12 for k in range(len(arcs))]
    worst = max(range(len(misses)), key=misses.__getitem__)
    print(f"from 2024-05: the marker nearest the pointer is not the paid segment in "
          f"{sum(misses) / len(misses):.2%} of spins on average, at most {misses[worst]:.2%} (segment {worst})")


def main() -> None:
    if sys.argv[1:2] == ["old"]:
        frame = 1 / float(sys.argv[2]) if len(sys.argv) > 2 else FRAME
        for layout in ("real", "even"):
            for top in (10.0, 16.0):
                show_old(top, frame, layout)
        new_look()
        return
    spins = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    source = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    hits = collections.Counter()
    back = collections.Counter()
    longest_without_20 = current = 0
    for _ in range(spins):
        segment = spin(source)
        number = SEGMENTS[segment]
        hits[number] += 1
        for n in (1, 3, 5, 10, 20):
            back[n] += payout({n: 100}, segment)
        current = 0 if number == 20 else current + 1
        longest_without_20 = max(longest_without_20, current)
    print(f"spins={spins}")
    for n in (1, 3, 5, 10, 20):
        expected = SEGMENTS.count(n) / len(SEGMENTS)
        print(f"{n:>2}: hit {hits[n] / spins:.2%} (expected {expected:.0%})  "
              f"average return on 100 = {back[n] / spins - 100:+.2f}")
    print(f"longest run without 20: {longest_without_20}")


if __name__ == "__main__":
    main()
