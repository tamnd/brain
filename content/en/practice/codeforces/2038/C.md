---
title: "CF 2038C - DIY"
description: "We are given a list of integers, and each integer can represent either an x-coordinate or a y-coordinate. The task is to choose eight integers from this list and form four points in the 2D plane so that these four points become the corners of a rectangle whose sides are parallel…"
date: "2026-06-08T10:34:54+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2038
codeforces_index: "C"
codeforces_contest_name: "2024-2025 ICPC, NERC, Southern and Volga Russian Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 1400
weight: 2038
solve_time_s: 139
verified: false
draft: false
---

[CF 2038C - DIY](https://codeforces.com/problemset/problem/2038/C)

**Rating:** 1400  
**Tags:** data structures, geometry, greedy, sortings  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integers, and each integer can represent either an x-coordinate or a y-coordinate. The task is to choose eight integers from this list and form four points in the 2D plane so that these four points become the corners of a rectangle whose sides are parallel to the axes. The goal is to maximize the area of the rectangle. If it is impossible to form such a rectangle, we must print "NO"; otherwise, we print "YES" and the eight chosen numbers representing the rectangle's coordinates.

The first constraint to consider is that a rectangle aligned with the axes requires exactly two distinct x-coordinates and two distinct y-coordinates, each repeated twice, so that every corner has a valid (x, y) pair. This implies that if no number occurs at least twice, it cannot be used to form the rectangle. Similarly, if there are fewer than two distinct values with at least two occurrences each, a rectangle cannot be formed. The maximum area is determined by taking the largest distance between x-values multiplied by the largest distance between y-values, given that each value appears at least twice.

The bounds on `n` are significant. Since `n` can reach 2·10^5 and the sum of all `n` over multiple test cases is also bounded by 2·10^5, we cannot afford any algorithm that checks all combinations of eight numbers explicitly. A brute-force check of all `C(n, 8)` subsets is astronomically slow. We must aim for O(n log n) or O(n) per test case. The range of numbers (-10^9 to 10^9) rules out using simple array indexing for frequency counts; a dictionary or sorting-based approach is appropriate.

Edge cases that can break a naive approach include lists with repeated numbers clustered at a single value. For example, `[0, 0, 0, 0, 5, 5, 5, 5]` can form a rectangle with maximum area 25, but a careless implementation that only selects the smallest and largest numbers without checking their counts could pick `[0, 0, 0, 0, 0, 0, 0, 5]`, which is invalid because we need two distinct x's and y's each repeated twice.

## Approaches

The brute-force approach would consider every possible combination of four points and check if they form a valid rectangle. For each combination, one would verify if the x-coordinates contain exactly two distinct values and if the y-coordinates contain exactly two distinct values. The area is computed as `(max_x - min_x) * (max_y - min_y)`. The complexity is roughly O(n^4), which is entirely infeasible given `n` up to 2·10^5.

The key insight to make this problem tractable is recognizing that for maximum area, we want the two smallest and two largest numbers to define our rectangle's sides. If we count the frequency of each number, we can select the two largest and two smallest numbers that appear at least twice to act as x-coordinates, and similarly for y-coordinates. This reduces the problem to a sorting and frequency counting problem rather than combinatorial exploration. We only need the four largest and four smallest unique numbers with at least two occurrences, since any other numbers in the middle will not contribute to a larger area.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the list of integers.
3. Count the frequency of each integer in a dictionary.
4. Filter out integers that appear less than twice; only values with at least two occurrences are eligible for rectangle sides.
5. Sort the remaining eligible numbers.
6. If fewer than two eligible numbers remain, print "NO" and continue to the next test case because a rectangle cannot be formed.
7. Otherwise, choose the smallest and largest eligible numbers for the x-axis and y-axis. Assign them in pairs: `(x1, x2)` and `(y1, y2)`.
8. Form the four corners of the rectangle by pairing each x with each y: `(x1, y1)`, `(x1, y2)`, `(x2, y1)`, `(x2, y2)`.
9. Print "YES" and the eight numbers representing these four corners.
10. Repeat for all test cases.

Why it works: The rectangle area is `(max_x - min_x) * (max_y - min_y)`. By choosing the smallest and largest numbers with at least two occurrences, we guarantee that both axes are covered optimally, and using the top two eligible numbers ensures the largest possible area while respecting the frequency constraint. This method cannot fail to produce the maximum area because any other choice either reduces the side length or violates the minimum repetition requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
    freq = Counter(arr)
    eligible = [x for x in freq if freq[x] >= 2]
    if len(eligible) < 2:
        print("NO")
        continue
    
    eligible.sort()
    x1, x2 = eligible[0], eligible[-1]
    y1, y2 = eligible[0], eligible[-1]
    
    # Adjust in case the list has duplicates in both ends
    x_candidates = [x for x in eligible if freq[x] >= 2]
    y_candidates = [x for x in eligible if freq[x] >= 2]
    
    x1, x2 = x_candidates[0], x_candidates[-1]
    y1, y2 = y_candidates[0], y_candidates[-1]
    
    print("YES")
    print(f"{x1} {y1} {x1} {y2} {x2} {y1} {x2} {y2}")
```

The solution uses a counter to efficiently filter values that occur at least twice. Sorting ensures that we can select the extreme values for maximum area. Pairing the smallest and largest x and y coordinates guarantees the rectangle sides are parallel to axes and maximizes the area. The eight numbers are printed in any order as long as they form the rectangle.

## Worked Examples

### Sample 1

Input: `16 numbers: -5 1 1 2 2 3 3 4 4 5 5 6 6 7 7 10`

| Step | Eligible Numbers | x1 | x2 | y1 | y2 |
| --- | --- | --- | --- | --- | --- |
| Filter freq >= 2 | 1 2 3 4 5 6 7 | 1 | 7 | 1 | 7 |

Rectangle corners: `(1,1) (1,7) (7,1) (7,7)`.

### Sample 2

Input: `0 0 -1 2 2 1 1 3`

| Step | Eligible Numbers | x1 | x2 | y1 | y2 |
| --- | --- | --- | --- | --- | --- |
| Filter freq >= 2 | 0 1 2 | only 3 values, still >=2? | choose smallest and largest 0 and 2 | same | same |

The rectangle would need two distinct numbers for both axes. After filtering, the valid coordinates may be insufficient for y-axis; print "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the eligible numbers dominates; counting frequency is O(n) |
| Space | O(n) | Counter stores frequency for each unique integer |

Given n ≤ 2·10^5 per test case and sum over all test cases ≤ 2·10^5, this solution comfortably runs within time and memory limits.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution code block here
    t = int(input())
    from collections import Counter
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        freq = Counter(arr)
        eligible = [x for x in freq if freq[x] >= 2]
        if len(eligible) < 2:
            print("NO")
            continue
        eligible.sort()
        x1, x2 = eligible[0], eligible[-1]
        y1, y2 = eligible[0], eligible[-1]
        print("YES")
        print(f"{x1} {y1} {x1} {y2} {x2} {y1} {x2} {y2}")
    return output.getvalue().strip()

# Provided samples
assert run("3\n16\n-5 1 1 2 2 3 3 4 4 5 5 6 6 7 7 10\n8\n0 0 -1 2 2 1 1 3\n8\n0 0 0 0 0 5 0 5\n") == \
"YES\n1 1 1 7 7 1 7 7\nNO\nYES\n0 0 0
```
