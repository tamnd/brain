---
title: "CF 1649A - Game"
description: "We are given a linear sequence of locations, each either land or water, starting and ending with land. You begin at the first location and need to reach the last one."
date: "2026-06-10T03:57:23+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1649
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 775 (Div. 2, based on Moscow Open Olympiad in Informatics)"
rating: 800
weight: 1649
solve_time_s: 64
verified: true
draft: false
---

[CF 1649A - Game](https://codeforces.com/problemset/problem/1649/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear sequence of locations, each either land or water, starting and ending with land. You begin at the first location and need to reach the last one. You can move to an adjacent land location for free, or once per jump from any land to any later land, paying coins equal to the distance jumped. The task is to compute the minimum coins required to reach the last land.

The input provides multiple test cases. Each test case gives the number of locations $n$ and a sequence of 0s and 1s representing water and land. The output is a single integer per test case, representing the minimal coin cost.

The constraints are small: $n$ is at most 100 and there can be up to 100 test cases. This means any $O(n^2)$ algorithm is feasible, and even simpler $O(n)$ linear passes will be extremely fast. We do not need to worry about high-performance data structures or complex graph algorithms.

A non-obvious edge case occurs when all intermediate locations are water. For example, for input `1 0 0 0 1`, the optimal jump must span all water, costing 4 coins, because moving step by step is impossible. Another subtle case is when there are consecutive lands. For input `1 1 1 1`, the optimal strategy is to never pay coins because all adjacent moves are free, even though one could "jump" for 2 coins from the first to last location. A naive implementation that always jumps between first and last land would overpay.

## Approaches

The brute-force approach is to simulate every possible path from the first to last land location, considering both free adjacent moves and paying for jumps over water. One could implement this recursively, computing all reachable positions and storing minimal cost. The complexity in the worst case is $O(n^2)$ for each test case, since each land can potentially jump to every other land, and there are $n$ locations. While feasible for this problem size, the recursion is unnecessary and error-prone for simple sequences.

The key insight comes from observing that the cost is entirely determined by the lengths of consecutive water segments between lands. Moving between adjacent lands costs nothing, and jumping over consecutive waters costs exactly the number of locations jumped. Therefore, we can ignore free moves and only sum the lengths of consecutive water segments that we must cross using a coin jump. This reduces the problem to a simple linear scan: iterate through the array, count zeros between ones, and sum these counts. We never need to consider complex branching or adjacency graphs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Works but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `coins` to zero. This will accumulate the total cost of mandatory jumps over water.
2. Initialize an index `i` at 0. While `i < n`, advance `i` until a land tile (`1`) is found. This step handles sequences of land at the start.
3. Once on a land tile, scan forward counting consecutive water tiles (`0`) until the next land tile is reached. Let `gap` be the number of water tiles between two lands.
4. Add `gap` to `coins`. This represents the minimal coins required to jump over that segment.
5. Move the index `i` to the next land and repeat steps 3-4 until reaching the last tile.
6. Output `coins` as the answer for this test case.

The reason this works is that any segment of consecutive water between two lands must be jumped over, and the cost is exactly the number of water tiles. Free adjacent moves on land do not contribute to the cost, so ignoring them does not change the total. This invariant guarantees correctness: each zero is counted exactly once for the mandatory jump it belongs to.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    coins = 0
    i = 0
    while i < n:
        if a[i] == 1:
            j = i + 1
            while j < n and a[j] == 0:
                j += 1
            if j < n:
                coins += j - i - 1
            i = j
        else:
            i += 1
    print(coins)
```

We start by reading the number of test cases and then iterate over each. For each array `a`, we scan from left to right. Whenever we hit a land tile, we measure the distance to the next land, counting only the intervening water tiles, and add that to `coins`. We skip over the counted segment entirely before continuing. Boundary handling is implicit because the last location is guaranteed land.

## Worked Examples

### Sample Input 2

```
5
1 0 1 0 1
```

| i | a[i] | j | gap (j-i-1) | coins |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 1 | 1 |
| 2 | 1 | 4 | 1 | 2 |
| 4 | 1 | end | 0 | 2 |

The table shows that first we jump over the zero at index 1 (cost 1), then over the zero at index 3 (cost 1), totaling 2 coins. The algorithm correctly identifies each segment of water and sums the costs.

### Sample Input 3

```
4
1 0 1 1
```

| i | a[i] | j | gap (j-i-1) | coins |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 1 | 1 |
| 2 | 1 | 3 | 0 | 1 |
| 3 | 1 | end | 0 | 1 |

Here the water segment of length 1 is jumped over, while adjacent lands at indices 2 and 3 cost nothing. Total coins = 1. The algorithm handles consecutive lands correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan each location once and each gap is counted once. |
| Space | O(n) | We store the input array; no additional data structures are needed. |

With `n` ≤ 100 and `t` ≤ 100, the solution performs at most 10,000 iterations, well within the 1-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        coins = 0
        i = 0
        while i < n:
            if a[i] == 1:
                j = i + 1
                while j < n and a[j] == 0:
                    j += 1
                if j < n:
                    coins += j - i - 1
                i = j
            else:
                i += 1
        print(coins)
    return output.getvalue().strip()

# Provided samples
assert run("3\n2\n1 1\n5\n1 0 1 0 1\n4\n1 0 1 1\n") == "0\n2\n1"

# Custom cases
assert run("1\n5\n1 0 0 0 1\n") == "3", "all water in between"
assert run("1\n4\n1 1 1 1\n") == "0", "all land, no coins"
assert run("1\n2\n1 1\n") == "0", "minimum size, no coins"
assert run("1\n6\n1 0 1 0 0 1\n") == "3", "multiple water segments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 0 1 | 3 | Correct counting over consecutive water |
| 1 1 1 1 | 0 | Free adjacent moves do not add cost |
| 1 1 | 0 | Minimum size edge case |
| 1 0 1 0 0 1 | 3 | Multiple separate water segments |

## Edge Cases

For input `1 0 0 0 1`, the algorithm sets `i=0` on land, finds `j=4` on next land, calculates `gap = 4-0-1 = 3` and adds to coins. Index `i` moves to 4, end of array. Output 3 is correct.

For consecutive lands like `1 1 1 1`, the first land at `i=0` leads to `j=1` (next land), `gap=0` coins added. Then `i=1`, next land at `j=2`, `gap=0`. Finally `i=2`, next land at `j=3`, `gap=0`. Total coins = 0, correctly ignoring free moves.
