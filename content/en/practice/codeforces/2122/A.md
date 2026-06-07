---
title: "CF 2122A - Greedy Grid"
description: "We are working on a grid where each cell contains a nonnegative number, and we are only allowed to move either right or down starting from the top-left corner. Any such path from the top-left to the bottom-right has a total score equal to the sum of all visited cells."
date: "2026-06-08T03:41:13+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2122
codeforces_index: "A"
codeforces_contest_name: "Order Capital Round 1 (Codeforces Round 1038, Div. 1 + Div. 2)"
rating: 800
weight: 2122
solve_time_s: 69
verified: true
draft: false
---

[CF 2122A - Greedy Grid](https://codeforces.com/problemset/problem/2122/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a grid where each cell contains a nonnegative number, and we are only allowed to move either right or down starting from the top-left corner. Any such path from the top-left to the bottom-right has a total score equal to the sum of all visited cells.

Among all possible right-down paths, some achieve the maximum possible sum. Independently, there is a deterministic way to generate a path called a greedy path: at every step, you look at the cell to the right and the cell below, and you move to the one with the larger value, or choose either if they are equal.

The question is whether it is possible to construct an n by m grid such that every greedy path is strictly suboptimal, meaning no greedy path achieves the maximum possible path sum.

The input consists of multiple independent grid dimensions. For each pair n, m, we must decide whether such a construction exists.

The constraints are small enough that each test can be answered in constant time reasoning per case. With up to 5000 test cases and n, m up to 100, any solution that tries to explicitly construct or simulate grids is unnecessary. The structure of the problem suggests a pure combinational condition depending only on the shape of the grid.

A subtle edge case is when one of the dimensions is 1. In a 1 by m or n by 1 grid, there is only one possible path, and it is simultaneously greedy and optimal. So any construction trying to separate greedy from optimal paths is impossible there.

Another important edge case is when both dimensions are at least 2. It is tempting to assume greedy behavior is always close to optimal, but small grids like 2 by 2 already allow conflicting choices between local and global optimality.

## Approaches

A brute-force perspective would be to attempt all possible grids of reasonable size, enumerate all down-right paths, compute the maximum path sum, and then simulate the greedy path rule to see if it ever matches the optimum. This immediately becomes infeasible because even for a 5 by 5 grid there are binomially many paths, and the number of possible grids is infinite over nonnegative integers.

The key insight is that the question does not depend on actual values, but only on whether local greedy decisions can be globally misleading. This reduces the problem to reasoning about whether the grid shape forces a unique path or allows a conflict between two directions at the start.

If either dimension is 1, the path is unique, so greedy is trivially optimal. If both dimensions are at least 2, we can construct a simple counterexample where the optimal path requires initially moving in the direction that looks worse locally, while the greedy rule is forced to take the locally better neighbor and gets trapped into a suboptimal corridor. The sample construction already demonstrates this behavior for a 3 by 3 grid, and the same idea scales to any larger grid by embedding such a structure.

The conclusion is that the answer depends only on whether both dimensions exceed 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | Exponential | Too slow |
| Constant-time logic | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the pair n and m for the grid dimensions. These define the shape of all valid paths.
2. Check whether either n equals 1 or m equals 1. This identifies a degenerate grid where movement is forced along a single line.
3. If one dimension is 1, output NO because there is exactly one path, so greedy and optimal coincide by necessity.
4. Otherwise, both n and m are at least 2. In this case, output YES because we can construct a grid where greedy decisions at the start force a suboptimal trajectory.

The reasoning behind step 4 is that having at least one 2 by 2 substructure is enough to create a local versus global conflict. The greedy rule only looks one step ahead, while the optimal path can depend on longer-range structure, so a construction exists that misleads the greedy choice.

### Why it works

The correctness rests on a structural dichotomy of the grid graph. When either dimension is 1, the grid graph degenerates into a path graph with exactly one source-to-sink route, eliminating any choice and making greedy vacuously optimal. When both dimensions are at least 2, the grid contains a junction where two different first moves are available, and it is possible to assign values so that the locally better neighbor leads into a region with strictly worse total sum than the alternative branch. This separation between local comparison and global accumulation is sufficient to ensure that greedy cannot always achieve optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    if n == 1 or m == 1:
        print("NO")
    else:
        print("YES")
```

The solution reduces the entire problem to a single structural check per test case. The key implementation detail is that no simulation or construction is required. The condition is purely based on whether branching is possible in the grid graph.

The only subtlety is ensuring correct handling of the 1-dimensional cases. Both 1 by m and n by 1 grids must be treated symmetrically, since in both cases there is exactly one monotone path.

## Worked Examples

### Example 1

Input:

```
3 3
```

| Step | n | m | Decision | Reason |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | YES | both dimensions exceed 1 |

This case confirms that once a grid has at least one internal choice point, we can design values so greedy is forced into a suboptimal corridor.

### Example 2

Input:

```
1 5
```

| Step | n | m | Decision | Reason |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | NO | only one path exists |

This case shows that when movement is linear, greedy cannot deviate from the unique optimal path, so separation is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | each test case is a constant-time comparison |
| Space | O(1) | no auxiliary structures are used |

The solution scales directly with the number of test cases, and even at 5000 tests it runs instantly because each decision is a single conditional check.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        out.append("YES" if n > 1 and m > 1 else "NO")
    return "\n".join(out) + "\n"

# provided samples
assert run("""2
3 3
1 2
""") == """YES
NO
"""

# custom cases
assert run("""4
1 1
1 10
10 1
2 2
""") == """NO
NO
NO
YES
"""

assert run("""3
2 3
3 2
4 4
""") == """YES
YES
YES
"""

assert run("""1
100 100
""") == """YES
"""

assert run("""1
1 100
""") == """NO
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1, 1xN, Nx1, 2x2 | NO NO NO YES | all boundary degeneracies |
| mixed 2x3, 3x2, 4x4 | YES YES YES | general valid constructions |
| 100x100 | YES | large dimension behavior |
| 1x100 | NO | single-row edge case |

## Edge Cases

A 1 by 1 grid is the most degenerate case. The algorithm reads n equals 1 or m equals 1 and immediately outputs NO. There is exactly one path consisting of the single cell, so greedy and optimal are identical.

For a 1 by 5 grid, the check triggers the same condition. The loop over test cases sees m equals 5 and n equals 1, so it outputs NO without further logic. This matches the fact that there is no branching point where greedy could make a wrong choice.

For a 2 by 2 grid, both n and m exceed 1, so the algorithm outputs YES. This corresponds to the existence of a local decision at the start that can be exploited by a constructed grid to mislead greedy selection away from the globally optimal path.
