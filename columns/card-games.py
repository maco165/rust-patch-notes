"""The blackjack of the column card-games.md, rewritten from scratch: same rules, none of the game's code.

    python3 content/columns/card-games.py              # 1,000,000 rounds with seed 1, the numbers quoted in the column
    python3 content/columns/card-games.py 500000 7     # other counts and seeds

Rules reproduced: a fresh 10-deck shoe every round, the dealer draws on soft 17, a two-card 21 pays 3:2
(also after a split), double on any two cards without an ace, one split per round, split aces get one card each,
and the dealer's two-card 21 is only revealed at the end (doubled and split bets are lost to it).
"""
import collections
import functools
import random
import sys

DECKS = 10
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # one suit, 2..K then the ace (11)
SHOE = VALUES * 4 * DECKS  # built in order: deck by deck, suit by suit. The last card is the top of the shoe.
UNIFORM = {v: VALUES.count(v) / 13 for v in set(VALUES)}  # chance of each value when the shoe is treated as endless


class Shoe:
    """A shuffled shoe. Cards are taken from the end of the list.

    The shuffle walks n from the top down and swaps position n with a random position BELOW n (never n itself).
    Position n is final after its step, so doing the step only when a card is taken gives the same result.
    With fair=True position n may also stay, which is the textbook shuffle, kept here for comparison.
    """

    def __init__(self, rng: random.Random, fair: bool = False, cards: list[int] = SHOE):
        self.cards, self.n, self.rng, self.fair = cards[:], len(cards), rng, fair

    def take(self) -> int:
        self.n -= 1
        n = self.n
        if n:
            k = self.rng.randrange(n + 1 if self.fair else n)
            self.cards[k], self.cards[n] = self.cards[n], self.cards[k]
        return self.cards[n]


def best(hard: int, ace: bool) -> int:
    """hard counts every ace as 1. One ace counts as 11 when that does not go over 21."""
    return hard + 10 if ace and hard + 10 <= 21 else hard


def add(hard: int, ace: bool, card: int) -> tuple[int, bool]:
    return (hard + 1, True) if card == 11 else (hard + card, ace)


def state(cards: list[int]) -> tuple[int, bool]:
    return sum(1 if c == 11 else c for c in cards), 11 in cards


def dealer_draws(hard: int, ace: bool) -> bool:
    """The dealer stops on a hard 17 or more and on a soft 18 to 21. A soft 17 draws."""
    return not (hard >= 17 or (ace and 18 <= hard + 10 <= 21))


def settle(cards: list[int], bet: int, dealer: list[int]) -> int:
    """What comes back for one hand. A two-card 21 ("natural") pays bet * 2.5 rounded down, a win bet * 2, a tie bet."""
    mine, natural = best(*state(cards)), len(cards) == 2 and best(*state(cards)) == 21
    if mine > 21:
        return 0
    house = best(*state(dealer))
    if len(dealer) == 2 and house == 21:
        return bet if natural else 0
    if house > 21:
        house = 0
    if mine > house or (mine == house and natural):
        return bet * 5 // 2 if natural else bet * 2
    return bet if mine == house else 0


# --- basic strategy, worked out for these rules with the shoe treated as endless ---

@functools.cache
def dealer_final(hard: int, ace: bool) -> tuple[tuple[int, float], ...]:
    """Chances of the dealer's final total from this state (0 = bust)."""
    if not dealer_draws(hard, ace):
        return ((best(hard, ace) if best(hard, ace) <= 21 else 0, 1.0),)
    out = collections.Counter()
    for card, p in UNIFORM.items():
        for total, q in dealer_final(*add(hard, ace, card)):
            out[total] += p * q
    return tuple(out.items())


def dealer_from(up: int, hole=None) -> tuple[tuple[int, float], ...]:
    """Chances of the dealer's result given the face-up card. 22 stands for a two-card 21."""
    out = collections.Counter()
    for card, p in (hole or UNIFORM).items():
        hard, ace = add(*add(0, False, up), card)
        for total, q in ((22, 1.0),) if best(hard, ace) == 21 else dealer_final(hard, ace):
            out[total] += p * q
    return tuple(out.items())


class Strategy:
    """Expected results per unit bet against one face-up card, and the best move for each hand."""

    def __init__(self, up: int, hole=None):
        self.dealer = dealer_from(up, hole)
        self.play = functools.cache(self.play)

    def stand(self, hard: int, ace: bool, natural: bool = False) -> float:
        mine = best(hard, ace)
        if mine > 21:
            return -1.0
        ev = 0.0
        for house, q in self.dealer:
            if house == 22:
                ev -= 0.0 if natural else q
            elif natural:
                ev += 1.5 * q
            else:
                ev += q * ((mine > house) - (mine < house))
        return ev

    def play(self, hard: int, ace: bool, fresh: bool, pair: int = 0) -> tuple[float, str]:
        """(expected result, move). fresh: two cards, so a double is allowed. pair: value of a pair that may split."""
        if best(hard, ace) >= 21:
            return self.stand(hard, ace), "S"
        options = [(self.stand(hard, ace), "S"),
                   (sum(p * self.play(*add(hard, ace, c), False)[0] for c, p in UNIFORM.items()), "H")]
        if fresh and not ace:
            options.append((2 * sum(p * self.stand(*add(hard, ace, c)) for c, p in UNIFORM.items()), "D"))
        if pair:
            options.append((2 * sum(p * self.after_split(pair, c) for c, p in UNIFORM.items()), "P"))
        return max(options)

    def after_split(self, pair: int, card: int) -> float:
        hard, ace = state([pair, card])
        if best(hard, ace) == 21:
            return self.stand(hard, ace, natural=True)  # ten + ace after a split still pays 3:2
        return self.stand(hard, ace) if pair == 11 else self.play(hard, ace, True)[0]


STRATEGY = {up: Strategy(up) for up in UNIFORM}


def basic(hard: int, ace: bool, fresh: bool, pair: int, up: int) -> str:
    return STRATEGY[up].play(hard, ace, fresh, pair)[1]


def like_dealer(hard: int, ace: bool, fresh: bool, pair: int, up: int) -> str:
    return "H" if dealer_draws(hard, ace) else "S"


def never_bust(hard: int, ace: bool, fresh: bool, pair: int, up: int) -> str:
    return "H" if hard <= 11 and best(hard, ace) <= 17 else "S"


def expected_basic(first=None, second=None, up_card=None, hole=None) -> float:
    """Expected result of basic strategy per unit bet, shoe treated as endless. The four dicts can skew the first deal."""
    total = 0.0
    for up, pu in (up_card or UNIFORM).items():
        table = Strategy(up, hole) if hole else STRATEGY[up]
        for c1, p1 in (first or UNIFORM).items():
            for c2, p2 in (second or UNIFORM).items():
                hard, ace = state([c1, c2])
                if best(hard, ace) == 21:
                    total += pu * p1 * p2 * table.stand(hard, ace, natural=True)
                else:
                    total += pu * p1 * p2 * table.play(hard, ace, True, c1 if c1 == c2 else 0)[0]
    return total


def without_starting_card(position: int) -> dict[int, float]:
    """Values of the card dealt from this shoe position: any card except the one that started there."""
    left = collections.Counter(SHOE)
    left[SHOE[position]] -= 1
    return {value: n / (len(SHOE) - 1) for value, n in left.items()}


# --- one round at the table ---

def play_hand(cards: list[int], bet: int, up: int, shoe: Shoe, choose, may_split: bool) -> list[tuple[list[int], int]]:
    while True:
        hard, ace = state(cards)
        if best(hard, ace) >= 21:
            return [(cards, bet)]
        fresh = len(cards) == 2
        move = choose(hard, ace, fresh, cards[0] if may_split and fresh and cards[0] == cards[1] else 0, up)
        if move == "S":
            return [(cards, bet)]
        if move == "P":
            first, second = [cards[0], shoe.take()], [cards[1], shoe.take()]
            if cards[0] == 11:
                return [(first, bet), (second, bet)]
            return play_hand(first, bet, up, shoe, choose, False) + play_hand(second, bet, up, shoe, choose, False)
        cards.append(shoe.take())
        if move == "D":
            return [(cards, bet * 2)]


def play_round(rng: random.Random, choose, bet: int = 10, fair: bool = False) -> tuple[int, int, bool]:
    """One player against the dealer. Returns (staked, returned, natural). A new shoe every round, as in the game."""
    shoe = Shoe(rng, fair)
    player, dealer = [shoe.take()], [shoe.take()]  # the dealer's first card stays face down
    player.append(shoe.take())
    dealer.append(shoe.take())                      # the second one is face up
    natural = best(*state(player)) == 21
    hands = [(player, bet)] if natural else play_hand(player, bet, dealer[1], shoe, choose, True)
    if any(best(*state(cards)) <= 21 for cards, _ in hands) and not all(
            len(cards) == 2 and best(*state(cards)) == 21 for cards, _ in hands):
        while dealer_draws(*state(dealer)):
            dealer.append(shoe.take())
    return sum(b for _, b in hands), sum(settle(cards, b, dealer) for cards, b in hands), natural


def simulate(rounds: int, seed: int, choose, fair: bool = False) -> dict[str, float]:
    rng = random.Random(seed)
    net_sum = net_sq = naturals = 0
    outcome = collections.Counter()
    for _ in range(rounds):
        staked, returned, natural = play_round(rng, choose, 10, fair)
        net = (returned - staked) / 10
        net_sum += net
        net_sq += net * net
        naturals += natural
        outcome["win" if net > 0 else "lose" if net < 0 else "tie"] += 1
    mean = net_sum / rounds
    error = ((net_sq / rounds - mean * mean) / rounds) ** 0.5
    return {"mean": mean, "error": error, "naturals": naturals / rounds,
            **{k: outcome[k] / rounds for k in ("win", "tie", "lose")}}


def holds_top_card(rounds: int, seed: int, players: int, fair: bool = False) -> list[float]:
    """A 52-card deck dealt one card at a time around the table, twice. How often each seat holds card 51,
    the one that starts on top of the unshuffled deck (the ace of clubs in the game's order)."""
    rng = random.Random(seed)
    held = [0] * players
    for _ in range(rounds):
        deck = Shoe(rng, fair, list(range(52)))
        for i in range(2 * players):
            if deck.take() == 51:
                held[i % players] += 1
    return [n / rounds for n in held]


def main() -> None:
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    print(f"rounds={rounds} seed={seed} decks={DECKS} cards={len(SHOE)}")
    print(f"basic strategy, endless shoe (calculated): {expected_basic():+.3%} of the first bet per round")
    top = len(SHOE) - 1  # one player: own cards from positions top and top-2, dealer's hidden card top-1, face-up top-3
    skewed = expected_basic(*(without_starting_card(top - i) for i in (0, 2, 3, 1)))
    print(f"same, first four cards as this shuffle deals them (calculated): {skewed:+.3%}")
    for name, choose in (("basic strategy", basic), ("play like the dealer", like_dealer), ("never risk a bust", never_bust)):
        r = simulate(rounds, seed, choose)
        print(f"{name:>20}: {r['mean']:+.3%} +-{r['error']:.3%}  win {r['win']:.2%} tie {r['tie']:.2%} "
              f"lose {r['lose']:.2%}  two-card 21: {r['naturals']:.3%}")
    # The hidden card's place held a ten-value card before the shuffle, and a card never stays in its place.
    tens, cards = 16 * DECKS - 1, 52 * DECKS - 2
    print(f"insurance (pays 2:1): {3 * tens / cards - 1:+.2%} of the insurance bet, knowing only the dealer's ace")
    for fair in (False, True):
        shares = " ".join(f"{x:.2%}" for x in holds_top_card(rounds, seed, 2, fair))
        print(f"52 cards, 2 seats, {'textbook' if fair else 'this'} shuffle: seat holds the top card of the new deck: {shares}")
    print("basic strategy (rows: player, columns: dealer 2..10, A)")
    ups = sorted(UNIFORM)
    for label, rows in (("hard", [(h, False, 0) for h in range(5, 21)]), ("soft", [(h, True, 0) for h in range(3, 11)]),
                        ("pair", [(2 if v == 11 else 2 * v, v == 11, v) for v in ups])):
        for hard, ace, pair in rows:
            name = f"{pair},{pair}".replace("11", "A") if pair else f"{best(hard, ace)}"
            print(f"  {label} {name:>5}: " + " ".join(basic(hard, ace, True, pair, up) for up in ups))


if __name__ == "__main__":
    main()
