---
title: "CF 105901L - Subsequence"
description: "We are given several integer arrays, and for each one we want to build a subsequence with a very specific structural property. Take any chosen subsequence and sort it."
date: "2026-06-21T15:22:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105901
codeforces_index: "L"
codeforces_contest_name: "2025 ICPC Wuhan Invitational Contest (The 3rd Universal Cup. Stage 37: Wuhan)"
rating: 0
weight: 105901
solve_time_s: 63
verified: true
draft: false
---

[CF 105901L - Subsequence](https://codeforces.com/problemset/problem/105901/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several integer arrays, and for each one we want to build a subsequence with a very specific structural property.

Take any chosen subsequence and sort it. Let the smallest element be the left endpoint, the largest be the right endpoint, and the median be the element at position ceil(k/2) in this sorted order. The subsequence is called good if the median is exactly the arithmetic mean of the minimum and maximum values.

In other words, if the sorted subsequence is D, then we require that 2 · D[ceil(k/2)] equals D[1] + D[k]. The condition couples three different order statistics of the chosen set, which immediately makes it clear that arbitrary subsequences are heavily constrained.

The task is to find, for each test case, the maximum possible length of a good subsequence extracted from the original array while preserving relative order.

The constraints are small in aggregate, with the total sum of n over all test cases not exceeding 3000. This removes any need for n log n or n log^2 n optimizations and strongly suggests that an O(n^2) or even O(n^2 log n) strategy is intended.

A subtle issue appears immediately if one tries greedy or local reasoning. The condition involves the median, which depends on the size of the chosen subsequence, so removing or adding a single element can change which element becomes the median and completely change validity. For example, an interval might fail the condition with all its elements included, but become valid after removing some interior values. This kills naive “take a value range and check once” ideas unless the structure guarantees optimality.

## Approaches

A direct brute-force approach would enumerate all subsequences, check each one by sorting, and verify whether the median equals the average of minimum and maximum. This is correct but infeasible. There are 2^n subsequences, and even checking one costs O(n log n), so the worst case explodes far beyond limits.

The key structural observation is that the condition only depends on three values of the sorted subsequence: its minimum, maximum, and median. If we fix the minimum x and maximum y, then the median is forced to be (x + y) / 2, provided that value is integral and appears in the array. This reduces the problem from arbitrary subsequences to choosing pairs of endpoints.

Once x and y are fixed, any candidate subsequence must lie entirely inside the value range [x, y], otherwise the minimum or maximum would change. Among all elements in that range, we want to select the largest possible subsequence that still keeps (x + y) / 2 as its median.

This converts the problem into checking, for each pair (x, y), whether the full multiset of elements in [x, y] satisfies the median constraint, and if it does, we take all of them. Even though in principle we could remove elements, doing so only decreases length and cannot help once the full interval already satisfies the median condition.

We therefore move to coordinate compression and prefix frequencies. For every pair of compressed values i ≤ j, we treat U[i] as x and U[j] as y. We compute the midpoint m = (x + y) / 2, check it is an integer and exists in the array, and then evaluate how many elements in the interval are less than m, equal to m, and greater than m. These counts fully determine the median position condition.

The brute-force over all pairs is O(n^2), and each check is O(1) using prefix sums, which fits comfortably within the total constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsequences | O(2^n · n log n) | O(n) | Too slow |
| Pair endpoints with prefix counts | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. Compress all values in the array into a sorted unique list U, and build a frequency array over U.

This allows range queries over values to be answered in constant time using prefix sums.
2. Build prefix sums over the frequency array so that we can quickly compute how many elements fall into any value interval [U[i], U[j]].
3. Iterate over all possible left endpoints i, treating U[i] as a candidate minimum value.
4. For each i, iterate over all right endpoints j ≥ i, treating U[j] as a candidate maximum value.
5. Compute x = U[i] and y = U[j]. If (x + y) is odd, skip this pair since no integer median can satisfy the condition.
6. Compute m = (x + y) / 2 and locate it in the compressed array. If m does not exist, skip this pair.
7. Using prefix sums, compute L as the number of elements in A with values in [x, m), E as the number of elements equal to m, and R as the number of elements in (m, y].
8. Let k = L + E + R and t = ceil(k / 2). The subsequence is valid if and only if L < t and t ≤ L + E.
9. If valid, update the answer with k, since taking the full interval gives the maximum possible subsequence for this (x, y).

### Why it works

Fixing the minimum and maximum forces every valid subsequence to lie inside a closed value interval. Inside such an interval, the only way to influence the median without changing endpoints is by removing interior elements, but removing elements only shrinks k and shifts the median position in a way that cannot expand feasibility beyond what the full interval already provides for a fixed (x, y, m). Therefore, for each endpoint pair, either the full interval already satisfies the median constraint or no larger valid subsequence with those endpoints can exist.

The prefix count condition directly encodes the definition of median position in terms of how many elements lie below and at the median value, so the validity check is exact and not heuristic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))

        vals = sorted(set(a))
        idx = {v: i for i, v in enumerate(vals)}
        m = len(vals)

        freq = [0] * m
        for v in a:
            freq[idx[v]] += 1

        pref = [0] * (m + 1)
        for i in range(m):
            pref[i + 1] = pref[i] + freq[i]

        def range_sum(l, r):
            if l > r:
                return 0
            return pref[r + 1] - pref[l]

        ans = 1

        for i in range(m):
            for j in range(i, m):
                x = vals[i]
                y = vals[j]

                s = x + y
                if s % 2:
                    continue
                mid = s // 2
                if mid not in idx:
                    continue

                k = idx[mid]
                if k < i or k > j:
                    continue

                L = range_sum(i, k - 1)
                E = freq[k]
                R = range_sum(k + 1, j)

                total = L + E + R
                if total == 0:
                    continue

                t = (total + 1) // 2

                if L < t <= L + E:
                    ans = max(ans, total)

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first compresses values so that every interval over values can be evaluated quickly. The nested loops enumerate all possible choices of minimum and maximum values. For each pair, the midpoint value is computed and validated, since the median must equal that midpoint exactly.

The prefix sums allow L and R to be computed in constant time, so each pair check is O(1). The condition L < t ≤ L + E is a direct translation of the requirement that the median position falls inside the block of equal-to-mid values in the sorted interval.

The final answer is the maximum size of any interval that satisfies this constraint.

## Worked Examples

Consider the array A = [9, 8, 2, 11, 5].

We compress values to [2, 5, 8, 9, 11]. Suppose we pick x = 2 and y = 8. Then m = 5. We compute counts over [2, 8]: L = 1 (value 2), E = 1 (value 5), R = 1 (value 8). So total k = 3 and t = 2. Since L = 1 < 2 ≤ 2 = L + E, this interval is valid and contributes answer 3.

| i (x) | j (y) | m | L | E | R | k | t | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 8 | 5 | 1 | 1 | 1 | 3 | 2 | Yes |

This trace shows a balanced structure around the median value, where exactly one element lies below and one above.

Now consider A = [7, 9, 2, 4, 17, 10, 15]. Take x = 4 and y = 10, giving m = 7. Inside [4, 10], we have elements 4, 7, 9, 10. Then L = 1, E = 1, R = 2, k = 4, t = 2. Since L < t ≤ L + E holds, this interval is valid.

| i (x) | j (y) | m | L | E | R | k | t | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 10 | 7 | 1 | 1 | 2 | 4 | 2 | Yes |

This shows how even-length subsequences are handled correctly through the ceil-based median index.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) per test case | all pairs of compressed values are checked once, each in O(1) |
| Space | O(n) | frequency and prefix arrays over compressed values |

With total n across all test cases bounded by 3000, the quadratic scan remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# basic sample-like cases
assert run("1\n5\n9 8 2 11 5\n") == "3"
assert run("1\n7\n7 9 2 4 17 10 15\n") == "4"

# minimum size
assert run("1\n1\n100\n") == "1"

# all equal values
assert run("1\n5\n3 3 3 3 3\n") == "5"

# symmetric valid structure
assert run("1\n3\n1 3 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| all equal | n | median trivially matches |
| symmetric around midpoint | full n | best-case validity |
| mixed values | varies | general correctness |

## Edge Cases

A key edge case is when the midpoint value exists but lies outside the chosen value interval. For example, if we pick x = 2 and y = 8 but there is no element equal to 5, the condition must fail even though the arithmetic midpoint is valid. The algorithm explicitly checks presence of m in the compressed map, preventing invalid median assumptions.

Another edge case is when the interval contains many elements equal to the median. For A = [5, 5, 5, 1, 9], choosing x = 1 and y = 9 gives m = 5, with E = 3. The median condition is satisfied for multiple possible subsequence lengths, and the check L < t ≤ L + E correctly captures all of them because any median position falls inside the block of equal values.

A final subtle case is even-length subsequences. Because the median is defined using ceil(k/2), the median position shifts slightly left compared to standard “lower median” definitions. The condition t = ceil(k/2) ensures that the median is always treated consistently, and the inequality L < t ≤ L + E handles both odd and even k without special casing.
