---
title: "CF 102365B - Balanced Fighters"
description: "We have up to 100 fighters. Each fighter is described by a name and three statistics: health, attack, and defence. When two fighters meet, every round deals fixed damage to both sides."
date: "2026-08-12T23:45:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102365
codeforces_index: "B"
codeforces_contest_name: "UBC Programming Contest 2019 (UBCPC 2019)"
rating: 0
weight: 102365
solve_time_s: 92
verified: true
draft: false
---

[CF 102365B - Balanced Fighters](https://codeforces.com/problemset/problem/102365/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We have up to 100 fighters. Each fighter is described by a name and three statistics: health, attack, and defence. When two fighters meet, every round deals fixed damage to both sides. A fighter's incoming damage is their opponent's attack minus their own defence, clamped at zero. Both damage values are applied simultaneously.

The task is to find every set of three fighters whose pairwise results form a directed cycle. For three fighters A, B, and C, this means one fighter beats the second, the second beats the third, and the third beats the first. A draw does not count as a win, so every edge in the cycle must represent an actual victory.

The first input line gives N, followed by N fighter descriptions. The output starts with the number of valid triples, followed by one line for every such triple. The order of the triples and the order of the three names inside each triple are unrestricted.

The constraint N <= 100 is small enough for O(N^3), which means we can inspect every possible group of three. What we cannot afford is repeatedly simulating thousands of combat rounds for every pair inside every triple. With 100 fighters there are C(100, 3) = 161,700 triples, and potentially millions or billions of round operations if every combat is simulated directly. The useful target is thus to make every pairwise fight constant time, then spend O(N^3) only on checking triples.

The health, attack, and defence values are at most 10,000. Python integers easily handle all products involved, so there is no overflow issue. More importantly, the maximum health bounds the number of rounds needed to kill a fighter once positive damage is being dealt, but relying on that fact for a direct simulation would still be far too expensive.

There are several edge cases that can make a careless implementation wrong. The first is a fight where neither fighter can damage the other. For example,

```
1
Solo 500 500 500
```

has no opponent, so the answer is simply zero. More generally, if both incoming damage values are zero, the fight never ends and must be treated as a draw. A simulation that waits for one health value to become nonpositive without checking zero damage would loop forever.

A second edge case is simultaneous death. Consider two fighters with the following statistics:

```
2
A 4 6 1
B 10 3 1
```

A deals 5 damage per round to B, while B deals 2 damage per round to A. B dies after 2 rounds, while A also reaches zero after 2 rounds. The result is a draw, not an A victory. The winning condition is strict: after the killing round, the winner must still have positive health.

A third edge case occurs when one fighter needs several rounds to defeat the other. Suppose A deals 5 damage per round to B, B starts with 10 HP, and B deals 2 damage per round to A. If A has 5 HP, both fighters die after the second round. If A instead has 6 HP, A survives that round and wins. Using a non-strict comparison such as `<=` in the final health test would incorrectly classify the first case as a win.

Finally, draws must not accidentally become edges in the graph of fighter results. A triple containing a draw cannot be an intransitive triple, even if the other two pairwise matches form wins.

## Approaches

The direct approach is to enumerate every triple of fighters and simulate the three fights needed to determine whether it is intransitive. This is correct because the definition of an intransitive triple depends only on those three pairwise results. If a combat is simulated one round at a time, each round updates both health values until one fighter is dead or the fight is recognized as a draw.

The problem is the repeated work. There are 161,700 possible triples when N is 100. Each triple needs three combats, and a combat can require up to 10,000 rounds when the damage per round is only one point. That gives a worst-case upper bound of roughly 4.85 billion simulated rounds. The actual number can be smaller for many inputs, but this is nowhere near suitable for a one-second limit.

The key observation is that a fight does not actually require round-by-round simulation. Against a fixed opponent, both fighters take exactly the same damage every round. We can calculate how many rounds each fighter needs to die and compare those two numbers directly.

Suppose A is fighting B. Let

`damage_to_A = max(0, AT_B - DF_A)`

and

`damage_to_B = max(0, AT_A - DF_B)`.

If `damage_to_B` is positive, B dies after

`ceil(HP_B / damage_to_B)`

rounds. At exactly that round, A wins precisely when A's remaining health is positive. Thus A beats B when

`ceil(HP_B / damage_to_B) * damage_to_A < HP_A`.

If B cannot damage A's opponent, meaning `damage_to_B` is zero, B can never die, so A cannot win. The same reasoning handles the opposite direction.

This turns every pairwise combat into O(1). We can precompute the winner of every ordered pair once, storing the result in a boolean matrix. After that, checking a triple requires only a few boolean operations. The brute-force idea still survives at the outer level, but the expensive part has been removed.

The relationship between the two approaches is therefore simple. The brute-force solution works because every triple can be checked independently, but it fails because it repeatedly performs the same combat simulation. The observation that combat has constant damage per round lets us replace every simulation with an arithmetic calculation. Once all pairwise results are cached, checking all triples in O(N^3) is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^3 · H) | O(1) | Too slow |
| Optimal | O(N^2 + N^3) = O(N^3) | O(N^2) | Accepted |

Here H is the maximum number of simulated rounds, which can be as large as 10,000.

## Algorithm Walkthrough

1. Read all fighters and store their names, health, attack, and defence. We keep the fighters in input order so that each combination of indices `i < j < k` represents exactly one set of three fighters.
2. Create an N by N boolean matrix `win`. The value `win[i][j]` will mean that fighter i defeats fighter j. A missing or false value means that i does not win, which includes both a loss and a draw.
3. For every ordered pair of distinct fighters A and B, calculate the damage A receives from B and the damage B receives from A. These values never change during the fight, so there is no reason to simulate individual rounds.
4. If B's damage to A is zero, A cannot possibly defeat B, because A's health can never reach zero. Otherwise calculate the number of rounds B needs to die as `(HP_B + damage_to_B - 1) // damage_to_B`. A wins exactly when the damage A receives during those rounds is still strictly smaller than A's starting health.
5. Store the result in `win[A][B]`. Repeat this for every ordered pair. Since the outcome of a fight is not necessarily symmetric, both directions need to be considered, although in practice the calculation for one pair can determine both.
6. Enumerate every triple `i < j < k`. A triple is valid if the results form a cycle in either orientation. We check `i beats j`, `j beats k`, `k beats i`, or the reverse cycle `i beats k`, `k beats j`, `j beats i`.

Checking both orientations matters because the output does not prescribe which fighter must appear first. For any three fighters that form a directed cycle, exactly one of these two orientations will match.
7. Store every valid triple and finally print its count followed by the three corresponding fighter names. Because indices are considered only with `i < j < k`, the same set of fighters can never be output twice.

Why it works: after preprocessing, `win[A][B]` is true exactly when A has positive health after the round in which B reaches zero health. The formula for that round count is exact because B loses the same positive amount every round. If B cannot take damage, the stored result is false, correctly representing a draw or a situation where A cannot win. Thus every edge in the `win` matrix exactly represents a real victory. For every three indices, the algorithm accepts precisely when those three edges form a directed cycle, which is exactly the definition of an intransitive triple.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    fighters = []
    for _ in range(n):
        name, hp, atk, defense = input().split()
        fighters.append((name, int(hp), int(atk), int(defense)))

    win = [[False] * n for _ in range(n)]

    for i in range(n):
        name_a, hp_a, atk_a, def_a = fighters[i]

        for j in range(n):
            if i == j:
                continue

            name_b, hp_b, atk_b, def_b = fighters[j]

            damage_to_a = max(0, atk_b - def_a)
            damage_to_b = max(0, atk_a - def_b)

            if damage_to_b == 0:
                continue

            rounds_to_kill_b = (
                hp_b + damage_to_b - 1
            ) // damage_to_b

            if rounds_to_kill_b * damage_to_a < hp_a:
                win[i][j] = True

    answer = []

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                cycle_1 = (
                    win[i][j]
                    and win[j][k]
                    and win[k][i]
                )

                cycle_2 = (
                    win[i][k]
                    and win[k][j]
                    and win[j][i]
                )

                if cycle_1 or cycle_2:
                    answer.append(
                        (fighters[i][0], fighters[j][0], fighters[k][0])
                    )

    print(len(answer))
    for a, b, c in answer:
        print(a, b, c)

if __name__ == "__main__":
    solve()
```

The input loop stores each fighter as `(name, HP, AT, DF)`. Converting the three statistics to integers immediately keeps the later arithmetic simple.

The pairwise preprocessing follows the fourth and fifth algorithm steps. For A against B, `damage_to_b` is the amount B loses each round. If it is zero, B can never reach zero HP, so A cannot win and the matrix entry remains false.

When `damage_to_b` is positive, the ceiling division computes the exact first round at whose end B's health is nonpositive. The expression `(hp_b + damage_to_b - 1) // damage_to_b` is the standard integer-only form of ceiling division. Python's arbitrary-precision integers also make the multiplication `rounds_to_kill_b * damage_to_a` safe without any special handling.

The comparison is deliberately strict. If the product equals `hp_a`, A also reaches zero in that round, so the fight is a draw. A victory requires `rounds_to_kill_b * damage_to_a < hp_a`.

The triple loops use `i < j < k`, so every unordered set of three fighters appears exactly once. The two cycle expressions cover both possible orientations of a directed three-cycle. A draw never satisfies either expression because draws are represented by false entries in `win`.

No combat simulation appears in the final program. Every pair is reduced to a few arithmetic operations, and every triple is reduced to six boolean lookups.

## Worked Examples

The first sample contains five fighters:

```
5
TheStrong 90 60 10
TheInvincible 10000 10000 10000
TheTough 70 50 25
TheBrick 3 1 4159
TheResilient 160 40 10
```

The relevant pairwise results can be traced as follows.

| Pair | Damage to first | Damage to second | Rounds to kill second | First survives? | Result |
| --- | --- | --- | --- | --- | --- |
| TheStrong vs TheTough | 40 | 35 | 2 | 90 - 70 = 20 > 0 | Strong wins |
| TheTough vs TheResilient | 15 | 40 | 4 | 70 - 60 = 10 > 0 | Tough wins |
| TheResilient vs TheStrong | 30 | 50 | 2 | 160 - 60 = 100 > 0 | Resilient wins |

These three results form the cycle `TheStrong -> TheTough -> TheResilient -> TheStrong`. The other fighters do not create another valid cycle, so the final output is one triple.

```
1
TheStrong TheTough TheResilient
```

The official sample permits any ordering of the names, so this is equivalent to the sample's ordering.

The second sample contains only one fighter:

```
1
TheLonely 500 500 500
```

The triple enumeration has no combination satisfying `i < j < k`, so no pairwise combat needs to be performed at all.

| i | j | k | Triple checked? | Result |
| --- | --- | --- | --- | --- |
| none | none | none | No, N < 3 | No triples |

The output is consequently:

```
0
```

This trace exercises the smallest possible input and confirms that the algorithm does not assume that at least three fighters exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^3) | O(N^2) pairwise preprocessing plus O(N^3) triple enumeration |
| Space | O(N^2) | The winner matrix stores one result for every ordered pair |

For N = 100, the triple enumeration examines only 161,700 combinations. The pairwise preprocessing examines 10,000 ordered pairs, and every operation inside those loops is constant time. This is comfortably within the stated limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    fighters = []

    for _ in range(n):
        name, hp, atk, defense = input().split()
        fighters.append((name, int(hp), int(atk), int(defense)))

    win = [[False] * n for _ in range(n)]

    for i in range(n):
        _, hp_a, atk_a, def_a = fighters[i]

        for j in range(n):
            if i == j:
                continue

            _, hp_b, atk_b, def_b = fighters[j]

            damage_to_a = max(0, atk_b - def_a)
            damage_to_b = max(0, atk_a - def_b)

            if damage_to_b == 0:
                continue

            rounds = (hp_b + damage_to_b - 1) // damage_to_b

            if rounds * damage_to_a < hp_a:
                win[i][j] = True

    answer = []

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if (
                    (win[i][j] and win[j][k] and win[k][i])
                    or
                    (win[i][k] and win[k][j] and win[j][i])
                ):
                    answer.append((
                        fighters[i][0],
                        fighters[j][0],
                        fighters[k][0]
                    ))

    result = [str(len(answer))]
    for a, b, c in answer:
        result.append(f"{a} {b} {c}")

    return "\n".join(result)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample1 = """\
5
TheStrong 90 60 10
TheInvincible 10000 10000 10000
TheTough 70 50 25
TheBrick 3 1 4159
TheResilient 160 40 10
"""

assert run(sample1) == """\
1
TheStrong TheTough TheResilient
""", "sample 1"

assert run("""\
1
TheLonely 500 500 500
""") == """\
0
""", "sample 2"

assert run("""\
3
A 10 10 10
B 10 10 10
C 10 10 10
""") == """\
0
""", "all equal values"

assert run("""\
2
A 4 6 1
B 10 3 1
""") == """\
0
""", "simultaneous death must be a draw"

assert run("""\
3
A 6 6 1
B 10 3 1
C 100 1 100
""") == """\
0
""", "boundary and no-damage cases"

max_input = ["100"]
for i in range(100):
    max_input.append(f"F{i} 10000 10000 10000")

assert run("\n".join(max_input) + "\n") == """\
0
""", "maximum N with all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / TheLonely 500 500 500` | `0` | Minimum-size input with no possible triple |
| Three identical fighters | `0` | All fights are draws because every attack is absorbed by defence |
| `A 4 6 1`, `B 10 3 1` | `0` | Both fighters die in the same round, so equality must not count as a win |
| Three fighters including a fighter with defence 100 against attack 1 | `0` | Zero-damage fights and boundary arithmetic |
| 100 identical fighters | `0` | Maximum N and O(N^3) enumeration under the actual constraints |

The sample test uses the deterministic order produced by `i < j < k`. Since the problem accepts arbitrary ordering, a different valid implementation could print the same triple in another order.

## Edge Cases

The zero-damage case is handled before the ceiling division. Consider a fight where A cannot damage B because `AT_A <= DF_B`. Then `damage_to_b` is zero, so B's health never decreases. The algorithm immediately records `win[A][B] = False`. For example, with `A 100 10 100` and `B 100 10 100`, both damage values are zero, so the fight is a draw. The algorithm never attempts an infinite simulation.

The simultaneous-death case is handled by the strict `<` comparison. With

```
2
A 4 6 1
B 10 3 1
```

A deals `6 - 1 = 5` damage to B, while B deals `3 - 1 = 2` damage to A. B reaches zero after `ceil(10 / 5) = 2` rounds. A has taken `2 * 2 = 4` damage, exactly its starting health. Since `4 < 4` is false, `win[A][B]` remains false. The reverse direction is also false, so the result is correctly treated as a draw.

The exact-final-round boundary is the same comparison from the other side. If A had 5 HP instead of 4 in that example, A would have `5 - 4 = 1` HP after B died, so `4 < 5` would be true and A would win. Changing one HP changes the result exactly where the game rules say it should.

A fighter that takes no damage from an opponent is also handled correctly. Suppose A has defence 100 and B has attack 1. Then A's incoming damage is `max(0, 1 - 100) = 0`. A can survive indefinitely, but that alone does not mean A wins. The algorithm separately checks whether A can eventually kill B. If A also deals zero damage, the result is a draw. If A deals positive damage, B eventually dies while A remains alive, so A wins.

Finally, triples are checked in both orientations. Suppose the results are `A beats B`, `B beats C`, and `C beats A`. If the indices happen to be ordered as A, C, B, the first cycle expression would not match that index order, but the reverse expression does. Checking both directions makes the result independent of the input ordering of the fighters. Because every triple is still generated only once with `i < j < k`, this does not introduce duplicate output.
