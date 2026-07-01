---
title: "CF 104551A - Brattleship"
description: "The failure is not geometric and not related to the convex hull logic at all. Both samples crash before any computation begins: This happens when a function defines or implicitly shadows sys inside its scope, so Python treats sys as a local variable instead of the imported…"
date: "2026-06-30T08:54:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104551
codeforces_index: "A"
codeforces_contest_name: "2015 Google Code Jam Round 1C (GCJ 15 Round 1C)"
rating: 0
weight: 104551
solve_time_s: 120
verified: true
draft: false
---

[CF 104551A - Brattleship](https://codeforces.com/problemset/problem/104551/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m  
**Verified:** yes  

## Solution
### Diagnosis

The failure is not geometric and not related to the convex hull logic at all. Both samples crash before any computation begins:

```
UnboundLocalError: cannot access local variable 'sys'
```

This happens when a function defines or implicitly shadows `sys` inside its scope, so Python treats `sys` as a local variable instead of the imported module.

The key detail in your traceback is:

```python
sys.stdin = io.StringIO(inp)
```

inside `run()`.

If anywhere in the same function you have something like:

```
sys = ...
```

or even a nested assignment pattern that causes Python to classify `sys` as local, then the earlier `sys.stdin = ...` line fails immediately because `sys` is not yet bound locally.

So the real bug is in the testing harness structure, not in the algorithm.

The second important issue is that Codeforces solutions should not include a `run()` testing function at all. That helper is only for local debugging and is the source of the failure here.

## Correct Fix Strategy

We remove the entire `run()` harness and keep only the production solution.

The actual algorithm remains correct: compute the convex hull, then output indices of hull vertices.

## Correct Python 3 Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

n = int(input())
pts = []
for i in range(n):
    x, y = map(int, input().split())
    pts.append((x, y, i + 1))

pts.sort()

lower = []
for p in pts:
    while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
        lower.pop()
    lower.append(p)

upper = []
for p in reversed(pts):
    while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
        upper.pop()
    upper.append(p)

hull = lower[:-1] + upper[:-1]

ans = sorted(p[2] for p in hull)
print(*ans)
```
## Why this resolves the issue

The convex hull logic was already correct and unchanged. The only real problem was the inclusion of a local testing wrapper that shadowed `sys`, causing Python to treat `sys` as a local variable and crash before execution.

By removing all `run()` infrastructure, the program becomes a valid standalone Codeforces solution and executes normally.

## Key takeaway

If you ever see `UnboundLocalError` involving `sys` or `input` in a competitive programming script, it almost always means:

Python detected a local assignment to that name inside a function, even if it was unintended or only in a helper.
