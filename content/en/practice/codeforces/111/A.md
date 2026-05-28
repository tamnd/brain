---
title: "CF 111A - Petya and Inequiations"
description: "We need to construct an array of n positive integers. The array must satisfy two conditions at the same time. The sum of squares of all elements must be at least x, while the ordinary sum of the elements must not exceed y. The task is not to optimize anything."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 111
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 85 (Div. 1 Only)"
rating: 1400
weight: 111
solve_time_s: 153
verified: false
draft: false
---

[CF 111A - Petya and Inequiations](https://codeforces.com/problemset/problem/111/A)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct an array of `n` positive integers. The array must satisfy two conditions at the same time.

The sum of squares of all elements must be at least `x`, while the ordinary sum of the elements must not exceed `y`.

The task is not to optimize anything. We only need to find one valid construction, or determine that no construction exists.

The constraints immediately rule out any expensive search. The value of `n` can reach `10^5`, so anything quadratic or exponential is impossible. The value of `x` is especially large, up to `10^12`, which means brute forcing candidate arrays is completely unrealistic. We need a direct mathematical construction that can be computed in linear time.

The key detail is that the square condition grows much faster than the ordinary sum. A single large number contributes enormously to the sum of squares while only contributing linearly to the ordinary sum. That observation strongly suggests concentrating most of the value into one element instead of spreading it evenly.

Several edge cases are easy to mishandle.

Consider:

```
1 10 3
```

We need one positive integer whose square is at least `10`, but whose value is at most `3`. The only possible element would need to satisfy both:

```
a^2 >= 10
a <= 3
```

No such integer exists, because `3^2 = 9`. The correct output is:

```
-1
```

A careless implementation might only check the square condition and print `4`, forgetting that the sum limit is violated.

Another subtle case is when the minimum possible sum already exceeds `y`.

```
5 100 4
```

All numbers must be positive, so the smallest possible sum is already `5`. Since `5 > 4`, the answer is impossible regardless of `x`. The correct output is:

```
-1
```

An implementation that focuses only on the square requirement may miss this immediately impossible scenario.

One more tricky example:

```
3 11 5
```

A naive idea is to distribute values evenly, for example `[2,2,1]`. The sum is valid:

```
2 + 2 + 1 = 5
```

But the square sum is only:

```
4 + 4 + 1 = 9
```

which is too small. The valid construction is:

```
3 1 1
```

because:

```
9 + 1 + 1 = 11
3 + 1 + 1 = 5
```

This demonstrates why concentrating value into one element is stronger than spreading it out.

## Approaches

A brute-force approach would try to generate arrays and check whether they satisfy the two inequalities. Even if we restricted each element to at most `y`, the number of arrays would still be astronomical. For example, with `n = 20` and `y = 20`, there are already `20^20` possible arrays. This is completely infeasible.

The brute-force idea works conceptually because checking a candidate array is easy. We can compute both sums in linear time. The problem is the search space.

The breakthrough comes from understanding how squares behave. Suppose we already fixed the total sum. Among all arrays with that sum, putting as much value as possible into one element maximizes the sum of squares.

For example:

```
5^2 = 25
```

while:

```
3^2 + 2^2 = 13
```

Splitting a number into smaller pieces reduces the square contribution.

That means the best strategy is extremely simple. Make `n - 1` elements equal to `1`, since all numbers must be positive. Put everything else into one large element.

Let that large element be `k`.

Then:

```
sum = k + (n - 1)
square_sum = k^2 + (n - 1)
```

We need:

```
k^2 + (n - 1) >= x
k + (n - 1) <= y
```

The smallest valid `k` for the square condition is:

```
k >= ceil(sqrt(x - (n - 1)))
```

If that `k` also satisfies the sum constraint, we have a valid construction. Otherwise, no solution exists.

This reduces the whole problem to a few arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read `n`, `x`, and `y`.
2. Reserve `n - 1` elements as `1`.

This is the smallest possible contribution from those positions, because all numbers must be positive.
3. Let the remaining element be `k`.

The total square sum becomes:

```
k^2 + (n - 1)
```
4. Compute the minimum `k` satisfying the square condition.

We need:

```
k^2 >= x - (n - 1)
```

So:

```
k = ceil(sqrt(x - (n - 1)))
```

If `x - (n - 1)` is already non-positive, then `k = 1` is enough.
5. Check whether the ordinary sum constraint is satisfied.

The total sum is:

```
k + (n - 1)
```

If this exceeds `y`, print `-1`.
6. Otherwise, print `k` followed by `n - 1` ones.

### Why it works

The construction minimizes the ordinary sum for any given square contribution.

Suppose we want a large square sum. Splitting value across multiple numbers is inefficient because:

```
(a + b)^2 > a^2 + b^2
```

for positive integers `a` and `b`.

So the maximum square contribution for a fixed ordinary sum is achieved by concentrating as much value as possible into one element. By setting all other elements to `1`, we leave the largest possible budget for a single large number.

If even this best possible arrangement cannot satisfy both inequalities simultaneously, then no other arrangement can.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

n, x, y = map(int, input().split())

need = x - (n - 1)

if need <= 1:
    k = 1
else:
    k = math.isqrt(need)
    if k * k < need:
        k += 1

if k + (n - 1) > y:
    print(-1)
else:
    print(k)
    for _ in range(n - 1):
        print(1)
```

The implementation follows the construction directly.

First, we reserve `n - 1` positions for ones. Their square contribution is also `n - 1`, so the remaining square requirement becomes:

```
x - (n - 1)
```

We then compute the smallest integer `k` whose square is large enough. Using `math.isqrt` avoids floating-point precision issues. `isqrt(v)` returns the floor of the square root, so we increase by one if needed.

The condition:

```
if need <= 1:
    k = 1
```

handles cases where the existing ones already almost satisfy the square condition. Since all values must remain positive, `k` cannot be zero.

The final check:

```
if k + (n - 1) > y:
```

is the crucial impossibility test. Even the most square-efficient construction violates the sum limit, so no solution exists.

The output order does not matter. Any valid array is accepted.

## Worked Examples

### Example 1

Input:

```
5 15 15
```

We compute:

```
need = 15 - 4 = 11
```

The smallest integer with square at least `11` is `4`.

| Step | Value |
| --- | --- |
| n - 1 ones contribution | 4 |
| Remaining square need | 11 |
| Chosen k | 4 |
| Total sum | 8 |
| Total square sum | 20 |

The produced array can be:

```
4 1 1 1 1
```

The sum is:

```
8 <= 15
```

and the square sum is:

```
16 + 1 + 1 + 1 + 1 = 20 >= 15
```

This trace demonstrates the core idea: one large value dominates the square sum.

### Example 2

Input:

```
3 11 5
```

We compute:

```
need = 11 - 2 = 9
```

The smallest valid `k` is `3`.

| Step | Value |
| --- | --- |
| n - 1 ones contribution | 2 |
| Remaining square need | 9 |
| Chosen k | 3 |
| Total sum | 5 |
| Total square sum | 11 |

The output is:

```
3 1 1
```

This example hits the sum limit exactly. It confirms that the algorithm handles equality correctly and does not require the sum to be strictly smaller than `y`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Printing the array dominates the runtime |
| Space | O(1) | Only a few variables are stored |

The arithmetic itself is constant time. The only linear work is outputting `n` integers, which easily fits within the constraints for `n <= 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    n, x, y = map(int, input().split())

    need = x - (n - 1)

    if need <= 1:
        k = 1
    else:
        k = math.isqrt(need)
        if k * k < need:
            k += 1

    if k + (n - 1) > y:
        print(-1)
    else:
        print(k)
        for _ in range(n - 1):
            print(1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("5 15 15\n") == "4\n1\n1\n1\n1\n"

# minimum size, impossible
assert run("1 10 3\n") == "-1\n"

# exact boundary
assert run("3 11 5\n") == "3\n1\n1\n"

# already satisfied by all ones
assert run("4 4 10\n") == "1\n1\n1\n1\n"

# impossible because minimum sum exceeds y
assert run("5 100 4\n") == "-1\n"

# large square requirement
out = run("2 1000000 2000\n")
vals = list(map(int, out.strip().split()))
assert len(vals) == 2
assert vals[0] + vals[1] <= 2000
assert vals[0] * vals[0] + vals[1] * vals[1] >= 1000000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 10 3` | `-1` | Single-element impossibility |
| `3 11 5` | `3 1 1` | Exact equality on both conditions |
| `4 4 10` | `1 1 1 1` | All ones already sufficient |
| `5 100 4` | `-1` | Minimum positive sum already too large |
| `2 1000000 2000` | Any valid array | Large values and square-root computation |

## Edge Cases

Consider the input:

```
1 10 3
```

The algorithm computes:

```
need = 10
```

The smallest valid square root ceiling is:

```
k = 4
```

But:

```
4 > 3
```

so the sum condition fails immediately. The algorithm prints:

```
-1
```

This correctly handles single-element impossibility cases.

Now consider:

```
5 100 4
```

Even before worrying about squares, five positive integers must sum to at least `5`.

The algorithm computes:

```
need = 96
k = 10
```

Then:

```
10 + 4 = 14
```

which exceeds `y = 4`.

The algorithm prints:

```
-1
```

This correctly captures the fact that the sum bound alone already makes the task impossible.

Finally, consider:

```
4 4 10
```

The reserved ones already contribute:

```
3
```

to the square sum, so:

```
need = 1
```

The algorithm keeps:

```
k = 1
```

and outputs:

```
1 1 1 1
```

The square sum is exactly `4`, satisfying the requirement with the smallest possible values.
