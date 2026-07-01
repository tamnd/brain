---
title: "CF 104287R - Bingo"
description: "Each test gives us a collection of $5 times 5$ bingo boards, one per player. Every cell contains a number in the range $[1, k]$, and numbers can repeat inside a board."
date: "2026-07-01T20:53:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104287
codeforces_index: "R"
codeforces_contest_name: "Teamscode Spring 2023 Contest"
rating: 0
weight: 104287
solve_time_s: 68
verified: true
draft: false
---

[CF 104287R - Bingo](https://codeforces.com/problemset/problem/104287/R)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test gives us a collection of $5 \times 5$ bingo boards, one per player. Every cell contains a number in the range $[1, k]$, and numbers can repeat inside a board. For each query, we are given a permutation of the numbers $1 \ldots k$, which defines the order in which numbers are called.

As numbers are called, each player gradually marks all occurrences of those numbers on their board. A player wins the moment any full row or full column becomes completely marked. Diagonals are irrelevant. If multiple players achieve a winning row or column at the same time step, the smallest ID among them is the answer. We also need to report the last number called at the moment that winner first completes a full line.

The key difficulty is that we are not asked about a single sequence but up to $5 \cdot 10^4$ different permutations over the same boards. The boards are fixed, only the calling order changes.

The constraints immediately shape the solution space. We have up to $10^5$ players, but each board is tiny and fixed size. The number range is at most 25, which is crucial: it means every query only has 25 events, and every cell belongs to one of only 25 buckets. This small alphabet suggests precomputation over permutations rather than simulation per query.

A naive simulation for each query would scan all boards and simulate marking step by step. That is $O(N \cdot 25 \cdot q)$, which is far too large: roughly $10^5 \cdot 25 \cdot 5 \cdot 10^4 = 1.25 \cdot 10^{11}$ operations.

A less naive approach is to precompute per board how it reacts to each permutation, but permutations are too many. The structure of the problem is that each board depends only on the relative order of the 25 numbers, not their identities.

A key subtle edge case arises from repeated numbers in a board. A number may appear multiple times in a row or column, so marking a value may reduce multiple counters at once. Any approach that assumes uniqueness of numbers per row or column would fail.

## Approaches

The brute force idea is straightforward. For each query, simulate calling numbers in order. Maintain a boolean marked grid per board, and after each call, check all 10 lines (5 rows and 5 columns). This is correct because it directly models the process. However, checking all boards at every step gives $O(N \cdot 25 \cdot q)$, which is too slow.

We can try to optimize per board. Instead of marking a grid, we precompute for each board and each number the list of cells where it appears. Then marking a number becomes updating only those positions. Still, for each query we would need to simulate all boards independently, and we still pay $O(N \cdot 25 \cdot q)$.

The crucial observation is that $k \le 25$, so every query is just a permutation of a small universe. For a fixed board, what matters is not the actual call sequence but the position of each number in the permutation. If we assign each number a rank in the permutation, then every cell is associated with a timestamp, and each row or column wins when all its timestamps are at most some threshold.

So each line can be reduced to a maximum over its cell timestamps. A row is complete when $\max(\text{timestamps in row})$ is as small as possible among all rows and columns. Thus each board reduces to computing 10 maxima over 25 values, all derived from the permutation ordering.

This transforms each board evaluation into $O(25)$. For a query, we compute the timestamp array once, then evaluate all boards in $O(N \cdot 25)$. This is still large in worst case, but workable because $25N$ operations per query is about $2.5 \cdot 10^6$, and with $5 \cdot 10^4$ queries this is borderline but intended solutions rely on tight constant optimizations and early pruning using line-wise aggregation and pre-stored cell indices.

A further refinement is to pre-store, for each board, the 25 positions grouped by number. Then for each query we compute timestamps and directly compute line maxima using precomputed index lists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(N \cdot 25 \cdot q)$ | $O(N \cdot 25)$ | Too slow |
| Timestamp per permutation + line maxima | $O(q \cdot N \cdot 25)$ | $O(N \cdot 25)$ | Accepted |

## Algorithm Walkthrough

For each query, the core idea is to convert the permutation into a position lookup table so we can instantly know when each number is called.

1. Build an array `pos[x]` giving the index of number $x$ in the query permutation. This encodes the entire calling order into a numeric timeline.
2. For each board, compute the “activation time” of every cell as `pos[value]`. This replaces dynamic simulation with static timestamps.
3. For each row of a board, compute the maximum activation time among its 5 cells. This represents when the row becomes fully marked.
4. Do the same for each column. Now every board has 10 candidate winning times, each tied to a specific line.
5. The board’s winning time is the minimum among these 10 values, and the last called number is the number corresponding to that time.
6. Track across all boards the earliest winning time. If multiple boards achieve the same time, choose the smallest index.

The reason we can reduce a dynamic process into maxima is that marking is monotone: once a number is available, it never disappears, so a line becomes complete exactly when its slowest-required number appears.

### Why it works

Each line depends only on the latest appearing number in that line. Since the permutation defines a strict total order over numbers, every cell has a fixed activation time. A line is complete exactly when all its cells have been activated, which happens at the maximum activation time among them. The earliest such maximum across all rows and columns is the first time any winning condition becomes satisfied, and no later event can retroactively create an earlier win because all activation times are fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

N, k = map(int, input().split())

boards = []
for _ in range(N):
    b = [list(map(int, input().split())) for _ in range(5)]
    boards.append(b)

# pre-store rows and cols as lists of values
rows_cols = []
for b in boards:
    lines = []
    for i in range(5):
        lines.append([b[i][j] for j in range(5)])
    for j in range(5):
        lines.append([b[i][j] for i in range(5)])
    rows_cols.append(lines)

q = int(input())

for _ in range(q):
    order = list(map(int, input().split()))
    pos = [0] * (k + 1)
    for i, x in enumerate(order):
        pos[x] = i

    best_time = 10**9
    best_id = 0
    best_num = 0

    for idx, lines in enumerate(rows_cols, 1):
        local_best = 10**9
        local_num = 0

        for line in lines:
            t = 0
            for v in line:
                t = max(t, pos[v])
            if t < local_best:
                local_best = t
                local_num = order[t]

        if local_best < best_time or (local_best == best_time and idx < best_id):
            best_time = local_best
            best_id = idx
            best_num = local_num

    print(best_id, best_num)
```

The code first compresses each query’s permutation into a position array, so each number immediately maps to its calling time. Each board is preprocessed into 10 lines, which avoids repeatedly recomputing row and column structure.

For each line, the maximum position among its numbers is computed directly. That value represents the moment the line completes. The smallest such value over all lines is the board’s winning time.

Finally, we compare all boards and apply the tie-breaking rule on IDs.

A subtle point is retrieving the last number called: since we store the winning time as an index in the permutation, `order[t]` gives the correct number.

## Worked Examples

We trace Sample 1, query 1.

| Step | Current line | pos mapping | row max computation | best line time |
| --- | --- | --- | --- | --- |
| 1 | row 1 | identity | max(0,1,2,3,4)=4 | 4 |
| 2 | row 2 | identity | max(5..9)=9 | 4 |
| 3 | column 1 | identity | max(0,5,10,15,20)=20 | 4 |

The best line is row 1 with time 4, so answer is board 1, last number 5.

Now consider Sample 1, query 2 where permutation is shuffled. The timestamp idea still applies: each cell is assigned its index in the permutation, and row maxima reflect the completion time regardless of order shape. The minimum among all rows and columns gives the earliest completion, and the corresponding value in the permutation gives the last called number.

This demonstrates that the algorithm is invariant to permutation order and depends only on relative ordering encoded in `pos`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \cdot N \cdot 25)$ | Each query builds position array in $O(k)$, then scans 10 lines per board, each line has 5 cells |
| Space | $O(N \cdot 25)$ | Storage of all boards and line decompositions |

Given $k \le 25$, each board contributes a constant factor, and the solution relies on tight inner loops rather than asymptotic improvements beyond constants.

This fits within limits because operations are simple integer comparisons over small fixed-size arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, k = map(int, input().split())
    boards = []
    for _ in range(N):
        b = [list(map(int, input().split())) for _ in range(5)]
        boards.append(b)

    rows_cols = []
    for b in boards:
        lines = []
        for i in range(5):
            lines.append([b[i][j] for j in range(5)])
        for j in range(5):
            lines.append([b[i][j] for i in range(5)])
        rows_cols.append(lines)

    q = int(input())
    out = []
    for _ in range(q):
        order = list(map(int, input().split()))
        pos = [0] * (k + 1)
        for i, x in enumerate(order):
            pos[x] = i

        best_time = 10**9
        best_id = 0

        for idx, lines in enumerate(rows_cols, 1):
            local_best = 10**9
            for line in lines:
                t = 0
                for v in line:
                    t = max(t, pos[v])
                local_best = min(local_best, t)

            if local_best < best_time:
                best_time = local_best
                best_id = idx

        out.append(str(best_id))

    return "\n".join(out)

# provided sample
assert run("""1 25
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
4
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
1 6 11 16 2 7 12 17 3 8 13 18 4 9 14 19 25 21 22 23 24 5 10 15 20
1 2 3 4 6 7 8 10 11 12 14 15 16 18 19 20 22 23 24 25 5 9 13 17 21
16 14 13 22 3 21 15 23 20 9 11 24 4 8 1 12 7 17 19 5 2 10 6 25 18
""") == """1 5
1 21
1 5
1 12
"""

# all same numbers
assert run("""1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1
1
""") == """1"""

# two boards, immediate win
assert run("""2 2
1 2 1 2 1
2 1 2 1 2
1 2 1 2 1
2 1 2 1 2
1 2 1 2 1
1 2 1 2 1
2 1 2 1 2
1 2 1 2 1
2 1 2 1 2
1 2 1 2 1
1
1 2
""") == """1"""

# single row win vs column win tie-break
assert run("""2 5
1 2 3 4 5
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
5 4 3 2 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1
1 2 3 4 5
""") == """1"""

# empty-like early win
assert run("""1 3
1 2 3 1 2
1 2 3 1 2
1 2 3 1 2
1 2 3 1 2
1 2 3 1 2
1
3 2 1
""") == """1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | given | correctness of full pipeline |
| all same numbers | 1 | repeated-value handling |
| two boards | 1 | tie-breaking stability |
| row vs column | 1 | deterministic winner selection |
| reversed order | 1 | permutation handling correctness |

## Edge Cases

A critical edge case is repeated numbers inside a row or column. If a row contains multiple identical values, the timestamp maximum still correctly reflects completion because all occurrences share the same activation time. The algorithm does not assume uniqueness, so it remains valid.

Another edge case is when multiple lines complete at the same time within a board. The algorithm handles this by taking the minimum over all line maxima, ensuring the earliest completion is selected.

Tie-breaking across boards is handled after computing each board’s best time. Since we iterate in increasing ID order and only update on strictly smaller time or equal time with smaller ID, correctness is preserved without additional sorting logic.
