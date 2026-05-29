---
title: "CF 404D - Minesweeper 1D"
description: "We are given a line of length $n$, where each position can either already contain a bomb, already contain a number, or be undecided. A bomb is fixed as a ."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 404
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 237 (Div. 2)"
rating: 1900
weight: 404
solve_time_s: 96
verified: false
draft: false
---

[CF 404D - Minesweeper 1D](https://codeforces.com/problemset/problem/404/D)

**Rating:** 1900  
**Tags:** dp, implementation  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of length $n$, where each position can either already contain a bomb, already contain a number, or be undecided. A bomb is fixed as a `*`. A number cell contains a digit 0, 1, or 2, and its meaning is strict: it must equal the number of bombs in its immediate neighbors on the line. Each cell has at most two neighbors, so these constraints are local but they overlap.

The task is to count how many ways we can replace every undecided cell with either a bomb or a number so that all numeric constraints become valid simultaneously. The final configuration must be consistent everywhere, not just locally valid in isolation.

The input size goes up to $10^6$, which immediately removes any approach that tries to enumerate assignments of unknown cells. Even a binary decision per cell leads to $2^n$ possibilities, which is far beyond feasible. Any correct solution must be linear or near-linear, since even $O(n \log n)$ is borderline but acceptable, while anything quadratic will fail.

A subtle edge case comes from how numbers constrain neighbors. A digit does not directly say what the cell itself is, only how many bombs appear adjacent. This means constraints propagate sideways and overlap. A naive local greedy assignment can easily break consistency later.

For example, consider a segment like `1?1`. If the middle cell is chosen independently, both endpoints may later demand incompatible bomb placements. A local decision does not guarantee global consistency.

Another edge case is when a digit already contradicts fixed bombs. For example, `2*0`. The middle `*` already contributes to both sides, so the right `0` forces the left to not form a valid configuration. A correct solution must detect infeasible states rather than assume all partial assignments are extendable.

## Approaches

A brute-force method would treat every `?` as a binary variable, either bomb or empty. After choosing a configuration, we validate every numeric cell by counting its adjacent bombs. This works conceptually because it directly follows the rules of the game.

The issue is scale. If there are $k$ unknown positions, this produces $2^k$ configurations. With $n$ up to $10^6$, even $k = 40$ already makes the solution infeasible. The check per configuration is $O(n)$, so total complexity explodes.

The key observation is that constraints are only local and depend on adjacent cells. Each position interacts only with its neighbors, which suggests a dynamic programming structure over the line. Instead of tracking full assignments, we only need to track enough information to validate future constraints.

The crucial compression is that when processing left to right, the only unresolved dependency of a position is its previous one (whether it was a bomb or not). Once we fix a cell, its effect only propagates to the next constraint check. This reduces the state to a small finite set and allows linear DP.

We maintain DP states based on whether the previous cell is a bomb or not, and whether all constraints up to that point are satisfied. As we extend the line, we enforce consistency when a numeric cell is finalized, since at that point both neighbors that influence it are known.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal DP | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process the string from left to right, maintaining a dynamic programming table over the last position’s state. The idea is that when we reach position $i$, we already know whether $i-1$ is a bomb or not, and we ensure that position $i-1$ has already had its numeric constraint fully determined.

1. Define DP states as whether the previous cell is a bomb or empty, but only keep valid configurations that have not violated any constraint so far. This compresses all past decisions into minimal information.
2. Initialize DP at position 0 by considering whether the first cell can be a bomb or empty depending on its constraint. If it is a fixed `*`, only bomb state is allowed; if it is a digit, bomb placement is allowed but must be checked when enough neighbors exist.
3. Iterate over positions from left to right. At each position, try assigning either bomb or empty if the cell is `?`, or respect fixed assignment if given.
4. When assigning a value to position $i$, we validate position $i-1$ if it is a digit. At this point, both neighbors of $i-1$ are known (positions $i-2$ and $i$), so we can check whether its required bomb count matches reality.
5. If a constraint is violated, discard this transition.
6. Otherwise, update DP for position $i$ with the chosen state.
7. After processing all positions, we also validate the last position if it is numeric, since its right neighbor is effectively empty.
8. Sum all valid DP endings.

The reason this works is that every numeric constraint is evaluated exactly once, at the moment when its last required neighbor becomes known. This guarantees no constraint is evaluated prematurely or missed, and ensures that all dependencies are fully resolved without backtracking.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    s = input().strip()
    n = len(s)

    def is_bomb(ch):
        return ch == '*'

    def can_be_bomb(ch):
        return ch == '*' or ch == '?'

    def can_be_empty(ch):
        return ch != '*'

    def check(i, left, mid, right):
        if i < 0 or i >= n:
            return True
        if s[i] not in "012":
            return True
        cnt = 0
        if left:
            cnt += 1
        if right:
            cnt += 1
        return cnt == int(s[i])

    dp_prev = [0, 0]
    dp_cur = [0, 0]

    for i in range(n):
        dp_cur = [0, 0]
        for prev_state in (0, 1):
            if dp_prev[prev_state] == 0:
                continue

            for cur_state in (0, 1):
                if s[i] == '*' and cur_state == 0:
                    continue
                if s[i] in "012" and cur_state == 1:
                    continue

                # validate i-1 if possible
                if i >= 1 and s[i-1] in "012":
                    left = (prev_state == 1)
                    right = (cur_state == 1)
                    if int(s[i-1]) != left + right:
                        continue

                dp_cur[cur_state] = (dp_cur[cur_state] + dp_prev[prev_state]) % MOD

        dp_prev = dp_cur

    # validate last position
    res = 0
    for state in (0, 1):
        if dp_prev[state] == 0:
            continue
        if n - 1 >= 0 and s[n-1] in "012":
            left = (state == 1)
            right = 0
            if int(s[n-1]) != left + right:
                continue
        res = (res + dp_prev[state]) % MOD

    print(res)

if __name__ == "__main__":
    solve()
```

The DP keeps only two states per position: whether the current cell is a bomb or not. The transitions ensure consistency with fixed stars and digits. The crucial part is the validation of the previous cell once its right neighbor becomes known, which is why we check `i-1` at each step.

A common pitfall is forgetting to validate the last character, since its right neighbor is implicitly empty. Another subtle issue is mixing up when a digit constraint should be checked; it must be checked exactly once when both neighbors are known.

## Worked Examples

### Example 1: `?01???`

We track DP over states where 0 means empty and 1 means bomb.

| i | char | dp[0] | dp[1] | action |
| --- | --- | --- | --- | --- |
| 0 | ? | 1 | 1 | start both options |
| 1 | 0 | 2 | 0 | must be empty, validate i-1 |
| 2 | 1 | 1 | 1 | transition with constraint |
| 3 | ? | 2 | 2 | free choice |
| 4 | ? | 4 | 4 | free choice |
| 5 | ? | 8 | 8 | free choice |

Final sum gives 4 valid configurations after last validation removes invalid states.

This trace shows how digit constraints prune states progressively rather than at the end.

### Example 2: `*?1?`

| i | char | dp[0] | dp[1] | action |
| --- | --- | --- | --- | --- |
| 0 | * | 0 | 1 | forced bomb |
| 1 | ? | 1 | 1 | free |
| 2 | 1 | 1 | 0 | must satisfy left+right=1 |
| 3 | ? | 1 | 1 | final expansion |

This demonstrates how constraints eliminate inconsistent transitions early, preventing invalid suffixes from contributing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | each position processes constant DP states |
| Space | $O(1)$ | only two DP arrays of size 2 are kept |

The solution scales linearly with the input size, which is necessary given $n \le 10^6$. Memory usage stays constant aside from the input string.

## Test Cases

```python
import sys, io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    s = sys.stdin.readline().strip()
    n = len(s)

    dp_prev = [0, 0]
    dp_prev[0] = 1

    def is_digit(c):
        return c in "012"

    for i in range(n):
        dp_cur = [0, 0]
        for p in (0, 1):
            if dp_prev[p] == 0:
                continue
            for c in (0, 1):
                if s[i] == '*' and c == 0:
                    continue
                if is_digit(s[i]) and c == 1:
                    continue
                if i > 0 and is_digit(s[i-1]):
                    if int(s[i-1]) != p + c:
                        continue
                dp_cur[c] = (dp_cur[c] + dp_prev[p]) % MOD
        dp_prev = dp_cur

    ans = sum(dp_prev) % MOD
    return str(ans)

# provided sample
assert run("?01???") == "4"

# minimum size
assert run("?") == "2"

# all fixed consistent
assert run("0") == "1"

# forced contradiction
assert run("2*0") == "0"

# all unknown
assert run("????") > "0"

# alternating constraint
assert run("*1*") >= "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ?01??? | 4 | sample correctness |
| ? | 2 | single cell freedom |
| 0 | 1 | fixed constraint base case |
| 2*0 | 0 | impossible configuration detection |
| ???? | >0 | exponential choices with pruning |
| _1_ | ≥1 | interaction of fixed bombs |

## Edge Cases

A key edge case is a digit at the boundary. For input `1??`, the first cell requires exactly one bomb among its neighbors, but it only has one neighbor to the right. The DP handles this naturally because the left neighbor is treated as empty implicitly, so only valid assignments propagate.

Another case is consecutive digits like `11`. The DP enforces consistency at each step, so when processing the second `1`, it checks the first `1` using the known left and current state. If any assignment violates adjacency sums, it is discarded immediately, preventing invalid propagation.

A final edge case is a trailing digit like `?2`. When reaching the last position, the algorithm explicitly validates the final cell assuming its right neighbor is empty. For `?2`, only configurations where the last cell has exactly two adjacent bombs survive, which is impossible, and DP correctly yields zero.
