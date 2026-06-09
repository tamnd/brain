---
title: "CF 1690D - Black and White Stripe"
description: "We are given a stripe of tiles, each either white or black, and the goal is to ensure that at least one segment of exactly k consecutive tiles is entirely black."
date: "2026-06-09T23:17:48+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1690
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 797 (Div. 3)"
rating: 1000
weight: 1690
solve_time_s: 84
verified: true
draft: false
---

[CF 1690D - Black and White Stripe](https://codeforces.com/problemset/problem/1690/D)

**Rating:** 1000  
**Tags:** implementation, two pointers  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stripe of tiles, each either white or black, and the goal is to ensure that at least one segment of exactly `k` consecutive tiles is entirely black. The input provides multiple test cases, each specifying the length of the stripe, the required segment length, and the sequence of tiles. Our task is to compute the minimum number of white tiles we need to repaint to black to achieve a contiguous black segment of length `k`. If such a segment already exists, the answer is zero.

The constraints allow `n` to be as large as 200,000, and the sum of all `n` across test cases also caps at 200,000. This implies that any solution with complexity worse than O(n) per test case will likely time out. Naive O(n*k) approaches are too slow because `k` can be comparable to `n`.

Subtle edge cases arise when the required segment length equals the total length, `k = n`, or when `k = 1`. For example, a stripe `W` of length 1 with `k=1` requires a single repaint. Another scenario is a fully black stripe of length `n` with `k<n`; the answer is zero. Handling these edge cases incorrectly often comes from off-by-one errors in segment indexing or from failing to consider segments starting at the first or last position.

## Approaches

The brute-force approach is straightforward: examine every possible contiguous segment of length `k`, count the number of white tiles in it, and take the minimum. This works because each segment is independent, and the number of repaints is exactly the number of white tiles in that segment. However, the brute-force has complexity O(n_k) because for each of the roughly `n-k+1` segments, we iterate over `k` tiles. In the worst case of `n = 2*10^5` and `k ≈ n`, this would result in approximately 4_10^10 operations, which is infeasible.

The key insight is that the problem exhibits a sliding window property. The number of white tiles in a segment of length `k` changes predictably as we move the window one position to the right: we subtract the contribution of the tile leaving the window and add the contribution of the tile entering. This lets us compute the number of white tiles in every segment of length `k` in O(n) time.

The observation that the sum of whites in a sliding window can be updated incrementally reduces the solution from O(n*k) to O(n). We only need to maintain a running count of whites and update it as the window moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*k) | O(1) | Too slow |
| Sliding Window | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `k`, and the stripe string.
3. Initialize a counter `current_whites` for the first window of length `k` by counting the number of white tiles in positions 0 through k-1.
4. Set `min_whites` to `current_whites`.
5. Slide the window from position 1 to n-k. For each step, if the tile leaving the window is white, decrement `current_whites`. If the tile entering the window is white, increment `current_whites`.
6. Update `min_whites` to the minimum of itself and `current_whites`.
7. After sliding through the entire stripe, output `min_whites` as the minimum number of repaints needed.

Why it works: The sliding window invariant guarantees that `current_whites` always accurately reflects the number of white tiles in the current segment of length `k`. By iterating over all segments exactly once and keeping track of the minimum, we find the optimal number of repaints.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    
    # initial window count
    current_whites = sum(1 for c in s[:k] if c == 'W')
    min_whites = current_whites
    
    for i in range(1, n - k + 1):
        if s[i-1] == 'W':
            current_whites -= 1
        if s[i+k-1] == 'W':
            current_whites += 1
        min_whites = min(min_whites, current_whites)
    
    print(min_whites)
```

The first loop counts whites in the initial segment. Sliding the window one position at a time updates the count efficiently. Boundary handling is critical: the first index leaving the window is `i-1`, and the new tile entering is `i+k-1`. Using `sum(1 for c in ...)` avoids off-by-one errors in counting whites.

## Worked Examples

**Example 1**: `n=5, k=3, s="BBWBW"`

| Window start | Window content | Whites | min_whites |
| --- | --- | --- | --- |
| 0 | BBW | 1 | 1 |
| 1 | BWB | 2 | 1 |
| 2 | WBW | 2 | 1 |

The algorithm correctly finds that repainting 1 tile is sufficient.

**Example 2**: `n=5, k=5, s="BBWBW"`

| Window start | Window content | Whites | min_whites |
| --- | --- | --- | --- |
| 0 | BBWBW | 2 | 2 |

Only one window exists, so 2 repaints are needed. The algorithm handles the edge of window length equal to the stripe length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is processed at most twice: once entering and once leaving the sliding window |
| Space | O(1) | Only a few counters are used; no additional arrays proportional to n |

Given the sum of n across all test cases ≤ 2*10^5, the solution runs comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        current_whites = sum(1 for c in s[:k] if c == 'W')
        min_whites = current_whites
        for i in range(1, n - k + 1):
            if s[i-1] == 'W':
                current_whites -= 1
            if s[i+k-1] == 'W':
                current_whites += 1
            min_whites = min(min_whites, current_whites)
        print(min_whites)
    
    return output.getvalue().strip()

# provided samples
assert run("4\n5 3\nBBWBW\n5 5\nBBWBW\n5 1\nBBWBW\n1 1\nW\n") == "1\n2\n0\n1", "sample tests"

# custom cases
assert run("3\n1 1\nB\n3 2\nWWW\n6 3\nBBBWBB\n") == "0\n2\n0", "edge cases"
assert run("2\n5 5\nBBBBB\n4 2\nWBWB\n") == "0\n1", "full black and alternating"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 B | 0 | minimum-length stripe already black |
| 3 2 WWW | 2 | all whites require multiple repaints |
| 6 3 BBBWBB | 0 | segment of length k already exists |
| 5 5 BBBBB | 0 | entire stripe already black, k=n |
| 4 2 WBWB | 1 | alternating pattern, window sliding |

## Edge Cases

For `n=1, k=1, s="W"`, the initial window contains a single white tile. The algorithm counts `current_whites=1`, `min_whites=1`, and prints 1. This is correct: we must repaint the only tile. No index errors occur because the sliding window loop does not run when `n-k=0`.

For `n=5, k=5, s="BBBBB"`, the only window already contains zero whites. `current_whites=0`, `min_whites=0`. The algorithm outputs 0 correctly without entering the loop.

For alternating patterns like `WBWB`, `current_whites` starts at 1 (for the first window). Sliding the window updates counts accurately, confirming that incremental updates handle variable distributions of whites and blacks.
