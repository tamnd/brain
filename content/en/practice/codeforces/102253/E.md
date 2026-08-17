---
title: "CF 102253E - Expectation of Division"
description: "We start with a positive integer (n1). In one operation, we choose one of its positive divisors uniformly at random and replace the current number by that divisor. The process stops when the number first becomes (1). The task is to find the expected number of operations."
date: "2026-08-17T21:28:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "E"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 209
verified: true
draft: false
---

[CF 102253E - Expectation of Division](https://codeforces.com/problemset/problem/102253/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a positive integer (n>1). In one operation, we choose one of its positive divisors uniformly at random and replace the current number by that divisor. The process stops when the number first becomes (1). The task is to find the expected number of operations.

The input gives (n), the number of distinct prime factors (m), and those prime factors. The crucial detail is that (n) can be as large as (10^{24}), so treating every integer up to (n) as a state is impossible. The supplied prime factors let us recover the exponent of every prime in the factorization of (n).

The expected value is a rational number. Instead of printing its numerator and denominator, we print the numerator multiplied by the modular inverse of the denominator modulo (10^9+7).

The original editorial derives the same recurrence and then reduces the state space from actual integers to multisets of prime exponents.

The bound (n\le 10^{24}) is the reason a standard divisor DP is not enough. A number in this range can have more than a million divisors, and there can be about (2\times10^5) test cases. Enumerating every divisor for every test case would require far more than the available time. The number of distinct prime factors is much smaller, at most (18), because the product of the first (18) primes is already around (10^{23}). This makes a state representation based on prime exponents feasible.

There are several edge cases that are easy to mishandle. For (n=2), the divisors are (1) and (2), and the current state can be selected again. The expectation satisfies

[
f(2)=1+\frac{f(1)+f(2)}2,
]

so (f(2)=2), giving `Case #1: 2`. A recurrence that averages only proper divisors would incorrectly obtain (1).

For (n=4), the correct value is (5/2), which becomes `500000006` modulo (10^9+7). The self-transition through divisor (4) must remain in the recurrence.

For (n=6), the proper divisor expectations are (f(1)=0), (f(2)=2), and (f(3)=2). Since (6) has four divisors,

[
f(6)=1+\frac{0+2+2+f(6)}4=\frac83.
]

Its modular representation is `666666674`. A common mistake is to use (f(p)=1) for a prime (p), forgetting that choosing (p) itself creates a self-loop.

Finally, equal exponents must be treated as a multiset rather than as distinguishable positions. The numbers (12=2^2\cdot3) and (18=2\cdot3^2) have the same exponent multiset ({1,2}), and their expectations are equal. A state keyed by the ordered prime list would miss this symmetry.

## Approaches

The direct approach follows the expectation recurrence. Let (f(n)) denote the expected remaining number of operations from (n), with (f(1)=0). If (\tau(n)) is the number of positive divisors, choosing a divisor uniformly gives

[
f(n)=1+\frac1{\tau(n)}\sum_{d\mid n}f(d).
]

The term (f(n)) appears in the sum because choosing (d=n) leaves the number unchanged. Rearranging gives

[
f(n)=
\frac{\tau(n)+\sum_{d\mid n,\ d<n}f(d)}
{\tau(n)-1}.
]

A brute-force implementation can generate every divisor (d\mid n), recursively calculate (f(d)), and memoize the result. It is correct because every divisor is exactly one possible next state. The problem is the divisor count. For (n\le10^{24}), a single number can have (1,290,240) divisors, and the total divisor count over all relevant states is on the order of (1.5\times10^{10}). That many operations cannot fit into a three-second contest limit.

The first useful observation is that the actual prime values do not matter. Suppose

[
x=\prod_i p_i^{e_i}
]

and

[
y=\prod_i q_i^{e'_i}
]

have the same multiset of exponents. Their divisors are obtained by independently choosing an exponent between (0) and each (e_i). Since the expectation of every resulting divisor depends only on its own exponent multiset, induction on the value of the number shows that (f(x)=f(y)). Thus a state can be represented solely by the unordered multiset of its positive prime exponents.

For example, the exponent states of (12) and (18) are both ((2,1)), so they share one memoized value. The representative with the smallest possible integer is obtained by assigning the largest exponent to the smallest prime, the next largest exponent to the next smallest prime, and so on. This gives a canonical ordering.

We still cannot enumerate every divisor of a representative. The second observation is to compute divisor sums as multidimensional prefix sums. Define

[
h(n,k)=
\sum_{d\mid\prod_{i=1}^k p_i^{e_i}}
f\left(
d\frac{n}{\prod_{i=1}^k p_i^{e_i}}
\right)
]

and let (g(n,k)) be the same sum restricted to proper divisors of the prefix. Then (h(n,k)=f(n)+g(n,k)).

Instead of enumerating all choices for the (k)-th exponent, split them into the case where its full exponent is used and the cases where at least one copy is removed. The latter part is exactly a partial divisor sum for (n/p_k). This gives a transition requiring only one smaller state per dimension. The resulting computation is proportional to the number of relevant exponent multisets times their number of distinct primes, rather than their number of divisors. The official analysis reports (172513) possible exponent multisets and about (1.17) million state-dimension transitions for (n\le10^{24}).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(\sum \tau(n))) over all states | (O(\text{number of states})) | Too slow |
| Optimal | (O( | S | \omega(n)+T\log n)) | (O( | S | \omega(n))) | Accepted |

Here (S) is the set of possible exponent multisets and (\omega(n)) is the number of distinct prime factors. The factorization of each input number costs only (O(m\log n)) with repeated division.

## Algorithm Walkthrough

1. Factor the given (n) using the supplied distinct prime factors. For every supplied prime (p), repeatedly divide (n) by (p) and count its exponent. The resulting exponent list is the complete prime factorization.
2. Sort the positive exponents in non-increasing order. This removes the identity of the primes from the state. Two integers with the same exponent multiset now use exactly the same DP state.
3. Define (F(E)) as the expected value for the exponent multiset (E), and define (G(A,B)) as the sum of (F) over all proper divisors obtained by changing only the prime factors represented by the multiset (A), while the multiset (B) is kept fixed.
4. If (A) is empty, there is no proper divisor generated by changing the empty prefix, so (G(\varnothing,B)=0). This is the base case of the prefix-sum recurrence.
5. Choose one exponent (a) from (A), preferably the largest one because all multisets are stored canonically. Let (A_0) be (A) with that exponent removed, and let (A_1) be (A) with (a) decreased by one, removing it if it becomes zero.
6. Partition the divisors according to the exponent chosen for this particular prime. If that exponent remains equal to (a), the divisor must be proper in the remaining prefix, giving (G(A_0,B\cup{a})). If it is smaller than (a), every resulting divisor is already proper, and its sum is (F(A_1\cup B)+G(A_1,B)).
7. Combine those two cases:

[
G(A,B)=
G(A_0,B\cup{a})
+
F(A_1\cup B)
+
G(A_1,B).
]

The first recursive call decreases the number of active prefix factors. The second branch decreases the total exponent sum, so the recursion is acyclic.

1. For a complete exponent multiset (E), the value (G(E,\varnothing)) is exactly the sum of (F(d)) over all proper divisors (d<E). Let

[
\tau(E)=\prod_{e\in E}(e+1).
]

The expectation recurrence becomes

[
F(E)=
\frac{\tau(E)+G(E,\varnothing)}
{\tau(E)-1}.
]

All arithmetic is performed modulo (10^9+7), replacing division by multiplication with a modular inverse.

1. Memoize both (F(E)) and (G(A,B)). Because (F) depends only on the sorted exponent multiset, all test cases with the same exponent pattern immediately reuse the result. The canonical sorting of both (A) and (B) also merges states that differ only by a permutation of equivalent prime factors.

### Why it works

The recurrence preserves exactly the set of proper divisors being summed. For (G(A,B)), every divisor chooses an exponent for the distinguished prime. Either that exponent is the original (a), in which case the remaining prefix must itself be a proper divisor, or it is at most (a-1), in which case the divisor is automatically proper. These cases are disjoint and cover every proper divisor exactly once. The recursive calls reduce either the number of active prefix factors or the total exponent sum, so every required value eventually reaches a base case. Finally, the expectation equation follows directly from conditioning on the uniformly selected divisor, so the computed (F(E)) is exactly the required expected value.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

# f_cache[E] = expected value for the exponent multiset E.
# E is always a tuple sorted in non-increasing order.
f_cache = {(): 0}

# g_cache[(A, B)] = sum of F over proper divisors generated by A,
# with the exponents in B fixed.
g_cache = {}

def get_f(e):
    e = tuple(sorted((x for x in e if x), reverse=True))
    if not e:
        return 0

    cached = f_cache.get(e)
    if cached is not None:
        return cached

    proper = get_g(e, ())
    tau = 1
    for x in e:
        tau = tau * (x + 1) % MOD

    ans = (tau + proper) % MOD
    ans = ans * pow(tau - 1, MOD - 2, MOD) % MOD

    f_cache[e] = ans
    return ans

def get_g(A, B):
    A = tuple(A)
    B = tuple(B)

    key = (A, B)
    cached = g_cache.get(key)
    if cached is not None:
        return cached

    if not A:
        return 0

    # A and B are stored in non-increasing order.
    # We take the largest exponent from A.
    a = A[0]
    A0 = A[1:]

    # Case 1: the chosen prime keeps its full exponent a.
    B0 = tuple(sorted(B + (a,), reverse=True))
    part_full = get_g(A0, B0)

    # Case 2: its exponent is smaller than a.
    if a == 1:
        A1 = A0
    else:
        A1 = tuple(sorted((a - 1,) + A0, reverse=True))

    combined = tuple(sorted(A1 + B, reverse=True))
    part_reduced = (get_f(combined) + get_g(A1, B)) % MOD

    ans = (part_full + part_reduced) % MOD
    g_cache[key] = ans
    return ans

def solve_case(n, primes):
    exponents = []

    for p in primes:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        exponents.append(e)

    exponents.sort(reverse=True)
    return get_f(tuple(exponents))

def main():
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, input().split())
        primes = list(map(int, input().split()))

        ans = solve_case(n, primes)
        out.append(f"Case #{case_id}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The factorization loop uses the supplied primes rather than trial division. Since every supplied prime divides the original (n), repeatedly dividing by it recovers its exact exponent. The remaining value of (n) becomes (1) after all supplied primes have been processed.

`get_f` canonicalizes its argument before looking it up. This is the symmetry reduction that makes (12) and (18), for example, share the same state ((2,1)).

`get_g` implements the two cases in the prefix recurrence. Taking `A[0]` is safe because the order inside (A) is irrelevant. After modifying an exponent, the resulting multisets are sorted again before memoization. Sorting is not merely cosmetic, it is what identifies states that differ only by a permutation of prime factors.

The expression for `tau` is (\prod(e_i+1)), the number of divisors. The denominator is `tau - 1` because the original state itself contributes (f(n)) to the divisor average. The modular inverse is computed with Fermat's theorem, since (10^9+7) is prime and the statement guarantees that the required denominator is invertible modulo the modulus.

Python integers safely hold the input bound (10^{24}), so no special big-integer representation is necessary. The modular values themselves remain below the modulus after every transition, preventing unnecessary growth.

The recurrence is memoized rather than evaluated for every divisor. This is the central implementation choice that changes the practical complexity from depending on the divisor count to depending on the much smaller exponent-state space. The state reduction and prefix-sum idea are the same structural simplifications used by the official solution.

## Worked Examples

### Sample 1: (n=2)

The input is

```
2 1
2
```

The factorization is (2^1), so the canonical exponent state is `(1)`.

| State | (A) | (B) | Value |
| --- | --- | --- | --- |
| Initial | `(1)` | `()` | (F(1)) |
| Prefix reduction | `()` | `(1)` | (G=0) |
| Smaller exponent | `()` | `()` | (F(\varnothing)=0) |
| Complete proper sum | `(1)` | `()` | (G=0) |
| Final | `(1)` | `()` | (F=2) |

There are two divisors, (1) and (2). The recurrence gives (f(2)=1+(0+f(2))/2), hence (f(2)=2). The output is `Case #1: 2`.

### Sample 2: (n=4)

The input is

```
4 1
```

with prime factor (2). Its exponent state is `(2)`.

| State | (A) | (B) | Contribution |
| --- | --- | --- | --- |
| Initial | `(2)` | `()` | (G((2),())) |
| Full exponent branch | `()` | `(2)` | (0) |
| Reduced exponent | `(1)` | `()` | (F(1)+G((1),())) |
| Prime state | `(1)` | `()` | (F(1)=2,\ G=0) |
| Complete proper sum | `(2)` | `()` | (G=2) |
| Final | `(2)` | `()` | ((3+2)/(3-1)=5/2) |

The three divisors of (4) are (1,2,4). Their expectations are (0,2,f(4)), so

[
f(4)=1+\frac{0+2+f(4)}3
]

and (f(4)=5/2). Since (2^{-1}\equiv500000004\pmod {10^9+7}), (5/2) becomes `500000006`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O( | S | \omega_{\max}+T\log n)) | Each relevant exponent state participates in only a small number of prefix transitions, while each test factors (n) using its supplied primes |
| Space | (O( | S | \omega_{\max})) | Memoized expectation and prefix-sum states |
| Number of exponent multisets | (172513) | Bound for (n\le10^{24}) |
| Total state-dimension transitions | about (1.17\times10^6) | Reported for the full allowed exponent-state space |

The official analysis gives (172513) possible exponent multisets and about (1173627) relevant state-dimension transitions under the (10^{24}) bound. This is small enough for the intended dynamic programming approach, while the brute-force divisor count is far too large.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# Provided samples.
sample = """6
2 1
2
4 1
2
6 2
2 3
8 1
2
10 2
2 5
12 2
2 3
"""

expected = """Case #1: 2
Case #2: 500000006
Case #3: 666666674
Case #4: 833333342
Case #5: 666666674
Case #6: 233333338
"""

assert run(sample) == expected, "provided samples"

# Minimum input.
assert run("""1
2 1
2
""") == """Case #1: 2
""", "minimum n"

# Same exponent multiset on different primes.
# 12 = 2^2 * 3 and 18 = 2 * 3^2, so both states are (2, 1).
assert run("""2
12 2
2 3
18 2
2 3
""") == """Case #1: 233333338
Case #2: 233333338
""", "same exponent multiset"

# Equal exponents exercise repeated values in the canonical multiset.
assert run("""1
36 2
2 3
""") == """Case #1: 675000013
""", "equal exponents"

# Maximum-size input allowed by the statement.
# The assertion checks that the solver handles the full 10^24 range
# and produces a valid single-case result.
maximum_input = """1
1000000000000000000000000 2
2 5
"""
maximum_output = run(maximum_input)
assert maximum_output.startswith("Case #1: "), "10^24 boundary"
value = int(maximum_output.split(": ")[1])
assert 0 <= value < 1000000007, "answer must be a residue"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 2` | `Case #1: 2` | Minimum-size state and self-transition |
| `12 2 / 2 3` and `18 2 / 2 3` | `Case #1: 233333338`, `Case #2: 233333338` | Exponent-multiset symmetry |
| `36 2 / 2 3` | `Case #1: 675000013` | Repeated equal exponents |
| `10^24, primes 2 5` | A residue in `[0,10^9+7)` | Maximum numerical boundary and large integer parsing |

For (36=2^2\cdot3^2), the exact expectation is (147/40), whose residue is `675000013`. This case is useful because a representation that accidentally treats equal exponents as distinct ordered data can create unnecessary states or produce inconsistent memoization.

## Edge Cases

For (n=2), the exponent state is `(1)`. The proper-divisor sum is zero because the only proper divisor is (1), whose expectation is zero. The divisor count is (2), so the formula gives (F=(2+0)/(2-1)=2). The algorithm reaches the empty prefix immediately and returns the correct result.

For (n=4), the exponent state is `(2)`. The recursive prefix calculation obtains (F(1)=2), so the proper-divisor sum for (4) is (2). With three divisors, (F(4)=(3+2)/2=5/2), producing `500000006`. The self-transition is accounted for by the denominator (\tau-1).

For (n=6), the exponent state is `(1,1)`. The two prime states both have expectation (2), and the proper-divisor sum is (0+2+2=4). Since (\tau(6)=4),

[
F(6)=\frac{4+4}{3}=\frac83,
]

which becomes `666666674`. This catches the common error of assuming that a prime always takes one operation.

For (n=12), the exponent state is `(2,1)`. The actual prime names disappear after factorization, so the state is identical to (18=2\cdot3^2). Both inputs consequently retrieve the same memoized value, (91/30), represented by `233333338`.

For (n=36), the exponent state is `(2,2)`. Equal exponents are kept as repeated entries rather than collapsed into a set, because the two prime factors still represent two independent choices. The resulting expectation is (147/40), and the algorithm outputs `675000013`.

For the maximum input (n=10^{24}=2^{24}5^{24}), the exponent state is simply `(24,24)`. Python can represent the input integer directly, while the DP never attempts to enumerate its (1,625) divisors repeatedly for each test case. More generally, the algorithm works with the exponent structure, which is the reason the (10^{24}) bound is manageable. The official solution likewise reduces the problem to the relatively small collection of possible exponent multisets rather than the huge collection of individual integers.
