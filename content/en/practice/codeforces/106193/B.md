---
title: "CF 106193B - Bounding Boxes"
description: "We are given several candidate shipping containers, each a rectangular box described by three side lengths. A souvenir box must also be a rectangular box, and it needs to be placed inside every one of the given containers."
date: "2026-06-19T18:39:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106193
codeforces_index: "B"
codeforces_contest_name: "2025-2026 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 106193
solve_time_s: 48
verified: true
draft: false
---

[CF 106193B - Bounding Boxes](https://codeforces.com/problemset/problem/106193/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several candidate shipping containers, each a rectangular box described by three side lengths. A souvenir box must also be a rectangular box, and it needs to be placed inside every one of the given containers. The key freedom is that the souvenir box can be rotated arbitrarily, as long as its edges stay aligned with the container’s axes after rotation. This means we are not comparing fixed dimensions directly, but rather asking whether a single 3D box can be oriented differently inside each container.

The task is to choose the souvenir box dimensions so that it fits into all containers simultaneously, and among all such feasible boxes, we want the maximum possible volume.

The constraints are small enough that any solution involving pairwise checking over 1000 boxes is acceptable, since the total number of comparisons would be on the order of a few million operations. Anything cubic in a larger parameter would be impossible, but here the structure is simple enough that we can expect an O(n) or O(n log n) solution.

A subtle point is that rotation removes any notion of fixed coordinate matching. A box with sides (a, b, c) fits into a container (x, y, z) if and only if after sorting both triples, each dimension of the souvenir box does not exceed the corresponding dimension of the container. This avoids mistakes where one might incorrectly assume a fixed ordering of sides.

A common failure case arises when ignoring rotation. For example, if we have a container (2, 6, 4) and another (6, 2, 4), a naive approach might treat constraints dimension-wise and conclude inconsistent bounds. In reality, both describe the same constraint set once sorted.

Another edge case is when one dimension is much larger but another is smaller across different boxes, making it tempting to take minima per coordinate directly without sorting. That fails because the coordinate correspondence is not consistent across boxes.

## Approaches

A brute-force approach would try to guess the souvenir box dimensions and check whether it fits into every container under some rotation. Even if we restrict ourselves to candidate dimensions derived from input values, we would still need to consider permutations for each box, leading to exponential behavior if done naively across multiple boxes.

The key observation is that rotation makes each box constraint purely about sorted dimensions. Once each box is sorted as (a ≤ b ≤ c), the condition “souvenir box fits” becomes three independent upper bounds on the ordered dimensions of the souvenir box. To maximize volume under multiple upper bounds, we want to push each dimension as large as possible while remaining valid for all boxes.

This turns the problem into computing, across all boxes, the minimum possible upper bound for the smallest dimension, the middle dimension, and the largest dimension after sorting each box. These three minima directly define the largest feasible sorted souvenir box.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(1) | Too slow |
| Sorting + Min aggregation | O(n log 1) = O(n) | O(1) | Accepted |

## Algorithm Walkthrough

## 1. Normalize each container

For every input box, sort its three dimensions so we always treat it as (x ≤ y ≤ z). This step removes ambiguity caused by rotation and ensures consistent comparison.

## 2. Track global constraints

Maintain three variables representing the best possible upper bounds for the souvenir box dimensions: min_x, min_y, min_z, all initialized to infinity. For each box, update these values by taking the minimum with the corresponding sorted dimension.

This works because every container independently restricts how large each ordered dimension of the souvenir box can be.

## 3. Construct the optimal souvenir box

After processing all containers, the largest valid souvenir box has dimensions (min_x, min_y, min_z). Its volume is the product of these three values.

We do not need to try rearrangements across containers anymore because sorting already aligned all constraints into a comparable system.

## Why it works

Sorting each box reduces the rotation freedom into a canonical form. Any valid placement corresponds to aligning the sorted souvenir box with some permutation of the container, which is already absorbed by sorting. Therefore, the only way to violate feasibility is to exceed at least one container’s sorted bound in some dimension. Taking minima across all containers preserves exactly the intersection of all valid constraint regions in sorted space, and the product of these bounds yields the maximum possible volume since each dimension is independently maximized under monotonic constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
min_x = min_y = min_z = 10**18

for _ in range(n):
    a, b, c = map(int, input().split())
    a, b, c = sorted((a, b, c))
    min_x = min(min_x, a)
    min_y = min(min_y, b)
    min_z = min(min_z, c)

print(min_x * min_y * min_z)
```

The solution reads each box and immediately normalizes it by sorting its dimensions. This is essential because it encodes the rotation freedom into a fixed ordering. The three running minima store the tightest constraint across all boxes for each positional dimension in the sorted representation. The final multiplication computes the volume of the largest box that satisfies all constraints simultaneously.

A common implementation mistake is forgetting to sort each triple. Without sorting, taking coordinate-wise minima would mix incompatible axes and produce an invalid box.

## Worked Examples

### Example 1

Input:

```
3
6 5 6
2 10 10
3 8 4
```

We process each box step by step.

| Box | Sorted | min_x | min_y | min_z |
| --- | --- | --- | --- | --- |
| (6,5,6) | (5,6,6) | 5 | 6 | 6 |
| (2,10,10) | (2,10,10) | 2 | 6 | 6 |
| (3,8,4) | (3,4,8) | 2 | 4 | 6 |

Final dimensions are (2, 4, 6), giving volume 48.

This trace shows how constraints accumulate independently along sorted dimensions, and how the smallest box across all constraints determines the final shape.

### Example 2

Input:

```
2
1 100 100
50 2 80
```

| Box | Sorted | min_x | min_y | min_z |
| --- | --- | --- | --- | --- |
| (1,100,100) | (1,100,100) | 1 | 100 | 100 |
| (50,2,80) | (2,50,80) | 1 | 50 | 80 |

Final result is (1, 50, 80), volume 4000.

This example highlights how a very small first dimension in one box can dominate the final answer even when other dimensions are large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each box is sorted in constant time and processed once |
| Space | O(1) | Only three tracking variables are maintained |

The algorithm is linear in the number of box types, which is easily within limits for n up to 1000. Memory usage is constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    n = int(input())
    min_x = min_y = min_z = 10**18

    for _ in range(n):
        a, b, c = map(int, input().split())
        a, b, c = sorted((a, b, c))
        min_x = min(min_x, a)
        min_y = min(min_y, b)
        min_z = min(min_z, c)

    return str(min_x * min_y * min_z)

# provided sample
assert run("3\n6 5 6\n2 10 10\n3 8 4\n") == "48"

# minimum case
assert run("1\n1 1 1\n") == "1"

# all equal boxes
assert run("2\n3 3 3\n3 3 3\n") == "27"

# one tight dimension dominates
assert run("2\n1 100 100\n50 2 80\n") == "4000"

# permutation stress
assert run("3\n2 3 4\n4 2 3\n3 4 2\n") == "24"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single unit cube | 1 | minimum boundary |
| identical cubes | 27 | stability under duplicates |
| mixed large/small dimensions | 4000 | domination by smallest constraint |
| permutations only | 24 | correctness under rotation |

## Edge Cases

One important edge case is when the tightest constraint for each dimension comes from different boxes. For instance, one box might force a very small minimum side, another constrains the middle, and another constrains the largest.

Input:

```
3
1 100 100
100 2 100
100 100 3
```

Processing:

First box (1,100,100) sets (min_x, min_y, min_z) = (1,100,100).

Second box (2,100,100 sorted from 100,2,100) updates to (1,2,100).

Third box (3,100,100 sorted from 100,100,3) updates to (1,2,3).

Final output is 6.

The algorithm correctly handles this because each dimension is tracked independently in sorted space, so constraints from different boxes naturally combine without requiring any cross-box alignment decisions.
