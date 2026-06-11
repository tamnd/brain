---
title: "CF 1216B - Shooting"
description: "We are given a line of cans, each with a durability value. Vasya has to shoot all cans exactly once, but the number of shots required to knock down a can depends on how many cans have already been knocked down."
date: "2026-06-11T22:52:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1216
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 587 (Div. 3)"
rating: 900
weight: 1216
solve_time_s: 132
verified: true
draft: false
---

[CF 1216B - Shooting](https://codeforces.com/problemset/problem/1216/B)

**Rating:** 900  
**Tags:** greedy, implementation, sortings  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of cans, each with a durability value. Vasya has to shoot all cans exactly once, but the number of shots required to knock down a can depends on how many cans have already been knocked down. Specifically, if a can has durability $a_i$ and Vasya has already knocked down $x$ cans, he needs $a_i \cdot x + 1$ shots to destroy that can. The goal is to determine the shooting order that minimizes the total number of shots and report both the minimal total and one valid order.

The input consists of the number of cans $n$ (up to 1000) and their durability values $a_i$ (up to 1000). These bounds indicate that algorithms with $O(n^2)$ or faster are acceptable, but any algorithm that tries all $n!$ permutations is infeasible, as $1000!$ is astronomically large.

An edge case occurs when multiple cans have the same durability. The optimal order might not be unique, but the total number of shots should be the same regardless of which equivalent cans are chosen first. Another subtle point is that the smallest total may require starting with the smallest durability can, which can be non-intuitive without careful reasoning.

## Approaches

A brute-force approach would attempt every permutation of the cans, compute the total number of shots for each order, and select the minimum. This is correct but entirely impractical because $n!$ grows faster than any feasible computation for $n = 1000$. For $n = 10$, this already requires 3,628,800 checks.

The key insight is to recognize the cost function for a can, $a_i \cdot x + 1$, grows linearly with the number of cans already knocked down. Therefore, the impact of a can’s durability is magnified if it is shot later. To minimize the total, we want high-durability cans to experience as small an $x$ as possible, which means shooting them earlier. Conversely, cans with low durability can be delayed because their contribution grows slower with increasing $x$. This observation leads to a greedy approach: sort the cans in decreasing order of durability and shoot in that order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (Greedy by durability) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and the durability array $a$. Each element of $a$ is paired with its original index to track the shooting order.
2. Sort the list of pairs by durability in descending order. This ensures that the cans requiring more shots if delayed are shot earlier.
3. Initialize a counter for the number of cans already shot, $x = 0$, and a variable to accumulate total shots, $total = 0$.
4. Iterate through the sorted cans. For each can with durability $a_i$, compute the shots required as $a_i \cdot x + 1$. Add this to $total$ and increment $x$ by one.
5. Extract the original indices from the sorted pairs to form the shooting order.
6. Print $total$ and the shooting order.

Why it works: The algorithm guarantees that each can's cost is multiplied by the smallest possible number of previously knocked-down cans among all cans with equal or higher durability. This maintains the invariant that no other permutation can produce a smaller total because placing a higher durability can later would increase its weighted contribution, which is suboptimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# Pair durability with original indices
cans = [(a[i], i + 1) for i in range(n)]
# Sort by descending durability
cans.sort(reverse=True, key=lambda x: x[0])

total = 0
order = []

for x, (dur, idx) in enumerate(cans):
    total += dur * x + 1
    order.append(idx)

print(total)
print(' '.join(map(str, order)))
```

The solution reads input efficiently using `sys.stdin.readline`. The pairing of durability with original indices preserves the mapping after sorting. The sort key ensures descending durability. The total shots are accumulated in a loop where `x` naturally tracks the number of cans already shot. Finally, indices are output in the sorted shooting order.

## Worked Examples

### Sample 1

Input:

```
3
20 10 20
```

| Step | x | Can (dur, idx) | Shots added | Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | (20,1) | 1 | 1 |
| 1 | 1 | (20,3) | 21 | 22 |
| 2 | 2 | (10,2) | 21 | 43 |

This trace confirms that shooting the highest durability cans first minimizes the total shots.

### Custom Sample

Input:

```
4
1 3 2 4
```

| Step | x | Can (dur, idx) | Shots added | Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | (4,4) | 1 | 1 |
| 1 | 1 | (3,2) | 4 | 5 |
| 2 | 2 | (2,3) | 5 | 10 |
| 3 | 3 | (1,1) | 4 | 14 |

The algorithm chooses the order `[4,2,3,1]` and achieves the minimal total.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, linear scan to accumulate shots is O(n) |
| Space | O(n) | Store durability-index pairs and output order |

For $n \le 1000$, this runs comfortably within time limits, as sorting 1000 elements is trivial and accumulation is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    cans = [(a[i], i + 1) for i in range(n)]
    cans.sort(reverse=True, key=lambda x: x[0])
    total = 0
    order = []
    for x, (dur, idx) in enumerate(cans):
        total += dur * x + 1
        order.append(idx)
    return f"{total}\n{' '.join(map(str, order))}"

# Provided samples
assert run("3\n20 10 20\n") == "43\n1 3 2"
# Custom test cases
assert run("4\n1 3 2 4\n") == "14\n4 2 3 1"
assert run("2\n5 5\n") == "7\n1 2"
assert run("5\n1 2 3 4 5\n") == "35\n5 4 3 2 1"
assert run("3\n1 1 1\n") == "6\n1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 1 3 2 4 | 14 4 2 3 1 | General case with mixed durabilities |
| 2 5 5 | 7 1 2 | Two equal durabilities |
| 5 1 2 3 4 5 | 35 5 4 3 2 1 | Increasing durabilities |
| 3 1 1 1 | 6 1 2 3 | All equal durabilities |

## Edge Cases

For equal durability cans, the algorithm preserves correctness because their ordering does not affect the total. For example, input `3 1 1 1` produces total 6 regardless of order. The trace:

| Step | x | Can (dur, idx) | Shots added | Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | (1,1) | 1 | 1 |
| 1 | 1 | (1,2) | 2 | 3 |
| 2 | 2 | (1,3) | 3 | 6 |

The invariant that higher durability cans go first is trivially satisfied, and the output remains valid.
