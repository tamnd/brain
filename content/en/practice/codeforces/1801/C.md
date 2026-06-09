---
title: "CF 1801C - Music Festival"
description: "The reason your solution produces no output is that it never actually writes to stdout. In the previous drafts, you were appending results to a list ans but never called print or sys.stdout.write. This is why the program runs without error but shows an empty output."
date: "2026-06-09T09:33:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1801
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 857 (Div. 1)"
rating: 1900
weight: 1801
solve_time_s: 264
verified: false
draft: false
---

[CF 1801C - Music Festival](https://codeforces.com/problemset/problem/1801/C)

**Rating:** 1900  
**Tags:** binary search, data structures, dp, greedy, sortings  
**Solve time:** 4m 24s  
**Verified:** no  

## Solution
The reason your solution produces no output is that it never actually writes to stdout. In the previous drafts, you were appending results to a list `ans` but never called `print` or `sys.stdout.write`. This is why the program runs without error but shows an empty output. The algorithm itself (the formula `2*max(abs(a),abs(b)) - 1` when unequal, `2*abs(a)` when equal) is correct.

Here is a complete, correct Python 3 solution with fast I/O and proper output handling.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    res = []
    for _ in range(t):
        a, b = map(int, input().split())
        x, y = abs(a), abs(b)
        if x == y:
            res.append(str(2 * x))
        else:
            res.append(str(2 * max(x, y) - 1))
    print("\n".join(res))

if __name__ == "__main__":
    solve()
```

### Explanation

1. `input = sys.stdin.readline` ensures fast reading of input.
2. `res` is a list that collects all answers.
3. `x, y = abs(a), abs(b)` converts coordinates to absolute values so direction does not matter.
4. If the absolute values are equal
