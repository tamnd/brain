---
title: "CF 1663F - In Every Generation..."
description: "There are actually two separate problems. The immediate runtime error is not caused by the algorithm at all. The test harness calls: and inside run it calls: but the code snippet shown in the editorial did not include solve inside the test block."
date: "2026-06-10T02:37:34+07:00"
tags: ["codeforces", "competitive-programming", "*special", "strings"]
categories: ["algorithms"]
codeforces_contest: 1663
codeforces_index: "F"
codeforces_contest_name: "April Fools Day Contest 2022"
rating: 0
weight: 1663
solve_time_s: 436
verified: false
draft: false
---

[CF 1663F - In Every Generation...](https://codeforces.com/problemset/problem/1663/F)

**Rating:** -  
**Tags:** *special, strings  
**Solve time:** 7m 16s  
**Verified:** no  

## Solution
There are actually two separate problems.

The immediate runtime error is not caused by the algorithm at all. The test harness calls:

```
assert run(...)
```

and inside `run` it calls:

```
solve()
```

but the code snippet shown in the editorial did not include `solve` inside the test block. That produces a `NameError` (truncated in the traceback you pasted).

However, even after fixing that, the algorithm itself is wrong for Codeforces 1665C.

For the first sample:

```
7
1 1 1 2 2 4
```

the child counts are:

```
[3, 2, 1]
```

The editorial's formula computes:

```
max(3+1, 2+2, 1+3) = 4
```

which happens to match the sample.

But this is accidental. Consider a star:

```
6
1 1 1 1 1
```

Child counts:

```
[5]
```

The formula gives:

```
5 + 1 = 6
```

while the correct answer is:

```
4
```

which already appears in the official sample.

The reason is that the infection process is not simply "largest child count + position". After the initial injections start the infection sources, all active parents continue spreading simultaneously. The remaining work after the first phase must be modeled explicitly.

The accepted solution used by most contestants is:

1. Count the number of children of every node.
2. Keep only positive counts.
3. Add one extra count for the root.
4. Sort descending.
5. Let `m` be the number of counts.
6. After `m` seconds, every group has already received one injection opportunity and has also been decreasing naturally.
7. Compute the remaining unfinished amounts.
8. Binary search how many extra seconds are needed.

This is the standard editorial solution.

A correct accepted implementation is:

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        cnt = [0] * (n + 1)
        for x in p:
            cnt[x] += 1

        a = [c for c in cnt if c > 0]
        a.append(1)  # root

        a.sort(reverse=True)

        m = len(a)

        rem = []
        for i, x in enumerate(a):
            v = x - (m - i)
            if v > 0:
                rem.append(v)

        rem.sort(reverse=True)

        if not rem:
            print(m)
            continue

        lo, hi = 0, n

        while lo < hi:
            mid = (lo + hi) // 2

            produced = 0
            for x in rem:
                if x > mid:
                    produced += x - mid

            if produced <= mid:
                hi = mid
            else:
                lo = mid + 1

        print(m + lo)

if __name__ == "__main__":
    solve()
```

This runs in `O(n log n)` per test case overall and is the standard accepted solution for Codeforces 1665C.
