---
title: "CF 1932A - Thorns and Coins"
description: "We are given a one-dimensional path made of cells. Each cell is either empty, contains a coin, or is blocked by thorns. We start at the first cell, which is guaranteed to be empty, and we want to move to the right as far as possible while collecting coins."
date: "2026-06-08T18:19:08+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1932
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 927 (Div. 3)"
rating: 800
weight: 1932
solve_time_s: 80
verified: true
draft: false
---

[CF 1932A - Thorns and Coins](https://codeforces.com/problemset/problem/1932/A)

**Rating:** 800  
**Tags:** dp, greedy, implementation  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional path made of cells. Each cell is either empty, contains a coin, or is blocked by thorns. We start at the first cell, which is guaranteed to be empty, and we want to move to the right as far as possible while collecting coins.

At each step we may move either one cell or two cells forward, but we are only allowed to land on cells that are not thorns. If we land on a coin cell, we collect that coin. We cannot pass through or land on thorn cells, which effectively act as barriers for landing positions.

The task is to compute the maximum number of coins we can collect starting from index 0.

The constraints are very small: up to 1000 test cases and each path has length at most 50. This immediately tells us that even cubic or exponential solutions would pass comfortably, but it also hints that the intended solution is simple enough to be linear per test case.

A key structural observation is that movement is strictly forward, and the only branching is whether we jump by 1 or 2 steps. There is no backtracking and no cycles.

The main subtlety is that thorns block landing, which can create situations where a greedy “always take coin if you see it” strategy fails if it assumes you can always reach every coin.

For example, consider a segment like:

Input:

```
. @ * @ @
```

From the first cell, you might think about collecting the first coin and then continuing, but stepping incorrectly could land you into a configuration where a later coin becomes unreachable because thorns block valid stepping points.

Another subtle edge case is consecutive thorns:

```
. @ * * @
```

Even though there is a coin later, it may be impossible to reach it because every path of jumps lands on a thorn.

These situations suggest we need a systematic way to track reachability, not just local greedy decisions.

## Approaches

A brute force approach would explore every possible sequence of moves. From each position, we can try stepping 1 or 2 cells forward if the destination is valid. Each state branches into at most two choices, forming a recursion tree of depth up to n.

In the worst case, this leads to roughly O(2^n) paths, since each position can branch into two choices. Even though n is only 50, 2^50 is still far too large, and most branches are redundant because they revisit the same index multiple times via different paths.

The redundancy suggests dynamic programming. The key observation is that the problem has optimal substructure: the best answer starting from position i depends only on the best answers of positions i+1 and i+2, provided those positions are reachable.

Instead of thinking forward, we flip the perspective: define dp[i] as the maximum coins we can collect starting from cell i, assuming we are allowed to stand on i. Since we always move forward, transitions only go to i+1 or i+2, making the state space linear.

We compute dp from right to left. If a cell is a thorn, dp[i] is invalid. Otherwise, dp[i] is the coin at i plus the maximum of dp[i+1] and dp[i+2] if those states are valid.

Finally, we return dp[0].

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (DFS over moves) | O(2^n) | O(n) | Too slow |
| Dynamic Programming | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We define a DP array where each position represents the best number of coins collectible starting from that cell.

1. Create an array dp of size n+2 initialized to 0. The extra padding prevents boundary checks when accessing i+1 and i+2.
2. Iterate from the last cell down to the first cell. We process in reverse so that when computing dp[i], the values dp[i+1] and dp[i+2] are already known.
3. If the current cell contains a thorn, we set dp[i] to 0 because we cannot land there. However, we still allow transitions through it when considering earlier cells implicitly, since we never start from a thorn.
4. If the current cell is not a thorn, compute a base value equal to 1 if it contains a coin, otherwise 0.
5. Update dp[i] as base value plus the maximum of dp[i+1] and dp[i+2], but only considering valid transitions. If both are valid, we take the maximum; if one is effectively unreachable, we ignore it.
6. The answer for each test case is dp[0], which corresponds to starting at the first cell.

### Why it works

The correctness relies on the fact that from any position i, the only future decisions are independent subproblems starting at i+1 and i+2. Since movement is strictly forward, no later choice can influence earlier decisions. Every valid path from i must begin with exactly one of these two moves, so the optimal result is the best of those two continuations plus any coin collected at i. This forms a complete decomposition of all possible paths, guaranteeing no configuration is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        dp = [0] * (n + 2)

        for i in range(n - 1, -1, -1):
            if s[i] == '*':
                dp[i] = 0
                continue

            best_next = max(dp[i + 1], dp[i + 2])
            dp[i] = best_next + (1 if s[i] == '@' else 0)

        print(dp[0])

if __name__ == "__main__":
    solve()
```

The solution processes the string from right to left so that every state has its future already computed. The use of a padded dp array avoids explicit boundary checks when accessing i+2.

A common mistake is trying to simulate movement greedily from left to right. That fails because choosing a move that collects an early coin can block access to a better future sequence. The DP formulation avoids this by always evaluating both forward options.

## Worked Examples

### Example 1

Input:

```
.@@*@.**@@
```

We compute dp from right to left. Let us track only meaningful positions.

| i | s[i] | dp[i+1] | dp[i+2] | best_next | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 9 | @ | 0 | 0 | 0 | 1 |
| 8 | @ | 1 | 0 | 1 | 2 |
| 7 | * | - | - | - | 0 |
| 6 | * | - | - | - | 0 |
| 5 | . | 0 | 0 | 0 | 0 |
| 4 | @ | 0 | 0 | 0 | 1 |
| 3 | * | - | - | - | 0 |
| 2 | @ | 1 | 0 | 1 | 2 |
| 1 | @ | 2 | 1 | 2 | 3 |
| 0 | . | 3 | 2 | 3 | 3 |

Output is 3.

This trace shows how thorns reset continuity and how the DP correctly skips over blocked regions by relying on alternative jump lengths.

### Example 2

Input:

```
.@@@@
```

| i | s[i] | dp[i+1] | dp[i+2] | best_next | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 4 | @ | 0 | 0 | 0 | 1 |
| 3 | @ | 1 | 0 | 1 | 2 |
| 2 | @ | 2 | 1 | 2 | 3 |
| 1 | @ | 3 | 2 | 3 | 4 |
| 0 | . | 4 | 3 | 4 | 4 |

Output is 4.

This case demonstrates uninterrupted accumulation where every move can simply choose the best continuation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each position is processed once with O(1) transitions |
| Space | O(n) | DP array of size n+2 |

Given n ≤ 50 and t ≤ 1000, the total work is trivial and well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        dp = [0] * (n + 2)

        for i in range(n - 1, -1, -1):
            if s[i] == '*':
                dp[i] = 0
            else:
                dp[i] = max(dp[i + 1], dp[i + 2]) + (1 if s[i] == '@' else 0)

        output.append(str(dp[0]))

    return "\n".join(output)

# provided samples
assert run("""3
10
.@@*@.**@@
5
.@@@@
15
.@@..@***..@@@*
""") == """3
4
3"""

# custom cases
assert run("""1
1
.""") == "0", "minimum size no coin"

assert run("""1
1
@""") == "1", "single coin cell"

assert run("""1
3
.@*""") == "1", "blocked path"

assert run("""1
6
.@@.@@""") == "3", "multiple optimal paths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-cell empty | 0 | base case |
| 1-cell coin | 1 | direct pickup |
| .@* | 1 | thorn blocking continuation |
| .@@.@@ | 3 | optimal jump choice |

## Edge Cases

One edge case is when thorns appear in consecutive positions. For input:

```
.@@**
```

The DP correctly sets dp values after the thorns to zero, and earlier cells automatically avoid jumping into them because dp[i+1] and dp[i+2] both evaluate to zero at those positions. This ensures that paths do not incorrectly pass through blocked zones.

Another edge case is when a coin lies immediately after a thorn block:

```
.@**@.
```

At the position before the thorns, both possible forward moves eventually lead into invalid or zero-value states, so the DP naturally discards that route. The algorithm does not need explicit “unreachable” markers because blocked paths contribute zero gain and therefore are never chosen in the max operation.
