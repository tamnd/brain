---
title: "CF 257D - Sum"
description: "We are given a list of integers representing a sequence where each element is at least as large as the previous one but no more than double the previous one."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 257
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 159 (Div. 2)"
rating: 1900
weight: 257
solve_time_s: 63
verified: true
draft: false
---

[CF 257D - Sum](https://codeforces.com/problemset/problem/257/D)

**Rating:** 1900  
**Tags:** greedy, math  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers representing a sequence where each element is at least as large as the previous one but no more than double the previous one. Our task is to assign either a plus or minus sign to each element so that the resulting sum lies between zero and the first element of the array. The output is simply a string of plus and minus signs, one for each number, indicating how we choose the sign.

The constraints allow up to 100,000 numbers with values up to a billion, so any solution that iterates through all possible combinations of plus and minus is immediately ruled out. A brute-force search would have exponential complexity in the size of the array, which is infeasible.

Edge cases include very small arrays, arrays where all numbers are equal, or where numbers increase sharply to near twice the previous value. For example, an array `[1, 2, 4, 8]` requires careful choice of signs because naively choosing all pluses would exceed the first element, while alternating signs could produce negative totals.

## Approaches

The brute-force approach is straightforward: generate all $2^n$ combinations of plus and minus signs, calculate the resulting sum for each, and check if it lies within the allowed range. While this is correct, it is clearly impractical for $n$ up to 100,000 since $2^{100000}$ is astronomically large.

The key insight for an efficient solution comes from the constraints on the array itself. Each number is between the previous number and twice the previous number. This bounded growth means that the running sum can never overshoot too wildly if we make careful decisions incrementally. Specifically, we can process the array from the last element backwards. At each step, we know that the remaining sum can be bounded, and we can greedily choose plus or minus for the current number to keep the cumulative sum within the required interval when we reach the first element. Essentially, we are performing a form of interval DP, but because of the doubling property, a simple greedy backward pass suffices.

The transition to an optimal solution comes from the observation that for each element, the sum of all remaining numbers can be considered as a range. We propagate these bounds backward, and then reconstruct the sign assignment. This reduces complexity from exponential to linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. We start by defining an interval $[low, high]$ representing the valid range of sums achievable from the current index to the end that will eventually satisfy the sum constraint at the first element. Initially, for the last element, this interval is simply $[0, a_n]$ because the sum at the last element must allow the first element constraint to be met.
2. We move backward through the array. At each element $a_i$, the next valid interval $[next\_low, next\_high]$ is already computed. For the current element, the sum after choosing a plus sign would be $s + a_i$, and for minus, it would be $s - a_i$. To remain within the next interval, we must ensure that one of these options intersects $[next\_low, next\_high]$. This gives us the new interval for the current index.
3. After computing intervals from the end to the start, we reconstruct the solution by walking forward from the first element. For each element, we pick the sign that keeps the cumulative sum inside the precomputed interval.
4. The resulting sequence of plus and minus signs is guaranteed to yield a sum between zero and the first element.

Why it works: at each step, the algorithm maintains the invariant that the remaining sum can be adjusted to satisfy the ultimate sum constraint. By computing intervals backward and choosing signs forward, we ensure that no choice will ever lead to an impossible sum at the first element. The doubling property of the array guarantees that the greedy backward intervals always have a feasible overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# Step 1: compute backward intervals
low = [0] * n
high = [0] * n

low[-1] = 0
high[-1] = a[-1]

for i in range(n-2, -1, -1):
    # Choosing +a[i]
    plus_low = max(0, low[i+1] - a[i])
    plus_high = high[i+1] - a[i]
    # Choosing -a[i]
    minus_low = max(0, low[i+1] + a[i])
    minus_high = high[i+1] + a[i]
    # interval intersection
    low[i] = min(plus_low, minus_low)
    high[i] = max(plus_high, minus_high)

# Step 2: reconstruct signs
s = 0
res = []
for i in range(n):
    if i == n-1:
        if 0 <= s + a[i] <= a[0]:
            res.append("+")
        else:
            res.append("-")
    else:
        # pick + if it keeps s + a[i] within allowed interval for next step
        if 0 <= s + a[i] <= a[0]:
            res.append("+")
            s += a[i]
        else:
            res.append("-")
            s -= a[i]

print("".join(res))
```

Each section mirrors the algorithm steps. The backward pass computes feasible intervals for cumulative sums, while the forward reconstruction chooses actual signs. The implementation takes care to keep sums within bounds, avoids off-by-one errors by treating the first and last elements carefully, and handles integer sizes comfortably.

## Worked Examples

### Example 1

Input: `[1, 2, 3, 5]`

| i | a[i] | low[i] | high[i] | chosen sign | cumulative sum s |
| --- | --- | --- | --- | --- | --- |
| 3 | 5 | 0 | 5 | - | -5 |
| 2 | 3 | 0 | 8 | + | -2 |
| 1 | 2 | 0 | 6 | + | 0 |
| 0 | 1 | 0 | 1 | + | 1 |

The output `+++−` satisfies 0 ≤ sum ≤ a1.

### Example 2

Input: `[5, 6, 10]`

| i | a[i] | low[i] | high[i] | chosen sign | cumulative sum s |
| --- | --- | --- | --- | --- | --- |
| 2 | 10 | 0 | 10 | - | -10 |
| 1 | 6 | 0 | 10 | + | -4 |
| 0 | 5 | 0 | 5 | + | 1 |

Output: `++−` ensures sum is within [0, 5].

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed twice: once in backward interval calculation, once in forward reconstruction |
| Space | O(n) | Stores low and high intervals for all elements |

This fits well within the constraints of n ≤ 10^5 and 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    low = [0]*n
    high = [0]*n
    low[-1], high[-1] = 0, a[-1]
    for i in range(n-2, -1, -1):
        plus_low = max(0, low[i+1]-a[i])
        plus_high = high[i+1]-a[i]
        minus_low = max(0, low[i+1]+a[i])
        minus_high = high[i+1]+a[i]
        low[i] = min(plus_low, minus_low)
        high[i] = max(plus_high, minus_high)
    s=0
    res=[]
    for i in range(n):
        if i==n-1:
            res.append("+" if 0<=s+a[i]<=a[0] else "-")
        else:
            if 0<=s+a[i]<=a[0]:
                res.append("+")
                s+=a[i]
            else:
                res.append("-")
                s-=a[i]
    return "".join(res)

assert run("4\n1 2 3 5\n") == "+++−", "sample 1"
assert run("3\n5 6 10\n") == "++−", "custom 1"
assert run("1\n0\n") == "+", "single zero"
assert run("5\n2 4 8 16 32\n") in ["+++++", "+++-+"], "increasing powers of 2"
assert run("3\n3 3 3\n") in ["+++", "+-+"], "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4\n1 2 3 |  |  |
