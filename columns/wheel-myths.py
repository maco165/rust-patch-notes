"""The roulette of the column wheel-myths.md, rewritten from scratch: same behaviour, none of the game's code.

    python3 content/columns/wheel-myths.py            # 100,000 spins with seed 1, the numbers quoted in the column
    python3 content/columns/wheel-myths.py 500000 7   # other counts and seeds
    python3 content/columns/wheel-myths.py old        # the wheel before 2024-05, worked out exactly (frame 1/30 s)
    python3 content/columns/wheel-myths.py old 256    # the same with a frame of 1/256 s
"""
import collections
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


# Before 2024-05 the wheel was not told where to stop. A spin added a random speed (7 to `top`) to the wheel at
# rest; each frame it turned min(180 x speed, 180) degrees a second and lost min(max(speed / 2, 0.1), 1) x the
# frame time of speed. It stopped wherever that took it, the segment nearest the pointer won, and the next spin
# started from there. `top` was 10 until 2023-04 and 16 from 2023-05.
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


def old_era(top: float, frame: float = FRAME) -> None:
    """Print how the old wheel's next result leans on the previous one. Not a simulation: the start speed (7 to
    `top`) and where in the previous segment the wheel rested are both spread evenly over a fine grid, so the
    numbers are exact for these assumptions and the same on every run. Segments are taken as evenly spaced
    (14.4 degrees); in today's bundle they sit 13.6 to 15.1 degrees apart."""
    speeds = [7 + (top - 7) * (i + 0.5) / 4000 for i in range(4000)]
    grid = [7 + (top - 7) * i / 400 for i in range(401)]
    turns = [old_turn(v, frame) for v in grid]
    step = (top - 7) / 400

    def turn(v: float) -> float:
        x = (v - 7) / step
        i = min(int(x), 399)
        return turns[i] + (turns[i + 1] - turns[i]) * (x - i)

    rests = [SECTOR * ((i + 0.5) / 100 - 0.5) for i in range(100)]   # where in the previous segment it rested
    ahead = [0.0] * len(SEGMENTS)   # the next result, counted from the previous one in the turning direction
    for v in speeds:
        t = turn(v)
        for r in rests:
            ahead[round((r + t) / SECTOR) % len(SEGMENTS)] += 1 / (len(speeds) * len(rests))
    print(f"start speed 7 to {top:g}, frame 1/{round(1 / frame)} s: one spin turns {turns[0]:.0f} to {turns[-1]:.0f}"
          f" degrees ({(turns[-1] - turns[0]) / 360:.2f} turns of spread)")
    print("  next result, segments ahead of the previous one: "
          + " ".join(f"{j}:{a:.2%}" for j, a in enumerate(ahead)))
    # Turning the wheel the positive way takes the pointer to lower segment numbers (today's DoSpin aims at
    # -(360 / 25) x segment), so j segments ahead of segment k is segment k - j.
    for n in (1, 3, 5, 10, 20):
        back = {k: sum(ahead[j] for j in range(len(SEGMENTS)) if SEGMENTS[(k - j) % len(SEGMENTS)] == n) * (1 + n)
                for k in range(len(SEGMENTS))}
        best = max(back, key=back.get)
        print(f"  {n:>2}: return on 1 after the best previous segment {back[best]:.4f} (segment {best}), "
              f"worst {min(back.values()):.4f}, above 1 after {sum(b > 1 for b in back.values())} of 25 segments")


def main() -> None:
    if sys.argv[1:2] == ["old"]:
        frame = 1 / float(sys.argv[2]) if len(sys.argv) > 2 else FRAME
        for top in (10.0, 16.0):
            old_era(top, frame)
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
