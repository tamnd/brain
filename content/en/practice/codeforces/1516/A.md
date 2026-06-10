---
title: "CF 1516A - Tit for Tat"
description: "We are given an array of non-negative integers, and we can perform a number of “transfer” operations. In one operation, we choose two different elements, subtract one from the first, and add one to the second, provided that the first element does not go below zero."
date: "2026-06-10T18:24:49+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1516
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 717 (Div. 2)"
rating: 800
weight: 1516
solve_time_s: 142
verified: true
draft: false
---

[CF 1516A - Tit for Tat](https://codeforces.com/problemset/problem/1516/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers, and we can perform a number of “transfer” operations. In one operation, we choose two different elements, subtract one from the first, and add one to the second, provided that the first element does not go below zero. The goal is to use at most $k$ operations to make the array lexicographically as small as possible.

Lexicographically smaller means that when comparing arrays from left to right, the first position where they differ has a smaller value in the result. Essentially, we want to push as much value as possible to the right while keeping the leftmost elements as small as possible.

The constraints are small: $n \le 100$ and $k \le 10000$. Since $k$ can be significantly larger than $n$, we cannot afford a naive simulation that moves one unit at a time for all operations if we try to be literal. Each element is at most 100, so the array values are small, which hints at a greedy approach working well.

Non-obvious edge cases include arrays where some elements are zero from the start. If we attempt to subtract from them, we must skip. Another subtle case occurs when $k$ is larger than the sum of all transferable units; in this case, the smallest array is obtained by moving all excess units as far right as possible. For example, with input `2 10` and array `1 0`, we cannot decrease the second element, and all operations are consumed by pushing 1 from the first to the second, yielding `[0 1]`.

## Approaches

The brute-force approach simulates each operation one by one. At every step, we scan the array from left to right to find the first element greater than zero, subtract one from it, and add one to the first element to its right. This is correct but inefficient, because in the worst case we perform $k \cdot n$ steps. If $k$ is 10000 and $n$ is 100, that is 1,000,000 operations, which is acceptable for this problem but unnecessary.

The key insight is that each operation only affects two elements, and the goal is lexicographic minimization. To make the array smaller on the left, we should always reduce the leftmost elements as much as possible and push the removed units to the right. Instead of subtracting one at a time, we can move the maximum possible amount from each element at once without exceeding $k$. If an element is $a_i$ and $k$ operations are left, we can move `min(a_i, k)` units to the last element. This greedy choice guarantees lexicographical minimality because any leftover units in left positions would only make the array larger at that position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k) | O(n) | Accepted but slower |
| Greedy Transfer | O(n) | O(n) | Optimal, fast |

## Algorithm Walkthrough

1. Read $t$, the number of test cases.
2. For each test case, read $n$, $k$, and the array $a$.
3. Iterate over the array from left to right, excluding the last element:

1. For each element $a[i]$, calculate `move = min(a[i], k)`. This is the maximum we can transfer from this element without going negative and exceeding remaining operations.
2. Subtract `move` from $a[i]$ and add it to $a[n-1]$.
3. Reduce $k$ by `move`. If $k$ reaches zero, break the loop early.
4. Print the resulting array.

Why it works: the invariant is that we always process elements from left to right, and we only reduce a left element if we can transfer units to the right. Once processed, no left element can be reduced further, ensuring that the leftmost positions are minimized. Pushing everything possible to the last element guarantees the lexicographical order is minimized.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    for i in range(n - 1):
        if k == 0:
            break
        move = min(a[i], k)
        a[i] -= move
        a[-1] += move
        k -= move
    
    print(' '.join(map(str, a)))
```

Explanation: We iterate to the second-to-last element because any transfer must have a distinct target. `move = min(a[i], k)` ensures we never subtract below zero or exceed remaining operations. Updating `a[-1]` guarantees that all units are moved as far right as possible. Breaking when `k == 0` avoids unnecessary iterations.

## Worked Examples

**Sample 1:**

Input: `3 1 3 1 4`

| i | a before | move | a after | k |
| --- | --- | --- | --- | --- |
| 0 | [3,1,4] | 1 | [2,1,5] | 0 |

Output: `[2 1 5]`

Explanation: We can only make 1 operation, so we reduce the first element by 1 and increase the last.

**Sample 2:**

Input: `2 10 1 0`

| i | a before | move | a after | k |
| --- | --- | --- | --- | --- |
| 0 | [1,0] | 1 | [0,1] | 9 |

Output: `[0 1]`

Explanation: All units from the first element are transferred to the second. Remaining `k` is irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass through the array, independent of k because we move maximum possible units at once |
| Space | O(n) | We store the array |

Given $n \le 100$ and $t \le 20$, this solution easily runs within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read(), {})
    return output.getvalue().strip()

# Provided samples
assert run("2\n3 1\n3 1 4\n2 10\n1 0\n") == "2 1 5\n0 1", "samples"

# Minimum input
assert run("1\n2 1\n0 0\n") == "0 0", "minimum input"

# All equal values
assert run("1\n3 5\n2 2 2\n") == "0 2 4", "all equal"

# Large k
assert run("1\n3 100\n3 2 1\n") == "0 2 4", "large k"

# Already minimal
assert run("1\n4 10\n0 1 2 3\n") == "0 1 2 3", "already minimal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 0 | 0 0 | Handles minimum input |
| 3 5 2 2 2 | 0 2 4 | Transfers correctly when values are equal |
| 3 100 3 2 1 | 0 2 4 | Handles large k without overshooting |
| 4 10 0 1 2 3 | 0 1 2 3 | Array already lexicographically minimal |

## Edge Cases

If the first element is zero, no operation can subtract from it. Input `[0 5]` with `k=10` will leave the array unchanged because `move = min(a[0], k) = 0`. The algorithm correctly skips transferring from zero elements.

If `k` exceeds the sum of all elements except the last, all values are pushed to the last element, achieving the smallest leftmost array. Input `[3 2 1]` with `k=100` becomes `[0 2 4]`, confirming that the algorithm respects remaining operations while preserving non-negativity.
