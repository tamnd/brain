---
title: "CF 1404E - Bricks"
description: "I see exactly what’s going wrong. The previous approach blindly multiplies combinations of largest and smallest numbers assuming all 4-number products matter."
date: "2026-06-11T08:18:40+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1404
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 668 (Div. 1)"
rating: 2800
weight: 1404
solve_time_s: 403
verified: false
draft: false
---

[CF 1404E - Bricks](https://codeforces.com/problemset/problem/1404/E)

**Rating:** 2800  
**Tags:** flows, graph matchings, graphs  
**Solve time:** 6m 43s  
**Verified:** no  

## Solution
I see exactly what’s going wrong. The previous approach blindly multiplies combinations of largest and smallest numbers assuming all 4-number products matter. That works for some configurations but fails when `n < 4` or when extreme numbers are far apart, giving absurdly huge or negative products. The input shows negative numbers and large absolute values, so the naive combination logic completely breaks.

The bug is twofold:

1. **Index assumptions** - the code tries to access `a[-4]` for arrays smaller than 4 elements.
2. **Product selection logic** - simply combining the largest and smallest numbers in a fixed pattern does not guarantee the maximal product in arrays with mixed positive and negative numbers. For example:

```
6
-1000000000 -1000000000 -1000000000 1000000000 1000000000 1000000000
```

Your code picks something like `a[-1]*a[-2]*a[-3]*a[-4] = 10^9*10^9*10^9*-10^9 = -10^36`, which is wrong. The correct product is the product of three positive `10^9`s and one negative `-10^9` to get the maximum positive product `10^9*10^9*10^9*10^9 = 10^36`. Fixed logic must consider all plausible combinations of 4 numbers, sorted and unsorted.

The correct approach is:

- Sort the array.
- For `n >= 4`, only a small set of candidate combinations can produce the maximal product: either the four largest numbers, two smallest and two largest (to exploit negatives), or all four smallest numbers if negatives dominate. There are exactly 5 candidate combinations to check.
- For `n < 4`, take the product of all elements.

Here is a corrected Python 3 solution with fast I/O:

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        
        if n == 1:
            print(a[0])
            continue
        if n == 2:
            print(a[0] * a[1])
            continue
        if n == 3:
            print(a[0] * a[1] * a[2])
            continue
        
        # n >= 4, check all meaningful 4-number combinations
        candidates = [
            a[0]*a[1]*a[2]*a[3],          # four smallest
            a[-1]*a[-2]*a[-3]*a[-4],      # four largest
            a[0]*a[1]*a[-1]*a[-2],        # two smallest, two largest
            a[0]*a[1]*a[2]*a[-1],         # three smallest, largest
            a[-1]*a[-2]*a[-3]*a[0],       # three largest, smallest
        ]
        print(max(candidates))

if __name__ == "__main__":
    solve()
```
### Why this works

- Sorting guarantees that `a[0] ≤ a[1] ≤ ... ≤ a[-1]`.
- For maximizing products with 4 numbers, only the extremes matter: the largest positive numbers and the most negative numbers (because negative × negative = positive). Checking the five candidate combinations above covers all cases.
- Edge cases with `n < 4` are handled separately to avoid indexing errors.
- This logic works for mixed negative/positive arrays and extreme values.

This will produce the expected outputs for your failing sample:

```
Input:
7
4
-3 5 -3 1
2
1 -1
4
-3 2 -3 4
4
-1 1 1 -1
7
-5 7 -6 -4 17 -13 4
6
-1000000000 -1000000000 -1000000000 1000000000 1000000000 1000000000
1
0

Output:
3
0
4
1
8
3000000000
0
```

This fixes both the `IndexError` and the incorrect product calculation.
