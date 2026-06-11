---
title: "CF 1206B - Make Product Equal One"
description: "We are given an array of integers. In one operation, we may choose any element and either increase it by 1 or decrease it by 1. Each such change costs one coin."
date: "2026-06-11T23:32:40+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1206
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 580 (Div. 2)"
rating: 900
weight: 1206
solve_time_s: 103
verified: true
draft: false
---

[CF 1206B - Make Product Equal One](https://codeforces.com/problemset/problem/1206/B)

**Rating:** 900  
**Tags:** dp, implementation  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. In one operation, we may choose any element and either increase it by 1 or decrease it by 1. Each such change costs one coin.

The goal is to modify the array so that the product of all elements becomes exactly 1, while spending the minimum possible number of coins.

Since the final product must be 1, every element in the final array must be either 1 or -1. Any value with absolute value greater than 1 would contribute unnecessary cost, because moving it further toward ±1 always decreases the number of operations needed. A zero also cannot remain zero because any product containing zero is zero.

The constraint $n \le 10^5$ immediately suggests that we need a linear or near-linear solution. Any approach that tries many possible final configurations or performs dynamic programming over products would be far too expensive. With 100,000 elements, an $O(n)$ scan is ideal.

Several edge cases deserve attention.

Consider an array containing only zero:

```
1
0
```

The answer is 1. We can change 0 into 1 in one operation. A solution that only counts negatives and positives may forget to handle zeros.

Consider an odd number of negatives with no zero available:

```
3
-1 -1 -1
```

The product is -1. To make the product equal to 1, one element must be changed from -1 to 1, costing 2 operations. The correct answer is 2. A careless greedy solution might stop after converting everything to the nearest ±1 and incorrectly return 0.

Now consider an odd number of negatives with at least one zero:

```
2
-1 0
```

The cheapest choice is to convert the zero into -1 for cost 1, giving product 1. The answer is 1. A solution that automatically converts every zero to 1 would spend 3 operations instead.

## Approaches

A brute-force viewpoint is to think about every element's final value and try all possible assignments of 1 and -1. Since each element has two possible final states, there are $2^n$ possible target arrays. For each assignment we could compute the cost and check whether the product equals 1.

This works conceptually because every valid final array consists only of 1s and -1s. The problem is the size of the search space. With $n=10^5$, even $2^{50}$ possibilities would already be impossible, let alone $2^{100000}$.

The key observation is that each element can be processed independently when computing the cheapest way to reach either 1 or -1.

For a positive number $x>0$, the cheapest contribution is to turn it into 1, costing $x-1$.

For a negative number $x<0$, the cheapest contribution is to turn it into -1, costing $-1-x$.

For zero, reaching either 1 or -1 costs exactly 1.

After making every element as close as possible to its natural target, the only remaining issue is the parity of the number of negative values. The product equals 1 if and only if the number of -1 values is even.

If the number of negatives is already even, we are done.

If it is odd, we need one more adjustment. When a zero exists, we can simply convert one zero into -1 instead of 1 for no extra cost beyond the usual 1 coin. Without a zero, we must change one final -1 into 1, which requires 2 additional operations.

This leads directly to a linear-time greedy solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize three variables: total cost, number of negative elements, and number of zeros.
2. Scan through the array once.
3. If the current value is positive, convert it conceptually to 1. Add $x-1$ to the cost.
4. If the current value is negative, convert it conceptually to -1. Add $-1-x$ to the cost and increment the negative counter.
5. If the current value is zero, add 1 to the cost and increment the zero counter.

A zero can become either 1 or -1 with the same cost, so for now we only record its existence.
6. After processing all elements, check whether the number of negatives is even.
7. If the number of negatives is even, the current cost is already optimal.
8. If the number of negatives is odd and at least one zero exists, no extra cost is needed.

One zero can be turned into -1 instead of 1, fixing the parity while still costing exactly 1 coin.
9. If the number of negatives is odd and there are no zeros, add 2 to the answer.

The only option is changing one final -1 into 1, which requires two operations.
10. Output the total cost.

### Why it works

For every nonzero element, the cheapest reachable value among $\{-1,1\}$ is determined independently. Any alternative choice costs more. For example, changing a positive number to -1 always costs exactly 2 more than changing it to 1.

After these local optimal choices, the only global condition is that the total number of -1 values must be even. If the parity is already correct, the locally optimal decisions form a globally optimal solution.

When the parity is wrong, the cheapest correction is either using an existing zero, which can become -1 at no extra cost, or paying exactly 2 additional operations to flip one final -1 into 1. No cheaper adjustment exists, so the algorithm always produces the minimum cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    cost = 0
    negatives = 0
    zeros = 0

    for x in a:
        if x > 0:
            cost += x - 1
        elif x < 0:
            cost += -1 - x
            negatives += 1
        else:
            cost += 1
            zeros += 1

    if negatives % 2 == 1 and zeros == 0:
        cost += 2

    print(cost)

solve()
```

The first loop computes the minimum cost to bring every element to its nearest useful value. Positive numbers move toward 1, negative numbers move toward -1, and zeros cost one operation to leave zero.

The variable `negatives` records how many elements naturally become -1. The variable `zeros` records whether we have the flexibility to repair parity for free.

The final condition is the only subtle part. An odd number of negatives means the product would be -1. If there is no zero available, one -1 must become 1, which costs exactly 2 additional operations. When at least one zero exists, that zero can become -1 instead of 1, fixing the parity without increasing the already counted cost.

Python integers easily handle the answer size, since the maximum possible cost is well below $10^{14}$.

## Worked Examples

### Example 1

Input:

```
2
-1 1
```

| Element | Cost Added | Negatives | Zeros | Total Cost |
| --- | --- | --- | --- | --- |
| -1 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 |

After the scan, the number of negatives is odd and there are no zeros.

We add 2 extra operations.

| Final Adjustment | Added Cost | Total |
| --- | --- | --- |
| Flip one -1 to 1 | 2 | 2 |

Answer: **2**

This example demonstrates the parity correction step. Every element is already at ±1, but the product is -1, so one additional adjustment is necessary.

### Example 2

Input:

```
5
-5 -3 5 3 0
```

| Element | Cost Added | Negatives | Zeros | Total Cost |
| --- | --- | --- | --- | --- |
| -5 | 4 | 1 | 0 | 4 |
| -3 | 2 | 2 | 0 | 6 |
| 5 | 4 | 2 | 0 | 10 |
| 3 | 2 | 2 | 0 | 12 |
| 0 | 1 | 2 | 1 | 13 |

The number of negatives is already even, so no extra adjustment is needed.

Answer: **13**

This trace shows how each element contributes independently to the answer. The final zero costs one operation, and the parity is already correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass through the array |
| Space | $O(1)$ | Only a few counters are stored |

The algorithm examines each element exactly once and performs only constant-time work per element. With $n = 10^5$, this easily fits within the 1-second time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    cost = 0
    negatives = 0
    zeros = 0

    for x in a:
        if x > 0:
            cost += x - 1
        elif x < 0:
            cost += -1 - x
            negatives += 1
        else:
            cost += 1
            zeros += 1

    if negatives % 2 == 1 and zeros == 0:
        cost += 2

    return str(cost)

# provided sample
assert run("2\n-1 1\n") == "2", "sample 1"

# minimum size, single zero
assert run("1\n0\n") == "1", "single zero"

# odd negatives, no zero
assert run("3\n-1 -1 -1\n") == "2", "parity correction"

# odd negatives, with zero
assert run("2\n-1 0\n") == "1", "zero fixes parity"

# all positive
assert run("4\n2 2 2 2\n") == "4", "convert all to 1"

# mixed values
assert run("5\n-5 -3 5 3 0\n") == "13", "editorial example"

# boundary-sized values
assert run("2\n1000000000 -1000000000\n") == "1999999998", "large magnitudes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Single-element zero case |
| `3 / -1 -1 -1` | `2` | Odd negatives without zeros |
| `2 / -1 0` | `1` | Zero can repair parity |
| `4 / 2 2 2 2` | `4` | All positive numbers |
| `5 / -5 -3 5 3 0` | `13` | Mixed values and zero handling |
| `2 / 1000000000 -1000000000` | `1999999998` | Large absolute values |

## Edge Cases

### Odd number of negatives and no zero

Input:

```
3
-1 -1 -1
```

The scan produces cost 0, negatives 3, zeros 0. The product would be -1 because the number of negatives is odd. Since there is no zero available, the algorithm adds 2 and returns 2.

This is the cheapest possible fix because changing one -1 into 1 requires exactly two operations.

### Odd number of negatives with a zero

Input:

```
2
-1 0
```

The scan produces cost 1, negatives 1, zeros 1. The negative count is odd, but a zero exists. Instead of converting the zero into 1, we convert it into -1 using the same one operation already counted.

The final array becomes `[-1, -1]`, whose product is 1. The answer remains 1.

### All zeros

Input:

```
3
0 0 0
```

Each zero contributes 1, giving cost 3. Negatives remain 0, which is even.

The algorithm returns 3. One valid final array is `[1, 1, 1]`.

### Single negative element

Input:

```
1
-1
```

The scan gives cost 0, negatives 1, zeros 0. The parity is odd, so the algorithm adds 2.

The final answer is 2, corresponding to changing `-1` into `1`.

This case is easy to overlook because the element is already at one of the target values, but the product requirement still forces an additional adjustment.
