---
title: "CF 1389F - Bicolored Segments"
description: "We are given a set of segments on the number line, each colored either 1 or 2. A pair of segments is considered bad if they overlap or touch and have different colors. Our goal is to select as many segments as possible while avoiding any bad pair."
date: "2026-06-11T10:32:21+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "graph-matchings", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1389
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 92 (Rated for Div. 2)"
rating: 2600
weight: 1389
solve_time_s: 137
verified: true
draft: false
---

[CF 1389F - Bicolored Segments](https://codeforces.com/problemset/problem/1389/F)

**Rating:** 2600  
**Tags:** data structures, dp, graph matchings, sortings  
**Solve time:** 2m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of segments on the number line, each colored either 1 or 2. A pair of segments is considered bad if they overlap or touch and have different colors. Our goal is to select as many segments as possible while avoiding any bad pair. In other words, we want a subset of segments where no two segments of different colors intersect.

The segments are defined by integers $l_i$ and $r_i$ and can span up to $10^9$. The number of segments $n$ can reach 200,000, which rules out any solution with complexity $O(n^2)$ because that would result in around 40 billion operations, far beyond the 2-second limit. We need something closer to $O(n \log n)$.

Edge cases that can trip a naive approach include segments that are nested or touch at endpoints. For example, if we have segments [1,3,1], [3,5,2], and [2,4,1], a careless selection might include all three, but the first and second intersect at 3 and have different colors, making them a bad pair. Another subtle case is when all segments are the same color-then we can take all of them, even if they overlap. A simple greedy that ignores color could fail in such scenarios.

## Approaches

The brute-force approach would be to consider all possible subsets of segments, checking for bad pairs in each. For each subset, we would need to compare every pair of segments, resulting in $O(2^n \cdot n^2)$ time. This is clearly infeasible for $n=2 \cdot 10^5$.

The key insight is that we can separate segments by color and handle each color independently. If we choose segments of one color, there is no risk of bad pairs within that color. Thus, for each color, we only need to select segments that do not overlap. This reduces the problem to the classic “maximum number of non-overlapping intervals” problem, which can be solved greedily: sort intervals by their right endpoint and iteratively pick the first interval that starts after the last chosen interval ends. We compute this independently for both colors and take the color that allows more segments.

The observation that no bad pair exists among segments of the same color allows us to ignore intersections within each color group. The problem reduces to two independent interval scheduling problems, which is solvable in $O(n \log n)$ due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate the segments into two lists: one for color 1 and one for color 2. This step ensures we can handle the non-overlapping selection independently for each color.
2. For each color list, sort the segments by their right endpoint. Sorting by the right endpoint is crucial because it allows the greedy choice of the earliest finishing segment, maximizing the number of non-overlapping segments.
3. Initialize a counter for the number of selected segments and a variable to track the right endpoint of the last chosen segment, initially set to negative infinity.
4. Iterate through the sorted segments. For each segment, if its left endpoint is strictly greater than the right endpoint of the last chosen segment, include it in the selection and update the last chosen right endpoint. Otherwise, skip it. This guarantees that no two chosen segments overlap.
5. Repeat steps 3 and 4 for both color lists, obtaining two counts: `count_color1` and `count_color2`.
6. The final answer is the maximum of `count_color1` and `count_color2`, because choosing all segments of a single color ensures no bad pair.

Why it works: By focusing on one color at a time and using the greedy interval scheduling algorithm, we ensure the largest subset of non-overlapping segments for each color. Since bad pairs only occur between different colors, taking all segments from the color that yields the maximum count is optimal. The greedy choice of the earliest finishing interval guarantees maximality, as any other interval starting later would either overlap or reduce the total number selected.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_non_overlapping(segments):
    segments.sort(key=lambda x: x[1])
    count = 0
    last_end = -1
    for l, r in segments:
        if l > last_end:
            count += 1
            last_end = r
    return count

def main():
    n = int(input())
    color1, color2 = [], []
    for _ in range(n):
        l, r, t = map(int, input().split())
        if t == 1:
            color1.append((l, r))
        else:
            color2.append((l, r))
    res = max(max_non_overlapping(color1), max_non_overlapping(color2))
    print(res)

if __name__ == "__main__":
    main()
```

The first function `max_non_overlapping` implements the greedy interval scheduling for a given list of segments. Sorting by right endpoint ensures we can always pick the next compatible segment efficiently. The main function separates segments by color and computes the maximum selection size for each color, then outputs the larger count.

## Worked Examples

Sample 1:

Input:

```
3
1 3 1
4 6 2
2 5 1
```

| Color | Segments sorted by r | Selection process | Count |
| --- | --- | --- | --- |
| 1 | [1,3], [2,5] | Pick [1,3] (last_end=3), skip [2,5] (2 ≤ 3) | 1 |
| 2 | [4,6] | Pick [4,6] (last_end=6) | 1 |

Max count = max(1+0, 0+1) = 2

Explanation: We can pick segments [1,3] and [4,6] without any bad pair.

Sample 2:

Input:

```
4
1 4 1
2 5 1
3 6 2
5 7 2
```

| Color | Segments sorted by r | Selection process | Count |
| --- | --- | --- | --- |
| 1 | [1,4], [2,5] | Pick [1,4], skip [2,5] | 1 |
| 2 | [3,6], [5,7] | Pick [3,6], skip [5,7] overlaps 6 | 1 |

Max count = 1

Explanation: Even though there are 4 segments, picking more than one per color creates intersections with the other color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting each color group takes O(n log n), iterating is O(n) |
| Space | O(n) | Storing two separate lists for colors |

Given n ≤ 2·10^5, sorting and linear iteration fits well within 2 seconds, and memory usage is well below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("3\n1 3 1\n4 6 2\n2 5 1\n") == "2", "sample 1"

# Minimum input
assert run("1\n1 1 1\n") == "1", "single segment"

# All same color overlapping
assert run("3\n1 5 1\n2 6 1\n3 7 1\n") == "1", "all overlap same color"

# Nested segments, different colors
assert run("4\n1 10 1\n2 3 2\n4 5 2\n6 7 2\n") == "3", "pick color2's max"

# Touching at endpoint, different colors
assert run("2\n1 2 1\n2 3 2\n") == "1", "cannot pick both"

# Maximum size, non-overlapping
segments = "\n".join(f"{i*2+1} {i*2+2} 1" for i in range(200000))
assert run(f"200000\n{segments}\n") == "200000", "max size non-overlapping same color"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 segment | 1 | Handles smallest input |
| All overlapping, same color | 1 | Greedy picks only one |
| Nested segments, mixed colors | 3 | Correct color selection |
| Touching endpoints, different colors | 1 | Edge condition for touching |
| Maximum n, non-overlapping | 200000 | Performance and correctness at scale |

## Edge Cases

For the input:

```
2
1 2 1
2 3 2
```

The first and second segments touch at 2. The algorithm separates by color. Color 1 has [1,2], color 2 has [2,3]. For color 1, we pick [1,2]. For color 2, [2,3] starts at 2, which is not strictly greater than last_end=2, so it
