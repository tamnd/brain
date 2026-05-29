---
title: "CF 440B - Balancer"
description: "We are given a row of matchboxes, each containing some number of matches. The total number of matches is divisible by the number of boxes, so there exists a target configuration where every box ends up holding exactly the same number."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 440
codeforces_index: "B"
codeforces_contest_name: "Testing Round 10"
rating: 1600
weight: 440
solve_time_s: 63
verified: true
draft: false
---

[CF 440B - Balancer](https://codeforces.com/problemset/problem/440/B)

**Rating:** 1600  
**Tags:** greedy, implementation  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of matchboxes, each containing some number of matches. The total number of matches is divisible by the number of boxes, so there exists a target configuration where every box ends up holding exactly the same number.

The only allowed operation is moving a single match from one box to its immediate neighbor. A move is local, so transporting a match from box 1 to box 5 costs multiple moves because it must pass through intermediate boxes.

The task is to compute the minimum number of such adjacent moves required to transform the initial distribution into a perfectly balanced one.

The key constraint is that the number of boxes can be as large as 50000, while values can reach 10^9. This immediately rules out any simulation that moves individual matches one by one. Even a single match might require O(n) steps to relocate, and doing that naively for all matches would lead to O(nk) behavior, which is far beyond limits.

The hidden difficulty is that moves are not independent. Moving one match changes the local imbalance and affects future decisions, so greedy local balancing must be carefully structured to avoid double counting or missing indirect flows.

A common failure case appears when trying to “fix” each box independently by sending excess to the right or left without tracking cumulative flow. For example, if we try to greedily push surplus to neighbors, we might count the same movement multiple times as it propagates through the line.

A small illustration of failure: consider input `3` with `[1, 0, 5]`. A naive approach might send 2 matches from the last box to the middle, and then 2 from the middle to the first, but if the propagation is not tracked properly, the same unit movement can be counted inconsistently depending on direction handling.

The correct solution needs a global view of imbalance flow rather than local fixes.

## Approaches

A brute-force idea is to repeatedly scan the array, find a box with surplus, and move one match step by step toward a deficit. Each such move is simulated explicitly. This is correct because it literally follows the allowed operation, but it is far too slow. In the worst case, a match may travel O(n) distance and there may be O(nk) such moves, leading to quadratic or worse behavior depending on distribution.

The improvement comes from noticing that we do not need to simulate individual matches. What matters is how many matches must cross each boundary between adjacent boxes.

If we look at the prefix of boxes up to index i, it has some difference between the number of matches it currently holds and the number it should hold in the final balanced state. That difference must be pushed across the boundary between i and i+1. This means every imbalance in a prefix translates directly into required movement across that edge.

So instead of tracking individual matches, we track a running imbalance. As we move from left to right, we maintain how many extra or missing matches have accumulated so far. The absolute value of this imbalance at each position is exactly the number of matches that must cross that boundary.

This reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nk) worst case | O(n) | Too slow |
| Prefix imbalance tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the target number of matches per box by dividing the total sum by n. This gives the final required value for each position.
2. Initialize two variables: a running imbalance `carry` and an answer accumulator `moves`. The `carry` represents how many excess matches have been passed from previous boxes but not yet absorbed.
3. Iterate through each box from left to right.
4. At each box i, update the imbalance by adding the current box’s deviation from the target:

`carry += a[i] - target`.
5. Add the absolute value of `carry` to the answer. This represents matches that must cross the boundary between box i and i+1 due to accumulated imbalance.
6. Continue until the end. The final answer is the sum of all absolute imbalances.

The crucial reasoning step is that once we fix a prefix, any remaining imbalance must physically pass through the boundary to the next segment, and each such pass costs exactly one move per unit match.

### Why it works

At every position i, the variable `carry` equals the net surplus of matches in the prefix `[0..i]` compared to what that prefix should contain in the final configuration. Since matches can only move across adjacent boundaries, every unit of this surplus must cross the boundary at i at some point. Summing absolute values of these surpluses counts each crossing exactly once, because each imbalance is associated with exactly one boundary transition in the flow representation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    target = total // n
    
    carry = 0
    moves = 0
    
    for x in a:
        carry += x - target
        moves += abs(carry)
    
    print(moves)

if __name__ == "__main__":
    solve()
```

The implementation follows the prefix imbalance idea directly. The target is computed once. The loop maintains the running surplus or deficit. The absolute value accumulation is the key step, since it counts how much flow must cross each boundary.

A subtle point is that we do not reset `carry` after adding to `moves`. The carry represents persistent imbalance propagating through the array, so resetting it would destroy the global flow structure.

## Worked Examples

### Example 1

Input:

```
6
1 6 2 5 3 7
```

Target per box is 4.

| i | a[i] | carry before | carry after | abs(carry) | moves |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | -3 | 3 | 3 |
| 1 | 6 | -3 | -1 | 1 | 4 |
| 2 | 2 | -1 | -3 | 3 | 7 |
| 3 | 5 | -3 | -2 | 2 | 9 |
| 4 | 3 | -2 | -3 | 3 | 12 |
| 5 | 7 | -3 | 0 | 0 | 12 |

Final answer is 12.

This trace shows how imbalance propagates across the array rather than being resolved locally. Each step’s absolute carry corresponds to required cross-boundary movement.

### Example 2

Input:

```
4
0 0 8 0
```

Target is 2.

| i | a[i] | carry before | carry after | abs(carry) | moves |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | -2 | 2 | 2 |
| 1 | 0 | -2 | -4 | 4 | 6 |
| 2 | 8 | -4 | 2 | 2 | 8 |
| 3 | 0 | 2 | 0 | 0 | 8 |

This shows a strong buildup of deficit on the left until surplus arrives at index 2, after which it gets absorbed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over array computing prefix imbalance |
| Space | O(1) | only constant extra variables are used |

The algorithm fits comfortably within constraints since n can reach 50000 and we only perform a linear scan with simple arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("6\n1 6 2 5 3 7\n") == "12"

# all equal (no moves needed)
assert run("3\n2 2 2\n") == "0"

# simple imbalance
assert run("2\n0 10\n") == "5"

# alternating imbalance
assert run("4\n0 0 8 0\n") == "8"

# minimum n
assert run("1\n0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 equal values | 0 | no movement needed |
| 0 10 | 5 | single boundary flow |
| 0 0 8 0 | 8 | multi-step redistribution |
| n=1 | 0 | edge case stability |

## Edge Cases

One edge case is when all matches are already evenly distributed. The algorithm handles this cleanly because `carry` remains zero throughout, and no absolute contributions are added.

Another case is when imbalance accumulates heavily on one side before being resolved later. For example:

```
4
0 0 8 0
```

The carry becomes increasingly negative until the surplus is encountered. Each step contributes correctly to the answer because each boundary must carry that deficit forward.

A final case is minimal input size:

```
1
k
```

Since there are no boundaries, no movement is needed. The loop runs once, but carry is immediately zero after subtracting target, resulting in zero moves.
