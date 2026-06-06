---
title: "CF 405A - Gravity Flip"
description: "We are given a row of vertical stacks of cubes. Each position in the row holds a column, and the input array describes how many cubes are stacked at each position. Then a “gravity switch” happens. Before the switch, gravity acts downward, so each column is stable and independent."
date: "2026-06-07T01:37:13+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 405
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 238 (Div. 2)"
rating: 900
weight: 405
solve_time_s: 256
verified: true
draft: false
---

[CF 405A - Gravity Flip](https://codeforces.com/problemset/problem/405/A)

**Rating:** 900  
**Tags:** greedy, implementation, sortings  
**Solve time:** 4m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of vertical stacks of cubes. Each position in the row holds a column, and the input array describes how many cubes are stacked at each position.

Then a “gravity switch” happens. Before the switch, gravity acts downward, so each column is stable and independent. After the switch, gravity starts acting to the right, which causes cubes to slide horizontally. A cube always moves as far right as possible, filling lower available positions in columns to its right before staying where it is.

After everything settles, we need to report how many cubes end up in each column.

The key mental shift is that nothing is created or destroyed, only rearranged under a directional force. The final state depends only on how cubes redistribute under repeated rightward falling.

The constraints are small: at most 100 columns and at most 100 cubes per column. Even a slow simulation that touches every cube many times would still run comfortably within limits, since the total number of cubes is at most 10,000 and any quadratic behavior over 100 elements is negligible.

A few situations can trip up naive thinking.

If all columns already have the same height, for example `3 3 3`, then nothing changes after gravity, because there is no “lower” configuration achievable by rearrangement.

If the array is decreasing like `5 4 3 2`, the final state becomes sorted as `2 3 4 5`. A common mistake is assuming gravity preserves the original order of columns while only shifting cubes, but in reality the redistribution fully reorders heights.

If there is only one column, such as `n = 1`, the answer is identical to input, since there is nowhere for cubes to move.

## Approaches

A direct way to think about the process is to simulate what each cube does. You could imagine iterating repeatedly over the array and letting cubes “fall right” step by step whenever the next column has space relative to the current configuration. However, this viewpoint quickly becomes inefficient because a cube may need to traverse many columns, and interactions between columns mean you would repeatedly re-check stability.

If we try to formalize this naive simulation, each cube could potentially be moved across up to `n` positions, and there are up to `n * 100` cubes total. This leads to a worst-case behavior around `O(n^2 * max height)` which is unnecessary for such a small structural problem.

The key observation is that gravity does not depend on positions at all, only on the multiset of column heights. Once gravity acts to the right, cubes effectively “sort themselves” into nondecreasing column heights from left to right. Every configuration converges to the same state: the sorted version of the original array.

This happens because any inversion, where a left column is taller than a right column, can be resolved by shifting cubes rightward until the heights are ordered. Repeatedly applying this idea removes all inversions, which is exactly what sorting does.

So the entire problem reduces to sorting the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n² · max(a)) | O(1) | Too slow and unnecessary |
| Sorting | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of columns and the array of heights. At this point, we only interpret the array as a collection of values, not positions, since positions will not matter after gravity acts.
2. Sort the array in nondecreasing order. This step directly constructs the final stable configuration under rightward gravity because all cubes must end up as far right as possible, which forces smaller stacks to appear first.
3. Output the sorted array as the final column heights.

### Why it works

The process preserves the total number of cubes and allows only redistribution to the right. Any configuration that is not sorted contains at least one adjacent inversion where a larger column stands before a smaller one. Gravity eliminates such inversions by effectively moving cubes rightward. Since inversions can always be resolved and no operation introduces new inversions in the opposite direction, the system converges to a fully nondecreasing sequence, which is unique and equal to the sorted array.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

a.sort()

print(*a)
```

The solution reads the array, sorts it, and prints it directly. The sorting step is the entire transformation logic, and no simulation is needed.

The only subtle point is ensuring correct output formatting. Using `print(*a)` avoids manual joining mistakes and guarantees space-separated output.

## Worked Examples

### Example 1

Input:

`4`

`3 2 1 2`

After sorting, we track the transformation.

| Step | Array state |
| --- | --- |
| Initial | 3 2 1 2 |
| After sort | 1 2 2 3 |

The sorted array matches the final stable configuration under rightward gravity. Smaller stacks accumulate on the left.

### Example 2

Input:

`5`

`1 1 1 1 1`

| Step | Array state |
| --- | --- |
| Initial | 1 1 1 1 1 |
| After sort | 1 1 1 1 1 |

This shows a fully uniform configuration remains unchanged, since there are no inversions to resolve.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the computation |
| Space | O(1) extra (or O(n) depending on sort) | In-place or Python’s Timsort auxiliary usage |

With `n ≤ 100`, sorting is effectively instantaneous, far below any time limit concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().split()))
    a.sort()
    return " ".join(map(str, a))

# provided samples
assert run("4\n3 2 1 2\n") == "1 2 2 3", "sample 1"
assert run("3\n1 2 3\n") == "1 2 3", "sample 2"

# custom cases
assert run("1\n5\n") == "5", "single column"
assert run("5\n5 4 3 2 1\n") == "1 2 3 4 5", "reverse sorted"
assert run("4\n2 2 2 2\n") == "2 2 2 2", "all equal"
assert run("6\n1 3 2 3 1 2\n") == "1 1 2 2 3 3", "mixed duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | same value | minimal edge case |
| reverse order | sorted ascending | worst inversion case |
| all equal | unchanged | stability under no movement |
| mixed duplicates | grouped sorted | handling repeated values |

## Edge Cases

For `n = 1`, input like `7` produces output `7`. The algorithm reads the array, sorts a single element, and outputs it unchanged, since sorting does not modify singleton lists.

For a decreasing sequence like `5 4 3 2 1`, sorting produces `1 2 3 4 5`. The algorithm does not simulate movement, it directly computes the final equilibrium configuration, which corresponds to fully removing all inversions.

For a uniform sequence like `4 4 4 4`, sorting leaves the array unchanged. No inversion exists, so the invariant that the array is nondecreasing already holds at the start, and the algorithm performs no effective transformation beyond identity.
