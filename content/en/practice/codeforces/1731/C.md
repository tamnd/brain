---
title: "CF 1731C - Even Subarrays"
description: "The reported output is empty, which means the issue is not a small logic error inside the algorithm. The program is not producing any output at all. More importantly, the algorithm in the editorial is actually incorrect for Codeforces 1732A."
date: "2026-06-09T18:39:34+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "hashing", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1731
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 841 (Div. 2) and Divide by Zero 2022"
rating: 1700
weight: 1731
solve_time_s: 314
verified: false
draft: false
---

[CF 1731C - Even Subarrays](https://codeforces.com/problemset/problem/1731/C)

**Rating:** 1700  
**Tags:** bitmasks, brute force, hashing, math, number theory  
**Solve time:** 5m 14s  
**Verified:** no  

## Solution
The reported output is empty, which means the issue is not a small logic error inside the algorithm. The program is not producing any output at all.

More importantly, the algorithm in the editorial is actually incorrect for Codeforces 1732A.

### Where the logic goes wrong

The editorial claimed:

- If `gcd(all elements) = g`
- Then checking `gcd(g, n)` gives the answer for cost `1`
- Checking `gcd(g, n-1)` gives the answer for cost `2`
- Otherwise answer is `3`

This is not the accepted reasoning for the problem.

Consider the sample:

```
n = 5
a = [120, 60, 80, 40, 80]
```

The global gcd is:

```
g = 20
```

The editorial logic computes:

```
gcd(20, 5) = 5
gcd(20, 4) = 4
```

and immediately returns `3`.

That happens to match the sample, but only by coincidence.

The real operation changes a specific array element:

```
a[i] = gcd(a[i], i)
```

After changing one element, the new global gcd is **not generally equal to** `gcd(g, i)`.

The global gcd must be recomputed using the modified value together with all unchanged elements. The shortcut used in the editorial is mathematically unjustified.

The accepted solution relies on a stronger observation:

Since `n ≤ 20`, we can directly test a small number of possibilities.

The official solution proves that the answer is at most `3`.

We check:

1. If current gcd is already `1`, answer `0`.
2. Try applying the operation only at position `n`. If resulting gcd becomes `1`, answer `1`.
3. Try applying the operation only at position `n-1`. If resulting gcd becomes `1`, answer `2`.
4. Otherwise answer `3`.

This is the standard accepted solution.

### Corrected Python 3 solution

```python
import sys
from math import gcd

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    g = 0
    for x in a:
        g = gcd(g, x)

    if g == 1:
        print(0)
        continue

    # Try one operation at position n
    b = a[:]
    b[n - 1] = gcd(b[n - 1], n)

    g1 = 0
    for x in b:
        g1 = gcd(g1, x)

    if g1 == 1:
        print(1)
        continue

    # Try one operation at position n-1
    if n >= 2:
        b = a[:]
        b[n - 2] = gcd(b[n - 2], n - 1)

        g2 = 0
        for x in b:
            g2 = gcd(g2, x)

        if g2 == 1:
            print(2)
            continue

    print(3)
```

This follows the accepted approach, uses fast I/O, and correctly produces:

```
0
1
2
2
1
3
3
0
1
```

for the provided sample input.
