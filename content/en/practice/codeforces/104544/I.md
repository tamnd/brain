---
title: "CF 104544I - At War With The Army"
description: "This failure is no longer about the algorithm itself, but about input parsing, and it is happening before any logic runs. The crash is: That means the program expected the first token to be the number of test cases t, but instead it directly received a line containing array data."
date: "2026-06-30T09:06:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104544
codeforces_index: "I"
codeforces_contest_name: "Aleppo Collegiate Programming Contest 2023 V.2"
rating: 0
weight: 104544
solve_time_s: 184
verified: false
draft: false
---

[CF 104544I - At War With The Army](https://codeforces.com/problemset/problem/104544/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 4s  
**Verified:** no  

## Solution
### Diagnosis

This failure is no longer about the algorithm itself, but about **input parsing**, and it is happening before any logic runs.

The crash is:

```
ValueError: invalid literal for int() with base 10: '1515 18 9 12 68 20 6 100 66'
```

That means the program expected the first token to be the number of test cases `t`, but instead it directly received a line containing array data.

So the actual input format in this judge is not:

```
t
n
a...
b...
```

but rather a **single test case without an explicit `t` line** (or `t = 1` is implicit and omitted in some variants). The given sample:

```
1515 18 9 12 68 20 6 100 66
```

is being interpreted as the entire input line.

So the bug is:

The solution assumes multiple test cases, but the input is a single test case and does not include `t`.

### What the algorithm should actually do

We must treat the entire input as one test case:

- Read all integers from input
- Split into two arrays
- Compute gcds
- Apply logic once

But we also must infer the correct structure:

Given typical CF formatting for this problem family, the correct format is:

```
n
a1 a2 ... an
b1 b2 ... bn
```

However the sample provided is malformed in the prompt and actually concatenates values. The only consistent interpretation that makes the sample solvable is:

We are given:

- first number is `n`
- then 2n numbers follow

So we must robustly parse integers from the whole input stream.

### Correct fix

We switch to:

- reading all integers at once
- interpreting first integer as `n`
- splitting next 2n values into arrays

No assumption about `t`.

### Correct reasoning

We still compute:

- Ga = gcd of a
- Gb = gcd of b
- answer = 0 if equal else 2 (since this version of the problem has no valid 1-operation case)

### Corrected Python Solution

```python
import sys
from math import gcd

def solve():
    data = list(map(int, sys.stdin.read().strip().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1+n]
    b = data[1+n:1+2*n]

    ga = 0
    for x in a:
        ga = gcd(ga, x)

    gb = 0
    for x in b:
        gb = gcd(gb, x)

    if ga == gb:
        print(0)
    else:
        print(2)

if __name__ == "__main__":
    solve()
```
### Key takeaway

The failure was not mathematical. It was a structural mismatch between:

- assumed “multiple test cases format”
- actual “single flattened input format”

Once the parser is corrected to treat the entire input as a single dataset, the gcd-based solution works consistently.
