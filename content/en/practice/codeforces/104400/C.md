---
title: "CF 104400C - Construct A Permutation"
description: "We are asked to construct a permutation of numbers from 1 to n that maximizes a nested alternating absolute expression of the form where differences are repeatedly taken between consecutive elements with absolute value applied at each subtraction level."
date: "2026-06-30T23:00:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104400
codeforces_index: "C"
codeforces_contest_name: "Hunan University 2023 the 19th Programming Contest"
rating: 0
weight: 104400
solve_time_s: 47
verified: true
draft: false
---

[CF 104400C - Construct A Permutation](https://codeforces.com/problemset/problem/104400/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a permutation of numbers from 1 to n that maximizes a nested alternating absolute expression of the form where differences are repeatedly taken between consecutive elements with absolute value applied at each subtraction level. Conceptually, we arrange the numbers so that when we evaluate this “alternating absolute subtraction chain”, the final value is as large as possible.

The input is a single integer n, and the output is any permutation of length n that maximizes this expression. Since the output is a permutation, every integer from 1 to n must appear exactly once.

The constraint n ≤ 10^6 immediately rules out any approach that tries to evaluate the objective function over permutations. The number of permutations is n!, which is far too large even for n = 20. Even trying to simulate the expression for a fixed permutation is O(n), so brute forcing all permutations would be O(n · n!), which is completely infeasible.

A subtle edge case is that the expression structure depends heavily on ordering, not just the multiset. For example, for n = 3, permutations like [1, 3, 2] and [3, 1, 2] produce different intermediate absolute values even though they contain the same elements. A greedy local swap approach can easily fail because early decisions affect all remaining operations.

## Approaches

The key difficulty is understanding how the alternating absolute subtraction behaves. The expression repeatedly takes a current value and subtracts the next element, then wraps the result in an absolute value, and continues.

If we expand the structure, we notice that the final result is heavily influenced by how large values are placed early in the sequence and how small values are used to “amplify” differences via sign flipping before absolute values collapse the structure.

A brute force approach would try all permutations, compute the expression in O(n) time each, and track the maximum. This is correct but immediately breaks down because it requires O(n!) permutations, which is impossible for n up to 10^6.

The key observation is that the absolute value destroys sign information at every step, which means we are essentially controlling the magnitude of intermediate results by choosing when large jumps occur. To maximize the final value, we want to force the expression to repeatedly create large differences instead of cancelling them out. This is achieved by alternating between large and small values so that each subtraction step produces a large magnitude before absolute value is applied.

This structure leads to a simple optimal construction: place the largest number first, then interleave remaining numbers from the opposite ends of the range. This guarantees that every subtraction step produces a large gap between the current value and the next chosen element, avoiding cancellation effects.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n) | Too slow |
| Alternating construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

The optimal strategy is to build a permutation by alternating between the largest remaining and smallest remaining values.

1. Initialize two pointers, low = 1 and high = n. We maintain that all numbers in [low, high] are not yet used.
2. Start building the answer list. We begin by taking the largest remaining value, high, and append it. We then decrement high because it is now used. Starting from the largest value ensures early large gaps in the expression.
3. Next, we take the smallest remaining value, low, and append it, then increment low. This creates a strong contrast with the previous large value.
4. We continue alternating: take from high, then low, repeatedly until all numbers are used.
5. If one pointer crosses the other, stop. This handles both even and odd n naturally.

The reason we alternate is that consecutive extreme differences maximize the magnitude of intermediate results before the absolute value is applied. If we placed numbers in sorted order, differences would be small and cancellations would dominate, reducing the final value.

### Why it works

At every step of the constructed permutation, the next chosen value is an extreme of the remaining interval. This guarantees that the difference between consecutive chosen elements is always as large as possible given what remains. Since the expression applies absolute value after each subtraction, the sign of intermediate results does not matter, only the magnitude of the difference at each step. The construction ensures that every step produces a near-maximum possible gap, and no rearrangement of remaining elements can increase any local transition without decreasing another. This yields a globally optimal sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    l, r = 1, n
    res = []
    
    while l <= r:
        res.append(r)
        r -= 1
        if l <= r:
            res.append(l)
            l += 1
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation maintains two pointers representing the smallest and largest unused values. Each iteration appends the current maximum, then the current minimum, shrinking the available range. This directly encodes the alternating strategy described earlier. The loop condition ensures we never reuse elements, and the final print outputs a valid permutation.

A subtle point is that we always append the high value first. Starting with low would produce a valid permutation but breaks the intended alternation pattern that maximizes early differences in the expression structure.

## Worked Examples

Consider n = 6.

We start with l = 1, r = 6.

| Step | l | r | Chosen | Current permutation |
| --- | --- | --- | --- | --- |
| 1 | 1 | 6 | 6 | [6] |
| 2 | 2 | 6 | 1 | [6, 1] |
| 3 | 2 | 5 | 5 | [6, 1, 5] |
| 4 | 3 | 5 | 2 | [6, 1, 5, 2] |
| 5 | 3 | 4 | 4 | [6, 1, 5, 2, 4] |
| 6 | 4 | 4 | 3 | [6, 1, 5, 2, 4, 3] |

This shows how extremes are progressively consumed, ensuring maximal spread at each step.

For n = 5, we proceed similarly.

| Step | l | r | Chosen | Current permutation |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 5 | [5] |
| 2 | 2 | 5 | 1 | [5, 1] |
| 3 | 2 | 4 | 4 | [5, 1, 4] |
| 4 | 3 | 4 | 2 | [5, 1, 4, 2] |
| 5 | 3 | 3 | 3 | [5, 1, 4, 2, 3] |

The odd case demonstrates that the middle element is naturally placed at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number from 1 to n is appended exactly once |
| Space | O(n) | We store the resulting permutation |

The algorithm is linear and works comfortably within limits even for n = 10^6, since it only performs a single pass with constant-time pointer updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    solve()
    
    return output.getvalue().strip()

# sample-style cases
assert run("1\n") == "1"
assert run("2\n") in ["2 1", "1 2"]

# small case
assert run("3\n") in ["3 1 2", "3 2 1"]

# even case
assert run("6\n") == "6 1 5 2 4 3"

# large structure sanity (just length check)
out = run("10\n").split()
assert sorted(map(int, out)) == list(range(1, 11))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 1 | minimal boundary |
| n=2 | 2 1 or 1 2 | smallest non-trivial swap |
| n=6 | 6 1 5 2 4 3 | alternating structure correctness |
| n=10 | permutation of 1..10 | validity under constraints |

## Edge Cases

For n = 1, the algorithm sets l = r = 1. It appends 1 once and terminates immediately, producing a valid permutation.

For n = 2, we start with l = 1, r = 2. The algorithm appends 2 then 1, producing [2, 1]. The loop ends because pointers cross. This confirms the alternating rule handles the smallest meaningful input without special casing.

For odd n such as n = 5, the last remaining element is the middle value. When l == r, it is appended once at the final step. The construction never skips this element because the loop condition allows equality.
