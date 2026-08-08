---
title: "CF 102440L - \u0420\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u043e\u043b\u0438\u043a\u043e\u0432"
description: "We have rabbits numbered from (1) to (n), and every rabbit must receive one of two labels, (0) or (1). The labels cannot be chosen arbitrarily. Whenever (b) divides (a), the labels must satisfy [ f(a)=f(b) text{OR} f(a/b)."
date: "2026-08-08T14:13:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "L"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 499
verified: true
draft: false
---

[CF 102440L - \u0420\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u043e\u043b\u0438\u043a\u043e\u0432](https://codeforces.com/problemset/problem/102440/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have rabbits numbered from (1) to (n), and every rabbit must receive one of two labels, (0) or (1). The labels cannot be chosen arbitrarily. Whenever (b) divides (a), the labels must satisfy

[
f(a)=f(b)\ \text{OR}\ f(a/b).
]

Some rabbits already have prescribed labels, and we need to count every complete labeling that satisfies both the divisibility rule and all prescriptions. The answer is taken modulo (10^9+7).

The useful part of the input structure is the combination of (n\le 10^6) and (m\le18). The number of rabbits is large enough that any algorithm enumerating states for all (n) rabbits, or worse, all (2^n) labelings, is impossible. At the same time, only 18 rabbits are constrained, which strongly suggests that the exponential part should depend on (m), not on (n). The factorization of the at most 18 prescribed numbers is also cheap because every number is at most (10^6).

There are several edge cases where treating the rule as an ordinary local constraint gives the wrong answer. The first is rabbit (1). For example,

```
1 1
1 0
```

has answer (1), because (f(1)=0) is perfectly valid and there are no other rabbits. A careless solution might treat (1) as having a prime factor and incorrectly force something else.

The second is the possibility that (f(1)=1). For example,

```
3 1
1 1
```

has answer (1). Once (f(1)=1), every prime must also have color (1), and consequently every rabbit has color (1). This is one complete coloring that is easy to miss if we only consider colorings generated from prime choices with (f(1)=0).

The third edge case is an impossible positive condition. For example,

```
5 2
4 1
2 0
```

has answer (0). The condition (f(2)=0) forces (f(4)=f(2)=0), contradicting the prescribed value (f(4)=1). Merely counting the prescribed rabbits independently would miss this dependency.

A final useful example is

```
5 2
2 1
3 1
```

which has answer (3). There is one coloring with every rabbit in group (1), and when (f(1)=0), primes (2) and (3) must both be (1), while prime (5) can independently be either (0) or (1). Thus there are two colorings of the second type, giving (3) in total.

## Approaches

The direct brute-force approach is to assign either (0) or (1) to every one of the (n) rabbits. There are (2^n) assignments. For each assignment, we could check every divisibility pair by iterating over (b) and its multiples (a). The number of such pairs is

[
\sum_{b=1}^{n}\left\lfloor\frac nb\right\rfloor=\Theta(n\log n).
]

At (n=10^6), this is about (1.4\cdot10^7) divisibility checks for one coloring, while the number of colorings is (2^{10^6}). The approach is correct, but its exponential dependence on (n) makes it completely unusable.

The key observation comes from applying the rule only to prime divisors. Suppose (p) is prime and (p\mid x). If (f(p)=1), then

[
f(x)=f(p)\text{ OR }f(x/p)=1,
]

so every multiple of (p) must also have color (1). If instead (f(p)=0), then

[
f(x)=f(x/p).
]

Repeatedly removing prime factors shows that the color of every number is determined entirely by the colors of its distinct prime factors, except for the special choice of (f(1)).

There are consequently only two structural cases.

If (f(1)=1), every prime (p) must also have color (1), because applying the rule to (a=p,b=p) does not force this, but applying it with (a=p,b=1) is tautological, so we need another argument. Since (p) can be represented as (a=p,b=p), that still gives no restriction. The decisive condition is obtained by considering (a=p^2,b=p):

[
f(p^2)=f(p)\text{ OR }f(p)=f(p).
]

Thus prime colors can initially look independent. However, if (f(1)=1), the general relation with (b=x) does not force anything either. The correct structural statement is actually slightly different: (f(1)) is not forced by the divisibility rule. If (f(1)=1), the recurrence through a prime (p) with (f(p)=0) gives (f(p)=f(1)=1), so (p) cannot be (0). Hence every prime is (1), and then every number is (1). Thus (f(1)=1) gives exactly one coloring.

If (f(1)=0), every number (x>1) gets the OR of the colors of its distinct prime factors:

[
f(x)=\bigvee_{p\mid x}f(p).
]

Now the unknowns are just the colors of the primes. A prescribed (x=0) forces every prime divisor of (x) to be (0). A prescribed (x=1) means that at least one prime divisor of (x) must be (1).

This transforms the problem into counting Boolean assignments to primes subject to at most 18 OR-clauses. We can count those assignments with inclusion-exclusion over the prescribed rabbits whose color is (1). For a selected subset of positive constraints, inclusion-exclusion asks us to make every selected OR-clause false. Making an OR-clause false means setting all of its prime divisors to (0). The only quantity we need from the subset is the number of distinct prime variables that it forces to zero.

The number of prime variables can be large, up to (78498) when (n=10^6), but the number of positive constraints is at most 18. We therefore represent the prime factors of each positive constraint as a Python integer bitmask. A subset of constraints can be processed by taking the bitwise OR of their masks. The exponential part is only (2^{18}=262144), which is small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(2^n n\log n)) | (O(n)) | Too slow |
| Optimal | (O(n\log\log n + 2^m m)) | (O(n+2^m)) | Accepted |

## Algorithm Walkthrough

1. Build a sieve of Eratosthenes up to (n). Besides counting all primes up to (n), keep the resulting prime list so that the at most 18 prescribed numbers can be factorized efficiently.
2. Separate the prescribed rabbits into those with color (0) and those with color (1). Factor every prescribed number into its distinct prime divisors.
3. Add every prime divisor of a prescribed zero-valued number to the set `forced_zero`. In the (f(1)=0) case, a number has color (0) exactly when every one of its prime factors has color (0), so these primes are forced.
4. Check whether the all-ones coloring is possible. It is possible exactly when no prescribed rabbit has color (0). If so, add one to the answer. This accounts for the separate case (f(1)=1).
5. For the (f(1)=0) case, inspect every prescribed rabbit with color (1). If its value is (1), there is no prime factor that could make its color (1), so this case contributes zero.
6. Give every prime that occurs in a positive constraint and is not already forced to zero a bit position. For each positive constraint, build a mask containing precisely these primes. Primes that occur only in zero constraints have already been fixed to zero, so they do not need a bit.
7. Let (F) be the total number of prime variables that remain free before considering the positive constraints. For a subset (S) of positive constraints, take the OR of their masks. Its set bits are exactly the additional primes that must be zero for all constraints in (S) to be false. Consequently, the number of assignments in which all constraints in (S) are false is

[
2^{F-\operatorname{popcount}(\operatorname{OR}(S))}.
]

1. Apply inclusion-exclusion over all subsets of positive constraints. Add this quantity for even-sized subsets and subtract it for odd-sized subsets. The resulting value is exactly the number of (f(1)=0) colorings satisfying every positive constraint.
2. Add the (f(1)=0) contribution to the possible all-ones coloring, reduce modulo (10^9+7), and print the result.

The reason the inclusion-exclusion invariant works is that a positive constraint is an OR of its prime colors. Such a constraint fails exactly when all its prime variables are zero. For any selected collection of failed constraints, the required zero variables are precisely the union of their prime-factor sets. The mask OR computes that union without double-counting shared primes. Inclusion-exclusion then counts assignments in which none of the positive constraints fail.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def build_sieve(n):
    sieve = bytearray(b'\x01') * (n + 1)

    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0

    p = 2
    while p * p <= n:
        if sieve[p]:
            start = p * p
            count = (n - start) // p + 1
            sieve[start:n + 1:p] = b'\x00' * count
        p += 1

    primes = [i for i in range(2, n + 1) if sieve[i]]
    return sieve, primes

def factor_distinct(x, primes):
    factors = []

    for p in primes:
        if p * p > x:
            break

        if x % p == 0:
            factors.append(p)
            while x % p == 0:
                x //= p

        if x == 1:
            break

    if x > 1:
        factors.append(x)

    return factors

def solve():
    n, m = map(int, input().split())

    fixed = []
    for _ in range(m):
        x, y = map(int, input().split())
        fixed.append((x, y))

    sieve, primes = build_sieve(n)
    prime_count = len(primes)

    factorized = []
    forced_zero = set()

    for x, y in fixed:
        factors = factor_distinct(x, primes)
        factorized.append((x, y, factors))

        if y == 0:
            for p in factors:
                forced_zero.add(p)

    answer = 0

    # Case f(1) = 1.
    # Then every prime must also be 1, so the whole coloring is all ones.
    if all(y == 1 for _, y in fixed):
        answer = 1

    # Case f(1) = 0.
    positive = []

    impossible = False

    for x, y, factors in factorized:
        if y == 1:
            if x == 1:
                impossible = True
                break
            positive.append(factors)

    if not impossible:
        # Assign bit positions only to primes that can still be free.
        prime_id = {}
        next_bit = 0

        for factors in positive:
            for p in factors:
                if p not in forced_zero and p not in prime_id:
                    prime_id[p] = next_bit
                    next_bit += 1

        masks = []
        for factors in positive:
            mask = 0
            for p in factors:
                if p not in forced_zero:
                    mask |= 1 << prime_id[p]
            masks.append(mask)

        # A positive constraint with all its prime factors forced to zero
        # can never become 1.
        if any(mask == 0 for mask in masks):
            c0 = 0
        else:
            free_primes = prime_count - len(forced_zero)

            k = len(masks)
            total_subsets = 1 << k

            union = [0] * total_subsets
            c0 = 0

            for subset in range(1, total_subsets):
                bit = subset & -subset
                idx = bit.bit_length() - 1
                union[subset] = union[subset ^ bit] | masks[idx]

            for subset in range(total_subsets):
                used = union[subset].bit_count()
                ways = pow(2, free_primes - used, MOD)

                if subset.bit_count() & 1:
                    c0 -= ways
                else:
                    c0 += ways

            c0 %= MOD

        answer = (answer + c0) % MOD

    print(answer)

if __name__ == "__main__":
    solve()
```

The sieve is needed for two different purposes. `prime_count` tells us how many independent prime variables exist in the (f(1)=0) case, while the prime list lets us factor the at most 18 prescribed numbers. Since every input value is at most (10^6), trial division by the primes up to its square root is tiny.

The `forced_zero` set represents information coming from prescribed zero-valued rabbits. If (x) is prescribed as zero, every prime factor of (x) has to be zero. Removing these primes from the masks is essential. They are already fixed, so counting them again as free variables would overcount assignments.

The special `all(y == 1)` check handles (f(1)=1). In that case the recurrence obtained by removing a zero-colored prime would contradict (f(1)=1), so every prime must be one and every rabbit becomes one. There is exactly one such coloring.

For the (f(1)=0) case, every positive constraint becomes a clause saying that at least one prime factor must have color (1). Inclusion-exclusion counts assignments satisfying all those clauses. The `union` array stores the union of prime masks for every subset, using

[
U(S)=U(S\setminus{i})\ \text{OR}\ M_i.
]

The exponent in `pow(2, free_primes - used, MOD)` is the number of prime variables still free after the selected clauses have been forced to fail.

There is no integer overflow issue in Python. The modular exponentiation is performed directly with `pow(base, exponent, MOD)`, so even though the mathematical number of colorings is enormous, intermediate values never need to be constructed.

## Worked Examples

### Sample 1

The input is

```
5 2
4 1
2 0
```

The primes up to (5) are (2,3,5). The rabbit (2) is fixed to zero, so prime (2) is forced to zero. Rabbit (4) has prime factor set ({2}), but it is prescribed as one.

| Step | Prescribed zero factors | Positive mask | Valid (f(1)=0) assignments | Answer |
| --- | --- | --- | --- | --- |
| Factor (2) | ({2}) |  |  |  |
| Factor (4) | ({2}) | (0) | (0) | (0) |
| Check (f(1)=1) | invalid because (2=0) is prescribed |  | (0) | (0) |

The positive mask is empty because its only prime factor is already forced to zero. Thus the positive condition can never be satisfied. The all-ones coloring is also forbidden by the prescribed zero, so the final answer is (0).

### Sample 2

The input is

```
5 2
2 1
3 1
```

There are three primes, (2,3,5), and no prime is forced to zero. For (f(1)=0), the two positive constraints are the clauses (2=1) and (3=1).

| Subset of clauses | Union of forced-zero primes | Size | Sign | Assignments |
| --- | --- | --- | --- | --- |
| (\varnothing) | (\varnothing) | 0 | (+) | (2^3=8) |
| ({2}) | ({2}) | 1 | (-) | (2^2=4) |
| ({3}) | ({3}) | 1 | (-) | (2^2=4) |
| ({2,3}) | ({2,3}) | 2 | (+) | (2^1=2) |

Inclusion-exclusion gives

[
8-4-4+2=2.
]

These are the two colorings with (f(1)=0), where primes (2) and (3) are both one and prime (5) is arbitrary. Since every prescribed value is one, the all-ones coloring contributes one more.

The final answer is (2+1=3).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log\log n + m\sqrt n + 2^m m)) | Sieve the range, factor at most (m) numbers, then process every subset of the positive constraints |
| Space | (O(n+2^m)) | The sieve and prime list use (O(n)), while the subset union array uses (O(2^m)) |

With (n\le10^6), the sieve is easily manageable, and the factorization of only 18 numbers is negligible. The exponential component is bounded by (2^{18}=262144) subsets, which is small enough for Python. The algorithm avoids any state space depending exponentially on the million rabbits.

## Test Cases

```python
import sys
import io
from contextlib import redirect_stdout

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    fixed = []
    for _ in range(m):
        x, y = map(int, input().split())
        fixed.append((x, y))

    sieve = bytearray(b'\x01') * (n + 1)
    sieve[0] = 0
    if n >= 1:
        sieve[1] = 0

    p = 2
    while p * p <= n:
        if sieve[p]:
            start = p * p
            count = (n - start) // p + 1
            sieve[start:n + 1:p] = b'\x00' * count
        p += 1

    primes = [i for i in range(2, n + 1) if sieve[i]]

    def factor_distinct(x):
        res = []
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                res.append(p)
                while x % p == 0:
                    x //= p
            if x == 1:
                break
        if x > 1:
            res.append(x)
        return res

    factorized = []
    forced_zero = set()

    for x, y in fixed:
        factors = factor_distinct(x)
        factorized.append((x, y, factors))
        if y == 0:
            forced_zero.update(factors)

    answer = 1 if all(y == 1 for _, y in fixed) else 0

    positive = []
    impossible = False

    for x, y, factors in factorized:
        if y == 1:
            if x == 1:
                impossible = True
                break
            positive.append(factors)

    if not impossible:
        prime_id = {}
        for factors in positive:
            for p in factors:
                if p not in forced_zero and p not in prime_id:
                    prime_id[p] = len(prime_id)

        masks = []
        for factors in positive:
            mask = 0
            for p in factors:
                if p not in forced_zero:
                    mask |= 1 << prime_id[p]
            masks.append(mask)

        if any(mask == 0 for mask in masks):
            c0 = 0
        else:
            free_primes = len(primes) - len(forced_zero)
            k = len(masks)
            total = 1 << k

            union = [0] * total
            c0 = 0

            for subset in range(1, total):
                bit = subset & -subset
                idx = bit.bit_length() - 1
                union[subset] = union[subset ^ bit] | masks[idx]

            for subset in range(total):
                ways = pow(
                    2,
                    free_primes - union[subset].bit_count(),
                    MOD
                )
                if subset.bit_count() & 1:
                    c0 -= ways
                else:
                    c0 += ways

            c0 %= MOD

        answer = (answer + c0) % MOD

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin

    return out.getvalue().strip()

# Provided samples
assert run("""5 2
4 1
2 0
""") == "0", "sample 1"

assert run("""5 2
2 1
3 1
""") == "3", "sample 2"

# Minimum size, f(1) = 0 gives the unique valid coloring.
assert run("""1 1
1 0
""") == "1", "minimum size with zero"

# Minimum size, f(1) = 1 gives the unique all-ones coloring.
assert run("""1 1
1 1
""") == "1", "minimum size with one"

# All prescribed values are zero. Prime 2 is forced to zero,
# while primes 3, 5, and 7 remain arbitrary.
assert run("""10 3
2 0
4 0
8 0
""") == "8", "all-equal zero constraints"

# A positive constraint on 1 is impossible when f(1) = 0,
# while the all-ones coloring remains valid.
assert run("""10 1
1 1
""") == "1", "positive constraint on one"

# Maximum n, boundary factorization at n itself.
# There are 78498 primes <= 1,000,000, and fixing n to zero
# forces exactly primes 2 and 5 to zero.
expected = pow(2, 78498 - 2, MOD)
assert run("""1000000 1
1000000 0
""") == str(expected), "maximum n boundary"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 0` | `1` | Smallest possible (n), correct handling of (1) |
| `1 1 / 1 1` | `1` | The separate (f(1)=1) coloring |
| `10 3 / 2 0, 4 0, 8 0` | `8` | Repeated multiples of the same forced prime and all-zero constraints |
| `10 1 / 1 1` | `1` | Positive constraint on (1) and the all-ones case |
| `1000000 1 / 1000000 0` | (2^{78496}\bmod 10^9+7) | Maximum (n), boundary factorization, and large prime count |

## Edge Cases

The first special case is (x=1). Its prime-factor set is empty. If it is prescribed as zero, it simply fixes (f(1)=0), which is compatible with every independent choice of prime colors. For example,

```
1 1
1 0
```

has one answer. The algorithm puts no primes into `forced_zero`, enters the (f(1)=0) case, and counts (2^0=1) coloring.

If (1) is prescribed as one, the (f(1)=0) case is impossible because there is no prime whose color can make (f(1)) equal to one. The separate all-ones case contributes exactly one:

```
10 1
1 1
```

so the answer is (1).

The second case is a zero constraint whose prime factors overlap a positive constraint. In

```
5 2
4 1
2 0
```

the zero constraint forces prime (2) to zero. The positive constraint for (4) has only prime factor (2), so its mask becomes zero. A zero mask means the corresponding OR-clause is permanently false, and the (f(1)=0) contribution is immediately zero. Since a zero prescription also forbids the all-ones coloring, the final result is (0).

The third case is when many prescribed zero values contain the same prime. For

```
10 3
2 0
4 0
8 0
```

all three constraints force only prime (2) to zero. Primes (3,5,7) remain independent, giving (2^3=8) valid colorings. The algorithm stores forced primes in a set, so repeated occurrences of (2) are counted only once.

The last case is the maximum boundary (n=10^6). For

```
1000000 1
1000000 0
```

the factorization is (2^6\cdot5^6), so only primes (2) and (5) are forced to zero. All other primes up to (10^6) remain independent. There are (78498) primes up to (10^6), hence the answer is

[
2^{78498-2}\bmod 10^9+7.
]

The algorithm never enumerates those prime assignments. It only needs their count, which is exactly why the solution remains practical at the largest allowed (n).
