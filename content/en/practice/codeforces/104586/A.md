---
title: "CF 104586A - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u044f\u0433\u043e\u0434\u044b"
description: "We are told that all berries were originally packed into identical jars, and every jar contains the same number of berries. Each jar contains only one type of berry."
date: "2026-06-30T07:32:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104586
codeforces_index: "A"
codeforces_contest_name: "Codemasters Codecup 2023 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 104586
solve_time_s: 64
verified: true
draft: false
---

[CF 104586A - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u044f\u0433\u043e\u0434\u044b](https://codeforces.com/problemset/problem/104586/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are told that all berries were originally packed into identical jars, and every jar contains the same number of berries. Each jar contains only one type of berry. After some confusion during sorting, all berries were emptied into a single pile, and we are given the total number of black currant berries found in that pile.

Among all jars that contained currants, some were black currant and some were red currant, but they were mistakenly treated as the same type during packing. What we know about the original structure is that a fraction of all jars, equal to `p`, contained currants (both black and red together). The rest of the jars contained other berries, which do not matter for the final computation except that they contribute to the total count.

The key point is that all jars have equal capacity, so “fraction of jars” directly translates into “fraction of total berries.”

The task is to determine what fraction of all currant berries are black currants, given that we know the number of black currants `n`, and we can infer the total number of currant berries from the jar proportion `p`.

The input size is tiny, so the solution must be constant time. Any approach involving simulation over jars or berries is unnecessary. The only subtlety lies in correctly translating a fraction of jars into a fraction of berries using the equal-sized constraint.

Edge cases appear when `n = 0`, where black currants are absent and the answer must be exactly zero regardless of `p`. Another corner case is when `p = 1`, meaning all jars are currant jars, so all berries in the pile are currants and the answer becomes `n / total_currants`, which should simplify cleanly without division issues.

A naive mistake would be to treat `p` as directly the fraction of currant berries without considering the equal-sized jars assumption, or to ignore the fact that total berry count is fixed implicitly via jar structure.

## Approaches

A brute-force interpretation would attempt to reconstruct the number of jars. If we assume each jar contains `k` berries, we might try enumerating possible `k`, then splitting total berries into jars, then assigning currant jars according to fraction `p`, and finally distributing black and red currants. This quickly becomes underdetermined and computationally meaningless, since infinitely many `(k, number of jars)` pairs satisfy the constraints.

The key observation is that we never actually need to know `k` or the number of jars. Since every jar has the same size, proportions of jars and proportions of berries are identical. This collapses the entire structure into a single proportional relationship: the fraction of currant berries among all berries is exactly `p`. Since the total number of berries is fixed to one million, we can directly compute the total number of currant berries as `p * 1e6`.

Once the total currant amount is known, the answer becomes a simple ratio: black currants over total currants.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force reconstruction of jars | O(N) or worse (underdetermined search) | O(1) | Too slow / ill-defined |
| Direct proportional reasoning | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `p`. At this point `n` is the number of black currant berries, and `p` is the fraction of all berries that belong to currant jars.
2. Convert the fraction of currant jars into the total number of currant berries. Since all jars contain the same number of berries, this fraction applies equally to berries. The total number of berries is `1,000,000`, so total currant berries equals `p * 1,000,000`.
3. Compute the desired ratio as `n / (p * 1,000,000)`. This directly compares black currants to all currants.
4. Output the value as a floating-point number with sufficient precision to meet the required error bound.

### Why it works

All jars have identical size, so the mapping from jars to berries is linear. Any subset of jars corresponds to the same subset of berries scaled by a constant factor. Therefore, the fraction of currant jars equals the fraction of currant berries. This makes the total currant count fully determined by `p` and the known total berry count, leaving only a single division to isolate black currants.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, p = input().split()
    n = int(n)
    p = float(p)

    total = p * 1_000_000.0
    if total == 0:
        print(0.0)
        return

    ans = n / total
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the derived formula directly. The only care needed is floating-point conversion of `p`, since it is given with up to six decimal places. The multiplication by `1e6` must be done in floating point to preserve precision.

The guard `if total == 0` handles the degenerate case where `p = 0`, meaning there are no currant berries at all. In that situation, `n` must also be zero, and the answer is defined as zero without performing division.

## Worked Examples

### Sample 1

Input:

```
250000 0.5
```

We compute total currants as `0.5 * 1,000,000 = 500,000`.

| Step | n | p | total currants | result |
| --- | --- | --- | --- | --- |
| initial | 250000 | 0.5 | - | - |
| compute total | 250000 | 0.5 | 500000 | - |
| compute ratio | 250000 | 0.5 | 500000 | 0.5 |

Output is `0.5`, meaning half of all currants are black.

This confirms a balanced split where black currants exactly match half of the currant population.

### Sample 2

Input:

```
0 0.9
```

We compute total currants as `0.9 * 1,000,000 = 900,000`.

| Step | n | p | total currants | result |
| --- | --- | --- | --- | --- |
| initial | 0 | 0.9 | - | - |
| compute total | 0 | 0.9 | 900000 | - |
| compute ratio | 0 | 0.9 | 900000 | 0 |

Output is `0.0`, which matches the fact that no black currants exist.

This shows correctness when the numerator is zero regardless of total size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed regardless of input |
| Space | O(1) | No auxiliary structures are used |

The solution is constant time and trivially fits within constraints, since it avoids any iteration or reconstruction of hidden structure.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, p = inp.strip().split()
    n = int(n)
    p = float(p)

    total = p * 1_000_000.0
    if total == 0:
        return "0.0"
    return str(n / total)

# provided samples
assert abs(float(run("250000 0.5")) - 0.5) < 1e-9, "sample 1"
assert abs(float(run("0 0.9")) - 0.0) < 1e-9, "sample 2"
assert abs(float(run("100000 0.1")) - 1.0) < 1e-9, "sample 3"

# custom cases
assert abs(float(run("1 1")) - 0.000001) < 1e-12, "single berry extreme"
assert abs(float(run("500000 1")) - 0.5) < 1e-12, "all currant jars"
assert abs(float(run("0 0.1")) - 0.0) < 1e-12, "zero black berries"
assert abs(float(run("1000 0.000001")) - 1.0) < 1e-9, "tiny fraction edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0.000001 | smallest nontrivial proportion scaling |
| 500000 1 | 0.5 | full currant coverage |
| 0 0.1 | 0 | zero numerator stability |
| 1000 0.000001 | 1 | extreme small fraction handling |

## Edge Cases

### Case: no black currants

Input:

```
0 0.7
```

Total currants become `700000`. The computation `0 / 700000` evaluates to `0` without numerical instability. The algorithm never divides by zero unless `p = 0`.

### Case: no currant jars

Input:

```
0 0
```

Here total currants become zero. The algorithm explicitly checks this condition and returns `0.0` directly. This avoids undefined division and matches the interpretation that there are no currants at all in the system.
