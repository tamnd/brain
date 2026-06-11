---
title: "CF 1288A - Deadline"
description: "For each test case, we have a deadline of n days and a program that normally needs d days to finish. Before running the program, we may spend x days optimizing it."
date: "2026-06-11T19:00:43+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1288
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 80 (Rated for Div. 2)"
rating: 1100
weight: 1288
solve_time_s: 117
verified: true
draft: false
---

[CF 1288A - Deadline](https://codeforces.com/problemset/problem/1288/A)

**Rating:** 1100  
**Tags:** binary search, brute force, math, ternary search  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we have a deadline of `n` days and a program that normally needs `d` days to finish.

Before running the program, we may spend `x` days optimizing it. After spending those `x` days, the running time becomes:

$$\left\lceil \frac{d}{x+1} \right\rceil$$

Since optimization and execution cannot happen at the same time, the total time spent is:

$$x + \left\lceil \frac{d}{x+1} \right\rceil$$

We must determine whether there exists some non-negative integer `x` such that the total time is at most `n`.

The constraints are the main challenge. Both `n` and `d` can be as large as `10^9`, so iterating through every possible value of `x` is impossible. Even a single test case could require checking billions of candidates. With up to 50 test cases, any solution close to `O(d)` is completely infeasible.

The expression

$$f(x)=x+\left\lceil \frac{d}{x+1} \right\rceil$$

has a useful shape. As `x` increases, the first term grows while the second term shrinks. The minimum occurs near the point where these effects balance each other. Exploiting that structure is what makes the problem easy.

Several edge cases can cause mistakes.

Consider:

```
1
1 1
```

The correct answer is `YES` because choosing `x = 0` gives total time `1`. A solution that only checks positive values of `x` would fail.

Consider:

```
1
5 11
```

The answer is `NO`. Even though optimization helps, no value of `x` reduces the total time to `5` or less. A greedy strategy such as "keep optimizing until runtime becomes small" does not guarantee the minimum total.

Consider:

```
1
1000000000 1000000000
```

The answer is `YES`. Large values require careful integer arithmetic. Languages with fixed-width integers could overflow if the implementation is careless. Python handles this automatically, but the algorithm should still avoid unnecessary large computations.

## Approaches

The most direct idea is to try every possible optimization amount `x`. For each candidate we compute

$$x+\left\lceil \frac{d}{x+1} \right\rceil$$

and check whether it is at most `n`.

This brute-force approach is correct because it examines every legal choice. The problem is its running time. In the worst case, `d` can be `10^9`, so checking all values from `0` to `d` would require roughly one billion evaluations for a single test case. That is far beyond the limit.

To find something faster, look at the function

$$f(x)=x+\left\lceil \frac{d}{x+1} \right\rceil.$$

Ignoring the ceiling for a moment gives

$$x+\frac{d}{x+1}.$$

This is a classic convex-shaped expression. Initially, increasing `x` helps because the division term drops quickly. Later, increasing `x` hurts because the linear term dominates.

The minimum occurs near

$$x \approx \sqrt d - 1.$$

Since `d ≤ 10^9`, we have

$$\sqrt d \le 31623.$$

That observation changes everything. The optimal value can only be near the square root, so it is enough to test all values up to about `√d`. This costs only around thirty thousand checks per test case.

Another way to view it is that Codeforces intended a simple mathematical brute force. If `x` becomes much larger than `√d`, the linear term is already too expensive, while the division term changes very slowly. The minimum cannot hide far away from the square root region.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d) | O(1) | Too slow |
| Optimal | O(√d) | O(1) | Accepted |

## Algorithm Walkthrough

1. For a test case, first check whether `d ≤ n`.

If the program already finishes before the deadline, no optimization is needed and the answer is immediately `YES`.
2. Compute `limit = ⌊√d⌋ + 2`.

The minimum of the objective function occurs near `√d`, so checking slightly beyond that point is sufficient.
3. For every integer `x` from `0` to `limit`, compute

$$x+\left\lceil \frac{d}{x+1} \right\rceil.$$

The ceiling can be computed using integer arithmetic:

$$\left\lceil \frac{d}{x+1} \right\rceil
=
\frac{d+x}{x+1}$$

with integer division.
4. If any candidate produces a value not exceeding `n`, output `YES`.

We only need one feasible optimization amount.
5. If all candidates fail, output `NO`.

### Why it works

The function

$$f(x)=x+\left\lceil \frac{d}{x+1} \right\rceil$$

is the sum of an increasing term and a decreasing term. Its minimum is attained near the balance point of those two effects, which is around `√d`.

For values significantly larger than `√d`, the linear part `x` already exceeds the region where the minimum can occur, while the division term changes only slightly. Checking all values from `0` through roughly `√d` guarantees that we encounter the minimum or a value no worse than it. If any feasible solution exists, one of those checked values will satisfy the deadline condition.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, d = map(int, input().split())

    ok = False
    limit = math.isqrt(d) + 2

    for x in range(limit + 1):
        total = x + (d + x) // (x + 1)
        if total <= n:
            ok = True
            break

    print("YES" if ok else "NO")
```

The loop over `x` is the core of the solution. Instead of exploring all possible optimization amounts, it only checks values up to approximately `√d`.

The expression

```
(d + x) // (x + 1)
```

implements the ceiling division

$$\left\lceil \frac{d}{x+1} \right\rceil.$$

A common mistake is to use ordinary integer division:

```
d // (x + 1)
```

which computes the floor and can incorrectly accept impossible schedules.

Using `math.isqrt(d)` avoids floating-point precision issues. Since `d` can reach `10^9`, either approach would work here, but integer square roots are cleaner and exact.

The algorithm stops as soon as it finds a feasible value because the problem only asks whether such a value exists.

## Worked Examples

### Example 1

Input:

```
n = 4
d = 5
```

| x | ceil(5/(x+1)) | total |
| --- | --- | --- |
| 0 | 5 | 5 |
| 1 | 3 | 4 |

At `x = 1`, the total time becomes `4`, which matches the deadline.

The algorithm immediately outputs `YES`. This example shows that a small amount of optimization can be beneficial even when the original runtime exceeds the deadline.

### Example 2

Input:

```
n = 5
d = 11
```

| x | ceil(11/(x+1)) | total |
| --- | --- | --- |
| 0 | 11 | 11 |
| 1 | 6 | 7 |
| 2 | 4 | 6 |
| 3 | 3 | 6 |
| 4 | 3 | 7 |
| 5 | 2 | 7 |

The minimum total achieved is `6`, which is still larger than `5`.

Since no checked value satisfies the deadline, the answer is `NO`.

This example illustrates that optimization cannot always compensate for a large runtime.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√d) | We test only values from `0` to about `√d` |
| Space | O(1) | Only a few variables are stored |

Since `√10^9 ≈ 31623`, each test case performs only a few tens of thousands of iterations. With at most 50 test cases, this easily fits within the time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io, math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n, d = map(int, input().split())

        ok = False
        limit = math.isqrt(d) + 2

        for x in range(limit + 1):
            total = x + (d + x) // (x + 1)
            if total <= n:
                ok = True
                break

        ans.append("YES" if ok else "NO")

    return "\n".join(ans) + "\n"

# provided samples
assert run("3\n1 1\n4 5\n5 11\n") == "YES\nYES\nNO\n", "sample 1"

# minimum values
assert run("1\n1 1\n") == "YES\n", "minimum case"

# exact boundary where no optimization needed
assert run("1\n10 10\n") == "YES\n", "d equals n"

# impossible case
assert run("1\n1 100\n") == "NO\n", "far beyond deadline"

# maximum values
assert run("1\n1000000000 1000000000\n") == "YES\n", "maximum constraints"

# near optimum around sqrt(d)
assert run("1\n6 11\n") == "YES\n", "minimum total equals 6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `YES` | Smallest valid input |
| `10 10` | `YES` | No optimization required |
| `1 100` | `NO` | Clearly impossible schedule |
| `1000000000 1000000000` | `YES` | Largest values |
| `6 11` | `YES` | Boundary where optimum exactly meets deadline |

## Edge Cases

Consider:

```
1
1 1
```

The algorithm checks `x = 0`.

$$0+\left\lceil \frac{1}{1}\right\rceil = 1$$

Since `1 ≤ 1`, it outputs `YES`. This is why the search must include `x = 0`.

Consider:

```
1
10 10
```

Without any optimization:

$$0+\left\lceil \frac{10}{1}\right\rceil = 10$$

The condition already holds. The algorithm immediately finds a feasible value and returns `YES`.

Consider:

```
1
5 11
```

The examined totals are:

$$11,7,6,6,7,\ldots$$

The minimum is `6`, which is still larger than `5`. After checking all relevant values up to roughly `√11`, the algorithm concludes correctly that no feasible schedule exists and prints `NO`.

Consider:

```
1
1000000000 1000000000
```

The optimum occurs near `√10^9 ≈ 31623`.

For example:

$$31622+\left\lceil \frac{10^9}{31623}\right\rceil
\approx 63245$$

which is far below `10^9`. The algorithm quickly finds such a value and outputs `YES`. This confirms that the implementation handles the largest inputs efficiently.
