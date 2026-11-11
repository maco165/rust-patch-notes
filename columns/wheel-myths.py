"""The roulette of the column wheel-myths.md, rewritten from scratch: same behaviour, none of the game's code.

    python3 content/columns/wheel-myths.py            # 100,000 spins with seed 1, the numbers quoted in the column
    python3 content/columns/wheel-myths.py 500000 7   # other counts and seeds
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


def main() -> None:
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
