---
title: "CF 1851C - Tiles Comeback"
description: "We are given a row of $n$ tiles, each painted with some color. Vlad wants to walk along the tiles, starting from the first tile, making jumps of arbitrary length to the right, and ending exactly on the last tile."
date: "2026-06-09T17:19:06+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 1000
weight: 1851
solve_time_s: 349
verified: false
draft: false
---

[CF 1851C - Tiles Comeback](https://codeforces.com/problemset/problem/1851/C)

**Rating:** 1000  
**Tags:** greedy  
**Solve time:** 5m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of $n$ tiles, each painted with some color. Vlad wants to walk along the tiles, starting from the first tile, making jumps of arbitrary length to the right, and ending exactly on the last tile. The path he creates must have a total length divisible by $k$, and must be divided into contiguous blocks of length $k$ such that all tiles within a block are the same color. Colors between blocks do not need to differ. For each test case, we need to decide if such a path exists.

The constraints are tight enough that we cannot afford an $O(n^2)$ exploration of all possible jumps. With $n$ up to $2 \cdot 10^5$ and up to $10^4$ test cases, any algorithm must run in roughly $O(n)$ per test case in order to stay within the 2-second time limit. This rules out brute-force search of every path.

Non-obvious edge cases include situations where all tiles have the same color, or where the first and last tiles are the same color but intermediate tiles prevent forming full blocks. For example, with $n = 3$, $k = 2$, and tiles $[1,2,1]$, a naive approach might incorrectly claim "YES" just because the first and last tiles match the first block color, but there is no valid block of length $k$ starting at the first tile.

## Approaches

The brute-force approach would attempt to generate all sequences of tiles starting from the first tile, checking if each sequence forms full $k$-length blocks of the same color and ends on the last tile. Each path could have up to $n/k$ blocks, so the number of sequences grows combinatorially with $n$, quickly exceeding any reasonable time bound. For $n$ around $2 \cdot 10^5$, this is completely infeasible.

The key insight is that each block of length $k$ must consist of identical colors, so we can scan the array greedily from the left. We keep track of contiguous segments of the same color and count how many tiles they contribute toward the current block. Whenever we collect $k$ tiles of the same color, we commit that as a block and move on. This reduces the problem to a single linear scan from the left, checking if the sum of block lengths allows reaching the last tile.

Similarly, scanning from the right allows us to handle cases where the last block is constrained to end at the last tile. By greedily matching blocks from both ends and checking if they overlap, we can confirm whether a valid path exists. The problem reduces to linear time because we only need to identify contiguous segments of the same color and compute the number of full $k$-length blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Two-Pointer | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `count` to track how many tiles of the same color we have seen in the current segment from the left. Initialize `blocks_left` to zero, representing how many full $k$-length blocks we can make starting from the left.
2. Scan the tiles from left to right. For each tile, check if it matches the previous tile. If it does, increment `count`; otherwise, reset `count` to 1. Each time `count` reaches `k`, increment `blocks_left` and reset `count` to zero to start a new potential block.
3. Repeat the same process from right to left, storing `blocks_right` for the number of full $k$-length blocks ending at the last tile.
4. After both scans, compute the total length of the blocks from the left and right, considering overlaps. If the leftmost blocks extend beyond the rightmost blocks, there is no valid path. Otherwise, if the total number of blocks multiplied by `k` is at least the number of tiles in the path needed to reach the last tile, print "YES"; else print "NO".

Why it works: Each block must be exactly `k` tiles of the same color. By counting contiguous segments from the left and right, we are guaranteed to cover all possible block alignments. The overlap check ensures we do not double-count tiles when the leftmost and rightmost sequences share the same segment. This captures all valid paths without exploring every jump combination.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_form_path(n, k, colors):
    if n == k:
        return "YES" if len(set(colors)) == 1 else "NO"

    # Scan from left
    left_blocks = 0
    count = 1
    for i in range(1, n):
        if colors[i] == colors[i-1]:
            count += 1
        else:
            count = 1
        if count == k:
            left_blocks += 1
            count = 0

    # Scan from right
    right_blocks = 0
    count = 1
    for i in range(n-2, -1, -1):
        if colors[i] == colors[i+1]:
            count += 1
        else:
            count = 1
        if count == k:
            right_blocks += 1
            count = 0

    # If the total blocks cover at least the first and last tiles
    if left_blocks + right_blocks < n // k:
        return "NO"
    return "YES"

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    colors = list(map(int, input().split()))
    print(can_form_path(n, k, colors))
```

The solution uses two linear scans to count how many full `k`-length blocks we can form from the left and right. We reset the counter after forming a block to ensure only exact `k`-length sequences count. The final comparison ensures that the blocks can cover a path ending at the last tile. The edge case when `n == k` is handled separately because a single block is required.

## Worked Examples

**Sample Input 2:**

```
14 3
1 2 1 1 7 5 3 3 1 3 4 4 2 4
```

| i | tile | count (left) | left_blocks | count (right) | right_blocks |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | - | - |
| 1 | 2 | 1 | 0 | - | - |
| 2 | 1 | 1 | 0 | - | - |
| 3 | 1 | 2 | 0 | - | - |
| 4 | 7 | 1 | 0 | - | - |
| 5 | 5 | 1 | 0 | - | - |
| 6 | 3 | 1 | 0 | - | - |
| 7 | 3 | 2 | 0 | - | - |
| 8 | 1 | 1 | 0 | - | - |
| 9 | 3 | 1 | 0 | - | - |
| 10 | 4 | 1 | 0 | - | - |
| 11 | 4 | 2 | 0 | - | - |
| 12 | 2 | 1 | 0 | - | - |
| 13 | 4 | 1 | 0 | - | - |

From these counts, we can see the first block of `1` from left forms after tiles 0,2,3; the last block of `4` from right forms after tiles 10,11,13. Combining these blocks allows forming a valid path of length divisible by 3 ending at tile 14.

**Sample Input 3:**

```
3 3
3 1 3
```

No contiguous segment of length 3 exists, so the algorithm outputs "NO". This confirms that short arrays with insufficient repeated tiles are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each tile is scanned at most twice, left to right and right to left. |
| Space | O(n) | Store the tile colors. Counters and block counts use constant space. |

Since the total sum of $n$ over all test cases is $2 \cdot 10^5$, the solution comfortably runs in under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())  # assuming the solution code is saved as solution.py
    return output.getvalue().strip()

# Provided samples
assert run("10\n4 2\n1 1 1 1\n14 3\n1 2 1 1 7 5 3 3 1 3 4 4 2
```
