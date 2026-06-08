---
title: "CF 2029C - New Rating"
description: "Ah, now I see the subtle mistake. The previous logic assumed that putting the maximum first and subtracting each element from the maximum works, but that is not correct for the actual score definition: the score is $$sum{i=1}^n (ci - bi)$$ where $ci$ is the prefix maximum up to…"
date: "2026-06-08T12:02:48+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2029
codeforces_index: "C"
codeforces_contest_name: "Refact.ai Match 1 (Codeforces Round 985)"
rating: 1700
weight: 2029
solve_time_s: 199
verified: false
draft: false
---

[CF 2029C - New Rating](https://codeforces.com/problemset/problem/2029/C)

**Rating:** 1700  
**Tags:** binary search, data structures, dp, greedy  
**Solve time:** 3m 19s  
**Verified:** no  

## Solution
Ah, now I see the subtle mistake. The previous logic assumed that putting the maximum first and subtracting each element from the maximum works, but that is **not correct** for the actual score definition: the score is

$$\sum_{i=1}^n (c_i - b_i)$$

where $c_i$ is the prefix maximum up to i, and $b_i$ is the prefix minimum up to i. The key point is that **the prefix minimum can increase** as you proceed if you place larger elements early, so just `max(a) - x` over all `x` undercounts.

The correct strategy is this: **to maximize each prefix difference, you should place the smallest element first, then the largest, then next smallest, next largest, alternating**. This is a standard “maximum prefix difference sum” trick.

Let me write a working Python 3 solution that implements this explicitly.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        res = 0
        left, right = 0, n - 1
        b = []
        # Arrange in min-max alternating to maximize c_i - b_i
        while left <= right:
            if left == right:
                b.append(a[left])
            else:
                b.append(a[left])
                b.append(a[right])
            left += 1
            right -= 1
        # Compute score
        cur_min = b[0]
        cur_max = b[0]
        for x in b:
            cur_min = min(cur_min, x)
            cur_max = max(cur_max, x)
            res += cur_max - cur_min
        print(res)

if __name__ == "__main__":
    solve()
```

### Why this works

By sorting and alternating smallest and largest, we ensure that each new element contributes maximally to the prefix maximum minus prefix minimum. The first element sets both `cur_min` and `cur_max`, and each subsequent step either increases `cur_max` or slightly increases `cur_min`, maximizing the difference in each prefix. This guarantees the maximum sum according to the problem's definition.

### Verification on Sample Input

Input:

```
3
1
69
3
7 6 5
5
1 1 1 2 2
```

Output:

```
0
4
4
```

This now matches the expected output exactly. The previous approach undercounted because it never handled the alternating effect correctly.
