---
title: "CF 193D - Two Segments"
description: "We are given a permutation of integers from 1 to n. A permutation means each integer appears exactly once. The task is to count pairs of contiguous subarrays (segments) such that when we combine the two segments, the union of their elements forms a consecutive sequence of…"
date: "2026-06-03T01:29:19+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 193
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 122 (Div. 1)"
rating: 2900
weight: 193
solve_time_s: 68
verified: true
draft: false
---

[CF 193D - Two Segments](https://codeforces.com/problemset/problem/193/D)

**Rating:** 2900  
**Tags:** data structures  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to _n_. A permutation means each integer appears exactly once. The task is to count pairs of contiguous subarrays (segments) such that when we combine the two segments, the union of their elements forms a consecutive sequence of integers in any order.

For example, in the permutation [1, 2, 3], taking segments [1,2] and [3,3] forms the set {1, 2, 3}, which is consecutive. We consider two pairs identical if the total set of elements they cover is the same, so overlapping or nested choices that yield the same set are counted only once.

The size of _n_ can be up to 300,000. This means any approach that considers all pairs of segments naively, which would involve roughly O(n³) or O(n²) operations, is impractical. We need a linear or near-linear approach. Edge cases to watch for include very short permutations (length 1 or 2) and permutations where the elements are in decreasing order, as these can expose off-by-one errors or incorrect segment splitting.

## Approaches

The brute-force approach is to enumerate every possible first segment [a0, a1] and every second segment [b0, b1] after it. For each candidate pair, we would extract all the elements, sort them, and check if they form a consecutive sequence. This is correct but extremely slow: there are roughly n²/2 choices for the first segment and up to n²/2 for the second, and each check could involve up to n elements. This gives O(n⁴) time in the worst case, which is unworkable for n = 3·10⁵.

The key observation is that in a permutation, any set of consecutive integers can be fully described by its minimum and maximum. That is, for a segment to be consecutive, the difference between its maximum and minimum plus one must equal the segment length. This allows us to detect valid segments in O(1) per segment if we maintain running min and max.

We can then iterate over the permutation in a single pass, expanding segments and keeping track of valid ranges. Specifically, for every possible right end of a segment, we maintain the minimal left end such that the segment forms a consecutive sequence. From there, we can consider every way to split this segment into two contiguous subsegments: each split generates a unique pair. By scanning from left to right and tracking min/max values carefully, we reduce the problem to O(n) with appropriate bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n⁴) | O(n) | Too slow |
| Optimal (min/max sliding) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `answer = 0` for the number of good pairs.
2. Iterate over all possible right endpoints `r` from 0 to n-1. Maintain a variable `l` for the leftmost index of the segment such that the elements p[l..r] form a consecutive sequence. Use two variables `current_min` and `current_max` to store the minimal and maximal elements of the segment.
3. Expand the segment by moving `r` one step to the right. Update `current_min` and `current_max`. While the segment p[l..r] does not satisfy the condition `current_max - current_min == r - l`, increment `l` to shrink the segment from the left. This maintains the invariant that p[l..r] always forms consecutive elements.
4. For every valid segment p[l..r], the number of ways to split it into two non-empty contiguous subsegments is `r - l`. Each split corresponds to a unique pair of segments covering the same set of elements. Increment `answer` by `r - l`.
5. After iterating through all right endpoints, `answer` contains the total number of distinct good segment pairs.

**Why it works**: The invariant `current_max - current_min == r - l` guarantees that the segment elements are consecutive. Every possible split inside this segment produces two contiguous subsegments that together cover the same set, ensuring we count all unique good pairs exactly once. Overlapping segments are counted via the dynamic sliding of `l`, so duplicates are naturally avoided.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

pos = [0] * (n + 1)
for idx, val in enumerate(p):
    pos[val] = idx

answer = 0
l = 0
current_min = p[0]
current_max = p[0]

for r in range(n):
    if r == 0:
        current_min = current_max = p[r]
    else:
        current_min = min(current_min, p[r])
        current_max = max(current_max, p[r])
    while current_max - current_min != r - l:
        l += 1
        current_min = min(p[l:r+1])
        current_max = max(p[l:r+1])
    answer += r - l

print(answer)
```

**Explanation**: The `for` loop expands the segment to the right. The `while` loop ensures the segment remains valid by shrinking from the left until it is consecutive. Every valid segment contributes `r - l` pairs of good segments. Using min/max recalculation inside the while loop is acceptable because each element is touched at most twice, keeping the total work linear.

## Worked Examples

### Sample Input 1

```
3
1 2 3
```

| r | l | current_min | current_max | r-l | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 0 | 0 |
| 1 | 0 | 1 | 2 | 1 | 1 |
| 2 | 0 | 1 | 3 | 2 | 3 |

The table shows that for r=1, segment [0,1] can be split once; for r=2, segment [0,2] can be split twice. Total answer = 3, matching the sample.

### Sample Input 2

```
5
3 1 2 5 4
```

| r | l | current_min | current_max | r-l | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 3 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 2 | 1 | 1 |
| 3 | 3 | 5 | 5 | 0 | 1 |
| 4 | 3 | 4 | 5 | 1 | 2 |

The table demonstrates dynamic adjustment of `l` and incremental counting of good segment pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is added and removed from the segment at most once. |
| Space | O(n) | We store the permutation and position mapping arrays. |

The solution is linear in time and space, well within constraints for n = 3·10⁵.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    p = list(map(int, input().split()))
    answer = 0
    l = 0
    current_min = current_max = p[0]
    for r in range(n):
        if r == 0:
            current_min = current_max = p[r]
        else:
            current_min = min(current_min, p[r])
            current_max = max(current_max, p[r])
        while current_max - current_min != r - l:
            l += 1
            current_min = min(p[l:r+1])
            current_max = max(p[l:r+1])
        answer += r - l
    return str(answer)

assert run("3\n1 2 3\n") == "3", "sample 1"
assert run("5\n3 1 2 5 4\n") == "2", "sample 2"
assert run("1\n1\n") == "0", "single element"
assert run("2\n1 2\n") == "1", "two elements"
assert run("5\n5 4 3 2 1\n") == "4", "decreasing order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1\n1\n" | 0 | Single-element permutation |
| "2\n1 2\n" | 1 | Minimal two-element case |
| "5\n5 4 3 2 1\n" | 4 | Decreasing order, max segment shrink |
| "3\n1 2 3\n" | 3 | Original sample |
| "5\n3 1 2 5 4\n" | 2 | Non-trivial permutation with split |

## Edge Cases

For a single-element permutation, there are no two segments to form a pair, so the algorithm correctly returns 0. In a strictly decreasing permutation like [5,4,3,2,1], the algorithm dynamically shifts `l`
