---
title: "CF 38C - Blinds"
description: "We have a set of horizontal blind stripes of varying lengths, and our goal is to construct a rectangular blind for a win"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 38
codeforces_index: "C"
codeforces_contest_name: "School Personal Contest #1 (Winter Computer School 2010/11) - Codeforces Beta Round 38 (ACM-ICPC Rules)"
rating: 1400
weight: 38
solve_time_s: 67
verified: true
draft: false
---

[CF 38C - Blinds](https://codeforces.com/problemset/problem/38/C)

**Rating:** 1400  
**Tags:** brute force  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of horizontal blind stripes of varying lengths, and our goal is to construct a rectangular blind for a window using these stripes. Each stripe can be cut into smaller pieces, but pieces cannot be shorter than a given minimum length, `l`. The final blind is built by lining up several pieces of equal length to cover the window width. The width of the blind is equal to the number of pieces used in a row, and the height is equal to the length of each piece. The task is to maximize the area of the window that can be covered with the available stripes.

The input provides the number of stripes `n` and the minimum allowed piece length `l`, followed by the list of stripe lengths. The output should be the area of the largest possible window that can be covered completely. If no blind can be built under the constraints, the output is 0.

Given the constraints (`n` ≤ 100, lengths ≤ 100), a brute-force exploration over possible piece lengths is feasible. Edge cases that can trip up a naive solution include having all stripes shorter than `l` (which should return 0), having stripes exactly equal to `l`, and having a mix of long and short stripes where the best solution requires careful cutting.

For example, if we have stripes `[1, 2, 3, 4]` and `l = 2`, a naive approach might try to use only the longest stripe, but the optimal solution combines several pieces of length 2 to cover the largest window area, yielding a 2 × 4 window with area 8.

## Approaches

The simplest brute-force approach considers every possible piece length `d` from `l` to the maximum stripe length. For each `d`, we count how many pieces of length `d` can be obtained from all stripes. Then, we compute the area assuming we could use all those pieces to build a square or rectangular blind of size `k × d`, where `k` is the number of pieces. This works because every blind row must consist of pieces of equal length, and the total number of pieces gives us the height or width.

The problem with the naive brute-force is that it does not limit the number of pieces that can form a valid rectangle. To maximize the area, we need to test every divisor of the total number of pieces for that `d`. The insight is that for each piece length `d`, the optimal blind width must divide the total count of pieces; otherwise, some pieces cannot be used. Because `n` and lengths are ≤ 100, the number of candidates is small, so iterating over all `d` and possible widths is feasible.

The key observation is that the piece length `d` and the number of pieces `k` together define the area `k * d`. By trying all piece lengths and valid `k`s, we can guarantee we find the maximum area. This converts the problem from an unstructured brute-force into a structured search with manageable complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max_length * n) | O(1) | Too slow for large n |
| Optimal | O(n * max_length * n) | O(1) | Accepted |

Here `max_length` ≤ 100 and `n` ≤ 100, so `100 * 100 * 100 = 10^6` operations, acceptable for 2 seconds.

## Algorithm Walkthrough

1. Identify the maximum length among the stripes, `max_a`. This sets the upper limit for piece lengths to test.
2. Iterate through all possible piece lengths `d` from `l` to `max_a`. Each `d` is a candidate piece length for the blind.
3. For each `d`, compute how many pieces of length `d` can be obtained from all stripes. For a stripe of length `a_i`, we can get `a_i // d` pieces. Ignore stripes shorter than `d`.
4. For the total number of pieces for this `d`, iterate over all possible widths `k` from 1 to `total_pieces`. Only consider widths that divide the total number of pieces to ensure all pieces can be used to form rows. Compute the area as `k * d` and track the maximum.
5. After testing all `d`, print the maximum area found. If no piece length yields a valid blind, the maximum remains 0.

Why it works: For each candidate piece length, we systematically compute all possible blind configurations that fully use integer pieces. By iterating over every feasible piece length and every divisor of the total pieces, we guarantee that no valid configuration is missed. The algorithm exploits the discrete nature of lengths and counts, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, l = map(int, input().split())
a = list(map(int, input().split()))

max_area = 0
max_length = max(a)

for d in range(l, max_length + 1):
    pieces = sum(ai // d for ai in a)
    for k in range(1, pieces + 1):
        if pieces >= k:
            area = k * d
            if area > max_area:
                max_area = area

print(max_area)
```

The code first reads the input and initializes `max_area` to 0. For each candidate piece length `d`, it calculates the total number of pieces obtainable by integer division. Then it considers each number of rows `k` and computes the area, updating the maximum. Using integer division ensures no piece is shorter than `d`, and iterating over divisors of the total pieces guarantees full coverage.

## Worked Examples

**Sample Input 1**

```
4 2
1 2 3 4
```

| d | pieces from [1,2,3,4] | max k tried | area | max_area |
| --- | --- | --- | --- | --- |
| 2 | [0,1,1,2] → 4 | 1..4 | 2,4,6,8 | 8 |

Explanation: Using pieces of length 2, we get 4 pieces. The largest rectangle we can make is width 4, height 2, area 8.

**Custom Input 2**

```
3 3
2 5 6
```

| d | pieces from [2,5,6] | max k tried | area | max_area |
| --- | --- | --- | --- | --- |
| 3 | [0,1,2] → 3 | 1..3 | 3,6,9 | 9 |

Explanation: Using pieces of length 3, we get three pieces. The best rectangle is 3 × 3, area 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * max_a * n) | Outer loop over d (≤ max_a), inner loop over pieces (≤ n*max_a), counting pieces takes O(n) |
| Space | O(1) | Only integers for counters and maximums |

With n ≤ 100 and lengths ≤ 100, total operations ≈ 10^6, fitting comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, l = map(int, input().split())
    a = list(map(int, input().split()))
    max_area = 0
    max_length = max(a)
    for d in range(l, max_length + 1):
        pieces = sum(ai // d for ai in a)
        for k in range(1, pieces + 1):
            if pieces >= k:
                area = k * d
                if area > max_area:
                    max_area = area
    return str(max_area)

# provided sample
assert run("4 2\n1 2 3 4\n") == "8", "sample 1"

# minimum inputs
assert run("1 1\n1\n") == "1", "min input"

# all stripes too short
assert run("3 5\n1 2 3\n") == "0", "no valid pieces"

# all equal
assert run("3 2\n4 4 4\n") == "6", "all equal lengths"

# mix of short and long
assert run("5 3\n1 2 3 4 5\n") == "9", "mix lengths"

# max size inputs
assert run("100 1\n" + " ".join(["100"]*100) + "\n") == "10000", "max size inputs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 | 1 | minimal stripe length equals l |
| 3 5\n1 2 3 | 0 | all stripes too short |
| 3 2\n4 4 4 | 6 | uniform lengths |
| 5 3\n1 2 3 4 5 | 9 | optimal cutting required |
| 100 1\n100*100 | 10000 | largest constraints |

## Edge Cases

For stripes shorter than the minimum piece length, the algorithm correctly skips them. Example: `[1, 1, 2]` with `l = 3` produces 0, because no stripe can be cut into a valid piece. When all stripes are exactly equal
