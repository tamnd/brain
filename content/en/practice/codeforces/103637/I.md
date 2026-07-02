---
title: "CF 103637I - Items in boxes"
description: "We are given two integers. One of them, $n$, determines how many boxes exist, specifically $2n$ boxes in total. The second value, $a$, describes how many distinct items are inside each box, and every box is independent of the others. From each box we must pick exactly one item."
date: "2026-07-02T22:21:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103637
codeforces_index: "I"
codeforces_contest_name: "2019-2020 10th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 103637
solve_time_s: 43
verified: true
draft: false
---

[CF 103637I - Items in boxes](https://codeforces.com/problemset/problem/103637/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers. One of them, $n$, determines how many boxes exist, specifically $2n$ boxes in total. The second value, $a$, describes how many distinct items are inside each box, and every box is independent of the others.

From each box we must pick exactly one item. Since every box contains $a$ choices and all boxes are independent, the total number of ways to make a complete selection is the product of choices across all boxes. This raw count is then reduced modulo $2n + 2$, and that remainder is the required output.

The key difficulty is that both $n$ and $a$ can be as large as $10^9$, so the total number of boxes is also large, and the direct value $a^{2n}$ is astronomically large and cannot be computed explicitly.

The most important observation is that we are not asked for the full value, only its remainder modulo a number that is closely tied to the exponent structure, namely $2n + 2$. This makes the problem fundamentally about modular exponentiation with a modulus that depends on the exponent itself.

A naive failure case appears immediately if one tries to compute the power directly. For example, if $n = 10^9$ and $a = 2$, the value is $2^{2 \cdot 10^9}$, which is impossible to compute or even store. Even a modular exponentiation approach without noticing structure is still fine in complexity, but we must be careful with the modulus because it is not fixed.

Another subtle issue arises when $a$ is larger than the modulus. A careless implementation might assume reduction early is harmless, but because the modulus depends on $n$, the exponent and modulus interact in a nontrivial way, and we must preserve correctness under modular exponentiation rules.

## Approaches

The brute-force interpretation is straightforward: for each box, multiply the number of choices $a$, repeated $2n$ times. This gives $a^{2n}$. After computing this value, we take it modulo $2n + 2$.

This works conceptually because each box contributes an independent multiplicative factor. However, the computation itself is infeasible because exponentiation by repeated multiplication requires $2n$ multiplications, which can be up to $2 \cdot 10^9$, far beyond any reasonable time limit.

A natural improvement is to switch to fast exponentiation. This reduces the exponentiation cost from linear to logarithmic in $n$. However, the deeper insight is that the modulus is not arbitrary. It is exactly $2n + 2$, which is always even and strongly related to the exponent $2n$. This structure suggests that repeated squaring combined with modular reduction is sufficient, and no further number theory tricks like Euler’s theorem are required, since the modulus is not necessarily prime and $a$ is not guaranteed to be coprime.

Thus the optimal approach is simply binary exponentiation with modulus $2n + 2$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ multiplications | $O(1)$ | Too slow |
| Binary Exponentiation | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read integers $n$ and $a$. The number of boxes is $2n$, and the modulus is defined as $m = 2n + 2$.
2. Reduce the base $a$ modulo $m$. This does not change the final result because modular multiplication preserves equivalence, and it keeps intermediate values small.
3. Set the exponent $e = 2n$. We are computing $a^e \bmod m$.
4. Initialize the result as $res = 1$. This represents an empty product, which is the neutral element for multiplication.
5. While $e > 0$, process the exponent bit by bit. If the lowest bit of $e$ is 1, multiply the current result by $a$ modulo $m$. This ensures we include exactly the powers corresponding to the binary decomposition of the exponent.
6. Square the base $a = a^2 \bmod m$. This moves us to the next power of two.
7. Shift the exponent right by one bit, effectively dividing it by 2.

Each iteration reduces the exponent size exponentially, which is why the method is efficient even for very large inputs.

### Why it works

At every step, the algorithm maintains the invariant that $res \cdot a^e$ (where $a$ is the current base) is congruent to the original $a^{2n}$ modulo $m$. The binary representation of the exponent ensures that every power of two contributes exactly once when its corresponding bit is set. Since multiplication is associative under modular arithmetic, and each reduction preserves congruence, the final result matches the desired value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod_pow(a, e, mod):
    res = 1
    a %= mod
    while e > 0:
        if e & 1:
            res = (res * a) % mod
        a = (a * a) % mod
        e >>= 1
    return res

def solve():
    n, a = map(int, input().split())
    mod = 2 * n + 2
    exp = 2 * n
    print(mod_pow(a, exp, mod))

if __name__ == "__main__":
    solve()
```

The function `mod_pow` implements binary exponentiation. The base is reduced modulo `mod` immediately to avoid overflow growth during squaring. The loop processes the exponent bit by bit, multiplying into the result whenever the current bit contributes to the decomposition of the exponent.

The main function computes the modulus $2n + 2$, sets the exponent to $2n$, and delegates the computation to the modular exponentiation routine.

A common mistake is forgetting to reduce the base modulo `mod` before starting the loop. While not strictly required for correctness, it prevents intermediate values from growing unnecessarily large. Another subtle issue is mixing up exponent and modulus, since both depend on $n$.

## Worked Examples

### Example 1

Input:

```
n = 1, a = 2
```

We compute $2n = 2$ and modulus $m = 4$. So we evaluate $2^2 \bmod 4$.

| Step | res | base a | exponent e |
| --- | --- | --- | --- |
| init | 1 | 2 | 2 |
| use bit | 2 | 2 | 1 |
| square | 2 | 0 | 1 |
| final bit | 0 | 0 | 0 |

Result is $0$.

This confirms that even small cases may collapse under modular reduction, since the modulus is not prime and interacts strongly with the base.

### Example 2

Input:

```
n = 2, a = 3
```

We compute $2n = 4$, modulus $m = 6$, and evaluate $3^4 \bmod 6$.

| Step | res | base a | exponent e |
| --- | --- | --- | --- |
| init | 1 | 3 | 4 |
| use bit | 3 | 3 | 2 |
| square | 3 | 3 | 2 |
| use bit | 3 | 3 | 1 |
| square | 3 | 3 | 1 |
| final bit | 3 | 3 | 0 |

Final result is $3$.

This trace shows how binary exponentiation accumulates contributions only when exponent bits are active.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | Each step halves the exponent |
| Space | $O(1)$ | Only a few integer variables are used |

The constraints allow up to $10^9$, so any linear approach is impossible, but logarithmic exponentiation is easily fast enough within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, a = map(int, input().split())
    mod = 2 * n + 2

    def mod_pow(a, e, mod):
        res = 1
        a %= mod
        while e > 0:
            if e & 1:
                res = (res * a) % mod
            a = (a * a) % mod
            e >>= 1
        return res

    return str(mod_pow(a, 2 * n, mod))

# provided samples (from statement formatting)
assert run("1 2\n") == "0"
assert run("2 3\n") == "3"

# custom cases
assert run("1 1\n") == "1", "all ones"
assert run("2 2\n") == "4", "small power check"
assert run("5 10\n") == str(pow(10, 10, 12)), "mod consistency"
assert run("10 1\n") == "1", "identity base"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | base 1 identity behavior |
| 2 2 | 4 | correctness of exponentiation |
| 5 10 | computed value | modular consistency with small verification |
| 10 1 | 1 | exponent irrelevant when base is 1 |

## Edge Cases

One edge case is when $a = 1$. In that case, every multiplication is neutral, and the result must always be 1 regardless of $n$. The algorithm initializes `res = 1` and never changes it, since every multiplication is by 1 modulo $m$.

Another edge case is small $n$, especially $n = 1$, where the modulus is $4$. For any $a$, the algorithm computes $a^2 \bmod 4$. The binary exponentiation correctly handles this even when intermediate squaring causes reductions to zero, as seen in the example where $2^2 \equiv 0 \pmod 4$.

A third case is when $a$ is already larger than the modulus. The algorithm immediately reduces it with `a %= mod`, ensuring that subsequent operations remain bounded and correct.
