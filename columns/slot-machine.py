"""The slot machine of the column slot-machine.md, rewritten from scratch: same behaviour, none of the game's code.

    python3 content/columns/slot-machine.py              # 1,000,000 spins with seed 1, the numbers quoted in the column
    python3 content/columns/slot-machine.py 5000000 7    # other counts and seeds
"""
import collections
import itertools
import random
import sys
from fractions import Fraction

# The 16 faces of a reel in order, with the weight each has out of 330 stops (0: never comes up).
FACES = [("scrap", 8), ("rope", 40), ("apple", 1), ("lowgrade", 8), ("wood", 100), ("bandage", 40), ("charcoal", 100),
         ("gunpowder", 1), ("rust", 1), ("meat", 1), ("hammer", 1), ("sulfur", 8), ("techscrap", 1), ("frags", 0),
         ("cloth", 0), ("seven", 20)]
STOPS = sum(weight for _, weight in FACES)  # 330
# Scrap paid for three of the same face at a bet of 2 scrap.
TRIPLES = {"charcoal": 15, "wood": 25, "rope": 40, "bandage": 45, "lowgrade": 80, "sulfur": 100, "scrap": 400, "seven": 1000}
BONUS_FACE, BONUS = "lowgrade", 5  # paid per face shown, on any reel, on top of a triple
COST = 2
SEEDS = 1000  # each reel draws a seed from 0..999 and takes the first number of a .NET System.Random(seed)
INT_MAX = 2147483647


def dotnet_first_sample(seed: int) -> float:
    """The first Sample() of .NET's System.Random(seed): Knuth's subtractive generator, as published by Microsoft."""
    table = [0] * 56
    previous = 161803398 - abs(seed)
    table[55] = previous
    value, index = 1, 0
    for _ in range(54):
        index = (index + 21) % 55
        table[index] = value
        value = previous - value
        if value < 0:
            value += INT_MAX
        previous = table[index]
    for _ in range(4):
        for i in range(1, 56):
            mixed = table[i] - table[1 + (i + 30) % 55]
            mixed = (mixed + 2**31) % 2**32 - 2**31  # 32-bit wrap-around
            table[i] = mixed + INT_MAX if mixed < 0 else mixed
    number = table[1] - table[22]
    if number == INT_MAX:
        number -= 1
    if number < 0:
        number += INT_MAX
    return number * (1.0 / INT_MAX)


def face_of_stop(stop: int) -> str:
    """Walk the weights until the stop falls inside a face."""
    edge = 0
    for name, weight in FACES:
        edge += weight
        if stop < edge:
            return name
    return FACES[-1][0]


# What each of the 1,000 seeds shows on a reel. This table is the whole reel.
REEL = [face_of_stop(int(dotnet_first_sample(seed) * STOPS)) for seed in range(SEEDS)]


def spin(source: random.Random) -> tuple[str, str, str]:
    """One pull: three seeds, one per reel, each on its own."""
    return tuple(REEL[source.randrange(SEEDS)] for _ in range(3))


def payout(faces: tuple[str, str, str], multiplier: int = 1) -> int:
    """Scrap that comes back: the bonus per bonus face, plus the triple if all three match, times the multiplier."""
    total = BONUS * faces.count(BONUS_FACE)
    if faces[0] == faces[1] == faces[2]:
        total += TRIPLES.get(faces[0], 0)
    return total * multiplier


def exact_return(chance: dict[str, Fraction]) -> tuple[Fraction, Fraction]:
    """(average payout per spin, chance of any payout) from the chance of each face on one reel."""
    average = hit = Fraction(0)
    for faces in itertools.product(chance, repeat=3):
        p = chance[faces[0]] * chance[faces[1]] * chance[faces[2]]
        won = payout(faces)
        average += p * won
        hit += p if won else 0
    return average, hit


def main() -> None:
    spins = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    source = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    seeds_per_face = collections.Counter(REEL)
    designed = {name: Fraction(weight, STOPS) for name, weight in FACES}
    actual = {name: Fraction(seeds_per_face[name], SEEDS) for name, _ in FACES}

    print("face        weight  designed  seeds/1000")
    for name, weight in FACES:
        print(f"{name:<10} {weight:>6}  {float(designed[name]):>8.2%}  {seeds_per_face[name]:>10}")
    for label, chance in (("designed (weight/330)", designed), ("actual (seeds/1000)", actual)):
        average, hit = exact_return(chance)
        print(f"exact, {label}: back {float(average):.4f} per {COST} bet = {float(average / COST):.2%}, "
              f"any payout {float(hit):.2%}, three sevens 1 in {float(1 / chance['seven'] ** 3):,.0f}")

    back = wins = sevens = longest = dry = 0
    for _ in range(spins):
        faces = spin(source)
        won = payout(faces)
        back += won
        wins += won > 0
        sevens += faces == ("seven", "seven", "seven")
        dry = 0 if won else dry + 1
        longest = max(longest, dry)
    print(f"simulated, spins={spins}: back {back / spins:.4f} per {COST} bet = {back / spins / COST:.2%}, "
          f"any payout {wins / spins:.2%}, three sevens {sevens} times, longest run without a payout {longest}")


if __name__ == "__main__":
    main()
