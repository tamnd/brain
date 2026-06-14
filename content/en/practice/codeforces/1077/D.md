---
title: "CF 1077D - Cutting Out"
description: "We are given a multiset of integers, and we want to construct a pattern array of fixed length $k$. Once we choose this pattern, we repeatedly try to “extract” it from the original multiset: each extraction consumes one occurrence of every value in the pattern, and after each…"
date: "2026-06-15T06:40:46+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1077
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 521 (Div. 3)"
rating: 1600
weight: 1077
solve_time_s: 140
verified: true
draft: false
---

[CF 1077D - Cutting Out](https://codeforces.com/problemset/problem/1077/D)

**Rating:** 1600  
**Tags:** binary search, sortings  
**Solve time:** 2m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of integers, and we want to construct a pattern array of fixed length $k$. Once we choose this pattern, we repeatedly try to “extract” it from the original multiset: each extraction consumes one occurrence of every value in the pattern, and after each full extraction the consumed elements disappear permanently from the pool.

The goal is to choose the pattern so that the number of complete extractions is as large as possible. We are free to permute the pattern and to repeat values inside it, but every copy must be fully supported by the available frequencies in the original array.

The key viewpoint is that the answer depends only on how many times each value appears in the final pattern, because order is irrelevant for feasibility. If a value appears $x$ times in the pattern, then each full extraction consumes $x$ copies of that value from the array.

The constraints allow up to $2 \cdot 10^5$ elements, so any solution that tries all candidate patterns or simulates extraction for many choices would be too slow. Anything quadratic in $n$ or dependent on enumerating all subsets of values is immediately ruled out.

A subtle edge case arises when frequencies are extremely skewed. If one number appears very often and others are rare, a naive greedy selection might overuse the frequent number in the pattern, blocking the possibility of balancing the pattern across $k$ positions. Another tricky case is when $k$ is large relative to the number of distinct elements, forcing repetitions that must be carefully controlled by frequency constraints rather than intuition.

## Approaches

A brute-force approach would attempt to build every possible multiset of size $k$ from the distinct values in $s$, then simulate how many times it can be extracted. Even if we restrict ourselves to only values present in $s$, the number of possible patterns grows exponentially in $k$, and for each candidate we would need to compute the limiting frequency ratio, which costs $O(n)$. This quickly becomes infeasible.

The central observation is that if we fix a candidate pattern, the number of times it can be extracted is determined purely by frequencies: if a value $v$ appears $c_v$ times in the pattern, and appears $f_v$ times in the array, then we can extract the pattern at most $\min_v \lfloor f_v / c_v \rfloor$ times.

This suggests a reverse viewpoint: instead of choosing a pattern and computing its score, we decide how many total “slots” each value should occupy across all extracted copies. If we aim for $x$ copies, then we need a pattern whose total demand per value does not exceed available frequencies. That is, the total usage of each value across all copies must be at most $f_v$, so each copy can use at most $\lfloor f_v / x \rfloor$ occurrences of value $v$.

This leads to a key transformation: for a fixed number of copies $x$, we can greedily construct the best possible pattern by taking up to $\lfloor f_v / x \rfloor$ occurrences of each value, up to total size $k$. If we can reach size $k$, then $x$ copies are feasible.

Now the problem becomes finding the maximum $x$. Since feasibility is monotonic in $x$ (if we can extract $x$ copies, we can extract fewer), we can binary search $x$. For each candidate $x$, we test feasibility and construct a pattern greedily.

Finally, once the maximum $x$ is known, we output any valid pattern constructed under that constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Binary search + greedy construction | $O(n \log n)$ | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each value in the array. This gives the maximum supply constraint for every possible pattern element.
2. Define a function that checks whether we can build a pattern supporting at least $x$ full extractions. For each value $v$, compute how many times it can appear in a single copy: $\lfloor f_v / x \rfloor$. This is the maximum per-copy allowance without exhausting the value over $x$ repetitions.
3. Sum all these per-value capacities. If the total is less than $k$, then even the most generous pattern cannot reach length $k$, so $x$ copies are impossible.
4. If feasible, construct the pattern by iterating through values and adding each value up to $\lfloor f_v / x \rfloor$ times until the pattern reaches length $k$.
5. Use binary search on $x$ between 1 and $n$, repeatedly testing feasibility and adjusting bounds.
6. After finding the maximum feasible $x$, rebuild the final pattern using the same greedy construction.

The reason this works is that for a fixed number of copies $x$, the best possible pattern is always obtained by fully saturating each value up to its per-copy limit. Any deviation would either reduce total size or waste available frequency capacity. The binary search ensures we find the largest $x$ that still allows constructing a full-length pattern of size $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(x, freq, k):
    total = 0
    for v in freq:
        total += freq[v] // x
        if total >= k:
            return True
    return total >= k

def build(x, freq, k):
    res = []
    for v in freq:
        cnt = freq[v] // x
        take = min(cnt, k - len(res))
        res.extend([v] * take)
        if len(res) == k:
            break
    return res

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    freq = {}
    for v in arr:
        freq[v] = freq.get(v, 0) + 1

    lo, hi = 1, n
    best = 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, freq, k):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1

    ans = build(best, freq, k)
    print(*ans)

if __name__ == "__main__":
    solve()
```

The implementation separates feasibility checking from reconstruction. The `can` function computes whether a given number of copies is achievable without constructing the actual pattern, which keeps binary search efficient. The `build` function then reconstructs the pattern greedily using the same logic, ensuring consistency with the feasibility test.

A subtle detail is that reconstruction must respect the exact same per-value limits used in `can`. Any mismatch between the two would lead to incorrect patterns even if the feasibility test is correct.

## Worked Examples

Consider the input:

```
7 3
1 2 3 2 4 3 1
```

We first compute frequencies:

| value | freq |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |
| 4 | 1 |

We test feasibility. For $x = 2$, each value contributes $\lfloor f_v / 2 \rfloor$:

| value | contribution |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 0 |

Total is 3, which is enough for $k = 3$, so 2 copies are possible. For $x = 3$, contributions become all zero except impossible to reach 3 elements, so it fails. Thus best $x = 2$.

Reconstruction picks one of each of 1, 2, 3, giving `[1, 2, 3]`.

Now consider a skewed case:

```
6 4
1 1 1 1 2 2
```

Frequencies:

| value | freq |
| --- | --- |
| 1 | 4 |
| 2 | 2 |

Try $x = 2$: contributions are 2 for value 1 and 1 for value 2, total 3, insufficient for $k = 4$. So only $x = 1$ works. We can take up to 4 ones and 2 twos, but only need 4 elements, so a valid pattern is `[1, 1, 1, 2]` or similar.

This trace shows that the algorithm naturally balances frequent and rare elements without explicitly reasoning about ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Binary search over $x$, each check scans frequency map |
| Space | $O(n)$ | Frequency dictionary and output storage |

The complexity fits comfortably within limits since $n \le 2 \cdot 10^5$, and about 18-20 feasibility checks are performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    freq = {}
    for v in arr:
        freq[v] = freq.get(v, 0) + 1

    def can(x):
        total = 0
        for v in freq:
            total += freq[v] // x
        return total >= k

    lo, hi = 1, n
    best = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1

    res = []
    for v in freq:
        cnt = freq[v] // best
        res.extend([v] * min(cnt, k - len(res)))
        if len(res) == k:
            break

    return " ".join(map(str, res))

# provided sample
assert run("7 3\n1 2 3 2 4 3 1\n") in {"1 2 3", "1 3 2", "2 1 3"}

# all equal
assert len(run("5 2\n1 1 1 1 1\n").split()) == 2

# k = n
assert len(run("4 4\n1 2 3 4\n").split()) == 4

# skewed frequencies
assert len(run("6 3\n1 1 1 2 2 3\n").split()) == 3

# minimum case
assert run("1 1\n7\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | size k output | high repetition stability |
| k = n | full reconstruction | boundary saturation |
| skewed frequencies | valid length k | balancing behavior |
| single element | itself | minimal edge case |

## Edge Cases

For an input where all elements are identical, such as `5 3` with `[7 7 7 7 7]`, the algorithm computes that each copy can contain only one value, and binary search finds that at most $\lfloor 5/3 \rfloor = 1$ full extraction is possible. Reconstruction simply outputs any three 7s, which matches feasibility constraints.

For cases where $k = n$, the algorithm effectively reduces to selecting a full multiset without repetition constraints, and binary search still returns a valid maximum number of copies, often 1. The reconstruction fills the entire array up to $n$, which trivially satisfies correctness.

For highly imbalanced inputs like `[1,1,1,1,2]` with large $k$, the feasibility check ensures that the rare element does not get over-allocated, preventing over-optimistic patterns that would fail during extraction.
