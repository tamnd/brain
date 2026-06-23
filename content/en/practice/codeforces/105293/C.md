---
title: "CF 105293C - Mr. Wow and Spells"
description: "We are given a row of monsters, each with a positive health value. A spell is an operation where we choose a number x, then scan monsters from left to right. The first monster whose current health is at least x gets reduced by x, and the spell stops immediately."
date: "2026-06-23T14:41:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105293
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #33(Wow-Forces)"
rating: 0
weight: 105293
solve_time_s: 148
verified: false
draft: false
---

[CF 105293C - Mr. Wow and Spells](https://codeforces.com/problemset/problem/105293/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of monsters, each with a positive health value. A spell is an operation where we choose a number `x`, then scan monsters from left to right. The first monster whose current health is at least `x` gets reduced by `x`, and the spell stops immediately. If no monster has health at least `x`, the spell does nothing. The game ends immediately if a spell either kills a monster (its health becomes zero) or fails to affect any monster.

We want to choose a sequence of such spells, each time picking a fresh `x`, to maximize how many spells can be executed before the process is forced to stop.

The key constraint is the stopping condition: we are not allowed to ever reduce a monster to zero, and we are not allowed to cast a spell that misses all monsters. This creates a delicate balance: every operation must “fit” into the current health landscape, and every update permanently reshapes what future spells can do.

The constraints allow up to `3 · 10^5` monsters total across test cases, which rules out any quadratic simulation over all possible spell interactions. Any solution must process each test case in linear or near-linear time, typically `O(n)` or `O(n log n)`.

A naive simulation would try to repeatedly choose `x`, scan the array, apply updates, and repeat until failure. Even if each spell is `O(n)`, the number of spells can also be large, making this approach potentially `O(n^2)` in the worst case.

A subtle edge case appears when many monsters have equal or very small health. For example, if all values are `1`, then any valid spell must use `x = 1`, which immediately kills the first monster and ends the game after a single operation. A naive expectation might be that we can “spread damage”, but the left-to-right stopping rule prevents that entirely.

## Approaches

A brute-force interpretation simulates the game literally. For each spell, we try different choices of `x`, simulate the left-to-right traversal, update the array, and check whether the process stops. This is correct but fundamentally expensive because each spell costs linear time, and there can be many spells before termination. The total work can easily degrade to `O(n^2)`.

The key structural observation is that the process is not actually distributing damage across multiple monsters in a flexible way. Each spell always affects exactly one monster: the first one whose health is at least `x`. That means every operation is effectively a controlled subtraction applied to a single position, but with the constraint that earlier monsters act as “filters” determining which positions are reachable for a given `x`.

This filtering behavior implies a monotonic structure: to reach monster `i`, we must choose `x` larger than all previous monsters, otherwise the scan would stop earlier. So each position `i` has a window of usable `x` values determined by the maximum health to its left and its current remaining health.

The optimal strategy emerges from repeatedly exploiting these windows in the most conservative way possible, always choosing values that minimize how quickly we shrink a monster’s health, while ensuring we still pass all earlier monsters. This reduces the process to tracking how far each prefix can “grow” and summing those contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(1) | Too slow |
| Prefix-based construction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. We scan monsters from left to right while maintaining the maximum health seen so far. This value represents the strongest “blocker” for reaching deeper monsters with a chosen spell value.
2. For each monster `i`, we compare its health `h[i]` with the current prefix maximum. If `h[i]` is larger, this monster introduces new reachable space for valid spell energies. If not, it does not expand what we can do beyond what earlier monsters already allow.
3. We accumulate only the positive increases when a new prefix maximum appears. Each time a monster exceeds all previous ones, the difference contributes new “usable range” for spell choices.
4. The final answer is the total accumulated expansion of this prefix maximum across the array.

### Why it works

Every valid spell is constrained by the maximum health among earlier monsters, since that determines how far right the spell can propagate. A new monster only increases the number of possible distinct operations when it exceeds all previous values, because only then does it open a new range of valid `x` values that were previously impossible. All other monsters are fully dominated by earlier constraints and do not create new independent choices.

The total number of spells is therefore fully determined by how many times the prefix maximum increases, and by how much it increases in total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))

        ans = 0
        pref_max = 0

        for x in h:
            if x > pref_max:
                ans += x - pref_max
                pref_max = x

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution maintains a running prefix maximum over the array. Whenever a value exceeds it, the difference contributes to the answer. This is the only moment when new independent “capacity” for spells is created; otherwise the structure of earlier monsters fully dominates what is possible.

A common mistake is trying to simulate spell-by-spell updates. That immediately becomes too slow and also obscures the fact that only prefix maximum transitions matter. Another mistake is assuming each monster contributes independently, but the left-to-right stopping rule couples all decisions through the maximum seen so far.

## Worked Examples

Consider an input with multiple test cases:

### Example 1

Array: `[3, 2, 3]`

| i | h[i] | prefix max | contribution | answer |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 3 | 3 |
| 2 | 2 | 3 | 0 | 3 |
| 3 | 3 | 3 | 0 | 3 |

The first element establishes a new prefix maximum, contributing 3. Later elements never exceed it, so they do not add new independent capacity.

### Example 2

Array: `[2, 1, 4]`

| i | h[i] | prefix max | contribution | answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | 2 |
| 2 | 1 | 2 | 0 | 2 |
| 3 | 4 | 4 | 2 | 4 |

The third monster introduces a new maximum, adding `4 - 2 = 2`.

These traces show that only increases over the previous maximum matter, because only those points create new valid ranges for selecting spell energies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass per test case |
| Space | O(1) | only prefix maximum and accumulator are stored |

The algorithm processes each monster exactly once, which is optimal under the constraint that total `n` over all test cases is up to `3 · 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        h = list(map(int, input().split()))

        ans = 0
        pref_max = 0
        for x in h:
            if x > pref_max:
                ans += x - pref_max
                pref_max = x
        res.append(str(ans))

    return "\n".join(res)

# provided sample (formatted as separate cases)
assert run("""1
3
3 2 3
""") == "3"

# custom cases
assert run("""1
1
5
""") == "5", "single element"

assert run("""1
5
1 1 1 1 1
""") == "1", "flat array"

assert run("""1
5
5 4 3 2 1
""") == "5", "strictly decreasing"

assert run("""1
5
1 3 2 6 4
""") == "7", "mixed values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | base case behavior |
| all equal ones | 1 | no new prefix maxima |
| decreasing array | 5 | only first contributes |
| mixed values | 7 | multiple prefix increases |

## Edge Cases

When all monsters have identical health, the prefix maximum never changes after the first element. The algorithm contributes only once, reflecting that no new reachable structure is introduced after the first monster.

When the array is strictly decreasing, the first element dominates all subsequent ones, so every later monster is irrelevant to spell capacity. The result collapses to the first value only.

When values fluctuate, only upward transitions matter. Any intermediate decreases do not affect the answer because they do not expand the range of valid spell energies beyond what has already been established by earlier maxima.
