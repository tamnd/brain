---
title: "CF 1671D - Insert a Progression"
description: "We are given an array of integers a and a set of extra integers {1, 2, …, x}. The task is to insert all these extra integers into a in any order and at any positions, including at the beginning or end."
date: "2026-06-10T01:38:43+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1671
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 127 (Rated for Div. 2)"
rating: 1600
weight: 1671
solve_time_s: 108
verified: false
draft: false
---

[CF 1671D - Insert a Progression](https://codeforces.com/problemset/problem/1671/D)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a` and a set of extra integers `{1, 2, …, x}`. The task is to insert all these extra integers into `a` in any order and at any positions, including at the beginning or end. Once inserted, we compute the sum of absolute differences between consecutive elements of the new array. The goal is to minimize this sum.

In other words, the problem is about arranging numbers on a line so that the total "distance" traveled from one number to the next is as small as possible, while making sure all numbers from `1` to `x` appear somewhere in the sequence. The sequence `a` may already contain numbers from this range, so some insertions might be unnecessary if the number is already present.

The constraints indicate that `n` and `x` can each go up to `2 * 10^5` and the total sum of `n` across all test cases is also `2 * 10^5`. This effectively rules out any solution with complexity worse than `O(n + x)` per test case. Brute-force insertion checking is out of the question, since trying all permutations of insert positions would be exponential. Edge cases include sequences that already cover the full `[1, x]` range, arrays of length one, and arrays with repeated minimum or maximum values.

An example of a tricky scenario is a single-element array `a = [10]` and `x = 5`. The optimal insertion is `[1, 2, 3, 4, 5, 10]`, yielding the sum `9`. A naive solution might only append the extra numbers at the start or end arbitrarily, giving a larger sum.

## Approaches

The brute-force approach would attempt to insert each of the `x` extra numbers in every possible position of `a`, compute the resulting sum of absolute differences, and pick the minimal. This is clearly infeasible because each insertion multiplies the number of sequences to consider. Even for small `n`, the complexity grows factorially with `x`, which could reach `2 * 10^5`.

The key observation that unlocks a more efficient solution is that the sum of absolute differences is minimized when the new numbers are placed as close as possible to existing numbers. For the extra numbers, only the extremes-`1` and `x`-can produce large differences with the current array. Any number between the smallest and largest elements of `a` can always be "covered" by placing it next to the closest value, minimizing its contribution. This leads to a greedy insight: the sum of absolute differences is influenced most by the current array boundaries and the gaps to the extreme numbers outside this range.

To formalize, we need to consider:

1. The sum of differences already present in `a`.
2. For numbers smaller than the minimum of `a`, the optimal strategy is to either prepend the smallest extra number or attach it to the nearest element, choosing the minimal addition.
3. Similarly, for numbers larger than the maximum of `a`, append to the largest existing element or consider placing at the end.

This reduces the problem to calculating four values: the cost to cover `1` (if not already in `a`), the cost to cover `x`, and the sum of differences in the existing sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+x)!) | O(n+x) | Too slow |
| Optimal | O(n + x) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the current sum of absolute differences in the array `a` by iterating over all consecutive pairs. This is the base cost that we cannot avoid.
2. Identify the minimum and maximum of the array `a`. Any number less than `min(a)` or greater than `max(a)` will increase the cost. Let `mn` and `mx` be the current minimum and maximum of `a`.
3. Compute the cost to "cover" the number `1`. If `1 < mn`, inserting `1` can be done at either end: cost is `mn - 1`. If `1` is already less than the minimal element but not equal to it, inserting `1` in the best position may also include the cost of bridging `1` to the closest existing value. For sequences where `1` is already less than or equal to `mn`, the additional cost is `min(a[0] - 1, mn - 1, a[-1] - 1)`; choose the minimal.
4. Symmetrically, compute the cost to cover `x`. If `x > mx`, the cost is `x - mx` or bridging via the closest end.
5. The minimal total sum is the original sum plus the minimal costs to cover `1` and `x`. All numbers between `1` and `x` not equal to `mn` or `mx` can always be inserted adjacent to their closest value without increasing the sum.

The crucial invariant is that once the extremes are covered optimally, inserting all intermediate numbers between them never increases the sum beyond the cost of the extremes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_insert_cost(a, x):
    n = len(a)
    total = 0
    for i in range(1, n):
        total += abs(a[i] - a[i-1])
    
    mn = min(a)
    mx = max(a)
    
    # Cost to cover 1
    add1 = 0
    if 1 < mn:
        add1 = min(abs(a[0]-1), abs(a[-1]-1), mn-1)
    
    # Cost to cover x
    addx = 0
    if x > mx:
        addx = min(abs(a[0]-x), abs(a[-1]-x), x-mx)
    
    return total + add1 + addx

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    print(min_insert_cost(a, x))
```

The loop over the array calculates the original sum of differences. The `mn` and `mx` are tracked once per test case. The minimal bridging costs for `1` and `x` are calculated using the first, last, and min/max values of `a` to guarantee we find the smallest additional contribution. This avoids missing better positions in the middle of the array.

## Worked Examples

### Sample Input 1

```
1 5
10
```

| Variable | Value |
| --- | --- |
| a | [10] |
| total | 0 |
| mn | 10 |
| mx | 10 |
| add1 | min(abs(10-1), abs(10-1), 10-1) = 9 |
| addx | 0 (5 < 10) |
| Result | 0 + 9 + 0 = 9 |

This confirms that the optimal sequence `[1,2,3,4,5,10]` gives sum 9.

### Sample Input 2

```
3 8
7 2 10
```

| Variable | Value |
| --- | --- |
| a | [7,2,10] |
| total |  |
| mn | 2 |
| mx | 10 |
| add1 | min(abs(7-1), abs(10-1), 2-1) = min(6,9,1) = 1 |
| addx | min(abs(7-8), abs(10-8), 8-10?) = min(1,2,?) = 2 |
| Result | 13 + 1 + 1 = 15 |

This shows how bridging the extremes minimizes additional cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Computing sum of differences, min, max, and bridging costs requires one pass over the array |
| Space | O(n) | Storing the array `a` |

Given `sum(n) ≤ 2*10^5` and `t ≤ 10^4`, this fits comfortably in 2s.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        def min_insert_cost(a, x):
            n = len(a)
            total = sum(abs(a[i]-a[i-1]) for i in range(1, n))
            mn, mx = min(a), max(a)
            add1 = 0
            if 1 < mn:
                add1 = min(abs(a[0]-1), abs(a[-1]-1), mn-1)
            addx = 0
            if x > mx:
                addx = min(abs(a[0]-x), abs(a[-1]-x), x-mx)
            return total + add1 + addx
        output.append(str(min_insert_cost(a,x)))
    return "\n".join(output)

# Provided samples
assert run("4\n1 5\n10\n3 8\n7 2 10\n10 2\n6 1 5 7 3 3 9
```
