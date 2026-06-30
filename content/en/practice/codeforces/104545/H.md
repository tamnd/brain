---
title: "CF 104545H - Hero Morethor"
description: "We are simulating a sequential combat process involving a hero and a list of monsters. The hero starts with an initial power value, and then encounters monsters one by one in a fixed order. Each monster has a strength value."
date: "2026-06-30T08:58:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104545
codeforces_index: "H"
codeforces_contest_name: "VIII MaratonUSP Freshman Contest"
rating: 0
weight: 104545
solve_time_s: 57
verified: true
draft: false
---

[CF 104545H - Hero Morethor](https://codeforces.com/problemset/problem/104545/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a sequential combat process involving a hero and a list of monsters. The hero starts with an initial power value, and then encounters monsters one by one in a fixed order. Each monster has a strength value. When the hero meets a monster, he can defeat it only if his current power is at least the monster’s strength. If he wins, his power increases by exactly that monster’s strength. If he ever meets a monster he cannot defeat, the process stops immediately.

The task is to determine whether the hero can successfully defeat every monster in the given sequence, starting from his initial power.

The input size allows up to 100,000 monsters. This immediately suggests that any approach involving nested loops or repeated scanning of the list multiple times would be too slow. A single linear pass over the monsters is necessary, since O(N²) operations would be far beyond acceptable limits.

A subtle edge case arises when there are no monsters at all. In that case, the hero trivially succeeds regardless of his initial power. Another corner case appears when the hero’s initial power is zero. If the first monster has positive strength, the hero cannot proceed at all, and the answer becomes negative unless the first monster also has zero strength. This zero-strength interaction matters because it does not break the monotonic accumulation behavior, but it can affect early termination decisions.

## Approaches

The brute-force interpretation is already very close to the actual simulation. We iterate through the monsters in order, checking at each step whether the current hero power is sufficient. If it is, we add the monster’s strength to the hero’s power and continue. If not, we immediately conclude failure.

This direct simulation is correct because the rules explicitly define a deterministic process with no choices or alternative strategies. There is no way to reorder fights or skip monsters, so the state evolution is fixed.

The naive concern would be whether we need to reconsider earlier decisions or attempt backtracking if the hero fails later. That intuition does not apply here because once the hero defeats a monster, his power only increases. There is no mechanism that reduces power or introduces branching states. As a result, the simulation is already optimal.

The only meaningful optimization insight is recognizing that no sorting, greedy rearrangement, or preprocessing is required. The input order is fixed and must be followed exactly, so the solution is purely linear accumulation with a conditional check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) | O(1) | Accepted |
| Optimal Linear Scan | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of monsters N and the initial hero power H. This defines the starting state of the simulation before any interactions occur.
2. Iterate through each monster strength in the given order. The order is essential because the hero cannot choose which monster to fight first.
3. For each monster, compare its strength with the current hero power. If the hero’s power is strictly less than the monster’s strength, terminate immediately and output failure.
4. If the hero can defeat the monster, increase his power by adding the monster’s strength. This models the rule that defeating a monster permanently strengthens the hero.
5. Continue this process until either all monsters are processed or a failure occurs.
6. If the loop completes without failure, output success.

### Why it works

The key invariant is that after processing the i-th monster successfully, the hero’s power is exactly equal to the initial power plus the sum of strengths of all defeated monsters up to that point. Since every successful fight strictly preserves all previous power gains and only adds positive values, the hero’s power is monotonically non-decreasing. This guarantees that once a monster is defeatable at its turn, there is no earlier hidden condition that could invalidate future comparisons. The simulation therefore exactly mirrors the problem’s definition, and any failure encountered is the earliest possible failure point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, h = map(int, input().split())
    if n == 0:
        print("SIM")
        return

    monsters = list(map(int, input().split()))

    for f in monsters:
        if h < f:
            print("NAO")
            return
        h += f

    print("SIM")

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the step-by-step simulation. The check `if n == 0` handles the empty sequence explicitly, since no comparisons are needed and the hero trivially succeeds.

Inside the loop, the comparison `h < f` captures the defeat condition. If it triggers, we immediately stop processing because later monsters are irrelevant once failure occurs. Otherwise, we accumulate the monster’s strength into `h`, which models the permanent power gain.

There is no need for additional data structures because the state depends only on the current power value.

## Worked Examples

### Example 1

Input:

```
5 10
1 2 3 4 5
```

| Step | Hero Power (before) | Monster | Can Defeat | Hero Power (after) |
| --- | --- | --- | --- | --- |
| 1 | 10 | 1 | Yes | 11 |
| 2 | 11 | 2 | Yes | 13 |
| 3 | 13 | 3 | Yes | 16 |
| 4 | 16 | 4 | Yes | 20 |
| 5 | 20 | 5 | Yes | 25 |

The hero always maintains enough power because each monster is weaker than or equal to the accumulated growth from previous fights. This confirms the monotonic growth property.

Output:

```
SIM
```

### Example 2

Input:

```
4 7
1 1 1 11
```

| Step | Hero Power (before) | Monster | Can Defeat | Hero Power (after) |
| --- | --- | --- | --- | --- |
| 1 | 7 | 1 | Yes | 8 |
| 2 | 8 | 1 | Yes | 9 |
| 3 | 9 | 1 | Yes | 10 |
| 4 | 10 | 11 | No | stop |

The failure occurs exactly at the first impossible encounter. Since the process halts immediately, later monsters are irrelevant.

Output:

```
NAO
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each monster is processed exactly once with constant-time work |
| Space | O(1) | Only a single running variable stores the hero’s power |

The constraints allow up to 100,000 monsters, and a single linear scan easily fits within time limits. Memory usage is constant and independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return capture(solve)

def capture(func):
    import sys
    from io import StringIO
    backup = sys.stdout
    sys.stdout = StringIO()
    func()
    out = sys.stdout.getvalue()
    sys.stdout = backup
    return out.strip()

# provided samples
assert run("5 10\n1 2 3 4 5\n") == "SIM"
assert run("4 7\n1 1 1 11\n") == "NAO"

# edge: no monsters
assert run("0 5\n") == "SIM"

# edge: immediate failure
assert run("3 1\n2 1 1\n") == "NAO"

# edge: all zeros
assert run("5 0\n0 0 0 0 0\n") == "SIM"

# edge: large increasing
assert run("4 1\n1 2 4 8\n") == "SIM"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 5` | SIM | empty sequence handling |
| `3 1 / 2 1 1` | NAO | immediate failure at first monster |
| `5 0 / all zeros` | SIM | zero-strength accumulation stability |
| `4 1 / 1 2 4 8` | SIM | growing chain correctness |

## Edge Cases

One important edge case is when there are no monsters. The input is `0 H`. The algorithm reads `n = 0` and immediately outputs success without attempting to read or process the second line. This prevents unnecessary input parsing and avoids edge indexing errors.

Another case is when the hero starts with zero power. For input:

```
3 0
0 0 1
```

the simulation proceeds as follows. First monster is 0, so `h < f` is false and power stays 0. Second is also 0, still fine. At the third monster, `0 < 1` triggers failure. The algorithm correctly identifies the first impossible fight without skipping or reordering.

A third case is when all monsters are zero. For example:

```
4 0
0 0 0 0
```

every comparison passes since `h >= f` always holds. The hero’s power remains unchanged but the process never fails, producing success.
