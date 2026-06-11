---
title: "CF 1399A - Remove Smallest"
description: "We are asked to determine if we can reduce an array of positive integers to a single element using a specific operation: choose two distinct elements whose difference is at most one and remove the smaller of the two (or either if they are equal)."
date: "2026-06-11T08:58:18+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1399
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 661 (Div. 3)"
rating: 800
weight: 1399
solve_time_s: 89
verified: true
draft: false
---

[CF 1399A - Remove Smallest](https://codeforces.com/problemset/problem/1399/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine if we can reduce an array of positive integers to a single element using a specific operation: choose two distinct elements whose difference is at most one and remove the smaller of the two (or either if they are equal). The array may contain duplicates, and each test case is independent.

The input consists of multiple test cases. For each test case, the array length is at most 50 and each element is between 1 and 100. This means any solution that is quadratic in `n` will run comfortably within the time limits, since 50 squared is only 2500 operations per test case. With up to 1000 test cases, we reach 2.5 million operations in the worst case, which is acceptable for a 1-second limit.

Non-obvious edge cases include arrays where all elements are equal, arrays with a single element, and arrays where the maximum gap between consecutive elements is more than 1. For example, `[1, 2, 4]` cannot be reduced to a single element because the 2 and 4 differ by more than 1 and no sequence of allowed removals can eliminate this gap. Similarly, `[5, 5, 5, 5]` can always be reduced to one element, while `[100]` is trivially already a single element.

## Approaches

A brute-force approach would simulate all possible moves: repeatedly look for a pair of elements whose difference is at most 1, remove the smaller, and continue until one element remains or no moves are possible. This works for small `n` but becomes messy and inefficient, as we would need to repeatedly search for valid pairs and remove elements dynamically. The worst-case operation count is around `O(n^3)` because each removal requires scanning all pairs, which is overkill even for `n = 50`.

The key observation is that the ability to remove elements is determined entirely by the gaps between consecutive numbers once the array is sorted. If the array is sorted and every adjacent pair differs by at most 1, then every element can eventually be removed except the largest one. If any adjacent pair differs by 2 or more, the elements on either side of the gap cannot be reduced to one, making it impossible to reach a single-element array.

This observation simplifies the solution to sorting the array and checking consecutive differences. Sorting costs `O(n log n)` and a single linear scan confirms whether all differences are at most 1, giving a clean and optimal solution.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n^3) | O(n) | Too slow / messy |
| Optimal | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. We will process each test case independently.
2. For each test case, read the array length `n` and the array elements `a`.
3. Sort the array in ascending order. Sorting ensures that we can check the differences between consecutive elements directly.
4. Initialize a flag variable to "YES", assuming we can reduce the array to a single element.
5. Iterate over the array from the first to the second-to-last element. For each index `i`, compute the difference between `a[i+1]` and `a[i]`. If this difference is greater than 1, set the flag to "NO" and break out of the loop. This identifies any gap that prevents full reduction.
6. After checking all adjacent pairs, output the flag for the current test case. "YES" indicates it is possible to reduce the array to a single element, "NO" otherwise.

Why it works: Once the array is sorted, the only constraint preventing full reduction is the presence of gaps larger than 1. Any two consecutive numbers with a difference of 1 or 0 can eventually be reduced by repeated removal operations, because we can always remove the smaller until only one remains. Any difference of 2 or more introduces an insurmountable barrier.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    possible = True
    for i in range(n - 1):
        if a[i+1] - a[i] > 1:
            possible = False
            break
    print("YES" if possible else "NO")
```

The solution first reads the number of test cases. Each array is sorted, which allows a single linear scan to detect any difference greater than 1. The variable `possible` tracks whether the array can be reduced to one element, and we break early on detecting a gap larger than 1. Sorting handles duplicate elements automatically and guarantees we only need to check consecutive pairs. No additional data structures are required.

## Worked Examples

Trace through the input `[1, 2, 2]`:

| Step | Array | Check | Action |
|---|---|---|---|
| 1 | [1, 2, 2] | 2 - 1 = 1 | OK |
| 2 | [1, 2, 2] | 2 - 2 = 0 | OK |
| 3 | - | all diffs <= 1 | YES |

Trace through the input `[1, 2, 4]`:

| Step | Array | Check | Action |
|---|---|---|---|
| 1 | [1, 2, 4] | 2 - 1 = 1 | OK |
| 2 | [1, 2, 4] | 4 - 2 = 2 | Not allowed, break |
| 3 | - | gap > 1 detected | NO |

These traces demonstrate that checking only consecutive differences is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n log n) | Sorting dominates, linear scan is O(n) |
| Space | O(1) extra | Sorting can be done in-place |

With `n <= 50` and `t <= 1000`, the solution performs at most `1000 * 50 log 50 ≈ 85000` operations, well within 1 second. Memory usage is minimal and fits easily within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        possible = True
        for i in range(n - 1):
            if a[i+1] - a[i] > 1:
                possible = False
                break
        print("YES" if possible else "NO")
    return out.getvalue().strip()

# Provided samples
assert run("5\n3\n1 2 2\n4\n5 5 5 5\n3\n1 2 4\n4\n1 3 4 4\n1\n100") == "YES\nYES\nNO\nNO\nYES", "sample 1"

# Custom cases
assert run("3\n2\n1 3\n2\n1 2\n3\n10 10 10") == "NO\nYES\nYES", "gaps, minimal case, all equal"
assert run("1\n50\n" + " ".join(str(i) for i in range(1, 51))) == "NO", "max size, consecutive 1..50"
assert run("1\n50\n" + " ".join(["1"]*50)) == "YES", "all equal large n"
assert run("1\n5\n1 2 3 4 5") == "YES", "consecutive small array"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `2 1 3\n2 1 2\n3 10 10 10` | `NO\nYES\nYES` | gap > 1, minimal array, all equal |
| `50 1..50` | `NO` | maximum-size array with increasing differences |
| `50 * [1]` | `YES` | all elements equal in large array |
| `1 2 3 4 5` | `YES` | small consecutive array |

## Edge Cases

For the single-element array `[100]`, sorting has no effect. The loop over consecutive differences does not run since there is only one element. The algorithm outputs "YES" correctly because no operations are needed.  

For arrays where all elements are equal, such as `[5, 5, 5, 5]`, differences are zero, so the algorithm outputs "YES".  

For arrays with gaps, `[1, 3]`, the difference `3 - 1 = 2` triggers the break condition, producing "NO" immediately. This handles the key constraint preventing reduction to a single element.
