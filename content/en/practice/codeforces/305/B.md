---
title: "CF 305B - Continued Fractions"
description: "We are given a rational number written as a normal fraction p / q, and another number written as a finite continued fraction."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 305
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 184 (Div. 2)"
rating: 1700
weight: 305
solve_time_s: 85
verified: true
draft: false
---

[CF 305B - Continued Fractions](https://codeforces.com/problemset/problem/305/B)

**Rating:** 1700  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rational number written as a normal fraction `p / q`, and another number written as a finite continued fraction.

The continued fraction has the form:

$$a_1 + \frac{1}{a_2 + \frac{1}{a_3 + \dots}}$$

We must determine whether both representations describe the same rational number.

The continued fraction length is at most 90, which is tiny. The values themselves can be as large as $10^{18}$, so arithmetic must be done carefully. Python handles arbitrarily large integers naturally, which makes the implementation much safer than in fixed-width integer languages.

A direct floating-point comparison is completely unreliable here. Continued fractions can represent huge numerators and denominators, and floating-point rounding would silently corrupt equality checks.

The most dangerous edge cases come from intermediate fractions.

Consider this input:

```
3 2
2
1 2
```

The continued fraction equals:

$$1 + \frac{1}{2} = \frac{3}{2}$$

The correct answer is `YES`.

A careless implementation using floating point may compute something like `1.4999999999999998` and incorrectly reject the equality.

Another subtle case appears when the continued fraction has length 1:

```
5 1
1
5
```

The continued fraction is simply `5`. There is no nested denominator at all. Code that blindly assumes at least two terms will either crash or produce the wrong result.

One more tricky scenario comes from reducing fractions too late.

```
1000000000000000000 1
2
999999999999999999 1
```

The continued fraction equals:

$$999999999999999999 + \frac{1}{1}
= 1000000000000000000$$

Intermediate values become extremely large. Languages with 64-bit overflow would fail if the implementation multiplies before simplifying. Python avoids overflow, but the algorithm should still stay mathematically clean.

## Approaches

The brute-force idea is straightforward: explicitly evaluate the continued fraction into a numerator and denominator, then compare it with `p / q`.

We can reconstruct the fraction from the back. Suppose we already know the value of the suffix as `x / y`. Then adding the previous term `a[i]` transforms it into:

$$a_i + \frac{y}{x}
=
\frac{a_i x + y}{x}$$

This works because every finite continued fraction represents a rational number.

The brute-force version repeatedly constructs fractions using arbitrary precision arithmetic. Since `n ≤ 90`, even huge integers remain manageable. The algorithm performs only linear many arithmetic operations.

The key observation is that we do not actually need to compute decimal values or simulate division at all. Continued fractions are tightly connected to the Euclidean algorithm.

Suppose:

$$\frac{p}{q} = a_1 + \frac{r}{q}$$

Then:

$$a_1 = \left\lfloor \frac{p}{q} \right\rfloor$$

and the remainder recursively defines the rest of the continued fraction.

This means we can compare the given sequence directly against the Euclidean decomposition of `p / q`.

At each step:

1. The next continued fraction coefficient must equal `p // q`.
2. Then we replace `(p, q)` with `(q, p % q)`.

This is exactly the Euclidean algorithm.

The brute-force construction already passes comfortably because `n` is only 90, but the Euclidean interpretation is cleaner, simpler, and avoids constructing gigantic intermediate numerators explicitly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force reconstruction | O(n) | O(1) | Accepted |
| Euclidean comparison | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `p` and `q`.
2. Read the continued fraction sequence `a`.
3. For each value `x` in the sequence:

Check whether `p // q` equals `x`.

If they differ, the representations cannot be equal, so print `NO`.
4. Replace `(p, q)` with `(q, p % q)`.

This mirrors the recursive structure of continued fractions. After removing the integer part, the remaining fraction becomes:

$$\frac{q}{p \bmod q}$$
5. After processing all coefficients, verify that the Euclidean process finished exactly.

The remaining denominator must be zero. If not, the continued fraction ended too early.
6. Print `YES` if all checks succeeded, otherwise print `NO`.

### Why it works

A finite continued fraction is exactly the sequence of quotients produced by the Euclidean algorithm on `(p, q)`.

At every iteration:

$$p = q \cdot \left\lfloor \frac{p}{q} \right\rfloor + (p \bmod q)$$

The integer quotient becomes the next continued fraction coefficient. The remainder defines the next recursive fraction.

Because the Euclidean algorithm uniquely decomposes a rational number into continued fraction coefficients, matching every quotient guarantees equality. Any mismatch means the represented numbers differ.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p, q = map(int, input().split())

    n = int(input())
    a = list(map(int, input().split()))

    for x in a:
        if q == 0:
            print("NO")
            return

        if p // q != x:
            print("NO")
            return

        p, q = q, p % q

    if q == 0:
        print("YES")
    else:
        print("NO")

solve()
```

The implementation follows the Euclidean algorithm directly.

The loop compares each continued fraction coefficient with the current integer quotient `p // q`. If they differ even once, equality is impossible.

After consuming one coefficient, we move to the next remainder state using:

```
p, q = q, p % q
```

This transformation is the heart of the continued fraction recursion.

The final check is subtle and easy to miss. We must ensure the fraction expansion ended exactly when the Euclidean algorithm terminated. If `q != 0` after processing all coefficients, then the sequence was too short.

The guard:

```
if q == 0:
```

inside the loop prevents division by zero in malformed situations where the continued fraction is longer than the Euclidean decomposition.

Python integers automatically expand to arbitrary size, so we never worry about overflow even when values grow far beyond $10^{18}$.

## Worked Examples

### Example 1

Input:

```
9 4
2
2 4
```

Trace:

| Step | p | q | p // q | Expected coefficient | New (p, q) |
| --- | --- | --- | --- | --- | --- |
| Start | 9 | 4 | 2 | 2 | (4, 1) |
| Next | 4 | 1 | 4 | 4 | (1, 0) |

After all coefficients are processed, `q = 0`, so the answer is `YES`.

This trace shows the exact connection between continued fractions and Euclid's algorithm. The quotients match perfectly at every step.

### Example 2

Input:

```
3 2
2
1 3
```

Trace:

| Step | p | q | p // q | Expected coefficient | Result |
| --- | --- | --- | --- | --- | --- |
| Start | 3 | 2 | 1 | 1 | continue |
| Next | 2 | 1 | 2 | 3 | mismatch |

At the second step, the Euclidean quotient is `2`, but the continued fraction expects `3`. The representations are different, so the answer is `NO`.

This demonstrates that even a single coefficient mismatch immediately proves inequality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One Euclidean step per coefficient |
| Space | O(1) | Only a few integer variables are stored |

Since `n ≤ 90`, the algorithm is extremely fast. Even arbitrary precision arithmetic easily fits within the limits because only a small number of operations are performed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    p, q = map(int, input().split())

    n = int(input())
    a = list(map(int, input().split()))

    for x in a:
        if q == 0:
            print("NO")
            return

        if p // q != x:
            print("NO")
            return

        p, q = q, p % q

    if q == 0:
        print("YES")
    else:
        print("NO")

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
assert run("9 4\n2\n2 4\n") == "YES\n", "sample 1"

# minimum size
assert run("5 1\n1\n5\n") == "YES\n", "single coefficient"

# mismatch in middle
assert run("3 2\n2\n1 3\n") == "NO\n", "wrong coefficient"

# exact large-value reconstruction
assert run(
    "1000000000000000000 1\n2\n999999999999999999 1\n"
) == "YES\n", "large integers"

# continued fraction too short
assert run("8 3\n1\n2\n") == "NO\n", "sequence ended early"

# continued fraction too long
assert run("2 1\n3\n2 1 1\n") == "NO\n", "sequence too long"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5/1` with `[5]` | `YES` | Length-1 continued fractions |
| `3/2` with `[1,3]` | `NO` | Quotient mismatch detection |
| Huge values near $10^{18}$ | `YES` | Arbitrary precision arithmetic |
| `8/3` with `[2]` | `NO` | Sequence ending too early |
| `2/1` with `[2,1,1]` | `NO` | Sequence longer than Euclidean decomposition |

## Edge Cases

Consider the single-element continued fraction:

```
5 1
1
5
```

The algorithm begins with `p = 5`, `q = 1`.

The quotient is:

$$5 // 1 = 5$$

which matches the only coefficient. Then:

$$(p, q) = (1, 0)$$

The loop ends and `q == 0`, so the answer is `YES`.

This case confirms that the implementation correctly handles continued fractions with no recursive part.

Now consider a sequence that ends too early:

```
8 3
1
2
```

The first quotient is:

$$8 // 3 = 2$$

which matches. The state becomes:

$$(p, q) = (3, 2)$$

The sequence is already exhausted, but `q != 0`. The Euclidean process still has remaining terms, so the answer must be `NO`.

This validates the final termination check.

Finally, consider a sequence that is too long:

```
2 1
3
2 1 1
```

After processing coefficient `2`, the state becomes:

$$(p, q) = (1, 0)$$

The algorithm still has more coefficients to read. Since `q == 0`, division is impossible and the answer is immediately `NO`.

This prevents invalid extra terms from being accepted accidentally.
