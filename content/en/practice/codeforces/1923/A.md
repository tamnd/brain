---
title: "CF 1923A - Moving Chips"
description: "We are given a row of cells, each either containing a chip or empty. The goal is to move chips leftward into contiguous groups by repeatedly picking a chip and moving it into the closest empty cell to its left."
date: "2026-06-08T19:12:27+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1923
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 162 (Rated for Div. 2)"
rating: 800
weight: 1923
solve_time_s: 112
verified: false
draft: false
---

[CF 1923A - Moving Chips](https://codeforces.com/problemset/problem/1923/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of cells, each either containing a chip or empty. The goal is to move chips leftward into contiguous groups by repeatedly picking a chip and moving it into the closest empty cell to its left. The task is to determine the minimum number of moves required to make all chips form a single uninterrupted block.

The input provides multiple test cases. Each test case has a number of cells `n` (between 2 and 50) and an array describing which cells contain chips. The output for each test case is a single integer representing the fewest moves needed.

Because `n` is at most 50, any algorithm that does a simple scan over the array a few times will run efficiently. With `t` up to 1000 test cases, a solution that processes each array in linear time is acceptable.

The problem has subtle edge cases. For example, if all chips are already contiguous, no moves are needed. If there is a single chip with empty cells on its left, no moves are needed. A naive implementation that counts every empty cell or attempts to simulate moves blindly may overcount, because only empty cells **between the leftmost and rightmost chip** matter. For example, `[0, 1, 0, 1, 0, 1, 0]` has 3 chips and 3 gaps, but only the two gaps between the first and last chip need to be closed, so only 2 moves are required.

## Approaches

A brute-force approach is to simulate the process explicitly: repeatedly pick chips and move them left until a contiguous block forms. While correct, this is unnecessary because we only care about the minimum number of moves, not the exact sequence. Simulating each move is inefficient even for small arrays, and it risks off-by-one errors.

The key observation is that only empty cells **between the first and last chips** contribute to moves. Any empty cells to the left of the leftmost chip or to the right of the rightmost chip never need to be filled because no chip will move into them. Therefore, the minimal number of moves is simply the count of zeros between the first and last chip.

This reduces the problem to scanning the array once to find the indices of the first and last chip, then counting zeros in that subarray. This solution is linear, extremely simple to implement, and avoids pitfalls of naive simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) per test case | O(n) | Overkill / unnecessary |
| Count zeros between first and last chip | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a`.
3. Identify the leftmost chip by scanning from left to right. Store its index as `first`.
4. Identify the rightmost chip by scanning from right to left. Store its index as `last`.
5. Initialize a counter `moves` to zero.
6. Iterate from `first` to `last`. For each cell, if it is empty (`0`), increment `moves`.
7. After scanning, `moves` now holds the minimum number of operations required. Print it.

Why it works: moving any chip leftward can fill exactly one empty cell. Since all moves are independent and only zeros between the first and last chip matter, counting them gives the minimal number of moves. No move can reduce this count further, and no move outside this range is ever needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    first = a.index(1)  # leftmost chip
    last = len(a) - 1 - a[::-1].index(1)  # rightmost chip
    
    moves = 0
    for i in range(first, last + 1):
        if a[i] == 0:
            moves += 1
    print(moves)
```

The solution uses `list.index` to locate the first chip and a reversed scan to locate the last chip. The iteration between these indices counts all empty cells, which directly corresponds to the number of moves needed. No extra arrays are created, and all operations are O(n) per test case. Reversing the array to find the last index is safe since `n <= 50`.

## Worked Examples

Sample input: `[0, 1, 1, 1, 0, 1, 1, 0]`

| i | a[i] | moves |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 1 | 0 |
| 3 | 1 | 0 |
| 4 | 0 | 1 |
| 5 | 1 | 1 |
| 6 | 1 | 1 |

Explanation: The first chip is at index 1, last chip at index 6. There is exactly one zero between them (index 4), so `moves = 1`.

Another example: `[1, 0, 1, 0, 1]`

| i | a[i] | moves |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 0 | 1 |
| 2 | 1 | 1 |
| 3 | 0 | 2 |
| 4 | 1 | 2 |

Explanation: First chip at 0, last at 4. There are zeros at positions 1 and 3. Both need to be filled, so minimal moves is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case scans the array twice: once for first chip, once for last chip, then once to count zeros between. Each scan is O(n). |
| Space | O(n) | Only the input array is stored. No additional data structures beyond loop variables. |

With `t <= 1000` and `n <= 50`, the worst-case operation count is 50,000, well within the 2-second limit. Memory use is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        first = a.index(1)
        last = len(a) - 1 - a[::-1].index(1)
        moves = sum(1 for i in range(first, last + 1) if a[i] == 0)
        output.append(str(moves))
    return "\n".join(output)

# provided samples
assert run("5\n8\n0 1 1 1 0 1 1 0\n6\n0 1 0 0 0 0\n6\n1 1 1 1 1 1\n5\n1 0 1 0 1\n9\n0 1 1 0 0 0 1 1 0\n") == "1\n0\n0\n2\n3"

# custom tests
assert run("2\n2\n1 0\n3\n0 1 0\n") == "0\n0"  # minimal n, single chip
assert run("1\n6\n0 0 1 0 1 0\n") == "2"  # zeros outside first/last ignored
assert run("1\n7\n1 0 0 0 0 0 1\n") == "5"  # all
```
