---
title: "CF 920A - Water The Garden"
description: "We are given a linear garden with n consecutive beds and a subset of these beds containing water taps. Each tap, once turned on, waters the bed it occupies immediately, and in each subsequent second it extends its coverage by one bed in both directions."
date: "2026-06-12T09:46:32+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 920
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 37 (Rated for Div. 2)"
rating: 1000
weight: 920
solve_time_s: 128
verified: true
draft: false
---

[CF 920A - Water The Garden](https://codeforces.com/problemset/problem/920/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear garden with _n_ consecutive beds and a subset of these beds containing water taps. Each tap, once turned on, waters the bed it occupies immediately, and in each subsequent second it extends its coverage by one bed in both directions. Our goal is to determine the minimum number of seconds needed for all beds to be watered if all taps are turned on simultaneously.

The input specifies multiple test cases, each giving the number of beds _n_, the number of taps _k_, and the positions of the taps. The output for each test case is a single integer: the earliest second when every bed is watered.

The constraints are small: _n_ is at most 200, and the sum of _n_ over all test cases does not exceed 200. This means any solution that is roughly O(n²) per test case will run comfortably, so we can afford to simulate or process each bed individually if needed.

Non-obvious edge cases include gardens where taps are clustered at one end or when multiple taps overlap heavily. For example, if _n = 5_ and the taps are at positions 1 and 2, the leftmost bed is watered instantly, but the rightmost bed is farther away, and a naive approach that only looks at the nearest tap may underestimate the required time. Another subtle scenario occurs when there is only one tap at one end of the garden; the algorithm must account for the farthest distance from any tap to a bed, not just the nearest.

## Approaches

A brute-force approach is to simulate the watering process second by second. We could maintain an array representing the garden beds, and for each second, expand the watering range of every tap. After each second, we check whether all beds are watered. This is correct, but inefficient: for the worst-case garden of 200 beds and a single tap, this simulation may perform up to 200 operations per second for 200 seconds, resulting in roughly 40,000 operations. While acceptable given the problem limits, it is unnecessarily verbose.

The optimal approach stems from observing that for any bed, the minimum time to be watered is determined by the closest tap. If we sort the taps and examine the distance from each bed to its nearest tap, the maximum of these minimum distances over all beds gives the answer. This works because water spreads symmetrically from each tap at a rate of one bed per second, so the farthest bed from all taps dictates the total time needed.

The brute-force works because it literally simulates the process, but it fails in elegance and clarity. The observation that the required time is simply the maximum distance from a bed to the nearest tap lets us reduce the problem to a straightforward linear scan after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted but verbose |
| Optimal | O(n log n) | O(n) | Clean, accepted |

## Algorithm Walkthrough

1. For each test case, read the number of beds _n_, the number of taps _k_, and the list of tap positions. Sorting the tap positions simplifies distance calculations.
2. Initialize a variable to track the maximum time required for a bed to be watered. This represents the answer.
3. Iterate over every bed from 1 to _n_. For each bed, compute the absolute distance to each tap, then select the minimum distance. This gives the time needed to water this specific bed.
4. Update the maximum time if the current bed's minimum distance is greater than the previous maximum. After scanning all beds, the maximum time represents the earliest second when the entire garden is watered.
5. Print the maximum time for the current test case.

Why it works: The algorithm ensures that every bed is accounted for. The water from multiple taps does not reduce the time for a bed below the distance from the nearest tap, and the farthest bed governs the total watering time. Sorting is optional for this small input size, but it makes nearest-tap calculation conceptually simpler. The invariant is that at every iteration, `max_time` holds the longest minimum distance encountered so far.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    taps = list(map(int, input().split()))
    max_time = 0
    for bed in range(1, n + 1):
        min_dist = min(abs(bed - tap) for tap in taps)
        max_time = max(max_time, min_dist)
    print(max_time + 1)
```

The solution first reads the number of test cases. For each test case, it reads the garden size and tap positions. The loop over beds calculates the distance to each tap, picks the closest, and tracks the maximum distance. We add one because the first second waters the tap's own bed. The careful handling of indices ensures we do not go out of bounds and respects 1-based bed numbering.

## Worked Examples

For the input:

```
5 1
3
```

| Bed | Distances to taps | Min Distance | Max Time So Far |
| --- | --- | --- | --- |
| 1 | [2] | 2 | 2 |
| 2 | [1] | 1 | 2 |
| 3 | [0] | 0 | 2 |
| 4 | [1] | 1 | 2 |
| 5 | [2] | 2 | 2 |

The maximum minimum distance is 2, so total seconds needed is 3. This matches the expected output.

For the input:

```
3 3
1 2 3
```

| Bed | Distances to taps | Min Distance | Max Time So Far |
| --- | --- | --- | --- |
| 1 | [0,1,2] | 0 | 0 |
| 2 | [1,0,1] | 0 | 0 |
| 3 | [2,1,0] | 0 | 0 |

Maximum minimum distance is 0, total seconds needed is 1.

These traces demonstrate that the algorithm correctly identifies the farthest bed from any tap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | For each bed, we compute distances to all k taps. With n ≤ 200 and k ≤ n, this is acceptable. |
| Space | O(n + k) | Arrays for taps and simple scalar tracking of max time. |

Given n and k are small and sum over all test cases ≤ 200, this solution runs well within the 1-second limit and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution function inline
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        taps = list(map(int, input().split()))
        max_time = 0
        for bed in range(1, n + 1):
            min_dist = min(abs(bed - tap) for tap in taps)
            max_time = max(max_time, min_dist)
        print(max_time + 1)
    return output.getvalue().strip()

# provided samples
assert run("3\n5 1\n3\n3 3\n1 2 3\n4 1\n1") == "3\n1\n4", "sample 1"

# custom cases
assert run("1\n1 1\n1") == "1", "single bed with tap"
assert run("1\n5 2\n1 5") == "3", "taps at ends"
assert run("1\n6 1\n3") == "4", "single tap in middle"
assert run("1\n6 3\n1 3 6") == "2", "multiple taps uneven"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | single bed with tap |
| 5 2 1 5 | 3 | taps at opposite ends, farthest bed coverage |
| 6 1 3 | 4 | single tap in the middle, farthest distance computation |
| 6 3 1 3 6 | 2 | multiple taps, ensures algorithm picks nearest tap |

## Edge Cases

For a single-bed garden with a tap at that bed, input `1 1\n1`, the algorithm computes min distance 0 for bed 1, adds 1, giving total seconds 1. For a garden where taps occupy only the ends, `5 2\n1 5`, beds 2 and 4 have a minimum distance of 1 to the nearest tap, bed 3 has distance 2. Maximum minimum distance is 2, total seconds is 3. These examples confirm the approach handles boundaries and single-tap coverage correctly.
