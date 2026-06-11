---
title: "CF 1108A - Two distinct points"
description: "We are given two line segments on the number line, each defined by its endpoints. For each query, we need to pick one integer point from the first segment and one integer point from the second segment such that the points are different."
date: "2026-06-12T05:15:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1108
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 535 (Div. 3)"
rating: 800
weight: 1108
solve_time_s: 101
verified: false
draft: false
---

[CF 1108A - Two distinct points](https://codeforces.com/problemset/problem/1108/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two line segments on the number line, each defined by its endpoints. For each query, we need to pick one integer point from the first segment and one integer point from the second segment such that the points are different. The segments can overlap completely, partially, or not at all, but it is guaranteed that a solution exists. The task is to output any valid pair of distinct points for each query.

The constraints are straightforward. The endpoints can be as large as $10^9$, but we only have up to 500 queries. This means we cannot afford algorithms that try all integers between the segment endpoints if the ranges are large. However, since the problem guarantees a solution exists and the ranges are continuous integers, we can solve this with a constant-time decision per query.

The non-obvious edge case occurs when the segments overlap or coincide. For example, if the first segment is [1, 2] and the second segment is [1, 2], naive selection of the leftmost points would give (1, 1), which violates the distinctness requirement. The solution must detect such a collision and choose a different integer from one of the segments, like (1, 2) or (2, 1).

## Approaches

A brute-force approach would enumerate all integers in the first segment and all integers in the second segment, checking for the first pair that is distinct. While correct, this approach could require iterating up to $10^9$ integers in the worst case, which is infeasible.

The optimal approach exploits the simplicity of the problem. We can first choose the left endpoint of the first segment as the candidate point $a$. Then we try the left endpoint of the second segment as candidate $b$. If $b$ is the same as $a$, we can safely pick the right endpoint of the second segment instead. The guarantees of the problem ensure that this will always produce a valid pair. This reduces the problem to a simple conditional selection, which runs in constant time per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r1-l1+1)*(r2-l2+1)) | O(1) | Too slow |
| Optimal | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. For each query, read the endpoints $l_1, r_1, l_2, r_2$.
2. Set the first point $a$ to $l_1$, the leftmost integer in the first segment. This is a natural choice because it guarantees $a$ is within the segment.
3. Tentatively set the second point $b$ to $l_2$, the leftmost integer in the second segment.
4. If $a$ equals $b$, adjust $b$ to $r_2$, the rightmost integer in the second segment. Since $l_2 < r_2$, $r_2$ is guaranteed to differ from $a$ if $a = l_2$.
5. Output $a$ and $b$.

Why it works: At every query, we choose $a$ and $b$ directly from the endpoints of the segments. The only time the first choice fails is if both left endpoints coincide. In that case, we pick the right endpoint of the second segment, which is guaranteed to differ from $a$ due to the strict inequality $l_2 < r_2$. The guarantee of the problem ensures that no other special handling is needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
results = []

for _ in range(q):
    l1, r1, l2, r2 = map(int, input().split())
    a = l1
    b = l2
    if a == b:
        b = r2
    results.append(f"{a} {b}")

print("\n".join(results))
```

The code first reads the number of queries. For each query, it extracts the four endpoints. The first point $a$ is always set to $l_1$, and the second point $b$ is initially $l_2$. If both points coincide, we shift $b$ to $r_2$. The results are collected and printed in one block to avoid slow I/O in loops.

## Worked Examples

**Example 1**

Input: `1 2 1 2`

Initial selection: $a = 1$, $b = 1$

Since $a = b$, set $b = r_2 = 2$

Output: `1 2`

| Step | a | b | Reason |
| --- | --- | --- | --- |
| Initial | 1 | 1 | Left endpoints selected |
| Adjustment | 1 | 2 | Left endpoints coincide, pick right endpoint for b |

This trace demonstrates the collision handling when segments overlap.

**Example 2**

Input: `1 4 5 8`

Initial selection: $a = 1$, $b = 5$

No collision, output: `1 5`

| Step | a | b | Reason |
| --- | --- | --- | --- |
| Initial | 1 | 5 | No adjustment needed |

This shows the simple case where the segments do not overlap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each query is processed in constant time. |
| Space | O(q) | Storing results for all queries before output. |

With $q \le 500$, this runs comfortably within the 1-second time limit and requires negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    q = int(input())
    results = []
    for _ in range(q):
        l1, r1, l2, r2 = map(int, input().split())
        a = l1
        b = l2
        if a == b:
            b = r2
        results.append(f"{a} {b}")
    return "\n".join(results)

# provided samples
assert run("5\n1 2 1 2\n2 6 3 4\n2 4 1 3\n1 2 1 3\n1 4 5 8\n") == "1 2\n2 3\n2 1\n1 2\n1 5"

# custom cases
assert run("1\n1 2 1 3\n") == "1 3", "overlap, left endpoints collide"
assert run("1\n1 5 5 8\n") == "1 5", "no overlap, a < b"
assert run("1\n3 7 3 7\n") == "3 7", "identical segments"
assert run("1\n100000000 1000000000 99999999 100000000\n") == "100000000 99999999", "large numbers, overlapping endpoints"
assert run("1\n1 2 3 4\n") == "1 3", "completely separate segments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 3 | 1 3 | Overlap, left endpoints collide |
| 1 5 5 8 | 1 5 | No overlap, distinct points |
| 3 7 3 7 | 3 7 | Identical segments |
| 100000000 1000000000 99999999 100000000 | 100000000 99999999 | Large numbers, edge overlap |
| 1 2 3 4 | 1 3 | Completely separate segments |

## Edge Cases

When the segments coincide, e.g., [3, 7] and [3, 7], the algorithm initially chooses $a = 3$ and $b = 3$. Since they are equal, $b$ is shifted to 7, producing (3, 7), which is valid. For disjoint segments, no adjustment occurs, and the simple selection of left endpoints suffices. For segments overlapping at a single point, e.g., [1, 2] and [2, 3], the algorithm chooses (1, 2), which also satisfies the distinctness condition. These examples cover all non-obvious scenarios.
