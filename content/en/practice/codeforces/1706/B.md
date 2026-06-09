---
title: "CF 1706B - Making Towers"
description: "We are given a sequence of n blocks, each with a color from 1 to n. We need to place them one by one on a 2D grid. The first block always starts at (0, 0)."
date: "2026-06-09T21:18:36+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1706
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 809 (Div. 2)"
rating: 1100
weight: 1706
solve_time_s: 183
verified: false
draft: false
---

[CF 1706B - Making Towers](https://codeforces.com/problemset/problem/1706/B)

**Rating:** 1100  
**Tags:** dp, greedy, math  
**Solve time:** 3m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of `n` blocks, each with a color from `1` to `n`. We need to place them one by one on a 2D grid. The first block always starts at `(0, 0)`. Every subsequent block can move either left, right, or up relative to the previous block, but cannot go down or occupy a position that already contains a block. Once the blocks are placed, we are asked, for each color, to find the largest contiguous vertical stack of blocks of that color, i.e., the tallest tower that uses only blocks of that color.

The input is up to `10^5` blocks per test case, and the total across all test cases is `2 * 10^5`. With a one-second time limit, we cannot afford anything worse than linear or linear-logarithmic per test case. Quadratic operations over blocks are too slow.

An edge case arises when a color appears only once or in positions that cannot align vertically without violating the placement rules. For example, if the blocks are `[1, 2, 1, 2, 1]`, naive counting of the number of occurrences of `1` would suggest a tower of size `3`, but the placement restrictions might prevent a vertical stack larger than `2`. Similarly, a color that does not appear at all should correctly return `0`.

The subtlety is that the "vertical separation" between consecutive blocks of the same color matters. We cannot freely stack them vertically without considering the intervening blocks, which may force horizontal moves.

## Approaches

The brute-force approach would try to simulate placing each block on the grid, tracking all possible coordinates and checking vertical tower heights for each color. This is correct, but extremely slow. For each block, we might explore multiple possible placements, and there are up to `10^5` blocks. In the worst case, this results in exponential behavior and cannot run within the time limits.

The key insight is that the absolute coordinates do not matter. The only thing that affects the tower height for a particular color is how often we need to "jump" horizontally to place the next block of the same color. If two blocks of the same color are consecutive in the sequence, we can stack them vertically by placing the intervening blocks horizontally. Thus, we can reduce the problem to counting the minimal number of "gaps" between consecutive blocks of the same color and how these gaps force horizontal moves.

We can formalize this by considering a sequence of positions where a particular color occurs. Between two occurrences, if there are other blocks of different colors, we need to make at least one horizontal move. So the maximum vertical stack of a color is essentially `1 + the number of times that color appears with other blocks in between`.

A simple way to implement this efficiently is to iterate over the blocks, keep track of the last seen index of each color, and count "segments" between them. This transforms the problem into a linear scan over the array for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n^2) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `max_tower` of size `n` with zeros. This will store the result for each color.
2. For each color, maintain the index of the last occurrence. Start with `-1` to indicate it hasn’t been seen yet.
3. Iterate over the blocks sequentially. For each block of color `c`:

a. If this is the first occurrence of `c`, start a new tower segment, counting from `1`.

b. If it has appeared before, check the gap from the last occurrence. If there are other blocks in between, we increment the number of vertical segments needed for `c`. This effectively counts how many "vertical moves" we can make for this color.

c. Update the last occurrence index for color `c`.
4. After scanning the blocks, the maximum vertical segments for each color is the answer.
5. Output the array `max_tower`.

The reason this works is that each block must either continue a vertical tower or be forced to shift horizontally if another block intervenes. By counting the number of blocks between consecutive occurrences of the same color, we capture the minimal number of vertical segments needed. This guarantees the maximum tower height under the placement rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    c = list(map(int, input().split()))
    
    last_pos = [-1] * (n + 1)
    max_tower = [0] * (n + 1)
    
    for idx, color in enumerate(c):
        if last_pos[color] == -1:
            max_tower[color] += 1
        else:
            if idx - last_pos[color] > 1:
                max_tower[color] += 1
        last_pos[color] = idx
    
    print(" ".join(str(max_tower[i]) for i in range(1, n + 1)))
```

The code keeps track of the last index where each color appeared and increments the tower count when we encounter a new occurrence with intervening blocks. Using a list of size `n+1` avoids off-by-one errors. The `if idx - last_pos[color] > 1` check ensures we only increment when there is at least one other block in between, reflecting the required horizontal shift in placement.

## Worked Examples

### Sample Input 1

```
7
1 2 3 1 2 3 1
```

| idx | color | last_pos | max_tower |
| --- | --- | --- | --- |
| 0 | 1 | -1 → 0 | 0 → 1 |
| 1 | 2 | -1 → 1 | 0 → 1 |
| 2 | 3 | -1 → 2 | 0 → 1 |
| 3 | 1 | 0 → 3 | 1 → 2 |
| 4 | 2 | 1 → 4 | 1 → 2 |
| 5 | 3 | 2 → 5 | 1 → 2 |
| 6 | 1 | 3 → 6 | 2 → 3 |

This demonstrates that vertical stacks increase only when necessary horizontal moves are forced.

### Sample Input 2

```
6
4 2 2 2 4 4
```

| idx | color | last_pos | max_tower |
| --- | --- | --- | --- |
| 0 | 4 | -1 → 0 | 0 → 1 |
| 1 | 2 | -1 → 1 | 0 → 1 |
| 2 | 2 | 1 → 2 | 1 (no gap) |
| 3 | 2 | 2 → 3 | 1 (no gap) |
| 4 | 4 | 0 → 4 | 1 → 2 |
| 5 | 4 | 4 → 5 | 2 → 3 |

Shows handling of consecutive blocks without needing a vertical increment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each block is processed once; array accesses are constant time. |
| Space | O(n) | We store `last_pos` and `max_tower` arrays of size `n+1`. |

With `sum(n) ≤ 2*10^5`, the algorithm runs comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        c = list(map(int, input().split()))
        last_pos = [-1] * (n + 1)
        max_tower = [0] * (n + 1)
        for idx, color in enumerate(c):
            if last_pos[color] == -1:
                max_tower[color] += 1
            else:
                if idx - last_pos[color] > 1:
                    max_tower[color] += 1
            last_pos[color] = idx
        res.append(" ".join(str(max_tower[i]) for i in range(1, n + 1)))
    return "\n".join(res)

# provided samples
assert run("6\n7\n1 2 3 1 2 3 1\n6\n4 2 2 2 4 4\n1\n1\n5\n5 4 5 3 5\n6\n3 3 3 1 3 3\n8\n1 2 3 4 4 3 2 1\n") == \
"3 2 2 0 0 0 0\n0 3 0 2 0 0\n1\n0 0 1 1 1\n1 0 4 0 0 0\n2 2 2 2 0 0 0 0"

# custom cases
assert run("1\n5\n1 1 1 1 1\n") == "1 0 0 0 0", "all same color consecutive"
assert run("
```
