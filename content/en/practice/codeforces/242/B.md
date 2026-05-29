---
title: "CF 242B - Big Segment"
description: "We are given a list of segments on a number line, each defined by a left and right endpoint. The task is to find if there exists a single segment among them that fully contains every other segment."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 242
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 149 (Div. 2)"
rating: 1100
weight: 242
solve_time_s: 72
verified: true
draft: false
---

[CF 242B - Big Segment](https://codeforces.com/problemset/problem/242/B)

**Rating:** 1100  
**Tags:** implementation, sortings  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of segments on a number line, each defined by a left and right endpoint. The task is to find if there exists a single segment among them that fully contains every other segment. If such a segment exists, we should return its 1-based index; otherwise, we return -1.

The input size can reach up to 100,000 segments, and each coordinate can be as large as 1 billion. This rules out solutions that compare every segment against every other segment because an O(n²) algorithm would perform roughly 10¹⁰ operations, far exceeding the 2-second time limit. The output is a single integer, so the problem is essentially a search for a segment that satisfies a global containment property.

Non-obvious edge cases include scenarios where all segments are disjoint or equal in length but do not overlap fully. For example, if segments are `1 2`, `2 3`, and `3 4`, no single segment contains all others, so the output must be `-1`. Another subtle case occurs when there is only one segment; it trivially contains itself, so the output should be `1`.

## Approaches

A brute-force approach would be to check for each segment whether it contains all others. This requires two nested loops over all segments, giving O(n²) comparisons. While this works for very small `n`, it becomes infeasible when `n` is 100,000 because it results in tens of billions of operations.

The key observation for optimization is that a segment covers all others if and only if its left endpoint is the minimum among all left endpoints and its right endpoint is the maximum among all right endpoints. This reduces the problem to finding the minimum `l` and maximum `r`, then checking if any segment exactly matches these values. This approach reduces the time complexity from O(n²) to O(n) and uses only constant extra space apart from storing the segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all segments into a list along with their original indices to preserve input order. This allows us to return the correct 1-based index at the end.
2. Initialize two variables, `min_left` and `max_right`, to keep track of the smallest left endpoint and largest right endpoint among all segments.
3. Iterate through the segments. For each segment, update `min_left` if the segment’s left endpoint is smaller and update `max_right` if the segment’s right endpoint is larger.
4. After the first pass, iterate through the segments again to find a segment whose left endpoint equals `min_left` and right endpoint equals `max_right`. If such a segment exists, return its index; otherwise, return -1.

The invariant is that any segment covering all others must have its left endpoint equal to the global minimum and right endpoint equal to the global maximum. This guarantees that no other segment extends beyond it.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
segments = []

min_left = float('inf')
max_right = float('-inf')

for i in range(n):
    l, r = map(int, input().split())
    segments.append((l, r, i + 1))  # store 1-based index
    if l < min_left:
        min_left = l
    if r > max_right:
        max_right = r

answer = -1
for l, r, idx in segments:
    if l == min_left and r == max_right:
        answer = idx
        break

print(answer)
```

This solution reads the segments, computes the global minimum left and maximum right endpoints, and checks for a segment that matches both. By storing the original index in the tuple, we can immediately return the 1-based position without additional searches. The only subtle points are initializing `min_left` and `max_right` to extremes to handle edge cases correctly and remembering to use the 1-based index when reporting the answer.

## Worked Examples

Sample 1:

Input:

```
3
1 1
2 2
3 3
```

| Segment | l | r | min_left | max_right | Candidate? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | No |
| 2 | 2 | 2 | 1 | 2 | No |
| 3 | 3 | 3 | 1 | 3 | No |

After processing, no segment matches `min_left=1` and `max_right=3`. Output is `-1`.

Sample 2:

Input:

```
4
1 5
2 3
1 5
4 5
```

| Segment | l | r | min_left | max_right | Candidate? |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 1 | 5 | Yes |

The first segment matches both `min_left` and `max_right`, so we return index `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each segment is processed twice: once to find min/max and once to check coverage |
| Space | O(n) | Store all segments to preserve original indices |

The solution easily fits within the 2-second limit for n=100,000 and the memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    segments = []
    min_left = float('inf')
    max_right = float('-inf')
    for i in range(n):
        l, r = map(int, input().split())
        segments.append((l, r, i + 1))
        min_left = min(min_left, l)
        max_right = max(max_right, r)
    for l, r, idx in segments:
        if l == min_left and r == max_right:
            return str(idx)
    return "-1"

# provided sample
assert run("3\n1 1\n2 2\n3 3\n") == "-1", "sample 1"

# custom cases
assert run("1\n7 7\n") == "1", "single segment"
assert run("4\n1 5\n2 3\n1 5\n4 5\n") == "1", "segment covers all"
assert run("3\n2 4\n1 5\n3 5\n") == "2", "middle segment covers all"
assert run("5\n1 3\n2 4\n3 5\n2 5\n1 5\n") == "5", "last segment covers all"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n7 7` | 1 | Single segment trivially covers itself |
| `4\n1 5\n2 3\n1 5\n4 5` | 1 | Multiple segments, first segment covers all |
| `3\n2 4\n1 5\n3 5` | 2 | Middle segment covers all, tests order handling |
| `5\n1 3\n2 4\n3 5\n2 5\n1 5` | 5 | Last segment covers all, confirms correct index selection |

## Edge Cases

For the case with a single segment `1 1`, `min_left` and `max_right` both equal `1`. The segment matches both, so the output is `1`.

For segments that do not overlap fully, like `1 2`, `2 3`, `3 4`, `min_left` is `1` and `max_right` is `4`. No segment spans both, so the algorithm correctly outputs `-1`.

For multiple segments with identical min/max endpoints, the algorithm returns the first one in input order that satisfies the coverage condition, preserving the 1-based index requirement.
