---
title: "CF 448C - Painting Fence"
description: "We are asked to compute the minimum number of brush strokes needed to paint a fence of vertical planks. Each plank has a width of 1 meter and an individual height. The brush is exactly 1 meter wide, and it can be applied either vertically or horizontally."
date: "2026-06-07T17:06:51+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 448
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 256 (Div. 2)"
rating: 1900
weight: 448
solve_time_s: 91
verified: true
draft: false
---

[CF 448C - Painting Fence](https://codeforces.com/problemset/problem/448/C)

**Rating:** 1900  
**Tags:** divide and conquer, dp, greedy  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the minimum number of brush strokes needed to paint a fence of vertical planks. Each plank has a width of 1 meter and an individual height. The brush is exactly 1 meter wide, and it can be applied either vertically or horizontally. A vertical stroke paints an entire plank at once, while a horizontal stroke paints all contiguous planks at a certain height.

The input consists of `n`, the number of planks, followed by an array `a` of length `n`, representing the heights of the planks. The output is a single integer: the fewest strokes needed to cover the entire fence.

The constraints reveal that `n` can go up to 5000, and individual plank heights can reach 10^9. This means any algorithm that examines all pairs or triples of planks in a naive way could potentially perform tens of millions of operations and risk a TLE. We need an approach closer to O(n^2) or better.

Edge cases that often break naive solutions include fences where all heights are equal, fences with heights strictly increasing or decreasing, or fences with alternating high and low planks. For example, if the input is `1 1 1 1`, the answer is clearly 1, but a careless horizontal-first greedy algorithm might mistakenly consider multiple strokes.

## Approaches

A brute-force approach is simple: for each unpainted plank, we could paint it vertically, reducing its height to zero, then recurse on the remaining heights. While correct, this approach leads to exponential complexity because it considers all sequences of vertical strokes.

A slightly better approach is to use horizontal strokes greedily: at each step, find the minimum height among the unpainted section, paint that height across the entire interval, then recursively solve the segments above this minimum. This can be thought of as a divide-and-conquer approach: paint the base across the interval, then handle remaining "sub-fences" formed by planks taller than the minimum.

The key insight is that each stroke counts as one, whether vertical or horizontal, so we need to decide at each segment whether it is cheaper to paint planks individually with vertical strokes or use a horizontal stroke and solve recursively. For a given segment of length `len`, we can compute the minimal strokes as the minimum of `len` vertical strokes versus `min_height + sum(recursive calls on subsegments)`.

This approach works because the recursive structure guarantees that at each step, we either reduce the segment completely via vertical strokes or optimally reduce its height via a horizontal stroke and solve only the remaining parts. The total number of recursive calls is manageable because each call strictly reduces the range size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Horizontal + Divide & Conquer | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start with the full interval `[l, r)` of planks and an initial height offset `base` which is the height already painted by previous horizontal strokes.
2. If the interval is empty (`l >= r`), return 0.
3. Compute the minimum height in the current interval relative to `base`. This represents the height we can paint with a horizontal stroke.
4. Count the horizontal stroke to paint up to `min_height`.
5. Scan the interval and split it into contiguous subsegments of planks taller than `min_height`. For each subsegment, recursively compute the minimum strokes needed, adding them to the current horizontal stroke count.
6. Compare this total with simply painting each plank individually using vertical strokes (`r - l`) and return the smaller number.
7. Initially, call the function on the full interval `[0, n)` with `base = 0`.

Why it works: At each recursive step, the algorithm either counts a horizontal stroke and recursively solves only the unpainted segments, or counts vertical strokes. This ensures that we never undercount strokes, and the recursive divide ensures we always handle each plank exactly as needed. The invariant is that at every call, `base` represents the height already painted, so remaining heights are accurately represented.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10000)

def min_strokes(a, l, r, base):
    if l >= r:
        return 0
    min_h = min(a[l:r]) - base
    strokes = min_h
    i = l
    while i < r:
        if a[i] - base == min_h:
            i += 1
            continue
        j = i
        while j < r and a[j] - base > min_h:
            j += 1
        strokes += min_strokes(a, i, j, base + min_h)
        i = j
    return min(strokes, r - l)

def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(min_strokes(a, 0, n, 0))

if __name__ == "__main__":
    main()
```

The `min_strokes` function directly implements the recursive divide-and-conquer approach. We carefully handle empty intervals and correctly adjust `base` to account for heights already painted. Off-by-one errors are avoided by treating ranges as `[l, r)`.

## Worked Examples

Sample 1: `5 2 2 1 2 1`

| Interval | Base | Min Height | Segments | Horizontal Strokes | Vertical Option | Result |
| --- | --- | --- | --- | --- | --- | --- |
| [0,5) | 0 | 1 | [0,1],[1,2],[3,4] | 1 | 5 | 3 |
| [0,2) | 1 | 1 | [0,1],[1,2] | 1 | 2 | 2 |
| [3,4) | 1 | 1 | [3,4] | 1 | 1 | 1 |

This trace confirms the algorithm counts horizontal strokes across all planks at base height 1, then recursively solves the remaining parts optimally.

Sample 2: `1 4`

| Interval | Base | Min Height | Segments | Horizontal Strokes | Vertical Option | Result |
| --- | --- | --- | --- | --- | --- | --- |
| [0,1) | 0 | 4 | none | 4 | 1 | 1 |

The algorithm correctly chooses a single vertical stroke rather than 4 horizontal strokes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each interval can trigger up to `n` splits, and min computation is O(n) |
| Space | O(n) | Maximum recursion depth is `n` and auxiliary memory is O(1) |

With n ≤ 5000, the worst-case operations (≈25 million) are feasible within the 1s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    from contextlib import redirect_stdout
    output = io.StringIO()
    with redirect_stdout(output):
        main()
    return output.getvalue().strip()

# Provided samples
assert run("5\n2 2 1 2 1\n") == "3", "sample 1"
assert run("2\n1 3\n") == "2", "sample 2"
assert run("1\n1\n") == "1", "sample 3"

# Custom cases
assert run("4\n1 1 1 1\n") == "1", "all equal"
assert run("3\n3 2 3\n") == "3", "valley in the middle"
assert run("5\n5 4 3 2 1\n") == "5", "strictly decreasing"
assert run("6\n1 2 3 2 1 2\n") == "4", "peaks and valleys"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 1 1 1 1 | 1 | All equal heights, horizontal stroke optimal |
| 3 3 2 3 | 3 | Middle lower, split correctly |
| 5 5 4 3 2 1 | 5 | Strictly decreasing, vertical strokes optimal |
| 6 1 2 3 2 1 2 | 4 | Peaks and valleys, recursive splitting |

## Edge Cases

All-equal heights like `1 1 1 1` are handled correctly: the algorithm computes min height 1, applies one horizontal stroke, and finds no unpainted segments.

Single-plank cases like `1 4` are handled by comparing vertical strokes vs horizontal strokes, correctly choosing one vertical stroke.

Intervals with valleys such as `3 2 3` are split into `[0,1)` and `[2,3)`, with recursive horizontal strokes applied above the base, resulting in an optimal total of 3 strokes.

This approach reliably handles all identified edge cases by maintaining the invariant that `base` tracks the already-painted height, ensuring no plank is undercounted or overcounted.
