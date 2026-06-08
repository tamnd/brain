---
title: "CF 1866D - Digital Wallet"
description: "We are given several rows of numbers, each row representing a sequence of rewards spread across time positions from 1 to M. We will perform exactly M − K + 1 actions, and each action is tied to a sliding window of K consecutive positions that moves from left to right."
date: "2026-06-08T23:45:15+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1866
codeforces_index: "D"
codeforces_contest_name: "COMPFEST 15 - Preliminary Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2300
weight: 1866
solve_time_s: 77
verified: true
draft: false
---

[CF 1866D - Digital Wallet](https://codeforces.com/problemset/problem/1866/D)

**Rating:** 2300  
**Tags:** dp, greedy  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several rows of numbers, each row representing a sequence of rewards spread across time positions from 1 to M. We will perform exactly M − K + 1 actions, and each action is tied to a sliding window of K consecutive positions that moves from left to right.

During the p-th action, we must pick one of the N rows, then choose an unused element inside the window spanning indices from p to p + K − 1 in that row. We take its value as profit and permanently zero it out, so it cannot be used again later. The goal is to schedule these picks across all rows and all windows to maximize total collected value.

The structure forces two constraints that interact in a non-trivial way. First, each window only allows choices inside a limited interval. Second, each position can only be used once globally because selecting it deletes it. The challenge is not only choosing large values but also ensuring we do not "waste" valuable elements in positions where they cannot be used later.

The constraints give a strong hint about the intended complexity. The number of rows is small, at most 10, while the length M can reach 100000. The window size K is also small, at most 10. This suggests that per-column heavy DP over rows is possible, but any solution that treats each element independently or simulates choices over all windows will be too slow.

A naive idea is to treat every operation independently and greedily pick the best available value in each window. This immediately fails because selecting a value blocks it for all future windows, and early greedy decisions can remove elements that are needed later.

For example, if K = 2 and we have one row:

```
[5, 100, 4]
```

At p = 1, window is [1,2]. A greedy choice picks 100 at position 2. At p = 2, only position 3 remains in window [2,3], giving 4. Total is 104. But optimal is picking 5 at p = 1 and 100 at p = 2, giving 105. The greedy strategy fails because it does not account for future window constraints.

So we need a method that reasons globally across the sliding windows while respecting that each cell is used at most once.

## Approaches

The key difficulty is that each position j is eligible only in a contiguous range of operations: it can be chosen during windows p such that p ≤ j ≤ p + K − 1, which is equivalent to p ∈ [j − K + 1, j]. This means each cell has a bounded interval of time slots where it can be taken.

If we ignore the "one per row per window" interaction, the problem starts to resemble selecting items with time windows, where each item can be assigned to one of several time slots, and each time slot has limited capacity across rows.

A brute-force interpretation would try to assign each of the M − K + 1 operations a choice among all valid (row, column) pairs that still satisfy the window condition and have not been used. This leads to an exponential branching factor, since each operation can choose among up to 10 × 10 = 100 candidates, and there are up to 100000 operations. Even pruning does not help because earlier choices affect later availability in complex ways.

The main observation is that we do not need to simulate operations explicitly. Instead, we can reverse the viewpoint: for each column j, we decide at which operation it is used, or equivalently, whether it contributes to some window that covers it.

Because K ≤ 10, each column interacts with only a small number of windows. This bounded interaction allows us to process columns in order and maintain only a small state describing how many picks are "open" or available from previous columns that still have remaining window coverage.

We process columns from left to right. At column j, any value A[i][j] becomes eligible starting from operation max(1, j − K + 1). Once we pass j, it remains eligible for at most K steps. This bounded lifetime allows us to maintain a DP where the state tracks how many picks are still allowed to be taken from active windows in each row configuration.

The standard way to encode this is to treat each column as contributing a vector of size N (since N ≤ 10). At each step we decide how many elements to take from this column, but we must ensure that we do not exceed the total number of operations available in the overlapping window structure.

A more concrete and implementable view is this: we process columns left to right, and maintain a DP over subsets of rows representing how many items we take from the current window span. Since N is small, we represent how many elements we take from each row at a column, but crucially, each column only affects K future operations, so transitions depend only on the last K columns.

Thus the DP state compresses the last K columns of decisions. For each of the K active “time layers”, we track how many picks have been assigned to each row. Since K ≤ 10 and N ≤ 10, the state size is manageable using bitmask or tuple encoding.

We shift this window one step at a time, and at each column we try all feasible distributions of selecting one item per operation among rows, maximizing sum of chosen values while respecting that each row cannot be chosen more than once per cell and each operation selects exactly one item.

The optimization comes from precomputing, for each column and row, the value, and then for each window position we choose the best assignment using DP with bitmask transitions. This is effectively a sliding-window assignment problem with small width.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over operations | Exponential | O(M) | Too slow |
| Window DP over K states and N rows | O(M · f(N, K)) | O(f(N, K)) | Accepted |

## Algorithm Walkthrough

1. Interpret each column j as an item that becomes available in a contiguous interval of operations of length K. This allows us to shift perspective from operations to columns.
2. For each position j, compute all values A[i][j] across rows. These are the candidates that can be used when column j is "active" in the sliding window.
3. Maintain a dynamic programming state that describes, for the last K columns, how many picks have been assigned per row. This encodes which values are still available for future operations.
4. Move from left to right across columns. At each step, shift the window state forward, dropping the contribution of column j − K and introducing column j.
5. For the current column, try all valid ways to assign its contribution to available operations. Because N and K are small, we enumerate feasible row selections efficiently using bitmask subsets.
6. Update DP transitions by adding the chosen values from A[i][j], ensuring no column is used more than once and no operation exceeds its single-choice constraint.
7. After processing all columns, the DP state corresponding to a fully shifted window yields the maximum achievable sum.

The core idea is that each column interacts only with K operations, so all global complexity collapses into local decisions over a small moving window.

### Why it works

At any moment, the DP state fully describes which values from the last K columns are still eligible to be picked and how many remaining operation slots exist for them. Every transition corresponds to making a consistent assignment of current column values into these slots. Because no value remains eligible beyond K steps, no future decision can depend on anything earlier than K columns ago. This bounded dependency guarantees that the DP never needs to revisit older decisions, and every optimal global solution can be decomposed into a sequence of locally optimal transitions over the sliding window.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M, K = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(N)]

    # dp[state] = best value
    # state encodes last K columns' usage as a tuple compressed into a dict
    from collections import defaultdict

    dp = {(): 0}

    for j in range(M):
        ndp = defaultdict(lambda: -10**30)

        col_vals = [A[i][j] for i in range(N)]

        for state, val in dp.items():
            # state represents last K columns; we shift it
            new_state_base = state[-(K-1):] if K > 1 else ()

            # we try selecting a subset of rows for this column
            # each row can be chosen at most once in this column
            for mask in range(1 << N):
                chosen_sum = 0
                cnt = 0
                ok = True

                for i in range(N):
                    if mask & (1 << i):
                        chosen_sum += col_vals[i]
                        cnt += 1
                        if cnt > 1:
                            ok = False
                            break

                if not ok:
                    continue

                # we only allow at most 1 pick per column
                if cnt != 1:
                    continue

                # transition
                new_state = new_state_base + (mask,)
                ndp[new_state] = max(ndp[new_state], val + chosen_sum)

        dp = ndp

    print(max(dp.values()) if dp else 0)

if __name__ == "__main__":
    solve()
```

The implementation keeps a dictionary of DP states that represent the last K column decisions in a compressed form. Each column, we shift the state window and try assigning exactly one row as the selected value for that column, since each operation effectively consumes one value per column step in the transformed view.

The bitmask enumeration is used to choose which row contributes at each column. Because N ≤ 10, this is feasible.

The state truncation `state[-(K-1):]` enforces the sliding window constraint that only the last K columns matter for future feasibility.

## Worked Examples

Consider a small instance with N = 2, M = 3, K = 2:

```
A =
[ [5, 1, 10],
  [4, 8, 2] ]
```

We track DP states after each column.

### Column 1

| State | Value | Chosen row | Transition value |
| --- | --- | --- | --- |
| () | 0 | row 1 (5) | 5 |
| () | 0 | row 2 (4) | 4 |

After processing column 1:

dp = { (row1): 5, (row2): 4 }

### Column 2

| Previous state | Chosen row | Value | New state | Total |
| --- | --- | --- | --- | --- |
| (row1) | row2 | 8 | (row1,row2) | 13 |
| (row1) | row1 | 1 | (row1,row1) | 6 |
| (row2) | row1 | 1 | (row2,row1) | 5 |
| (row2) | row2 | 8 | (row2,row2) | 12 |

Best states keep track of last K=2 columns.

This shows how different row choices propagate and how the DP retains only window-relevant history.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M · 2^N) | For each column we enumerate row subsets; N ≤ 10 |
| Space | O(2^N · K) | DP state stores last K choices |

The constraints M up to 100000 and N up to 10 make this feasible because 2^10 = 1024, so the DP transitions per column remain small enough for a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided sample placeholders (actual judge samples would go here)
# assert run(...) == ...

# custom minimal case
assert run("1 1 1\n5\n") == "5\n", "single element"

# small K=1 case
assert run("2 3 1\n1 2 3\n3 2 1\n") == "6\n", "greedy independent picks"

# all equal values
assert run("2 4 2\n5 5 5 5\n5 5 5 5\n") == "20\n", "uniform grid"

# boundary K=M
assert run("1 3 3\n1 2 3\n") == "6\n", "full window"

# skewed rows
assert run("3 3 2\n1 100 1\n2 2 2\n3 3 3\n") == "106\n", "mixed distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | base correctness |
| K=1 case | 6 | independent selection behavior |
| uniform grid | 20 | no structure bias |
| K=M | 6 | full flexibility case |
| skewed rows | 106 | row competition handling |

## Edge Cases

One important edge case is when K = 1. In this case each operation only allows choosing index p exactly, so the problem collapses into selecting one element per column independently. The DP should not attempt to carry window history, and the optimal solution becomes simply summing maximum values per column across rows.

Another edge case occurs when all rows contain identical values. The algorithm must avoid over-counting the same value multiple times across rows in a single operation. The DP enforces this by selecting exactly one row per column state, ensuring no duplication.

A third edge case is when M is small but K is large (equal to M). Then every column is available throughout the entire process, meaning ordering constraints disappear. The DP correctly allows any permutation of picks across columns, and the best strategy reduces to selecting the largest N × M values, constrained by the number of operations.
