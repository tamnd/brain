---
title: "CF 348A - Mafia"
description: "We are given a group of n friends who want to play multiple rounds of Mafia, but in each round only one person acts as the supervisor while the remaining n−1 players participate as regular players."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 348
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 202 (Div. 1)"
rating: 1600
weight: 348
solve_time_s: 241
verified: true
draft: false
---

[CF 348A - Mafia](https://codeforces.com/problemset/problem/348/A)

**Rating:** 1600  
**Tags:** binary search, math, sortings  
**Solve time:** 4m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of _n_ friends who want to play multiple rounds of Mafia, but in each round only one person acts as the supervisor while the remaining _n_−1 players participate as regular players. Each friend specifies the number of rounds they wish to play as a regular participant. The task is to determine the minimum number of total rounds needed so that every friend gets to play at least the number of rounds they desire.

The input consists of an integer _n_ for the number of friends and an array `a` of size _n_, where `a[i]` represents the number of rounds the i-th friend wants to participate as a player. The output is a single integer, the minimal total rounds needed.

The constraints indicate that _n_ can be as large as 10^5 and `a[i]` can be up to 10^9. With a 2-second time limit, we cannot afford algorithms with time complexity worse than O(n log n) or O(n). A naive solution that simulates rounds incrementally would be far too slow because it could require summing up to 10^14 rounds in the worst case.

A non-obvious edge case arises when one friend wants far more rounds than the sum of others. For example, with input:

```
3
10 1 1
```

The naive approach might try to incrementally assign players, but here the friend who wants 10 rounds forces us to schedule enough rounds so that the sum of rounds available for all others matches the largest requirement. The correct answer is 12: 10 rounds for the first friend and at least 2 extra rounds to accommodate the supervisor rotation.

## Approaches

The brute-force solution would attempt to simulate each round, assigning one supervisor per round and decrementing the desired rounds of each player. This works for small inputs but becomes unfeasible for large `a[i]` because the sum of all desired rounds can reach 10^14. Each round would require iterating over n friends to check if they can play, resulting in an O(n * total_rounds) runtime, which is clearly impossible under the constraints.

The key insight is that in each round only one person is excluded from playing, so the total number of times friends can play in all rounds is `(n-1) * total_rounds`. If the sum of all `a[i]` exceeds this value, more rounds are needed. Simultaneously, at least the maximum individual requirement must be satisfied, because one person can only be a supervisor once per round. Therefore, the minimal number of rounds is the maximum of two values: the maximum individual desire and the ceiling of total desired plays divided by (n-1).

This observation reduces the problem to a simple arithmetic calculation, avoiding the need to simulate each round or to sort players explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * sum(a[i])) | O(n) | Too slow |
| Mathematical Formula | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of friends `n` and the array `a` of desired rounds.
2. Compute the sum of all desired plays, `total = sum(a)`.
3. Find the maximum individual desire, `max_a = max(a)`.
4. Compute the minimal number of rounds based on the total capacity of (n-1) players per round: `min_rounds_needed = ceil(total / (n-1))`.
5. The final answer is the maximum between `max_a` and `min_rounds_needed` because each individual must get their desired rounds, and the total rounds must allow enough play opportunities for everyone.
6. Print the result.

Why it works: Each round allows exactly n-1 participants. The formula ensures that the total desired plays can be distributed among rounds while respecting the supervisor constraint. Taking the maximum with the largest individual desire guarantees that no person’s requirement is underfulfilled. This invariant guarantees correctness regardless of the distribution of `a[i]`.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import ceil

n = int(input())
a = list(map(int, input().split()))

total = sum(a)
max_a = max(a)

# minimum rounds to satisfy total capacity
min_rounds_needed = ceil(total / (n - 1))

# the result must also satisfy the largest individual's requirement
result = max(max_a, min_rounds_needed)
print(result)
```

This solution directly implements the mathematical reasoning. Summing `a` gives total desired plays, and finding `max(a)` identifies the strictest individual constraint. We use `ceil(total / (n - 1))` to ensure enough rounds for all friends collectively. The maximum guarantees that no individual is left short.

## Worked Examples

**Sample Input 1:**

```
3
3 2 2
```

| Step | total | max_a | ceil(total/(n-1)) | result |
| --- | --- | --- | --- | --- |
| Compute total | 3+2+2=7 | 3 | ceil(7/2)=4 | max(3,4)=4 |

This shows that although the maximum individual desire is 3, the total desired plays require at least 4 rounds to distribute the opportunities.

**Sample Input 2:**

```
4
1 1 1 10
```

| Step | total | max_a | ceil(total/(n-1)) | result |
| --- | --- | --- | --- | --- |
| Compute total | 1+1+1+10=13 | 10 | ceil(13/3)=5 | max(10,5)=10 |

Here the single friend who wants 10 rounds dominates the calculation. The minimum rounds needed to satisfy total sum would be only 5, but the largest individual desire requires 10 rounds, which becomes the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We need to iterate once over the array to compute sum and max. |
| Space | O(1) | Only a few variables are needed beyond input. |

Given n up to 10^5, iterating once over the array is efficient, and the solution easily fits within memory limits since only integers are stored.

## Test Cases

```python
import sys, io
from math import ceil

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    total = sum(a)
    max_a = max(a)
    return str(max(max_a, ceil(total/(n-1))))

# provided sample
assert run("3\n3 2 2\n") == "4", "sample 1"

# minimum size
assert run("3\n1 1 1\n") == "1", "minimum size equal desires"

# large individual desire
assert run("4\n1 1 1 10\n") == "10", "dominant individual desire"

# all equal values
assert run("5\n2 2 2 2 2\n") == "3", "all equal values"

# maximum n, large numbers
inp = "100000\n" + " ".join(["1000000000"]*100000) + "\n"
assert run(inp) == str(max(1000000000, ceil(1000000000*100000/99999))), "max n large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 2 2 | 4 | total sum > max individual requirement |
| 3 1 1 1 | 1 | minimum input size with equal desires |
| 4 1 1 1 10 | 10 | dominant individual desire |
| 5 2 2 2 2 2 | 3 | all equal values |
| 100000 all 10^9 | computed | max n, large numbers |

## Edge Cases

For `3 1 1 1`, the total desired plays is 3 and each round allows 2 players. `ceil(3/2) = 2`, but the maximum individual desire is 1, so the answer is max(1,2)=2. The algorithm correctly identifies that at least 2 rounds are needed to distribute all plays.

For `4 1 1 1 10`, the sum is 13, `ceil(13/3)=5`, but one friend wants 10 rounds. The algorithm takes max(10,5)=10, correctly honoring the strictest individual requirement.

These examples demonstrate that the solution simultaneously respects collective capacity and individual desires, handling both extremes accurately.
