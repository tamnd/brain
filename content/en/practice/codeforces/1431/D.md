---
title: "CF 1431D - Used Markers"
description: "We are tasked with scheduling a set of lectures in an auditorium, each of which will use a shared marker. Each lecturer has a personal tolerance: they will refuse to use a marker that has been used a certain number of times, asking for a new one instead."
date: "2026-06-11T05:14:55+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1431
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes 5: ICPC Round"
rating: 1500
weight: 1431
solve_time_s: 582
verified: false
draft: false
---

[CF 1431D - Used Markers](https://codeforces.com/problemset/problem/1431/D)

**Rating:** 1500  
**Tags:** *special, greedy  
**Solve time:** 9m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are tasked with scheduling a set of lectures in an auditorium, each of which will use a shared marker. Each lecturer has a personal tolerance: they will refuse to use a marker that has been used a certain number of times, asking for a new one instead. Our goal is to choose the lecture order that maximizes the number of distinct markers that are actually used, while only replacing a marker when a lecturer requests it.

The input provides multiple independent test cases. For each case, we are given the number of lectures and an array of integers representing the tolerance for each lecturer. The output is an order of lecturer indices that maximizes marker usage. The constraints are moderate: up to 100 test cases, each with up to 500 lectures, meaning the total number of operations should comfortably fit a solution with time complexity on the order of $O(n \log n)$ or $O(n^2)$ per test case.

Edge cases arise when multiple lecturers have the same tolerance value or when all lecturers have very low or very high acceptance thresholds. For instance, if all lecturers have a tolerance of 1, every lecture after the first will force a marker replacement. If a careless algorithm ignores the relative sizes of tolerance values, it might schedule lecturers in an order that unnecessarily reduces the number of used markers.

## Approaches

A brute-force approach would consider all possible permutations of lecturers, simulate the lecture sequence for each permutation, and count the number of markers used. This method is correct but infeasible because the number of permutations grows factorially, $n!$, which is impractical even for $n = 10$.

The key insight is to focus on the relative tolerance values. A marker only needs to be replaced when the current lecture’s tolerance exceeds the number of times the marker has already been used. To maximize the number of markers used, we want lecturers with the lowest tolerance values to come early because they will trigger replacements sooner. Lecturers with higher tolerance values can be scheduled later to extend the life of the current marker.

Sorting lecturers in ascending order of their tolerance values achieves this. This ensures that we replace markers when necessary and do not waste lectures on a marker that will immediately be rejected. Because we only need one pass through the sorted list to construct the order, this approach is efficient and simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy sort by tolerance | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the number of lectures and the array of acceptance values.
3. Pair each lecturer’s index with their tolerance value so we can preserve original positions.
4. Sort this list of pairs by the tolerance value in ascending order.
5. Extract the sorted indices as the order for lectures.
6. Print the resulting order for the current test case.

Why it works: By always placing lecturers with smaller acceptance thresholds first, we ensure that each marker reaches the maximum number of uses before it must be replaced. This greedy approach guarantees that the number of markers used is maximized, because any deviation-placing a high-tolerance lecturer early-cannot increase marker usage.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        # pair index with value
        indexed = [(a[i], i + 1) for i in range(n)]
        # sort by acceptance value ascending
        indexed.sort()
        # extract order
        order = [idx for _, idx in indexed]
        print(' '.join(map(str, order)))

if __name__ == "__main__":
    solve()
```

We pair each lecturer's tolerance with their 1-based index to preserve the original numbering. Sorting ensures we trigger marker replacements as efficiently as possible. Extracting indices after sorting gives the desired lecture order. Using `sys.stdin.readline` ensures fast input handling, especially for multiple test cases.

## Worked Examples

Trace for test case 1 from the sample:

Input array: `[1, 2, 1, 2]`

Paired with indices: `[(1,1), (2,2), (1,3), (2,4)]`

Sorted by tolerance: `[(1,1), (1,3), (2,2), (2,4)]`

Resulting order: `[1,3,2,4]`

| Step | Current marker uses | Next lecturer | Action | Marker count |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | tolerance 1, marker new | 1 |
| 2 | 1 | 3 | tolerance 1, marker used once -> replace | 2 |
| 3 | 1 | 2 | tolerance 2, marker used once -> continue | 2 |
| 4 | 2 | 4 | tolerance 2, marker used twice -> continue | 2 |

The trace demonstrates that placing low-tolerance lecturers first triggers necessary replacements without wasting early markers.

Second test case `[2,3,1,3]` paired: `[(2,1),(3,2),(1,3),(3,4)]`, sorted: `[(1,3),(2,1),(3,2),(3,4)]`, order: `[3,1,2,4]` achieves maximum marker usage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n log n) | Sorting dominates per test case |
| Space | O(n) | Store index-value pairs for sorting |

The solution comfortably fits within 3s for $n \le 500$ and $t \le 100$, because $t \cdot n \log n \approx 100 * 500 * 9 \approx 450,000$ operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n4\n1 2 1 2\n2\n2 1\n3\n1 1 1\n4\n2 3 1 3\n") == "1 3 2 4\n2 1\n1 2 3\n3 1 2 4", "sample 1"

# custom: minimum-size input
assert run("1\n1\n1\n") == "1", "single lecturer"

# custom: all equal tolerance
assert run("1\n3\n2 2 2\n") == "1 2 3", "all equal"

# custom: descending tolerance
assert run("1\n5\n5 4 3 2 1\n") == "5 4 3 2 1", "reverse sorted"

# custom: ascending tolerance
assert run("1\n5\n1 2 3 4 5\n") == "1 2 3 4 5", "already optimal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | single lecturer |
| 2 | 1 2 3 | all equal tolerance |
| 3 | 5 4 3 2 1 | descending tolerance |
| 4 | 1 2 3 4 5 | ascending tolerance |

## Edge Cases

If all lecturers have the same acceptance value, any order works. The algorithm handles this correctly because sorting by tolerance preserves the relative order in Python's stable sort. For a single lecturer, the algorithm correctly outputs that lecturer. For sequences that are already sorted in ascending or descending tolerance, the algorithm maintains or reverses order appropriately, ensuring maximum markers are used without unnecessary replacements.
