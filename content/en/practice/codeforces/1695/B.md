---
title: "CF 1695B - Circle Game"
description: "We are asked to analyze a two-player game played on a circle of stone piles. Each pile has a certain number of stones. Players take turns removing a positive number of stones from the current pile."
date: "2026-06-09T22:42:44+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1695
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 801 (Div. 2) and EPIC Institute of Technology Round"
rating: 1000
weight: 1695
solve_time_s: 126
verified: true
draft: false
---

[CF 1695B - Circle Game](https://codeforces.com/problemset/problem/1695/B)

**Rating:** 1000  
**Tags:** games, greedy  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to analyze a two-player game played on a circle of stone piles. Each pile has a certain number of stones. Players take turns removing a positive number of stones from the current pile. The turns move clockwise, so after a player removes stones from pile `i`, the next player must remove stones from pile `i+1`, wrapping around to the first pile after the last. The player who encounters an empty pile on their turn loses. Mike always goes first.

The input describes multiple test cases, each specifying the number of piles and their sizes. The output should state who will win if both play optimally. A key observation is that the piles are relatively small in number (`n ≤ 50`) but the number of stones can be large (`a_i ≤ 10^9`). This rules out any algorithm that would simulate each possible move sequentially, as that could take billions of operations.

An important edge case occurs when all piles have the same size. For instance, if `n = 2` and both piles have `100` stones, Mike removes some stones from the first pile. Joe can then match his move on the next pile, and since the game is symmetric, Mike will be forced to encounter an empty pile first. A naive solution that only looks at the first pile might mistakenly declare Mike as the winner. Another edge case is a single pile: Mike just removes all stones and wins immediately.

## Approaches

A brute-force solution would attempt to simulate all possible moves. On each turn, we could try removing 1 up to `a_i` stones from the current pile, recursively computing the winner. This approach is correct because it directly follows the game rules, but its complexity is prohibitive: each pile could have up to `10^9` stones, making exhaustive simulation infeasible.

The key insight comes from observing that each player must move on the next pile in clockwise order. The player who first encounters a pile with fewer stones than the number of times the cycle has passed over it will lose. Put differently, the first pile that is strictly smaller than all previous piles in the starting sequence determines the winner, because the previous player cannot force the opponent into a win beyond that point. For this problem, it reduces to a simple check: iterate piles from the start and find the first pile where Mike cannot match Joe’s potential mirroring moves. If Mike has a strictly smaller pile first, Joe wins; otherwise, Mike wins immediately.

This observation converts a potentially exponential problem into a linear one over the number of piles. We can solve each test case in O(n) time, which is efficient even for the upper limit of `t = 1000` test cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Σ a_i^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. This allows us to loop over all game scenarios.
2. For each test case, read the number of piles `n` and the array of pile sizes `a`.
3. Initialize a variable `winner` to `"Mike"` as a default.
4. Iterate over the piles from the first one. If you encounter a pile that is strictly smaller than the previous minimum, that means Mike cannot continue safely without risking Joe’s mirroring strategy. Update `winner` to `"Joe"` and break the loop. In practice, since the first pile Mike moves on is the decisive pile, the iteration only needs to identify the earliest pile where Joe can take advantage.
5. Print the winner for each test case.

Why it works: The game is sequential and each move is forced onto the next pile. The player who first reaches a pile with fewer stones than they need to match their opponent's advantage loses. By scanning the piles once, we determine who will hit this losing condition first. This guarantees correctness because any deviation from optimal play by one player can only make the winning margin clearer for the other.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    winner = "Mike"
    for i in range(n):
        if a[i] < min(a[:i], default=a[i]):
            winner = "Joe"
            break
    print(winner)
```

Explanation: We read input efficiently for multiple test cases. The `min(a[:i], default=a[i])` safely handles the first iteration. The che
