---
title: "CF 102878B - Residue Problem"
description: "The problem asks us to answer many independent queries. In each query, a prime modulus P is fixed, and we define a value f(i,r,P) as the number of pairs (a,b) modulo P satisfying a modular equation involving a^r, b, and b^2."
date: "2026-07-25T12:42:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "B"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 48
verified: true
draft: false
---

[CF 102878B - Residue Problem](https://codeforces.com/problemset/problem/102878/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to answer many independent queries. In each query, a prime modulus `P` is fixed, and we define a value `f(i,r,P)` as the number of pairs `(a,b)` modulo `P` satisfying a modular equation involving `a^r`, `b`, and `b^2`. The final answer is not asking for the individual values of `f`; it asks for the product of `Y` raised to these values for every `i` from `1` to `N`, modulo `10^9+7`.

The useful first transformation is to combine the exponents. Since

$$\prod_{i=1}^{N}Y^{f(i,r,P)}=Y^{\sum_{i=1}^{N}f(i,r,P)},$$

each query only requires finding one exponent, the sum of all `f(i,r,P)` values.

The number of queries can reach `100000`, while `P` can be close to `10^9`. A solution that loops over all residues modulo `P`, or even over a large fraction of them, is impossible. We need a formula that depends only on small arithmetic properties of `P`, `r`, and `N`. The restriction `r <= 3` is the key clue, because it allows us to reason about powers in a finite field without performing expensive computations.

The equation is

$$a^r(b+b^2)^i \equiv b^i \pmod P.$$

The cases where the expression degenerates need special handling. If `b=0`, both sides are zero, so every `a` works. If `b=-1`, then `b+b^2=0` but `b^i` is nonzero, so no `a` works. For all other values, we can divide:

$$a^r \equiv (b/(b+b^2))^i.$$

Because `b+b^2=b(b+1)`, this becomes

$$a^r \equiv (b+1)^{-i}.$$

So the problem becomes counting how often a value is an `r`-th power in the multiplicative group of the field.

A careless implementation may forget the exceptional values. For example, if `P=5`, `r=2`, and `i=1`, the input query contains the modulus `5`. The value `b=0` contributes five valid pairs because every `a` works. If we only count nonzero residues and ignore zero, we lose these five pairs and get the wrong exponent.

Another common mistake is mishandling `b=-1`. For `P=7`, `r=3`, and `i=1`, choosing `b=6` gives `b+b^2=0`, while `b^i=6`, so there are no valid pairs from this value. Treating it like the `b=0` case would add invalid solutions.

## Approaches

The direct approach is to iterate over every possible `b`, then count the number of `a` values satisfying the equation. For a fixed `b`, we could test every `a` and check the congruence. This is correct because it examines exactly the definition of `f`. However, a single query could require around `P^2` checks, which is far beyond what is possible when `P` is close to `10^9`.

The important observation is that after removing the two exceptional values `b=0` and `b=-1`, every remaining `b` corresponds to exactly one nonzero field element `x=b+1` different from `1`. The number of solutions to

$$a^r=t$$

in the multiplicative group is determined only by whether `t` belongs to the subgroup of `r`-th powers.

For `r=1`, every value has one root. For `r=2`, exactly half of the nonzero values are squares. For `r=3`, either every value has a unique cube root when `3` does not divide `P-1`, or one third of the values are cubes and each cube has three roots when `3` divides `P-1`.

This lets us count all possible `b` values using only parity or divisibility of `i`.

For `r=2`, if `i` is even, every nonzero `x` gives a square because `x^i` is a square. If `i` is odd, only the square values of `x` work.

For `r=3`, if `P-1` is not divisible by `3`, the cube operation is a permutation, so every value works. Otherwise, only every third nonzero value is a cube. The pattern depends only on whether `i` is divisible by `3`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(P²N) | O(1) | Too slow |
| Optimal | O(log MOD) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the exponent `E = sum(f(i,r,P))` instead of the product directly. The final answer is `pow(Y, E, 1e9+7)`.
2. Handle `r=1`. Every nonzero `b` except `-1` contributes one valid `a`, and `b=0` contributes `P` valid pairs. The value for every `i` is therefore constant.
3. Handle `r=2`. There are always `P` solutions from `b=0`. Among the remaining `P-2` values, count how many of `(b+1)^(-i)` are squares. When `i` is even all values work. When `i` is odd only the nonzero quadratic residues work.
4. Handle `r=3`. Again, start with the `P` solutions from `b=0`. If `P-1` is not divisible by `3`, every nonzero value is a cube. Otherwise, only one third of the nonzero values are cubes, and this happens only when `i` is not a multiple of `3`.
5. Multiply the contributions by the number of indices having each property. For example, instead of iterating through every even `i`, compute how many even values appear in `1..N`.

Why it works:

After the substitution `x=b+1`, every valid nonzero case asks whether `x^{-i}` belongs to the subgroup of `r`-th powers. In a cyclic group, taking an inverse does not change membership in a subgroup, so the question is equivalent to asking whether `x^i` is an `r`-th power. The subgroup sizes for squares and cubes are fixed by `gcd(r,P-1)`, which gives the formulas used above. Every possible `b` is covered by exactly one case, so the summed exponent is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve_query(Y, N, r, P):
    if r == 1:
        exp = N * (2 * P - 2)
        return pow(Y, exp, MOD)

    if r == 2:
        even = N // 2
        odd = N - even

        per_even = P + 2 * (P - 2)
        per_odd = P + (P - 3)

        exp = even * per_even + odd * per_odd
        return pow(Y, exp, MOD)

    if (P - 1) % 3 != 0:
        exp = N * (2 * P - 2)
    else:
        div3 = N // 3
        other = N - div3

        per_div3 = P + 3 * (P - 2)
        per_other = P + (P - 4)

        exp = div3 * per_div3 + other * per_other

    return pow(Y, exp, MOD)

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        Y, N, r, P = map(int, input().split())
        ans.append(str(solve_query(Y, N, r, P)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The solution first converts the product into a single modular exponentiation. This is the reason the code never needs to store any sequence of `f(i,r,P)` values.

For `r=1`, the exponent is constant for every `i`. For `r=2`, the code separates odd and even positions because the square property changes exactly with the parity of the exponent. The number of even indices in `1..N` is `N//2`, and the remaining indices are odd.

For `r=3`, the code first checks whether the cube map is a bijection. If `P-1` is not divisible by `3`, all nonzero residues are cubes. Otherwise, indices divisible by `3` behave differently from the other indices.

All arithmetic is kept as integers. Python handles large intermediate values safely, but the final exponent is only needed by modular exponentiation, which runs in logarithmic time.

## Worked Examples

Using the first sample query:

```
100000 1234567 1 999999937
```

For `r=1`, every `i` contributes the same amount.

| Step | r | Contribution per i | Number of i | Exponent part |
| --- | --- | --- | --- | --- |
| 1 | 1 | `2P-2` | `1234567` | `1234567*(2P-2)` |

The whole answer is obtained by raising `100000` to this exponent modulo `10^9+7`.

For the second sample query:

```
100000 7654321 2 999999929
```

The modulus is odd, so half of the nonzero residues are squares.

| Step | i type | Count | Contribution |
| --- | --- | --- | --- |
| 1 | Even i | `3827160` | `P+2(P-2)` |
| 2 | Odd i | `3827161` | `P+(P-3)` |

This trace shows why parity is the only information needed for the quadratic case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log MOD) | Each query performs a constant number of arithmetic operations and one modular exponentiation. |
| Space | O(1) | No data structures depending on the input size are stored. |

The original limits allow up to `100000` queries, so even an `O(P)` method would fail. The constant work per query makes the solution suitable for the maximum input size.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def solve_query(Y, N, r, P):
    if r == 1:
        return pow(Y, N * (2 * P - 2), MOD)

    if r == 2:
        even = N // 2
        odd = N - even
        return pow(Y, even * (3 * P - 4) + odd * (2 * P - 3), MOD)

    if (P - 1) % 3:
        return pow(Y, N * (2 * P - 2), MOD)

    return pow(
        Y,
        (N // 3) * (4 * P - 6) + (N - N // 3) * (2 * P - 4),
        MOD
    )

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        Y, N, r, P = map(int, input().split())
        out.append(str(solve_query(Y, N, r, P)))
    return "\n".join(out)

assert run("""4
100000 1234567 1 999999937
100000 7654321 2 999999929
100000 7777777 3 999999893
100000 7777777 3 999999757
""") == """968518472
236321637
770733917
509589974"""

assert run("""1
5 1 1 3
""") == str(pow(5, 4, MOD))

assert run("""1
7 1 2 5
""") == str(pow(7, 7, MOD))

assert run("""1
10 6 2 11
""") == str(pow(10, 6 * (3 * 11 - 4) // 2 + 3 * (2 * 11 - 3), MOD))

assert run("""1
123 100000000 3 1000000007
""") == str(pow(123, 100000000 * (2 * 1000000007 - 2), MOD))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `r=1`, smallest modulus | computed value | Handles the direct counting formula |
| `r=2`, small prime | computed value | Checks odd and even exponent handling |
| `r=2`, mixed parity range | computed value | Catches parity counting errors |
| Large `N` | computed value | Confirms logarithmic exponentiation |

## Edge Cases

For `b=0`, the algorithm includes the fixed `P` valid pairs in every value of `f`. For example, with `P=5`, `r=2`, and `N=1`, the contribution from this single residue is five pairs, and the formula includes it before counting the remaining residues.

For `b=-1`, no pairs are added. The substitution `x=b+1` naturally removes this case because it corresponds to `x=0`, which is not part of the multiplicative group being counted.

When `P-1` is divisible by `3`, cube counting changes. For example, with `P=7`, only one third of the nonzero residues are cubes, and indices divisible by `3` must be separated because `x^3` is always a cube while `x` itself is not necessarily one. The algorithm handles this by counting multiples of three directly instead of assuming every index behaves the same.

When `N` is very large, iterating from `1` to `N` would be impossible. The solution only counts how many indices satisfy each category, such as even indices or multiples of three, so the runtime remains independent of `N`.
