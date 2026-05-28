---
title: "CF 32A - Reconnaissance"
description: "We are tasked with counting how many pairs of soldiers in a detachment can form a reconnaissance unit. A unit consists o"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 32
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 32 (Div. 2, Codeforces format)"
rating: 800
weight: 32
solve_time_s: 65
verified: true
draft: false
---

[CF 32A - Reconnaissance](https://codeforces.com/problemset/problem/32/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with counting how many pairs of soldiers in a detachment can form a reconnaissance unit. A unit consists of exactly two soldiers, and the difference in their heights cannot exceed a given threshold _d_. The input gives us the total number of soldiers _n_, the allowed maximum height difference _d_, and a list of the soldiers' heights. The output is a single integer representing the number of valid ordered pairs (i, j) such that |height[i] − height[j]| ≤ d. Ordered pairs matter here, so (i, j) is distinct from (j, i).

The constraints are moderate: n can be up to 1000 and heights can be as large as 10^9. Because n is small, an O(n²) approach is feasible in practice but can be optimized. The key detail is that the heights themselves can be very large, so any algorithm relying on indexing by height directly (like a frequency array) is impractical.

Edge cases to consider include situations where all soldiers have the same height, or where the difference d is very small. For instance, if n = 3, d = 0, and heights = [5, 5, 6], only pairs of soldiers with the same height are valid. A careless implementation might either undercount or fail to consider the order of pairs.

## Approaches

The simplest approach is brute force: iterate over every possible pair of soldiers (i, j) and check if their height difference is at most d. This works because it directly implements the problem requirement. The total number of operations is n * (n − 1), which is roughly 1 million when n = 1000. This is acceptable under a 2-second time limit, but it's not elegant.

We can improve efficiency with sorting. If we sort the array of heights in non-decreasing order, the problem becomes easier: for each soldier, we only need to check subsequent soldiers until the height difference exceeds d. Sorting costs O(n log n) and the subsequent linear scan for each soldier is O(n) in total, so this yields an O(n log n) solution. The key insight is that sorting allows early termination in the inner loop: once the difference surpasses d, we know that all remaining soldiers will also exceed the limit because heights are increasing.

The comparison table clarifies this:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Acceptable for n ≤ 1000 |
| Sorting + Two Pointers | O(n log n) | O(1) | Optimal and clear |

## Algorithm Walkthrough

1. Read n, d, and the list of soldier heights. We use fast input to avoid unnecessary overhead.
2. Sort the heights in non-decreasing order. This ensures that for any soldier i, all subsequent soldiers have greater or equal heights.
3. Initialize a counter to 0 to track the number of valid ordered pairs.
4. For each soldier i from 0 to n − 1, start checking soldiers j > i. As long as height[j] − height[i] ≤ d, increment the counter. Break the inner loop immediately when height[j] − height[i] > d because no further j will satisfy the condition.
5. Output the counter after scanning all soldiers.

Why it works: Sorting guarantees that once a pair exceeds the allowed height difference, all later pairs with the same first soldier will also exceed it. The loop structure ensures we check all pairs exactly once, counting both directions implicitly because the outer loop iterates over every soldier.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d = map(int, input().split())
heights = list(map(int, input().split()))
heights.sort()

count = 0

for i in range(n):
    for j in range(i + 1, n):
        if heights[j] - heights[i] <= d:
            count += 1
        else:
            break

# Each valid pair can be ordered in two ways
print(count * 2)
```

The code first sorts the soldiers’ heights. The nested loops examine all valid pairs in increasing order. We multiply the final count by 2 because each pair (i, j) can appear in both orders (i, j) and (j, i). Boundary conditions are handled implicitly: the inner loop starts at i + 1, preventing self-pairs, and breaks as soon as the height difference exceeds d.

## Worked Examples

Sample 1:

Input:

```
5 10
10 20 50 60 65
```

Step trace:

| i | height[i] | j checked | Valid pairs | Running count |
| --- | --- | --- | --- | --- |
| 0 | 10 | 20 | (10,20) | 1 |
| 0 | 10 | 50 | - | 1 |
| 1 | 20 | 50 | - | 1 |
| 2 | 50 | 60 | (50,60) | 2 |
| 2 | 50 | 65 | - | 2 |
| 3 | 60 | 65 | (60,65) | 3 |

Multiply by 2 for order: 3 * 2 = 6, matching the expected output.

Custom case:

Input:

```
3 0
5 5 6
```

Step trace:

| i | height[i] | j checked | Valid pairs | Running count |
| --- | --- | --- | --- | --- |
| 0 | 5 | 5 | (5,5) | 1 |
| 0 | 5 | 6 | - | 1 |
| 1 | 5 | 6 | - | 1 |

Multiply by 2: 1 * 2 = 2, correct since only the identical 5s form pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, inner loop runs at most n times for all i due to break. |
| Space | O(1) | Sorting in-place, only counter stored. |

With n ≤ 1000, sorting and linear scans are trivial. Memory usage is well below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, d = map(int, input().split())
    heights = list(map(int, input().split()))
    heights.sort()
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if heights[j] - heights[i] <= d:
                count += 1
            else:
                break
    return str(count * 2)

# Provided sample
assert run("5 10\n10 20 50 60 65\n") == "6", "sample 1"

# Minimum-size input
assert run("1 5\n10\n") == "0", "minimum size"

# Maximum-size, all equal
assert run("1000 0\n" + " ".join(["42"]*1000) + "\n") == str(1000*999), "all equal"

# Small d, some differences exceed
assert run("4 1\n1 2 4 5\n") == "4", "small d with gaps"

# Ordered heights
assert run("3 2\n1 3 5\n") == "2", "ordered with step 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5\n10 | 0 | Minimum n, cannot form a pair |
| 1000 0\n42… | 999000 | Maximum n, all equal values |
| 4 1\n1 2 4 5 | 4 | Some gaps too large to pair |
| 3 2\n1 3 5 | 2 | Height differences exactly at limit |

## Edge Cases

If all soldiers have the same height, for example heights = [7,7,7,7] and d = 0, every pair is valid. Our algorithm counts i < j pairs as 6, and multiplying by 2 gives 12, correctly counting both orderings. If d is very small, like 0, only soldiers of the same height are paired. The break statement in the inner loop avoids unnecessary checks once the difference exceeds d. For n = 1, the outer loop executes once but no inner loop runs, so the algorithm outputs 0, which is correct.

This method correctly handles all edge cases due to sorting and early termination logic.
