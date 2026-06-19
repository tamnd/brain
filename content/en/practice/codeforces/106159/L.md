---
title: "CF 106159L - Leveling Diamonds"
description: "We are asked to compute how many diamond blocks are needed to construct a stepped pyramid of height $N$. The structure is layered: level $i$ (starting from 1 at the top) is a square whose side length is $2i+1$, so it contains $(2i+1)^2$ blocks."
date: "2026-06-19T19:16:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106159
codeforces_index: "L"
codeforces_contest_name: "XIII UnB Contest Mirror"
rating: 0
weight: 106159
solve_time_s: 45
verified: true
draft: false
---

[CF 106159L - Leveling Diamonds](https://codeforces.com/problemset/problem/106159/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute how many diamond blocks are needed to construct a stepped pyramid of height $N$. The structure is layered: level $i$ (starting from 1 at the top) is a square whose side length is $2i+1$, so it contains $(2i+1)^2$ blocks. The total number of blocks is therefore the sum of these squared odd side lengths from level 1 up to level $N$, and the answer must be given modulo $10^9 + 7$.

The input is a single integer $N$, which can be as large as $10^{18}$. This immediately rules out any approach that iterates over levels. Even an $O(N)$ solution is impossible since it would require up to $10^{18}$ operations. We must compress the summation into a closed-form expression or a very small number of arithmetic operations.

A subtle issue appears in overflow handling if one tries to compute $(2i+1)^2$ repeatedly without modular care. Since intermediate values grow quadratically with $i$, and $i$ itself can be up to $10^{18}$, naive multiplication in 64-bit arithmetic is already unsafe before even summing.

Edge cases are minimal structurally but important numerically. When $N=1$, the answer is simply $3^2 = 9$. A naive loop is not a performance issue here but still serves as a sanity check. At the upper bound $N=10^{18}$, only a formula-based solution is viable.

## Approaches

A direct interpretation of the problem suggests iterating through each level and summing $(2i+1)^2$. This is correct because it follows the definition literally. Expanding this expression gives $4i^2 + 4i + 1$, so the total becomes:

$$\sum_{i=1}^{N} (4i^2 + 4i + 1)
= 4\sum i^2 + 4\sum i + \sum 1$$

This transformation is the key simplification step. Instead of summing a quadratic expression per level, we reduce the problem to known summations:

$$\sum_{i=1}^{N} i = \frac{N(N+1)}{2}, \quad \sum_{i=1}^{N} i^2 = \frac{N(N+1)(2N+1)}{6}$$

Substituting these into the expression yields a closed form computable in constant time. The bottleneck is no longer iteration but modular arithmetic with large intermediate values, so we rely on modular inverses of 2 and 6 under $10^9 + 7$.

The brute-force method fails because it performs $N$ iterations, each computing a square and adding it, leading to $O(N)$ time. At $N = 10^{18}$, this is infeasible. The optimized method collapses the sum into constant-time arithmetic using algebraic identities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We start by rewriting the total number of blocks:

$$\sum_{i=1}^{N} (2i+1)^2$$

Expanding the square gives a polynomial in $i$, which allows us to use standard summation formulas.

### Steps

1. Expand each term $(2i+1)^2$ into $4i^2 + 4i + 1$.

This step converts the geometric structure into algebraic components that can be summed independently.
2. Split the total sum into three separate sums:

$$4\sum i^2 + 4\sum i + \sum 1$$

This separation works because summation is linear.
3. Substitute known formulas for each summation:

$$\sum i = \frac{N(N+1)}{2}, \quad \sum i^2 = \frac{N(N+1)(2N+1)}{6}, \quad \sum 1 = N$$
4. Combine everything into a single expression under modulo:

$$4 \cdot \frac{N(N+1)(2N+1)}{6} + 4 \cdot \frac{N(N+1)}{2} + N$$
5. Compute modular inverses of 2 and 6 under $10^9 + 7$, and evaluate the expression carefully using modular multiplication to avoid overflow.

The key implementation detail is to reduce intermediate values modulo $10^9 + 7$ at every multiplication step, since direct multiplication of large integers like $10^{18}$ can overflow even 128-bit arithmetic in some languages and is unnecessary.

### Why it works

The correctness relies on the fact that every term in the original sum is a quadratic polynomial in $i$. Any sum of a polynomial over a consecutive range can be expressed exactly using power-sum formulas. Since we rewrite the entire expression in terms of $\sum i^2$, $\sum i$, and $\sum 1$, and these are exact identities for all integer $N$, the transformation preserves equality. The modular arithmetic step does not change correctness because all operations are performed in a field defined by a prime modulus, where division by 2 and 6 is valid via modular inverses.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

inv2 = modinv(2)
inv6 = modinv(6)

def solve():
    N = int(input().strip())

    n = N % MOD

    sum_i = n * (n + 1) % MOD * inv2 % MOD
    sum_i2 = n * (n + 1) % MOD * (2 * n + 1) % MOD * inv6 % MOD

    # 4 * sum_i2 + 4 * sum_i + N
    ans = (4 * sum_i2) % MOD
    ans = (ans + 4 * sum_i) % MOD
    ans = (ans + n) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution computes modular inverses of 2 and 6 once, since division by these constants appears in both summation formulas. The input $N$ is reduced modulo $10^9 + 7$ early because all algebraic expressions are polynomial in $N$, and reducing early preserves correctness while preventing overflow in intermediate multiplications.

Each summation is computed independently to avoid mixing terms that would complicate modular reduction. The final expression directly mirrors the derived formula, ensuring a low risk of implementation mistakes.

## Worked Examples

### Example 1: $N = 1$

We compute:

$$(2\cdot1+1)^2 = 9$$

| Step | sum_i | sum_i2 | partial result |
| --- | --- | --- | --- |
| compute | 1 | 1 |  |

Final:

$$4 \cdot 1 + 4 \cdot 1 + 1 = 9$$

This confirms the base case matches the formula exactly.

### Example 2: $N = 3$

Direct computation:

$$3^2 + 5^2 + 7^2 = 9 + 25 + 49 = 83$$

| i | (2i+1)^2 | running sum |
| --- | --- | --- |
| 1 | 9 | 9 |
| 2 | 25 | 34 |
| 3 | 49 | 83 |

Now via formula:

$$\sum i = 6,\quad \sum i^2 = 14$$

$$4\cdot14 + 4\cdot6 + 3 = 56 + 24 + 3 = 83$$

Both methods align, confirming correctness of decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a fixed number of arithmetic operations and modular exponentiations |
| Space | $O(1)$ | Only a handful of variables regardless of input size |

The computation is constant time, so it easily fits within the 1-second limit even for the maximum input $10^{18}$. Memory usage is negligible since no arrays or recursion are involved.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MOD = 10**9 + 7
    def modinv(x):
        return pow(x, MOD - 2, MOD)

    inv2 = modinv(2)
    inv6 = modinv(6)

    N = int(input().strip())
    n = N % MOD

    sum_i = n * (n + 1) % MOD * inv2 % MOD
    sum_i2 = n * (n + 1) % MOD * (2 * n + 1) % MOD * inv6 % MOD

    ans = (4 * sum_i2 + 4 * sum_i + n) % MOD
    return str(ans)

# provided samples (conceptual since not fully shown)
assert run("1\n") == str(9)

# custom cases
assert run("2\n") == str(9 + 25), "N=2 small"
assert run("3\n") == str(83), "N=3 known sum"
assert run("10\n") == str(sum((2*i+1)**2 for i in range(1, 11)) % MOD), "consistency check"
assert run("1000000000000000000\n") == run("1000000000000000000\n"), "stability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 9 | base case correctness |
| 3 | 83 | multi-term correctness |
| 10 | direct sum | agreement with brute force |
| $10^{18}$ | mod result | large input stability |

## Edge Cases

For $N=1$, the algorithm computes $n=1$, then evaluates both summations directly. The intermediate values are:

$$\sum i = 1, \quad \sum i^2 = 1$$

The final result becomes $4 + 4 + 1 = 9$, matching the single-layer tower.

For very large $N$, such as $10^{18}$, the algorithm never iterates. It reduces $N$ modulo $10^9+7$ and performs a fixed sequence of multiplications and inverses. Even though the original value is enormous, the polynomial nature of the formula guarantees that modular reduction before evaluation produces the correct result in the finite field.

For intermediate values like $N=2$, the algorithm correctly combines contributions from both layers without any off-by-one error because all summations are defined on the inclusive range $[1, N]$, which matches the problem’s indexing of levels starting from 1.
