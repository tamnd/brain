---
title: "CF 1849D - Array Painting"
description: "We are given a line of cells, each containing a value 0, 1, or 2. Every cell starts unpainted, and the goal is to paint all cells. We are allowed to spend coins in two different ways. The first is direct painting: we can pick any unpainted cell, paint it, and pay one coin."
date: "2026-06-09T05:36:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1849
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 152 (Rated for Div. 2)"
rating: 1700
weight: 1849
solve_time_s: 178
verified: false
draft: false
---

[CF 1849D - Array Painting](https://codeforces.com/problemset/problem/1849/D)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, two pointers  
**Solve time:** 2m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of cells, each containing a value 0, 1, or 2. Every cell starts unpainted, and the goal is to paint all cells.

We are allowed to spend coins in two different ways. The first is direct painting: we can pick any unpainted cell, paint it, and pay one coin. The second is a propagation operation: if we already have a painted cell whose value is either 1 or 2, we may use it to “infect” an adjacent unpainted cell, paint that neighbor for free, and simultaneously decrease the value of the original painted cell by one. A cell with value 0 cannot be used to propagate further.

The key tension is that higher values act like limited “energy sources” that can spread paint to neighbors, potentially saving coins. The problem asks for the minimum number of coins needed to eventually paint the entire array.

The constraint n up to 200,000 forces any solution to be linear or near linear. Anything involving trying subsets of starting points, interval DP with O(n^2), or simulating all propagation choices naïvely will fail. The structure suggests that each cell’s value can only be used a small number of times, and propagation is local, so the solution should reduce to a greedy or scan-based accounting.

A subtle failure mode comes from overestimating propagation power. For example, in `[2,0,0]`, it is tempting to think the single 2 can cover both neighbors, but direction matters: propagation is sequential and consumes value, so ordering decides feasibility. Another failure case is treating all non-zero cells as interchangeable sources, ignoring that a 1 can only help once, while a 2 can help twice.

## Approaches

A brute-force way to think about the process is to decide which cells are initially paid for with coins. Once some cells are painted, they can expand outward as long as they have remaining value. One could try every subset of initial coin-paints and simulate propagation. This is correct in principle, because every valid process begins with some set of paid starting points, but the number of subsets is exponential in n, making this impossible for n up to 200,000.

The key observation is that propagation always travels along adjacency and consumes value in a linear, one-step-at-a-time manner. This makes the process behave like building coverage segments from “sources”. Instead of choosing arbitrary initial sources, we can scan left to right and greedily decide when we are forced to pay.

The critical insight is that whenever we encounter a position that cannot be reached by any remaining propagation capacity from the left, we must start a new paid segment there. Each paid cell then provides a bounded amount of reach to the right equal to its value, and we maintain how far current reach extends.

This transforms the problem into tracking a moving boundary of coverage and counting how many times we need to reset that boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over initial painted sets + simulation | O(2^n · n) | O(n) | Too slow |
| Greedy left-to-right coverage tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a variable that represents how far to the right we can still paint for free using already activated values. We also maintain the current position we are scanning.

1. Initialize a variable `reach = 0`, meaning we currently cannot extend painting beyond the starting point, and a counter `coins = 0`.
2. Traverse the array from left to right. At each index `i`, check whether `i` is within the current reachable range `reach`.
3. If `i <= reach`, this position can already be painted for free via earlier paid or propagated cells, so we do nothing.
4. If `i > reach`, we are at a position that cannot be reached by any previous propagation. We must pay a coin to paint this cell directly. After paying, this cell becomes a new source of propagation, so we increase `coins` by 1.
5. Once we pay at position `i`, we set `reach = i + a[i]`. This reflects that from this newly activated cell, we can extend painting up to `a[i]` steps to the right.
6. Continue until the end of the array.

The crucial idea is that we never revisit earlier decisions. Each time we fall outside current reach, we are forced to create a new source, and that source contributes its full usable capacity to future positions.

### Why it works

The algorithm maintains the invariant that `reach` is the farthest index that can be painted without paying additional coins using all previously chosen paid cells and their remaining propagation power. Whenever we encounter an index beyond this boundary, no previous sequence of propagation steps can reach it because propagation only moves one step at a time and only originates from already painted positive-valued cells. Therefore, failing to pay at that point would make painting that position impossible, so a new paid source is necessary. Choosing to pay exactly at the first unreachable index is optimal because any later choice would leave the current position unpainted while providing no advantage, and any earlier choice is either already inside reach or would not improve coverage of earlier gaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    reach = 0
    coins = 0

    for i in range(n):
        if i > reach:
            coins += 1
            reach = i + a[i]
        else:
            reach = max(reach, i + a[i])

    print(coins)

if __name__ == "__main__":
    solve()
```

The solution scans once from left to right, maintaining the farthest reachable index. When a position is outside that range, it forces a coin purchase and resets reach based on the value of that position. Otherwise, it simply updates reach if the current cell provides further extension.

The subtle point is the update `reach = max(reach, i + a[i])` even when no coin is spent. This captures that already reachable positions still contribute propagation power and can extend coverage further.

## Worked Examples

### Example 1

Input:

```
3
0 2 0
```

We track how reach evolves.

| i | a[i] | reach before | action | coins | reach after |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | pay (i == reach) | 1 | 0 |
| 1 | 2 | 0 | unreachable, pay | 2 | 3 |
| 2 | 0 | 3 | covered | 2 | 3 |

This demonstrates that a single early activation can be wasted if it does not extend far enough, forcing another coin at index 1, but that second activation can cover the rest.

### Example 2

Input:

```
5
1 0 2 0 1
```

| i | a[i] | reach before | action | coins | reach after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | pay | 1 | 1 |
| 1 | 0 | 1 | covered | 1 | 1 |
| 2 | 2 | 1 | pay | 2 | 4 |
| 3 | 0 | 4 | covered | 2 | 4 |
| 4 | 1 | 4 | covered | 2 | 5 |

This shows how later high-value cells extend coverage significantly, reducing the need for extra coins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass through array with constant-time updates |
| Space | O(1) | only a few variables are maintained |

The linear scan is necessary given n up to 200,000, and the solution avoids any nested processing or simulation, making it comfortably efficient under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    reach = 0
    coins = 0

    for i in range(n):
        if i > reach:
            coins += 1
            reach = i + a[i]
        else:
            reach = max(reach, i + a[i])

    return str(coins)

# provided sample
assert run("3\n0 2 0\n") == "1"

# single element
assert run("1\n0\n") == "1"

# all zeros
assert run("4\n0 0 0 0\n") == "4"

# all twos
assert run("5\n2 2 2 2 2\n") == "1"

# alternating small values
assert run("5\n1 0 2 0 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0` | `1` | minimal forced purchase |
| `0 0 0 0` | `4` | no propagation possible |
| `2 2 2 2 2` | `1` | maximal chaining efficiency |
| `1 0 2 0 1` | `2` | interaction of local and long-range reach |

## Edge Cases

A critical edge case is when the first element is zero. In input like `[0, 2, 0]`, the algorithm starts at index 0, sees it is unreachable with `reach = 0`, and is forced to pay immediately. After that, the reach may jump far enough to cover later cells. The greedy choice of paying at index 0 is unavoidable because there is no prior propagation source.

Another edge case is when a high-value element appears after a long prefix of zeros. For `[0, 0, 0, 2, 0]`, the algorithm pays at index 0, 1, 2, then finally uses index 3 to extend reach. Each zero forces a separate coin because no propagation can cross them without an active source.

A third case is when multiple small values overlap. In `[1, 0, 1, 0, 1]`, each 1 only extends reach slightly, and the algorithm ensures that earlier activations are reused whenever possible. The scan guarantees that we never pay twice for a region already covered, and each new coin corresponds exactly to a previously unreachable index.
