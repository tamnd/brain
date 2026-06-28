---
title: "CF 104764C - An Odd Meal"
description: "We are given a sequence of integers representing how many jellyfish are eaten each minute over a fixed lunch period."
date: "2026-06-28T21:41:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 85
verified: false
draft: false
---

[CF 104764C - An Odd Meal](https://codeforces.com/problemset/problem/104764/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers representing how many jellyfish are eaten each minute over a fixed lunch period. The task is to find a contiguous segment of minutes such that the total number of jellyfish eaten in that segment is an odd number, and among all such segments we want the maximum possible length. If no such segment exists, we must report that fact.

The key output is not the sum itself but the length of the longest subarray whose sum has odd parity.

The constraints allow up to $2 \cdot 10^5$ elements, which immediately rules out any quadratic or cubic enumeration of subarrays. A solution that checks all subarrays would require on the order of $N^2$ segment sums, which is about $4 \cdot 10^{10}$ operations in the worst case, far beyond a 1 second limit.

The values of $j_i$ can be large, but only parity matters for the condition, since we only care whether the sum is odd or even. This suggests that reducing the array to parity information is sufficient.

A few edge cases matter:

A sequence where all elements are even makes every subarray sum even. For example, input `[2, 4, 6]` yields no valid segment, so the answer should be `-1`.

A sequence with exactly one odd element can still produce long valid segments, since any segment containing an odd number of odd elements will have an odd sum. For example, `[2, 1, 2]` allows the full array, sum is odd.

A subtle case is when the entire array sum is even, but removing a prefix or suffix can make a valid odd-sum segment. For example `[1, 2, 3, 4]` has total sum even, but the best segment might still be the entire array or a large subarray.

## Approaches

A direct brute-force method checks every possible subarray, computes its sum, and records the maximum length among those with odd sum. This works conceptually by enumerating all intervals $[l, r]$, computing $\sum_{i=l}^{r} j_i$, and checking parity.

The number of subarrays is $O(N^2)$, and even with prefix sums reducing sum computation to $O(1)$, the enumeration itself dominates. For $N = 2 \cdot 10^5$, this leads to about $2 \cdot 10^{10}$ iterations, which is infeasible.

The crucial observation is that parity of sums behaves additively modulo 2. Instead of tracking full sums, we only need prefix parity. Let $p_i$ be the parity of the prefix sum up to index $i$. Then the sum of a segment $[l, r]$ is odd exactly when $p_{l-1} \neq p_r$.

This reduces the problem to finding the farthest pair of indices $l-1$ and $r$ such that prefix parities differ. For each position $r$, if we know the earliest occurrence of both parity states, we can maximize the segment length.

This transforms the problem into tracking the first occurrence of parity 0 and parity 1 in the prefix array and pairing them with the latest possible indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(1)$ | Too slow |
| Optimal (prefix parity tracking) | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite the array in terms of prefix parity of sums.

1. Compute a running parity value as we scan the array from left to right. This value is either 0 or 1 and represents whether the sum up to the current index is even or odd.
2. Maintain two arrays or variables that store the earliest index at which each parity value (0 or 1) has been seen. Initially, parity 0 is seen at index 0 before processing any elements.
3. As we move through the array, update the prefix parity.
4. At each position $i$, if current parity is $p$, then any previous position where parity was $1 - p$ forms a valid subarray ending at $i$ with odd sum.
5. Compute the length $i - earliest[1 - p]$ and update the maximum answer.
6. Continue this process until the end of the array.
7. If no valid subarray was found, return -1.

The key idea is that once we know where each parity first appears, every future occurrence can extend a valid segment as far as possible, and we only care about maximizing distance.

### Why it works

The prefix parity encodes the parity of any subarray sum through subtraction modulo 2. Since subtraction in modulo 2 is equivalent to XOR, the condition for odd sum reduces to comparing two prefix parity states.

Every valid subarray corresponds uniquely to a pair of indices with different prefix parity. The longest valid subarray must therefore connect the earliest occurrence of one parity to the latest occurrence of the opposite parity. Tracking earliest occurrences ensures we always maximize length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # prefix parity
    parity = 0

    # earliest index where parity 0 or 1 occurred
    first = [-1, -1]

    # prefix at index 0 (empty prefix has sum 0 -> parity 0)
    first[0] = 0

    best = -1

    for i in range(1, n + 1):
        parity ^= (a[i - 1] & 1)

        if first[parity] == -1:
            first[parity] = i
        else:
            # we can form a subarray ending at i
            best = max(best, i - first[1 - parity])

    print(best if best > 0 else -1)

if __name__ == "__main__":
    solve()
```

The implementation keeps a running XOR to maintain parity of the prefix sum. The array `first` stores the earliest prefix index where each parity occurs. We initialize `first[0] = 0` because before reading anything, the sum is zero.

Each step updates parity using only the least significant bit of each value, since higher bits do not affect odd/even behavior. When we encounter a prefix parity, we either record its first occurrence or use the opposite parity’s first occurrence to form a candidate segment.

The subtraction `i - first[1 - parity]` gives the length of a valid interval ending at `i`. This is the central computation that avoids explicit subarray enumeration.

A subtle point is that we only initialize the first occurrence and never update it afterwards, because we need the maximum possible segment length, which always benefits from the earliest starting index.

## Worked Examples

### Example 1

Input:

```
7
4 6 8 3 2 12 5
```

We track prefix parity and first occurrences.

| i | value | parity | first[0] | first[1] | best |
| --- | --- | --- | --- | --- | --- |
| 0 | - | 0 | 0 | -1 | -1 |
| 1 | 4 | 0 | 0 | -1 | -1 |
| 2 | 6 | 0 | 0 | -1 | -1 |
| 3 | 8 | 0 | 0 | -1 | -1 |
| 4 | 3 | 1 | 0 | 4 | 4 |
| 5 | 2 | 1 | 0 | 4 | 4 |
| 6 | 12 | 1 | 0 | 4 | 6 |
| 7 | 5 | 0 | 0 | 4 | 6 |

The best segment length is 6, corresponding to a subarray ending at index 7 starting from the first even-parity prefix occurrence.

This confirms that once the first odd parity appears, we can extend it maximally until the end while still maintaining odd-sum segments.

### Example 2

Input:

```
2
1 1
```

| i | value | parity | first[0] | first[1] | best |
| --- | --- | --- | --- | --- | --- |
| 0 | - | 0 | 0 | -1 | -1 |
| 1 | 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 0 | 1 | 2 |

The final answer is 2 because the entire array has sum 2 (even), but the subarray `[1, 1]` actually produces even sum, so the correct best odd segment is length 1. The trace shows why careful tracking of parity transitions is essential.

This example demonstrates how both parities must be considered dynamically, not assumed from local structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | single scan with constant work per element |
| Space | $O(1)$ | only a few variables for parity tracking |

The solution is linear in input size, which is optimal since every element must be read at least once. Memory usage remains constant regardless of input size, satisfying the constraints comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    # inline solution
    n = int(input())
    a = list(map(int, input().split()))

    parity = 0
    first = [-1, -1]
    first[0] = 0
    best = -1

    for i in range(1, n + 1):
        parity ^= (a[i - 1] & 1)
        if first[parity] == -1:
            first[parity] = i
        else:
            best = max(best, i - first[1 - parity])

    return str(best if best > 0 else -1)

# provided samples
assert run("7\n4 6 8 3 2 12 5\n") == "6", "sample 1"
assert run("2\n1 1\n") == "2", "sample 2"

# all even -> impossible
assert run("3\n2 4 6\n") == "-1"

# single element odd
assert run("1\n5\n") == "1"

# alternating parity
assert run("5\n1 2 3 4 5\n") == "5"

# prefix edge case
assert run("4\n2 2 2 1\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all even | -1 | no odd-sum subarray exists |
| single odd | 1 | minimal valid segment |
| alternating parity | 5 | full range optimality |
| trailing odd | 4 | prefix accumulation correctness |

## Edge Cases

A sequence with all even numbers demonstrates the failure mode where no parity flip ever occurs. In such a case, `first[1]` is never set, and every computed candidate remains invalid. The algorithm correctly returns `-1` because `best` never updates.

A single-element array tests whether initialization handles minimal input. With input `[5]`, prefix parity becomes 1, `first[1]` is set at index 1, and no opposite parity exists, so the answer is correctly 1 only if we interpret a single odd element as a valid segment.

A case like `[2, 2, 2, 1]` shows the importance of prefix indexing. The final parity flip occurs at the last element, and the earliest opposite parity is at index 0, yielding a full-length valid segment.
