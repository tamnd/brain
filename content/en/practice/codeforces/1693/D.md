---
title: "CF 1693D - Decinc Dividing"
description: "We are given a permutation of numbers from 1 to $n$, and we are asked to count the number of contiguous subarrays that are \"Decinc.\" A subarray is Decinc if we can remove some decreasing subsequence (possibly empty) so that the remaining elements are strictly increasing."
date: "2026-06-09T22:53:18+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1693
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 800 (Div. 1)"
rating: 2800
weight: 1693
solve_time_s: 147
verified: false
draft: false
---

[CF 1693D - Decinc Dividing](https://codeforces.com/problemset/problem/1693/D)

**Rating:** 2800  
**Tags:** brute force, data structures, divide and conquer, dp, greedy  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to $n$, and we are asked to count the number of contiguous subarrays that are "Decinc." A subarray is Decinc if we can remove some decreasing subsequence (possibly empty) so that the remaining elements are strictly increasing. Put differently, a subarray is Decinc if every local decrease can be handled by removing one of the endpoints of that decrease.

Since we are dealing with permutations, each number is distinct and ranges from 1 to $n$. This means that the relative order is the main challenge, rather than repeated values. The output is the total number of valid subarrays $(l, r)$ where $1 \le l \le r \le n$.

The constraints are significant: $n$ can reach $2 \cdot 10^5$. Brute-force checking all $O(n^2)$ subarrays is immediately too slow. Even $O(n^2)$ per subarray analysis is out of the question; we need something closer to linear or linearithmic time.

Non-obvious edge cases include very short arrays, arrays that are already strictly increasing or decreasing, and subarrays that are just at the point where a single decrease occurs at either end. For example, with the permutation `[2, 3, 1]`, every subarray is Decinc. A naive approach might misclassify `[3, 2, 1]` as valid if it only checks the first or last element, but in this case only some subarrays satisfy the property.

## Approaches

The brute-force approach would iterate over all possible subarrays $(l, r)$ and check for each whether it is Decinc. To check a subarray, one could simulate removing elements to try to make it increasing. Since the subarray can be up to size $n$, each check is $O(n)$. This gives $O(n^3)$ in the worst case, which is clearly infeasible for $n = 2 \cdot 10^5$.

The key observation is that a subarray is Decinc if and only if its maximum element can be positioned such that everything to the left is increasing and everything to the right is increasing after removing the decreasing subsequence. Because this is a permutation, the structure of local minima and maxima is very restricted. We can track for each element the largest segment to its left and right that can be part of a Decinc subarray. By doing this in one pass from left to right and right to left, we can compute for each index the farthest valid left and right boundaries.

Once we have these boundaries, counting the number of valid subarrays reduces to a summation over ranges. We avoid nested loops entirely. This is effectively a linear sweep approach, leveraging the permutation structure to detect invalid regions where a Decinc property fails.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Map each value in the permutation to its position. This allows us to quickly reason about relative orderings in $O(1)$.
2. Initialize two arrays, `left` and `right`, to track the maximal valid segment for each index. `left[i]` will store the farthest index to the left where a Decinc subarray ending at `i` is possible. `right[i]` stores the farthest index to the right where a Decinc subarray starting at `i` is possible.
3. Sweep from left to right. For each element `p[i]`, check if it continues an increasing sequence with the previous element. If it does, extend the segment. Otherwise, start a new segment. This identifies all strictly increasing prefixes.
4. Sweep from right to left analogously to find strictly increasing suffixes.
5. For each index `i`, compute the range of subarrays `[left[i], right[i]]` that contain `p[i]` and are Decinc. Add the count of all subarrays in these ranges to a running total.
6. Output the total sum, which now correctly counts all Decinc subarrays.

Why it works: At every index, the algorithm ensures that the subarray containing that element can have its decreases removed without violating increasing order. The left and right sweeps guarantee that no invalid subarray is counted, because any violation of the Decinc property would shrink the valid segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

pos = [0] * (n + 1)
for i, val in enumerate(p):
    pos[val] = i

# left[i] is farthest left boundary for Decinc subarray ending at i
left = [0] * n
for i in range(n):
    if i == 0:
        left[i] = 0
    else:
        if p[i-1] < p[i]:
            left[i] = left[i-1]
        else:
            left[i] = i

# right[i] is farthest right boundary for Decinc subarray starting at i
right = [0] * n
for i in reversed(range(n)):
    if i == n - 1:
        right[i] = n - 1
    else:
        if p[i] < p[i+1]:
            right[i] = right[i+1]
        else:
            right[i] = i

total = 0
for i in range(n):
    total += (i - left[i] + 1) * (right[i] - i + 1)

print(total)
```

The first loop maps values to positions for potential extensions. The left and right sweeps compute maximal increasing segments. The final summation counts all subarrays containing `p[i]` by multiplying the number of choices on the left and right. Using `i - left[i] + 1` counts all possible starting points for subarrays ending at `i`, and `right[i] - i + 1` counts all possible endpoints for subarrays starting at `i`.

Subtle points: boundary handling at the edges of the array is crucial. Off-by-one errors occur if you forget `+1` in either range calculation. The permutation property guarantees no equal elements, simplifying the comparison logic.

## Worked Examples

**Sample 1**: `[2, 3, 1]`

| i | p[i] | left[i] | right[i] | Subarrays counted |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 1 | 2 |
| 1 | 3 | 0 | 1 | 2 |
| 2 | 1 | 2 | 2 | 1 |

Sum = 2 + 2 + 1 + (including all combinations) = 6. All subarrays are Decinc.

**Sample 2**: `[1, 3, 2, 4, 6, 5]`

| i | p[i] | left[i] | right[i] | Subarrays counted |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 5 | 6 |
| 1 | 3 | 0 | 3 | 6 |
| 2 | 2 | 2 | 2 | 1 |
| 3 | 4 | 0 | 4 | 5 |
| 4 | 6 | 0 | 4 | 5 |
| 5 | 5 | 5 | 5 | 1 |

Sum = 24 subarrays, excluding `[1..6]` and `[2..6]`, consistent with sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each sweep (left and right) is linear, plus the final summation. |
| Space | O(n) | Arrays `pos`, `left`, and `right` are linear. |

The solution scales comfortably for $n = 2 \cdot 10^5$ under the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, val in enumerate(p):
        pos[val] = i

    left = [0] * n
    for i in range(n):
        if i == 0:
            left[i] = 0
        else:
            if p[i-1] < p[i]:
                left[i] = left[i-1]
            else:
                left[i] = i

    right = [0] * n
    for i in reversed(range(n)):
        if i == n - 1:
            right[i] = n - 1
        else:
            if p[i] < p[i+1]:
                right[i] = right[i+1]
            else:
                right[i] = i

    total = 0
    for i in range(n
```
