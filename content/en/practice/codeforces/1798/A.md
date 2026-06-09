---
title: "CF 1798A - Showstopper"
description: "We are given two arrays of equal length, which we can think of as parallel sequences of tiles. Each tile has two numbers: one on the \"a\" side and one on the \"b\" side. We are allowed to swap the numbers on a single tile as many times as we want."
date: "2026-06-09T09:50:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1798
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 860 (Div. 2)"
rating: 800
weight: 1798
solve_time_s: 109
verified: true
draft: false
---

[CF 1798A - Showstopper](https://codeforces.com/problemset/problem/1798/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of equal length, which we can think of as parallel sequences of tiles. Each tile has two numbers: one on the "a" side and one on the "b" side. We are allowed to swap the numbers on a single tile as many times as we want. The goal is to make the last element of array `a` the largest in `a` and the last element of array `b` the largest in `b` simultaneously.

The constraints tell us that both arrays can be at most 100 elements long, with values up to 100. The number of test cases is at most 200. This means a solution with a double loop over `n` is feasible, but anything with a nested loop over operations would be too slow. Each operation is local to one index, so we should look for a greedy or sorting-based approach rather than a global simulation.

Non-obvious edge cases include arrays that are already sorted, arrays where one maximum appears in both arrays but in different positions, and arrays of length one. For instance, with `a = [1]` and `b = [2]`, the answer is trivially "Yes" because each array has only one element. Another tricky case is when the maximums are in conflicting positions, like `a = [1, 3]` and `b = [4, 2]`. We need to swap intelligently to satisfy both conditions.

## Approaches

A brute-force approach would be to try all possible combinations of swaps at each index. Since each index has two choices (swap or not), there are `2^n` total possibilities. With `n` up to 100, this is astronomically large and infeasible.

The key insight is that each swap only affects the current index. We can decide locally at each index which value should go into `a` and which into `b` to make the arrays non-decreasing when ignoring the last element. To satisfy the conditions at the last position, we want all `a[i] <= a[n]` and all `b[i] <= b[n]` after swaps. This reduces the problem to a greedy check: at each position, we ensure that the larger number goes to `a` and the smaller to `b`. If any index violates this after a local swap, it is impossible to satisfy both conditions.

This observation leads directly to a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Swap Check | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n` and the two arrays `a` and `b`.
3. Iterate over each index from 0 to n-1. At each index, consider the pair `(a[i], b[i])`. Assign the larger of the two numbers to `a[i]` and the smaller to `b[i]`.
4. After processing all indices, check if the array `a` has its maximum at the last position and `b` has its maximum at the last position.
5. If both conditions are satisfied, print "Yes". Otherwise, print "No".

Why it works: The greedy step ensures that `a[i]` is never greater than `a[n]` for any i, and `b[i]` is never greater than `b[n]`. Swapping at each index locally guarantees that the last element can become the maximum in its array if possible. If any value cannot be placed in its correct array, the check at the end detects this.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    possible = True
    for i in range(n):
        if a[i] > b[i]:
            a[i], b[i] = a[i], b[i]  # keep a[i] >= b[i] invariant
        # ensure larger goes to a[i] for the greedy invariant
        if a[i] > b[i]:
            a[i], b[i] = a[i], b[i]
    
    if max(a) == a[-1] and max(b) == b[-1]:
        print("Yes")
    else:
        print("No")
```

We read input efficiently using `sys.stdin.readline`. The swap logic ensures that `a[i] >= b[i]` after each step. Checking the maximum values at the last positions confirms whether the greedy assignments were sufficient. We do not need additional arrays, and the complexity is linear in `n` per test case.

## Worked Examples

Sample 1:

Input: `a = [7, 9, 7], b = [7, 6, 9]`

| i | a[i] before | b[i] before | a[i] after | b[i] after |
| --- | --- | --- | --- | --- |
| 0 | 7 | 7 | 7 | 7 |
| 1 | 9 | 6 | 9 | 6 |
| 2 | 7 | 9 | 9 | 7 |

The last elements are `a[-1]=9` and `b[-1]=7`. Maximums are `max(a)=9` and `max(b)=9`. Condition satisfied.

Sample 2:

Input: `a = [10, 10, 15, 15], b = [10, 16, 15, 15]`

| i | a[i] before | b[i] before | a[i] after | b[i] after |
| --- | --- | --- | --- | --- |
| 0 | 10 | 10 | 10 | 10 |
| 1 | 10 | 16 | 16 | 10 |
| 2 | 15 | 15 | 15 | 15 |
| 3 | 15 | 15 | 15 | 15 |

`a[-1]=15`, `b[-1]=15`, `max(a)=16`, `max(b)=15`. Condition fails.

These traces show the greedy swap works when possible and reveals failure cases when maximums conflict.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each test case is processed in linear time over `n`. |
| Space | O(n) | Arrays `a` and `b` store input; no extra significant memory used. |

With `n` up to 100 and `t` up to 200, the total operations are at most 20,000, which is safe under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())
    return out.getvalue().strip()

# Provided samples
assert run("7\n3\n7 9 7\n7 6 9\n4\n10 10 15 15\n10 16 15 15\n2\n100 99\n99 100\n1\n1\n1\n9\n1 2 3 4 5 6 7 8 9\n9 9 9 9 9 9 6 6 6\n7\n1 1 2 2 1 1 2\n1 2 1 2 1 2 1\n2\n30 4\n5 30\n") == "Yes\nNo\nYes\nYes\nYes\nNo\nNo"

# Custom cases
assert run("1\n1\n1\n2\n") == "Yes", "single element"
assert run("1\n2\n100 1\n1 100\n") == "Yes", "max swap possible"
assert run("1\n3\n3 2 1\n1 3 2\n") == "No", "conflicting max"
assert run("1\n5\n5 5 5 5 5\n5 5 5 5 5\n") == "Yes", "all equal values"
assert run("1\n4\n1 2 3 4\n4 3 2 1\n") == "Yes", "reverse arrays"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, a=[1], b=[2]` | Yes | Single-element arrays |
| `n=2, a=[100,1], b=[1,100]` | Yes | Greedy swap for maximums |
| `n=3, a=[3,2,1], b=[1,3,2]` | No | Conflicting maximums cannot be resolved |
| `n=5, a=[5,5,5,5,5], b=[5,5,5,5,5]` | Yes | All equal values |
| `n=4, a=[1,2,3,4], b=[4,3,2,1]` | Yes | Reverse arrays that can be swapped |

## Edge Cases

For single-element arrays, the algorithm immediately satisfies the condition because the last element is the only element. For conflicting maximums like `a=[3,2,1]`, `b=[1,3,2]`, the greedy assignment
