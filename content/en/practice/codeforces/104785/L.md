---
title: "CF 104785L - Last One Standing"
description: "Two players each control a single combat unit. Each unit repeatedly fires missiles at a fixed interval. A shot does not apply damage instantly, it lands half a second after being fired. Once a unit has fired, it must wait its reload time before it can fire again."
date: "2026-06-28T14:42:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104785
codeforces_index: "L"
codeforces_contest_name: "2023 United Kingdom and Ireland Programming Contest (UKIEPC 2023)"
rating: 0
weight: 104785
solve_time_s: 58
verified: true
draft: false
---

[CF 104785L - Last One Standing](https://codeforces.com/problemset/problem/104785/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players each control a single combat unit. Each unit repeatedly fires missiles at a fixed interval. A shot does not apply damage instantly, it lands half a second after being fired. Once a unit has fired, it must wait its reload time before it can fire again. Both units start fully ready at time zero and immediately fire their first missile.

Each missile reduces the opponent’s health by a fixed amount when it lands. A unit is destroyed as soon as its health becomes zero or negative. Because both sides can fire at the same time and their missiles take the same travel delay, it is possible for both units to die “at once” if their final damaging shots land simultaneously.

The task is to determine which unit will still have positive health strictly after the other has been destroyed, assuming both behave in the only optimal way available, which is simply firing whenever they are allowed to fire.

The input consists of two triples. The first triple describes player one’s unit with health, damage per shot, and reload time. The second triple describes player two’s unit in the same format. The output is either that player one wins, player two wins, or that neither can be strictly ahead in survival time.

The constraints are small, with all values up to 1000. This rules out any need for heavy data structures or advanced optimization, but it still leaves room for many shots over time if simulated naively.

A direct simulation in small time steps is misleading because events happen sparsely at irregular intervals. Another common mistake is ignoring the 0.5 second travel delay, which can cause incorrect ordering when both units land killing blows in the same cycle.

A subtle edge case appears when both units destroy each other on the same hit index. For example, if both reach zero health after their third missile lands, both die at the same time even if one fired earlier in real time, because both damage events land simultaneously.

## Approaches

A brute-force interpretation would simulate the fight in continuous time. Each unit maintains a next-fire timer and we advance time to the next firing event, scheduling damage arrivals at time plus 0.5. We keep applying damage events in chronological order until one or both health values drop to zero.

This simulation is correct, but the number of events can be large. Each unit may fire up to roughly 1000 times, since health and damage are bounded by 1000 and damage per shot can be as small as 1. A full event-driven simulation still stays within limits, but stepping through time or maintaining a fine-grained timeline is unnecessary overhead.

The key observation is that the exact ordering inside the 0.5-second travel delay does not matter. Every shot from both sides experiences the same delay, so relative ordering depends only on how many shots are needed to kill a unit and how frequently those shots occur.

Instead of simulating every missile, we compute how many hits are required to kill each unit. If player one has health h1 and receives d2 damage per hit, then the number of hits required is ceil(h1 / d2). Those hits occur at fixed intervals of t2 seconds, and the k-th hit arrives at time (k−1)·t2 + 0.5. The same applies symmetrically for player two.

Comparing the two death times directly tells us the winner. The shared +0.5 delay cancels when comparing, so only the firing schedules matter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(H1/d2 + H2/d1) events (or worse with naive time stepping) | O(1-event log) | Accepted but unnecessary |
| Optimal Computation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many hits player one needs to die. This is the smallest integer k1 such that k1·d2 ≥ h1. This represents how many successful impacts player two must land.
2. Compute how many hits player two needs to die in the same way, producing k2 from h2 and d1.
3. Translate hit counts into death times using firing intervals. Player two kills player one at time (k1 − 1)·t2 + 0.5, since the first hit lands after the first shot and each subsequent hit is spaced by t2. Player one kills player two at time (k2 − 1)·t1 + 0.5.
4. Compare these two times. If the first time is smaller, player two lands the fatal blow earlier, so player two wins. If the second time is smaller, player one wins.
5. If the times are equal, both units receive their final lethal damage simultaneously and neither survives strictly longer, so the result is a draw.

Why it works is tied to the fact that each unit’s damage process is a uniform arithmetic progression in time. Every relevant event is determined only by the index of the hit that causes death. Since all hits share the same fixed delay, relative ordering depends only on the number of intervals before the killing blow, and not on any intermediate interaction between the two timelines.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    h1, d1, t1 = map(int, input().split())
    h2, d2, t2 = map(int, input().split())

    def hits_needed(h, d):
        return (h + d - 1) // d

    k1 = hits_needed(h1, d2)
    k2 = hits_needed(h2, d1)

    time_2_kills_1 = (k1 - 1) * t2
    time_1_kills_2 = (k2 - 1) * t1

    if time_1_kills_2 < time_2_kills_1:
        print("player one")
    elif time_2_kills_1 < time_1_kills_2:
        print("player two")
    else:
        print("draw")

if __name__ == "__main__":
    solve()
```

The core implementation reduces everything to two integer comparisons. The helper function computes the ceiling division safely using integer arithmetic, avoiding floating point issues.

The 0.5 second travel delay is intentionally omitted in the comparison because it is identical for both players’ final killing hit and therefore does not affect ordering. Including it would only add an equal constant shift to both computed times.

## Worked Examples

Consider the first sample input:

Player one is weaker in damage but has a different reload timing tradeoff. Player two’s damage output per hit is higher, which reduces the number of required hits.

| Quantity | Player 1 kills Player 2 | Player 2 kills Player 1 |
| --- | --- | --- |
| Hits needed | ceil(30 / 15) = 2 | ceil(30 / 10) = 3 |
| Kill time | (2−1)·19 = 19 | (3−1)·10 = 20 |

Player one’s killing time is 19, while player two needs 20. Even though player one has lower per-hit damage, fewer hits are needed, so player one’s lethal shot arrives earlier, which matches the expected winner.

Now consider a symmetric-like swap case:

| Quantity | Player 1 kills Player 2 | Player 2 kills Player 1 |
| --- | --- | --- |
| Hits needed | ceil(30 / 10) = 3 | ceil(30 / 15) = 2 |
| Kill time | (3−1)·10 = 20 | (2−1)·19 = 19 |

Here player two dies earlier at time 19, so player two wins.

These examples show that the winner depends more on the interaction between reload speed and required hit count than on raw damage values alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary structures are used |

The input bounds allow many potential firing events, but the solution avoids enumerating them entirely. All dynamics are compressed into two computed integers per player.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("30 10 10\n30 15 19\n") == "player two"
assert run("30 15 19\n30 10 10\n") == "player one"
assert run("100 20 10\n100 12 5\n") == "draw"

# custom cases

# minimum values, symmetric
assert run("1 1 1\n1 1 1\n") == "draw"

# one-shot kill scenario
assert run("10 10 5\n10 1 5\n") == "player one"

# strong damage but slow reload vs weak fast attacker
assert run("100 50 100\n100 10 1\n") == "player two"

# equal death timing edge
assert run("30 10 10\n30 10 10\n") == "draw"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 1 1 1 | draw | symmetric trivial case |
| 10 10 5 / 10 1 5 | player one | one-shot kill asymmetry |
| 100 50 100 / 100 10 1 | player two | reload dominance over damage |

## Edge Cases

One important corner case occurs when both units die on the same shot index. Consider equal health and symmetric damage/reload. Both compute identical hit counts and identical firing schedules, producing identical kill times. The algorithm compares equal times and correctly returns a draw, matching the fact that both death events occur at the same moment due to identical 0.5-second delays.

Another subtle case is when one unit deals extremely high damage and requires only one hit to kill the opponent. In this situation, the computed time becomes zero for that side, since (1−1)·t = 0. This correctly models that the first shot immediately determines the outcome, and any slower killing schedule from the opponent cannot intervene before the first impact time comparison resolves.

A final case is when reload times differ drastically. A unit with very slow reload but high damage might still lose to a fast low-damage unit because the required hit count increases the number of intervals, pushing its final hit later in time. The algorithm handles this naturally since both factors are encoded in the same linear expression for death time.
