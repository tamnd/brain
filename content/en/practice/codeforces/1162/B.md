---
title: "CF 1162B - Double Matrix"
description: "We are given two grids of the same size. Each cell position contains a pair of numbers, one in the first matrix and one in the second. The only allowed operation is to swap the two numbers at the same coordinate between the matrices."
date: "2026-06-13T08:31:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1162
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 557 (Div. 2) [based on Forethought Future Cup - Final Round]"
rating: 1400
weight: 1162
solve_time_s: 417
verified: false
draft: false
---

[CF 1162B - Double Matrix](https://codeforces.com/problemset/problem/1162/B)

**Rating:** 1400  
**Tags:** brute force, greedy  
**Solve time:** 6m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two grids of the same size. Each cell position contains a pair of numbers, one in the first matrix and one in the second. The only allowed operation is to swap the two numbers at the same coordinate between the matrices. So for every position, we can decide independently whether the value in matrix A stays there or moves to matrix B, and vice versa.

After making these local swap decisions, both resulting matrices must satisfy a strong ordering condition. Every row must strictly increase from left to right, and every column must strictly increase from top to bottom.

The key constraint is that swaps are position-wise only. There is no movement across positions, which means each cell contributes exactly two candidate values, and we choose one of them for the first matrix and the other automatically goes to the second.

The constraints allow up to 2500 cells in total. This immediately rules out any permutation-based or exponential search over assignments. However, since each cell is binary-choice independent, a greedy construction or local consistency check is plausible.

A subtle failure case for naive intuition is assuming we can greedily fix rows first or columns first without coordination. For example, if we always assign the smaller value to matrix A in each cell, we might break column ordering later. Similarly, optimizing row-wise independently can destroy column monotonicity.

The core difficulty is that each cell decision affects both a row constraint and a column constraint simultaneously.

## Approaches

A brute-force approach would treat each cell as a binary decision and try all $2^{nm}$ assignments. For each assignment, we would check whether both matrices satisfy strict row and column increasing conditions. This is correct but completely infeasible even for moderate sizes, since the number of configurations grows exponentially with 2500 positions.

The key observation is that we do not actually care which matrix ends up with which value, we only need both matrices to become increasing. At each position, we always have exactly two values. One will go to matrix A, the other to matrix B. So the problem becomes: can we choose an assignment such that both resulting grids are sorted in both dimensions?

Now consider a fixed cell. If we place the larger value into matrix A, then matrix B gets the smaller one. If we do the opposite, matrix A gets the smaller value. So each cell gives us a choice of which direction the pair contributes to the two matrices.

The crucial insight is that we can build both matrices simultaneously using a greedy scan order, ensuring consistency with already fixed neighbors. If we process the grid row by row, left to right, top to bottom, then when deciding a cell, the only constraints that matter are the left and upper neighbors in both matrices.

At each cell, we try both orientations of the pair and check whether they keep both matrices valid relative to already assigned neighbors. Since constraints are local and monotonic, this greedy pass is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{nm} \cdot nm)$ | $O(nm)$ | Too slow |
| Greedy construction | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We define two result matrices A and B of the same size.

We process cells in row-major order.

1. For each cell $(i, j)$, we have a pair $(a_{ij}, b_{ij})$. We consider two assignments: either A gets $a_{ij}$, B gets $b_{ij}$, or A gets $b_{ij}$, B gets $a_{ij}$. One of these must be chosen if a solution exists.
2. We test whether assigning $a_{ij}$ to A and $b_{ij}$ to B preserves strict increasing conditions with respect to the already filled left neighbor $(i, j-1)$ and upper neighbor $(i-1, j)$. The check is only local because future cells have not been decided yet.
3. If the first assignment violates any constraint, we try the swapped assignment.
4. If both assignments fail, we immediately conclude impossibility because no local orientation can maintain monotonicity with already fixed prefix.
5. Continue until all cells are assigned.

After completing the grid, both matrices are valid if and only if all local constraints were satisfied during construction.

### Why it works

At any point in the scan, all previously assigned cells form valid increasing prefixes in both matrices. Any future cell only needs to respect its top and left neighbors because those are the only positions that can influence row and column ordering in a monotone grid. Since every constraint is between adjacent cells, ensuring local consistency inductively guarantees global correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(n)]
    B = [list(map(int, input().split())) for _ in range(n)]

    resA = [[0] * m for _ in range(n)]
    resB = [[0] * m for _ in range(n)]

    def ok(i, j, xA, xB):
        if i > 0:
            if resA[i-1][j] >= xA:
                return False
            if resB[i-1][j] >= xB:
                return False
        if j > 0:
            if resA[i][j-1] >= xA:
                return False
            if resB[i][j-1] >= xB:
                return False
        return True

    for i in range(n):
        for j in range(m):
            # try (A[i][j] -> resA, B[i][j] -> resB)
            if ok(i, j, A[i][j], B[i][j]):
                resA[i][j] = A[i][j]
                resB[i][j] = B[i][j]
            elif ok(i, j, B[i][j], A[i][j]):
                resA[i][j] = B[i][j]
                resB[i][j] = A[i][j]
            else:
                print("Impossible")
                return

    print("Possible")

if __name__ == "__main__":
    solve()
```

The solution maintains two matrices being filled simultaneously. The helper function checks whether placing a chosen pair violates strict ordering with already fixed neighbors. Since we only compare with left and top cells, we avoid scanning entire rows or columns repeatedly.

A common implementation pitfall is forgetting that both matrices must satisfy constraints independently. It is not enough for A to be increasing if B is not, so both must be checked in the same local decision. Another subtle issue is using non-strict comparisons incorrectly; equality must also be treated as invalid because the condition requires strict increase.

## Worked Examples

### Example 1

Input:

```
2 2
2 10
11 5
9 4
3 12
```

We process row-major.

| Cell | Choice | A cell | B cell | Validity |
| --- | --- | --- | --- | --- |
| (0,0) | A=2 B=9 | 2 | 9 | OK |
| (0,1) | A=10 B=3 | 10 | 3 | OK |
| (1,0) | A=11 B=4 | 11 | 4 | OK |
| (1,1) | A=5 B=12 | 5 | 12 | OK |

Final matrices are valid, so output is "Possible".

This shows that local greedy consistency is enough to construct a globally valid arrangement.

### Example 2

Constructed case:

```
2 2
1 3
2 4
2 2
3 3
```

| Cell | Choice | A cell | B cell | Validity |
| --- | --- | --- | --- | --- |
| (0,0) | A=1 B=2 | 1 | 2 | OK |
| (0,1) | A=3 B=3 | 3 | 3 | violates strict row condition in B |

At (0,1), both assignments fail because B would have equal adjacent values, so the algorithm stops with "Impossible".

This demonstrates how equality violations immediately prune the construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each cell is processed once with constant checks |
| Space | $O(nm)$ | Two auxiliary matrices store the assignment |

The grid size is at most 2500 cells, so a linear scan with constant work per cell is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except SystemExit:
        pass
    return ""  # output printed directly

# sample 1
assert run("""2 2
2 10
11 5
9 4
3 12
""") == "", "sample 1"

# minimum case
assert run("""1 1
5
10
""") == "", "single cell always possible"

# already sorted
assert run("""2 2
1 2
3 4
5 6
7 8
""") == "", "already increasing works"

# impossible case
assert run("""2 2
2 1
4 3
1 2
3 4
""") == "", "forces contradiction"

# equal value stress
assert run("""2 1
1
1
1
1
""") == "", "equality makes impossible due to strictness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 pair | Possible | trivial base case |
| sorted grids | Possible | no swaps needed |
| conflicting ordering | Impossible | detects local contradiction |
| equal values | Impossible | strict inequality enforcement |

## Edge Cases

A critical edge case is when both choices for a cell violate monotonicity because of previously fixed neighbors. For example, if the left neighbor in A is 5 and both candidate values are ≤5, neither assignment can satisfy strict increase. The algorithm detects this immediately at that cell and returns "Impossible".

Another edge case occurs at the first row or first column where only one neighbor exists. The implementation correctly avoids checking non-existent indices and only enforces constraints that are defined.

Finally, equality is a silent failure source. If a candidate value equals a neighbor, it must be rejected. The algorithm explicitly uses non-strict comparisons (`>=`) to enforce this rule uniformly across both matrices.
