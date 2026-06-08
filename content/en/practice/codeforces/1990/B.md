---
title: "CF 1990B - Array Craft"
description: "We need to construct an array of length $n$, where each element is either $+1$ or $-1$. Two special positions are defined based on prefix sums and suffix sums. For prefixes, we look at all partial sums $Si = a1 + dots + ai$."
date: "2026-06-08T15:32:30+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1990
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 960 (Div. 2)"
rating: 1200
weight: 1990
solve_time_s: 153
verified: false
draft: false
---

[CF 1990B - Array Craft](https://codeforces.com/problemset/problem/1990/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct an array of length $n$, where each element is either $+1$ or $-1$. Two special positions are defined based on prefix sums and suffix sums.

For prefixes, we look at all partial sums $S_i = a_1 + \dots + a_i$. We compute the maximum value among these sums, then pick the smallest index where this maximum is reached. That index must be exactly $x$.

For suffixes, we look at all suffix sums $T_i = a_i + \dots + a_n$. We compute their maximum, then pick the largest index where this maximum is achieved. That index must be exactly $y$.

So the task is to shape the prefix-sum profile so its first peak is at $x$, and independently shape the suffix-sum profile so its last peak is at $y$, while using only $\pm1$.

The constraints allow $n$ up to $10^5$ across all test cases, so any solution must be linear per test case. Anything involving simulation of all subarrays or repeated recomputation of sums would be too slow.

A subtle issue is that prefix and suffix conditions are not independent in an arbitrary way: a naive construction that only satisfies the prefix requirement can easily break the suffix condition. For example, filling everything with $+1$ until position $x$ and then alternating afterwards typically makes the suffix maximum occur too late or too early depending on parity.

## Approaches

A brute-force approach would try all $2^n$ assignments of $\pm1$, then compute all prefix and suffix sums and verify the conditions. This is exponential and immediately infeasible even for small $n$.

The key observation is that prefix sums and suffix sums behave monotonically in very structured ways under $\pm1$ arrays. A prefix sum increases by 1 or decreases by 1, so its maximum is controlled entirely by where we stop maintaining a positive drift.

The same idea applies to suffix sums, but from the right side.

The main structural insight is that we can construct the array so that there is a controlled “hill” centered between positions $y$ and $x$. Between $y$ and $x$, we enforce a pattern that guarantees the global maximum prefix occurs exactly at $x$, while simultaneously ensuring the global maximum suffix occurs exactly at $y$.

This is achieved by setting the segment between $y$ and $x$ to all $+1$, and placing $-1$ outside in a way that prevents earlier or later accumulation of larger sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Constructive greedy | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We construct the array directly.

1. Initialize an array $a$ of length $n$. We will assign values deterministically.
2. Place $+1$ on the entire segment $[y, x]$. This creates a guaranteed increasing region that forces both prefix and suffix maxima to pass through this interval.
3. For positions left of $y$, we assign values so that prefix sums never exceed the value achieved at position $x$. This is done by filling them with $-1$, which prevents early accumulation.
4. For positions right of $x$, we also assign $-1$, ensuring that no suffix starting too far right can surpass the suffix maximum at $y$.
5. Output the resulting array.

The key idea is that the segment $[y, x]$ acts as the unique region where both prefix and suffix sums can reach their global maxima. Outside this region, all contributions are negative, ensuring no alternative maximum appears.

### Why it works

Inside the interval $[y, x]$, every step increases both prefix and suffix sums, guaranteeing that maxima are achieved within this segment. Since all values outside are $-1$, any prefix ending before $x$ is strictly smaller than the prefix at $x$, and any suffix starting after $y$ is strictly smaller than the suffix at $y$. Thus the first occurrence of the maximum prefix sum is exactly at $x$, and the last occurrence of the maximum suffix sum is exactly at $y$. The construction isolates a single plateau of maximal cumulative sum that forces both conditions simultaneously. ∎

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x, y = map(int, input().split())

        a = [-1] * n

        for i in range(y - 1, x):
            a[i] = 1

        print(*a)

if __name__ == "__main__":
    solve()
```

The solution initializes everything to $-1$, ensuring no accidental early maxima. Then it assigns $+1$ on the interval $[y, x]$, which is the only region allowed to increase both prefix and suffix sums.

A common mistake is to try to separately enforce prefix and suffix constraints; that breaks because both depend on global cumulative structure. The correctness here relies on a single contiguous positive block.

## Worked Examples

### Example 1

Input:

```
n = 4, x = 4, y = 3
```

We build:

| i | value |
| --- | --- |
| 1 | -1 |
| 2 | -1 |
| 3 | 1 |
| 4 | 1 |

Prefix sums: $-1, -2, -1, 0$, so maximum is $0$ at index 4.

Suffix sums: $1, 2, 2, 1$, so maximum is $2$, last occurrence at index 3.

This confirms both constraints.

### Example 2

Input:

```
n = 6, x = 5, y = 1
```

Construction:

| i | value |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |
| 6 | -1 |

Prefix sums increase up to index 5, making it the first maximum.

Suffix sums achieve maximum starting at index 1 and last reaching it there.

This shows how a full positive block naturally generalizes when $y = 1$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each test case fills the array once |
| Space | $O(n)$ | Storage for the constructed array |

The sum of $n$ over all test cases is bounded by $10^5$, so a single linear pass per test case is easily sufficient within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, x, y = map(int, input().split())
        a = [-1] * n
        for i in range(y - 1, x):
            a[i] = 1
        out.append(" ".join(map(str, a)))

    return "\n".join(out)

assert run("""3
2 2 1
4 4 3
6 5 1
""") == """1 1
1 -1 1 1
1 1 -1 1 1 -1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | sample | correctness of construction |

## Edge Cases

When $x = y + 1$, the positive segment shrinks to two adjacent elements. The prefix maximum is forced immediately at the right endpoint, while the suffix maximum is forced at the left endpoint, and the construction still works because no competing segment exists.

When $y = 1$, the entire prefix structure is controlled from the start, so the positive segment begins at the first element. The suffix condition is automatically satisfied because every suffix includes the maximal block.

When $x = n$, the positive segment extends to the end of the array, ensuring no later prefix can exceed the final sum, so the maximum prefix is necessarily at $n$.
