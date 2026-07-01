---
title: "CF 104451B - \u041e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435"
description: "We are given an array of distinct integers, and we are allowed to pick exactly one contiguous segment and reverse it."
date: "2026-06-30T14:49:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104451
codeforces_index: "B"
codeforces_contest_name: "\u041f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0441\u0440\u0435\u0434\u0438 \u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0445 2023"
rating: 0
weight: 104451
solve_time_s: 44
verified: true
draft: false
---

[CF 104451B - \u041e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/104451/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers, and we are allowed to pick exactly one contiguous segment and reverse it. The task is to determine whether there exists some segment whose reversal turns the entire array into a strictly increasing sequence, and if so, to output one such segment.

The input is simply the length of the array followed by the array itself. The output is either a confirmation that it is possible along with the segment boundaries, or a statement that no single reversal can sort the array.

The key structural constraint is that the array size can be up to 100,000, so any solution that tries all possible segments is immediately infeasible. A naive O(n³) or even O(n²) approach would time out, and even O(n²) simulation of reversals is too slow if done repeatedly. This forces us toward an O(n) or O(n log n) reasoning based on structural properties of nearly sorted arrays.

A subtle edge case arises when the array is already sorted. In this case, reversing a length-1 segment is valid and must be accepted. Another important corner case is when the unsorted portion is very small, for example a single inversion like `[2, 1, 3, 4]`, where only one swap-equivalent segment exists. Finally, there are cases where the array looks “almost sorted” locally but cannot be fixed by a single reversal, such as `[3, 1, 2, 4]`, where any reversal disrupts other parts of the order.

## Approaches

A brute-force strategy is to try every possible pair of indices `l, r`, reverse that segment, and check whether the array becomes sorted. Each check takes O(n), and there are O(n²) segments, giving O(n³) overall. Even optimizing the check with precomputation does not remove the quadratic number of candidates, so this is too slow for n = 100,000.

The key insight is to shift from “trying all reversals” to “characterizing what a valid reversal must look like”. If reversing a segment sorts the array, then outside that segment the array must already be sorted in correct order. Inside the segment, the order must be exactly reversed relative to a sorted array, meaning the segment must appear strictly decreasing in the original array.

This leads to a structural observation: if a solution exists, the array differs from its sorted version in exactly one contiguous block, and that block is strictly decreasing. Outside that block, the array must already match the sorted order.

So instead of trying operations, we compare the array to its sorted version and identify mismatch boundaries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all segments) | O(n³) | O(1) | Too slow |
| Compare with sorted + single segment validation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a sorted copy of the array. This represents the target final configuration after a successful reversal.
2. Find the first index `l` where the original array differs from the sorted array. This is the earliest position that must be included in the reversed segment, since everything before it is already correct.
3. Find the last index `r` where the original array differs from the sorted array. This is the farthest boundary of the segment that must be reversed, since everything after it is already correct.
4. Reverse the subarray from `l` to `r` in a copy of the original array.
5. Check whether this modified array matches the sorted array exactly. If it does, the segment `[l, r]` is valid. Otherwise, no single reversal can fix the array.

The reason we can safely focus on this single candidate segment is that any valid solution must align exactly with the mismatch interval between the array and its sorted version. If a valid reversal exists but differs from this interval, it would imply that parts outside the mismatch are being altered, which would immediately break sorted order elsewhere.

### Why it works

The correctness hinges on the fact that sorting via one reversal cannot introduce new correctly ordered elements outside the reversed segment. Every position outside the chosen segment remains fixed. Therefore, all positions that already match the sorted array must lie outside the segment, and all mismatches must lie inside it. This forces the reversed segment to be exactly the contiguous interval covering all mismatches. Once this interval is determined, there is only one candidate reversal to test, and it is either valid or not.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    b = sorted(a)

    l = 0
    while l < n and a[l] == b[l]:
        l += 1

    if l == n:
        print("yes")
        print(1, 1)
        return

    r = n - 1
    while r >= 0 and a[r] == b[r]:
        r -= 1

    segment = a[:]
    segment[l:r+1] = reversed(segment[l:r+1])

    if segment == b:
        print("yes")
        print(l + 1, r + 1)
    else:
        print("no")

if __name__ == "__main__":
    solve()
```

The code first builds the sorted reference array, then isolates the first and last mismatching positions. Those indices define the only plausible segment that could fix the array. Reversing that segment in a copy is enough because any valid solution must coincide with this mismatch window.

A common mistake is to assume any decreasing segment is valid without verifying global consistency. The final equality check against the sorted array is essential because local monotonicity does not guarantee correctness outside the segment.

## Worked Examples

### Example 1

Input:

```
3
3 2 1
```

Sorted array is `[1, 2, 3]`. The first mismatch is at index 0 and last mismatch is at index 2.

| Step | l | r | array after reverse |
| --- | --- | --- | --- |
| initial | 0 | 2 | 3 2 1 |
| reverse | 0 | 2 | 1 2 3 |

After reversal, the array matches the sorted version, so the answer is `yes 1 3`.

This confirms that the full array can be reversed when it is strictly decreasing.

### Example 2

Input:

```
4
3 1 2 4
```

Sorted array is `[1 2 3 4]`. Mismatch interval is from index 0 to 2.

| Step | l | r | array after reverse |
| --- | --- | --- | --- |
| initial | 0 | 2 | 3 1 2 4 |
| reverse | 0 | 2 | 2 1 3 4 |

The result is not sorted, so no single reversal works.

This demonstrates that even when all mismatches are contiguous, the internal structure must still align perfectly after reversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, all other operations are linear |
| Space | O(n) | Extra array for sorted copy |

This comfortably fits within constraints for n up to 100,000, since sorting and a single scan are both efficient at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n = int(input())
    a = list(map(int, input().split()))
    b = sorted(a)

    l = 0
    while l < n and a[l] == b[l]:
        l += 1

    if l == n:
        return "yes\n1 1"

    r = n - 1
    while r >= 0 and a[r] == b[r]:
        r -= 1

    segment = a[:]
    segment[l:r+1] = reversed(segment[l:r+1])

    if segment == b:
        return f"yes\n{l+1} {r+1}"
    return "no"

# provided samples
assert run("3\n3 2 1\n") == "yes\n1 3"
assert run("4\n3 1 2 4\n") == "no"

# custom cases
assert run("2\n1 2\n") == "yes\n1 1"
assert run("4\n2 1 3 4\n") == "yes\n1 2"
assert run("5\n5 4 3 2 1\n") == "yes\n1 5"
assert run("5\n1 3 2 5 4\n") == "no"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted array | single element reversal | already sorted edge case |
| one swap | yes segment | minimal reversal case |
| full reverse | full segment | maximal decreasing array |
| two disjoint inversions | no | non-contiguous fix impossible |

## Edge Cases

When the array is already sorted, the mismatch interval is empty, and the algorithm treats it as a trivial valid case. Returning `[1, 1]` is correct because reversing a length-1 segment leaves the array unchanged.

When the array is fully decreasing, the mismatch interval spans the whole array. Reversing it produces a fully increasing sequence, and the check against the sorted array confirms correctness.

When mismatches form a contiguous block but internal structure is not strictly reversed, such as `[3, 1, 2, 4]`, the algorithm still selects the correct interval but fails the final verification. This prevents incorrect acceptance of partial reversals that cannot globally sort the array.
