---
title: "CF 405A - Gravity Flip"
description: "We are given a row of vertical stacks of cubes, where each position holds a certain number of cubes. You can think of this as an array where each index represents a column and the value is its height."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 405
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 238 (Div. 2)"
rating: 900
weight: 405
solve_time_s: 381
verified: false
draft: false
---

[CF 405A - Gravity Flip](https://codeforces.com/problemset/problem/405/A)

**Rating:** 900  
**Tags:** greedy, implementation, sortings  
**Solve time:** 6m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of vertical stacks of cubes, where each position holds a certain number of cubes. You can think of this as an array where each index represents a column and the value is its height.

Initially, gravity acts downward, so cubes are stacked vertically inside each column. Then gravity is switched so that instead of falling down, all cubes effectively slide to the right. After this switch, cubes redistribute across columns while preserving their total count, but they rearrange as if everything is now being “pushed” horizontally to the right side of the box.

The task is to determine what the column heights become after this transformation.

The constraints are small: the number of columns is at most 100, and each height is at most 100. This immediately tells us that even quadratic or cubic solutions would be fast enough, but the structure of the transformation suggests something simpler is possible.

A naive misunderstanding often comes from thinking the transformation depends on simulating individual cube movement. That would be unnecessary and error-prone.

A few edge cases clarify the behavior:

If all columns already have equal heights, nothing changes. For example, `[2, 2, 2]` remains `[2, 2, 2]`.

If there is only one column, the answer is identical to the input because there is nowhere to redistribute cubes.

If the array is unsorted, like `[3, 1, 2]`, the output becomes sorted as `[1, 2, 3]`, which reveals the key structure of the problem.

## Approaches

If we try to simulate gravity literally, we might imagine each cube moving one step at a time until it reaches its final resting position. That would involve iterating over all cubes and repeatedly shifting them rightward into available space. In the worst case, with n columns and up to n cubes per column, this simulation would require tracking up to 10,000 individual cube movements, and more importantly, managing collisions and stacking logic. While still feasible under constraints, it introduces unnecessary complexity.

The key observation is that gravity switching to the right does not preserve column identities. It only preserves the multiset of cube heights. All cubes simply get redistributed so that smaller stacks end up earlier and larger stacks end up later in order to form a sorted sequence.

This happens because after switching gravity, cubes effectively "fall" into the rightmost available positions. The final configuration is equivalent to sorting the column heights in non-decreasing order.

So instead of simulating motion, we only need to sort the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of cube movement | O(n²) or worse | O(n) | Too slow / unnecessary |
| Sort heights | O(n log n) | O(1) extra (ignoring sort internals) | Accepted |

## Algorithm Walkthrough

1. Read the integer n, which gives the number of columns. This defines the size of the array we are working with.
2. Read the array of heights a. Each value represents a stack of cubes in a column before gravity changes.
3. Sort the array in non-decreasing order. This step directly models the effect of all cubes sliding to the right and accumulating in order of increasing stack size.
4. Output the sorted array as the final configuration.

### Why it works

The transformation preserves only the total number of cubes and allows them to be redistributed freely along the line. Since there is no constraint tying a specific cube to a specific column after the switch, the final arrangement depends only on how many cubes exist in total at each height level. Sorting ensures that all smaller stacks occupy earlier positions and larger stacks occupy later positions, matching the rightward accumulation effect of gravity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    print(*a)

if __name__ == "__main__":
    solve()
```

The solution is centered entirely on sorting the input array. The input parsing uses fast I/O, though it is not strictly necessary given the constraints.

The critical implementation detail is that sorting is done in-place on the list of heights. No additional data structures are required beyond storing the input.

The output uses Python’s unpacking operator to print the sorted values in a single line.

## Worked Examples

### Example 1

Input:

```
4
3 2 1 2
```

Sorted process:

| Step | Array state |
| --- | --- |
| Initial | 3 2 1 2 |
| After sort | 1 2 2 3 |

Output:

```
1 2 2 3
```

This demonstrates how values simply rearrange globally without any structural dependency on original positions.

### Example 2

Input:

```
3
2 2 2
```

| Step | Array state |
| --- | --- |
| Initial | 2 2 2 |
| After sort | 2 2 2 |

Output:

```
2 2 2
```

This confirms that identical values remain unchanged under sorting, matching the intuition that no redistribution occurs when all columns are already uniform.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(1) extra | Sorting is in-place aside from recursion/internal buffers |

Given n ≤ 100, this is far below any practical time limit, and even a naive approach would pass, though unnecessary.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    return " ".join(map(str, a))

# provided sample
assert run("4\n3 2 1 2\n") == "1 2 2 3", "sample 1"

# single element
assert run("1\n5\n") == "5", "single column"

# already sorted
assert run("5\n1 2 3 4 5\n") == "1 2 3 4 5", "already sorted"

# reverse order
assert run("5\n5 4 3 2 1\n") == "1 2 3 4 5", "reverse order"

# all equal
assert run("4\n7 7 7 7\n") == "7 7 7 7", "uniform heights"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | unchanged | minimal boundary |
| sorted input | same order | stability case |
| reverse input | sorted output | correctness of transformation |
| all equal | unchanged | uniform case |

## Edge Cases

One important edge case is when there is only a single column. For input `1` with value `[10]`, sorting leaves it unchanged, and the output remains `[10]`. The algorithm handles this naturally because sorting a single-element array is a no-op.

Another case is when all values are identical, such as `[4, 4, 4, 4]`. The sorted result is the same array. This confirms that no unintended reordering or instability affects equal elements.

A final subtle case is when values are already strictly increasing or decreasing. In both scenarios, sorting produces a consistent canonical ordering, and since the transformation depends only on multiset structure, the result remains correct regardless of initial arrangement.
