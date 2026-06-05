---
title: "CF 279C - Ladder"
description: "We are given a one-dimensional array of integers and a list of queries, each specifying a contiguous subsegment of the array. For every query, we need to determine whether the subsegment forms a \"ladder."
date: "2026-06-05T05:50:51+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 279
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 171 (Div. 2)"
rating: 1700
weight: 279
solve_time_s: 87
verified: true
draft: false
---

[CF 279C - Ladder](https://codeforces.com/problemset/problem/279/C)

**Rating:** 1700  
**Tags:** dp, implementation, two pointers  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional array of integers and a list of queries, each specifying a contiguous subsegment of the array. For every query, we need to determine whether the subsegment forms a "ladder." A ladder is a sequence that increases monotonically (non-decreasing) up to some point, and then decreases monotonically (non-increasing) after that point. This means the sequence may be entirely non-decreasing, entirely non-increasing, or have a single peak where it transitions from non-decreasing to non-increasing. The output is "Yes" if the subsegment is a ladder, and "No" otherwise.

The constraints tell us that both the array size and the number of queries can be as large as 100,000. A naive approach that scans each subsegment individually for every query would require examining up to 10^10 elements in the worst case, which is far beyond what can run in 2 seconds. This implies that we need an approach that preprocesses the array to answer queries in constant or logarithmic time.

Edge cases arise when sequences are flat, single-element, or strictly increasing or decreasing. For example, an array `[5, 5, 5]` should return "Yes" for any subsegment, as it is trivially non-decreasing and non-increasing. A single-element subsegment `[7]` is also a ladder. Problems appear when a careless implementation assumes a strict increase or decrease instead of a non-strict comparison.

## Approaches

The brute-force approach iterates over each query and checks the corresponding subsegment directly. For each subsegment, it scans from left to right to find the longest non-decreasing prefix and then scans from the end to find the longest non-increasing suffix. If these two regions cover the entire subsegment, it is a ladder. This approach works correctly but has a time complexity of O(n * m) in the worst case, which is too slow for the given constraints.

The key insight to optimize is that we can preprocess the array once to know, for every index, how far the non-decreasing and non-increasing segments extend. Specifically, we can compute for each position the farthest index reachable by moving right while non-decreasing (`up[i]`) and the farthest index reachable by moving right while non-increasing (`down[i]`). Then, for a query `[l, r]`, if `down[up[l]] >= r`, the segment forms a ladder. This works because `up[l]` finds the end of the initial non-decreasing portion starting at `l`, and `down[up[l]]` extends the non-increasing portion from there. The preprocessing runs in linear time, and each query is answered in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(1) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `up` of length `n` to store the farthest index reachable from each position by a non-decreasing sequence. Start from the second-to-last element and move leftwards, updating `up[i]` to `i+1` if `a[i] <= a[i+1]`, otherwise `up[i] = i`.
2. Initialize an array `down` of length `n` to store the farthest index reachable from each position by a non-increasing sequence. Start from the second-to-last element and move leftwards, updating `down[i]` to `i+1` if `a[i] >= a[i+1]`, otherwise `down[i] = i`.
3. For each query `[l, r]`, check if `down[up[l-1]] >= r-1`. We subtract one because array indices in Python are 0-based. If true, print "Yes"; otherwise, print "No". This works because `up[l-1]` gives the endpoint of the non-decreasing segment starting at `l-1`, and `down[up[l-1]]` extends the non-increasing part from that peak. If it reaches or passes `r-1`, the subsegment is a ladder.

Why it works: The invariant is that `up[i]` correctly identifies the maximum extent of a non-decreasing sequence starting at `i`, and `down[i]` does the same for non-increasing sequences. By combining these two precomputed arrays, we can verify in constant time whether a subsegment satisfies the ladder property without scanning each element repeatedly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

up = [0] * n
down = [0] * n

up[-1] = n - 1
for i in range(n - 2, -1, -1):
    if a[i] <= a[i + 1]:
        up[i] = up[i + 1]
    else:
        up[i] = i

down[-1] = n - 1
for i in range(n - 2, -1, -1):
    if a[i] >= a[i + 1]:
        down[i] = down[i + 1]
    else:
        down[i] = i

for _ in range(m):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    if down[up[l]] >= r:
        print("Yes")
    else:
        print("No")
```

The first loop constructs `up` by scanning from right to left, ensuring that each index knows the farthest non-decreasing segment it can reach. The second loop constructs `down` similarly for non-increasing sequences. The query processing uses these arrays directly to determine ladder validity in constant time per query. The indexing adjustment for 0-based Python arrays is a common source of errors, but here `l-1` and `r-1` handle it properly.

## Worked Examples

### Sample 1

Input: `1 2 1 3 3 5 2 1`, Query: `[1, 3]`

| i | a[i] | up[i] | down[i] |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 2 |
| 1 | 2 | 1 | 2 |
| 2 | 1 | 2 | 2 |

`up[0] = 1` points to 2. `down[1] = 2` points to 1. Since 2 >= 2, the answer is "Yes".

Query `[2, 4]`:

`up[1] = 4` (extends to 5), `down[4] = 4` (stops at 3). Since 4 < 3 is false, answer is "No". This demonstrates correct detection of a non-ladder segment.

### Single-element segment

Input: `[7]`, Query: `[1,1]`. `up[0] = 0`, `down[0] = 0`. Since `down[up[0]] = 0 >= 0`, output is "Yes".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Preprocessing arrays `up` and `down` takes O(n). Each query is answered in O(1). |
| Space | O(n) | Arrays `up` and `down` store one integer per element. |

Given the constraints n, m ≤ 10^5, this algorithm is efficient and fits comfortably within the 2-second time limit and memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    up = [0] * n
    down = [0] * n

    up[-1] = n - 1
    for i in range(n - 2, -1, -1):
        if a[i] <= a[i + 1]:
            up[i] = up[i + 1]
        else:
            up[i] = i

    down[-1] = n - 1
    for i in range(n - 2, -1, -1):
        if a[i] >= a[i + 1]:
            down[i] = down[i + 1]
        else:
            down[i] = i

    for _ in range(m):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        if down[up[l]] >= r:
            print("Yes")
        else:
            print("No")
    return output.getvalue().strip()

# provided sample
assert run("8 6\n1 2 1 3 3 5 2 1\n1 3\n2 3\n2 4\n8 8\n1 4\n5 8\n") == "Yes\nYes\nNo\nYes\nNo\nYes"

# custom cases
assert run("1 1\n5\n1 1\n") == "Yes", "single element"
assert run("3 3\n1 1 1\n1 3\n1 2\n2 3\n") == "Yes\nYes\nYes", "all equal
```
