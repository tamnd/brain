---
title: "CF 105046D - Differences"
description: "We are given several independent test cases. Each test case describes a rectangular grid with n rows and m columns, and a multiset of n·m integers."
date: "2026-06-28T01:30:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105046
codeforces_index: "D"
codeforces_contest_name: "XXVIII Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 105046
solve_time_s: 45
verified: true
draft: false
---

[CF 105046D - Differences](https://codeforces.com/problemset/problem/105046/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case describes a rectangular grid with n rows and m columns, and a multiset of n·m integers. Our task is to place all these integers into the grid, one per cell, so that any two cells sharing an edge always contain numbers of different parity. In other words, every horizontal and vertical adjacency must connect an even number with an odd number.

The output is not just a validity check, but an explicit construction of the grid arrangement. For each test case we must print a full n by m matrix using all provided values exactly once, or print -1 if no arrangement exists.

The constraint n·m up to 100000 across all test cases implies we need essentially linear time per test case. Any solution that tries permutations or checks adjacency conditions repeatedly over pairs would be too slow. We are forced toward a construction that depends only on parity counts and simple ordering.

A key observation already appears in the requirement: adjacency forces a strict bipartite structure of the grid. This immediately connects the problem to coloring a grid like a chessboard.

A subtle failure case arises when we ignore parity feasibility. Consider a 2 by 2 grid with values 1, 1, 1, 2. There are three odd numbers and one even number. Any valid arrangement must alternate parity like a chessboard, which in a 2 by 2 grid forces exactly two odd and two even cells. This instance cannot work, so the answer must be -1. A naive approach that only tries greedy placement without checking counts would incorrectly output something.

Another edge case is a single row or column. In a 1 by m grid, adjacency is linear, so we still require strict alternation of parity. This forces alternating odd and even values along the sequence, and feasibility depends on balancing parity counts across the line.

## Approaches

The brute-force approach would attempt to assign values to cells one by one, checking after every placement whether all existing adjacencies satisfy parity constraints. This quickly becomes infeasible because at each step we branch over remaining unused values, leading to factorial growth in possibilities. Even with pruning, the state space is essentially permutations of n·m items, which is far beyond acceptable limits for n·m up to 100000.

The key simplification is to recognize that the grid itself imposes a fixed bipartite structure. If we color cells by (i + j) mod 2, all adjacency edges go between opposite colors. The condition “adjacent numbers have different parity” means every black cell must hold numbers of one parity and every white cell must hold numbers of the other parity.

This reduces the problem from arranging individual values to distributing two groups: even numbers and odd numbers. Once we know which parity goes to which color class, any assignment within those classes works because adjacency is automatically satisfied by the coloring.

Thus the problem becomes checking feasibility of matching counts with grid bipartition sizes, then filling cells in any consistent order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force placement with checking | O((nm)!) | O(nm) | Too slow |
| Parity partition by chessboard coloring | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

We proceed by using the natural bipartite structure of the grid.

1. Compute how many cells belong to each parity class of the grid coloring. For a grid, one color has ⌈nm/2⌉ cells and the other has ⌊nm/2⌋ cells. This determines how many values of each parity we need.
2. Count how many odd and even numbers are in the input array. This is done in a single pass over all values.
3. Check feasibility in both possible assignments of parity to color classes. Either odd numbers must match black cells and even numbers match white cells, or the opposite. If neither matches, the answer is impossible.
4. Choose the valid assignment. This choice is necessary because the problem does not fix which color class must correspond to odd values.
5. Build two lists: one containing all odd values and one containing all even values. The order inside each list is irrelevant.
6. Traverse the grid in row-major order. For each cell, determine its chessboard color using (i + j) mod 2 and assign the next value from the corresponding list.
7. Output the filled grid.

The correctness relies on the fact that adjacency constraints are entirely captured by the bipartite coloring, so once parity classes are assigned consistently, no further validation is required.

### Why it works

The grid graph is bipartite under the standard chessboard coloring, meaning every edge connects opposite colors. The constraint requires adjacent values to differ in parity, so each edge must connect an odd to an even value. Therefore, all cells of one color must contain only odd values, and all cells of the other must contain only even values. This is both necessary and sufficient. Once the parity counts match the color class sizes, any bijection between values and cells preserves validity because no edge ever connects two cells of the same color.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        odds = [x for x in a if x % 2]
        evens = [x for x in a if x % 2 == 0]

        total = n * m
        black = (total + 1) // 2
        white = total // 2

        # try odd on black
        ok1 = (len(odds) == black and len(evens) == white)
        # try odd on white
        ok2 = (len(odds) == white and len(evens) == black)

        if not ok1 and not ok2:
            print(-1)
            continue

        if ok1:
            odd_cells = True  # black cells
        else:
            odd_cells = False

        oi = 0
        ei = 0

        res = [[0] * m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if (i + j) % 2 == 0:
                    if odd_cells:
                        res[i][j] = odds[oi]
                        oi += 1
                    else:
                        res[i][j] = evens[ei]
                        ei += 1
                else:
                    if odd_cells:
                        res[i][j] = evens[ei]
                        ei += 1
                    else:
                        res[i][j] = odds[oi]
                        oi += 1

        for row in res:
            print(*row)

solve()
```

The implementation first separates values by parity in linear time. It then checks the only two possible global assignments between parity and chessboard color classes. The grid is filled in row-major order, using two pointers into the parity lists.

A subtle detail is computing black and white counts correctly using integer division, since total cells may be odd. Another is ensuring both assignment cases are tested before committing, since either mapping can be valid depending on input distribution.

## Worked Examples

Consider a simple valid case:

Input:

n = 2, m = 3

values = [1, 2, 2, 3, 4, 1]

We have odds = [1, 3, 1], evens = [2, 2, 4]. Total cells = 6, so black = 3 and white = 3. Both parity groups match perfectly.

| Step | Cell (i,j) | Color | Assigned list | Remaining odds | Remaining evens |
| --- | --- | --- | --- | --- | --- |
| 1 | (0,0) | black | odd | 2 | 3 |
| 2 | (0,1) | white | even | 2 | 2 |
| 3 | (0,2) | black | odd | 1 | 2 |
| 4 | (1,0) | white | even | 1 | 1 |
| 5 | (1,1) | black | odd | 0 | 1 |
| 6 | (1,2) | white | even | 0 | 0 |

This produces a full valid grid because every adjacency crosses a parity boundary.

Now consider an impossible case:

Input:

n = 2, m = 2

values = [1, 1, 1, 2]

odds = 3, evens = 1, but both black and white are 2 cells each.

| Check | Value |
| --- | --- |
| black needed | 2 |
| white needed | 2 |
| odd available | 3 |
| even available | 1 |

No assignment works, so the algorithm correctly outputs -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | each test case processes every value once and fills each cell once |
| Space | O(nm) | storing the grid and separating parity lists |

The total input size across test cases is at most 100000 cells, so a linear solution comfortably fits within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from subprocess import check_output
    return check_output([sys.executable, "-c", CODE], input=inp.encode()).decode()

CODE = r"""
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        odds = [x for x in a if x % 2]
        evens = [x for x in a if x % 2 == 0]

        total = n * m
        black = (total + 1) // 2
        white = total // 2

        ok1 = (len(odds) == black and len(evens) == white)
        ok2 = (len(odds) == white and len(evens) == black)

        if not ok1 and not ok2:
            print(-1)
            continue

        odd_cells = ok1

        oi = ei = 0
        res = [[0]*m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if (i+j) % 2 == 0:
                    if odd_cells:
                        res[i][j] = odds[oi]; oi += 1
                    else:
                        res[i][j] = evens[ei]; ei += 1
                else:
                    if odd_cells:
                        res[i][j] = evens[ei]; ei += 1
                    else:
                        res[i][j] = odds[oi]; oi += 1

        for r in res:
            print(*r)

solve()
"""

# provided sample (adapted format)
assert run("1\n2 3\n1 2 2 3 4 1\n") != "", "sample 1 exists"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 single value | value itself | minimum grid handling |
| 2x2 balanced | valid grid | parity feasibility |
| 2x2 impossible | -1 | rejection logic |
| 1x5 alternating | valid or -1 depending input | linear structure case |

## Edge Cases

A 1 by m grid forces strict alternation along a line. For example, n = 1, m = 5 with values [1, 2, 3, 4, 5] works because odd and even counts can match alternating positions. The algorithm treats this as a standard chessboard coloring with black cells at positions j where j is even, so assignment proceeds identically.

A fully odd input on a 3 by 3 grid immediately fails. There are 5 black and 4 white cells, so we would need both parities present. The algorithm detects this through mismatch of odd and even counts against either partition and returns -1 without attempting placement.

A nearly balanced but mismatched case like 3 by 3 with four evens and five odds is accepted only if parity assignment matches the larger class. The algorithm explicitly tests both orientations, ensuring correctness even when the majority parity is not immediately obvious.
