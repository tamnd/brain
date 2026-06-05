---
title: "CF 285A - Slightly Decreasing Permutations"
description: "We are asked to construct a permutation of numbers from 1 to n that has exactly k positions where a number is greater than the number immediately after it. In other words, we need a sequence of length n where precisely k \"descents\" occur."
date: "2026-06-05T09:45:27+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 285
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 175 (Div. 2)"
rating: 1100
weight: 285
solve_time_s: 127
verified: false
draft: false
---

[CF 285A - Slightly Decreasing Permutations](https://codeforces.com/problemset/problem/285/A)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of numbers from 1 to _n_ that has exactly _k_ positions where a number is greater than the number immediately after it. In other words, we need a sequence of length _n_ where precisely _k_ "descents" occur. The input consists of two integers, _n_ and _k_, and the output is any permutation that satisfies this property. The numbers in the permutation are distinct and range from 1 to _n_.

The constraints allow _n_ up to 10^5 and _k_ less than _n_. This implies we cannot afford algorithms with quadratic or higher complexity. A solution must operate in linear or near-linear time. Memory usage is generous, but unnecessary extra data structures should be avoided.

Edge cases include _k_ equal to 0, where the permutation must be fully increasing. Another case is _k_ equal to _n_-1, where the permutation is fully decreasing. Any careless implementation that constructs the sequence by trial-and-error or swaps without structure may fail on these extremes. For example, with input `5 0`, a naive descending-first strategy would produce `[5,4,3,2,1]`, which has four descents instead of zero.

## Approaches

A brute-force approach would try all permutations of numbers from 1 to _n_ and count the descents until a permutation with exactly _k_ descents is found. The number of permutations is _n_! and counting descents takes O(n), so the total work is O(n! × n), which is infeasible even for small _n_, as 10! is already 3,628,800.

The key insight for an optimal solution is that each descent occurs when a larger number is immediately followed by a smaller one. To generate exactly _k_ descents, we can choose the first _k_ numbers to be the largest _k_ numbers in decreasing order, ensuring a descent at every position, and then append the remaining numbers in increasing order to avoid additional descents. This greedy construction guarantees exactly _k_ descents without trial-and-error.

The greedy approach works because each descent is controlled directly by choosing a number larger than the next. Once we place the first _k_ numbers in descending order, any further numbers appended in ascending order cannot create extra descents, ensuring the decreasing coefficient is exactly _k_.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! × n) | O(n) | Too slow |
| Greedy Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers: `left = 1` and `right = n`. These represent the smallest and largest numbers available to place in the permutation.
2. Create an empty list `perm` to hold the final permutation.
3. Repeat _k_ times:

- Append `right` to `perm`. This places the largest available number to ensure a descent.
- Decrease `right` by 1. This removes the number from the available set.
4. Repeat for the remaining _n - k_ numbers:

- Append `left` to `perm`. This places the smallest available number, maintaining no further descents.
- Increase `left` by 1. This removes the number from the available set.
5. Output the `perm` list.

Why it works: Every descent is caused by placing a larger number before a smaller one. By taking the _k_ largest numbers in descending order, we ensure exactly _k_ descents at the start. Placing the remaining numbers in ascending order guarantees no additional descents. The invariant is that after each step, the number of descents placed equals the number of times we chose from the `right` pointer. This method cannot overproduce or underproduce descents.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

perm = []
left, right = 1, n

for _ in range(k):
    perm.append(right)
    right -= 1

for _ in range(n - k):
    perm.append(left)
    left += 1

print(" ".join(map(str, perm)))
```

The first loop ensures we get exactly _k_ descents by picking the largest numbers first. The second loop fills in the remaining numbers in increasing order to prevent any additional descents. The two-pointer approach avoids extra sorting or set operations, making it O(n).

## Worked Examples

**Sample 1**: `n = 5, k = 2`

| Step | left | right | perm |
| --- | --- | --- | --- |
| 0 | 1 | 5 | [] |
| 1 | 1 | 4 | [5] |
| 2 | 1 | 3 | [5, 4] |
| 3 | 1 | 3 | [5, 4, 1] |
| 4 | 2 | 3 | [5, 4, 1, 2] |
| 5 | 3 | 3 | [5, 4, 1, 2, 3] |

This produces `[5,4,1,2,3]` with two descents at positions 1→2 and 2→3.

**Sample 2**: `n = 4, k = 0`

| Step | left | right | perm |
| --- | --- | --- | --- |
| 0 | 1 | 4 | [] |
| 1 | 1 | 4 | [1] |
| 2 | 2 | 4 | [1,2] |
| 3 | 3 | 4 | [1,2,3] |
| 4 | 4 | 4 | [1,2,3,4] |

This produces `[1,2,3,4]` with zero descents.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is added exactly once in a linear pass |
| Space | O(n) | We store the final permutation of size n |

With _n_ ≤ 10^5, the algorithm executes within 2 seconds comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    perm = []
    left, right = 1, n
    for _ in range(k):
        perm.append(right)
        right -= 1
    for _ in range(n - k):
        perm.append(left)
        left += 1
    return " ".join(map(str, perm))

# provided sample
assert run("5 2\n") == "5 4 1 2 3", "sample 1"

# custom cases
assert run("4 0\n") == "1 2 3 4", "increasing permutation, k=0"
assert run("4 3\n") == "4 3 2 1", "fully decreasing permutation, k=n-1"
assert run("1 0\n") == "1", "single element, k=0"
assert run("6 2\n") == "6 5 1 2 3 4", "mixed descending/ascending"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 0 | 1 2 3 4 | Handles k=0 correctly |
| 4 3 | 4 3 2 1 | Handles k=n-1 correctly |
| 1 0 | 1 | Single-element edge case |
| 6 2 | 6 5 1 2 3 4 | Proper placement of k descents with remaining ascending |

## Edge Cases

For `k=0` with input `4 0`, the algorithm places no numbers from the right pointer, and all numbers are taken from the left, producing `[1,2,3,4]`. This correctly avoids any descents.

For `k=n-1` with input `4 3`, the algorithm takes the three largest numbers `[4,3,2]` from the right and the remaining smallest `[1]` from the left, producing `[4,3,2,1]`, giving exactly three descents.

For `n=1`, input `1 0`, the loops execute zero and one times respectively, producing `[1]`, which satisfies the requirement trivially.

This confirms the greedy approach handles minimum-size, maximum-size, and boundary cases correctly.
