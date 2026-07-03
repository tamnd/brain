---
title: "CF 103069K - Allin"
description: "We are given a simplified heads-up Texas hold ’em situation with only two players and no folding. Each test case provides five cards: two private cards for Wolf Chicken and three shared community cards representing the flop."
date: "2026-07-04T01:01:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103069
codeforces_index: "K"
codeforces_contest_name: "2020 ICPC Asia East Continent Final"
rating: 0
weight: 103069
solve_time_s: 46
verified: true
draft: false
---

[CF 103069K - Allin](https://codeforces.com/problemset/problem/103069/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simplified heads-up Texas hold ’em situation with only two players and no folding. Each test case provides five cards: two private cards for Wolf Chicken and three shared community cards representing the flop. Two more community cards and the opponent’s two private cards are still unknown.

The question is not to simulate an actual poker game, but to decide something stronger: whether Wolf Chicken can guarantee a win regardless of how the remaining four cards are chosen from the unseen deck. If there exists even one possible completion of the board and opponent hand that allows the opponent to tie or beat Wolf Chicken, then Wolf Chicken must not go all-in. Only if Wolf Chicken’s current information already forces a strict win in every possible future state should we answer that he can all-in.

This transforms the problem into a worst-case dominance check over all completions of a 7-card poker evaluation problem.

The constraints are extremely large, up to 100000 test cases. Each test case is constant-sized input, so the solution must be O(1) per case after preprocessing. Any attempt to enumerate possible community cards or opponent hands is immediately impossible because there are tens of thousands of combinations even for a single test case.

The key difficulty is not evaluating poker hands, but reasoning about certainty under adversarial completion of hidden information.

A few subtle edge cases illustrate why naive reasoning fails. If Wolf Chicken already has a strong made hand like a straight or flush from the flop plus hole cards, it is still not automatically winning because the opponent may form an even stronger hand depending on unknown cards. For example, having a flush draw or even a completed flush does not guarantee victory if a straight flush is still possible for the opponent with remaining cards.

Another edge case is full house vs potential four of a kind. Even if Wolf Chicken currently holds trips, the remaining unknown cards might allow the opponent to complete quads, which strictly beats a full house. So local evaluation of current strength is insufficient.

The real challenge is to recognize when the visible cards already force a “locked” strongest possible poker configuration that cannot be overtaken by any completion of the remaining cards.

## Approaches

A direct brute force solution would attempt to simulate all possible outcomes of the remaining two community cards and all possible opponent hole cards drawn from the remaining deck. For each completion, we would evaluate both players’ best five-card hands over seven cards and check if Wolf Chicken always wins.

This approach is conceptually correct but completely infeasible. After removing five known cards, there are 47 unknown cards. We must choose 4 of them for the opponent and future community, leading to combinatorial explosion on the order of hundreds of millions of cases per test. Even with aggressive pruning, evaluating poker strength for each configuration is far beyond any reasonable limit.

The key observation is that “certainty of winning” is extremely rare in poker and only happens when Wolf Chicken already has a maximal structure that cannot be broken by any future draw. The only way to guarantee a win is to already hold a royal flush, and more importantly, ensure that no unknown card configuration can create an equal or higher-ranked royal flush for the opponent.

However, since suits are not shared and cards are unique, if Wolf Chicken already has a royal flush formed entirely from known cards (hole + flop), then no future cards can improve the opponent’s hand beyond that level, because a royal flush is the absolute maximum hand type and is defined on a specific suit structure that cannot be replicated without the exact missing cards.

Thus the problem collapses to checking whether Wolf Chicken already has a completed royal flush using his two hole cards plus the three flop cards.

If yes, the answer is “allin”. Otherwise, the answer is “check”, because in all other cases there exists at least one completion where the opponent can match or beat the best possible hand.

This reduction is powerful because it avoids reasoning about all hand classes. Instead, we identify that only the absolute top hand has a certainty property under adversarial completion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of all completions | O(C(47,4) × evaluations) | O(1) | Too slow |
| Check for existing royal flush only | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We reduce each test case to checking whether the five visible cards already form a royal flush.

1. Convert each card rank into a numeric scale where Ten, Jack, Queen, King, Ace correspond to consecutive high values in order. This allows direct comparison and pattern matching without string logic. This step is necessary because we only care about exact rank structure, not suit interactions beyond equality.
2. Group the five given cards by suit. A royal flush must lie entirely within a single suit, so any candidate solution must have all five cards sharing the same suit.
3. For each suit group, collect the ranks present and check whether the set contains exactly Ten, Jack, Queen, King, Ace. This verifies both completeness and exact structure.
4. If any suit satisfies this condition, immediately output “allin”, since the player already holds the strongest possible poker hand and no future combination can surpass it.
5. If no suit satisfies the condition, output “check”, since the current configuration does not force a guaranteed win under any completion of hidden cards.

The reason this is sufficient is that poker hand rankings are strictly ordered, and royal flush is the unique maximal element. Any hand that is not already a royal flush can be improved or matched by an adversarial completion of hidden cards, so it cannot guarantee a strict win.

## Python Solution

```python
import sys
input = sys.stdin.readline

RANK_MAP = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, 'T': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

ROYAL = {10, 11, 12, 13, 14}

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        parts = input().split()
        suits = {}
        ranks_by_suit = {}

        for card in parts:
            r = RANK_MAP[card[0]]
            s = card[1]
            if s not in ranks_by_suit:
                ranks_by_suit[s] = set()
            ranks_by_suit[s].add(r)

        ok = False
        for s in ranks_by_suit:
            if ranks_by_suit[s] == ROYAL:
                ok = True
                break

        out.append("allin" if ok else "check")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first encodes ranks so comparisons are consistent and fast. It then aggregates cards by suit using sets to avoid duplication issues and to allow direct equality checking against the royal flush requirement. The final check is a simple set comparison, which captures both presence and completeness of the required five ranks.

A subtle point is that we do not need to ensure ordering or continuity explicitly, because the royal flush condition fully determines both.

## Worked Examples

Consider a case where all five visible cards form a royal flush in hearts.

| Step | Hearts set |
| --- | --- |
| Process cards | {10, J, Q, K, A} |
| Check condition | equals ROYAL |
| Result | allin |

This demonstrates the winning condition is detected purely by set equality.

Now consider a mixed-suit case where only part of a royal structure exists.

| Step | Spade set |
| --- | --- |
| Process cards | {10, J, Q, A} |
| Check condition | missing K |
| Result | check |

This shows that incomplete structures cannot qualify even if they look close to a royal flush.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test processes exactly 5 cards with constant-time operations |
| Space | O(1) | Only fixed-size maps and sets are used per test |

The solution easily fits within limits since even 100000 test cases only involve a few hundred thousand constant operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""2
AC KC QC JC TC
AC TD 8S 5H 2C
""") == """allin
check"""

# already a royal flush
assert run("""1
AH KH QH JH TH
""") == "allin"

# almost royal but missing one card
assert run("""1
AH KH QH JH 9H
""") == "check"

# mixed suits cannot form royal flush
assert run("""1
AS KH QH JH TH
""") == "check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| royal flush | allin | positive detection |
| missing rank | check | near-miss rejection |
| mixed suit | check | suit constraint enforcement |

## Edge Cases

A key edge case is when all five cards have the correct ranks but are split across suits. For example, having Ten through Ace present but not in a single suit.

Input:

```
AH KH QH JS TS
```

Even though all required ranks exist, they are not unified by suit, so no royal flush exists. The algorithm correctly groups by suit and fails the equality check, producing “check”.

Another edge case is duplicate-like rank distribution across suits where multiple partial royal patterns exist. Even then, because no single suit contains all five required ranks, no false positive occurs.
