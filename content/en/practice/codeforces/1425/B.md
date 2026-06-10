---
title: "CF 1425B - Blue and Red of Our Faculty!"
description: "The error is not in the logic of computing the floor. The RuntimeError you are seeing is a NameError: solve is not defined. This is a scoping issue: your testing harness calls solve()before it is actually defined."
date: "2026-06-11T05:57:52+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dp"]
categories: ["algorithms"]
codeforces_contest: 1425
codeforces_index: "B"
codeforces_contest_name: "2020 ICPC, COMPFEST 12, Indonesia Multi-Provincial Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2600
weight: 1425
solve_time_s: 511
verified: false
draft: false
---

[CF 1425B - Blue and Red of Our Faculty!](https://codeforces.com/problemset/problem/1425/B)

**Rating:** 2600  
**Tags:** divide and conquer, dp  
**Solve time:** 8m 31s  
**Verified:** no  

## Solution
The error is not in the logic of computing the floor. The `RuntimeError` you are seeing is a **NameError: `solve` is not defined`**. This is a **scoping issue**: your testing harness calls `solve()`before it is actually defined. Python cannot find a function named`solve` in the global scope at the point where you call it. This has nothing to do with arithmetic or edge cases.

To fix it, we must **wrap the main solution in a `solve()` function** and ensure it is defined **before** the test harness or the `__main__` block calls it. Here is a fully working Python 3 solution using fast I/O:

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        if n <= 2:
            # First floor contains apartments 1 and 2
            print(1)
        else:
            # Apartments on floors after the first
            # Subtract first floor (2 apartments), compute zero-based floor index
            # Then add 2 to account for first floor being floor 1
            floor = (n - 3) // x + 2
            print(floor)

if __name__ == "__main__":
    solve()
```

### Why this fixes the problem

1. The function `solve()` is now **explicitly defined**.
2. The `__main__` block calls `solve()` safely, so running the script directly works.
3. The logic `(n - 3) // x + 2` correctly computes the floor:

- Subtract the first floor's 2 apartments: `n - 3`.
- Integer division by `x` gives how many additional floors beyond the first.
- Add `2` to convert zero-based index to floor number (1 for first floor, plus additional).

### Example trace

For input `7 3`:

- `n = 7`, `x = 3`
- `n > 2`, so compute floor: `(7 - 3) // 3 + 2 = 4 // 3 + 2 = 1 + 2 = 3`
- Output: `3`  matches expected.

For input `1 5`:

- `n = 1` → `n <= 2`, first floor → output `1`  matches expected.

This structure also allows your `run()` test harness to work because `solve()` is now defined in scope. You can safely do:

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

assert run("4\n7 3\n1 5\n22 5\n987 13\n") == "3\n1\n5\n77"
```

The `NameError` will no longer occur. All edge cases, including first-floor apartments and exact multiples of `x`, are handled correctly.
