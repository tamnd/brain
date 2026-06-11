---
title: "CF 1157D - N Problems During K Days"
description: "We need to distribute exactly n solved problems across k consecutive days. Let a[i] be the number of problems solved on day i. Every day must contain at least one problem."
date: "2026-06-12T02:34:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1157
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 555 (Div. 3)"
rating: 1900
weight: 1157
solve_time_s: 105
verified: false
draft: false
---

[CF 1157D - N Problems During K Days](https://codeforces.com/problemset/problem/1157/D)

**Rating:** 1900  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We need to distribute exactly `n` solved problems across `k` consecutive days.

Let `a[i]` be the number of problems solved on day `i`. Every day must contain at least one problem. The sequence must be strictly increasing, and each day's value may grow by at most a factor of two:

$$a_i < a_{i+1} \le 2a_i$$

The sum of all values must be exactly `n`.

The task is not to optimize anything. We only need to construct one valid sequence or determine that no such sequence exists.

The constraints are unusual. The number of days can be as large as `10^5`, while the total number of problems can be as large as `10^9`. Any algorithm that tries to search over possible sequences is hopeless. Even storing many candidate states per day would be too expensive. We need a direct constructive method that runs in roughly linear time in `k`.

The first observation comes from the smallest possible valid sequence. Since the values must be strictly increasing positive integers, the minimum sequence is

$$1,2,3,\ldots,k$$

whose sum is

$$\frac{k(k+1)}2$$

If `n` is smaller than this value, no solution exists because every valid sequence must have at least that many total problems.

A second subtle case occurs when the sequence is forced too large. Suppose `k=3` and `n=100`. Starting from any first value `x`, the largest possible sequence is approximately

$$x,\ 2x,\ 4x$$

with total `7x`. The growth restriction limits how much total sum can be packed into the sequence. A construction must respect both the lower and upper growth bounds.

Consider `n=5, k=3`.

The minimum possible sum is

$$1+2+3=6$$

so the correct answer is `NO`. A careless implementation that only checks positivity might incorrectly output `1 1 3`, but the sequence is not strictly increasing.

Consider `n=8, k=3`.

A valid answer is

$$1\ 2\ 5$$

No, it is not valid because `5 > 2·2`. The doubling restriction is easy to forget when greedily dumping remaining problems into the last day.

Consider `n=26, k=6`.

The minimum sequence already uses

$$1+2+3+4+5+6 = 21$$

There are only 5 extra problems to distribute. The distribution must preserve both monotonicity and doubling constraints. Simply adding all extras to the last element would create

$$1\ 2\ 3\ 4\ 5\ 11$$

which violates `11 ≤ 10`.

These examples show that the difficulty is balancing the extra sum while maintaining all local constraints.

## Approaches

A brute force approach would try to generate increasing sequences whose sum is `n` and test the doubling condition. Even for moderate values this becomes enormous. The number of increasing integer sequences with fixed sum grows combinatorially, and `n` can reach `10^9`. Exhaustive search is completely infeasible.

The key observation is that every valid sequence can be viewed as a base sequence

$$x,\ x+1,\ x+2,\ \ldots,\ x+k-1$$

plus some additional increments distributed across the days.

If the first value is fixed to `x`, the minimum achievable sum is

$$kx + \frac{k(k-1)}2.$$

This immediately suggests finding the largest possible starting value `x` whose minimum sum does not exceed `n`.

Why is a large starting value useful? Because increasing every element by one consumes `k` units of total sum while automatically preserving all constraints. We want to absorb as much of `n` as possible this way before handling the remaining smaller amount.

After fixing `x`, there remains some extra amount

$$r = n - \left(kx + \frac{k(k-1)}2\right).$$

The sequence starts as

$$x,\ x+1,\ \ldots,\ x+k-1.$$

Now we distribute `r` additional units. The doubling constraint determines how much each position may be increased. Processing from left to right, each element can grow until it reaches either

$$2a_{i-1}$$

or whatever amount is still needed. This greedy distribution maximizes earlier elements first, creating as much room as possible for later elements.

If after processing all positions the remainder becomes zero, we have a valid sequence. Otherwise the target sum cannot be achieved.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum possible sum:

$$S_{\min}=\frac{k(k+1)}2$$

If `n < Smin`, print `NO`.
2. Find the largest integer `x` such that

$$kx+\frac{k(k-1)}2 \le n.$$

This is

$$x=\left\lfloor\frac{n-\frac{k(k-1)}2}{k}\right\rfloor.$$

Choosing the largest possible starting value absorbs most of the total sum while automatically satisfying all constraints.
3. Build the base sequence

$$a_i = x+i$$

using zero-based indexing.
4. Compute the remaining amount

$$r = n-\sum a_i.$$
5. Process positions from the end toward the beginning.

For position `i`, determine the largest increase that keeps

$$a_i \le 2a_{i-1}.$$

The available capacity is

$$2a_{i-1}-a_i.$$
6. Add

$$\min(r,\text{capacity})$$

to `a_i`, then subtract the same amount from `r`.
7. Continue until all positions have been processed.
8. If `r` is still positive, print `NO`. Otherwise print `YES` and the sequence.

### Why it works

The base sequence is the smallest valid sequence with first value `x`. Any larger valid sequence with the same first value can only be obtained by adding nonnegative increments.

When distributing the remaining sum, increasing a later position never affects constraints involving earlier positions. Giving each position as much as possible maximizes the future capacity of the sequence. If this greedy process cannot absorb all remaining units, then no other distribution can, because every position has already reached its maximum legal value. Hence the algorithm succeeds exactly when a valid sequence exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    if n < k * (k + 1) // 2:
        print("NO")
        return

    x = (n - k * (k - 1) // 2) // k

    a = [x + i for i in range(k)]

    cur_sum = sum(a)
    rem = n - cur_sum

    for i in range(k - 1, 0, -1):
        cap = 2 * a[i - 1] - a[i]
        add = min(rem, cap)
        a[i] += add
        rem -= add

    if rem != 0:
        print("NO")
        return

    print("YES")
    print(*a)

solve()
```

The first check handles the fundamental impossibility condition. If even the strictly increasing sequence `1,2,...,k` exceeds `n`, no construction exists.

The value `x` is chosen as the largest feasible starting value. This is the critical idea that reduces the remaining adjustment to less than `k`.

The array initially contains the minimum valid sequence beginning at `x`. Its sum is guaranteed not to exceed `n`.

The remainder is distributed from right to left. For each position we compute exactly how much room remains before the doubling constraint becomes tight. Adding more than this amount would violate the problem conditions.

The final remainder check is essential. Some values of `n` cannot be represented even though `n` exceeds the minimum sum. In those cases the greedy filling reaches all capacities while some remainder still exists, proving impossibility.

All arithmetic comfortably fits in 64-bit integers. Python integers handle this automatically.

## Worked Examples

### Example 1

Input:

```
26 6
```

First compute

$$x=\left\lfloor\frac{26-15}{6}\right\rfloor=1$$

Base sequence:

$$[1,2,3,4,5,6]$$

Sum = 21, remainder = 5.

| Position | Value Before | Capacity | Added | Value After | Remaining |
| --- | --- | --- | --- | --- | --- |
| 5 | 6 | 4 | 4 | 10 | 1 |
| 4 | 5 | 3 | 1 | 6 | 0 |

Final sequence:

```
1 2 3 4 6 10
```

The sum is 26, the sequence is strictly increasing, and every value is at most twice the previous one.

### Example 2

Input:

```
10 4
```

Minimum possible sum:

$$1+2+3+4=10$$

So `x=1`.

| Position | Value Before | Capacity | Added | Value After | Remaining |
| --- | --- | --- | --- | --- | --- |
| Initial | - | - | - | [1,2,3,4] | 0 |

Final sequence:

```
1 2 3 4
```

This example shows the boundary where no extra distribution is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | One pass to build the sequence and one pass to distribute the remainder |
| Space | O(k) | Stores the constructed answer |

With `k ≤ 100000`, a linear scan is easily fast enough. Memory usage is also modest because only the final sequence is stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, k = map(int, input().split())

    if n < k * (k + 1) // 2:
        return "NO\n"

    x = (n - k * (k - 1) // 2) // k

    a = [x + i for i in range(k)]
    rem = n - sum(a)

    for i in range(k - 1, 0, -1):
        cap = 2 * a[i - 1] - a[i]
        add = min(rem, cap)
        a[i] += add
        rem -= add

    if rem:
        return "NO\n"

    return "YES\n" + " ".join(map(str, a)) + "\n"

assert run("26 6\n").startswith("YES"), "sample"

assert run("1 1\n") == "YES\n1\n", "minimum input"

assert run("5 3\n") == "NO\n", "below minimum sum"

assert run("10 4\n") == "YES\n1 2 3 4\n", "exact minimum"

assert run("1000000000 1\n") == "YES\n1000000000\n", "largest n with k=1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `YES 1` | Smallest legal instance |
| `5 3` | `NO` | Sum below minimum possible |
| `10 4` | `1 2 3 4` | Exact lower boundary |
| `1000000000 1` | Single value | Large-number handling |

## Edge Cases

Consider:

```
5 3
```

The minimum valid sum is

$$1+2+3=6$$

Since `5 < 6`, the algorithm immediately prints `NO`. This prevents constructions that satisfy the sum but violate strict increase.

Consider:

```
8 3
```

The algorithm builds `[1,2,3]` with remainder `2`.

The last position has capacity

$$2\cdot2-3=1$$

so it becomes `4`, leaving remainder `1`.

The middle position cannot increase because it would break strict ordering with the first element. The remainder survives, so the algorithm outputs `NO`.

This correctly rejects sequences such as `1 2 5`, which satisfy the sum but violate the doubling limit.

Consider:

```
100 3
```

The algorithm starts with a large `x`, then attempts to distribute the remaining amount. Every position eventually reaches its maximum legal value. If extra sum still remains, the algorithm reports impossibility. This captures the upper-growth restriction that many naive greedy solutions overlook.
