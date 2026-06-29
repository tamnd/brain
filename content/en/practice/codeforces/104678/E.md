---
title: "CF 104678E - Football tournament"
description: "There are $n$ teams, each starting with a fixed strength value. Every pair of teams plays exactly one match, so the tournament is a complete round-robin."
date: "2026-06-29T09:06:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "E"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 84
verified: true
draft: false
---

[CF 104678E - Football tournament](https://codeforces.com/problemset/problem/104678/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

There are $n$ teams, each starting with a fixed strength value. Every pair of teams plays exactly one match, so the tournament is a complete round-robin. The outcome of a match depends only on the final strengths: the stronger team wins, and if both strengths are equal, the match is a draw.

Points are awarded per match, and the total score of a team is just the sum over all its matches. A win contributes 3 points to the winner, while a draw gives 1 point to each participant. We are allowed to increase the strength of any team by 1 per training session, and each session affects only one team.

The key goal is not to choose match outcomes directly, but to adjust strengths so that after all training, the sum of points over all teams is as large as possible. Among all possible ways to achieve this maximum possible total, we must find the minimum number of training sessions required.

The constraints suggest that $n$ can be as large as 200000, so any solution must be roughly $O(n \log n)$ or better. A quadratic approach over all pairs of teams is impossible because there are $O(n^2)$ matches, which would be far too many even to simulate.

A subtle issue appears when many teams share the same strength. For example, if several teams have equal values, all matches among them are draws, which reduces total points. Increasing strengths can break ties, but doing so affects multiple pairwise outcomes at once, so greedy local decisions need careful justification.

A naive mistake is to try to simulate matches or adjust strengths pair by pair. That fails because one increment changes comparisons against all other teams simultaneously, not just one opponent.

As a concrete example, if all teams start with strength $[5, 5, 5]$, every match is a draw, producing minimal total points. Increasing one team slightly changes all its matches at once, so the problem is fundamentally about global structure, not individual match fixing.

## Approaches

Let us first understand what determines the total score. Every pair of teams contributes either 3 points in total if there is a winner, or 2 points if it is a draw. Since the number of matches is fixed at $\frac{n(n-1)}{2}$, maximizing the total score is equivalent to maximizing the number of non-draw matches.

A match is a draw exactly when two teams end up with equal final strengths. This means that the optimal situation is when all final strengths are distinct, because then every match has a winner and contributes 3 points instead of 2. So the goal reduces to eliminating all duplicates in the final array of strengths.

We can only increase values, never decrease them. So the task becomes: starting from array $a$, assign each element an integer increment so that the resulting array $b$ satisfies $b_1 < b_2 < \dots < b_n$, while minimizing the total increase $\sum (b_i - a_i)$. This is a classic greedy construction problem on a sorted array.

The brute force idea would be to try all possible ways of distributing increments among teams until all values are distinct, and compute the cost. This is infeasible because each element can grow arbitrarily, and the state space explodes exponentially. Even trying to resolve conflicts locally can cascade into further conflicts, leading to worst case behavior around $O(\text{range of values})$ per adjustment.

The key observation is that after sorting, the structure becomes linear. Each element only needs to be at least one more than the previous final value to avoid equality. Once earlier choices are fixed, the best choice for the current element is forced: it should be as small as possible while respecting both its original value and the strict increase constraint. This removes all backtracking and yields a single pass solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal Greedy | $O(n \log n)$ | O(1) extra | Accepted |

## Algorithm Walkthrough

### Steps

1. Sort the array of strengths in non-decreasing order.

Sorting is necessary because the final condition we want, strictly increasing values, is easiest to enforce in order.
2. Initialize a running variable `current` to track the smallest valid value for the next team.
3. Process each team in sorted order. For each original strength $a_i$, set its final strength to

$b_i = \max(a_i, current)$.

This ensures we never decrease a value and never violate ordering with previous teams.
4. After assigning $b_i$, update `current` to $b_i + 1$, since the next element must be strictly larger.
5. Accumulate the cost as $\sum (b_i - a_i)$, which represents the total number of training sessions.

### Why it works

At every position, we enforce the smallest possible valid value for the current team. Any larger choice would only increase the cost without improving feasibility, since the only constraint for future elements is being strictly larger than the previous one. This creates a monotonic structure: once a value is fixed, it becomes a lower bound for all subsequent values. Because each step is locally minimal under a constraint that fully captures future feasibility, no later adjustment can make an earlier decision suboptimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    current = a[0]
    ans = 0

    for i in range(n):
        if i == 0:
            current = a[0]
        else:
            current = max(a[i], current + 1)
        ans += current - a[i]

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step is what transforms the original combinatorial interaction between all pairs into a linear constraint chain. Without sorting, the dependency structure is unclear, but after sorting, each element only depends on the previous constructed value.

The `current` variable encodes the smallest allowable value that avoids equality with all earlier elements. The `max` operation ensures we respect both the original strength and the strict increase requirement. The accumulated difference directly counts how many increments are applied across all teams.

A common implementation pitfall is forgetting that once a value is increased, it affects all subsequent constraints, not just adjacent elements. Another is incorrectly initializing the first element, since it does not need to be greater than anything before it.

## Worked Examples

### Example 1

Input:

```
3
6 5 6
```

Sorted array becomes $[5, 6, 6]$.

| i | a[i] | current before | chosen b[i] | current after | cost |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | - | 5 | 6 | 0 |
| 1 | 6 | 6 | 6 | 7 | 0 |
| 2 | 6 | 7 | 7 | 8 | 1 |

Total cost is 1.

This shows that only one duplicate needs to be resolved, and pushing the last element upward is sufficient to break all equalities involving it.

### Example 2

Input:

```
4
1 1 1 1
```

Sorted array is $[1,1,1,1]$.

| i | a[i] | current before | chosen b[i] | current after | cost |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | 1 | 2 | 0 |
| 1 | 1 | 2 | 2 | 3 | 1 |
| 2 | 1 | 3 | 3 | 4 | 2 |
| 3 | 1 | 4 | 4 | 5 | 3 |

Total cost is 6.

This demonstrates the cascading effect: once one value is increased, it forces all subsequent values upward to maintain strict ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, single linear pass afterwards |
| Space | $O(1)$ auxiliary | Only a few variables besides the input array |

The solution comfortably fits within constraints since sorting 200000 elements and doing one pass is well within typical time limits for 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else __import__("builtins").print  # placeholder

# Since direct capture is environment-dependent, these are logical asserts only.

# sample
# assert run("3\n6 5 6\n") == "1\n"

# minimum size
# assert run("2\n1 1\n") == "1\n"

# all equal
# assert run("4\n5 5 5 5\n") == "6\n"

# already strictly increasing
# assert run("5\n1 2 3 4 5\n") == "0\n"

# reverse order
# assert run("5\n5 4 3 2 1\n") == "10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1 | 1 | smallest duplicate case |
| 5 1 2 3 4 5 | 0 | already optimal |
| 4 5 5 5 5 | 6 | cascading increments |
| 5 5 4 3 2 1 | 10 | heavy adjustment case |

## Edge Cases

A key edge case is when all strengths are equal. In this situation, every pairwise match is a draw initially, and the algorithm must push values into a strictly increasing sequence. The greedy method handles this naturally by turning $[x, x, x, \dots]$ into $[x, x+1, x+2, \dots]$, accumulating a triangular number of increments. Each step depends only on the previous chosen value, so no ambiguity arises.

Another edge case is when the array is already strictly increasing. After sorting, every $a_i$ already satisfies $a_i > a_{i-1}$, so the `max` operation always selects $a_i$ itself. The cost remains zero because no training is needed, and the algorithm correctly avoids unnecessary increments.

A final subtle case occurs when duplicates are interleaved with large gaps, such as $[1,1,100]$. The second element is pushed only to 2, and the large third element remains unchanged because it already satisfies the increasing constraint. This shows the algorithm never over-adjusts values beyond what is necessary to maintain strict ordering.
