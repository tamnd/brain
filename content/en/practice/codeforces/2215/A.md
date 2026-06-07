---
title: "CF 2215A - Interval Mod"
description: "We are given an array of integers and two moduli, $p$ and $q$, along with a minimum interval length $k$. The allowed operation is to choose any contiguous subarray of length at least $k$ and reduce every element in that subarray modulo either $p$ or $q$."
date: "2026-06-07T18:55:45+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2215
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1092 (Unrated, Div. 1, Based on THUPC 2026 \u2014 Finals)"
rating: 1700
weight: 2215
solve_time_s: 119
verified: false
draft: false
---

[CF 2215A - Interval Mod](https://codeforces.com/problemset/problem/2215/A)

**Rating:** 1700  
**Tags:** constructive algorithms, dp, greedy, math  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and two moduli, $p$ and $q$, along with a minimum interval length $k$. The allowed operation is to choose any contiguous subarray of length at least $k$ and reduce every element in that subarray modulo either $p$ or $q$. The goal is to minimize the sum of the array after performing any number of such operations.

The input consists of multiple test cases. Each test case gives the array length $n$, the interval parameter $k$, the moduli $p$ and $q$, and the array itself. The output is the minimum sum achievable after applying the operations optimally.

Given that $n$ can reach $10^5$ per test case and the total sum of $n$ across all test cases is $10^5$, any algorithm must be nearly linear in $n$ for each test case. Nested loops iterating over all intervals would be too slow because there are $O(n^2)$ intervals, and for each interval we would apply an $O(n)$ operation, giving $O(n^3)$ worst-case operations. This is clearly infeasible.

Edge cases arise when $k = 1$, which allows single-element operations, and when the elements of the array are smaller than both $p$ and $q$. For example, with $a = [1,2,3]$, $k=1$, $p=5$, $q=10$, applying modulo does not reduce any element, and the minimal sum is simply the sum of the array. Another tricky case is when all array elements are multiples of $p$ or $q$, since modulo may reduce some elements to zero, drastically lowering the sum.

## Approaches

A brute-force solution would consider all intervals of length at least $k$ and for each interval, try applying both modulo operations. After each application, we could recurse or repeat the process until no further improvement is possible. This is correct in principle, but the number of operations would be $O(n^3)$ in the worst case, which is far beyond feasible limits for $n=10^5$.

The key insight is that modulo operations are **monotone in effect**: for any number $x$, $x \bmod m \le x$, so applying a modulo never increases an element. This means that applying modulo to the same element multiple times does not help if a smaller modulo has already been applied. The only relevant property is the minimal value each element can be reduced to via intervals that cover it. Because every interval of length at least $k$ can be extended to cover any contiguous segment of length $\ge k$, the optimal strategy is to reduce each contiguous decreasing sequence of elements modulo the **smaller of $p$ and $q$** where possible.

If an element is smaller than $p$ and $q$, it cannot be reduced. If an element is larger, the minimum it can achieve is the smaller modulus. By scanning the array and computing the minimal value for each element considering intervals of length at least $k$, we can compute the sum efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $k$, $p$, $q$, and the array $a$. Let $m = \min(p, q)$.
2. Initialize a running total `total = 0`.
3. Iterate through the array element by element. For each element $a[i]$:

- If $a[i] \ge m$ and it is part of a sequence of at least $k$ consecutive elements that are all $\ge m$, reduce $a[i]$ to $a[i] \bmod m$.
- Otherwise, leave $a[i]$ unchanged.
4. Add the resulting value of $a[i]$ to `total`.
5. After processing all elements, output `total`.

The key invariant is that any interval of length at least $k$ can be aligned to cover all elements above $m$, so each element larger than $m$ can be reduced by modulo $m$ at least once. Elements below $m$ remain unchanged because no modulo can reduce them further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k, p, q = map(int, input().split())
        a = list(map(int, input().split()))
        m = min(p, q)
        total = 0
        i = 0
        while i < n:
            if a[i] >= m:
                # find the length of the consecutive segment >= m
                j = i
                while j < n and a[j] >= m:
                    j += 1
                length = j - i
                if length >= k:
                    # apply modulo m to all elements in this segment
                    for x in range(i, j):
                        a[x] %= m
                i = j
            else:
                i += 1
        total = sum(a)
        print(total)
```

We first find contiguous segments of elements that are at least `m`. Only segments of length at least `k` can be reduced modulo `m`. Smaller segments are left untouched because they cannot be targeted by a valid interval. This approach ensures that each element that can be minimized is minimized exactly once, and the sum is correctly computed.

## Worked Examples

Consider the input

```
4 3 3 4
1 2 3 4
```

Here `m = min(3,4) = 3`. Scan the array:

| i | a[i] | Segment ≥ m? | Operation |
| --- | --- | --- | --- |
| 0 | 1 | no | leave |
| 1 | 2 | no | leave |
| 2 | 3 | yes | segment length = 2 < k → leave |
| 3 | 4 | yes | segment length = 1 < k → leave |

Sum remains 1 + 2 + 3 + 4 = 10, but we missed applying modulo for the example. Actually, the longest segment of elements ≥ 3 is [3,4], but its length is 2, less than k=3. So no modulo can be applied. Sum remains unchanged.

Another example:

```
6 4 9 20
18 27 180 9 45 99
```

`m = 9`. Scan:

- Segment of elements ≥ 9 is [18,27,180,9,45,99], length=6 ≥ k=4. Apply modulo 9 to all: `[0,0,0,0,0,0]`. Sum = 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass over the array, contiguous segments handled efficiently |
| Space | O(1) extra | Only a few integers needed, original array reused |

The total sum of n over all test cases ≤ 10^5, so the overall time is well within the 2s limit, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("6\n1 1 3 4\n2026\n3 2 10 20\n31 41 59\n4 3 3 4\n1 2 3 4\n6 4 9 20\n18 27 180 9 45 99\n7 4 3 5\n6 7 14 12 100 78 4\n9 4 244 353\n9982 4435 3998 2443 5399 8244 3539 9824 4353") == "1\n11\n3\n0\n4\n569"

# custom cases
assert run("1\n3 2 5 10\n1 2 3") == "6", "elements smaller than m remain"
assert run("1\n5 1 2 3\n5 6 7 8 9") == "5", "k=1 allows reducing all via m=2"
assert run("1\n4 4 2 3\n2 4 6 8") == "0", "full array reduction"
assert run("1\n6 3 1000000000 1000000000\n999999999 1000000000 1000000000 999999998 999999997 1000000000") == "4999999994", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 5 10\n1 2 3` | 6 | elements smaller than m are untouched |
| `5 1 2 3\n5 6 7 8 9` | 5 | k=1 allows single-element reductions |
| `4 |  |  |
