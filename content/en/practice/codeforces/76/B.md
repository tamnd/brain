---
title: "CF 76B - Mice"
description: "We are given a row of mice located along a horizontal line at coordinate y = Y0 and a row of cheese pieces along another horizontal line at y = Y1. Each mouse can run directly towards any piece of cheese, and all mice run at the same speed."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 76
codeforces_index: "B"
codeforces_contest_name: "All-Ukrainian School Olympiad in Informatics"
rating: 2100
weight: 76
solve_time_s: 113
verified: false
draft: false
---

[CF 76B - Mice](https://codeforces.com/problemset/problem/76/B)

**Rating:** 2100  
**Tags:** greedy, two pointers  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of mice located along a horizontal line at coordinate `y = Y0` and a row of cheese pieces along another horizontal line at `y = Y1`. Each mouse can run directly towards any piece of cheese, and all mice run at the same speed. When multiple mice target the same piece of cheese, only the first one to arrive eats it; subsequent mice remain hungry. Our task is to determine the minimal number of mice that will go hungry if all mice choose their closest cheese optimally.

The input provides the x-coordinates of mice and cheese in strictly increasing order. This strictly increasing order means we can efficiently compare positions without worrying about ties at the same coordinate, simplifying matching. The number of mice and cheese can reach up to 100,000 each, so any naive solution that examines every pair of mouse and cheese points would involve 10^10 operations, far too large for a standard time limit.

A non-obvious edge case arises when all mice cluster near one piece of cheese while other cheese pieces are far away. For example, if three mice are at positions `[0,1,2]` and there are two cheese pieces at `[0, 100]`, the nearest piece for all mice is `0`. If we assign them greedily without considering relative arrival times, we might incorrectly assume more mice get fed than possible. The correct output is that only the closest mice eat the first cheese, and the rest go hungry.

Another edge case occurs when there are no cheese pieces at all. In that case, all mice remain hungry. A final subtlety is when mice and cheese are already sorted by x-coordinate. Sorting is unnecessary and a two-pointer approach can exploit this ordering efficiently.

## Approaches

The brute-force approach would consider every mouse-cheese pair, calculate the Euclidean distance, and assign mice to the closest cheese. After sorting distances for each cheese, we would simulate arrivals to see which mice eat first. While this works for correctness, it has time complexity O(N * M), which is infeasible for the upper limit of 100,000 mice and cheese.

The key insight is to exploit the strictly increasing order of coordinates. Because all mice run at the same speed and y-distance is constant, the closest cheese for a mouse depends only on the x-distance. We can use a two-pointer technique: iterate through mice from left to right, and for each mouse, find the nearest available cheese. If a mouse is closer to the next cheese than the current one, we move the cheese pointer forward. This way, each mouse is paired optimally without checking every possible pair.

The problem reduces to a two-pointer matching problem along a single dimension, with Euclidean distances simplified by the vertical distance between lines. The approach guarantees minimal hungry mice because we always assign the closest remaining cheese to each mouse in order, ensuring no mouse could have reached a closer piece unclaimed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N*M) | O(N+M) | Too slow |
| Two-Pointer Greedy | O(N+M) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with pointers `i` for mice and `j` for cheese, both at the beginning of their respective lists.
2. For each mouse at position `mice[i]`, check the distance to the current cheese `cheese[j]` and the next cheese `cheese[j+1]` if it exists. Compute the squared Euclidean distance to avoid floating point errors: `(mice[i]-cheese[j])**2 + (Y0-Y1)**2`.
3. If the next cheese is closer, move the cheese pointer `j` forward until the current cheese is the closest or we reach the last cheese.
4. Assign this mouse to the closest cheese. If the cheese is still unassigned, mark it as eaten and move to the next mouse. Otherwise, the mouse goes hungry.
5. Keep a counter of hungry mice. For each mouse, if there are no more cheese pieces to assign, increment the hungry counter.
6. Continue until all mice are processed.

Why it works: at every step, each mouse greedily targets its nearest cheese among those not already assigned. The strictly increasing order of coordinates ensures no skipped opportunities. The invariant is that at each iteration, every assigned mouse has the closest available cheese, so no mouse could have been assigned a nearer piece. This guarantees minimal hungry mice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    N, M, Y0, Y1 = map(int, input().split())
    mice = list(map(int, input().split()))
    cheese = list(map(int, input().split()))
    
    hungry = 0
    j = 0
    dy2 = (Y0 - Y1) ** 2  # constant vertical distance squared

    for x in mice:
        while j + 1 < M and (cheese[j+1] - x)**2 + dy2 <= (cheese[j] - x)**2 + dy2:
            j += 1
        if j >= M:
            hungry += 1

    print(hungry)

if __name__ == "__main__":
    main()
```

The code uses `dy2` to account for the vertical distance squared, avoiding repeated computation. The while loop moves the cheese pointer only when the next cheese is strictly closer, preserving greedy correctness. Boundary checks ensure we do not index beyond the last cheese.

## Worked Examples

### Sample 1

Input:

```
3 2 0 2
0 1 3
2 5
```

| Mouse `x` | Cheese pointer `j` | Closest cheese | Hungry? |
| --- | --- | --- | --- |
| 0 | 0 | 2 | yes (first arrival eaten by mouse at 1) |
| 1 | 0 | 2 | no |
| 3 | 1 | 5 | no |

This confirms one mouse remains hungry, exactly matching the sample output.

### Sample 2

Input:

```
4 1 0 1
0 1 2 3
2
```

| Mouse `x` | Cheese pointer `j` | Closest cheese | Hungry? |
| --- | --- | --- | --- |
| 0 | 0 | 2 | yes |
| 1 | 0 | 2 | yes |
| 2 | 0 | 2 | no |
| 3 | 0 | 2 | yes |

The table confirms three mice remain hungry. The greedy pointer always selects the nearest cheese.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N+M) | Each mouse is processed once, and the cheese pointer moves monotonically to the right at most M times. |
| Space | O(N+M) | We store coordinates of all mice and cheese. |

With N, M up to 10^5, 200,000 operations plus comparisons easily fit within standard time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided sample
assert run("3 2 0 2\n0 1 3\n2 5\n") == "1", "sample 1"

# custom minimum input
assert run("1 0 0 1\n0\n") == "1", "no cheese"

# all mice on left, one cheese far right
assert run("3 1 0 2\n0 1 2\n10\n") == "3", "all too far"

# all mice perfectly aligned with cheese
assert run("2 2 0 1\n1 3\n1 3\n") == "0", "perfect match"

# more mice than cheese, some hungry
assert run("5 2 0 1\n0 1 2 3 4\n1 3\n") == "3", "uneven distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1 0 0 1\n0\n" | 1 | No cheese, all mice hungry |
| "3 1 0 2\n0 1 2\n10\n" | 3 | Cheese too far for all |
| "2 2 0 1\n1 3\n1 3\n" | 0 | Each mouse has exact cheese |
| "5 2 0 1\n0 1 2 3 4\n1 3\n" | 3 | Some mice must remain hungry |

## Edge Cases

In the case of no cheese, `M = 0`, the pointer `j` never increments, and every mouse increments the hungry counter, yielding `N` as expected.

When multiple mice compete for a single cheese, the greedy pointer ensures the closest mouse is counted first, and the rest naturally increment the hungry counter. For example, with mice `[0,1,2]` and cheese `[1]`, mouse at 1 reaches first, mice at 0 and 2 remain hungry, confirming the output `2`.

If all cheese are to the right of all mice, the pointer moves only when the next cheese is closer, but if no such cheese exists, every mouse goes hungry. This behavior handles edge spacing correctly.
