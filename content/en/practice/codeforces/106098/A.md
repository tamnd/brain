---
title: "CF 106098A - Bald and Tourist"
description: "The problem is a two-player game played on a list of problems, where each problem has a distinct difficulty value. The difficulty values form a permutation, so every number from 1 to n appears exactly once. Tourist moves first, and the players alternate turns."
date: "2026-06-25T11:54:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106098
codeforces_index: "A"
codeforces_contest_name: "The American University in Cairo CSEA Fall 2025 contest"
rating: 0
weight: 106098
solve_time_s: 38
verified: true
draft: false
---

[CF 106098A - Bald and Tourist](https://codeforces.com/problemset/problem/106098/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is a two-player game played on a list of problems, where each problem has a distinct difficulty value. The difficulty values form a permutation, so every number from 1 to n appears exactly once.

Tourist moves first, and the players alternate turns. On each turn, the current player selects any remaining problem and immediately gains points equal to its difficulty. That problem is then removed from the pool. The game ends when no problems remain, and the winner is the player with the larger total score. If both scores are equal, Tourist still does not lose explicitly, but the task asks us to decide who wins under optimal play.

A key observation is that there is no restriction on which problem can be taken at any time, so the only structure comes from the scoring rule and turn order. Since all values are positive and distinct, both players are always incentivized to take large remaining values when possible.

The input size goes up to 100000, which immediately rules out any solution that simulates strategies involving searching or recomputing choices per move in quadratic time. Any approach that inspects all remaining elements repeatedly would degrade to O(n^2), which is too slow. We should expect that the answer depends on a direct combinational property of the permutation rather than any dynamic simulation.

A subtle edge case appears when n is small or when the ordering is adversarial.

For example, when n = 1 and the array is [1], Tourist takes the only element and wins.

When n = 2 and the array is [1, 2], Tourist takes 2, Bald takes 1, and Tourist wins by 1 point. A naive idea might be that turn order alone determines the winner, but this is already misleading because the optimal play always selects the largest remaining element.

The deeper issue is that any strategy that tries to track “positions” in the array is irrelevant because the array is not positional in effect, only the multiset of values matters.

## Approaches

A brute-force simulation would try to model the game state explicitly. At each turn, a player would scan all remaining elements, pick one according to some strategy, and remove it. Even if both players always pick greedily, we still simulate n turns, and each turn requires scanning up to O(n) elements, leading to O(n^2) time. This already fails for n = 100000.

The important simplification is to recognize that both players are symmetric in capability and fully rational, and every move is simply a choice of a remaining number. Since all values are distinct and additive, the only meaningful decision is the ordering in which the multiset of values is consumed.

If we sort all values in descending order, optimal play effectively assigns the largest remaining value to the current player on their turn. There is no scenario where a player would skip a larger value to take a smaller one, because that only reduces their final sum and gives the opponent a strictly better future position.

Thus the game reduces to distributing sorted values alternately between Tourist and Bald. Tourist gets the first pick, then Bald, and so on.

So Tourist receives values at positions 0, 2, 4, ... in the sorted array, and Bald receives positions 1, 3, 5, ...

The winner is determined by comparing the sum of these two subsequences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Sort + Alternating Sum | O(n log n) | O(1) extra (besides input) | Accepted |

## Algorithm Walkthrough

1. Read the permutation of size n and store all values.
2. Sort the values in descending order so that we always consider the best remaining choice first.
3. Initialize two accumulators, one for Tourist and one for Bald.
4. Iterate through the sorted array. Assign index 0, 2, 4, ... to Tourist and 1, 3, 5, ... to Bald, adding each value to the respective sum.
5. Compare the two sums. If Tourist’s total is strictly larger, he wins. Otherwise Bald wins.

The key reasoning step is why alternating assignment is valid. At any point in the game, both players see the same remaining set. Since all values are positive and independent, taking a smaller value while a larger one exists can never improve the outcome. This forces both players into the same greedy behavior, making the sorted alternating assignment represent the unique optimal outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    tourist = 0
    bald = 0
    
    for i, val in enumerate(a):
        if i % 2 == 0:
            tourist += val
        else:
            bald += val
    
    if tourist > bald:
        print("Tourist")
    else:
        print("Bald")

if __name__ == "__main__":
    solve()
```

The solution first sorts the array in descending order so that the strongest available choices are always considered first. The loop then assigns values based purely on parity of turn index, which corresponds to who plays first and maintains strict alternation.

A common mistake here is trying to simulate actual game decisions with a priority queue but still recomputing choices each turn unnecessarily. That leads to redundant logic without changing the outcome. The correct insight is that the game never deviates from global descending order assignment.

## Worked Examples

### Example 1

Input:

```
3
1 3 2
```

Sorted array is [3, 2, 1].

| Step | Chosen Value | Tourist Sum | Bald Sum |
| --- | --- | --- | --- |
| 0 | 3 | 3 | 0 |
| 1 | 2 | 3 | 2 |
| 2 | 1 | 4 | 2 |

Tourist ends with 4, Bald with 2, so Tourist wins.

This example shows how early access to the largest value dominates the outcome even when later values are balanced.

### Example 2

Input:

```
4
4 1 7 2
```

Sorted array is [7, 4, 2, 1].

| Step | Chosen Value | Tourist Sum | Bald Sum |
| --- | --- | --- | --- |
| 0 | 7 | 7 | 0 |
| 1 | 4 | 7 | 4 |
| 2 | 2 | 9 | 4 |
| 3 | 1 | 9 | 5 |

Tourist wins with 9 vs 5.

This confirms that the alternating greedy assignment consistently models optimal play regardless of original ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, single linear pass after |
| Space | O(1) extra | Only two accumulators beyond input storage |

The constraints allow up to 100000 elements, and sorting at this scale is comfortably within limits. The linear pass is negligible compared to the sort, and memory usage remains minimal since no additional structures beyond the array are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    t = 0
    b = 0
    
    for i, v in enumerate(a):
        if i % 2 == 0:
            t += v
        else:
            b += v
    
    return "Tourist" if t > b else "Bald"

# provided sample
assert run("3\n1 3 2\n") == "Tourist"

# minimum size
assert run("1\n1\n") == "Tourist"

# small even case
assert run("2\n1 2\n") == "Tourist"

# all increasing
assert run("5\n1 2 3 4 5\n") == "Tourist"

# all large spread
assert run("4\n10 1 100 2\n") == "Tourist"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | Tourist | base case |
| 2 elements | Tourist | first move advantage |
| increasing sequence | Tourist | sorting correctness |
| mixed values | Tourist | greedy assignment consistency |

## Edge Cases

One important edge case is n = 1. With input `1 1`, Tourist immediately takes the only value and wins. The algorithm assigns index 0 to Tourist, so Tourist gets the full sum correctly.

Another edge case is when the largest value is much larger than the sum of all others, for example `100000 1 2 3 ...`. After sorting, Tourist always takes the largest element first, guaranteeing dominance regardless of remaining distribution. The alternating assignment correctly reflects this because the first element is always assigned to Tourist.

A final subtle case is when sums are very close. For instance `3 2 1`. The sorted process yields Tourist = 3 + 1 and Bald = 2, so Tourist still wins. This confirms that parity-based allocation correctly models optimal behavior even when naive intuition might suggest balancing moves.
