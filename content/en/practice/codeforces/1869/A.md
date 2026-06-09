---
title: "CF 1869A - Make It Zero"
description: "For Codeforces 1869A, the entire solution is a constructive observation. If n is even, perform: After the first operation, every element becomes X, where X is the XOR of the whole array."
date: "2026-06-09T00:55:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1869
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 896 (Div. 2)"
rating: 900
weight: 1869
solve_time_s: 158
verified: false
draft: false
---

[CF 1869A - Make It Zero](https://codeforces.com/problemset/problem/1869/A)

**Rating:** 900  
**Tags:** constructive algorithms  
**Solve time:** 2m 38s  
**Verified:** no  

## Solution
For Codeforces 1869A, the entire solution is a constructive observation.

If `n` is even, perform:

```
(1, n)
(1, n)
```

After the first operation, every element becomes `X`, where `X` is the XOR of the whole array.

Since the segment length is even, the XOR of the whole array is now:

```
X xor X xor ... xor X = 0
```

Applying the same operation again turns every element into `0`.

If `n` is odd, use the first `n - 1` elements, whose length is even:

```
(1, n - 1)
(1, n - 1)
(n - 1, n)
(n - 1, n)
```

The first two operations make positions `1..n-1` equal to zero. Then the last two operations make positions `n-1` and `n` equal to zero as well.

This uses at most 4 operations, well below the limit of 8.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))  # values are irrelevant

        if n % 2 == 0:
            print(2)
            print(1, n)
            print(1, n)
        else:
            print(4)
            print(1, n - 1)
            print(1, n - 1)
            print(n - 1, n)
            print(n - 1, n)

if __name__ == "__main__":
    solve()
```

Why it works:

For an even-length segment, after replacing the segment by its XOR value `x`, every position contains `x`. The XOR of that entire segment becomes `x` repeated an even number of times, which equals `0`. Reapplying the operation on the same segment replaces all positions by `0`.

When `n` is odd, the segment `[1, n-1]` has even length, so two operations zero it out. After that, position `n-1` is already zero. Applying the operation twice on `[n-1, n]` zeroes the final two positions, leaving the entire array equal to zero.
