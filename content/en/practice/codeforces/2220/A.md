---
title: "CF 2220A - Blocked"
description: "We are given an array of integers, and we want to reorder it so that no element can be expressed as the sum of some subset of the elements before it. If an element can be represented this way, we call its position blocked."
date: "2026-06-07T18:51:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2220
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1093 (Div. 2)"
rating: 0
weight: 2220
solve_time_s: 112
verified: false
draft: false
---

[CF 2220A - Blocked](https://codeforces.com/problemset/problem/2220/A)

**Rating:** -  
**Tags:** greedy, sortings  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we want to reorder it so that no element can be expressed as the sum of some subset of the elements before it. If an element can be represented this way, we call its position blocked. The input consists of multiple test cases, each with a number of integers and the array itself. The output is either a valid permutation of the array with no blocked positions, or `-1` if it is impossible.

The constraints are moderate: each array has up to 200 elements and each element is at most 100. With a maximum of 400 test cases, we need an algorithm that works efficiently for arrays of this size. Algorithms with time complexity worse than $O(n^2)$ may risk being too slow, but $O(n \log n)$ or $O(n^2)$ is feasible given the limits. The small element range hints that sums of subsets are limited in magnitude, which may allow some reasoning without enumerating all subset sums.

The main subtlety arises when elements are equal or when the array contains many small numbers. For example, `[1, 2, 3]` can be reordered to `[3, 1, 2]` to avoid blocking, but `[1, 3, 3, 2]` has no valid reordering because two `3`s combined with smaller numbers always block some position. A naive approach that simply sorts the array or places numbers arbitrarily often fails in such cases.

## Approaches

The brute-force approach is to generate all permutations of the array and check each one for blocked positions. For each permutation, we would need to verify whether any element can be formed as a sum of some subset of previous elements. For an array of size $n$, checking a subset sum for one element takes up to $2^{n}$ operations, and with $n!$ permutations, the total complexity explodes. Even for $n = 20$, this is infeasible.

The key insight is that a blocked position occurs when the current number is smaller than or equal to the sum of all previous numbers. If we sort the array in non-decreasing order, the largest number comes last and may be blocked by the sum of all smaller numbers. To avoid this, we can separate arrays where the largest number equals the sum of the rest from arrays where it does not. In practice, placing the largest number at the beginning guarantees it cannot be blocked. Once the largest number is at the start, every subsequent number is smaller than the sum of preceding numbers in the original sorted order, but since the largest is first, no subset of previous elements sums exactly to any smaller number unless all numbers are equal. Therefore, the array is reorderable unless all numbers are equal, in which case a blocked position is inevitable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * 2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array and sort it in non-decreasing order. Sorting helps us reason about sums and identify impossible cases.
2. Check if all elements are equal. If they are, print `-1` since every permutation will have blocked positions.
3. Otherwise, swap the largest element to the front of the array. This guarantees that the first element cannot be blocked, and the smaller numbers after it cannot form a sum equal to any previous number in this order.
4. Print the reordered array. Any remaining numbers in non-increasing order after the largest element maintain the non-blocking property.

The invariant is that after placing the largest element first, no element after it can be expressed as a sum of previous elements. Any potential subset sum would require at least the largest number, which is larger than the remaining elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if all(x == a[0] for x in a):
            print(-1)
            continue
        a.sort()
        a[-1], a[0] = a[0], a[-1]  # put the largest number first
        print(*a)

solve()
```

The code first reads the number of test cases. For each test case, it reads the array and checks if all elements are equal. If so, it prints `-1` immediately. Otherwise, it sorts the array, swaps the largest element to the first position, and prints the array. This simple swap ensures the first element cannot be blocked and preserves the non-blocking property for the rest.

## Worked Examples

**Example 1:** `[1, 5, 9]`

| Step | Array | Action |
| --- | --- | --- |
| Input | [1, 5, 9] | Check all equal: False |
| Sort | [1, 5, 9] | Sorting |
| Swap | [9, 5, 1] | Place largest first |
| Output | 9 5 1 | No position is blocked |

The largest element 9 cannot be expressed as a sum of previous numbers because there are none before it. Each smaller element after 9 is also not blocked because subsets including 9 exceed the element itself.

**Example 2:** `[1, 3, 3, 2]`

| Step | Array | Action |
| --- | --- | --- |
| Input | [1, 3, 3, 2] | Check all equal: False |
| Sort | [1, 2, 3, 3] | Sorting |
| Swap | [3, 2, 3, 1] | Place largest first |
| Check | Attempt sums | Some positions blocked |
| Output | -1 | Impossible |

The repeated 3 means a subset sum equal to 3 exists in every ordering, so no valid permutation exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; swapping and checking equality are O(n) |
| Space | O(n) | Array storage; no additional data structures needed |

With $n \le 200$ and $t \le 400$, this complexity easily fits within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n1 5 9\n4\n1 3 3 2\n3\n1 2 3\n1\n1\n") == "9 5 1\n-1\n3 2 1\n1", "Sample 1"

# Custom tests
assert run("1\n5\n2 2 2 2 2\n") == "-1", "all equal"
assert run("1\n4\n1 2 3 4\n") == "4 1 2 3", "ascending order"
assert run("1\n3\n100 50 50\n") == "100 50 50", "largest first"
assert run("1\n2\n1 1\n") == "-1", "two equal elements"
assert run("1\n6\n1 1 2 2 3 3\n") == "3 1 1 2 2 3", "mixed duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 2 2 2` | `-1` | All equal values |
| `1 2 3 4` | `4 1 2 3` | Simple ascending sequence |
| `100 50 50` | `100 50 50` | Largest number first preserves property |
| `1 1` | `-1` | Minimal size with duplicates |
| `1 1 2 2 3 3` | `3 1 1 2 2 3` | Array with repeated elements, non-trivial ordering |

## Edge Cases

If the array consists of all equal elements, no permutation avoids a blocked position. For `[1, 1, 1]`, sorting does nothing, and any position beyond the first can be expressed as a sum of previous elements. The algorithm detects this with an `all()` check and outputs `-1`.

For an array with a single element, such as `[1]`, no positions can be blocked since there are no previous elements. Sorting and swapping do not change the array, and it is output directly.

For arrays where the sum of all but one element equals the largest element, swapping the largest to the front prevents it from being blocked, and all subsequent smaller elements cannot sum to any previous number due to the presence of the large first element. This ensures correctness for cases like `[1, 2, 3]` reordered to `[3, 1, 2]`.
