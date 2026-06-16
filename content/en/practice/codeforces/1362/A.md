---
title: "CF 1362A - Johnny and Ancient Computer"
description: "We are given a starting number and a target number, and we are allowed to transform the starting value using a very specific set of operations."
date: "2026-06-16T11:29:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1362
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 647 (Div. 2) - Thanks, Algo Muse!"
rating: 1000
weight: 1362
solve_time_s: 226
verified: true
draft: false
---

[CF 1362A - Johnny and Ancient Computer](https://codeforces.com/problemset/problem/1362/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 3m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a starting number and a target number, and we are allowed to transform the starting value using a very specific set of operations. Each operation either multiplies the number by 2, 4, or 8, or divides it by 2, 4, or 8, with the restriction that division is only allowed when it does not break the integer nature of the value.

The task is to determine the minimum number of such operations needed to turn the initial number into the target number, or conclude that it is impossible.

The key difficulty is that the allowed multipliers and divisors are all powers of two, and each operation can change the exponent by 1, 2, or 3. This means the problem is really about adjusting the exponent of 2 in the prime factorization, while everything else in the number must remain unchanged.

The input size is large in value range, up to 10^18, but the number of test cases is small enough that we are expected to solve each case in constant or logarithmic time. Any approach that explores states or builds a graph of transformations is infeasible because the state space grows multiplicatively and numbers go far beyond any reasonable BFS range.

A subtle edge case appears when the odd parts of the numbers differ. For example, from 6 to 10, or 7 to 1, no sequence of multiplying or dividing by powers of two can ever change the odd component. A naive attempt that only tracks powers of two would incorrectly assume all numbers are reachable if the ratio is a power of two, ignoring this invariant.

Another edge case is when the numbers are already equal, where the answer must be zero operations, even though a naive decomposition approach might still attempt unnecessary adjustments.

## Approaches

The brute-force idea is to treat each number as a node in a graph and connect it to all values reachable by multiplying or dividing by 2, 4, or 8. Then we could run a shortest path search from a to b. This is correct in principle because every operation corresponds to an edge of cost one. However, the branching factor is up to six at every state, and values grow unbounded in both directions. Even with pruning, the number of reachable states explodes extremely quickly, making this approach infeasible for values up to 10^18.

The key observation is that multiplying or dividing by powers of two does not affect the odd component of a number. Every integer can be written uniquely as x = odd_part × 2^k. All allowed operations only modify k, never the odd_part. This immediately implies that if the odd parts of a and b differ, the answer is impossible.

Once the odd parts match, the problem reduces to adjusting the difference in exponents of two. We want to transform 2^ka into 2^kb, and each operation allows changing k by +1, +2, or +3, or the same in reverse direction. This becomes a simple problem of minimizing the number of steps to move between two integers using jumps of size up to 3. The optimal strategy is greedy: take the largest possible steps first, because larger jumps always reduce the remaining difference faster without affecting optimality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (graph BFS) | Exponential | Exponential | Too slow |
| Optimal (factorization + greedy exponent match) | O(log a + log b) | O(1) | Accepted |

## Algorithm Walkthrough

We solve each test case independently.

1. Factor both numbers into their odd component and power of two exponent. We repeatedly divide by 2 until the number becomes odd, counting how many divisions we performed.
2. If the resulting odd components are different, we immediately return -1 because no sequence of allowed operations can change odd factors.
3. Otherwise, we now only need to match the exponent counts of two.
4. Compute the absolute difference between the two exponents.
5. To reduce this difference, use the fact that each operation can change the exponent by at most 3. The minimum number of operations is obtained by greedily subtracting 3 whenever possible, then 2 or 1 for the remainder.
6. Output the total number of operations needed.

The subtle point is that the greedy decomposition works because all step sizes divide the maximum step size structure cleanly: using fewer large jumps never increases the number of operations needed compared to decomposing them into smaller ones.

### Why it works

Every number is uniquely represented as an odd component multiplied by a power of two. Since multiplication and division by powers of two only modify the exponent and never the odd part, the odd component is invariant across all operations. This partitions all numbers into disconnected groups, and within each group, movement is only along the exponent axis. On this axis, each operation changes position by at most three, so the shortest path is exactly the minimum number of jumps needed to cover the distance using steps of size up to three. This guarantees optimality.

## Python Solution

```
PythonRun
```

The code begins by extracting the odd part and exponent of two for both numbers. This isolates the invariant structure of the problem. The comparison of odd parts acts as a feasibility check, ensuring we do not attempt impossible transformations.

Once feasibility is confirmed, the exponent difference is computed. The final loop does not explicitly simulate operations; instead it compresses the optimal strategy into arithmetic. Since every operation can adjust the exponent by at most three, the number of operations is simply the ceiling of the difference divided by three.

## Worked Examples

### Example 1: a = 10, b = 5

We factor both numbers into odd part and exponent of two.

| Step | a value | odd(a) | exp(a) | b value | odd(b) | exp(b) | diff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| init | 10 | 5 | 1 | 5 | 5 | 0 | 1 |
| final | same odd part | valid |  |  |  |  |  |

The odd parts match, so transformation is possible. The exponent difference is 1, which requires one operation of dividing by 2. This matches the output 1.

### Example 2: a = 96, b = 3

We decompose both numbers.

| Step | value | odd part | exponent |
| --- | --- | --- | --- |
| a | 96 | 3 | 5 |
| b | 3 | 3 | 0 |

The odd parts are equal, so the transformation is possible. The exponent difference is 5. Using steps up to size 3, we can do 3 + 2, which takes 2 operations. This matches the output 2.

These examples show that the entire problem reduces cleanly to comparing powers of two after factoring out the invariant odd component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log n) | each test factorizes by dividing by 2 repeatedly |
| Space | O(1) | only a few integer variables are stored |

The constraints allow up to 1000 test cases with values up to 10^18. Dividing by two is logarithmic in the value size, so the solution easily fits within the time limit.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 10 | -1 | different odd parts |
| 8 1 | 1 | single division by 8 |
| 3 3 | 0 | identical values |
| 1024 1 | 1 | large exponent collapse |

## Edge Cases

A key edge case is when the numbers differ only in odd factor. For example, 7 and 1 differ in odd component, so no amount of allowed operations can connect them. The algorithm catches this immediately when comparing the reduced odd parts after stripping powers of two.

Another case is when one number is already equal to the other. For 1000 and 1000, both odd part and exponent match, producing zero operations without any further computation.

A more subtle case is when the exponent difference is small but not divisible by 3. For instance, a = 16 and b = 2 gives exponent difference 3 and 1 respectively after decomposition, so diff = 2. The algorithm correctly returns one operation, reflecting a single division by 4.
