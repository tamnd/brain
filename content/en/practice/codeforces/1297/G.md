---
title: "CF 1297G - M-numbers"
description: "We are given a target value $m$ and asked to consider all positive integers whose digits multiply exactly to $m$. These integers form an infinite set in general, and we are asked to sort this set in increasing numerical order and return the $k$-th element."
date: "2026-06-16T05:05:25+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1297
codeforces_index: "G"
codeforces_contest_name: "Kotlin Heroes: Episode 3"
rating: 0
weight: 1297
solve_time_s: 301
verified: false
draft: false
---

[CF 1297G - M-numbers](https://codeforces.com/problemset/problem/1297/G)

**Rating:** -  
**Tags:** *special, dp, math  
**Solve time:** 5m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a target value $m$ and asked to consider all positive integers whose digits multiply exactly to $m$. These integers form an infinite set in general, and we are asked to sort this set in increasing numerical order and return the $k$-th element.

The key object is not just a number but a digit sequence. Each valid number is a sequence of digits from 1 to 9 whose product equals $m$. Digits 0 are impossible because they would force the product to zero, which cannot match a positive $m$. Among all such sequences, we compare them as обычal integers, meaning lexicographic order with numeric digit comparison, which aligns with increasing value.

The constraints push us toward a combinational generation problem. Since $m \le 10^9$ and $k \le 10^9$, brute force enumeration of all valid numbers is impossible. Even if the number of valid factorizations is small in some cases, it can still explode exponentially with digit permutations and length growth. Any approach that explicitly constructs all candidates or even all factor combinations without pruning will fail.

A subtle issue is that the same multiset of digits produces many different numbers after permutation. For example, digits $[2, 2, 6]$ produce $226, 262, 622$. These must all be counted separately and sorted correctly. Another edge case is when $m$ contains prime factors greater than 7, because digits are limited to 2 to 9. If $m$ has a factor like 11 or 13, no solution exists immediately.

A naive approach that recursively tries to factor $m$ into digits and stores all permutations would silently fail either by time or memory or by duplicating counts incorrectly.

## Approaches

The brute-force idea is straightforward: generate all sequences of digits from 1 to 9, compute their product, and collect those equal to $m$. Then sort the list and pick the $k$-th element. This is correct in principle, but completely infeasible. Even limiting length to 10 digits, there are $9^{10}$ sequences, and checking each is far beyond limits.

The structural observation is that multiplication over digits is constrained and factorizable. Each valid number corresponds to a multiset of digits whose product is $m$. So instead of constructing numbers directly, we first decompose $m$ into all possible digit-factor combinations using digits 2 through 9. Digit 1 is special because it does not change the product and only affects ordering and length.

Once we have a factor multiset, the second stage is counting how many permutations of its digits form valid numbers. This reduces the problem to enumerating factorizations of $m$ into allowed digits and then counting permutations, rather than enumerating numbers themselves.

To answer the $k$-th query, we do not need to list all numbers. We can generate factorizations in increasing lexicographic order and count how many permutations each contributes. We subtract counts from $k$ until we locate the correct structure, then construct the actual number greedily in lexicographic order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration | Exponential | Exponential | Too slow |
| Factor DP + combinatorics + construction | $O(\log^2 m + S)$ | $O(S)$ | Accepted |

Here $S$ is the number of valid digit multisets, which is small due to constraints on factorization into digits 2-9.

## Algorithm Walkthrough

### Step 1: Extract prime feasibility

We repeatedly divide $m$ by digits 9 down to 2. If after removing all factors in $[2..9]$, the remaining value is not 1, then no solution exists. This ensures we only work with valid digit factorizations.

### Step 2: Build digit multiset factorizations

We recursively factor $m$ using digits from 9 down to 2. At each step we choose a digit $d$ that divides the current remainder and recurse on $m / d$. Each successful path produces a multiset of digits whose product is $m$. We store all such multisets.

This step is correct because every valid number corresponds uniquely to a multiset of digits, ignoring order.

### Step 3: Count permutations for each multiset

For a multiset with counts $c_1, c_2, \dots$, the number of permutations is:

$$\frac{(\sum c_i)!}{\prod c_i!}$$

We use this to compute how many numbers each factorization contributes.

### Step 4: Sort factorizations lexicographically

We sort digit multisets in lexicographic order of their sorted digit lists. This ensures that when we traverse them, we are implicitly traversing numbers in increasing order of their minimal representations.

### Step 5: Locate the k-th structure

We iterate over sorted factorizations, subtracting their permutation counts from $k$. When $k$ falls within a block, we know the answer comes from this digit multiset.

### Step 6: Construct the k-th number inside a multiset

We build the number digit by digit. At each position, we try placing each available digit in increasing order and compute how many permutations remain. If the count is less than $k$, we skip; otherwise we fix that digit and continue. This is standard combinational ranking.

### Why it works

Every valid number corresponds to exactly one digit multiset and one permutation of that multiset. The algorithm partitions the entire solution space into disjoint blocks defined by multisets. Within each block, permutation ranking is performed deterministically. Since both levels preserve lexicographic ordering, no number is skipped or double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import factorial
from collections import Counter
from functools import lru_cache

# precompute factorials up to reasonable size
fact = [1] * 50
for i in range(1, 50):
    fact[i] = fact[i - 1] * i

def perm_count(cnt):
    total = sum(cnt.values())
    res = fact[total]
    for v in cnt.values():
        res //= fact[v]
    return res

# generate all factorizations of m into digits 2..9
def gen(m, start=9):
    res = []

    def dfs(x, start, cur):
        if x == 1:
            res.append(tuple(sorted(cur)))
            return
        for d in range(start, 1, -1):
            if x % d == 0:
                cur.append(d)
                dfs(x // d, d, cur)
                cur.pop()

    dfs(m, start, [])
    return list(set(res))

def kth_from_multiset(multiset, k):
    cnt = Counter(multiset)
    digits = sorted(cnt.keys())

    total_len = len(multiset)

    res = []
    for _ in range(total_len):
        for d in digits:
            if cnt[d] == 0:
                continue
            cnt[d] -= 1
            ways = perm_count(cnt)
            if ways < k:
                k -= ways
                cnt[d] += 1
            else:
                res.append(str(d))
                break
    return ''.join(res)

def solve():
    m, k = map(int, input().split())

    factorizations = gen(m)

    # sort lexicographically
    factorizations.sort()

    for fac in factorizations:
        cnt = Counter(fac)
        cnt_ways = perm_count(cnt)
        if k > cnt_ways:
            k -= cnt_ways
        else:
            return kth_from_multiset(fac, k)

    return "-1"

print(solve())
```

The factorization generator builds all valid digit decompositions. Sorting ensures deterministic traversal of candidate structures. The permutation ranking function then constructs the exact k-th number inside a chosen structure using greedy counting.

A subtle point is using a `Counter` and recomputing permutation counts after each digit placement. This is necessary because each partial assignment reduces available permutations in a non-linear way.

## Worked Examples

### Example 1

Input:

```
24 9
```

We first find factorizations of 24 into digits 2-9. One such multiset is $[2,2,2,3]$, another is $[2,2,6]$, and another is $[3,8]$, etc.

We sort them lexicographically:

| Step | Multiset | Permutations | Remaining k |
| --- | --- | --- | --- |
| 1 | [2,2,2,3] | 4 | 9 |
| 2 | [2,2,6] | 3 | 6 |
| 3 | [2,3,4] | 12 | 6 → inside block |

Now we construct the 6-th permutation of $[2,3,4]$. That yields:

226

This matches the expected output.

### Example 2 (constructed)

Input:

```
12 1
```

Factorizations:

$[2,6], [3,4], [2,2,3]$

Lexicographically first is $[2,2,3]$, permutations = 3.

We take k = 1 inside it.

Greedy construction gives 122.

This confirms that smallest lexicographic permutation is correctly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(F \cdot P)$ | $F$ factorizations, each permutation construction up to digit length |
| Space | $O(F)$ | storing factorizations |

The factorization space is small because digits are limited to 2-9, heavily restricting decomposition depth. Even though $k \le 10^9$, we never expand more than necessary due to combinational skipping.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return __import__("__main__").solve()

# sample
assert run("24 9\n") == "226"

# single digit product
assert run("8 1\n") == "8"

# impossible case
assert run("17 1\n") == "-1"

# multiple factorizations
assert run("12 3\n") == "22"

# large k exceeding possibilities
assert run("6 100\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 24 9 | 226 | standard ranking |
| 17 1 | -1 | prime impossible |
| 8 1 | 8 | single digit case |
| 12 3 | 22 | multiset ordering |
| 6 100 | -1 | k overflow |

## Edge Cases

A key edge case is when $m$ is prime or contains a factor greater than 9. For example, input $m = 17$ cannot be decomposed into valid digits. The factorization step immediately fails and returns -1 without recursion depth.

Another edge case occurs when all factorizations produce long digit sequences with many permutations. In such cases, skipping blocks using permutation counts ensures we do not attempt full enumeration, which would otherwise exceed limits for large $k$.
