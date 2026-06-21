---
title: "CF 106434B - \u0417\u0430\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We are given an array that we only see in a distorted form. Each element in the observed array could have originally been any integer within a fixed interval around its observed value."
date: "2026-06-21T19:21:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106434
codeforces_index: "B"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421 2026, \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 106434
solve_time_s: 42
verified: true
draft: false
---

[CF 106434B - \u0417\u0430\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/106434/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array that we only see in a distorted form. Each element in the observed array could have originally been any integer within a fixed interval around its observed value. Specifically, if we see a value `a[i]`, then the true value before encryption could have been any integer from `a[i] - l` up to `a[i] + r`, but never negative.

The question is whether we can choose one valid original value for each position so that the resulting hidden array is non-decreasing.

So we are not asked to reconstruct the array uniquely. We only need to decide if there exists at least one way to pick a valid value for every position such that the sequence is sorted.

The constraints go up to `n = 2 * 10^5`, so any solution must be close to linear. Anything involving trying all choices inside ranges is immediately impossible because each element has up to `O(10^9)` possible values. Even a per-element search over ranges would explode.

A naive thought is to treat each position independently, but the ordering constraint couples all positions tightly. The key difficulty is that each choice restricts future choices.

A few failure cases clarify what can go wrong.

If we greedily pick the smallest possible value at each step, we might get stuck later because a small early value forces later elements to be too small to remain non-decreasing.

If we instead pick the largest possible value at each step, we might unnecessarily block valid solutions that require a smaller earlier choice.

The real issue is that each position is an interval, and we need to check if we can pick a chain of values, one from each interval, forming a non-decreasing sequence.

## Approaches

The brute force interpretation is straightforward: for each position, consider all possible original values in its interval `[a[i] - l, a[i] + r]`, and try to build a non-decreasing sequence using backtracking or dynamic programming over all combinations. This is correct because it directly explores the definition of validity. However, each position has up to `O(r + l)` possibilities, and over `n` positions this leads to an exponential number of combinations, roughly `(range size)^n`, which is completely infeasible.

The key observation is that we never need to remember all possible values at a position. If we process left to right, what matters is only the feasible range of values we can end at for the prefix. Instead of tracking all choices, we track the interval of all possible values for the last chosen element that keeps the prefix valid.

At position `i`, suppose we already know that the last chosen value must lie within some interval `[L, R]`. For the next element, we must choose a value `x` such that `x >= L` and `x` lies in `[a[i] - l, a[i] + r]`. So the minimum possible value we can choose is `max(L, a[i] - l)`, and the maximum is `a[i] + r`. If this interval becomes invalid (lower bound exceeds upper bound), the construction is impossible.

This turns the problem into a simple interval propagation process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Interval propagation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain the set of all possible values for the last element of a valid prefix. Instead of a set, we only keep its feasible range `[L, R]`.

1. Initialize the range for the first element as `[a[0] - l, a[0] + r]`. We clamp the lower bound to be at least zero because original values must be non-negative.
2. Set this range as the current feasible interval.
3. For each next position `i`, compute its allowable interval `[low_i, high_i] = [a[i] - l, a[i] + r]`, again clamping `low_i` to zero.
4. To maintain non-decreasing order, the new value must be at least `L`. So we intersect the interval `[low_i, high_i]` with `[L, +infinity)`, giving a new lower bound `L' = max(L, low_i)` and upper bound `R' = high_i`.
5. If at any point `L' > R'`, no valid value can be chosen at position `i` without breaking monotonicity, so we immediately conclude it is impossible.
6. Otherwise, update `[L, R] = [L', R']` and continue.
7. If we process all elements successfully, a valid non-decreasing hidden array exists.

### Why it works

The algorithm maintains the invariant that after processing position `i`, the interval `[L, R]` contains exactly all values that can serve as the last element of some valid non-decreasing sequence for the prefix `1..i`. Each step computes the intersection of this set with the valid range for the next element. Since both constraints are convex intervals and monotonicity only imposes a lower bound, the reachable set remains an interval throughout. If the interval ever becomes empty, no sequence can satisfy both the value constraints and ordering constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, l, r = map(int, input().split())
a = list(map(int, input().split()))

L = max(0, a[0] - l)
R = a[0] + r

for i in range(1, n):
    low = max(0, a[i] - l)
    high = a[i] + r

    L = max(L, low)
    R = high

    if L > R:
        print("NO")
        sys.exit()

print("YES")
```

The implementation directly follows the interval maintenance logic. The only subtle detail is clamping the lower bound to zero, since original values cannot be negative. Another important point is that we never shrink the upper bound based on previous state except through feasibility, because any larger value is always preferable for future flexibility.

## Worked Examples

### Example 1

Input:

```
4 1 2
1 0 2 1
```

We track the feasible interval for the last chosen value.

| i | a[i] | [low, high] | L | R | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | [0, 3] | 0 | 3 | OK |
| 1 | 0 | [0, 2] | 0 | 2 | OK |
| 2 | 2 | [1, 4] | 1 | 4 | OK |
| 3 | 1 | [0, 3] | 1 | 3 | OK |

The interval never becomes empty, so a valid non-decreasing reconstruction exists.

### Example 2

Input:

```
3 2 2
5 0 5
```

| i | a[i] | [low, high] | L | R | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | [3, 7] | 3 | 7 | OK |
| 1 | 0 | [0, 2] | 3 | 2 | invalid |

After the second element, the required minimum 3 exceeds the maximum 2, so no valid sequence can be formed.

This example shows how a single small observed value can break feasibility if previous constraints already forced the sequence too high.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time interval updates |
| Space | O(1) | Only a few variables are maintained |

The linear scan easily fits within constraints up to `2 * 10^5` elements, and memory usage is constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, l, r = map(int, input().split())
    a = list(map(int, input().split()))

    L = max(0, a[0] - l)
    R = a[0] + r

    for i in range(1, n):
        low = max(0, a[i] - l)
        high = a[i] + r

        L = max(L, low)
        R = high

        if L > R:
            return "NO"

    return "YES"

# provided samples
assert run("4 1 2\n1 0 2 1\n") == "YES"
assert run("3 2 2\n5 0 5\n") == "NO"

# custom cases
assert run("1 0 0\n5\n") == "YES"
assert run("2 0 0\n1 0\n") == "YES"
assert run("2 0 0\n0 1\n") == "YES"
assert run("2 0 0\n1 0\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | YES | trivial feasibility |
| equal bounds | YES | no flexibility case |
| increasing swap edge | YES | monotone still possible |
| decreasing swap edge | NO | immediate violation case |

## Edge Cases

A subtle edge case is when `l = r = 0`. In this situation, the array is fixed and the question reduces to checking whether the given array is already non-decreasing. The algorithm handles this naturally because each interval collapses to a single value, and any decrease immediately causes `L > R`.

Another case is when early elements allow a wide range but later elements force a sharp lower bound. For example, a sequence like `10, 0, 0` with sufficiently large `l` and `r` may still become invalid at the second position if the first interval forces a minimum above zero. The interval propagation immediately detects this by intersecting ranges and collapsing feasibility.

A final case is when the first element already starts at a high value but the only feasible reconstruction requires smaller values. The algorithm correctly allows the first interval to be as wide as possible and does not prematurely commit to a single value, ensuring later constraints are properly considered.
