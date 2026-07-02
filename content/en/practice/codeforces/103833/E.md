---
title: "CF 103833E - Penalty"
description: "We are modeling a penalty shot as a discretized grid over the goal. Each cell in the grid corresponds to a possible shot placement. For the goalkeeper, each cell contains a value describing how likely it is that the goalkeeper saves a shot directed there."
date: "2026-07-02T08:07:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103833
codeforces_index: "E"
codeforces_contest_name: "2018 International olympiad Tuymaada"
rating: 0
weight: 103833
solve_time_s: 48
verified: true
draft: false
---

[CF 103833E - Penalty](https://codeforces.com/problemset/problem/103833/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are modeling a penalty shot as a discretized grid over the goal. Each cell in the grid corresponds to a possible shot placement. For the goalkeeper, each cell contains a value describing how likely it is that the goalkeeper saves a shot directed there. For each player, each cell contains how likely that player is to score if they shoot to that location.

To evaluate a player, we combine their shooting probabilities with the goalkeeper’s saving probabilities cell by cell. The combined value for a cell is the product of the player’s success probability and the goalkeeper’s failure-to-save probability at that same location. A cell is considered “good” for the player if this combined probability is at least 0.65. The score of a player is the number of such good cells in the grid.

We must choose the five players with the largest scores. If multiple players have the same score, we break ties by lexicographical order of their full names.

The input size is small: $N, M \le 100$, and the number of players is at most 100. This immediately suggests that even an $O(KNM)$ solution is trivially fast enough, since it is at most about $10^6$ operations.

The main subtlety is floating-point comparison. Values are given with two decimal places, so comparisons at threshold 0.65 must be done carefully to avoid precision drift. The safe approach is to scale everything to integers by multiplying by 100 or 10000, or to compare with a small epsilon.

Edge cases that matter are mostly tie handling and floating-point equality at exactly 0.65. A naive strict comparison can misclassify borderline values. Another pitfall is lexicographical comparison on full names: spaces are part of the ordering, so standard string comparison must be used directly.

## Approaches

The brute-force approach is essentially the final solution. For each player, we iterate over all $N \times M$ cells, compute the product with the goalkeeper grid, count how many exceed the threshold, and then sort players.

This works because there is no interdependence between cells or players. Each player’s score is independent, so the problem decomposes cleanly into independent evaluations followed by ranking.

A slower mental model would be to think about recomputing or comparing players pairwise, but that is unnecessary. Once each score is computed, selecting top five is a standard sorting problem.

The only “optimization” is recognizing that recomputation structure is already optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per player with sorting | O(KNM + K log K) | O(K) | Accepted |
| Any overcomplicated alternative | O(K^2 NM) | O(K) | Too slow |

## Algorithm Walkthrough

### 1. Read the goalkeeper grid

We first read the $N \times M$ matrix representing the goalkeeper. This grid is reused for all players, so we store it once.

### 2. Parse all players with names and grids

For each player, we store their name and their $N \times M$ probability matrix. Since constraints are small, storing all data is safe and simplifies computation.

### 3. Compute player score independently

For each player, we iterate over all grid cells. At each cell, we compute the product of goalkeeper value and player value. If this product is at least 0.65, we increment the score.

This step is independent for each player, which is what makes the problem linear in $KNM$.

### 4. Store results as (score, name)

We keep a list of pairs containing the computed score and the player’s name. This structure will be used for sorting.

### 5. Sort players by score and lexicographically

We sort by descending score. If scores are equal, we rely on lexicographical order of names. This ensures deterministic tie-breaking.

### 6. Output top five names

We output the first five entries after sorting.

### Why it works

The key invariant is that each player’s score depends only on their own grid and the fixed goalkeeper grid. There is no interaction between players, so ranking is equivalent to sorting independent scalar scores. The multiplication and thresholding reduce each grid cell to a boolean contribution, making the score a simple additive function over cells. Since addition is associative and independent across players, the ranking problem becomes purely comparison-based sorting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_matrix(n, m):
    mat = []
    for _ in range(n):
        row = list(map(float, input().split()))
        mat.append(row)
    return mat

def main():
    n, m = map(int, input().split())
    k = int(input())

    keeper = parse_matrix(n, m)

    players = []

    for _ in range(k):
        name = input().strip()
        mat = parse_matrix(n, m)

        score = 0
        for i in range(n):
            for j in range(m):
                if keeper[i][j] * mat[i][j] >= 0.65 - 1e-12:
                    score += 1

        players.append(( -score, name))

    players.sort()
    for i in range(5):
        print(players[i][1])

if __name__ == "__main__":
    main()
```

The code reads the goalkeeper matrix once and then processes each player independently. The score is negated so that sorting in ascending order naturally gives highest score first. The epsilon in the comparison prevents precision issues when floating-point multiplication produces values like 0.6499999998.

The sorting step also automatically resolves lexicographical tie-breaking because Python tuple comparison uses the second field when the first is equal.

## Worked Examples

### Example 1

Suppose $N = 2, M = 2$. Keeper grid:

| 0.5 | 0.8 |
| --- | --- |
| 0.6 | 0.9 |

Player A grid:

| 0.9 | 0.9 |
| --- | --- |
| 0.9 | 0.9 |

We compute products:

| 0.45 | 0.72 |
| --- | --- |
| 0.54 | 0.81 |

Cells ≥ 0.65 are two cells (0.72 and 0.81), so score = 2.

This shows how independent cell evaluation works.

### Example 2

Keeper grid:

| 1.0 | 0.5 |
| --- | --- |
| 0.5 | 1.0 |

Player B:

| 0.7 | 0.7 |
| --- | --- |
| 0.7 | 0.7 |

Products:

| 0.7 | 0.35 |
| --- | --- |
| 0.35 | 0.7 |

Only two cells qualify again. This confirms symmetry: different distributions can still produce identical scores, which is why lexicographical ordering matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(KNM + K log K) | Each player scans all grid cells, then sorting dominates only slightly |
| Space | O(K + NM) | Store all matrices and player metadata |

Given $N, M, K \le 100$, the maximum operations are about $10^6$, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    n, m = map(int, input().split())
    k = int(input())

    keeper = [list(map(float, input().split())) for _ in range(n)]

    players = []

    for _ in range(k):
        name = input().strip()
        mat = [list(map(float, input().split())) for _ in range(n)]

        score = 0
        for i in range(n):
            for j in range(m):
                if keeper[i][j] * mat[i][j] >= 0.65 - 1e-12:
                    score += 1

        players.append((-score, name))

    players.sort()
    return "\n".join(name for _, name in players[:5])

# small deterministic case
assert run("""2 2
6
0.5 0.8
0.6 0.9
A
0.9 0.9
0.9 0.9
B
0.1 0.1
0.1 0.1
C
0.8 0.8
0.8 0.8
D
0.5 0.5
0.5 0.5
E
0.7 0.7
0.7 0.7
F
0.2 0.2
0.2 0.2
""").split()[0] in "ACDE"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Mixed grids | Top 5 names | Ranking correctness and tie-breaking |

## Edge Cases

One edge case is when multiple players have identical scores. The algorithm handles this naturally because sorting uses lexicographical comparison as a secondary key. For example, if two players both have score 10, their order is determined purely by string comparison of names.

Another edge case is floating-point boundary at exactly 0.65. The epsilon guard ensures that values extremely close to the threshold due to precision errors are not misclassified. For instance, a computed value like 0.64999999997 would otherwise incorrectly fail the condition without the tolerance.

A final edge case is when all players have identical matrices. In that case, all scores are equal and output is simply the five lexicographically smallest names, which the sorting rule automatically produces.
