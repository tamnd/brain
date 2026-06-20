---
title: "CF 106159C - Creating a Playlist"
description: "We are given a sequence of songs, each associated with a value that can be positive or negative. We want to select a subset of these songs to maximize the total sum of selected values, but there is a spacing restriction: if we choose a song at position i, then we are forbidden…"
date: "2026-06-20T22:12:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106159
codeforces_index: "C"
codeforces_contest_name: "XIII UnB Contest Mirror"
rating: 0
weight: 106159
solve_time_s: 41
verified: true
draft: false
---

[CF 106159C - Creating a Playlist](https://codeforces.com/problemset/problem/106159/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of songs, each associated with a value that can be positive or negative. We want to select a subset of these songs to maximize the total sum of selected values, but there is a spacing restriction: if we choose a song at position `i`, then we are forbidden from choosing any song in the next `K - 1` positions, meaning indices strictly between `i` and `i + K` cannot be chosen.

The task is to compute the best possible total sum under this rule, including the possibility of choosing no songs at all, which yields sum zero.

The constraints allow up to `N = 10^5` elements. A naive solution that tries all subsets or even all valid combinations would explode exponentially, and even dynamic programming that checks all previous candidates per position would risk quadratic behavior. With a 1 second limit, we should aim for roughly linear or near-linear time, certainly no worse than `O(N log N)`.

A subtle edge case appears when all values are negative. A greedy or forced-selection interpretation might incorrectly pick some song, but the optimal strategy is to pick nothing and output zero. Another edge case is when `K = 1`, which removes all restrictions and reduces the problem to simply taking all positive contributions.

## Approaches

A brute-force approach would try every subset of songs and check whether it respects the spacing rule. This is correct but infeasible, as there are `2^N` subsets, and even validating each subset would cost linear time, leading to an astronomically large runtime.

A more structured brute force improves slightly by making a decision at each index: either take song `i` and jump to `i + K`, or skip it and move to `i + 1`. This recursion correctly explores all valid solutions but still branches heavily, leading to exponential behavior in the worst case because the same suffix states are recomputed repeatedly.

The key observation is that the problem has optimal substructure over positions. If we define the best answer starting from index `i`, it depends only on future choices, and the decision at `i` is local: either include it and skip forward by `K`, or exclude it and continue at `i + 1`. This naturally leads to dynamic programming over indices.

We define `dp[i]` as the maximum sum we can obtain starting from position `i`. Then we compute transitions in reverse order so that future states are already known. This reduces the problem to a linear DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| DP over indices | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We process the array from right to left so that when we are at position `i`, we already know the best answers for positions beyond it.

1. Define a DP array `dp` of size `N + K + 5`, initialized with zeros. The extra space avoids bounds checks when jumping forward.
2. Iterate `i` from `N` down to `1`. At each position, we compute two possibilities.
3. First option is to skip the current song, which gives value `dp[i + 1]`. This represents not using song `i` at all.
4. Second option is to take song `i`, which gives value `A[i] + dp[i + K]`. This works because after selecting `i`, the next valid position is `i + K`.
5. Set `dp[i]` to the maximum of these two values.
6. After filling the table, the answer is `dp[1]`, but we also compare it with zero to allow the empty selection.

### Why it works

At every index `i`, the state `dp[i]` captures the best achievable sum using only indices `i` and beyond. Any valid solution must either include `i` or exclude it. If it excludes `i`, it is exactly `dp[i + 1]`. If it includes `i`, the restriction forces the next choice to start at `i + K`, and the best continuation from there is `dp[i + K]`. Since both choices enumerate all valid possibilities without overlap, the recurrence is complete, and taking the maximum preserves optimality inductively from the end of the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    # 1-index the array for clarity
    A = [0] + A
    
    dp = [0] * (N + K + 5)
    
    for i in range(N, 0, -1):
        take = A[i] + dp[i + K]
        skip = dp[i + 1]
        dp[i] = max(take, skip)
    
    print(max(0, dp[1]))

if __name__ == "__main__":
    solve()
```

The DP array is sized with extra padding so that `i + K` and `i + 1` are always valid accesses, avoiding conditional checks inside the loop. The transition directly encodes the two possible decisions at each index.

The final `max(0, dp[1])` is essential because the recurrence assumes we must start from position `1`, but the optimal strategy might involve selecting nothing if all contributions are negative.

## Worked Examples

### Example 1

Input:

`N = 3, K = 1, A = [1, 2, 3]`

Here `K = 1` means there is effectively no restriction between picks.

| i | A[i] | dp[i+1] | A[i] + dp[i+K] | dp[i] |
| --- | --- | --- | --- | --- |
| 3 | 3 | 0 | 3 | 3 |
| 2 | 2 | 3 | 5 | 5 |
| 1 | 1 | 5 | 6 | 6 |

The final result is `6`, confirming that all elements can be taken.

### Example 2

Input:

`N = 4, K = 4, A = [2, 3, 0, 2]`

Here choosing any index blocks all others.

| i | A[i] | dp[i+1] | A[i] + dp[i+K] | dp[i] |
| --- | --- | --- | --- | --- |
| 4 | 2 | 0 | 2 | 2 |
| 3 | 0 | 2 | 0 | 2 |
| 2 | 3 | 2 | 3 | 3 |
| 1 | 2 | 3 | 2 | 3 |

The optimal answer is `3`, corresponding to selecting the second song.

These traces show how the DP naturally balances local gain against future availability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each position is processed once with O(1) transitions |
| Space | O(N) | DP array stores values for each position plus padding |

The linear complexity easily fits within the constraints for `N ≤ 10^5`, and memory usage remains well under typical limits since we only store a single array of size proportional to the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else __import__("builtins").print  # placeholder

# Note: In actual CF usage, replace run with proper capture logic

# Sample-style checks (conceptual)
# assert run("3 1\n1 2 3\n") == "6\n"

# custom cases
# all negative
# assert run("3 2\n-1 -2 -3\n") == "0\n"

# K = N case
# assert run("4 4\n2 3 0 2\n") == "3\n"

# alternating positives
# assert run("5 2\n5 1 5 1 5\n") == "15\n"

# minimum case
# assert run("1 1\n-5\n") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 / -1 -2 -3` | `0` | all-negative handling |
| `4 4 / 2 3 0 2` | `3` | full-block constraint |
| `5 2 / 5 1 5 1 5` | `15` | optimal skipping pattern |
| `1 1 / -5` | `0` | single-element edge case |

## Edge Cases

When all values are negative, the DP will still compute the best achievable suffix sum, but every transition will propagate negative values unless we explicitly clamp the result. The final `max(0, dp[1])` ensures that even if every choice reduces the sum, we prefer an empty selection.

For input `N = 3, K = 2, A = [-1, -2, -3]`, the DP evolves as follows. At `i = 3`, `dp[3] = max(-3, 0) = 0`. At `i = 2`, taking gives `-2 + dp[4] = -2`, skipping gives `0`, so `dp[2] = 0`. At `i = 1`, taking gives `-1 + dp[3] = -1`, skipping gives `0`, so `dp[1] = 0`. The final answer is `0`, matching the empty playlist.

When `K = 1`, every index is independent. For `A = [1, 2, 3]`, each state compares taking `A[i] + dp[i+1]` against skipping `dp[i+1]`, which reduces to simply accumulating all positives, and the DP correctly sums everything since all contributions are beneficial.
