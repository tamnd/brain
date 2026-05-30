---
title: "CF 454B - Little Pony and Sort by Shift"
description: "We are given a sequence of integers arranged in a line, and our goal is to sort them in non-decreasing order by repeatedly performing a single allowed operation: moving the last element of the sequence to the front."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 454
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 259 (Div. 2)"
rating: 1200
weight: 454
solve_time_s: 67
verified: true
draft: false
---

[CF 454B - Little Pony and Sort by Shift](https://codeforces.com/problemset/problem/454/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers arranged in a line, and our goal is to sort them in non-decreasing order by repeatedly performing a single allowed operation: moving the last element of the sequence to the front. Conceptually, we are allowed to "rotate" the array right by one position any number of times, and we want to find the minimum number of such rotations that results in a sorted sequence. If no number of rotations can sort the sequence, we return -1.

The input consists of the length of the sequence `n` and the sequence itself, where `n` can be as large as 100,000. With a 1-second time limit, any solution with complexity worse than O(n log n) is risky, and O(n^2) approaches are effectively ruled out. The elements themselves are all positive integers up to 100,000, which means we only need to worry about sorting logic, not special data types.

Edge cases include sequences that are already sorted, sequences sorted in strictly descending order (requiring a full rotation), sequences where multiple duplicates exist, and sequences where no rotation can make the sequence sorted. For instance, the input `[3, 1, 2]` cannot be sorted by any number of single rotations, so the correct output is -1. A careless approach that checks only if the array is cyclically rotated once would incorrectly return a number of rotations even when sorting is impossible.

## Approaches

The brute-force approach would try every possible rotation from 0 to n-1 and check if the sequence becomes sorted after each rotation. For each rotation, verifying if the array is sorted takes O(n) time. Since there are n possible rotations, this approach requires O(n^2) operations in the worst case. For n = 10^5, this results in 10^10 operations, which is far beyond acceptable limits, so brute-force is not feasible.

The key observation is that a sorted sequence can only be obtained by a rotation if the sequence is already "almost sorted" except for a single decreasing point where the sequence wraps around. In other words, there can be at most one position `i` where `a[i] > a[i+1]`. If there is more than one such position, no number of rotations can sort the array. If exactly one such position exists, the number of rotations needed is `n - (i + 1)` because moving all elements after `i` to the front aligns the sequence into sorted order.

This insight reduces the problem to a single linear scan to count "inversions" where a number is greater than its successor, and a simple arithmetic calculation of rotations if exactly one inversion exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `break_point_count` to zero and a variable `break_index` to -1. These will track the number of places where the current element is greater than the next element.
2. Iterate through the array from index 0 to n-2. For each index `i`, compare `a[i]` with `a[i+1]`. If `a[i] > a[i+1]`, increment `break_point_count` and set `break_index = i`.
3. After the loop, compare the last element `a[n-1]` with the first element `a[0]` to check if there is a wraparound inversion. If `a[n-1] > a[0]`, increment `break_point_count` and set `break_index = n-1`.
4. If `break_point_count` is zero, the array is already sorted and zero rotations are needed.
5. If `break_point_count` is exactly one, the minimum rotations needed are `n - (break_index + 1)`.
6. If `break_point_count` is greater than one, sorting the array via rotations is impossible, and we output -1.

Why it works: The algorithm maintains the invariant that a sorted sequence must have at most one "break" point where the order is violated, because each rotation can move only the tail segment to the front. By tracking this single break and calculating its offset, we can determine the exact number of rotations needed. Multiple breaks imply that no single rotation can bring all elements into sorted order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    break_point_count = 0
    break_index = -1
    
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            break_point_count += 1
            break_index = i
    
    if a[n - 1] > a[0]:
        break_point_count += 1
        break_index = n - 1
    
    if break_point_count == 0:
        print(0)
    elif break_point_count == 1:
        print(n - break_index - 1)
    else:
        print(-1)
```

The code first reads the sequence and initializes counters for break points. It loops through the array checking each consecutive pair and the wraparound pair at the end. If there is exactly one inversion, it calculates rotations using `n - break_index - 1`, which aligns the smallest element at the front. Zero inversions require no rotations. More than one inversion is impossible to fix with a single rotation type.

## Worked Examples

**Sample 1:** Input `[2, 1]`

| i | a[i] | a[i+1] | break_point_count | break_index |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 1 | 0 |

Wraparound check `a[1] > a[0]` → 1 > 2 → false

`break_point_count = 1`, `break_index = 0`, rotations = `2 - 0 - 1 = 1`

This matches the expected output 1.

**Custom Example:** Input `[3, 4, 1, 2]`

| i | a[i] | a[i+1] | break_point_count | break_index |
| --- | --- | --- | --- | --- |
| 0 | 3 | 4 | 0 | -1 |
| 1 | 4 | 1 | 1 | 1 |
| 2 | 1 | 2 | 1 | 1 |

Wraparound `a[3] > a[0]` → 2 > 3 → false

`break_point_count = 1`, rotations = `4 - 1 - 1 = 2`

This confirms the algorithm calculates the correct rotation count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single linear scan through the array and one wraparound check |
| Space | O(1) | Only a few integer variables used, no extra storage |

For n up to 10^5, this linear solution executes comfortably under the 1-second time limit and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided sample
assert run("2\n2 1\n") == "1", "sample 1"

# Already sorted
assert run("3\n1 2 3\n") == "0", "already sorted"

# Maximum rotations
assert run("3\n3 1 2\n") == "2", "wrap-around needed"

# Impossible to sort
assert run("4\n3 1 4 2\n") == "-1", "cannot sort"

# All equal values
assert run("5\n2 2 2 2 2\n") == "0", "all equal"

# Minimum size descending
assert run("2\n2 1\n") == "1", "min size descending"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 1 | Minimum size descending |
| 1 2 3 | 0 | Already sorted sequence |
| 3 1 2 | 2 | Rotations needed to sort |
| 3 1 4 2 | -1 | Impossible to sort |
| 2 2 2 2 2 | 0 | All equal values |

## Edge Cases

For an already sorted array like `[1, 2, 3]`, the algorithm finds no break points, outputs zero rotations, and avoids any unnecessary computation. For an array with multiple decreasing points like `[3, 1, 4, 2]`, the algorithm counts more than one break, correctly outputs -1, and demonstrates that the invariant of a single break point is necessary for rotation-based sorting. For arrays where the last element is larger than the first, such as `[3, 4, 1, 2]`, the algorithm accounts for the wraparound check and computes the minimal rotations accurately. Each of these cases confirms that the algorithm handles boundaries and special conditions consistently.
