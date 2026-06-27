---
title: "CF 105055H - Hawarma"
description: "We are given an integer parameter $N$ and a rational function $$f(x) = frac{5xN^2}{x^2 + 3xN - 5N^2}.$$ The task is to find all real values $a$ such that plugging $a$ into the function returns the same value, meaning $f(a) = a$."
date: "2026-06-28T00:24:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "H"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 54
verified: true
draft: false
---

[CF 105055H - Hawarma](https://codeforces.com/problemset/problem/105055/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer parameter $N$ and a rational function

$$f(x) = \frac{5xN^2}{x^2 + 3xN - 5N^2}.$$

The task is to find all real values $a$ such that plugging $a$ into the function returns the same value, meaning $f(a) = a$. We must output how many such values exist and list them explicitly.

The input size is tiny: $N$ lies in $[-300, 300]$ and is nonzero. This immediately rules out any need for asymptotically heavy methods; any solution that ends up solving a constant-size algebraic problem per test case is sufficient.

The main subtlety is that we are solving a rational equation with domain restrictions. The denominator can become zero for some values, and those values must be excluded even if they appear as algebraic roots after simplification. A naive algebraic manipulation that multiplies both sides by the denominator without tracking this restriction will accidentally include invalid points.

A second subtle point is that cancellation by $x$ is tempting because the numerator contains $x$, but $x = 0$ must be treated separately. It is easy to lose this root during simplification even though it is valid when the denominator is nonzero at zero.

Edge cases include:

For $N = 1$, the denominator becomes $x^2 + 3x - 5$, which has real roots, so some candidate solutions may coincide with poles of the function. A careless solver might include such points.

For $x = 0$, we always get $f(0) = 0$ as long as the denominator is nonzero, and since the denominator evaluates to $-5N^2 \neq 0$, zero is always a valid solution for any $N \neq 0$.

Finally, the equation may reduce to a quadratic, meaning at most two additional roots beyond zero, but we must verify none coincide with forbidden denominator zeros.

## Approaches

A brute-force interpretation would be to treat the equation $f(x) = x$ as a continuous equality and attempt to enumerate candidate real values. That is impossible since real solutions are not enumerable.

Instead, we directly solve the algebraic equation symbolically. The function equality

$$\frac{5xN^2}{x^2 + 3xN - 5N^2} = x$$

can be transformed by multiplying both sides by the denominator, but only after explicitly excluding values where the denominator is zero. This produces a polynomial equation whose roots can be found exactly.

Carrying out the algebra:

$$5xN^2 = x(x^2 + 3xN - 5N^2)$$

Expanding the right-hand side:

$$5xN^2 = x^3 + 3x^2N - 5xN^2.$$

Bringing everything to one side:

$$0 = x^3 + 3x^2N - 10xN^2.$$

Factoring out $x$:

$$x(x^2 + 3Nx - 10N^2) = 0.$$

So one solution is always $x = 0$. The remaining solutions come from a quadratic:

$$x^2 + 3Nx - 10N^2 = 0.$$

Its discriminant is:

$$\Delta = 9N^2 + 40N^2 = 49N^2.$$

So:

$$x = \frac{-3N \pm 7|N|}{2}.$$

Since $N^2$ is always positive, we simplify directly:

$$x = \frac{-3N \pm 7N}{2}.$$

Thus the two roots are:

$$x_1 = 2N, \quad x_2 = -5N.$$

We still must verify these do not make the denominator zero. Substituting shows they never do for $N \neq 0$, so all three roots are valid.

The brute force idea fails because it treats a rational equation as if it required search over reals, while the structure collapses cleanly into a cubic with obvious factorization. The key observation is that equality of a rational function to the identity function always produces a polynomial equation after clearing denominators, and here it factors completely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over reals | Impossible | O(1) | Too slow |
| Algebraic simplification | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from the equation $f(x) = x$ and multiply both sides by the denominator, but only under the assumption that the denominator is nonzero at valid solutions. This ensures we do not introduce invalid roots from forbidden points.
2. Expand the resulting expression into a polynomial equation in $x$. The structure becomes a cubic because the original denominator is quadratic and is multiplied by $x$.
3. Move all terms to one side to obtain a cubic polynomial. This step converts the functional equation into a standard root-finding problem.
4. Factor out $x$, since every term contains it. This immediately reveals that $x = 0$ is a solution, provided the original function is defined there.
5. Solve the remaining quadratic equation $x^2 + 3Nx - 10N^2 = 0$ using the discriminant method. The discriminant simplifies to a perfect square, ensuring clean integer roots.
6. Compute the two roots as $2N$ and $-5N$.
7. Output the three values $0$, $2N$, and $-5N$.

### Why it works

The transformation preserves equivalence between the original rational equation and the derived polynomial equation on the domain where the denominator is nonzero. Every valid solution of the original equation must satisfy the polynomial, and any root of the polynomial that does not cancel the denominator corresponds to a valid solution. Since we explicitly check the structure of the roots and none coincide with denominator zeros for $N \neq 0$, the solution set is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

N = int(input().strip())

res = [0, 2 * N, -5 * N]

# remove duplicates just in case (though none occur for N != 0)
res = list(set(res))

print(len(res))
print(*res)
```

The implementation directly encodes the closed-form derivation. The only computation is forming the three candidate roots. A set is used as a safety measure, although algebraically the three values are distinct for all nonzero $N$.

Care must be taken not to attempt direct numeric solving of the rational equation, since floating-point methods are unnecessary and risk precision issues even though constraints are small.

## Worked Examples

We trace the sample input $N = 3$.

The derived roots are $0$, $2N = 6$, and $-5N = -15$.

| Step | N | Root 1 | Root 2 | Root 3 | Action |
| --- | --- | --- | --- | --- | --- |
| init | 3 | 0 | 6 | -15 | compute candidates |
| finalize | 3 | 0 | 6 | -15 | output set |

This confirms that the algebraic reduction produces exactly the expected solution set, including both positive and negative multiples of $N$.

A second example with $N = 1$:

| Step | N | Roots |
| --- | --- | --- |
| compute | 1 | 0, 2, -5 |
| output | 1 | 0 2 -5 |

This shows that even for the smallest magnitude $N$, the structure remains consistent and produces three distinct solutions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed regardless of input size |
| Space | O(1) | Only a fixed-size list of candidate roots is stored |

The constraints allow any constant-time algebraic solution, and this approach trivially satisfies both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    N = int(sys.stdin.readline().strip())
    res = [0, 2 * N, -5 * N]
    res = list(set(res))
    return str(len(res)) + "\n" + " ".join(map(str, res)) + "\n"

# provided sample
assert run("3\n") == "3\n0 6 -15\n" or run("3\n") == "3\n6 0 -15\n"

# custom cases
assert run("1\n").split()[0] == "3"
assert run("-1\n").split()[0] == "3"
assert run("10\n").split()[0] == "3"
assert run("2\n") != "", "basic sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 | 0 6 -15 | sample correctness |
| 1 | 0 2 -5 | smallest positive case |
| -1 | 0 -2 5 | sign handling |
| 10 | 0 20 -50 | scaling behavior |

## Edge Cases

For $N = 1$, the equation becomes particularly clean and helps verify that the derived formula is not dependent on accidental cancellation at larger values. Substituting $N = 1$ gives roots $0, 2, -5$. The denominator is $x^2 + 3x - 5$, which is nonzero at all three points, so no root is invalidated.

For $N = -1$, we get roots $0, -2, 5$. A common mistake would be to forget that both $2N$ and $-5N$ flip sign consistently, but the structure remains symmetric. The denominator check remains safe because substituting either value never yields zero for nonzero $N$.

For any $N$, the root $x = 0$ is especially important. It survives only because the original rational expression has a numerator proportional to $x$, and the denominator evaluates to $-5N^2$, which is always nonzero. This guarantees that removing the $x$ factor during simplification does not discard a valid solution, provided we explicitly reintroduce it after factoring.
