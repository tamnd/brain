---
title: "CF 1013A - Piles With Stones"
description: "We are given two snapshots of the same system of stone piles. In the first snapshot, each pile has some number of stones, and in the second snapshot the piles have different counts."
date: "2026-06-16T22:32:08+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1013
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 500 (Div. 2) [based on EJOI]"
rating: 800
weight: 1013
solve_time_s: 75
verified: true
draft: false
---

[CF 1013A - Piles With Stones](https://codeforces.com/problemset/problem/1013/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two snapshots of the same system of stone piles. In the first snapshot, each pile has some number of stones, and in the second snapshot the piles have different counts. Between the two moments, during the night, two types of operations may happen any number of times: a stone can be removed from a pile entirely, or a stone can be moved from one pile to another pile. There is no restriction on how many such actions occur or how many different people perform them, so we only care about whether it is possible to transform the first configuration into the second using these two primitive operations.

The question is not to construct a sequence of moves, but only to decide feasibility. We are effectively checking whether one integer array can be transformed into another using “remove 1 from any index” and “transfer 1 unit between indices” operations.

The constraints are small, with at most 50 piles. That immediately rules out any need for heavy data structures or optimization beyond linear or quadratic reasoning. Any solution that is O(n²) or even O(n) is easily fast enough, and the problem is really about understanding what these operations preserve and what they can change.

A subtle failure case appears when the total number of stones changes in a way that cannot be explained only by removals, or when redistribution is not enough to match the target shape.

For example, if we had:

```
x = [1, 0]
y = [0, 2]
```

This is impossible, because we cannot create extra stones. Moves only redistribute or delete stones.

Another example:

```
x = [0, 0]
y = [1, 1]
```

This is also impossible for the same reason: no operation increases total stones.

These examples show that the core difficulty is not per-pile behavior but global conservation and inequality structure.

## Approaches

The brute-force interpretation would simulate all possible sequences of moves and removals. Each step either decreases total stones or transfers one unit between positions. Even though the branching factor is conceptually large, the state space is enormous because piles can take many intermediate values. This immediately becomes intractable, since even small values of n and pile sizes produce exponentially many reachable states.

The key observation is that the operations can be understood globally rather than locally. Moving a stone does not change the total number of stones, while removing a stone decreases the total by exactly one. This means the only irreversible effect in the system is decreasing the sum of all elements.

From this, we get a strong simplification: starting from the initial array, we can redistribute stones arbitrarily using moves, so the only real constraint is whether we have enough stones overall to match the target configuration. If the target requires more stones than we initially have, it is impossible. If we have at least as many stones, we can always discard extras and rearrange the rest using transfers.

Thus the entire problem reduces to comparing the sum of both arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | High | Too slow |
| Sum Comparison | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of stones in the initial configuration. This represents all stones we start with before any operations.
2. Compute the sum of stones in the final configuration. This is the amount of stone mass that must remain after all operations.
3. Compare the two sums. If the initial sum is less than the final sum, output “No”, because we cannot create new stones.
4. Otherwise, output “Yes”, since any surplus stones can be removed and any distribution differences can be fixed using transfers.

### Why it works

The crucial invariant is that transfers preserve the total sum, while removals decrease it by exactly one per operation. Therefore, the only constraint imposed by the process is that the final total cannot exceed the initial total. Since we can freely move stones between piles, any redistribution is achievable once we have enough total mass. There is no hidden structure such as parity or per-index constraints, because no operation limits how stones are rearranged aside from the fact that we cannot create new ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))

    if sum(x) >= sum(y):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The solution reads both arrays and computes their sums directly. The comparison is sufficient because all allowed operations either preserve or reduce the total number of stones, never increase it.

A common implementation mistake would be attempting to match piles individually. That is unnecessary and misleading, because transfers allow arbitrary reshaping. Only the global sum matters.

## Worked Examples

### Example 1

Input:

```
n = 5
x = [1, 2, 3, 4, 5]
y = [2, 1, 4, 3, 5]
```

| Step | sum(x) | sum(y) | Decision |
| --- | --- | --- | --- |
| initial | 15 | 15 | compare |
| final | 15 | 15 | equal |

We see both totals are equal, so no stones need to be removed. Since transfers allow arbitrary redistribution, we can transform x into y by moving stones between piles.

Output is “Yes”.

### Example 2

Input:

```
n = 4
x = [1, 1, 1, 1]
y = [3, 1, 1, 1]
```

| Step | sum(x) | sum(y) | Decision |
| --- | --- | --- | --- |
| initial | 4 | 6 | compare |

Here the target requires 6 stones while only 4 exist initially. Since we cannot create stones, the transformation is impossible regardless of redistribution.

Output is “No”.

These examples show that equality allows full flexibility, while deficit immediately blocks feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We sum two arrays of size n once |
| Space | O(1) | Only running totals are stored |

The constraints allow up to 50 piles, so a single linear pass is trivial. Even if n were much larger, this approach remains optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(input())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))

    return "Yes" if sum(x) >= sum(y) else "No"

# provided sample
assert run("5\n1 2 3 4 5\n2 1 4 3 5\n") == "Yes"

# custom: insufficient total
assert run("3\n1 1 1\n2 2 2\n") == "No"

# custom: exact match but different distribution
assert run("4\n0 5 0 0\n1 1 1 2\n") == "Yes"

# custom: all zeros
assert run("3\n0 0 0\n0 0 0\n") == "Yes"

# custom: single pile decrease
assert run("1\n5\n3\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal permutation | Yes | redistribution only |
| insufficient sum | No | impossibility due to creation requirement |
| sparse redistribution | Yes | transfers can reshape arbitrarily |
| all zeros | Yes | trivial edge case |
| single pile | Yes | minimal n behavior |

## Edge Cases

When all piles are zero initially and also zero finally, both sums are zero, so the algorithm correctly outputs “Yes” immediately.

For a case like:

```
x = [2, 0]
y = [1, 1]
```

the algorithm computes sum(x) = 2 and sum(y) = 2, so it returns “Yes”. Even though the distribution differs, a single transfer operation moves one stone from pile 1 to pile 2, matching the target exactly.

For a case like:

```
x = [1, 0]
y = [0, 2]
```

we get sum(x) = 1 and sum(y) = 2. The algorithm correctly returns “No”, because even unlimited transfers cannot compensate for missing total stones.

Each edge case confirms the same invariant: only total stone count matters, and redistribution has no additional constraints.
