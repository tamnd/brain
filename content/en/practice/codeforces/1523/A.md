---
title: "CF 1523A - Game of Life"
description: "The empty output indicates a runtime crash before any printing happens, not a logical error in the math. Tracing the execution on the input: The program first reads t = 3, then processes three test cases."
date: "2026-06-10T17:44:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1523
codeforces_index: "A"
codeforces_contest_name: "Deltix Round, Spring 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 800
weight: 1523
solve_time_s: 720
verified: false
draft: false
---

[CF 1523A - Game of Life](https://codeforces.com/problemset/problem/1523/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 12m  
**Verified:** no  

## Solution
The empty output indicates a runtime crash before any printing happens, not a logical error in the math.

Tracing the execution on the input:

```
3
3
100
25
```

The program first reads `t = 3`, then processes three test cases. The expected computation per test case is:

For each `k`, compute:

$$\frac{100}{\gcd(k, 100)}$$

The failure happens earlier than any arithmetic reasoning: the program never reaches `print`. The usual cause for exactly this symptom (no traceback shown in judge-style harnesses, just empty output) is a missing import or undefined symbol in the actual execution path, most commonly `math.gcd` or `gcd` being used without importing `math` or importing `gcd` explicitly.

In many Codeforces-style templates, the solution uses `gcd` directly, but if it was written as `math.gcd` without `import math`, or as `gcd` without `from math import gcd`, execution stops immediately.

The correct fix is to ensure the gcd function is properly imported and the program never depends on implicit namespace availability.

The algorithm itself is correct: the minimal number of liters is achieved by taking the smallest integer pair proportional to $k : (100-k)$, which reduces to dividing by their greatest common divisor.

## Corrected Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k = int(input())
    g = gcd(k, 100)
    print(100 // g)
```

This version ensures:

- `gcd` is defined in all execution environments.
- Each test case is processed independently in O(1).
- Output is produced immediately per case, avoiding buffering issues in broken early-exit runs.

The logic remains unchanged: reduce the ratio $k/100$ to lowest terms; the denominator gives the minimal total number of operations required to achieve that exact percentage using unit increments.
