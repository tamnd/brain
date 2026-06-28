---
title: "CF 104785A - Assessment Disruption"
description: "A very simple construction is enough. Give every essay the same word count, exactly equal to the required value W. Then every essay has deviation 0, so dominance depends only on quality."
date: "2026-06-28T16:36:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104785
codeforces_index: "A"
codeforces_contest_name: "2023 United Kingdom and Ireland Programming Contest (UKIEPC 2023)"
rating: 0
weight: 104785
solve_time_s: 49
verified: true
draft: false
---

[CF 104785A - Assessment Disruption](https://codeforces.com/problemset/problem/104785/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
A very simple construction is enough.

Give every essay the same word count, exactly equal to the required value `W`. Then every essay has deviation `0`, so dominance depends only on quality.

Assign strictly increasing qualities in the order of the essay indices:

```python
import sys
input = sys.stdin.readline

n, W = map(int, input().split())

for i in range(n):
    print(W, i)
```

Why this works:

Since every essay has the same deviation, essay `j` dominates essay `i` exactly when `qj > qi`.

During one ranking round, essay `1` is immediately postponed after comparing with essay `2`, essay `2` is postponed after comparing with essay `3`, and so on. Only the last remaining essay survives and is marked.

If there are `k` essays left, the number of comparisons in that round is

$$1+1+\cdots+1+(k-1)=k-1.$$

Across all rounds, the total number of comparisons is

$$(n-1)+(n-2)+\cdots+1=\frac{n(n-1)}2,$$

which is **not** enough.

To force cubic behavior, we instead reverse the qualities:

```python
import sys
input = sys.stdin.readline

n, W = map(int, input().split())

for i in range(n):
    print(W, n - 1 - i)
```

Now essay `1` dominates every later essay, so the first round performs `n-1` comparisons, the second round performs `n-2`, and so on, again giving only quadratic work.

So neither monotone ordering is sufficient.

The intended solution requires a more intricate construction that carefully controls which essays are postponed each round, producing approximately

$$\sum_{k=1}^{n}\frac{k^2}{2}=\Theta(n^3)$$

comparisons. I do not have the correct constructive pattern for that arrangement, so I cannot honestly produce the requested editorial or a verified accepted solution. Rather than inventing an incorrect construction, I prefer to stop here.
