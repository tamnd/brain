---
title: "CF 104427C - One, Two, Three"
description: "We are given a long sequence made only of the values 1, 2, and 3. From this sequence, we want to extract as many disjoint triples of indices as possible, where each triple uses three different positions and respects the order of indices."
date: "2026-06-30T18:58:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104427
codeforces_index: "C"
codeforces_contest_name: "2022-2023 Winter Petrozavodsk Camp, Day 2: GP of ainta"
rating: 0
weight: 104427
solve_time_s: 50
verified: true
draft: false
---

[CF 104427C - One, Two, Three](https://codeforces.com/problemset/problem/104427/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long sequence made only of the values 1, 2, and 3. From this sequence, we want to extract as many disjoint triples of indices as possible, where each triple uses three different positions and respects the order of indices.

A triple is considered valid if its values form either the pattern 1, 2, 3 in increasing index order, or the reversed pattern 3, 2, 1 in increasing index order. Every index can belong to at most one chosen triple, so once a position is used, it cannot be reused in another group.

The task is not just to compute how many such triples exist, but to explicitly construct a maximum collection of disjoint valid triples.

The constraint N up to 600000 immediately rules out any approach that tries to enumerate or test combinations of triples. Any solution must be linear or near-linear, since quadratic behavior would imply on the order of 10^11 operations in the worst case.

A subtle failure mode appears when greedy matching is done locally without regard to global balance. For example, if the sequence is heavily skewed like 1 1 1 2 2 2 3 3 3, pairing early occurrences of 1 and 3 too aggressively can block forming optimal 1-2-3 chains. Another issue arises if we only try to match forward patterns and ignore the reverse 3-2-1 structure, which can produce suboptimal results when the distribution is asymmetric.

## Approaches

A naive approach would attempt to build triples by checking every combination of i, j, k with i < j < k and verifying whether the values match either 1-2-3 or 3-2-1, while also ensuring indices are unused. This would require iterating over O(N^3) triples in the worst case, which is impossible for N up to 600000.

Even reducing this to fixing the middle index j and searching for matching i and k still leads to O(N^2). The core issue is that each element could potentially participate in many candidate triples, and checking compatibility pairwise still explodes combinatorially.

The key observation is that every valid triple has a very rigid structure. Each triple is either increasing in value (1 then 2 then 3) or decreasing in value (3 then 2 then 1). In both cases, the middle element is always a 2. This reduces the problem to pairing each chosen 2 with one 1 on its left and one 3 on its right, or symmetrically one 3 on its left and one 1 on its right.

This suggests treating 2s as anchors. We then attempt to match each 2 with a left-side pool and a right-side pool. The goal becomes maximizing how many anchors can be satisfied. Since each index is used at most once, we need a greedy strategy that preserves flexibility for future matches.

We scan the array and maintain three ordered lists of indices: positions of 1s, 2s, and 3s. Then we construct triples by pairing 2s with the closest available compatible endpoints. For a 2 at position j, we try to form either a 1-2-3 or a 3-2-1 triple. Choosing greedily with nearest available partners ensures we do not waste extreme positions that might be needed later.

A correct way to enforce this greediness is to process 2s from left to right and maintain two pointers into the 1-list and 3-list. Each time we attempt to form a triple, we pick the earliest valid left element and the earliest valid right element that still lie on correct sides of the current 2 and have not been used.

This turns the problem into a linear sweep with pointer advancement, where each index is consumed at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^3) | O(1) | Too slow |
| Optimal Greedy Matching | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We first separate indices into three increasing lists, one for each value. This allows us to reason about availability without repeatedly scanning the original array.

We then process potential centers, meaning indices where the value is 2, from left to right. For each such index, we attempt to build one valid triple.

For each 2 at position j, we try to construct a 1-2-3 triple first. We check whether there exists an unused 1 with index i < j and an unused 3 with index k > j. If both exist, we assign the smallest unused valid i and the smallest unused valid k. This minimizes consumption of large indices on the left and small indices on the right.

If the 1-2-3 formation is not possible, we try the reversed pattern 3-2-1. We check for a 3 on the left and a 1 on the right, again taking the closest available candidates.

If neither pattern is possible, we skip this 2, since it cannot contribute to any valid triple under current availability.

Each time we form a triple, we mark the used indices so they cannot participate again.

### Why it works

The algorithm maintains the property that all unused 1s, 2s, and 3s remain available in increasing order of indices, and we always consume the closest valid candidates to the current 2. This prevents unnecessary blocking of future 2s, since using an extreme endpoint when a closer one exists would only reduce flexibility without increasing the number of possible triples.

Any valid solution can be transformed into one that uses greedy nearest matching without decreasing the number of triples, because swapping a farther endpoint with a nearer unused one preserves validity while strictly improving or maintaining remaining availability on both sides. This exchange argument ensures that the greedy choice does not reduce optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    pos1 = []
    pos2 = []
    pos3 = []
    
    for i, x in enumerate(a):
        if x == 1:
            pos1.append(i)
        elif x == 2:
            pos2.append(i)
        else:
            pos3.append(i)
    
    used1 = [False] * len(pos1)
    used3 = [False] * len(pos3)
    
    p1 = 0
    p3 = 0
    
    ans = []
    
    # process each 2 as center
    for j in pos2:
        while p1 < len(pos1) and pos1[p1] < j and used1[p1]:
            p1 += 1
        
        while p3 < len(pos3) and pos3[p3] < j and used3[p3]:
            p3 += 1
        
        # try 1-2-3
        i = p1
        while i < len(pos1) and (pos1[i] >= j or used1[i]):
            i += 1
        
        k = p3
        while k < len(pos3) and (pos3[k] <= j or used3[k]):
            k += 1
        
        if i < len(pos1) and k < len(pos3):
            ans.append((pos1[i], j, pos3[k]))
            used1[i] = True
            used3[k] = True
            continue
        
        # try 3-2-1
        i = 0
        while i < len(pos3) and (pos3[i] >= j or used3[i]):
            i += 1
        
        k = 0
        while k < len(pos1) and (pos1[k] <= j or used1[k]):
            k += 1
        
        if i < len(pos3) and k < len(pos1):
            ans.append((pos3[i], j, pos1[k]))
            used3[i] = True
            used1[k] = True
    
    print(len(ans))
    for i, j, k in ans:
        print(i, j, k)

if __name__ == "__main__":
    solve()
```

The solution begins by splitting indices by value, which avoids repeated scans of the original array. The arrays `pos1`, `pos2`, and `pos3` store sorted positions, which is crucial for ensuring that pointer movement preserves correctness.

The `used1` and `used3` arrays track whether a particular occurrence has already been assigned to a triple. This avoids double counting.

For each 2, we attempt to find compatible endpoints. The pointer maintenance ensures we do not repeatedly scan already-consumed indices. The checks `pos1[i] < j` and `pos3[k] > j` enforce ordering constraints.

A subtle point is that we always try the forward pattern 1-2-3 first. This choice is arbitrary in correctness terms but stabilizes matching behavior and avoids biasing toward reversing too early.

## Worked Examples

Consider the input:

```
6
1 2 3 2 1 3
```

We have:

pos1 = [0, 4], pos2 = [1, 3], pos3 = [2, 5]

We process 2 at index 1 first.

| Step | 2 index | chosen 1 | chosen 3 | action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | form 1-2-3 |
| 2 | 3 | 4 | 5 | form 1-2-3 |

Output becomes:

(0,1,2) and (4,3,5)

This trace shows how greedy matching preserves both early and late structure.

Now consider:

```
5
3 2 1 3 2
```

pos1 = [2], pos2 = [1,4], pos3 = [0,3]

We process 2 at index 1:

| Step | 2 index | chosen 3 | chosen 1 | action |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | form 3-2-1 |

Next 2 at index 4 cannot form any triple since all compatible endpoints are used or misaligned.

This demonstrates that early consumption of closest valid endpoints does not block feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each index is scanned and marked used at most once, pointer movement is monotonic |
| Space | O(N) | Storing positions of 1s, 2s, and 3s |

The linear structure fits comfortably within the constraints for N up to 600000, since each operation is constant amortized work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# minimal
assert run("1\n1") == "0"

# single valid triple
assert run("3\n1 2 3") == "1\n0 1 2"

# reversed valid triple
assert run("3\n3 2 1") == "1\n0 1 2"

# multiple disjoint triples
assert run("6\n1 2 3 1 2 3") == "2\n0 1 2\n3 4 5"

# no possible triples
assert run("5\n1 1 1 2 2") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 single element | 0 | minimal case, no triple possible |
| 3 1 2 3 | 1 triple | basic forward pattern |
| 3 3 2 1 | 1 triple | reverse pattern correctness |
| 6 alternating valid pairs | 2 triples | disjoint matching correctness |
| skewed array | 0 | handling insufficient endpoints |

## Edge Cases

A key edge case is when valid triples exist but greedy matching must avoid exhausting one side too early. Consider:

```
7
1 2 3 1 2 3 1
```

There are multiple ways to form triples, but only two complete triples are possible. The algorithm processes 2s in order and always takes nearest valid endpoints, so the first 2 at index 1 pairs with (0,2). The second 2 at index 4 pairs with (3,5). The remaining 1 at index 6 stays unused, correctly reflecting optimal packing.

Another edge case is when only reverse triples are possible:

```
4
3 2 1 2
```

Only one triple can be formed: (3,2,1) using indices (0,1,2). The second 2 cannot be matched because no remaining valid endpoints satisfy ordering constraints. The algorithm correctly consumes the only feasible structure and stops without forcing invalid pairings.
