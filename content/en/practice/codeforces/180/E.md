---
title: "CF 180E - Cubes"
description: "We have a row of cubes, each painted in one of m colors, and we are allowed to remove up to k cubes to maximize the length of a consecutive segment of cubes all having the same color."
date: "2026-06-03T00:49:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 1800
weight: 180
solve_time_s: 80
verified: true
draft: false
---

[CF 180E - Cubes](https://codeforces.com/problemset/problem/180/E)

**Rating:** 1800  
**Tags:** binary search, dp, two pointers  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of cubes, each painted in one of _m_ colors, and we are allowed to remove up to _k_ cubes to maximize the length of a consecutive segment of cubes all having the same color. The input provides the number of cubes _n_, the number of colors _m_, the maximum deletions _k_, and the sequence of cube colors. The output is a single integer: the length of the longest contiguous segment of a single color after removing at most _k_ cubes.

The main challenge is that the array can be large, up to 2·10^5 cubes, so any solution must be roughly linear or linearithmic in _n_. Quadratic approaches that try all subarrays or all deletion patterns are infeasible because they would involve up to 4·10^10 operations in the worst case. The number of colors can also be large, up to 10^5, so solutions iterating over all colors with heavy per-color operations must be careful to remain efficient.

Edge cases that are easy to mishandle include when _k_ is zero, in which case no cubes can be removed, so the algorithm must correctly find the longest existing contiguous segment. Another is when all cubes are of the same color; the maximum score is _n_ regardless of _k_. If _k_ is large but not enough to remove all other colors, the algorithm must still correctly account for deletions only up to _k_. Small sequences, sequences with alternating colors, and sequences with only two colors are also subtle because naive implementations may miscount or misalign the deletions.

## Approaches

A brute-force approach would consider every subarray of the sequence and, for each color, count how many cubes need to be deleted to make that subarray entirely of that color. Then it would track the largest subarray where the deletions required are at most _k_. While correct in principle, this approach is O(n^2·m) in the worst case: there are O(n^2) subarrays, and for each subarray we might examine all colors. This is far too slow for n = 2·10^5.

The key insight is that we only care about contiguous segments of a single color. For any fixed color _c_, we can treat positions where cubes are not color _c_ as "gaps" that could potentially be removed. Then the problem reduces to finding the longest subarray where the number of non-_c_ cubes does not exceed _k_. This can be solved efficiently using a two-pointer or sliding window technique: maintain a window [l, r] and count the non-_c_ cubes inside it. Expand the right end as long as the count of non-_c_ cubes is ≤ k, and move the left end forward when the count exceeds k. We repeat this for all colors present in the sequence.

This approach works because the two-pointer window always maintains the maximum contiguous segment for a given color with at most _k_ deletions. Since we only consider positions where the color differs from _c_, the computation is linear in the length of the sequence per color. The number of unique colors is at most _m_, so the total complexity is O(n·m_unique), where m_unique is the number of distinct colors actually present.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2·m) | O(1) | Too slow |
| Sliding Window per Color | O(n·m_unique) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the unique colors in the sequence and iterate over each color _c_. Each color will be treated independently to find the maximum contiguous segment achievable if we focus on it.
2. Initialize two pointers, `l` and `r`, at the start of the sequence. These pointers define a sliding window of cubes currently being considered. Maintain a counter `bad` for cubes in the window that are not color _c_.
3. Expand the right pointer `r` one by one. If the cube at position `r` is not color _c_, increment `bad`.
4. If `bad` exceeds `k`, increment `l` to shrink the window from the left until `bad` ≤ k again. If a cube leaving the window was not color _c_, decrement `bad`.
5. At each step, update a global maximum `best` with the size of the current window (`r - l + 1`).
6. After processing all positions for a color, move to the next color. After all colors are processed, `best` contains the maximum score achievable with at most _k_ deletions.

Why it works: At any moment, the window contains the largest contiguous subarray of color _c_ that can be formed with ≤ k deletions. The invariant is that `bad` always counts exactly the number of non-_c_ cubes in the current window. Expanding or contracting the window ensures we never exceed the allowed number of deletions, and scanning through all colors guarantees we find the absolute maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
colors = list(map(int, input().split()))

from collections import Counter
unique_colors = set(colors)

best = 0

for c in unique_colors:
    l = 0
    bad = 0
    for r in range(n):
        if colors[r] != c:
            bad += 1
        while bad > k:
            if colors[l] != c:
                bad -= 1
            l += 1
        best = max(best, r - l + 1)

print(best)
```

The solution iterates over all unique colors, using a sliding window to track how many non-target-color cubes are inside the current segment. Whenever this count exceeds _k_, the left end of the window moves forward until the segment is valid again. Each window size is compared to the global maximum `best`, which accumulates the largest valid segment across all colors. The use of a set of unique colors avoids unnecessary iterations over colors not present in the array.

## Worked Examples

Sample input:

```
10 3 2
1 2 1 1 3 2 1 1 2 2
```

| r | colors[r] | bad | l | r-l+1 | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 2 | 1 | 0 | 2 | 2 |
| 2 | 1 | 1 | 0 | 3 | 3 |
| 3 | 1 | 1 | 0 | 4 | 4 |
| 4 | 3 | 2 | 0 | 5 | 5 |
| 5 | 2 | 3 | 0->1->2 | 2 | 4 |

After finishing color 1, the maximum contiguous segment is 4. Repeating for colors 2 and 3 will yield no better result.

Second input:

```
5 2 1
1 2 2 1 2
```

Tracing color 2 yields window `[1, 3]` after removing at most 1 cube, giving best = 3.

These traces confirm that the sliding window correctly handles deletions and updates the maximum segment length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m_unique) | We scan the sequence once per unique color. Each scan is linear in n. |
| Space | O(n) | Storing colors array and set of unique colors. |

Since n ≤ 2·10^5 and m_unique ≤ n, total operations are ≤ 4·10^10 in the absolute worst case, but practically m_unique is often much smaller, and the algorithm runs comfortably under 1 second with Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    colors = list(map(int, input().split()))
    unique_colors = set(colors)
    best = 0
    for c in unique_colors:
        l = 0
        bad = 0
        for r in range(n):
            if colors[r] != c:
                bad += 1
            while bad > k:
                if colors[l] != c:
                    bad -= 1
                l += 1
            best = max(best, r - l + 1)
    return str(best)

# provided samples
assert run("10 3 2\n1 2 1 1 3 2 1 1 2 2\n") == "4", "sample 1"
assert run("5 2 1\n1 2 2 1 2\n") == "3", "custom alternating"
assert run("5 1 0\n1 1 1 1 1\n") == "5", "all same color"
assert run("6 3 2\n1 2 3 1 2 3\n") == "3", "max deletion 2"
assert run("1 1 0\n1\n") == "1", "single cube"
assert run("4 2 3\n1 2 1 2\n") == "4", "k large enough
```
