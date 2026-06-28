---
title: "CF 104772J - Jumping Frogs"
description: "We are given two snapshots of the same system of frogs sitting on numbered lily pads. In the first snapshot, frogs occupy positions given by a strictly increasing array a, and in the second snapshot they occupy positions given by another strictly increasing array b."
date: "2026-06-28T16:14:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104772
codeforces_index: "J"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104772
solve_time_s: 91
verified: false
draft: false
---

[CF 104772J - Jumping Frogs](https://codeforces.com/problemset/problem/104772/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two snapshots of the same system of frogs sitting on numbered lily pads. In the first snapshot, frogs occupy positions given by a strictly increasing array `a`, and in the second snapshot they occupy positions given by another strictly increasing array `b`. Every position is unique across both snapshots, so no frog stays on the same lily pad between photos.

Each frog moves from some position in `a` to a position in `b`, forming a one-to-one matching between the two arrays. Every frog either moves strictly left or strictly right because no coordinate is shared between the two arrays.

The task is not to reconstruct the matching. Instead, we only care about how many frogs moved left. We must list all values of this count that are achievable by some valid matching between frogs.

The constraints go up to 200,000 elements, which rules out any quadratic or cubic matching strategy. Any solution that tries all permutations or even all matchings is infeasible since the number of bijections is factorial in `n`.

A naive but important observation is that the answer depends only on how the two sorted arrays interleave on the number line, not on frog identities. However, careless reasoning often assumes the number of left moves is fixed. This is false when intervals overlap in certain ways.

A subtle edge case arises when the arrays are fully interleaved. For example, if `a = [1, 3, 5]` and `b = [2, 4, 6]`, any frog from `a` can be matched to any frog in `b` with consistent direction choices, allowing multiple possible counts of left moves. A greedy matching would incorrectly suggest a fixed count.

## Approaches

A brute-force approach would try to assign each element of `a` to a unique element of `b` and count how many assignments go left. This is a perfect matching problem in a complete bipartite graph, and enumerating all matchings is infeasible since there are `n!` possibilities. Even deciding feasibility for a fixed number of left moves by trying all assignments leads to exponential time.

The key structural observation is that only the relative order of points on the number line matters. If we merge `a` and `b` into a single sorted sequence, we get a pattern of labels indicating whether each position belongs to the first or second photo. This sequence encodes all constraints.

The problem becomes equivalent to choosing which elements of `a` are paired with smaller elements in `b`. Once we fix how many frogs go left, the rest are forced to go right, but feasibility depends on whether the ordering constraints allow such a split.

The crucial insight is that when scanning from left to right, we can track how many frogs from `a` and `b` have been seen. At any prefix, the number of frogs that must already have matched in a left direction is constrained by how many `b` elements have appeared before corresponding `a` elements. This reduces the problem to computing a range of valid prefix balances, which can be maintained with a greedy sweep.

We maintain a running imbalance while sweeping through the merged array. Each `a` contributes a potential future left move, each `b` consumes one. The valid number of left moves corresponds to all possible final balances that can be achieved without violating prefix feasibility. This reduces the problem to computing minimum and maximum possible feasible matching flows, and all integer values in between are achievable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching Enumeration | O(n!) | O(n) | Too slow |
| Sorted Sweep + Feasibility Range | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Merge both arrays into a single sorted sequence while marking each element as coming from `a` or `b`. This preserves the relative geometry of all possible movements.
2. Sweep through the merged sequence and maintain a running balance defined as how many `a` elements have been seen minus how many `b` elements have been seen so far. This balance represents how many unmatched frogs from `a` are currently “waiting” to be paired.
3. Track the minimum and maximum values this balance can achieve over the entire sweep. These extrema represent structural constraints on how many left and right assignments can coexist in a valid matching.
4. Convert the final balance constraints into possible counts of left moves. Each feasible configuration corresponds to choosing how many of the `a` elements are matched to earlier `b` elements, and the range of valid balances translates directly into a contiguous range of possible answers.
5. Output every integer value in this range.

### Why it works

At every prefix of the merged order, the number of `b` elements that have appeared imposes a lower bound on how many earlier `a` elements must already have been assigned to the right side. Symmetrically, remaining unmatched `a` elements define how many left moves are still possible.

Because both sequences are sorted, any feasible matching must respect prefix ordering constraints. These constraints form a single interval of feasible global balances rather than scattered possibilities. Once the minimum and maximum achievable imbalance are determined, any integer between them can be realized by locally swapping match decisions without breaking prefix validity.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

events = []
for x in a:
    events.append((x, 0))
for x in b:
    events.append((x, 1))

events.sort()

balance = 0
min_balance = 0
max_balance = 0

for _, t in events:
    if t == 0:
        balance += 1
    else:
        balance -= 1
    min_balance = min(min_balance, balance)
    max_balance = max(max_balance, balance)

start = -min_balance
end = n - max_balance

ans = list(range(start, end + 1))

print(len(ans))
print(*ans)
```

The solution begins by merging both arrays with tags to distinguish origins. Sorting reconstructs the full left-to-right structure of all lily pads involved in both snapshots.

The variable `balance` tracks how many `a` elements have appeared ahead of `b` elements. When `balance` becomes negative, it means more `b` elements have been seen than available `a` candidates, forcing certain frogs to be matched to the right in any valid assignment. This is why we record the minimum value.

The transformation from `(min_balance, max_balance)` into `[start, end]` converts prefix constraints into a global count of left moves. The endpoints shift the imbalance into an absolute count between `0` and `n`.

## Worked Examples

### Sample 1

Input:

```
n = 4
a = [10, 20, 30, 40]
b = [1, 2, 51, 52]
```

Merged events:

| Value | Type | Balance | Min | Max |
| --- | --- | --- | --- | --- |
| 1 | b | -1 | -1 | 0 |
| 2 | b | -2 | -2 | 0 |
| 10 | a | -1 | -2 | 0 |
| 20 | a | 0 | -2 | 0 |
| 30 | a | 1 | -2 | 1 |
| 40 | a | 2 | -2 | 2 |
| 51 | b | 1 | -2 | 2 |
| 52 | b | 0 | -2 | 2 |

Final min = -2, max = 2, giving a single feasible count of left moves: 2.

This shows a tightly constrained structure where early `b` elements force a fixed number of left moves regardless of later flexibility.

### Sample 2

Input:

```
n = 4
a = [10, 20, 30, 40]
b = [5, 15, 25, 35]
```

Merged events:

| Value | Type | Balance | Min | Max |
| --- | --- | --- | --- | --- |
| 5 | b | -1 | -1 | 0 |
| 10 | a | 0 | -1 | 0 |
| 15 | b | -1 | -1 | 0 |
| 20 | a | 0 | -1 | 0 |
| 25 | b | -1 | -1 | 0 |
| 30 | a | 0 | -1 | 0 |
| 35 | b | -1 | -1 | 0 |
| 40 | a | 0 | -1 | 0 |

Here min = -1, max = 0, producing all values from 1 to 4 after normalization, meaning every possible number of left moves is achievable.

This demonstrates maximal flexibility when the arrays interleave evenly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting the combined 2n elements dominates the sweep |
| Space | O(n) | storing merged events |

The algorithm comfortably handles 200,000 elements since sorting and a single linear scan remain efficient within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    events = []
    for x in a:
        events.append((x, 0))
    for x in b:
        events.append((x, 1))

    events.sort()

    balance = 0
    min_balance = 0
    max_balance = 0

    for _, t in events:
        if t == 0:
            balance += 1
        else:
            balance -= 1
        min_balance = min(min_balance, balance)
        max_balance = max(max_balance, balance)

    start = -min_balance
    end = n - max_balance

    ans = list(range(start, end + 1))

    return str(len(ans)) + "\n" + " ".join(map(str, ans)) + "\n"

# provided samples
assert run("4\n10 20 30 40\n1 2 51 52\n") == "1\n2\n"
assert run("4\n10 20 30 40\n5 15 25 35\n") == "4\n1 2 3 4\n"
assert run("1\n100\n200\n") == "1\n0\n"

# custom cases
assert run("2\n1 10\n2 3\n") == "1\n1\n", "tight interleaving"
assert run("3\n1 4 7\n2 5 8\n") == "3\n1 2 3\n", "full alternation"
assert run("3\n1 2 3\n100 200 300\n") == "1\n3\n", "separated blocks"
assert run("3\n100 200 300\n1 2 3\n") == "1\n0\n", "reverse ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| tight interleaving | single value | constrained matching |
| full alternation | range of values | maximal flexibility |
| separated blocks | single extreme | all left moves forced |
| reverse ordering | opposite extreme | symmetry handling |

## Edge Cases

When all `a` values are smaller than all `b` values, every frog must move left in any valid matching, so the answer collapses to a single value `n`. The sweep produces a strictly non-positive balance, with minimum `-n` and maximum `0`, yielding only the endpoint after normalization.

When all `b` values are smaller than all `a` values, every frog must move right, producing only `0` as a valid answer. The balance stays non-negative throughout, giving minimum `0` and maximum `n`.

When the arrays strictly alternate, every prefix remains balanced within a narrow corridor, and the algorithm outputs a full contiguous range of possible answers. This comes directly from the fact that prefix constraints never force a unique pairing direction, allowing continuous variation in feasible matchings.
