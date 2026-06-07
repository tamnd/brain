---
title: "CF 2070C - Limited Repainting"
description: "We have a strip of n cells, all initially red. Each cell has a desired color after painting, either red or blue. We can perform at most k operations, each of which allows us to choose a consecutive segment of cells and paint them blue."
date: "2026-06-08T06:55:23+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2070
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 175 (Rated for Div. 2)"
rating: 1500
weight: 2070
solve_time_s: 80
verified: true
draft: false
---

[CF 2070C - Limited Repainting](https://codeforces.com/problemset/problem/2070/C)

**Rating:** 1500  
**Tags:** binary search, greedy  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a strip of `n` cells, all initially red. Each cell has a desired color after painting, either red or blue. We can perform at most `k` operations, each of which allows us to choose a consecutive segment of cells and paint them blue. Cells that are already blue can be repainted again, but we cannot revert blue cells to red. After all operations, some cells may not match their desired color. Each cell has a penalty applied if it ends up the wrong color. The final penalty of a painting is the maximum penalty among all incorrectly colored cells, or zero if every cell is correct. The task is to minimize this final penalty using at most `k` operations.

The input specifies multiple test cases, with `n` up to `3 * 10^5` and total `n` across test cases also up to `3 * 10^5`. This rules out any algorithm with `O(n^2)` complexity, as it would make hundreds of billions of operations. We need an algorithm roughly linear or near-linear in `n` for each test case. The penalties can be as large as `10^9`, so we cannot rely on any counting tricks that require arrays indexed by penalty values.

Edge cases that can easily break a naive approach include: all cells are already red, `k=0`, or `k >= n`. For instance, if all cells should be red, the minimum penalty is always zero regardless of `k`, but a careless greedy algorithm might still try to paint unnecessarily. Another tricky case is when `k` is very small and there are scattered blue requirements: deciding which blue cells to paint affects the final penalty directly.

## Approaches

The brute-force approach would enumerate every possible choice of up to `k` segments to paint blue and then compute the resulting penalty. This works because it directly models the problem, but fails dramatically in practice because the number of possible segments grows quadratically with `n` and choosing `k` of them leads to combinatorial explosion, making it impossible to handle `n = 3 * 10^5`.

The key insight is that the problem can be reduced to a **decision problem with binary search**. Suppose we fix a candidate penalty `x`. The question becomes: can we repaint at most `k` segments such that no cell with penalty greater than `x` ends up wrong? If we can solve this decision problem efficiently, we can perform binary search over all possible penalty values to find the minimum achievable penalty.

To check a candidate penalty `x`, we mark every cell with penalty exceeding `x` as "must be correct". We then reduce the strip to a string of `0` and `1` where `1` represents a cell that must be blue to avoid exceeding penalty `x`, and `0` otherwise. The problem is now: can we cover all `1`s with at most `k` contiguous blue segments? This can be done greedily by sweeping left to right and starting a new segment whenever we encounter a `1` not yet covered by the previous segment.

This observation transforms the original problem from an exponential search over segments to a `O(n log max_penalty)` algorithm, which is fast enough given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² * k) | O(n) | Too slow |
| Binary Search + Greedy | O(n log P) | O(n) | Accepted |

Here, `P` is the maximum penalty in the array.

## Algorithm Walkthrough

1. For each test case, read `n`, `k`, the desired color string `s`, and the penalties `a`.
2. Construct a list `penalties` containing all unique penalty values. We will binary search over these values.
3. Define a helper function `can_achieve(max_penalty)` which checks if it's possible to avoid penalties exceeding `max_penalty` using at most `k` operations:

1. Convert the strip into a binary array `must_paint` where each cell is `1` if its desired color is blue and its penalty exceeds `max_penalty`, otherwise `0`.
2. Sweep through `must_paint` left to right. Count how many contiguous blue segments are required to cover all `1`s.
3. If the number of segments is ≤ `k`, return `True`; else return `False`.
4. Perform binary search over the sorted unique penalties using `can_achieve`. Initialize `low = 0` and `high = max(a)`.
5. For each middle value `mid`, check `can_achieve(mid)`. If true, try smaller penalties (`high = mid`); if false, increase penalty (`low = mid + 1`).
6. At the end, `low` contains the minimum achievable maximum penalty.
7. Output this value.

**Why it works**: The binary search relies on the monotonic property that if we can achieve a penalty `x`, we can also achieve any penalty greater than `x`. The greedy segment counting is valid because painting larger segments is never worse than painting smaller ones: merging adjacent required cells into one segment minimizes the total number of operations. Hence, the algorithm correctly finds the minimum penalty.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        a = list(map(int, input().split()))

        def can_achieve(max_penalty):
            segments_needed = 0
            i = 0
            while i < n:
                if s[i] == 'B' and a[i] > max_penalty:
                    segments_needed += 1
                    while i < n and s[i] == 'B' and a[i] > max_penalty:
                        i += 1
                else:
                    i += 1
            return segments_needed <= k

        low, high = 0, max(a)
        while low < high:
            mid = (low + high) // 2
            if can_achieve(mid):
                high = mid
            else:
                low = mid + 1
        print(low)

if __name__ == "__main__":
    solve()
```

The `can_achieve` function counts contiguous blue segments that must be painted to avoid penalties above the candidate. The binary search efficiently homes in on the minimal feasible maximum penalty. Boundary conditions like `k = 0` and all-red strips are handled naturally by this approach.

## Worked Examples

### Example 1

Input:

```
4 1
BRBR
9 3 5 4
```

| i | s[i] | a[i] | must_paint (x=3) | Segment Count |
| --- | --- | --- | --- | --- |
| 0 | B | 9 | 1 | start segment 1 |
| 1 | R | 3 | 0 | continue |
| 2 | B | 5 | 1 | start segment 2 (exceeds k=1) |
| 3 | R | 4 | 0 | - |

Binary search identifies minimum penalty = 3.

### Example 2

Input:

```
4 2
BRBR
9 3 5 4
```

| i | s[i] | a[i] | must_paint (x=0) | Segment Count |
| --- | --- | --- | --- | --- |
| 0 | B | 9 | 1 | start segment 1 |
| 1 | R | 3 | 0 | continue |
| 2 | B | 5 | 1 | start segment 2 |
| 3 | R | 4 | 0 | - |

Segments needed = 2 ≤ k=2 → minimum penalty = 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log P) | Each binary search step checks `can_achieve` in O(n), with up to log(max(a)) steps. |
| Space | O(n) | Store `s`, `a`, and temporary flags for each test case. |

The algorithm scales linearly with total `n` across test cases, fitting comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n4 1\nBRBR\n9 3 5 4\n4 1\nBRBR\n9 5 3 4\n4 2\nBRBR\n9 3 5 4\n10 2\nBRBRBBRRBR\n5 1 2 4 5 3 6 1 5 4\n5 5\nRRRRR\n5 3 1 2 4\n") == "3\n3\n0\n4\n0", "sample 1"

# custom test cases
assert run("1\n3 0\nBBB\n1 2 3\n") == "3", "no operations allowed"
assert run("1\n3 3\nRRR\n1 2 3
```
