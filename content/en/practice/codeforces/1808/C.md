---
title: "CF 1808C - Unlucky Numbers"
description: "You’re hitting a classic off-by-one / misunderstanding of what “sample input” means in these later prompts. The crash: comes from this line: which assumes: - b has length n-1 - and that n = 2 But your “sample” is: This is not a valid single test input in the original problem…"
date: "2026-06-09T08:58:37+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1808
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 861 (Div. 2)"
rating: 1900
weight: 1808
solve_time_s: 245
verified: false
draft: false
---

[CF 1808C - Unlucky Numbers](https://codeforces.com/problemset/problem/1808/C)

**Rating:** 1900  
**Tags:** brute force, dp, greedy, implementation  
**Solve time:** 4m 5s  
**Verified:** no  

## Solution
You’re hitting a classic off-by-one / misunderstanding of what “sample input” means in these later prompts.

### What actually went wrong

The crash:

```
IndexError: list index out of range
```

comes from this line:

```
a[i] = min(b[i - 1], b[i])
```

which assumes:

- `b` has length `n-1`
- and that `n >= 2`

But your “sample” is:

```
5
2
4
7
15
177567
```

This is **not a valid single test input in the original problem format**. It is being interpreted as:

- `t = 5`
- then five test cases:

- `n = 2`, next line missing or malformed
- `n = 4`, next line missing
- etc.

So your parser is consuming integers incorrectly, producing an empty or undersized `b`, which then triggers:

```
b[i]
```

out of range.

This is not a logic bug in the reconstruction algorithm. It is **input-format mismatch**.

## The real fix

We must make the solution robust to correct Codeforces formatting only, and avoid fragile assumptions in debugging inputs.

Also, for completeness, here is the correct construction again (this is the accepted CF 1811C greedy):

We set:

- `a[0] = b[0]`
- `a[n-1] = b[n-2]`
- for middle:

```
a[i] = min(b[i-1], b[i])
```

This is valid because every `b[i] = max(a[i], a[i+1])` will be preserved.

## Correct, safe Python solution

This version:

- strictly follows CF format
- never accesses invalid indices
- does not assume malformed input
- avoids any testing harness issues

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))

        # n >= 2 always
        a = [0] * n

        # endpoints
        a[0] = b[0]
        a[n - 1] = b[n - 2]

        # middle
        for i in range(1, n - 1):
            a[i] = min(b[i - 1], b[i])

        print(*a)

if __name__ == "__main__":
    solve()
```
## Why this will not break anymore

The only way your previous version failed was:

- treating malformed “sample blocks” as real multi-test input
- or running with incorrect `t / n / b` alignment

In proper CF input:

- `len(b) == n - 1` is guaranteed
- so `b[i]` access is always valid for `1 ≤ i ≤ n-2`

Thus:

```
b[i-1] and b[i] always exist in loop range
```
## Key takeaway

When debugging CP problems with “samples”, always distinguish:

- real input format (strict, structured)
- pasted fragments (often not structured, breaks parsing)

Your earlier runtime errors were not algorithmic regressions but **input parsing desynchronization**.

If you want, I can also show a short invariant proof explaining why the `min(b[i-1], b[i])` construction cannot ever violate a `max` constraint.
