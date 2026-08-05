---
title: "CF 102500G - Gnoll Hypothesis"
description: "We have a circular list of n monster types. Before the update, type i appears with probability s[i] percent. A spawn location now keeps only k randomly chosen types."
date: "2026-08-05T18:07:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102500
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ICPC Northwestern European Regional Programming Contest (NWERC 2019)"
rating: 0
weight: 102500
solve_time_s: 227
verified: true
draft: false
---

[CF 102500G - Gnoll Hypothesis](https://codeforces.com/problemset/problem/102500/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a circular list of `n` monster types. Before the update, type `i` appears with probability `s[i]` percent. A spawn location now keeps only `k` randomly chosen types. The chosen types keep their own probabilities, while every removed type gives its probability to the first chosen type encountered when moving forward around the circle.

The task is to compute the expected final probability of every type after averaging over all possible random choices of the `k` kept types.

The important part is that we do not need to simulate the random pools. The number of possible pools is `C(n, k)`, which is enormous even for `n = 500`. We need to exploit the symmetry of the circular ordering and compute the contribution of every original probability independently.

Since `n` is at most 500, an `O(n^2)` algorithm is easily fast enough. An `O(n^3)` approach would already be around 125 million operations and would be risky in Python, while anything involving all subsets is impossible.

There are a few cases where incorrect solutions often fail. When `k = n`, every type is always selected, so the answer must equal the input. For example:

```
3 3
10 20 70
```

The output is:

```
10 20 70
```

A formula that accidentally allows neighboring types to contribute will produce a wrong answer here.

When `k = 1`, exactly one type survives, and it receives all probability mass. For:

```
3 1
10 20 70
```

the output is:

```
33.333333333333 33.333333333333 33.333333333333
```

Every type is equally likely to be the only selected type, regardless of its original probability.

The circular wraparound is another source of mistakes. For:

```
2 1
30 70
```

both answers are `50`. The second type can receive the first type's probability after wrapping, and the first type can receive the second type's probability.

## Approaches

A direct approach is to enumerate every possible set of `k` selected types. For each set, we could walk around the circle, assign every removed type to its next selected type, and add the resulting probabilities. This is correct because it follows the spawning rule exactly.

The problem is the number of sets. Even with `n = 500`, `C(500, 250)` is far beyond what can be processed. The brute force is not close to the required complexity.

The key observation is that expectation allows us to separate contributions. Instead of asking where a selected type receives probability from, we ask where the probability of a fixed original type goes.

Consider type `i`. Its original probability contributes to type `i + d` if that destination is selected and the `d` types immediately before it are not selected. The number of ways to choose the remaining selected types depends only on `d`, not on the actual position. This creates a fixed coefficient for every distance around the circle.

For a distance `d`, the probability that the type at distance `d` behind `i` contributes to `i` is:

```
C(n-d-1, k-1) / C(n, k)
```

The numerator chooses the other `k-1` selected types from the positions that are not blocked between the source and the destination.

After computing these coefficients once, every answer position is just a circular weighted sum of the original probabilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) * n) | O(n) | Too slow |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the coefficients for every possible circular distance. For distance `d`, store the probability that a type `d` positions behind the current type transfers its probability to the current type. This is based only on `n`, `k`, and `d`, so it can be reused for every answer position.
2. Compute combinations using floating point values. The binomial values themselves can be extremely large, but only their ratios are needed. Since `n` is small, a Pascal triangle of doubles is sufficient.
3. For every destination type `i`, iterate through all distances `d`. Add the original probability of the type at `(i - d) mod n` multiplied by the coefficient for `d`.
4. Print the resulting expected probabilities.

The invariant behind the algorithm is that every original probability is distributed exactly according to the probability of each possible destination. The coefficient for distance `d` counts precisely the events where the destination survives and all closer survivors are absent. Since all possible source contributions are added independently, linearity of expectation gives the correct expected final probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = list(map(float, input().split()))

    comb = [[0.0] * (n + 1) for _ in range(n + 1)]
    comb[0][0] = 1.0
    for i in range(1, n + 1):
        comb[i][0] = 1.0
        comb[i][i] = 1.0
        for j in range(1, i):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]

    total = comb[n][k]

    coef = []
    for d in range(n):
        coef.append(comb[n - d - 1][k - 1] / total)

    ans = [0.0] * n
    for i in range(n):
        cur = 0.0
        for d in range(n):
            cur += s[(i - d) % n] * coef[d]
        ans[i] = cur

    print(*ans)

if __name__ == "__main__":
    solve()
```

The combination table stores `C(a,b)` values as floating point numbers. Integer storage is not suitable because these values grow too large, while the final calculation only requires ratios.

The coefficient loop uses `n - d - 1` rather than `n - d`. The destination itself must already be selected, and the positions closer to the source must be absent. This boundary is the most common off-by-one mistake in this problem.

The final double loop uses modulo indexing because the monster list is circular. For a destination `i` and distance `d`, the source is `(i-d) mod n`.

## Worked Examples

For the first sample, the coefficients are:

| Distance | Coefficient |
| --- | --- |
| 0 | 0.6 |
| 1 | 0.3 |
| 2 | 0.1 |
| 3 | 0 |
| 4 | 0 |

The first answer position receives:

| Source type | Probability | Coefficient | Contribution |
| --- | --- | --- | --- |
| 1 | 1 | 0.6 | 0.6 |
| 5 | 23 | 0.3 | 6.9 |
| 4 | 12 | 0.1 | 1.2 |

The total is `8.7`, matching the sample output. The same rotation of coefficients is applied to every other position.

For the second sample, `n = 3` and `k = 2`.

| Distance | Coefficient |
| --- | --- |
| 0 | 0.666666 |
| 1 | 0.333333 |
| 2 | 0 |

The first type receives two thirds of its own probability and one third of the previous type's probability:

| Source | Value | Contribution |
| --- | --- | --- |
| Type 1 | 2.019 | 1.346 |
| Type 3 | 10.46866 | 3.489 |

The result is approximately `4.835553`, which matches the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Building combinations costs O(n^2), and computing all answers costs O(n^2). |
| Space | O(n^2) | The Pascal triangle stores all needed binomial coefficients. |

With `n = 500`, the algorithm performs about 250,000 operations in the main calculation and easily fits the limits.

## Test Cases

```python
import sys
import io

def solve_case(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    s = list(map(float, input().split()))

    comb = [[0.0] * (n + 1) for _ in range(n + 1)]
    comb[0][0] = 1.0
    for i in range(1, n + 1):
        comb[i][0] = comb[i][i] = 1.0
        for j in range(1, i):
            comb[i][j] = comb[i-1][j-1] + comb[i-1][j]

    total = comb[n][k]
    coef = [comb[n-d-1][k-1] / total for d in range(n)]

    ans = []
    for i in range(n):
        ans.append(sum(s[(i-d) % n] * coef[d] for d in range(n)))

    sys.stdin = old
    return ans

a = solve_case("""5 3
1 25 39 12 23
""")
assert all(abs(x-y) < 1e-6 for x, y in zip(a, [8.7, 17.6, 31, 21.4, 21.3]))

a = solve_case("""3 2
2.019 87.51234 10.46866
""")
assert all(abs(x-y) < 1e-6 for x, y in zip(a, [4.835553333333, 59.01456, 36.14988666667]))

a = solve_case("""1 1
100
""")
assert abs(a[0] - 100) < 1e-6

a = solve_case("""4 4
10 20 30 40
""")
assert all(abs(x-y) < 1e-6 for x, y in zip(a, [10, 20, 30, 40]))

a = solve_case("""4 1
25 25 25 25
""")
assert all(abs(x-25) < 1e-6 for x in a)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 100` | `100` | Minimum size and single type handling |
| `4 4 / 10 20 30 40` | Original values | The `k=n` boundary |
| `4 1 / equal values` | Equal values | The `k=1` probability distribution |
| Samples | Sample outputs | General correctness |

## Edge Cases

For `k = n`, every monster survives. In the formula, all coefficients except distance zero become zero because there are not enough unselected positions to create a transfer. The algorithm reduces to returning the original array.

For `k = 1`, every coefficient becomes `1/n`. There is exactly one selected monster, and every original probability eventually belongs to that one monster with equal probability of selection. The circular structure does not affect the result.

For wraparound cases, modulo indexing treats the list as a circle. A source near the beginning can contribute to a destination near the end, and the same coefficient calculation still applies because distance is measured cyclically.
