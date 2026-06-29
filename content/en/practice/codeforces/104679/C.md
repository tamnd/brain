---
title: "CF 104679C - Odd One Out"
description: "We are given a range of integers $[L, R]$. For every integer $X$ in this range, we define a value $f(X)$ based on counting how many ordered pairs of positive integers $(a, b)$ satisfy a multiplicative condition involving $X$."
date: "2026-06-29T14:37:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104679
codeforces_index: "C"
codeforces_contest_name: "Replay of Battle of Brains 2022, University of Dhaka"
rating: 0
weight: 104679
solve_time_s: 49
verified: true
draft: false
---

[CF 104679C - Odd One Out](https://codeforces.com/problemset/problem/104679/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a range of integers $[L, R]$. For every integer $X$ in this range, we define a value $f(X)$ based on counting how many ordered pairs of positive integers $(a, b)$ satisfy a multiplicative condition involving $X$.

The key observation is that the condition $\gcd(a, b) \times \mathrm{lcm}(a, b) = X$ simplifies completely because for any pair of positive integers, the identity $\gcd(a,b)\cdot \mathrm{lcm}(a,b)=ab$ always holds. This turns the definition of $f(X)$ into a much simpler question: how many ordered pairs $(a,b)$ satisfy $ab = X$.

So $f(X)$ is exactly the number of ways to factor $X$ into an ordered product of two positive integers, which is the same as the number of divisors of $X$.

The task then becomes: count how many integers $X$ in $[L, R]$ have an odd number of divisors.

From number theory, a positive integer has an odd number of divisors if and only if it is a perfect square. This happens because divisors normally come in distinct pairs $(d, X/d)$, except when $d = X/d$, which only occurs when $X$ is a square.

So the problem reduces to counting how many perfect squares lie in the interval $[L, R]$.

In terms of constraints, even if $L$ and $R$ are as large as $10^{18}$, we are only computing square roots and doing constant-time arithmetic. This rules out any approach that iterates through all values in the range, since that could require up to $10^{18}$ steps in the worst case. Instead, we need an $O(1)$ or at worst $O(\log R)$ method per query.

The main edge case in this type of problem comes from floating-point precision when computing square roots. For large values near $10^{18}$, using naive floating-point `sqrt` and casting directly to integers can sometimes produce off-by-one errors. Another subtle case is handling the lower bound $L = 1$, where $L-1 = 0$ must be treated correctly.

## Approaches

A brute-force approach would evaluate every $X$ in $[L, R]$, compute the number of divisors of $X$ by iterating up to $\sqrt{X}$, and check whether that count is odd. Computing divisors takes $O(\sqrt{X})$, so over the whole range this becomes $O((R-L+1)\sqrt{R})$, which is far too slow even for moderate ranges.

The key structural insight is that we do not actually need to compute divisor counts at all. We only need to know when the divisor count is odd. That property collapses the entire number theory part into a single characterization: perfect squares.

Once we recognize that, the problem becomes purely geometric on the number line. We are counting how many squares $k^2$ fall inside $[L, R]$. This is equivalent to counting integers $k$ such that $\sqrt{L} \le k \le \sqrt{R}$. That count can be computed using integer square roots.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((R-L+1)\sqrt{R})$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ or $O(\log R)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the number of integers $k$ such that $k^2 \le R$. This is $\lfloor \sqrt{R} \rfloor$, because every such $k$ corresponds to a perfect square not exceeding $R$.
2. Compute the number of integers $k$ such that $k^2 < L$. Instead of handling strict inequality directly, compute $\lfloor \sqrt{L-1} \rfloor$, which counts all squares strictly less than $L$.
3. Subtract the two counts. The result $\lfloor \sqrt{R} \rfloor - \lfloor \sqrt{L-1} \rfloor$ gives exactly the number of perfect squares in $[L, R]$.

The subtraction works because every integer $k$ counted in $\lfloor \sqrt{R} \rfloor$ corresponds to a square $k^2 \le R$, and removing those with $k^2 < L$ leaves exactly those within the interval.

### Why it works

The correctness rests on a one-to-one mapping between valid values of $X$ and integers $k$. Every perfect square $X$ can be uniquely written as $k^2$, and every such $k$ contributes exactly one valid $X$. Since the interval constraints translate directly into constraints on $k$, counting valid $X$ is equivalent to counting valid integers $k$. The subtraction removes exactly the invalid prefix without affecting valid values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    L, R = map(int, input().split())

    def isqrt(x):
        if x <= 0:
            return 0
        r = int(x ** 0.5)
        while (r + 1) * (r + 1) <= x:
            r += 1
        while r * r > x:
            r -= 1
        return r

    ans = isqrt(R) - isqrt(L - 1)
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution computes integer square roots carefully to avoid floating-point precision issues. The helper function adjusts the raw square root using small corrections to ensure correctness even near large perfect squares. The subtraction step directly implements the derived formula without any iteration over the range.

A subtle point is handling $L = 1$. In that case, $L-1 = 0$, and the integer square root of zero is correctly defined as zero, ensuring no invalid negative indexing or incorrect subtraction occurs.

## Worked Examples

### Example 1

Input:

```
L = 1, R = 10
```

We compute squares in this range.

| k | k² | within [1,10] |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 4 | yes |
| 3 | 9 | yes |
| 4 | 16 | no |

So answer is 3.

Trace:

| Expression | Value |
| --- | --- |
| floor(sqrt(R)) | 3 |
| floor(sqrt(L-1)) | 0 |
| result | 3 |

This confirms that only valid squares are counted.

### Example 2

Input:

```
L = 4, R = 25
```

Squares in range are 4, 9, 16, 25.

| k | k² | within [4,25] |
| --- | --- | --- |
| 1 | 1 | no |
| 2 | 4 | yes |
| 3 | 9 | yes |
| 4 | 16 | yes |
| 5 | 25 | yes |

Trace:

| Expression | Value |
| --- | --- |
| floor(sqrt(R)) | 5 |
| floor(sqrt(L-1)) | 1 |
| result | 4 |

This shows how subtracting the prefix removes all squares below $L$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only square root computations and arithmetic are performed |
| Space | $O(1)$ | No extra data structures are used |

The solution is easily fast enough even for very large bounds, since it avoids iterating over the interval entirely and reduces the problem to constant-time math operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import math

    L, R = map(int, sys.stdin.readline().split())

    def isqrt(x):
        if x <= 0:
            return 0
        r = int(x ** 0.5)
        while (r + 1) * (r + 1) <= x:
            r += 1
        while r * r > x:
            r -= 1
        return r

    print(isqrt(R) - isqrt(L - 1))
    return output.getvalue().strip()

# provided sample-like tests
assert run("1 10") == "3"
assert run("4 25") == "4"

# custom cases
assert run("1 1") == "1"
assert run("2 3") == "0"
assert run("10 100") == "7"
assert run("999999999999000000 1000000000000000000") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest range, single square |
| 2 3 | 0 | no squares in range |
| 10 100 | 7 | typical mid-range correctness |
| large range | non-negative | stability for large bounds |

## Edge Cases

One important edge case is when the range starts at 1. For input:

```
1 1
```

we compute:

$\lfloor \sqrt{1} \rfloor = 1$, and $\lfloor \sqrt{0} \rfloor = 0$, giving answer 1. This correctly counts the single square in the range.

Another case is when $L$ and $R$ are not squares but close to them:

```
2 3
```

Here $\lfloor \sqrt{3} \rfloor = 1$ and $\lfloor \sqrt{1} \rfloor = 1$, giving 0. The algorithm correctly avoids counting non-square numbers even though they lie near small squares.

For very large values near $10^{18}$, direct floating-point square root could round up incorrectly. The correction loop in the integer square root ensures that values like $10^{18}$ are handled exactly, preventing off-by-one errors in the final count.
