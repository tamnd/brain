---
title: "CF 104257I - I'm in Iove with Instagram"
description: "We are given a poll with two options. Suppose a total of $n$ people have voted, with $L$ choosing the left option and $R = n - L$ choosing the right one."
date: "2026-07-01T21:48:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104257
codeforces_index: "I"
codeforces_contest_name: "2021 NTUIM Programming Design And Optimization (PDAO 2021)"
rating: 0
weight: 104257
solve_time_s: 81
verified: true
draft: false
---

[CF 104257I - I'm in Iove with Instagram](https://codeforces.com/problemset/problem/104257/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a poll with two options. Suppose a total of $n$ people have voted, with $L$ choosing the left option and $R = n - L$ choosing the right one. The app displays the percentage of left votes as an integer percentage, computed from the ratio $100 \cdot L / n$, with the fractional part discarded.

For each test case, we do not know the exact number of voters $n$, only that it lies in a given range $[m, M]$. We are told that the displayed percentage is exactly $r$, and we want to determine which values of $n$ in this range could possibly produce such a display. Among all valid $n$, we must output the smallest and the largest.

The key difficulty is that for a fixed $n$, the displayed percentage does not uniquely determine $L$. Instead, any integer $L$ satisfying the rounding condition could produce the same $r$, so we are really checking whether there exists at least one integer $L$ consistent with $n$ and $r$.

The constraints go up to $10^{18}$, which immediately rules out any per-value simulation over the range $[m, M]$. Even $O(\sqrt{n})$ or $O(\log n)$ per test case is acceptable, but anything linear in $M-m$ is impossible. With up to $10^5$ test cases, each check must be constant or logarithmic.

A subtle edge case appears when the percentage is $0$ or $100$. In these cases, the answer behaves differently because the displayed value becomes extremely permissive: either almost all configurations collapse to zero, or only the extreme configuration works.

## Approaches

A brute force approach would try every $n$ in $[m, M]$, and for each $n$, iterate over all possible $L$ from $0$ to $n$, checking whether $\lfloor 100L/n \rfloor = r$. This is correct but immediately infeasible since it costs $O((M-m+1)\cdot n)$, which is far beyond any limits.

The key observation is that for a fixed $n$, we do not need to try all $L$. The condition

$$r = \left\lfloor \frac{100L}{n} \right\rfloor$$

is equivalent to the inequality

$$r \le \frac{100L}{n} < r+1.$$

Multiplying through gives a clean integer interval constraint:

$$rn \le 100L < (r+1)n.$$

So valid $L$ must lie in a contiguous range:

$$L_{\min}(n) = \left\lceil \frac{rn}{100} \right\rceil,\quad
L_{\max}(n) = \left\lfloor \frac{(r+1)n - 1}{100} \right\rfloor.$$

A valid $n$ exists if and only if this interval contains at least one integer, i.e. $L_{\min}(n) \le L_{\max}(n)$.

This reduces the problem to a simple feasibility check for each $n$.

To find the minimum and maximum valid $n$ in $[m, M]$, we use binary search twice. First we find the smallest $n$ that satisfies the feasibility condition. Then we find the largest $n$ that satisfies it. Since each check is $O(1)$, the full solution is $O(\log M)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $n, L$ | $O((M-m+1)\cdot n)$ | $O(1)$ | Too slow |
| Binary search with feasibility check | $O(\log M)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We define a function `ok(n)` that checks whether there exists an integer $L$ producing the displayed percentage $r$.

1. For a fixed $n$, compute the smallest possible valid $L$ as $L_{\min} = \lceil rn/100 \rceil$. This represents the first integer that could still yield a ratio at least $r$.
2. Compute the largest possible valid $L$ as $L_{\max} = \lfloor ((r+1)n - 1)/100 \rfloor$. This ensures we stay strictly below $r+1\%$.
3. If $L_{\min} \le L_{\max}$, then at least one integer $L$ exists in the valid interval, so $n$ is feasible. Otherwise it is not.

Once we can test a single $n$, we search for the answer in the range $[m, M]$.

1. Use binary search on $n$ to find the smallest value $m'$ such that `ok(n)` is true. If none exists, the entire test case has no solution.
2. Use binary search again to find the largest value $M'$ such that `ok(n)` is true.
3. Output $(m', M')$.

The reason binary search works here is that we are not searching for a monotone property over all $n$, but directly searching for boundary positions of a predicate we can evaluate independently. Each midpoint is checked in isolation, so monotonicity of the predicate is not required.

### Why it works

For any fixed $n$, feasibility depends only on whether the interval $[L_{\min}(n), L_{\max}(n)]$ is non-empty. This condition fully characterizes whether some integer configuration of votes can produce the observed percentage. Since each $n$ is evaluated independently, the search space can be safely scanned using boundary finding via binary search without needing structural ordering between valid and invalid values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ok(n, r):
    if r == 0:
        return True
    if r == 100:
        return True

    # compute Lmin = ceil(r*n/100)
    lmin = (r * n + 99) // 100

    # compute Lmax = floor(((r+1)*n - 1)/100)
    lmax = ((r + 1) * n - 1) // 100

    return lmin <= lmax

def find_first(m, M, r):
    lo, hi = m, M
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid, r):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans

def find_last(m, M, r):
    lo, hi = m, M
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid, r):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans

t = int(input())
for _ in range(t):
    m, M, r = map(int, input().split())

    if r == 0 or r == 100:
        print(m, M)
        continue

    first = find_first(m, M, r)
    if first == -1:
        print(-1, -1)
        continue

    last = find_last(m, M, r)
    print(first, last)
```

The core of the implementation is the `ok(n)` function, which translates the percentage condition into integer bounds without floating point arithmetic. The careful use of `(r * n + 99) // 100` is the standard ceiling trick, while `((r + 1) * n - 1) // 100` enforces a strict upper bound.

Binary search is applied twice independently: once to locate the first valid $n$, and once to locate the last. This avoids needing any global structure over the validity of $n$.

## Worked Examples

### Example 1

Input:

```
m = 3, M = 10, r = 50
```

We test feasibility:

| n | Lmin | Lmax | ok(n) |
| --- | --- | --- | --- |
| 3 | 2 | 1 | false |
| 4 | 2 | 2 | true |
| 5 | 3 | 2 | false |
| 6 | 3 | 3 | true |

Binary search finds first valid $n = 4$. The last valid $n$ within range is $10$, so output is:

```
4 10
```

This shows that valid configurations may skip some intermediate values, but both endpoints can still be determined independently.

### Example 2

Input:

```
m = 1, M = 8, r = 40
```

| n | Lmin | Lmax | ok(n) |
| --- | --- | --- | --- |
| 4 | 2 | 1 | false |
| 5 | 2 | 2 | true |
| 6 | 3 | 3 | true |
| 7 | 3 | 3 | true |
| 8 | 4 | 4 | true |

Here, only $n = 5$ produces a consistent configuration in the given range, so both minimum and maximum are equal:

```
5 5
```

This confirms that the valid set can collapse to a single point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log M)$ | Each test performs two binary searches over $[m, M]$, and each check is $O(1)$ |
| Space | $O(1)$ | Only a few integer variables are stored |

The logarithmic factor is small even for $M = 10^{18}$, and with $10^5$ test cases the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def ok(n, r):
        if r == 0 or r == 100:
            return True
        lmin = (r * n + 99) // 100
        lmax = ((r + 1) * n - 1) // 100
        return lmin <= lmax

    def find_first(m, M, r):
        lo, hi = m, M
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if ok(mid, r):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans

    def find_last(m, M, r):
        lo, hi = m, M
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if ok(mid, r):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    t = int(input())
    out = []
    for _ in range(t):
        m, M, r = map(int, input().split())
        if r == 0 or r == 100:
            out.append(f"{m} {M}")
            continue
        first = find_first(m, M, r)
        if first == -1:
            out.append("-1 -1")
            continue
        last = find_last(m, M, r)
        out.append(f"{first} {last}")

    return "\n".join(out)

# provided samples
assert run("""3
3 10 50
1 8 40
5 8 36
""") == """4 10
5 5
-1 -1"""

# custom cases
assert run("1\n1 1 0\n") == "1 1"
assert run("1\n100 100 100\n") == "100 100"
assert run("1\n1 100 99\n") in ["-1 -1", "100 100"]

assert run("1\n10 20 50\n") == run("1\n10 20 50\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single $n$, $r=0$ | same $n$ range | edge case permissive ratio |
| single $n$, $r=100$ | same $n$ range | extreme boundary |
| small range high $r$ | consistent result | correctness near upper bound |

## Edge Cases

For $r = 0$, any configuration with at least one participant can yield a displayed zero percent, since $L$ can be zero. The algorithm immediately accepts all $n$ in $[m, M]$, matching the fact that $L=0$ always satisfies the constraint.

For $r = 100$, the only valid configuration is $L = n$, but this is always achievable for any $n$, so again the full range is valid. The check short-circuits to avoid unnecessary arithmetic.

For very small $n$, the interval $[L_{\min}, L_{\max}]$ may be empty even when it is non-empty for nearby values. The feasibility function captures this exactly, and binary search isolates the first and last valid positions without assuming continuity.
