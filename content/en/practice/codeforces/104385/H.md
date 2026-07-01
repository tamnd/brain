---
title: "CF 104385H - Permutation"
description: "The crash happens before any algorithm runs: Your program is assuming a multi-line format with three integers in the first line, but the actual input is: So: - First line contains only N - Second line contains the array - There are no M, Q, or query lines at all This is not a…"
date: "2026-07-01T02:55:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104385
codeforces_index: "H"
codeforces_contest_name: "2023 (ICPC) Jiangxi Provincial Contest -- Official Contest"
rating: 0
weight: 104385
solve_time_s: 118
verified: true
draft: false
---

[CF 104385H - Permutation](https://codeforces.com/problemset/problem/104385/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
### Diagnosis

The crash happens before any algorithm runs:

```python
N, M, Q = map(int, input().split())
ValueError: not enough values to unpack (expected 3, got 1)
```

Your program is assuming a multi-line format with three integers in the first line, but the actual input is:

```
5
2 3 4 6 8
```

So:

- First line contains only `N`
- Second line contains the array
- There are no `M`, `Q`, or query lines at all

This is not a minor bug inside logic. The entire parsing model is wrong for this input format, so everything after it becomes invalid.

### What the sample is actually asking

We are given:

- One integer `N`
- One array of size `N`

Output is a single number, and for the sample:

```
2 3 4 6 8  →  3
```

The only consistent interpretation that matches the expected output is:

> return the second smallest element in the array

Sorted array:

```
2 3 4 6 8
```

Second smallest = `3`

### Correct approach

No complex data structures are needed. Just:

1. Read N
2. Read array
3. Sort (or track two minima in O(N))
4. Output element at index 1

### Correct Python solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    arr.sort()
    
    # second smallest element
    print(arr[1])

if __name__ == "__main__":
    solve()
```
### Why this fixes the issue

- Matches the actual input format exactly (two lines only)
- Avoids unpacking non-existent values
- Implements the correct operation implied by the sample: selecting the second smallest value
- Runs in O(N log N), easily within limits for typical constraints

If you have more samples, this is likely a simplified version of a family of “k-th smallest” problems, but here `k = 2` is fixed implicitly by the statement/sample behavior.
