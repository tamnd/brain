---
title: "CF 976C - Nested Segments"
description: "We are given a collection of closed intervals on a number line. Each interval represents a segment with a left endpoint and a right endpoint, and we need to determine whether there exists a pair of distinct segments such that one is fully contained inside the other."
date: "2026-06-17T01:29:46+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 976
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 43 (Rated for Div. 2)"
rating: 1500
weight: 976
solve_time_s: 76
verified: true
draft: false
---

[CF 976C - Nested Segments](https://codeforces.com/problemset/problem/976/C)

**Rating:** 1500  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of closed intervals on a number line. Each interval represents a segment with a left endpoint and a right endpoint, and we need to determine whether there exists a pair of distinct segments such that one is fully contained inside the other.

Formally, for two segments $[l_i, r_i]$ and $[l_j, r_j]$, we want to find indices $i \neq j$ such that $l_i \ge l_j$ and $r_i \le r_j$. If such a pair exists, we return the indices of any valid nested pair; otherwise we report that no nesting exists.

The constraints allow up to $3 \cdot 10^5$ segments, and endpoints can be as large as $10^9$. This immediately rules out any quadratic comparison strategy. A naive $O(n^2)$ scan would perform about $9 \cdot 10^{10}$ comparisons in the worst case, which is far beyond what can execute in two seconds.

The key difficulty is that containment depends on two dimensions simultaneously. Sorting by only one coordinate does not automatically preserve the other, so careless ordering can hide valid answers.

A few edge situations illustrate common pitfalls. If all segments are identical, any pair is valid and must be detected; a solution that only looks for strict inequality may incorrectly miss this. If segments are strictly increasing in both endpoints like $[1,2], [2,3], [3,4]$, there is no containment even though intervals overlap in a structured way. Another tricky case is when a segment is very long and contains many others, for example $[1,100]$ containing $[2,99]$, $[3,98]$, and so on. An algorithm that only compares neighbors in the original order would fail here unless the structure is reorganized.

## Approaches

A brute-force approach checks every pair of segments and verifies whether one contains the other. This is straightforward: for each $i$, compare it with all $j > i$ and test the containment condition. This is correct because it explicitly evaluates all possible pairs, but its cost grows quadratically. With $3 \cdot 10^5$ segments, the number of comparisons becomes prohibitive, and even optimized constant factors cannot salvage it.

The key observation is that containment becomes much easier to detect if we reduce the problem to a carefully chosen ordering. If we sort segments by their left endpoint in ascending order, then any potential container must appear earlier or at the same position in this ordering. However, this is still insufficient because among segments with the same left endpoint, the one with the larger right endpoint should be considered the outer segment.

This leads to a more precise structure: sort by left endpoint ascending, and for ties sort by right endpoint descending. Once in this order, whenever we scan through the list, any segment that starts earlier or at the same point and ends later is a potential container for all later segments.

We then maintain the best (largest right endpoint) segment seen so far while scanning. If the current segment ends at or before this maximum, it is contained in a previously seen segment. Otherwise, it becomes the new candidate container.

This turns a two-dimensional comparison problem into a single pass with a maintained invariant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sorted sweep with tracking | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform the problem into detecting a containment relationship while scanning a sorted list.

1. Attach indices to all segments so we can return original positions after sorting. This is necessary because sorting destroys input order.
2. Sort segments by increasing left endpoint. If two segments share the same left endpoint, sort by decreasing right endpoint. This ordering ensures that for equal starts, the widest interval comes first, which is the only one that can contain others with the same left boundary.
3. Initialize two variables: one to store the maximum right endpoint seen so far, and another to store which segment achieved that maximum.
4. Iterate through the sorted segments from left to right. For each segment $[l, r]$, compare its right endpoint with the current maximum right endpoint.
5. If $r \le \text{maxR}$, then this segment is fully contained in the segment that produced $\text{maxR}$, because that segment started no later and extends at least as far right.
6. If no containment is found, and the current segment’s right endpoint is larger than $\text{maxR}$, update the stored best segment to this one.

The crucial reasoning step is that once we ensure the sorted order, the only missing condition for containment is the right endpoint comparison, because the left endpoint condition is already implicitly enforced by the ordering.

### Why it works

At every step of the scan, the segment stored as having the maximum right endpoint among all previously seen segments is guaranteed to be a valid candidate container for any future segment, because it has the smallest possible left endpoint among those with the largest reach to the right. Any segment that fails the containment test must extend further right than all previous segments, in which case it becomes the new best candidate. This invariant ensures that if a containment pair exists, it will be detected exactly when we encounter the inner segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
segs = []

for i in range(n):
    l, r = map(int, input().split())
    segs.append((l, r, i + 1))

segs.sort(key=lambda x: (x[0], -x[1]))

best_r = -1
best_idx = -1

for l, r, idx in segs:
    if r <= best_r:
        print(idx, best_idx)
        sys.exit(0)
    if r > best_r:
        best_r = r
        best_idx = idx

print(-1, -1)
```

The solution begins by preserving original indices, since sorting changes ordering but the output must refer to input positions. The sorting step is the structural transformation that makes containment detectable in a single pass.

During the scan, `best_r` represents the furthest right endpoint seen so far among segments that are potential containers. If we find a segment whose right endpoint does not exceed this value, it must be fully covered by that earlier segment because earlier segments also have left endpoints less than or equal to the current one due to sorting.

The early exit is safe because once a valid pair is found, any pair is acceptable.

## Worked Examples

### Example 1

Input:

```
5
1 10
2 9
3 9
2 3
2 9
```

Sorted order (l asc, r desc):

| Step | Segment | best_r | best_idx | Action |
| --- | --- | --- | --- | --- |
| 1 | (1,10,1) | 10 | 1 | update |
| 2 | (2,9,2) | 10 | 1 | 9 ≤ 10 → answer |

At step 2, segment 2 ends inside segment 1, so we output a valid pair.

This demonstrates how the first segment becomes a universal container candidate for later ones.

### Example 2

Input:

```
4
1 5
2 6
3 4
4 7
```

Sorted:

| Step | Segment | best_r | best_idx | Action |
| --- | --- | --- | --- | --- |
| 1 | (1,5,1) | 5 | 1 | update |
| 2 | (2,6,2) | 6 | 2 | update |
| 3 | (3,4,3) | 6 | 2 | 4 ≤ 6 → answer |

At step 3, segment (3,4) is contained in (2,6), confirming the invariant that the best segment so far is always sufficient to test containment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, scan is linear |
| Space | $O(n)$ | storing segments with indices |

The constraints allow up to $3 \cdot 10^5$ segments, so an $O(n \log n)$ approach is well within limits. The memory usage is linear and fits comfortably in the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    n = int(input())
    segs = []
    for i in range(n):
        l, r = map(int, input().split())
        segs.append((l, r, i + 1))

    segs.sort(key=lambda x: (x[0], -x[1]))

    best_r = -1
    best_idx = -1

    for l, r, idx in segs:
        if r <= best_r:
            return f"{idx} {best_idx}"
        if r > best_r:
            best_r = r
            best_idx = idx

    return "-1 -1"

# provided sample
assert run("5\n1 10\n2 9\n3 9\n2 3\n2 9\n") in ["2 1", "3 1", "4 1", "5 1", "3 2", "4 2", "5 2", "2 5", "4 5"], "sample 1"

# all identical segments
assert run("3\n1 1\n1 1\n1 1\n") != "-1 -1"

# no nesting
assert run("3\n1 2\n2 3\n3 4\n") == "-1 -1"

# clear nesting
assert run("3\n1 10\n2 5\n6 9\n") != "-1 -1"

# reverse nested chain
assert run("4\n1 8\n2 7\n3 6\n4 5\n") != "-1 -1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all identical segments | any valid pair | duplicates are handled |
| increasing chain | -1 -1 | no false positives |
| clear nesting | valid pair | basic correctness |
| deep chain | valid pair | worst-case nesting structure |

## Edge Cases

One subtle case is when multiple segments share the same left endpoint. For example:

```
3
1 10
1 5
1 7
```

After sorting by right endpoint descending within equal left endpoints, the segment (1,10) appears first. As the scan progresses, `best_r` becomes 10 immediately, and all others are correctly detected as contained. Without the secondary sort, a shorter segment could incorrectly become the “best” and prevent detection.

Another case involves strictly increasing intervals:

```
3
1 2
2 3
3 4
```

Here, `best_r` always increases, and no segment ever satisfies `r <= best_r` at a meaningful time. The algorithm correctly reaches the end and returns `-1 -1`, reflecting the absence of containment.
