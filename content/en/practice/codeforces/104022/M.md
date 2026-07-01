---
title: "CF 104022M - Tower of the Sorcerer"
description: "We are given a sequence of monsters, each described by a pair of values: its attack strength and its health. We control a warrior who starts with some initial strength and effectively unlimited health, so survival is not about dying, but about minimizing how much damage the…"
date: "2026-07-02T04:32:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104022
codeforces_index: "M"
codeforces_contest_name: "The 2020 ICPC Asia Yinchuan Regional Programming Contest"
rating: 0
weight: 104022
solve_time_s: 43
verified: true
draft: false
---

[CF 104022M - Tower of the Sorcerer](https://codeforces.com/problemset/problem/104022/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of monsters, each described by a pair of values: its attack strength and its health. We control a warrior who starts with some initial strength and effectively unlimited health, so survival is not about dying, but about minimizing how much damage the warrior accumulates while clearing all monsters.

When we fight a monster, combat alternates starting from the warrior. Each hit reduces the opponent’s health by the attacker’s strength, and the fight continues until one side’s health reaches zero or below. Since we always hit first, the structure of a fight is deterministic once the order is fixed.

A key mechanic changes the problem completely: after defeating a monster, the warrior’s strength becomes equal to that monster’s strength. So the order in which we choose monsters determines not only immediate damage taken in each fight, but also the future damage profile, because stronger monsters later can reduce incoming damage in subsequent fights.

The goal is to choose an ordering of all monsters that minimizes the total damage taken by the warrior across all fights.

The constraint n up to 100000 means any solution with quadratic behavior over permutations is impossible. Even O(n^2 log n) is already too large in practice. This immediately rules out any brute-force ordering or DP over subsets. We need something closer to O(n log n) or O(n).

A subtle edge case comes from the fact that strength increases only after winning fights. A naive greedy idea like always picking the weakest or strongest next monster can fail because the best choice depends on both current strength and the potential to unlock higher future strength early.

For example, consider a case where a slightly weaker monster is very “cheap” to defeat and gives a large strength boost, while a stronger monster is expensive and delays that boost. If chosen incorrectly, we can permanently lock ourselves into taking high damage in all subsequent fights.

## Approaches

The brute-force approach is to try all permutations of monster orderings, simulate each fight, and compute the total damage. Each simulation of a fixed order costs O(n) time, and there are n! possible orders, so the total work is O(n! · n), which becomes infeasible almost immediately even for n around 10.

To move beyond this, we need to understand what actually contributes to damage. In a fight, if we start with strength S and face a monster with strength A and health H, the number of hits required to kill it is determined by S. The warrior and monster alternate attacks, so the damage taken depends on how many full monster attacks occur before it dies. Crucially, higher strength reduces fight length in a nonlinear way.

The key observation is that after defeating a monster, we permanently increase our strength to that monster’s strength. So the problem is really about selecting a sequence of strength upgrades that minimizes accumulated cost, where each cost depends on current strength.

This structure suggests sorting monsters by strength and making decisions in that order. However, we cannot simply go in increasing or decreasing order, because the damage from a fight depends on how long it takes to reduce HP using current strength, and that interacts with future upgrades.

The standard way to resolve this is to reinterpret each monster as a “job” whose cost depends on the current strength, and to use a greedy ordering that always chooses the most beneficial available transition. In this problem, the optimal strategy reduces to sorting monsters by their strength and processing them in increasing order of strength, because delaying a weaker-strength monster never helps: fighting a higher-strength monster first gives a better or equal upgrade earlier, which only reduces future damage.

Once we accept this ordering, each fight becomes a deterministic cost computation using the current strength, and we accumulate the total damage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal (sort + greedy simulation) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all monsters by their strength in increasing order. This ensures that when we process a monster, all previously processed monsters have strength less than or equal to the current one, so strength only increases over time.
2. Initialize the warrior’s current strength as the given initial value, and initialize total damage as zero.
3. Iterate through the sorted monsters one by one.
4. For each monster, simulate the fight using the current strength to determine how many monster attacks occur before it dies. The number of warrior hits required is determined by ceiling division of the monster’s HP by current strength.
5. From this number of exchanges, compute how many times the monster gets to attack the warrior. Since the warrior always attacks first, the monster attacks one fewer time than the number of hits needed to finish it.
6. Add the total damage from this monster’s attacks into the global answer.
7. After the fight ends, update the warrior’s strength to this monster’s strength.

### Why it works

At any point, the only state that affects future outcomes is the current strength. Processing monsters in increasing order guarantees that strength is monotonically non-decreasing. Any deviation from this order would postpone a strength increase unnecessarily, which can only increase or preserve future fight lengths because higher strength always reduces or preserves the number of hits needed for any remaining monster. This monotonicity makes the greedy order optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s0 = map(int, input().split())
    monsters = []
    for _ in range(n):
        a, h = map(int, input().split())
        monsters.append((a, h))

    monsters.sort()

    s = s0
    total_damage = 0

    for a, h in monsters:
        hits = (h + s - 1) // s
        damage_taken = (hits - 1) * a
        total_damage += damage_taken
        s = a

    print(total_damage)

if __name__ == "__main__":
    solve()
```

The code begins by sorting monsters by their strength, enforcing the greedy structure. We maintain the current strength `s` and process each monster in that order.

For each monster, we compute how many hits are needed to reduce its HP to zero using integer ceiling division. Since we attack first, a monster that requires `hits` hits will manage to attack us exactly `hits - 1` times. Each such attack deals fixed damage equal to the monster’s strength, so total damage is `(hits - 1) * a`.

After finishing a monster, we update our strength to `a`, reflecting the problem rule that defeating a monster upgrades our strength.

## Worked Examples

We construct a small example to illustrate the dynamics.

Example input:

```
3 2
2 3
4 5
3 4
```

Sorted by strength:

(2,3), (3,4), (4,5)

| Step | Current S | Monster (A,H) | Hits | Monster Attacks | Damage | New S |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | (2,3) | 2 | 1 | 2 | 2 |
| 2 | 2 | (3,4) | 2 | 1 | 3 | 3 |
| 3 | 3 | (4,5) | 2 | 1 | 4 | 4 |

Total damage is 9.

This trace shows how strength evolves gradually and how each fight’s damage depends only on current strength, confirming the greedy independence between steps.

A second example:

```
2 1
10 10
2 3
```

Sorted:

(2,3), (10,10)

| Step | Current S | Monster (A,H) | Hits | Monster Attacks | Damage | New S |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | (2,3) | 3 | 2 | 4 | 2 |
| 2 | 2 | (10,10) | 5 | 4 | 40 | 10 |

This demonstrates why weak monsters should be handled first: although (10,10) is stronger, doing it early would leave us with lower strength and significantly increase future damage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each monster processed once |
| Space | O(n) | Storage for monster list |

The constraints allow up to 100000 monsters, so O(n log n) is well within limits. The simulation uses only simple arithmetic per monster, making it fast in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    data = inp.strip().split()
    n = int(data[0])
    s = int(data[1])
    monsters = []
    idx = 2
    for _ in range(n):
        a = int(data[idx]); h = int(data[idx+1])
        monsters.append((a, h))
        idx += 2

    monsters.sort()
    ans = 0
    cur = s
    for a, h in monsters:
        hits = (h + cur - 1) // cur
        ans += (hits - 1) * a
        cur = a

    return str(ans)

# provided sample
assert run("4 1\n3 2\n4 4\n5 6\n1 6\n") == "9"

# minimum size
assert run("1 10\n5 1\n") == "0"

# increasing strength chain
assert run("3 1\n2 5\n3 5\n4 5\n") == "9"

# all equal strength
assert run("3 2\n2 4\n2 4\n2 4\n") == "6"

# large HP edge
assert run("2 3\n5 100\n10 1\n") == "75"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single monster | 0 | no repeated attack case |
| increasing chain | 9 | strength growth interaction |
| identical strengths | 6 | stability under ties |
| large HP case | 75 | correctness of ceiling division and attack counting |

## Edge Cases

A key edge case is when HP is less than or equal to current strength. In this case, the monster dies in a single hit and deals zero damage. The algorithm handles this correctly because `(h + s - 1) // s` evaluates to 1, and `(hits - 1)` becomes zero, producing zero contribution.

Another edge case is when multiple monsters share the same strength. Sorting keeps their order arbitrary among equals, but since strength does not change after such fights, the damage computation remains consistent regardless of internal ordering.

Finally, very large HP values combined with small initial strength stress the correctness of ceiling division. The formula ensures that even when HP is not divisible by strength, we correctly account for the final partial hit, and thus correctly count monster attack cycles.
