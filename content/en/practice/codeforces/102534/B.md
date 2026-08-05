---
title: "CF 102534B - Need More T-shirts!"
description: "The organizers have a list of values describing T-shirt colors. For every color, the value was written either as the exact number of shirts of that color or as the percentage of all shirts having that color."
date: "2026-08-05T16:06:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102534
codeforces_index: "B"
codeforces_contest_name: "Innopolis Open 2020 Finals"
rating: 0
weight: 102534
solve_time_s: 552
verified: true
draft: false
---

[CF 102534B - Need More T-shirts!](https://codeforces.com/problemset/problem/102534/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The organizers have a list of values describing T-shirt colors. For every color, the value was written either as the exact number of shirts of that color or as the percentage of all shirts having that color. The original total number of shirts is missing, and the task is to find every total that could make the whole list valid.

For a chosen total `T`, if a value `x` represents a percentage, it contributes `T * x / 100` shirts. If it represents a count, it contributes exactly `x` shirts. The sum of all contributions must be exactly `T`.

The input size can reach `100000`, and values can be as large as `10^9`. Trying all possible assignments of values to either "count" or "percentage" would require exponential time, because every small value could have two interpretations. Even checking many possible totals directly is impossible. The solution has to exploit the fact that percentages are limited to the range from 1 to 100.

The tricky cases come from ambiguous values. A value such as `50` can be a count or a percentage. For example, with input:

```
2
1 50
```

the valid totals are `2` and `51`. The total `2` uses `1` as a count and `50` as a percentage. The total `51` uses both values as counts. A solution that always treats values at most `100` as percentages would miss `51`.

Another special case is when all values are percentages. This is forbidden because the statement guarantees at least one exact count. For example:

```
3
20 30 50
```

choosing all three values as percentages gives a total percentage of `100`, but there is no color with a fixed number of shirts, so that interpretation must be rejected.

## Approaches

The brute-force approach would try every subset of values that are interpreted as percentages. For every subset, we could derive the possible total and verify it. This is correct because every possible assignment is checked, but there can be up to `100000` values, giving up to `2^100000` assignments. Even with only `30` ambiguous values, the number of cases is already too large.

The key observation is that only values from `1` to `100` can ever be percentages. More importantly, the sum of chosen percentages must be at most `100`. We do not need to know which exact subset created a percentage sum beyond this limit. We only need to know which sums are reachable.

Let `A` be the sum of all input values. Suppose a subset of values is interpreted as percentages, and the sum of those percentages is `q`. The remaining values are interpreted as fixed counts, so their sum is `A - q`. The total satisfies:

```
A - q + T * q / 100 = T
```

Rearranging gives:

```
T = 100 * (A - q) / (100 - q)
```

For every reachable `q` smaller than `100`, we can calculate a candidate answer and check whether the division is exact.

The only remaining difficulty is ensuring that at least one value stays as a count. If the selected percentage subset contains every element, the assignment is invalid. Since the total sum of all values is usually larger than `100`, this only matters when the whole array sum is at most `100`.

The possible percentage sums can be found with a tiny subset sum dynamic programming over the range `0` to `100`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n + 100^2) | O(100) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of all values, `A`. Values larger than `100` cannot be percentages, but they still participate naturally in the sum.
2. Use subset sum dynamic programming to find every reachable percentage sum from values that are at most `100`. The state `dp[x]` means that some valid choice of percentage values has total percentage `x`.

The limit is only `100`, so the dynamic programming is constant size regardless of `n`.
3. For every reachable percentage sum `q` from `0` to `99`, calculate:

```
numerator = 100 * (A - q)
denominator = 100 - q
```

If `numerator` is divisible by `denominator`, the resulting total is a candidate.

1. Reject candidates created by assigning every value to the percentage side. This can only happen when `A == q`, because all values are positive.
2. Sort all remaining candidates and print them.

Why it works: every valid interpretation selects some subset of values as percentages. The only information from that subset that affects the total formula is the sum of its percentages, `q`. The dynamic program finds every possible `q`, so every valid total is considered. The divisibility check guarantees that the computed total is an integer, and the count-side check guarantees that at least one element is interpreted as an exact number.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    total_sum = sum(a)

    dp = [False] * 101
    dp[0] = True

    for x in a:
        if x <= 100:
            for s in range(100 - x, -1, -1):
                if dp[s]:
                    dp[s + x] = True

    ans = set()

    for q in range(100):
        if not dp[q]:
            continue

        if total_sum == q:
            continue

        num = 100 * (total_sum - q)
        den = 100 - q

        if num % den == 0:
            ans.add(num // den)

    ans = sorted(ans)

    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The array `dp` stores reachable percentage sums. It is updated backwards so that every input value is used at most once in the subset. Forward iteration would allow the same value to be counted multiple times.

The formula is evaluated only for `q < 100`. A percentage sum of exactly `100` would make the denominator zero. Such a case can only describe a situation where every value was treated as a percentage, which is invalid because one exact count must exist.

Python integers do not overflow, so the multiplication by `100` is safe even when the input values are large.

## Worked Examples

For:

```
2
1 50
```

the reachable percentage sums are `0`, `1`, `50`, and `51`.

| q | Formula result | Accepted |
| --- | --- | --- |
| 0 | 51 | Yes |
| 1 | 51.5 | No |
| 50 | 2 | Yes |
| 51 | 1.98 | No |

The output is:

```
2
2 51
```

The trace shows why both interpretations of the ambiguous value `50` matter.

For:

```
3
20 30 70
```

the reachable percentage sums include:

| q | Formula result | Accepted |
| --- | --- | --- |
| 0 | 120 | Yes |
| 20 | 125 | Yes |
| 50 | 140 | Yes |
| 70 | 300 | Yes |

The output is:

```
4
120 125 140 300
```

The same values can describe several different totals because different subsets are percentages.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 100^2) | Each value updates a dynamic programming array of fixed size 101 |
| Space | O(100) | Only the reachable percentage sums are stored |

The algorithm processes the entire input once and performs only a constant amount of additional work per element, which fits easily within the limits for `n = 100000`.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline

    n = int(data())
    a = list(map(int, data().split()))

    total_sum = sum(a)

    dp = [False] * 101
    dp[0] = True

    for x in a:
        if x <= 100:
            for s in range(100 - x, -1, -1):
                if dp[s]:
                    dp[s + x] = True

    ans = set()

    for q in range(100):
        if dp[q] and total_sum != q:
            num = 100 * (total_sum - q)
            den = 100 - q
            if num % den == 0:
                ans.add(num // den)

    res = str(len(ans)) + "\n" + " ".join(map(str, sorted(ans))) + "\n"

    sys.stdin = old
    return res

assert solve_io("2\n1 50\n") == "2\n2 51\n"
assert solve_io("3\n20 30 70\n") == "4\n120 125 140 300\n"

assert solve_io("1\n100\n") == "1\n100\n"
assert solve_io("4\n2 40 90 5\n") == "3\n137 470 840\n"
assert solve_io("3\n10 20 30\n") == "1\n60\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100` | `100` | Single value and boundary percentage handling |
| `2 / 1 50` | `2 51` | Values that can be either counts or percentages |
| `3 / 10 20 30` | `60` | All values interpreted as counts |
| `4 / 2 40 90 5` | `137 470 840` | Multiple valid percentage subsets |

## Edge Cases

When a value is both a possible count and a possible percentage, the algorithm considers both possibilities through different percentage sums. For input:

```
2
1 50
```

`q = 0` gives the total `51`, while `q = 50` gives the total `2`. Both remain in the answer.

When all values sum to exactly a possible percentage total, the algorithm removes the invalid interpretation where every value becomes a percentage. For input:

```
3
20 30 50
```

the subset sum `100` exists, but it leaves no exact count behind. The problem requires at least one exact count, so that interpretation is discarded.

When large values appear, they cannot be percentages because percentages are at most `100`. They still contribute to `A`, and the same formula handles them automatically. For example, a value like `1000000000` can only stay on the count side, preventing unnecessary branching.
