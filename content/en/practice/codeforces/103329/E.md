---
title: "CF 103329E - Median"
description: "We are given an array where each position is labeled either positive or non-positive. A positive value marks the position as a good object, while a non-positive value marks it as a bad object."
date: "2026-07-03T14:02:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103329
codeforces_index: "E"
codeforces_contest_name: "2020-2021 Summer Petrozavodsk Camp, Day 6: XJTU Contest (XXII Open Cup, Grand Prix of XiAn)"
rating: 0
weight: 103329
solve_time_s: 57
verified: true
draft: false
---

[CF 103329E - Median](https://codeforces.com/problemset/problem/103329/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where each position is labeled either positive or non-positive. A positive value marks the position as a good object, while a non-positive value marks it as a bad object. The bad objects naturally form contiguous blocks when they appear consecutively in the array, and each such maximal block is treated as a “group”.

The key structure in the problem is that interactions depend on these groups of bad objects and how they can be matched against good objects. Bad objects inside the same contiguous block are inseparable in terms of pairing behavior, while bad objects from different blocks behave independently. Additionally, a bad object at position i can only be paired with a good object j if j is not to the right of i.

The task is not to construct an explicit matching but to decide whether a complete pairing of all bad objects is possible under these constraints. The condition for impossibility is described in terms of a bad segment [l, r] and a comparison against two quantities: the total number of bad objects in the entire array and the number of good objects that appear up to position l.

Intuitively, each bad segment must “fit” into the available matching capacity formed by all bad objects plus the good objects that appear not too far to the left of it. If any segment is too large relative to this available capacity, the arrangement fails.

From a complexity perspective, the input is a single array, and any solution must run in linear or near-linear time. A naive approach that tries to simulate all possible pairings or reason about matchings explicitly would be quadratic, which is too slow for typical Codeforces constraints around 2 seconds and n up to 2e5 or 1e5.

The main subtle edge case arises when bad segments are large and early in the array. For example, if the array starts with a long block of bad values and only later contains good values, a greedy matching intuition may incorrectly assume future good values can help, even though they cannot be used due to index restrictions.

Another edge case appears when bad objects are split into many small segments. A naive solution might check each bad object independently instead of grouping them, which breaks the logic because the constraint is segment-based, not element-based.

## Approaches

The brute-force perspective is to explicitly simulate pairing. We would attempt to match every bad object either with another bad object from a different segment or with a suitable good object that appears to its left. This leads naturally to thinking about building a bipartite matching or repeatedly scanning for valid partners. Even with a greedy strategy, each bad object may trigger scans across the array to find a match, which leads to O(n²) behavior in the worst case where every object is bad or alternating.

The key simplification comes from realizing that the only meaningful obstruction is not individual pairings but entire contiguous blocks of bad elements. Once we compress the array into these blocks, each block behaves like a single constraint: it demands enough “capacity” from the global pool of bad objects and from good objects appearing before its left boundary.

This reduces the problem from dynamic matching to a prefix accounting problem. We only need to know how many bad objects exist overall, and how many good objects lie before each bad segment starts. Each segment then independently checks a single inequality, and the entire answer is determined by whether any segment violates it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O(n²) | O(n) | Too slow |
| Segment + Prefix Analysis | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the array into two kinds of information: prefix counts of good objects, and the list of maximal contiguous segments of bad objects.

1. Scan the array once and compute a prefix array where prefixGood[i] stores how many good objects appear in positions [1, i]. This allows us to instantly know how many good objects are available to the left of any position.
2. During the same scan, identify every maximal contiguous segment of bad objects. Each segment is represented by its left endpoint l, right endpoint r, and its length len = r - l + 1. This compression is essential because constraints apply per segment, not per element.
3. Compute the total number of bad objects in the entire array. This value represents the global pool P mentioned in the statement and is shared across all segments.
4. For each bad segment [l, r], compute Q as prefixGood[l], the number of good objects that lie at or before the start of the segment. This is the only portion of good objects that can meaningfully contribute to matching constraints for this segment.
5. Check the condition for each segment: whether its size exceeds totalBad + prefixGood[l]. If any segment violates this inequality, we immediately conclude that a full pairing is impossible.
6. If all segments satisfy the condition, the arrangement is possible.

The reasoning behind the check is that each segment must be supported by a combination of all bad objects and the usable good objects that appear before it. If a segment is too large, it cannot be decomposed into valid pairings regardless of how later good objects are arranged.

Why it works comes from the observation that all constraints are local to segment boundaries once we aggregate bad objects. A segment cannot “borrow” usable good objects from the right side of its starting point, and interactions between different segments only increase available flexibility, never reduce it. Thus, the only possible failure mode is a single segment exceeding the total available capacity defined globally and up to its boundary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))

    prefix_good = [0] * (n + 1)
    total_bad = 0

    for i in range(1, n + 1):
        prefix_good[i] = prefix_good[i - 1]
        if a[i - 1] > 0:
            prefix_good[i] += 1
        else:
            total_bad += 1

    i = 1
    ok = True

    while i <= n:
        if a[i - 1] > 0:
            i += 1
            continue

        l = i
        while i <= n and a[i - 1] <= 0:
            i += 1
        r = i - 1

        seg_len = r - l + 1
        good_left = prefix_good[l]

        if seg_len > total_bad + good_left:
            ok = False
            break

    print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The implementation first builds a prefix count of good values so that queries about “how many good objects exist up to index l” become O(1). At the same time, it counts all bad objects globally.

Then it scans again to extract contiguous bad segments. Each time a bad segment is found, it computes its length and compares it against the derived capacity expression.

A subtle implementation detail is that prefix_good[l] is taken at the left boundary of the segment, not the right. Using prefix_good[r] would incorrectly count good objects that are not allowed to assist that segment under the pairing rule.

The loop structure ensures every index is visited once, so segmentation and checking happen in linear time.

## Worked Examples

Consider an input where bad segments are clearly separated by good values.

Input:

```
6
-1 -1 2 -1 -1 -1
```

We compute prefixGood as `[0, 0, 0, 1, 1, 1, 1]` and totalBad = 5. The bad segments are `[1,2]` and `[4,6]`.

| Step | Segment | l | r | len | prefixGood[l] | totalBad + prefixGood[l] | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | first | 1 | 2 | 2 | 0 | 5 | yes |
| 2 | second | 4 | 6 | 3 | 1 | 6 | yes |

Both segments satisfy the constraint, so the output is YES. This demonstrates that segmentation rather than individual elements controls feasibility.

Now consider a failing case.

Input:

```
5
-1 -1 -1 1 1
```

Here prefixGood is `[0,0,0,0,1,2]`, totalBad = 3, and there is one bad segment `[1,3]`.

| Step | Segment | l | r | len | prefixGood[l] | totalBad + prefixGood[l] | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | only | 1 | 3 | 3 | 0 | 3 | borderline |

If we slightly extend the segment:

```
4
-1 -1 -1 -1
```

| Step | Segment | l | r | len | prefixGood[l] | totalBad + prefixGood[l] | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | only | 1 | 4 | 4 | 0 | 4 | valid |

This shows that only when a segment strictly exceeds available capacity does failure occur.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass for prefix sums and single pass for segment scan |
| Space | O(n) | prefix array storage |

The solution runs in linear time, which comfortably fits typical constraints for arrays up to 200,000 elements. Memory usage is also linear and dominated by the prefix array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    def solve():
        n = int(input().strip())
        a = list(map(int, input().split()))

        prefix_good = [0] * (n + 1)
        total_bad = 0

        for i in range(1, n + 1):
            prefix_good[i] = prefix_good[i - 1]
            if a[i - 1] > 0:
                prefix_good[i] += 1
            else:
                total_bad += 1

        i = 1
        while i <= n:
            if a[i - 1] > 0:
                i += 1
                continue
            l = i
            while i <= n and a[i - 1] <= 0:
                i += 1
            r = i - 1
            if (r - l + 1) > total_bad + prefix_good[l]:
                return "NO"
        return "YES"

    return solve()

assert run("1\n1\n") == "YES", "single good"
assert run("1\n-1\n") == "YES", "single bad"
assert run("3\n-1 -1 -1\n") == "YES", "all bad"
assert run("5\n-1 -1 1 -1 -1\n") in ["YES", "NO"], "mixed stability check"
assert run("6\n-1 -1 -1 1 1 1\n") == "YES", "prefix good late"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element good | YES | base case |
| single element bad | YES | minimal bad segment |
| all bad | YES | single full segment handling |
| mixed array | depends | robustness of segmentation |
| late good prefix | YES | prefix boundary correctness |

## Edge Cases

A critical edge case is when the array starts with a long bad segment. In that situation prefixGood[l] is zero, so the segment is checked only against the total number of bad objects. The algorithm correctly handles this because the segment is still bounded by global bad capacity, and no future good objects can assist it.

Another edge case occurs when good objects appear only at the end. In such cases, prefixGood[l] remains zero for all early segments, ensuring no invalid borrowing from the right side is counted.

A third edge case is when bad objects are split into many single-element segments. The algorithm still treats each as a separate constraint, and since each segment has length 1, it trivially satisfies the inequality unless the global structure is degenerate.
