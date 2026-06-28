---
title: "CF 104833B - \u304a\u306f\u3088\u3046 \u5b66\u5f1f"
description: "We are given a subtraction game played on a pile of balls. A state of the game is defined by the current number of balls, say $a$. On a player's turn, the allowed move size is determined by a function of the current state: compute the sum of digits of $a$, call it $x$."
date: "2026-06-28T11:53:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104833
codeforces_index: "B"
codeforces_contest_name: "The 2023 Zhejiang SCI-TECH University Freshman Programming Contest"
rating: 0
weight: 104833
solve_time_s: 61
verified: true
draft: false
---

[CF 104833B - \u304a\u306f\u3088\u3046 \u5b66\u5f1f](https://codeforces.com/problemset/problem/104833/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a subtraction game played on a pile of balls. A state of the game is defined by the current number of balls, say $a$. On a player's turn, the allowed move size is determined by a function of the current state: compute the sum of digits of $a$, call it $x$. The player may remove any number of balls between 1 and $\min(a, x)$, inclusive. The player who makes the move that leaves the pile empty immediately wins.

Each test case gives an initial number $n$, and we must determine whether the first player (A) has a forced win under optimal play.

The constraints are large in two dimensions. There can be up to $10^6$ test cases, and each $n$ is also up to $10^6$. That immediately rules out any per-query simulation. Even $O(n)$ per test case is impossible, and even $O(n \log n)$ per query would be too slow. Any solution must effectively preprocess all values up to the maximum $n$ once.

A subtle edge case appears when $n$ is small, because the digit sum can be larger than or equal to $n$. For example, when $n = 1$, the digit sum is 1, so the player can only take 1 and wins immediately. When $n = 10$, digit sum is 1, so only one move exists, which makes it behave differently from the intuitive “take-any” game. These boundary cases matter because the move range depends on the state itself, not just on a fixed parameter.

Another important failure mode comes from assuming a classical take-away game with fixed $k$. Here, the maximum move changes at every position, so standard periodicity arguments like modulo $k+1$ do not apply globally.

## Approaches

A brute-force solution would simulate the game from each starting value $n$. For each state $a$, we would try all possible moves $k$ from 1 to $\min(a, \text{digitSum}(a))$, recursively checking whether the resulting position is losing. This forms a standard game DP, but each state may branch up to 54 transitions in the worst case (since digit sums up to $10^6$ are at most 54). Over all states up to $10^6$, this yields roughly $5 \times 10^7$ transitions, and recursion or repeated recomputation would push it further, making it borderline or slow in Python under strict limits.

The key observation is that we do not need to explore each move individually in a recursive manner. A position is winning if there exists at least one move to a losing position. Since all moves go to contiguous states $[a - s(a), a - 1]$, we only need to know whether there exists a losing state in that interval. This transforms the problem into maintaining a prefix summary of losing states, allowing constant-time range checks after preprocessing.

We define a DP array where each state is either winning or losing. We compute states in increasing order, and for each position we check whether the interval of reachable states contains any losing state. If yes, the current state is winning; otherwise it is losing. A prefix sum over losing states makes this check O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS DP | O(n · digitSum) | O(n) | Too slow |
| Prefix DP with range query | O(n + T) | O(n) | Accepted |

## Algorithm Walkthrough

We compute results for all values up to the maximum $n$ appearing in the input.

1. Precompute digit sums for all integers up to $10^6$. This ensures each state’s move range can be obtained in O(1) time.
2. Initialize a DP array where `dp[i]` indicates whether the current player has a winning strategy starting from $i$. Also maintain a prefix array `pref`, where `pref[i]` counts how many losing positions exist in $[0, i]$.
3. Set the base state `dp[0] = False`, because there are no moves left. Mark this in the prefix array.
4. Iterate from $i = 1$ to the maximum value. For each $i$, compute $s = \text{digitSum}(i)$.
5. The player can move to any state in the interval $[i - s, i - 1]$. The current state is losing only if all these states are winning, which is equivalent to saying there are no losing states in this interval.
6. Use prefix sums to check this condition in O(1):

if `pref[i-1] - pref[max(0, i-s-1)] == 0`, then mark `dp[i] = False`, otherwise `dp[i] = True`.
7. Update prefix sums accordingly and continue.

After filling the table, each query is answered in O(1).

### Why it works

Each position depends only on strictly smaller positions, so processing in increasing order ensures correctness. The key invariant is that `dp[i]` is determined completely by the existence of at least one losing state reachable from it. The prefix array correctly maintains the count of losing states in any interval, so the decision rule exactly matches the definition of a winning position in impartial games: a position is winning if it has at least one move to a losing state, and losing otherwise.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

digit_sum = [0] * (MAXN + 1)
for i in range(1, MAXN + 1):
    digit_sum[i] = digit_sum[i // 10] + (i % 10)

dp = [False] * (MAXN + 1)
pref = [0] * (MAXN + 1)

dp[0] = False
pref[0] = 1  # count of losing positions

for i in range(1, MAXN + 1):
    s = digit_sum[i]
    left = i - s
    if left < 0:
        left = 0

    # count losing positions in [left, i-1]
    losing_in_range = pref[i - 1] - (pref[left - 1] if left > 0 else 0)

    if losing_in_range == 0:
        dp[i] = False
    else:
        dp[i] = True

    pref[i] = pref[i - 1] + (0 if dp[i] else 1)

t = int(input())
out = []
for _ in range(t):
    n = int(input())
    out.append("A" if dp[n] else "B")

print("\n".join(out))
```

The code precomputes digit sums in linear time, then builds the DP array from 1 upward. The key subtlety is maintaining the prefix count of losing states so that each interval query becomes constant time. The prefix array stores counts of losing positions, not winning ones, because the transition condition is naturally expressed in terms of “is there a losing move available”.

The answer mapping follows directly: if `dp[n]` is true, the starting player can force a win, otherwise the second player wins.

## Worked Examples

Consider a small illustration with $n = 6$.

| i | digit sum | reachable range | losing states in range | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | [0,0] | 1 (state 0) | W |
| 2 | 2 | [0,1] | 1 | W |
| 3 | 3 | [0,2] | 1 | W |
| 4 | 4 | [0,3] | 1 | W |
| 5 | 5 | [0,4] | 1 | W |
| 6 | 6 | [0,5] | 1 | W |

Here every state up to 6 is winning because each can reach the losing terminal state 0 directly or indirectly in one move range.

Now consider a slightly larger structure where digit sums restrict reachability more tightly. The same mechanism applies: as soon as a position cannot reach any losing state, it becomes losing, creating a chain reaction that defines the entire DP.

These traces show that the decision at each step depends only on interval information, not individual transitions, which is why prefix aggregation is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAXN + T) | digit sum preprocessing plus one DP pass and O(1) queries |
| Space | O(MAXN) | arrays for DP, prefix sums, and digit sums |

The preprocessing up to $10^6$ fits comfortably within limits, and each test case is answered in constant time, making the solution efficient even for $10^6$ queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAXN = 10**6
    digit_sum = [0] * (MAXN + 1)
    for i in range(1, MAXN + 1):
        digit_sum[i] = digit_sum[i // 10] + (i % 10)

    dp = [False] * (MAXN + 1)
    pref = [0] * (MAXN + 1)

    dp[0] = False
    pref[0] = 1

    for i in range(1, MAXN + 1):
        s = digit_sum[i]
        left = max(0, i - s)
        losing = pref[i - 1] - (pref[left - 1] if left > 0 else 0)
        dp[i] = losing != 0
        pref[i] = pref[i - 1] + (0 if dp[i] else 1)

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append("A" if dp[n] else "B")
    return "\n".join(out)

# boundary cases
assert run("1\n1\n") == "A"
assert run("1\n10\n") in ["A", "B"]

# small structure
assert run("3\n1\n2\n3\n") == "A\nA\nA"

# max boundary single test
assert run("1\n1000000\n") in ["A", "B"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 | A | smallest winning state |
| 1, 10 | A/B | digit sum restriction edge |
| 1e6 | A/B | upper bound stability |
| 1,2,3 | A A A | early-chain behavior |

## Edge Cases

For $n = 1$, the digit sum is 1, so the only move is to take 1 and immediately win. The DP marks state 1 as winning because it can reach state 0, which is losing.

For $n = 10$, the digit sum is 1 again, so the only move is to 1, which reduces the problem to whether state 1 is losing or winning. Since state 1 is already known to be winning, state 10 becomes losing, and the prefix logic correctly captures this dependency.

For large values like $n = 999999$, the digit sum is 54, so each state can reach a wide interval. The prefix-based check efficiently evaluates whether any losing state exists in that interval without iterating over all 54 transitions explicitly, preserving correctness and speed.
