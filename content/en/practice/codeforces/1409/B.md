---
title: "CF 1409B - Minimum Product"
description: "We start with two numbers, a and b. We are allowed to perform at most n decrement operations. Each operation decreases either a or b by exactly one. The catch is that a can never go below x, and b can never go below y."
date: "2026-06-11T07:33:55+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1409
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 667 (Div. 3)"
rating: 1100
weight: 1409
solve_time_s: 106
verified: true
draft: false
---

[CF 1409B - Minimum Product](https://codeforces.com/problemset/problem/1409/B)

**Rating:** 1100  
**Tags:** brute force, greedy, math  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with two numbers, `a` and `b`. We are allowed to perform at most `n` decrement operations. Each operation decreases either `a` or `b` by exactly one. The catch is that `a` can never go below `x`, and `b` can never go below `y`.

The goal is to use up to `n` decrements in whatever way we want so that the final product `a × b` becomes as small as possible.

The input contains up to 20,000 independent test cases. The values themselves can be as large as `10^9`, which immediately rules out any simulation that performs decrements one by one. A single test case could require considering up to a billion operations, and with 20,000 test cases that would be completely infeasible.

The interesting part of the problem is deciding where to spend the available decrements. Reducing either number lowers the product, but because the numbers have different lower bounds, the order in which we reduce them matters.

Consider the test case:

```
a=10, b=10, x=8, y=5, n=3
```

If we spend all three operations on `a`, we get:

```
7 operations not allowed because x=8
10 -> 8
product = 8 × 10 = 80
```

If we spend all three on `b`:

```
10 -> 7
product = 10 × 7 = 70
```

The second choice is better.

A common mistake is to always reduce the larger number first. For example:

```
a=12, b=8, x=8, y=7, n=2
```

Reducing only `a` gives:

```
10 × 8 = 80
```

But splitting the decrements gives:

```
11 × 7 = 77
```

which is smaller.

Another subtle case occurs when one variable reaches its lower bound before all operations are used.

```
a=10, b=11, x=9, y=1, n=10
```

We can only reduce `a` once. The remaining nine operations must go to `b`:

```
9 × 2 = 18
```

A solution that blindly spends all operations on one variable would fail here.

## Approaches

A brute-force viewpoint is to decide exactly how many operations are applied to `a`. Suppose we spend `k` decrements on `a`. Then we spend as many of the remaining `n-k` decrements on `b` as possible.

This idea is correct because once `k` is fixed, the best choice for `b` is obvious: reduce it as much as allowed.

The problem is that `k` could range up to `10^9`. Enumerating every possibility is impossible.

The key observation is that there are only two meaningful orders in which decrements can be applied.

Suppose we want to minimize a product. Every decrement is more valuable when applied to a larger number because reducing a larger factor decreases the product more.

That suggests two natural strategies:

First, reduce `a` as much as possible, then use any remaining operations on `b`.

Second, reduce `b` as much as possible, then use any remaining operations on `a`.

It turns out one of these two orders is always optimal.

Why? Any valid sequence of operations can be rearranged into one of these greedy orders without making the result worse. The only thing that matters is how many decrements each variable ultimately receives, and for a fixed total budget the best distribution is achieved by exhausting one side first. Since either variable might be the better one to exhaust first, we simply test both possibilities and take the smaller product.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) or O(number of distributions) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Consider the strategy "reduce `a` first".

Compute how much `a` can be decreased:

```
decrease_a = min(n, a - x)
```

Apply that reduction to `a`.
2. Compute how many operations remain.

```
remaining = n - decrease_a
```
3. Use the remaining operations on `b`, respecting its lower bound.

```
decrease_b = min(remaining, b - y)
```
4. Compute the resulting product.
5. Repeat the same process with the roles reversed.

First reduce `b` as much as possible, then spend any remaining operations on `a`.
6. Output the smaller of the two products.

### Why it works

Let the final reductions be `ra` and `rb`, where `ra + rb ≤ n`.

The final product is

```
(a - ra)(b - rb)
```

subject to

```
0 ≤ ra ≤ a-x
0 ≤ rb ≤ b-y
```

For any feasible solution, pushing additional reductions into one variable until it reaches its limit cannot increase the product. The only question is which variable should be exhausted first. The two possibilities are exactly:

```
a first, then b
b first, then a
```

Every optimal allocation corresponds to one of these boundary cases, so checking both and taking the minimum guarantees the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        a, b, x, y, n = map(int, input().split())

        # Strategy 1: reduce a first
        da = min(n, a - x)
        a1 = a - da
        rem = n - da

        db = min(rem, b - y)
        b1 = b - db

        prod1 = a1 * b1

        # Strategy 2: reduce b first
        db = min(n, b - y)
        b2 = b - db
        rem = n - db

        da = min(rem, a - x)
        a2 = a - da

        prod2 = a2 * b2

        print(min(prod1, prod2))

if __name__ == "__main__":
    solve()
```

The solution directly implements the two candidate orders.

The expression `a - x` is the maximum amount by which `a` can be reduced. Taking `min(n, a - x)` ensures we never violate the lower bound.

After reducing one variable, the remaining budget is computed and applied to the other variable in the same way.

The products can be as large as:

```
10^9 × 10^9 = 10^18
```

Python integers handle this safely without overflow.

A common implementation error is forgetting to restore the original values before testing the second strategy. The code avoids this by storing separate variables (`a1`, `b1`, `a2`, `b2`) for the two scenarios.

## Worked Examples

### Example 1

Input:

```
10 10 8 5 3
```

Strategy 1, reduce `a` first:

| Step | a | b | Remaining n |
| --- | --- | --- | --- |
| Initial | 10 | 10 | 3 |
| Reduce a | 8 | 10 | 1 |
| Reduce b | 8 | 9 | 0 |

Product:

```
8 × 9 = 72
```

Strategy 2, reduce `b` first:

| Step | a | b | Remaining n |
| --- | --- | --- | --- |
| Initial | 10 | 10 | 3 |
| Reduce b | 10 | 7 | 0 |

Product:

```
10 × 7 = 70
```

Answer:

```
70
```

This example shows why trying both orders is necessary.

### Example 2

Input:

```
12 8 8 7 2
```

Strategy 1, reduce `a` first:

| Step | a | b | Remaining n |
| --- | --- | --- | --- |
| Initial | 12 | 8 | 2 |
| Reduce a | 10 | 8 | 0 |

Product:

```
80
```

Strategy 2, reduce `b` first:

| Step | a | b | Remaining n |
| --- | --- | --- | --- |
| Initial | 12 | 8 | 2 |
| Reduce b | 12 | 7 | 1 |
| Reduce a | 11 | 7 | 0 |

Product:

```
77
```

Answer:

```
77
```

This trace demonstrates that spending some operations on each variable can be better than spending them all on one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

Even with 20,000 test cases, the total work is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        a, b, x, y, n = map(int, input().split())

        da = min(n, a - x)
        a1 = a - da
        rem = n - da
        db = min(rem, b - y)
        b1 = b - db
        p1 = a1 * b1

        db = min(n, b - y)
        b2 = b - db
        rem = n - db
        da = min(rem, a - x)
        a2 = a - da
        p2 = a2 * b2

        ans.append(str(min(p1, p2)))

    return "\n".join(ans)

# provided samples
assert run(
"""7
10 10 8 5 3
12 8 8 7 2
12343 43 4543 39 123212
1000000000 1000000000 1 1 1
1000000000 1000000000 1 1 1000000000
10 11 2 1 5
10 11 9 1 10
"""
) == "\n".join([
    "70",
    "77",
    "177177",
    "999999999000000000",
    "999999999",
    "55",
    "10"
])

# minimum values
assert run(
"""1
1 1 1 1 1
"""
) == "1", "already at lower bounds"

# all values equal
assert run(
"""1
5 5 5 5 100
"""
) == "25", "no reductions possible"

# boundary where one variable reaches its limit
assert run(
"""1
10 11 9 1 10
"""
) == "10", "remaining operations must go to b"

# very large values
assert run(
"""1
1000000000 1000000000 1 1 1000000000
"""
) == "999999999"

print("OK")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1` | `1` | Minimum-size instance |
| `5 5 5 5 100` | `25` | No reductions possible |
| `10 11 9 1 10` | `10` | One variable hits its lower bound immediately |
| `1000000000 1000000000 1 1 1000000000` | `999999999` | Largest-value arithmetic and 64-bit range |

## Edge Cases

### One variable cannot be reduced at all

Input:

```
a=5, b=10, x=5, y=1, n=4
```

The algorithm computes:

```
a-x = 0
```

So reducing `a` first changes nothing. All four operations go to `b`:

```
5 × 6 = 30
```

The second strategy reaches the same result. The lower bound on `a` is respected automatically because `min(n, a-x)` becomes zero.

### More operations than the total available reductions

Input:

```
a=10, b=10, x=8, y=7, n=100
```

Only

```
(10-8) + (10-7) = 5
```

reductions are possible.

The algorithm reduces both variables to their minimum values:

```
8 × 7 = 56
```

Extra operations are simply unused, which is allowed because the problem says "at most `n` operations".

### The better answer depends on the order

Input:

```
a=10, b=10, x=8, y=5, n=3
```

Reducing `a` first yields:

```
8 × 9 = 72
```

Reducing `b` first yields:

```
10 × 7 = 70
```

The algorithm evaluates both and returns `70`.

This is exactly the situation that breaks greedy solutions that commit to only one order.

### Splitting reductions is necessary

Input:

```
a=12, b=8, x=8, y=7, n=2
```

The best result is:

```
11 × 7 = 77
```

The second strategy naturally finds this by reducing `b` to its minimum first and then spending the remaining operation on `a`. Checking both orders guarantees that such mixed allocations are not missed.
