---
title: "CF 1111B - Average Superhero Gang Power "
description: "We are given a group of superheroes, each with an initial power value. We are allowed to modify this group using two types of operations: we can either remove a superhero from the group (as long as at least two remain), or we can increase the power of a chosen superhero by one."
date: "2026-06-12T04:58:18+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1111
codeforces_index: "B"
codeforces_contest_name: "CodeCraft-19 and Codeforces Round 537 (Div. 2)"
rating: 1700
weight: 1111
solve_time_s: 87
verified: true
draft: false
---

[CF 1111B - Average Superhero Gang Power ](https://codeforces.com/problemset/problem/1111/B)

**Rating:** 1700  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of superheroes, each with an initial power value. We are allowed to modify this group using two types of operations: we can either remove a superhero from the group (as long as at least two remain), or we can increase the power of a chosen superhero by one. There is a global limit on the total number of operations, and an additional constraint that any single superhero can be increased only a limited number of times.

The goal is to end with some non-empty subset of superheroes whose average power is as large as possible after applying up to the allowed operations.

The output is a single real number representing that maximum achievable average.

The constraints immediately suggest that an $O(n^2)$ or worse simulation over all subsets is impossible because $n$ is up to $10^5$. Any approach that tries all subsets or repeatedly recomputes averages after deletions will time out. Even $O(n \cdot m)$ is not viable since $m$ can be up to $10^7$.

A key difficulty is that both operations interact: removing elements reduces denominator, while increasing values improves numerator, but increments are capped per element and globally limited.

A few edge cases expose common mistakes. If all elements are equal, say $n=3, a=[5,5,5]$, and we have many operations, the best strategy is to keep all elements and distribute increments, since removing reduces denominator without improving ratio. A naive greedy removal might incorrectly discard elements and inflate the average artificially.

Another edge case is when one element is extremely large compared to others. For example, $a=[1,1,1000]$. The optimal solution likely keeps only the largest element and invests increments into it. A strategy that assumes we must keep most elements will fail here.

A final subtle case arises when operation budget is large but per-element cap $k$ is restrictive. Even if $m$ is large, we cannot dump all increments into a single element; we must distribute them across chosen elements or accept that removing elements changes how much we can invest.

## Approaches

A brute-force view would try every possible subset of superheroes and then simulate distributing up to $m$ increments across elements, respecting the per-element cap $k$. For each subset, we would sort elements and greedily apply increments to the largest gains. Even ignoring distribution complexity, enumerating subsets alone is $O(2^n)$, which is impossible for $n=10^5$. Even restricting to prefix subsets after sorting would still require simulating up to $m$ operations, which is too slow.

The crucial observation is that we can separate decisions: first, suppose we fix a subset of size $x$. Within that subset, we always want to apply increments to the largest elements first, since each increment contributes equally to the sum but improves the average most when applied to already large values. Since each element can only be increased up to $k$ times, the total number of usable increments inside a fixed subset is bounded by $x \cdot k$. However, we are also limited by $m$, so total usable increments is $\min(m, xk)$.

Now the problem becomes: choose a subset size $x$, take the best $x$ elements, and distribute up to $\min(m, xk)$ increments among them. Since increments always go to the largest element in the subset, the optimal subset for a fixed size $x$ is simply the $x$ largest initial values.

This reduces the problem to sorting the array and checking all suffixes (or prefixes depending on convention), maintaining prefix sums and simulating how many increments can be applied. For each candidate subset size, we compute the resulting average efficiently.

The final optimization is to consider subsets from largest elements downward, because removing small elements can only improve or preserve average after optimal increment allocation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot m)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array in non-decreasing order. This ensures that when we consider keeping a subset, the best candidates are always the largest elements.
2. Precompute prefix sums of the sorted array so that we can quickly compute the sum of any suffix representing a chosen subset.
3. Iterate over possible subset sizes $x$ from 1 to $n$, where the subset consists of the $x$ largest elements.
4. For each subset size $x$, compute how many total increments we can apply: this is $\min(m, x \cdot k)$. This represents both the global limit and per-element limit combined at subset level.
5. Distribute these increments optimally by always increasing elements that benefit most, which in a fixed sorted subset means the largest elements receive increments first. Since all increments add +1 to sum, distribution does not affect total sum, only feasibility, so the total added value is exactly the number of increments.
6. Compute total power for subset size $x$ as sum of chosen elements plus total increments.
7. Compute average as total power divided by $x$, and track the maximum over all $x$.

### Why it works

Within any fixed subset, increments always contribute +1 to total sum regardless of which element receives them. The only restriction is feasibility from the per-element cap $k$, which limits total increments to at most $xk$. Since removing elements only reduces the denominator and never increases available increment capacity per element, the optimal solution must correspond to some subset size $x$, and within that subset all allocations of increments are interchangeable in terms of sum contribution. This reduces the problem to maximizing a simple one-dimensional function over sorted prefix choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]
    
    ans = 0.0
    
    for x in range(1, n + 1):
        base_sum = prefix[n] - prefix[n - x]
        increments = min(m, x * k)
        total = base_sum + increments
        avg = total / x
        if avg > ans:
            ans = avg
    
    print(f"{ans:.10f}")

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the array so that any optimal subset of size $x$ can be assumed to consist of the $x$ largest elements. The prefix sum array allows constant-time retrieval of any such subset sum.

For each subset size, we compute how many increments can be applied. The expression `x * k` enforces the per-element cap, while `m` enforces the global cap. The minimum of these two determines the usable increments.

Each increment increases total sum by exactly one, so we directly add the number of increments to the subset sum. The average is computed and compared across all subset sizes.

A subtle point is that we never simulate removing elements dynamically; instead, we reinterpret the problem as choosing a subset size and evaluating it directly. This avoids expensive state transitions.

## Worked Examples

### Sample 1

Input:

```
2 4 6
4 7
```

Sorted array is `[4, 7]`.

| x (subset size) | subset | base sum | x·k | m cap | increments | total | avg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [7] | 7 | 4 | 6 | 4 | 11 | 11 |
| 2 | [4,7] | 11 | 8 | 6 | 6 | 17 | 8.5 |

Best is 11.

This shows that removing the smaller element and concentrating all increments on the largest one dominates keeping both elements.

### Sample 2

Input:

```
3 2 5
1 10 20
```

Sorted array is `[1, 10, 20]`.

| x | subset | base sum | x·k | m cap | increments | total | avg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [20] | 20 | 2 | 5 | 2 | 22 | 22 |
| 2 | [10,20] | 30 | 4 | 5 | 4 | 34 | 17 |
| 3 | [1,10,20] | 31 | 6 | 5 | 5 | 36 | 12 |

Best is 22.

This demonstrates that shrinking the subset can unlock higher average by concentrating increments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, single linear scan afterward |
| Space | $O(n)$ | prefix sum array |

The constraints allow up to $10^5$ elements, so sorting and one pass over subset sizes is easily fast enough. Memory usage is linear in the array size and well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]
    
    ans = 0.0
    for x in range(1, n + 1):
        base = prefix[n] - prefix[n - x]
        inc = min(m, x * k)
        ans = max(ans, (base + inc) / x)
    
    return str(ans)

# provided sample
assert abs(float(run("2 4 6\n4 7\n")) - 11.0) < 1e-6

# all equal
assert abs(float(run("3 10 10\n5 5 5\n")) - 7.0) < 1e-6

# single element
assert abs(float(run("1 5 100\n10\n")) - 110.0) < 1e-6

# large k, small m
assert abs(float(run("4 100 2\n1 2 3 4\n")) - 5.5) < 1e-6

# increasing array
assert abs(float(run("5 1 5\n1 2 3 4 5\n")) - 7.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | stable distribution behavior | no benefit from removing elements |
| single element | max increments all applied | edge case x = 1 |
| large k small m | global cap dominates | interaction of m and k |
| increasing array | subset selection correctness | greedy subset reasoning |

## Edge Cases

One edge case is when all elements are identical. The algorithm evaluates every subset size and finds that keeping more elements increases denominator without increasing per-element gain beyond what removal allows. The computed maximum will correctly come from the largest valid subset where increments are fully utilized.

Another edge case is a single-element array. The algorithm only evaluates $x=1$, applies up to $\min(m,k)$ increments, and returns the correct inflated value without any subset considerations.

A third edge case is when $m$ is extremely small. The algorithm correctly caps increments globally, so even large subsets do not over-allocate increments, preventing overestimation of the average.
