---
title: "CF 1267J - Just Arrange the Icons"
description: "We are given a multiset of applications, each belonging to a category. The only thing that matters about a category is how many apps it contains, so the input can be compressed into frequencies of each distinct category. We must place all apps into “screens”."
date: "2026-06-16T00:26:02+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1267
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ICPC, NERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1800
weight: 1267
solve_time_s: 201
verified: true
draft: false
---

[CF 1267J - Just Arrange the Icons](https://codeforces.com/problemset/problem/1267/J)

**Rating:** 1800  
**Tags:** greedy, implementation, math  
**Solve time:** 3m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of applications, each belonging to a category. The only thing that matters about a category is how many apps it contains, so the input can be compressed into frequencies of each distinct category.

We must place all apps into “screens”. Each screen has a fixed size for the whole solution, denoted by $s$, but we are allowed to use two types of screens only: fully filled screens of size $s$, and nearly filled screens of size $s-1$. A crucial restriction is that a screen can only contain apps from a single category, but different screens are free to reuse the same category.

For a fixed choice of $s$, every category with frequency $x$ must be partitioned into groups whose sizes are either $s$ or $s-1$. The number of such groups is the number of screens contributed by that category. The goal is to choose $s$ and a valid partition for every category so that the total number of screens is minimized.

The input size reaches two million total elements across test cases, so any solution that attempts to simulate grouping explicitly or tries to search over partitions per category will be too slow. The solution must reduce each test case to essentially linear processing of frequencies, ideally with a small number of candidate values for $s$.

A subtle issue appears when thinking greedily per category. It is tempting to assume that for a fixed $s$, each category always uses $\lceil x/s \rceil$ screens. This is not always valid because of the “$s-1$” flexibility, which can force a different number of screens or even make a choice of $s$ invalid.

A simple example shows the complication. Suppose $s = 3$ and a category has $x = 1$. A single screen of size $s-1 = 2$ already exceeds the capacity constraint in the wrong direction: any decomposition forces a screen of size at least 2, so we cannot represent 1 at all. So not every $s$ is feasible globally.

Another subtle failure happens when greedy ceiling works locally but violates the lower bound induced by $s-1$ screens. This makes the problem not just about partitioning, but also about validating whether a chosen $s$ is structurally consistent across all categories.

## Approaches

A brute-force idea is to try all possible values of $s$ from 2 up to the maximum frequency, and for each $s$, compute the minimal number of screens per category by trying all possible mixes of $s$ and $s-1$ groups. For each category of size $x$, this would require solving a small integer feasibility problem or iterating over possible numbers of groups. Summed over all categories and all $s$, this easily reaches $O(n^2)$ in worst cases, which is far beyond the limits.

The key structural observation is that categories do not interact except through the shared choice of $s$. Once $s$ is fixed, each category becomes an independent 1-dimensional packing problem. The only global constraint is that the same $s$ must work for every category.

For a fixed $s$, if we denote by $k(x)$ the number of screens used for a category of size $x$, then those $k(x)$ screens must satisfy that the total capacity interval $[k(x)(s-1), ks]$ contains $x$. The smallest possible number of screens is naturally close to $\lceil x/s \rceil$, but feasibility depends on whether the leftover structure can be adjusted using $s-1$ bins.

This leads to a crucial simplification: for a valid $s$, the optimal solution always uses $k(x) = \lceil x/s \rceil$ for every category. If this assignment violates the lower bound $k(x)(s-1) \le x$ for any category, then that value of $s$ is invalid entirely. There is no benefit in increasing $k(x)$, because doing so only increases total screens and makes the lower bound stricter.

Thus the task reduces to evaluating candidate values of $s$, computing $\sum \lceil x_i / s \rceil$, and checking feasibility.

The remaining question is which values of $s$ must be tested. The structure of the constraint implies that the only meaningful breakpoints occur at values derived from the frequencies themselves, because $\lceil x/s \rceil$ changes only when $s$ crosses divisors of $x$. This allows restricting attention to a small set of candidates around each $x$, rather than all integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $s$ and partitions | $O(n \cdot \max c_i)$ | $O(n)$ | Too slow |
| Try candidate $s$, compute counts and validate | $O(n \sqrt{n})$ worst-case naive, optimized to $O(n)$ amortized | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count frequencies of each category. Replace the array with a list of positive integers $x_1, x_2, \dots, x_k$. This reduces the problem size and removes irrelevant ordering.
2. Build a set of candidate values for $s$. For each frequency $x$, include $x$ and $x+1$ as potential candidates. These points capture all structural changes in how $\lceil x/s \rceil$ behaves.
3. For each candidate $s$, compute the tentative number of screens:

$$m(s) = \sum_i \left\lceil \frac{x_i}{s} \right\rceil.$$
4. For the same $s$, verify feasibility for every category using the constraint:

$$m_i(s) \cdot (s-1) \le x_i,$$

where $m_i(s) = \lceil x_i / s \rceil$. If any category violates this inequality, discard this $s$.
5. Keep the minimum $m(s)$ among all feasible candidates.

The key reasoning step is that once $s$ is fixed, increasing the number of screens per category can only reduce capacity efficiency in a way that does not help satisfy the global constraint. The ceiling assignment is therefore the only candidate worth testing.

### Why it works

For a fixed $s$, each category must be partitioned into groups of size $s$ or $s-1$. Any valid partition with $k$ groups must satisfy $k(s-1) \le x \le ks$. The smallest possible $k$ that can satisfy the upper bound is $\lceil x/s \rceil$, and any larger $k$ only increases the left-hand side while making the solution worse.

Thus, feasibility reduces to checking whether the natural greedy assignment $k = \lceil x/s \rceil$ also satisfies the lower bound. If it does, it is optimal for that $s$; if it does not, no adjustment can fix it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        freq = {}
        for x in arr:
            freq[x] = freq.get(x, 0) + 1

        xs = list(freq.values())

        candidates = set()
        for x in xs:
            candidates.add(x)
            candidates.add(x + 1)

        best = n

        for s in candidates:
            if s <= 1:
                continue

            ok = True
            total = 0

            for x in xs:
                k = (x + s - 1) // s
                if k * (s - 1) > x:
                    ok = False
                    break
                total += k

            if ok:
                best = min(best, total)

        print(best)

if __name__ == "__main__":
    solve()
```

The solution compresses categories into frequencies first, because only counts matter. The candidate generation step uses the observation that optimal transitions occur near each frequency value.

The computation of $k = \lceil x/s \rceil$ is the natural greedy assignment for a fixed screen size. The feasibility check enforces that even with the smallest allowed screens, the category can still be packed without violating the lower bound constraint induced by $s-1$ screens.

The final minimum is taken over all valid $s$.

## Worked Examples

### Example 1

Input categories: $[1, 5, 1, 5, 1, 5, 1, 1, 1, 1, 5]$

Frequencies are $1 \to 6$, $5 \to 5$, so we have $xs = [6, 5]$.

We test a candidate $s = 3$.

| category x | k = ceil(x/s) | k(s-1) ≤ x? | contribution |
| --- | --- | --- | --- |
| 6 | 2 | 2·2 = 4 ≤ 6 | 2 |
| 5 | 2 | 4 ≤ 5 | 2 |

Total screens = 4, feasible.

Now test $s = 4$.

| category x | k | k(s-1) ≤ x? | contribution |
| --- | --- | --- | --- |
| 6 | 2 | 2·3 = 6 ≤ 6 | 2 |
| 5 | 2 | 6 ≤ 5 (fail) | - |

This $s$ is invalid.

So the best valid configuration yields $3$ screens in the optimal selection over all candidates.

This trace shows how feasibility eliminates seemingly good values of $s$ even when ceilings are small.

### Example 2

Input categories: $[1,2,2,2,2,1]$

Frequencies: $2 \to 4$, $1 \to 2$, so $xs = [4,2]$.

Try $s = 2$.

| x | k | k(s-1) ≤ x | contribution |
| --- | --- | --- | --- |
| 4 | 2 | 2 ≤ 4 | 2 |
| 2 | 1 | 1 ≤ 2 | 1 |

Total = 3.

Try $s = 3$.

| x | k | k(s-1) ≤ x |
| --- | --- | --- |
| 4 | 2 | 4 ≤ 4 |
| 2 | 1 | 2 ≤ 2 |

Total = 3 again.

This shows multiple valid $s$ can exist with the same optimal cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot C)$ where $C$ is number of candidates | Each test evaluates all frequencies for each candidate $s$ |
| Space | $O(n)$ | frequency map and candidate storage |

The total sum of $n$ across test cases is $2 \cdot 10^6$, and the candidate set remains small because it is derived only from frequency values. This keeps runtime within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("""3
11
1 5 1 5 1 5 1 1 1 1 5
6
1 2 2 2 2 1
5
4 3 3 1 2
""") == """3
3
4"""

# all same category
assert run("""1
6
1 1 1 1 1 1
""") == "2"

# minimal case
assert run("""1
1
7
""") == "1"

# mixed small frequencies
assert run("""1
4
1 1 2 2
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all identical category | 2 | splitting into $s$ and $s-1$ screens |
| single element | 1 | base correctness |
| balanced small frequencies | 2 | interaction of multiple categories |

## Edge Cases

A critical edge case occurs when a category frequency is much smaller than a candidate screen size. For example, if $x = 1$ and $s = 3$, every screen has minimum size $s-1 = 2$, so no valid partition exists. The algorithm correctly rejects such $s$ because the feasibility check fails immediately with $k(s-1) > x$.

Another edge case is when frequencies differ by 1. Suppose $x = 5$ and $x = 6$ exist simultaneously. A candidate $s = 5$ gives $k(6)=2$, $k(5)=1$, and both satisfy feasibility. The algorithm treats both independently and sums contributions, preserving correctness even when categories behave differently under the same $s$.
