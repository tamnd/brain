---
title: "CF 104639L - KaChang!"
description: "We are given a reference program whose running time is fixed at $T$, and a list of $n$ other programs with known running times."
date: "2026-06-29T16:58:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104639
codeforces_index: "L"
codeforces_contest_name: "The 2023 ICPC Asia EC Regionals Online Contest (I)"
rating: 0
weight: 104639
solve_time_s: 41
verified: true
draft: false
---

[CF 104639L - KaChang!](https://codeforces.com/problemset/problem/104639/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a reference program whose running time is fixed at $T$, and a list of $n$ other programs with known running times. We are asked to choose an integer multiplier $k \ge 2$ such that a time limit of $k \cdot T$ is sufficient for every program in the list to finish, meaning every $t_i \le k \cdot T$. Among all valid values, we must output the smallest possible $k$.

Rewriting the condition, each program imposes a lower bound on $k$: for a given $t_i$, we need $k \ge \frac{t_i}{T}$. Since $k$ must be an integer, the true constraint becomes $k \ge \left\lceil \frac{t_i}{T} \right\rceil$. The final answer is therefore the maximum over all programs of these per-program requirements, with the additional constraint that $k \ge 2$.

The constraints $n \le 10^5$ and $t_i \le 10^9$ suggest we must compute the answer in linear time. Any approach involving sorting is unnecessary and would be slower than required but still acceptable; however, a single pass is sufficient.

A subtle case appears when all programs are very fast compared to $T$. Then every ratio is less than 1, so the computed maximum becomes 1, but the problem explicitly enforces $k \ge 2$. For example, if $T = 1000$ and all $t_i \le 500$, the correct answer is 2 even though all programs already pass with $k = 1$.

Another edge case occurs when some $t_i$ is much larger than $T$, which can push the answer up to $10^9$ scale. Since multiplication is within 64-bit integer range, we are safe in Python but would need care in fixed-width languages.

## Approaches

A direct way to think about the problem is to try all possible values of $k$, starting from 2 upward, and check whether all programs satisfy $t_i \le kT$. For each $k$, this requires scanning all $n$ programs, so each check costs $O(n)$. In the worst case, $k$ could grow up to around $10^9$, which makes this approach completely infeasible.

The key observation is that feasibility is monotonic in $k$. If a certain $k$ works, then any larger $k$ also works. This reduces the problem to finding the smallest integer $k$ that satisfies a set of lower bounds, which can be derived directly from each program independently.

Each program contributes a requirement $k \ge \lceil t_i / T \rceil$. Instead of searching over $k$, we compute these requirements directly and take their maximum. This collapses the problem from a search over an interval to a single pass aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k | $O(n \cdot k)$ | $O(1)$ | Too slow |
| Direct maximum ratio | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$ and $T$. These define the scaling baseline for all comparisons.
2. Initialize a variable $k\_req = 2$, because the problem enforces a minimum allowed multiplier of 2 regardless of data.
3. For each program time $t_i$, compute the smallest multiplier that would make it pass. This is $\left\lceil \frac{t_i}{T} \right\rceil$.
4. Update $k\_req = \max(k\_req, \lceil t_i / T \rceil)$. This ensures that all constraints seen so far remain satisfied. The maximum is used because every program independently constrains the same global $k$.
5. After processing all programs, output $k\_req$.

### Why it works

Each program imposes an independent inequality $kT \ge t_i$, which can be rearranged into $k \ge t_i / T$. Since all constraints must hold simultaneously, $k$ must satisfy the strongest among them. The ceiling converts fractional requirements into integer feasibility constraints. Taking the maximum over all programs preserves exactly the tightest constraint, so the final value is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, T = map(int, input().split())
    arr = list(map(int, input().split()))
    
    k_req = 2
    
    for t in arr:
        # compute ceil(t / T)
        k = (t + T - 1) // T
        if k > k_req:
            k_req = k
    
    print(k_req)

if __name__ == "__main__":
    main()
```

The core of the implementation is the integer ceiling computation `(t + T - 1) // T`, which avoids floating point operations and ensures correctness for large values. The initialization to 2 is essential because even if all ratios suggest 1, the constraint disallows it.

## Worked Examples

Consider the sample-like input:

```
5 1000
998 244 353 1111 2333
```

We compute required multipliers:

| i | t_i | ceil(t_i / T) | k_req |
| --- | --- | --- | --- |
| 1 | 998 | 1 | 2 |
| 2 | 244 | 1 | 2 |
| 3 | 353 | 1 | 2 |
| 4 | 1111 | 2 | 2 |
| 5 | 2333 | 3 | 3 |

The final answer is 3, because the last program requires at least $3T = 3000$.

This trace shows that even though most programs are small relative to $T$, a single large value dominates the result.

Now consider a case where all programs are small:

```
3 100
10 20 30
```

| i | t_i | ceil(t_i / T) | k_req |
| --- | --- | --- | --- |
| 1 | 10 | 1 | 2 |
| 2 | 20 | 1 | 2 |
| 3 | 30 | 1 | 2 |

Even though all ratios are below 1, the constraint forces the answer to be 2.

This demonstrates that the lower bound $k \ge 2$ is independent of input data and must be enforced after all comparisons.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass over all program times, constant work per element |
| Space | $O(1)$ | Only a few integer variables are maintained |

The solution comfortably fits within constraints since $n \le 10^5$, and each operation is a constant-time integer computation.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    n, T = map(int, input().split())
    arr = list(map(int, input().split()))
    
    k_req = 2
    for t in arr:
        k_req = max(k_req, (t + T - 1) // T)
    
    return str(k_req)

# provided sample
assert solve("5 1000\n998 244 353 1111 2333\n") == "3"

# all small values, forces k=2
assert solve("3 100\n10 20 30\n") == "2"

# exact multiples
assert solve("3 10\n10 20 30\n") == "3"

# large single outlier
assert solve("4 1000\n1 2 3 1000000\n") == "1000"

# minimum case
assert solve("1 5\n1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small values | 2 | enforces lower bound k ≥ 2 |
| multiples | 3 | exact division correctness |
| outlier | 1000 | dominance of maximum constraint |
| single element | 2 | minimum boundary handling |

## Edge Cases

When all program times are much smaller than $T$, the computed ceiling is always 1. For example:

```
2 100
1 2
```

The algorithm computes $k = 1$ for both, but since initialization is $k\_req = 2$, the final output remains 2. The loop never overrides it, which correctly enforces the problem’s constraint.

When one program is extremely large:

```
2 10
1 100000
```

The computation proceeds as follows. First value gives $k = 1$, so $k\_req = 2$. Second value gives $k = 10000$, so $k\_req$ becomes 10000. This shows that a single constraint fully determines the answer, and previous values only serve as lower bounds.
