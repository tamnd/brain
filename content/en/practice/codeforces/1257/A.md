---
title: "CF 1257A - Two Rival Students"
description: "We have a line of students numbered from 1 to n. Among them, two students are rivals, located at positions a and b. The gym teacher wants to maximize the distance between these two students, where distance is simply the absolute difference of their positions."
date: "2026-06-11T20:47:45+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1257
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 76 (Rated for Div. 2)"
rating: 800
weight: 1257
solve_time_s: 121
verified: true
draft: false
---

[CF 1257A - Two Rival Students](https://codeforces.com/problemset/problem/1257/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of students numbered from 1 to n. Among them, two students are rivals, located at positions a and b. The gym teacher wants to maximize the distance between these two students, where distance is simply the absolute difference of their positions. We are allowed to perform at most x swaps, and each swap exchanges two adjacent students. The task is to determine the largest distance achievable between the rivals after these swaps.

Looking at the constraints, n is at most 100, x is at most 100, and there are up to 100 test cases. This is small enough that even an O(n) or O(1) per test case solution is extremely fast. There is no need for complex data structures or optimization tricks. However, we still need to reason carefully about which moves actually increase the distance.

A subtle point is that swaps only move students by one position at a time. So we cannot instantly place a student at an arbitrary position; the maximum increase in distance is limited by the number of available swaps. For example, if n = 5, x = 1, a = 3, b = 2, a naive approach that just places the students at positions 1 and 5 would be impossible because only one swap is allowed. We must account for the swap limit when computing the maximum distance.

Another edge case occurs when x = 0. Then no movement is possible, and the distance is just the current absolute difference |a - b|. Similarly, if the students are already at the ends and x is large, we can never increase the distance beyond n - 1 because that is the physical maximum distance in a line.

## Approaches

The brute-force approach is to simulate all possible sequences of swaps. For each test case, we could try moving one student left or right and the other student right or left, trying every combination of swap sequences up to x swaps. After each sequence, we compute the distance. This approach is correct but extremely inefficient: the number of sequences grows exponentially with x. For x = 100, this is clearly impractical.

The key observation is that we do not care about the exact intermediate positions of students. We only care about the distance between the two rivals, and swaps move students by one step per operation. Therefore, the maximum distance we can achieve is limited by two factors: the number of available swaps x and the maximum physical distance in the line, which is n - 1. If the initial distance between a and b is d = |a - b|, we can increase it by at most x, but we cannot exceed n - 1. This gives a simple formula for the optimal solution:

```
max_distance = min(n - 1, |a - b| + x)
```

This works because every swap can increase the distance by at most 1. We only need to consider moving the students toward opposite ends of the line. There is no need to simulate individual swaps, making the solution O(1) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^x) | O(n) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. Each test case consists of four integers: n, x, a, b.
2. For each test case, compute the current distance between the rivals as `d = abs(a - b)`.
3. Compute the maximum distance achievable after swaps. Each swap can increase the distance by at most 1, so add x to the current distance: `new_distance = d + x`.
4. The absolute maximum distance in a line of length n is n - 1. If `new_distance` exceeds this, cap it: `max_distance = min(new_distance, n - 1)`.
5. Output `max_distance` for each test case.

Why it works: The invariant is that each swap increases the distance between the rivals by at most 1. Starting from the initial positions, the maximum achievable distance is exactly the initial distance plus the number of swaps, bounded by the line length. This guarantees that the formula captures the optimal outcome in every scenario.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x, a, b = map(int, input().split())
    d = abs(a - b)
    max_distance = min(n - 1, d + x)
    print(max_distance)
```

In this solution, we first read the number of test cases. Then for each case, we calculate the absolute distance `d` between the two rivals. We add the number of swaps `x` and cap the result with `n - 1` to respect the line length. Printing the result directly ensures O(1) work per test case. Careful attention is given to using `abs(a - b)` and `min(...)` to handle all edge cases correctly.

## Worked Examples

**Sample 1:**

```
n = 5, x = 1, a = 3, b = 2
```

| Step | d | d + x | max_distance |
| --- | --- | --- | --- |
| Initial | 1 | 2 | 2 |

Explanation: The initial distance is 1. One swap increases it to 2, which is less than n - 1 = 4. The algorithm correctly outputs 2.

**Sample 2:**

```
n = 100, x = 33, a = 100, b = 1
```

| Step | d | d + x | max_distance |
| --- | --- | --- | --- |
| Initial | 99 | 132 | 99 |

Explanation: The initial distance is 99. Adding swaps gives 132, but the physical maximum is n - 1 = 99. The algorithm caps it at 99.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only absolute difference, addition, and min calculation are needed |
| Space | O(1) | No additional data structures are used, only a few integers |

Given t ≤ 100, n ≤ 100, and x ≤ 100, the algorithm runs in negligible time, comfortably within the 1-second limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, x, a, b = map(int, input().split())
        d = abs(a - b)
        max_distance = min(n - 1, d + x)
        print(max_distance)
    return output.getvalue().strip()

# Provided samples
assert run("3\n5 1 3 2\n100 33 100 1\n6 0 2 3\n") == "2\n99\n1"

# Custom cases
assert run("1\n2 0 1 2\n") == "1", "minimum size input"
assert run("1\n10 5 4 5\n") == "6", "moderate swaps increasing distance"
assert run("1\n10 100 1 2\n") == "9", "swaps exceed maximum distance"
assert run("1\n7 3 3 7\n") == "6", "rivals initially at distance 4, increase by swaps"
assert run("1\n100 0 50 51\n") == "1", "zero swaps, distance unchanged"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 1 2 | 1 | Minimum size array, zero swaps |
| 10 5 4 5 | 6 | Swaps increase distance within bounds |
| 10 100 1 2 | 9 | Swaps exceed maximum distance, capped at n - 1 |
| 7 3 3 7 | 6 | Rivals initially distant, swaps applied |
| 100 0 50 51 | 1 | Zero swaps, distance remains same |

## Edge Cases

For the case where x = 0, the algorithm correctly returns the initial distance. For example, `n = 6, x = 0, a = 2, b = 3` gives `abs(2-3) = 1`. No swaps can be performed, so the distance cannot increase. The min function does not alter the value since 1 < n - 1 = 5.

For the case where initial positions are at the extremes, `n = 100, x = 50, a = 1, b = 100`, the distance is already maximal at 99. Adding x gives 149, but the min function caps it at 99. This demonstrates the algorithm respects physical constraints of the line.

For a minimal line, `n = 2, x = 0, a = 1, b = 2`, distance is 1. No swaps are possible, and distance cannot exceed n - 1 = 1. The output matches expectations.

All these checks show the formula `min(n - 1, abs(a - b) + x)` correctly handles edge cases without special conditional logic.
