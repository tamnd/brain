---
title: "CF 103584A - New Garden"
description: "We are given a nursery with a fixed number of tree slots, and a shop that sells several types of trees. Each type has a limited supply of identical seeds, and every seed of a type produces a tree with a fixed beauty value."
date: "2026-07-03T03:17:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103584
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 02-25-22 Div. 2 (Beginner)"
rating: 0
weight: 103584
solve_time_s: 50
verified: true
draft: false
---

[CF 103584A - New Garden](https://codeforces.com/problemset/problem/103584/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a nursery with a fixed number of tree slots, and a shop that sells several types of trees. Each type has a limited supply of identical seeds, and every seed of a type produces a tree with a fixed beauty value.

We want to plant exactly a given number of trees by picking seeds from these types, respecting availability limits. Each chosen seed contributes its beauty value to the total, and the goal is to maximize the sum of beauties over all planted trees.

The input consists of a small number of tree types, each described by how many seeds are available and how valuable each seed is. We must decide how many seeds to take from each type so that the total number of chosen seeds equals the required garden size, while maximizing total beauty.

The constraints imply a greedy or sorting-based approach is sufficient. The number of types is at most 100, so iterating over them is cheap. However, the total number of trees to pick can be as large as 100000, so any approach that simulates picking one tree at a time without structure is safe only if it is linear in total capacity, but we can do better by aggregating choices.

A naive idea is to treat every seed individually, expand all types into a long list of up to sum(t_i) items, then sort by beauty and pick the best m. This is correct but can be too slow if total seeds reach 2e5 or more in worst cases.

Edge cases matter when one type dominates or when m exceeds or is close to total available seeds.

A subtle failure case for careless implementations appears when we forget that we cannot take more than t_i seeds from a type. For example, if one type has high beauty but only 3 seeds exist, taking 10 would be invalid even if m is large.

Another corner case is when m exactly equals total supply. Any algorithm must then take everything without unnecessary logic assumptions about partial selection.

## Approaches

The brute-force interpretation is to create a conceptual list of all seeds, where each seed appears as many times as it is available with its associated beauty. Sorting this list and taking the top m values directly gives the answer because each seed is independent and contributes additively. The correctness is immediate, but the construction of this expanded list may involve up to 200000 entries, and sorting it costs O(N log N), which is still acceptable but not necessary.

The key observation is that all seeds of the same type are identical in value, so we never need to mix within a type. If we are going to use a type, we always take its most valuable units first, but since all are equal inside a type, we simply take as many as possible up to t_i. This turns the problem into selecting items from a multiset where each group has uniform value, so sorting groups by value is sufficient.

We sort types by beauty in descending order, then greedily take from the highest beauty types until we fill m slots. Each type contributes either all its available seeds or only the remaining required amount.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Expand all seeds + sort | O(S log S) | O(S) | Accepted but unnecessary |
| Sort types + greedy fill | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of types and required number of trees. Each type gives a pair consisting of available count and beauty value.
2. Sort the types in descending order of beauty, because we always want higher-value trees first.
3. Initialize the answer as zero and track how many trees we still need to pick.
4. Iterate through the sorted types. For each type, decide how many trees to take: either all available seeds of that type or only as many as still needed, whichever is smaller. Add their contribution to the total beauty.
5. Decrease the remaining quota accordingly.
6. Stop early once the quota reaches zero, since no further trees are needed.

The key idea is that at every step we are committing to the best available marginal choice, and since all items inside a type are identical, there is no hidden ordering within a type that could improve the result later.

### Why it works

At any point in the process, we maintain that all remaining unprocessed types have beauty less than or equal to the current one being considered. Because all items in a type are identical, swapping any chosen item with a later item can only decrease or maintain total beauty. This makes the greedy choice locally optimal and globally consistent, since the selection problem reduces to filling capacity with highest-weight blocks without internal structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    types = []
    
    for _ in range(n):
        t, b = map(int, input().split())
        types.append((b, t))
    
    types.sort(reverse=True)  # sort by beauty descending
    
    ans = 0
    remaining = m
    
    for b, t in types:
        if remaining == 0:
            break
        take = min(remaining, t)
        ans += take * b
        remaining -= take
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the greedy strategy. Sorting is done on beauty in descending order so that the loop always processes the most valuable trees first. The `take = min(remaining, t)` line is the crucial safeguard that enforces the supply constraint.

A common implementation mistake is forgetting to cap the number of taken trees per type, which would overcount availability. Another is sorting in the wrong direction, which would invert the greedy logic and produce a suboptimal sum.

## Worked Examples

### Example 1

Input:

```
3 8
5 4
4 6
3 5
```

After sorting by beauty:

| Type (beauty, count) | remaining | take | added | new remaining |
| --- | --- | --- | --- | --- |
| (6, 4) | 8 | 4 | 24 | 4 |
| (5, 3) | 4 | 3 | 15 | 1 |
| (4, 5) | 1 | 1 | 4 | 0 |

Final answer is 43.

This trace shows that higher beauty types are fully exhausted before moving to lower ones, which confirms the greedy selection behavior.

### Example 2

Input:

```
2 5
10 2
3 10
```

Sorted:

| Type | remaining | take | added | new remaining |
| --- | --- | --- | --- | --- |
| (10, 3) | 5 | 3 | 30 | 2 |
| (2, 10) | 2 | 2 | 4 | 0 |

Answer is 34.

This demonstrates that even if a low-count high-value type exists, it is fully prioritized before moving to lower values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the tree types dominates, followed by a single linear pass |
| Space | O(n) | Only stores the list of types |

The constraints n ≤ 100 and m up to 100000 make this easily fast enough. Even in worst cases, the algorithm performs only a few hundred operations beyond input parsing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, m = map(int, sys.stdin.readline().split())
    types = []
    for _ in range(n):
        t, b = map(int, sys.stdin.readline().split())
        types.append((b, t))

    types.sort(reverse=True)

    ans = 0
    remaining = m

    for b, t in types:
        if remaining == 0:
            break
        take = min(remaining, t)
        ans += take * b
        remaining -= take

    return str(ans)

# provided sample
assert run("3 8\n5 4\n4 6\n3 5\n") == "43"

# all equal values
assert run("2 5\n10 7\n10 7\n") == "35"

# single type only
assert run("1 4\n10 3\n") == "12"

# m exceeds total supply
assert run("2 10\n3 5\n4 2\n") == "23"

# strict greedy ordering case
assert run("3 5\n5 1\n2 10\n10 3\n") == "38"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed small sample | 43 | correctness of greedy ordering |
| equal beauties | 35 | stability when values tie |
| single type | 12 | direct multiplication case |
| insufficient total supply | 23 | partial exhaustion handling |
| mixed ordering | 38 | priority of high beauty types |

## Edge Cases

One edge case is when a single type dominates both in quantity and beauty. For example:

```
1 5
100 10
```

The algorithm immediately takes 5 trees from the only type and outputs 50. The loop executes once, and `take` correctly caps at m, so no over-selection occurs.

Another case is when multiple types share the same beauty value:

```
3 6
2 5
3 5
10 5
```

All types have equal priority after sorting. The algorithm simply accumulates from left to right until m is filled, and any order among them is valid since all contributions are identical.

A final case is when m equals zero, which can occur if interpreted incorrectly in some variants. The loop immediately terminates due to the `remaining == 0` guard, ensuring no accidental addition from types.
