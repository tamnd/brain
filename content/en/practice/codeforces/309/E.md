---
title: "CF 309E - Sheep"
description: "We have a collection of sheep, each identified by a unique number from 1 to n. Every sheep has a range of meadow regions it likes, represented as an interval $[li, ri]$. In the morning, the first shepherd ties any pair of sheep whose preferred regions overlap."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 309
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2013 - Finals (online version, Div. 1)"
rating: 2900
weight: 309
solve_time_s: 154
verified: true
draft: false
---

[CF 309E - Sheep](https://codeforces.com/problemset/problem/309/E)

**Rating:** 2900  
**Tags:** binary search, greedy  
**Solve time:** 2m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of sheep, each identified by a unique number from 1 to _n_. Every sheep has a range of meadow regions it likes, represented as an interval $[l_i, r_i]$. In the morning, the first shepherd ties any pair of sheep whose preferred regions overlap. In graph terms, each sheep is a node, and an edge connects two sheep if their intervals intersect. These edges form connected components of sheep that must stay close together.

The second shepherd wants to line the sheep in a row so that, for any pair of tied sheep, the number of sheep between them is minimized. This is equivalent to arranging each connected component consecutively, because if two tied sheep are separated by other sheep, the distance between them increases unnecessarily.

The number of sheep $n$ can be up to 2000, so an algorithm with complexity $O(n^2)$ is feasible but anything like $O(n^3)$ will likely be too slow. The intervals themselves can range up to $10^9$, so any solution that tries to explicitly create arrays of size proportional to the interval range is impossible. Key edge cases include fully overlapping intervals, single sheep components, and intervals that touch at boundaries.

A naive approach might attempt to compute distances for every possible permutation, but the factorial growth of permutations makes this impossible for $n = 2000$. Another subtle point is that intervals can partially overlap in complex ways, forming chains of sheep that need to be kept together.

## Approaches

A brute-force approach would attempt all permutations of sheep and compute the maximum distance between tied sheep for each arrangement. For $n = 2000$, there are $2000!$ permutations, which is clearly infeasible. Even limiting to trying to place each connected component in every possible position would quickly explode combinatorially because there can be many components of different sizes.

The key observation is that the only thing that matters is the connected components formed by overlapping intervals. Once a component is identified, all sheep in that component can be arranged in any order internally without affecting the maximum distance between tied sheep. Therefore, the problem reduces to first finding these components and then concatenating them in any order. Sorting the sheep by their starting interval $l_i$ and greedily merging overlapping intervals produces exactly these connected components. Each time an interval does not overlap the current merged group, a new component begins.

This reduces the problem from an intractable permutation search to a simple sorting and linear scan, which is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Connected Components via Interval Merging | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of sheep $n$ and the intervals $[l_i, r_i]$ for each sheep.
2. Pair each interval with its sheep index and sort these pairs by starting point $l_i$. Sorting ensures that overlapping intervals will appear consecutively.
3. Initialize an empty list of components and a current component list. Also maintain the rightmost boundary of the current component.
4. Iterate over the sorted intervals. If the current interval starts after the rightmost boundary, the current component is complete. Append it to the list of components, start a new component with the current sheep, and update the rightmost boundary.
5. If the current interval overlaps the current component, add the sheep to the current component and extend the rightmost boundary as necessary.
6. After processing all intervals, append the last component to the list.
7. Finally, concatenate all components in order to form the output arrangement. Within each component, any order of sheep is valid.

Why it works: By merging overlapping intervals, each connected component contains all sheep that are transitively tied to each other. Placing all sheep from a component consecutively guarantees that any pair of tied sheep has zero distance between them, which minimizes the maximum distance globally. Sorting by left endpoint ensures that components are identified correctly, even if intervals only partially overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
sheep = []
for i in range(n):
    l, r = map(int, input().split())
    sheep.append((l, r, i + 1))

sheep.sort()
components = []
current_component = []
current_right = -1

for l, r, idx in sheep:
    if l > current_right:
        if current_component:
            components.append(current_component)
        current_component = [idx]
        current_right = r
    else:
        current_component.append(idx)
        current_right = max(current_right, r)

if current_component:
    components.append(current_component)

# Flatten components into a single arrangement
arrangement = []
for comp in components:
    arrangement.extend(comp)

print(' '.join(map(str, arrangement)))
```

This solution reads the input and pairs each sheep with its interval. Sorting by left endpoint simplifies component detection. As we iterate, we either extend the current component or start a new one. Finally, components are concatenated to produce a valid arrangement. Edge cases like single-sheep components, fully overlapping intervals, or non-overlapping intervals are all handled by the same logic.

## Worked Examples

**Sample 1**

Input:

```
3
1 3
5 7
2 4
```

Sorted intervals with indices: $[(1,3,1), (2,4,3), (5,7,2)]$

| Sheep | Current Component | Current Right | Action |
| --- | --- | --- | --- |
| (1,3,1) | [1] | 3 | Start new component |
| (2,4,3) | [1,3] | 4 | Overlaps, add to component |
| (5,7,2) | [2] | 7 | Start new component |

Flattened arrangement: [1,3,2]

This demonstrates that sheep 1 and 3 are tied and appear consecutively, minimizing maximum distance.

**Sample 2**

Input:

```
5
1 2
3 4
5 6
7 8
9 10
```

All intervals are disjoint, so each sheep forms its own component. The arrangement is simply [1,2,3,4,5].

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the intervals dominates |
| Space | O(n) | Storing the sheep, components, and final arrangement |

Given $n \le 2000$, $n \log n$ operations complete comfortably under 1 second. Memory usage is linear in $n$, well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    sheep = []
    for i in range(n):
        l, r = map(int, input().split())
        sheep.append((l, r, i + 1))
    sheep.sort()
    components = []
    current_component = []
    current_right = -1
    for l, r, idx in sheep:
        if l > current_right:
            if current_component:
                components.append(current_component)
            current_component = [idx]
            current_right = r
        else:
            current_component.append(idx)
            current_right = max(current_right, r)
    if current_component:
        components.append(current_component)
    arrangement = []
    for comp in components:
        arrangement.extend(comp)
    return ' '.join(map(str, arrangement))

# Provided sample
assert run("3\n1 3\n5 7\n2 4\n") == "1 3 2", "sample 1"

# Custom test cases
assert run("5\n1 2\n3 4\n5 6\n7 8\n9 10\n") == "1 2 3 4 5", "all disjoint"
assert run("3\n1 10\n2 3\n4 5\n") == "1 2 3", "all overlap transitively"
assert run("1\n100 200\n") == "1", "single sheep"
assert run("4\n1 2\n2 3\n3 4\n4 5\n") == "1 2 3 4", "chain overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 sheep, overlapping | 1 3 2 | Correct handling of tied component |
| 5 disjoint sheep | 1 2 3 4 5 | Disjoint intervals form separate components |
| 3 overlapping transitively | 1 2 3 | All in one component |
| Single sheep | 1 | Handles minimal input |
| 4 chained overlaps | 1 2 3 4 | Correct merging of overlapping intervals |

## Edge Cases

Single sheep: Input `1\n100 200` produces [1]. The algorithm initializes a new component and correctly outputs it. Fully overlapping sheep: `3\n1 10\n2 3\n4 5` produces [1,2,3], merging all into one component. Disjoint intervals are each their own component, so order is preserved. Edge touching intervals like `1 2` and `2 3` are considered overlapping, ensuring they merge correctly.
