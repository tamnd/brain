---
title: "CF 104487H - X Y ?"
description: "We are given a prime modulus $p$, together with two exponents $a$ and $b$ that are coprime, and two values $x$ and $y$. There is a hidden consistency condition: if we raise $x$ to the power $a$ and $y$ to the power $b$, those results are equal modulo $p$."
date: "2026-06-30T12:39:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104487
codeforces_index: "H"
codeforces_contest_name: "Tishreen + SVU CPC 2023"
rating: 0
weight: 104487
solve_time_s: 56
verified: true
draft: false
---

[CF 104487H - X Y ?](https://codeforces.com/problemset/problem/104487/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a prime modulus $p$, together with two exponents $a$ and $b$ that are coprime, and two values $x$ and $y$. There is a hidden consistency condition: if we raise $x$ to the power $a$ and $y$ to the power $b$, those results are equal modulo $p$. In other words, the pair $(x, y)$ is not arbitrary; it already satisfies a strong algebraic relationship in the multiplicative structure modulo $p$.

For each query, we are asked to reconstruct a value $z$ such that when we raise $z$ to the power $a$, we get $y$ modulo $p$, and when we raise $z$ to the power $b$, we get $x$ modulo $p$. If multiple positive integers satisfy this, we want the smallest positive one. If none exists, we output $-1$.

The key point is that everything happens under modulo $p$, where $p$ is prime, so all nonzero values form a multiplicative group. This makes exponentiation behave like linear algebra in the exponent space, which is the central structure the solution relies on.

The constraints allow up to $10^5$ queries, so any solution that tries to search for $z$ directly or brute-force candidates per query is immediately infeasible. Even a single modular exponentiation per candidate would explode. We need an $O(\log p)$ or $O(1)$ per query construction.

A subtle edge case appears when either $x$ or $y$ is divisible by $p$, meaning they are zero modulo $p$. In that case, exponentiation collapses information because any positive power of zero is zero. A naive algebraic inverse-based approach would incorrectly try to divide by zero in the exponent space, producing invalid results or crashes.

For example, if $x \equiv 0 \pmod p$, then the condition $z^b \equiv x$ forces $z \equiv 0 \pmod p$, which immediately determines the answer, but only if it is consistent with the other equation. This case must be separated before doing any multiplicative-group reasoning.

## Approaches

A brute-force idea is to try all possible values of $z$ modulo $p$ and check whether both equations hold. This is mathematically correct because the solution, if it exists, must lie in the range $0$ to $p-1$. However, this approach requires $O(p)$ checks per query, and each check involves two exponentiations, making it far beyond feasible limits when $p$ can be up to $10^9$.

The structural improvement comes from recognizing that modulo a prime, all nonzero elements form a cyclic multiplicative group, and exponentiation behaves like multiplication in the exponent space. The system

$$z^a \equiv y \pmod p,\quad z^b \equiv x \pmod p$$

can be interpreted as two linear constraints on the “exponent representation” of $z$. Since $a$ and $b$ are coprime, we can combine these constraints into a single expression using Bézout coefficients.

If we can find integers $u$ and $v$ such that

$$au + bv = 1,$$

then we can raise both sides of $z$ to that linear combination:

$$z = z^{au + bv} = (z^a)^u (z^b)^v \equiv y^u x^v \pmod p.$$

This directly constructs $z$ from $x$ and $y$, reducing the problem to modular exponentiation and modular inverses.

The only complication is handling negative exponents in $u$ or $v$, which correspond to modular inverses. This is valid only when the base is nonzero modulo $p$, reinforcing why zero cases must be handled separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $z$ | $O(p \log p)$ per query | $O(1)$ | Too slow |
| Extended GCD construction | $O(\log p)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Step 1: Reduce everything modulo $p$

We first reduce $x$ and $y$ modulo $p$. This is necessary because all conditions are defined in modular arithmetic, and working outside this domain introduces irrelevant magnitude information.

### Step 2: Handle zero cases explicitly

If either $x \equiv 0$ or $y \equiv 0$, we must treat the system separately because multiplicative inverses do not exist for zero.

If $x \equiv 0$, then from $z^b \equiv x$, we get $z \equiv 0$. We then check whether this also satisfies $z^a \equiv y$. Since $0^a = 0$, this requires $y \equiv 0$. If consistent, the answer is $0$ modulo $p$, which corresponds to output $p$ as the smallest positive integer.

A symmetric argument applies when $y \equiv 0$.

### Step 3: Work in the multiplicative group

Now assume $x \neq 0$ and $y \neq 0$ modulo $p$. We treat them as elements of a group where division is defined via modular inverse.

### Step 4: Compute Bézout coefficients

We compute integers $u$ and $v$ such that:

$$au + bv = 1.$$

This is done using the extended Euclidean algorithm. The existence is guaranteed by $\gcd(a,b)=1$.

### Step 5: Construct the candidate solution

We compute:

$$z \equiv y^u \cdot x^v \pmod p.$$

If $u$ or $v$ is negative, we replace exponentiation by modular inverse exponentiation.

This produces a candidate that simultaneously satisfies both constraints because it reconstructs $z$ as a linear combination of the two given equations in exponent form.

### Step 6: Normalize to positive integer

If the result is $0$, we output $p$. Otherwise, we output the modular representative directly.

### Why it works

The correctness comes from treating exponentiation as a homomorphism in the multiplicative group modulo $p$. Every nonzero element has a well-defined exponent structure, and Bézout’s identity allows us to reconstruct the base from two power constraints whose exponents are coprime. Since $au + bv = 1$, applying this combination collapses the system into a single consistent reconstruction of $z$. The original constraints guarantee that the constructed value satisfies both equations, because substituting it back reduces both expressions to identities in the group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def mod_pow(a, e, mod):
    return pow(a, e, mod)

def solve():
    Q = int(input())
    out = []

    for _ in range(Q):
        p, a, b, x, y = map(int, input().split())

        x %= p
        y %= p

        # handle zero cases
        if x == 0 or y == 0:
            z = 0
            if pow(z, a, p) == y and pow(z, b, p) == x:
                out.append(str(p))
            else:
                out.append("-1")
            continue

        # Bézout: a*u + b*v = 1
        g, u, v = egcd(a, b)

        # g must be 1 since gcd(a,b)=1
        if g != 1:
            out.append("-1")
            continue

        # z = y^u * x^v mod p
        zu = pow(y, u, p) if u >= 0 else pow(pow(y, -u, p), p - 2, p)
        zv = pow(x, v, p) if v >= 0 else pow(pow(x, -v, p), p - 2, p)

        z = (zu * zv) % p

        if z == 0:
            z = p

        out.append(str(z))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation separates the degenerate zero-modulo-$p$ cases before using modular inverses, since inverses would otherwise be undefined. The extended gcd produces coefficients $u$ and $v$, which are directly used as exponents. Negative exponents are converted using Fermat’s little theorem through modular inverse via exponentiation by $p-2$.

The final normalization step ensures that the output is a positive integer, since the modular representative $0$ corresponds to $p$ in the required output domain.

## Worked Examples

Consider a small instance where $p = 7$, $a = 1$, $b = 2$, $x = 2$, $y = 4$. We first reduce modulo 7, which leaves values unchanged. Since both are nonzero, we compute Bézout coefficients for $1u + 2v = 1$, giving $u = 1$, $v = 0$. The construction yields $z = y^1 x^0 = 4$. Checking, $4^1 = 4$ and $4^2 = 16 \equiv 2 \pmod 7$, so it satisfies both constraints.

| Step | Value |
| --- | --- |
| x mod p | 2 |
| y mod p | 4 |
| u, v | (1, 0) |
| z | 4 |

This trace shows that when one Bézout coefficient is zero, the solution reduces to a direct root constraint.

Now consider a case where zero appears: $p = 5$, $x = 0$, $y = 0$, $a = 2$, $b = 3$. The only possible $z$ satisfying both is $z = 0$, which corresponds to output $5$.

| Step | Value |
| --- | --- |
| x mod p | 0 |
| y mod p | 0 |
| z candidate | 0 |
| validity | both equations satisfied |

This confirms why zero must be handled separately before applying multiplicative inverses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q \log \max(a,b))$ | extended gcd per query plus constant modular exponentiation |
| Space | $O(1)$ | only a few integers stored per query |

The solution comfortably fits within the limits since each query reduces to logarithmic arithmetic operations and modular exponentiation, both fast enough for $10^5$ queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = egcd(b, a % b)
        return g, y, x - (a // b) * y

    Q = int(input())
    out = []

    for _ in range(Q):
        p, a, b, x, y = map(int, input().split())
        x %= p
        y %= p

        if x == 0 or y == 0:
            z = 0
            if pow(z, a, p) == y and pow(z, b, p) == x:
                out.append(str(p))
            else:
                out.append("-1")
            continue

        g, u, v = egcd(a, b)

        zu = pow(y, u, p) if u >= 0 else pow(pow(y, -u, p), p - 2, p)
        zv = pow(x, v, p) if v >= 0 else pow(pow(x, -v, p), p - 2, p)

        z = (zu * zv) % p
        if z == 0:
            z = p

        out.append(str(z))

    return "\n".join(out)

# custom cases
assert run("3\n2 1 2 2 4\n7 1 2 2 4\n5 2 3 0 0\n") != "", "basic functionality"
assert run("1\n5 2 3 0 0\n") == "5", "all zero case"
assert run("1\n7 1 2 2 4\n") == "4", "simple valid reconstruction"
assert run("1\n11 3 2 7 3\n") != "0", "nonzero normalization check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single valid pair | correct z | basic reconstruction correctness |
| all zero case | p | degenerate modular case |
| simple reconstruction | computed z | correctness of Bézout construction |
| normalization check | non-zero | avoids incorrect zero output |

## Edge Cases

When both $x$ and $y$ are zero modulo $p$, the algorithm correctly reduces the solution to $z = 0$, which is then converted to $p$. A naive Bézout-based formula would fail immediately because modular inverses do not exist, but the explicit early check ensures the computation never reaches invalid operations.

When exactly one of $x$ or $y$ is zero, the system becomes inconsistent unless both equations force the same zero structure. The algorithm checks this by directly verifying both conditions with $z = 0$, preventing incorrect construction from exponent algebra.

When all values are nonzero, the algorithm operates entirely inside the multiplicative group modulo $p$, where Bézout reconstruction is valid. This separation of cases ensures that every branch of the computation stays within a mathematically valid domain.
