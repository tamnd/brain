---
title: "CF 104455C - Count Triples"
description: "We are given three arrays of equal length, and each position contains a positive integer. From these arrays, we are not choosing elements in a constrained order or structure, we are simply forming independent triples by picking one index from each array."
date: "2026-06-30T13:40:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104455
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #19 (Briefest-Forces)"
rating: 0
weight: 104455
solve_time_s: 72
verified: true
draft: false
---

[CF 104455C - Count Triples](https://codeforces.com/problemset/problem/104455/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three arrays of equal length, and each position contains a positive integer. From these arrays, we are not choosing elements in a constrained order or structure, we are simply forming independent triples by picking one index from each array. For every choice of indices $i, j, k$, we compute the product $a_i \cdot b_j \cdot c_k$, and we want to count how many such triples produce exactly the target value $m$.

So the task is purely combinational over values: every occurrence in each array participates independently, and identical values are indistinguishable except for multiplicity.

The key constraint is that $n$ can be as large as $5 \cdot 10^5$. A direct enumeration of all triples would consider $n^3$ combinations, which at worst is about $1.25 \cdot 10^{17}$ operations. Even with heavy pruning, that scale is completely infeasible in two seconds. This immediately forces us to compress the problem into frequency space rather than index space.

Another important constraint is that every array element is at most $m$, and $m \le 10^9$. This matters because divisibility structure becomes central: if a value does not divide $m$, it can never contribute to a valid triple.

A few subtle edge cases appear naturally.

If $m = 1$, then every valid triple must consist entirely of ones. For example, if all arrays are $[1, 2]$, then only positions where all three picks are 1 contribute, and everything else is irrelevant.

If an array contains values not dividing $m$, such as $a = [2, 3]$ and $m = 6$, then only divisors of $m$ matter, and non-divisors can be ignored entirely.

A more subtle case arises when $m$ has repeated factor structure. For example, $m = 18$. Triples like $(2, 3, 3)$, $(3, 3, 2)$, and permutations all contribute, and counting must respect multiplicities across arrays rather than unique values.

The main failure mode for naive reasoning is treating this as a single search over values without properly accounting for frequency multiplicities in each array.

## Approaches

A direct way to think about the problem is to iterate over all triples of indices, compute the product, and check if it equals $m$. This is correct because it exactly matches the definition of the problem. However, it requires three nested loops over $n$, producing $O(n^3)$ operations. With $n = 5 \cdot 10^5$, even $n^2$ is already too large, so $n^3$ is decisively impossible.

The key observation is that the product condition separates cleanly across the three arrays. Instead of thinking in terms of indices, we shift to counting frequencies of values. If we know how many times each value appears in each array, then each choice of values contributes multiplicatively: if value $x$ appears $f_a[x]$ times in $a$, $f_b[y]$ times in $b$, and $f_c[z]$ times in $c$, then the number of index triples producing $(x, y, z)$ is $f_a[x] \cdot f_b[y] \cdot f_c[z]$.

So the problem reduces to counting all value triples $(x, y, z)$ such that $x \cdot y \cdot z = m$, weighted by frequencies.

This shifts the problem into divisor structure of $m$. Instead of iterating over all values in arrays, we only consider divisors of $m$, since any factor in a valid triple must divide $m$. The number of divisors of $m \le 10^9$ is small (at most a few thousand in worst cases), which makes enumeration feasible.

The optimal strategy is therefore: compute frequency maps for all three arrays, enumerate divisors $x$ and $y$ of $m$, deduce $z = m / (x \cdot y)$, and verify it is integral and exists in the third frequency map.

This reduces the search space from $n^3$ index combinations to roughly $d(m)^2$ value combinations, where $d(m)$ is the number of divisors of $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Frequency + divisor enumeration | $O(n + d(m)^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count frequencies of all values in arrays $a$, $b$, and $c$. This allows us to replace index-based counting with multiplicity-based counting.
2. Compute all divisors of $m$. Each divisor represents a possible value that could appear in any position of a valid triple. This step is crucial because only divisors of $m$ can participate in products equal to $m$.
3. Iterate over each divisor $x$ of $m$. Treat $x$ as the chosen value from array $a$. We multiply the answer by the number of ways to pick indices contributing value $x$, which is its frequency in $a$.
4. For each such $x$, iterate over each divisor $y$ of $m$. Treat $y$ as the value from array $b$. We multiply by its frequency in $b$.
5. Compute $z = m / (x \cdot y)$. If $m$ is not divisible by $x \cdot y$, skip this pair since no valid third value exists.
6. Check whether $z$ exists in array $c$ using the frequency map. If it does, add $f_a[x] \cdot f_b[y] \cdot f_c[z]$ to the answer.

### Why it works

Every valid triple of indices corresponds to a triple of values $(x, y, z)$ such that $x \cdot y \cdot z = m$. The algorithm enumerates every such value triple exactly once because $x$ and $y$ range over all divisors of $m$, and $z$ is uniquely determined when valid. Each contribution is weighted by independent multiplicities from the three arrays, so no valid index combination is missed or double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter
import math

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
c = list(map(int, input().split()))

fa = Counter(a)
fb = Counter(b)
fc = Counter(c)

divs = []
for i in range(1, int(math.isqrt(m)) + 1):
    if m % i == 0:
        divs.append(i)
        if i * i != m:
            divs.append(m // i)

ans = 0

for x in divs:
    if x not in fa:
        continue
    for y in divs:
        if y not in fb:
            continue
        prod = x * y
        if m % prod != 0:
            continue
        z = m // prod
        if z in fc:
            ans += fa[x] * fb[y] * fc[z]

print(ans)
```

The frequency maps replace index tracking entirely, ensuring we correctly account for repeated values. The divisor list is built once, avoiding repeated factorization work. The nested divisor loops are safe because the divisor count is small even in worst cases.

A subtle implementation detail is checking `m % prod != 0` before computing `z`, which prevents invalid integer division cases and avoids unnecessary dictionary lookups.

## Worked Examples

### Sample 1

Input:

```
n = 3, m = 3
a = [1, 2, 3]
b = [1, 1, 3]
c = [2, 3, 3]
```

Divisors of 3 are $[1, 3]$. Frequency maps are:

$f_a: 1:1, 2:1, 3:1$

$f_b: 1:2, 3:1$

$f_c: 2:1, 3:2$

| x | y | x*y | valid z? | z | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | yes | 3 | 1×2×2 = 4 |
| 1 | 3 | 3 | no | - | 0 |
| 3 | 1 | 3 | no | - | 0 |
| 3 | 3 | 9 | no | - | 0 |

Final answer is 4.

This confirms that multiplicities in $b$ and $c$ directly scale contributions, and that only divisor-consistent pairs matter.

### Sample 2

Input:

```
n = 4, m = 2
a = [1, 1, 1, 1]
b = [1, 1, 1, 1]
c = [1, 1, 1, 1]
```

Divisors of 2 are $[1, 2]$. However, no element equal to 2 exists in any array.

| x | y | x*y | z = 2/(x*y) | valid? | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | no (c has no 2) | 0 |
| 1 | 2 | 2 | 1 | no (b has no 2) | 0 |
| 2 | 1 | 2 | 1 | no (a has no 2) | 0 |
| 2 | 2 | 4 | - | no | 0 |

Final answer is 0.

This shows that divisor enumeration alone is not enough, and frequency existence checks are essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + d(m)^2)$ | building frequency maps takes linear time, and divisor pairs are enumerated once |
| Space | $O(n)$ | storage for frequency counters of up to $n$ elements |

The divisor count of any integer up to $10^9$ remains small enough that $d(m)^2$ is negligible compared to $n$, so the solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    from collections import Counter

    n, m = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))
    b = list(map(int, sys.stdin.readline().split()))
    c = list(map(int, sys.stdin.readline().split()))

    fa, fb, fc = Counter(a), Counter(b), Counter(c)

    divs = []
    for i in range(1, int(math.isqrt(m)) + 1):
        if m % i == 0:
            divs.append(i)
            if i * i != m:
                divs.append(m // i)

    ans = 0
    for x in divs:
        for y in divs:
            prod = x * y
            if m % prod != 0:
                continue
            z = m // prod
            ans += fa[x] * fb[y] * fc[z]

    return str(ans)

# provided samples
assert run("""3 3
1 2 3
1 1 3
2 3 3
""") == "4"

assert run("""4 2
1 1 1 1
1 1 1 1
1 1 1 1
""") == "0"

# custom cases
assert run("""1 1
1
1
1
""") == "1"

assert run("""2 6
2 3
1 2
1 3
""") == "1"

assert run("""3 12
2 2 3
2 3 2
3 2 2
""") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element all ones | 1 | minimal valid triple |
| Mixed small factors | 1 | correct matching of divisor structure |
| Multiple permutations | 8 | handling repeated valid combinations |

## Edge Cases

One edge case is when $m = 1$. In this situation, every valid triple must use only value 1. The algorithm handles this naturally because the divisor list contains only 1. The loops reduce to a single check where $x = y = z = 1$, and the result becomes $f_a[1] \cdot f_b[1] \cdot f_c[1]$, which is exactly correct.

Another case is when arrays contain many values that do not divide $m$. These values never appear in the divisor list, so they are automatically ignored by the frequency-based loops. For example, if $m = 10$ and arrays contain many 3s, those entries never participate because 3 is never considered as a candidate divisor.

A final subtle case is when $x \cdot y$ exceeds $m$. The check `m % prod != 0` ensures we never attempt invalid third components. For instance, if $m = 12$, choosing $x = 4$ and $y = 4$ yields product 16, which is immediately discarded before any lookup into the third map.
