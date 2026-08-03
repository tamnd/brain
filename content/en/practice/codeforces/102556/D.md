---
title: "CF 102556D - Riana and Distribution of Pie"
description: "Let the chosen percentage of the i-th person be Pi, written as a fraction between 0 and 1. When person i takes a turn, two things happen. They take Pi of the untouched pie, then they also take Pi of every slice already owned by previous people."
date: "2026-08-03T19:25:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102556
codeforces_index: "D"
codeforces_contest_name: "2020 Ateneo de Manila University DISCS PrO HS Division"
rating: 0
weight: 102556
solve_time_s: 150
verified: true
draft: false
---

[CF 102556D - Riana and Distribution of Pie](https://codeforces.com/problemset/problem/102556/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Let the chosen percentage of the `i`-th person be `P_i`, written as a fraction between `0` and `1`.

When person `i` takes a turn, two things happen. They take `P_i` of the untouched pie, then they also take `P_i` of every slice already owned by previous people. After every person has played, the untouched part of the pie must be zero, and we want the final slice sizes to be as equal as possible.

The input contains only the number of people. The output is the percentage chosen by each person, in order.

The only constraint is `N ≤ 1000`, so even an `O(N^2)` simulation would easily fit. The challenge is not efficiency, it is discovering the mathematical structure of the process.

The first non-obvious edge case is `N = 1`. The only valid answer is `100%`, because otherwise some pie remains uneaten.

The second subtle case is that making the last person choose `100%` is not required. For example, with `N = 2`, choosing `100%, 50%` leaves no untouched pie because the first player already consumed all of it. A greedy strategy that always forces the last player to take everything misses the optimal distribution.

The final trap is confusing the percentage a player chooses with the percentage they finally own. Later players repeatedly steal from earlier ones, so the chosen percentages and final shares are different quantities.

## Approaches

A direct simulation keeps every player's current slice. Whenever a new player arrives, every previous slice is multiplied by `(1 - P_i)`, the new player receives everything removed from those slices plus `P_i` of the untouched pie, and the untouched pie is also multiplied by `(1 - P_i)`. This faithfully models the game, but it does not tell us how to choose the percentages.

The key observation is that a player's gain from untouched pie and from stealing always adds up to the same value.

Suppose the untouched fraction before person `i` is `R`. The total amount already owned by previous players is `1 - R`. The new player receives

`P_i · R + P_i · (1 - R) = P_i`.

So immediately after their own turn, player `i` always owns exactly `P_i` of the original pie.

Afterward, every later player simply scales that slice by `(1 - P_j)`. Hence the final share is

$$F_i=P_i\prod_{j=i+1}^{N}(1-P_j).$$

Now define

$$S_i=\prod_{j=i}^{N}(1-P_j),$$

the untouched fraction just before person `i`.

Then

$$F_i=S_{i+1}-S_i.$$

The leftover pie is `S_1`, and the requirement of no leftovers means `S_1=0`. Also `S_{N+1}=1`.

Since the final shares sum to `1`, the smallest possible difference between the largest and smallest share is achieved when every final share is exactly `1/N`.

Setting every `F_i=1/N` gives

$$S_i=\frac{i-1}{N}.$$

Recovering the percentages,

$$P_i=\frac{S_{i+1}-S_i}{S_{i+1}}.$$

For `i=1`,

$$P_1=1.$$

For every `i≥2`,

$$P_i=\frac{1/N}{i/N}=\frac1i.$$

So the answer is remarkably simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation and search | Exponential | O(N) | Too slow |
| Closed-form formula | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `N`.
2. Print `100.0` for the first person. This guarantees the untouched pie immediately becomes zero, satisfying the no-leftovers condition.
3. For every person `i` from `2` to `N`, print `100 / i`. This is exactly the value obtained from the derived formula `P_i = 1/i`.

The derivation guarantees that every player's final share becomes exactly `1/N`, which is the best possible because all shares sum to one.

### Why it works

The invariant is that player `i` owns exactly `P_i` immediately after finishing their own turn. Every later turn simply multiplies every existing slice by the same factor. This gives the formula

$$F_i=P_i\prod_{j>i}(1-P_j).$$

Writing the suffix products as `S_i` converts the expression into

$$F_i=S_{i+1}-S_i.$$

Equal final shares uniquely determine every `S_i`, and those suffix products uniquely determine every percentage. Since equal shares make the maximum and minimum identical, no better distribution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    print(f"{100.0:.10f}")
    for i in range(2, n + 1):
        print(f"{100.0 / i:.10f}")

if __name__ == "__main__":
    solve()
```

The program directly prints the closed-form answer. The first value is always `100%`. Every later value is simply `100/i`. No simulation is required because the mathematical derivation already characterizes the unique optimal solution.

Floating point precision is more than sufficient here. The required error is `1e-4`, while printing ten decimal places keeps the accumulated error many orders of magnitude smaller.

## Worked Examples

### Example 1

Input:

```
1
```

| Person | Printed percentage |
| --- | --- |
| 1 | 100.0000000000 |

The only player takes the whole pie, so the final distribution is already perfectly equal.

### Example 2

Input:

```
4
```

| Person | Percentage printed |
| --- | --- |
| 1 | 100.0000000000 |
| 2 | 50.0000000000 |
| 3 | 33.3333333333 |
| 4 | 25.0000000000 |

The final shares become

| Person | Final share |
| --- | --- |
| 1 | 25% |
| 2 | 25% |
| 3 | 25% |
| 4 | 25% |

This confirms that every player finishes with exactly one quarter of the pie.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One value is printed for each person. |
| Space | O(1) | Only a loop variable is stored. |

With at most 1000 people, this runs comfortably within the limits.

## Test Cases

```python
import io
import sys

def solve():
    input = sys.stdin.readline
    n = int(input())
    print(f"{100.0:.10f}")
    for i in range(2, n + 1):
        print(f"{100.0 / i:.10f}")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue()

assert run("1\n") == "100.0000000000\n"

assert run("2\n") == (
    "100.0000000000\n"
    "50.0000000000\n"
)

assert run("3\n") == (
    "100.0000000000\n"
    "50.0000000000\n"
    "33.3333333333\n"
)

out = run("1000\n").splitlines()
assert len(out) == 1000
assert abs(float(out[-1]) - 0.1) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `100` | Minimum input size |
| `2` | `100`, `50` | First non-trivial case |
| `3` | `100`, `50`, `33.333...` | General formula |
| `1000` | Last value is `0.1` | Largest input size |

## Edge Cases

When `N = 1`, the algorithm prints only `100`. The untouched pie immediately becomes zero, and the only player owns the entire pie. Both requirements are satisfied.

When `N = 2`, the algorithm prints `100` and `50`. The first player initially owns the whole pie. The second player steals half of it, leaving both players with exactly `50%`. This demonstrates that the first player, not the last one, is the person who must choose `100%`.

For larger values such as `N = 3`, the algorithm prints `100`, `50`, and `33.333...`. The resulting final shares are all exactly `1/3`, confirming that the construction equalizes every player's final ownership while still leaving no untouched pie.
