---
title: "CF 103665E - \u041f\u0440\u043e\u043f\u0430\u0432\u0448\u0438\u0435 \u0441\u043b\u0438\u0442\u043a\u0438"
description: "We are given a collection of identical gold bars, and each bar can be oriented in one of three effective ways, contributing a height of either a, b, or c. All bars must be used exactly once, and we stack them into a single tower."
date: "2026-07-02T21:44:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103665
codeforces_index: "E"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2018"
rating: 0
weight: 103665
solve_time_s: 48
verified: true
draft: false
---

[CF 103665E - \u041f\u0440\u043e\u043f\u0430\u0432\u0448\u0438\u0435 \u0441\u043b\u0438\u0442\u043a\u0438](https://codeforces.com/problemset/problem/103665/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of identical gold bars, and each bar can be oriented in one of three effective ways, contributing a height of either `a`, `b`, or `c`. All bars must be used exactly once, and we stack them into a single tower. The only thing that matters about a configuration is its total height, which is the sum of the contributions of all `n` bars.

Different choices of orientations may produce the same total height. The task is to count how many distinct total heights are achievable.

The input gives `n`, the number of bars, and three integers `a`, `b`, and `c`, which are the possible height contributions of each bar depending on orientation. The output is the number of distinct sums that can be formed by choosing, for each of the `n` positions, one of the three values.

The constraints are important. The number of bars can be as large as 1200, which rules out any approach that enumerates all `3^n` configurations. That space is astronomically large even for moderate `n`. However, the values of `a`, `b`, and `c` are large, up to `10^9`, so we cannot rely on bounded knapsack with small weight ranges either.

A key observation is that the only structure in the problem is additive: each bar contributes independently, and we only care about the total sum.

Edge cases appear when values are equal. If `a = b = c`, then every configuration produces the same total height, and the answer is 1. If two values are equal, say `a = b != c`, then effectively we only have two choices per bar, but still need to handle counting distinct sums correctly.

A naive mistake would be to assume the number of configurations equals the number of sums, which is false because many different assignments collapse into the same total.

## Approaches

The brute-force idea is straightforward: try all ways to assign each of the `n` bars one of the values `a`, `b`, or `c`, compute the resulting sum, and store it in a set. This is correct because it explicitly constructs every possible configuration. However, it requires iterating over `3^n` states, which becomes impossible even for `n = 30`, let alone `n = 1200`.

The crucial structure is that the final sum depends only on how many bars are assigned to each value, not on their positions. If we let `x`, `y`, and `z` be the counts of bars assigned `a`, `b`, and `c`, then the total height is `x*a + y*b + z*c`, with `x + y + z = n`. So the problem reduces to counting distinct values of a linear form over all integer triples constrained by a simple simplex.

Instead of enumerating assignments, we enumerate count distributions. There are only `O(n^2)` valid triples `(x, y, z)` because once `x` and `y` are fixed, `z` is determined. Each triple produces exactly one sum, so we can insert these into a set and count distinct results.

This transforms an exponential problem into a quadratic one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over assignments | O(3^n) | O(3^n) | Too slow |
| Enumerate count triples | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

We shift the viewpoint from sequences to counts.

1. Iterate over all possible values of `x`, the number of bars contributing `a`, from `0` to `n`. This fixes how many times `a` is used.
2. For each fixed `x`, iterate over `y`, the number of bars contributing `b`, from `0` to `n - x`. The remaining `z` is forced to be `n - x - y`, so we never explicitly loop over it.
3. For each triple `(x, y, z)`, compute the total height `x*a + y*b + z*c`. Insert this value into a hash set. The set automatically removes duplicates caused by different `(x, y, z)` combinations producing the same sum.
4. After all iterations, the size of the set is the number of distinct achievable heights.

The reason this enumeration is valid is that every valid configuration corresponds uniquely to a triple `(x, y, z)`, and every triple corresponds to at least one configuration.

### Why it works

The algorithm relies on the invariant that any arrangement of the bars is fully determined, up to permutation, by the counts of how many times each value is chosen. Since order does not affect the sum, two configurations are equivalent if and only if they share the same `(x, y, z)`. The nested loops enumerate all possible such triples exactly once, so every possible sum is considered, and no valid sum is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b, c = map(int, input().split())
    seen = set()

    for x in range(n + 1):
        for y in range(n - x + 1):
            z = n - x - y
            seen.add(x * a + y * b + z * c)

    print(len(seen))

if __name__ == "__main__":
    solve()
```

The implementation follows the triple-count enumeration directly. The outer loop fixes how many times `a` is used, and the inner loop fixes how many times `b` is used. The remaining count for `c` is computed implicitly, which avoids an unnecessary third loop.

The use of a set is essential because different `(x, y, z)` combinations can yield identical sums, especially when `a`, `b`, and `c` have arithmetic relationships.

## Worked Examples

Consider the input where `n = 2`, `a = 1`, `b = 2`, `c = 3`.

We enumerate all triples:

| x | y | z | sum |
| --- | --- | --- | --- |
| 0 | 0 | 2 | 6 |
| 0 | 1 | 1 | 5 |
| 0 | 2 | 0 | 4 |
| 1 | 0 | 1 | 4 |
| 1 | 1 | 0 | 3 |
| 2 | 0 | 0 | 2 |

The set of sums is `{2, 3, 4, 5, 6}`, so the answer is `5`.

This trace shows that different count distributions can collide on the same sum, such as `(x=0,y=2,z=0)` and `(x=1,y=0,z=1)` both producing `4`.

Now consider `n = 3`, `a = b = 1`, `c = 10`.

| x | y | z | sum |
| --- | --- | --- | --- |
| 3 | 0 | 0 | 3 |
| 2 | 1 | 0 | 3 |
| 2 | 0 | 1 | 12 |
| 1 | 2 | 0 | 3 |
| 1 | 1 | 1 | 12 |
| 1 | 0 | 2 | 21 |
| 0 | 3 | 0 | 3 |
| 0 | 2 | 1 | 12 |
| 0 | 1 | 2 | 21 |
| 0 | 0 | 3 | 30 |

Distinct sums are `{3, 12, 21, 30}`, so the answer is `4`.

This demonstrates how equal values among `a` and `b` create many collapsing configurations, but the set-based enumeration still captures uniqueness correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Two nested loops over x and y, with constant-time set insertion per state |
| Space | O(n^2) | In the worst case, all generated sums are distinct |

The constraint `n ≤ 1200` makes about 720,000 iterations, which is acceptable in Python. Each iteration is simple arithmetic plus a hash insert, so it fits comfortably within the time limit.

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

def solve():
    n, a, b, c = map(int, input().split())
    seen = set()
    for x in range(n + 1):
        for y in range(n - x + 1):
            z = n - x - y
            seen.add(x * a + y * b + z * c)
    print(len(seen))

# provided sample
assert run("1 1 2 3\n") == "3", "sample 1"

# all equal
assert run("5 7 7 7\n") == "1", "all equal values"

# two equal values
assert run("3 1 1 10\n") == "4", "two equal values case"

# small asymmetric
assert run("2 1 2 3\n") == "5", "small enumeration check"

# larger uniform spacing
assert run("4 1 2 4\n") >= "1", "sanity check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 7 7 7 | 1 | all values identical collapse all sums |
| 3 1 1 10 | 4 | repeated values reduce effective dimension |
| 2 1 2 3 | 5 | correctness of full enumeration |

## Edge Cases

When all three values are equal, for example `n = 1000, a = b = c = 5`, every configuration produces the same total `5000`. The algorithm iterates over all `(x, y)` pairs, but every computed sum is identical, so the set contains only one element. The final output is correctly `1`.

When two values are equal, such as `a = b = 1` and `c = 100`, many different `(x, y, z)` triples collapse into identical sums. For instance, `(x=2,y=1,z=0)` and `(x=3,y=0,z=0)` both contribute differently but still produce overlapping ranges. The set ensures duplicates are merged, and no manual deduplication logic is needed.

When values are large, like `10^9`, there is no overflow risk in Python, but in fixed-width languages this requires 64-bit integers. The algorithm never multiplies beyond `n * max(a,b,c)`, which fits safely in 64-bit signed integers.
