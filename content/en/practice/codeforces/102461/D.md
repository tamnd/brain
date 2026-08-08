---
title: "CF 102461D - RSA factoring"
description: "The number (n) is deliberately generated from unusually close prime factors. For (k=2), there are two distinct (b)-bit primes (p1,p2), where (p2) is the prime immediately after (p1), and (n=p1p2). For (k=4), there are two independent such pairs, so [ n=p1p2q1q2."
date: "2026-08-08T09:55:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102461
codeforces_index: "D"
codeforces_contest_name: "Innopolis Open 2019-2020, qualification, contest 2"
rating: 0
weight: 102461
solve_time_s: 125
verified: true
draft: false
---

[CF 102461D - RSA factoring](https://codeforces.com/problemset/problem/102461/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The number (n) is deliberately generated from unusually close prime factors. For (k=2), there are two distinct (b)-bit primes (p_1,p_2), where (p_2) is the prime immediately after (p_1), and (n=p_1p_2). For (k=4), there are two independent such pairs, so

[
n=p_1p_2q_1q_2.
]

Every prime has exactly (b) bits, and all prime factors are distinct. The input gives (b), whether there are two or four factors, and (n) in hexadecimal. We have to print the prime factors, also in hexadecimal. These guarantees are part of the mathematical structure we exploit, rather than merely validation conditions.

The largest possible (n) has (4b\le240) bits. That is much too large for ordinary trial division. Even though all factors themselves have only 60 bits, trying every possible divisor up to the first factor can require about (2^{60}) divisions in the worst case. For (k=4), the usual generic bound of searching all divisors up to (\sqrt n) would be even worse, around (2^{120}) candidates. A one-second limit rules out both approaches.

The useful part of the construction is not that the primes are merely 60-bit numbers. Consecutive primes are close, so their products admit factor pairs that are extremely close to each other. Close factor pairs are exactly what Fermat's factorization method is designed to find.

There are several edge cases that a careless implementation can mishandle. The first is starting the Fermat search from the floor rather than the ceiling of (\sqrt n). For example,

```
4 2
dd
```

represents (221=13\cdot17). Since (\sqrt{221}) lies between 14 and 15, the correct starting value is (a=15). Then (15^2-221=4=2^2), giving (13) and (17). Starting at 14 produces a negative difference, so an implementation that immediately calls an integer square root on it fails.

The second edge case is assuming that (a) can be advanced only through odd values. For the sample

```
4 2
8f
```

we have (143=11\cdot13), and the successful value is (a=12), which is even. Restricting the search to odd (a) would skip the answer completely.

The third edge case appears when (k=4). For

```
6 4
534ee3
```

the factors are (37,41,59,61). One Fermat representation gives (2257=37\cdot61) and (2419=41\cdot59), but these are not prime factors. A solution that stops after finding one representation has only found two composite divisors. We need another representation and then gcds between the resulting divisors.

Finally, an input with all equal prime factors is not a valid test case. The statement explicitly guarantees that all factors are distinct, so a test such as (11\cdot11) would violate the input contract. In particular, the correct test suite should not expect the submitted solution to handle that invalid situation.

## Approaches

The straightforward approach is trial division. Starting from 2, test whether each integer divides (n), and stop after finding enough factors. This is correct because every composite integer has a divisor no larger than its square root, and here the first prime factor is itself roughly (2^{b-1}) or larger. With (b=60), that means potentially on the order of (2^{60}) divisibility tests. Even if each test were extremely cheap, this is far beyond the time limit.

The structure of the generated primes gives us a much better starting point. Suppose first that (k=2), so (n=pq) and (p,q) are close. Write

[
a=\frac{p+q}{2},\qquad c=\frac{q-p}{2}.
]

Because (p) and (q) are odd, both expressions are integers. Then

[
n=pq=(a-c)(a+c)=a^2-c^2.
]

Consequently,

[
a^2-n=c^2.
]

Instead of searching for a divisor, we search for the smallest (a\ge\sqrt n) for which (a^2-n) is a perfect square. Once such an (a) is found, the two factors are simply (a-c) and (a+c).

This is Fermat factorization. The reason it is fast here is the same reason the generation procedure is weak: the two prime factors are close. If their difference is (g=q-p), the successful value of (a) is only about

[
\frac{g^2}{8\sqrt n}
]

positions away from (\sqrt n). For consecutive primes around (2^b), the typical gap is on the logarithmic scale of the prime size, so this search is tiny for (b\le60). The average gap between primes near (x) is roughly (\ln x).

The four-factor case initially looks harder because (n) does not have to be a product of two close numbers. The key is to pair the four primes differently. Consider

[
n=(p_1q_1)(p_2q_2).
]

Since (p_1,p_2) are close and (q_1,q_2) are close, these two products are also close. We can similarly use

[
n=(p_1q_2)(p_2q_1).
]

Both are valid Fermat decompositions. Their four factors are composite, but they overlap in exactly one prime at a time. For example,

[
\gcd(p_1q_1,p_1q_2)=p_1.
]

Thus once we have several close factor pairs, ordinary gcd operations recover the individual primes.

The official solution follows the same square-difference idea, collecting several divisors produced by Fermat representations and then taking gcds between them.

The brute-force method works because divisibility eventually exposes a prime factor, but fails because the factor itself can be 60 bits. The observation that the generated factors are consecutive primes lets us search for square differences instead, reducing the work from exponential in (b) to a search governed by the small prime gaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^b)) divisions in the worst case | (O(1)) | Too slow |
| Optimal | (O(T\cdot M(b))), with (T) governed by the small prime gaps | (O(k)) | Accepted |

Here (M(b)) denotes the cost of arithmetic on (O(b))-bit integers, and (T) is the number of Fermat candidates tested. For the generated random primes, (T) is very small. For the four-factor construction, if the two consecutive-prime gaps are (g) and (h), the close cross-pair products lead to roughly (O((g+h)^2)) Fermat iterations, which is tiny for (b\le60).

## Algorithm Walkthrough

1. Parse (n) from hexadecimal into Python's arbitrary-precision integer type. Python integers can represent the full 240-bit value directly, so there is no overflow issue.
2. Compute (a=\lceil\sqrt n\rceil). Fermat's identity needs (a^2-n\ge0), so starting at the ceiling avoids negative values.
3. Repeatedly compute

[
d=a^2-n
]

and test whether (d) is a perfect square. We calculate (s=\lfloor\sqrt d\rfloor) and check whether (s^2=d). If it is, then

[
n=a^2-s^2=(a-s)(a+s),
]

so both (a-s) and (a+s) are divisors of (n). We insert them into a set because the same divisor can arise from different representations.

1. Continue until at least (k) distinct divisors have been found. For (k=2), the first successful representation must be the two prime factors themselves, because (n) has exactly two prime factors.
2. For (k=4), take the gcd of every pair of distinct divisors collected in the previous step. Every collected divisor is a product of two of the four original primes. Two different such products either share no prime or share exactly one prime, so their gcd is either 1 or one of the desired primes.
3. Keep all gcds greater than 1, sort the resulting prime factors, and print them in hexadecimal. The output order is not mathematically significant, but sorting makes the result deterministic.

### Why it works

The invariant is that every number inserted into the divisor set is a genuine divisor of (n), because it comes from an identity (n=(a-s)(a+s)). In the two-factor case, any nontrivial factor pair consists exactly of the two prime factors. In the four-factor case, the two cross-pair decompositions produce four distinct products such as (p_1q_1,p_2q_2,p_1q_2,p_2q_1). Because the four primes are distinct, taking gcds between these products isolates each prime. Thus every value eventually printed is prime and divides (n), while the required number of distinct prime factors is recovered.

## Python Solution

```python
import sys
from math import isqrt, gcd

input = sys.stdin.readline

def factor_case(b, k, n):
    a = isqrt(n)
    if a * a < n:
        a += 1

    divs = set()

    while len(divs) < k:
        d = a * a - n
        s = isqrt(d)

        if s * s == d:
            divs.add(a - s)
            divs.add(a + s)

        a += 1

    if k == 2:
        ans = sorted(divs)
    else:
        values = list(divs)
        ans = set()

        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                g = gcd(values[i], values[j])
                if g > 1:
                    ans.add(g)

        ans = sorted(ans)

    return ans[:k]

def solve():
    b, k = map(int, input().split())
    n = int(input().strip(), 16)

    ans = factor_case(b, k, n)

    for x in ans:
        print(format(x, "x"))

if __name__ == "__main__":
    solve()
```

The first part of `factor_case` establishes the Fermat search point. `isqrt(n)` returns the floor, so the explicit multiplication check is needed to move to the ceiling when (n) is not a perfect square.

The main loop mirrors the square-difference identity directly. Because (a\ge\lceil\sqrt n\rceil), `d` is never negative. `isqrt(d)` gives the largest integer whose square is at most `d`, and comparing `s * s` with `d` is an exact perfect-square test.

The set `divs` is deliberately used instead of a list. A square representation gives two divisors, and several representations may contain the same divisor. The stopping condition asks for distinct divisors, matching the logic needed for the four-factor case.

For (k=2), the divisors obtained from the first successful representation are already the two primes. For (k=4), the code does not perform a primality test. That is safe because every divisor we collected is a product of exactly two of the four distinct primes. Two distinct such products cannot have a composite gcd: if they share both primes, they would be the same product. Their gcd is consequently either 1 or one original prime.

Python's arbitrary-precision integers are particularly convenient here. The largest value of (n) has only 240 bits, so multiplication, subtraction, square root, and gcd are all practical.

The hexadecimal conversion uses `format(x, "x")`. It produces lowercase hexadecimal without leading zeroes, exactly matching the required representation.

## Worked Examples

### Sample 1

The input is

```
4 2
8f
```

The hexadecimal value `8f` is (143), and the required factors are (11) and (13).

| Step | (a) | (a^2-n) | (s=\lfloor\sqrt{d}\rfloor) | Square? | Divisors |
| --- | --- | --- | --- | --- | --- |
| Start | 12 | 1 | 1 | Yes | 11, 13 |

The ceiling of (\sqrt{143}) is 12. At once,

[
12^2-143=1^2,
]

so

[
143=(12-1)(12+1)=11\cdot13.
]

The hexadecimal output is therefore `b` and `d`. This example also demonstrates why the search must not skip even values of (a).

### Sample 2

The input is

```
6 4
534ee3
```

The decimal value is (5,459,683), and its prime factors are (37,41,59,61). The first useful cross pairing is

[
37\cdot61=2257,\qquad41\cdot59=2419.
]

Their midpoint is 2338.

| Step | (a) | (a^2-n) | (s) | Square? | New divisors |
| --- | --- | --- | --- | --- | --- |
| Start | 2338 | 6561 | 81 | Yes | 2257, 2419 |
| Next | 2339 | 11240 | 106 | No | none |
| Next | 2340 | 15917 | 126 | No | none |
| Next | 2341 | 20596 | 143 | No | none |
| Next | 2342 | 25281 | 159 | Yes | 2183, 2501 |

The second representation corresponds to

[
37\cdot59=2183,\qquad41\cdot61=2501.
]

Now the gcds reveal the primes:

[
\gcd(2257,2183)=37,
]

[
\gcd(2257,2501)=61,
]

[
\gcd(2419,2183)=59,
]

[
\gcd(2419,2501)=41.
]

The hexadecimal forms are `25`, `29`, `3b`, and `3d`, matching the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T\cdot M(b)+k^2\log n)) | (T) Fermat candidates are tested, followed by at most 6 gcds for (k=4) |
| Space | (O(k)) | At most four distinct divisors and four recovered primes are stored |

The important quantity is (T), not the magnitude of (n) itself. For two factors with gap (g), Fermat reaches the answer after roughly (g^2/(8\sqrt n)) increments. For four factors, if the two consecutive-prime gaps are (g) and (h), a cross pairing differs by about (2^b(g+h)), while its square root is about (2^{2b}). The resulting number of iterations is roughly ((g+h)^2/8). Consecutive prime gaps around (2^b) are small on the scale relevant here, so the search is easily practical for (b\le60). The problem's one-second limit is designed around this structural shortcut.

## Test Cases

The test helper below calls the same factoring routine used by the submitted solution. The maximum-size case uses the two consecutive primes immediately above (2^{60}), and constructs the hexadecimal input inside the test so there is no need to manually convert a 120-bit product.

```python
import sys
import io
from math import isqrt, gcd

input = sys.stdin.readline

def factor_case(b, k, n):
    a = isqrt(n)
    if a * a < n:
        a += 1

    divs = set()

    while len(divs) < k:
        d = a * a - n
        s = isqrt(d)

        if s * s == d:
            divs.add(a - s)
            divs.add(a + s)

        a += 1

    if k == 2:
        ans = sorted(divs)
    else:
        values = list(divs)
        ans = set()

        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                g = gcd(values[i], values[j])
                if g > 1:
                    ans.add(g)

        ans = sorted(ans)

    return ans[:k]

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        b, k = map(int, input().split())
        n = int(input().strip(), 16)
        ans = factor_case(b, k, n)

        return "".join(format(x, "x") + "\n" for x in ans)
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample 1.
assert run("""4 2
8f
""") == """b
d
""", "sample 1"

# Provided sample 2.
assert run("""6 4
534ee3
""") == """25
29
3b
3d
""", "sample 2"

# Minimum b, four factors: 5, 7 and 11, 13.
assert run("""4 4
138d
""") == """5
7
b
d
""", "minimum-size four-factor case"

# Boundary case where ceil(sqrt(n)) is exactly the successful Fermat value.
# 221 = 13 * 17, and ceil(sqrt(221)) = 15.
assert run("""4 2
dd
""") == """d
11
""", "ceil-sqrt boundary"

# Maximum b, two consecutive 60-bit primes.
p = 1152921504606847009
q = 1152921504606847067
max_n = p * q

max_input = f"60 2\n{max_n:x}\n"
max_output = f"{p:x}\n{q:x}\n"

assert run(max_input) == max_output, "maximum-size case"

# Four factors with different consecutive-prime gaps.
# 37, 41 and 59, 61.
assert run("""6 4
534ee3
""") == """25
29
3b
3d
""", "two close prime pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 4 / 138d` | `5, 7, b, d` | Minimum (b), four-factor construction |
| `4 2 / dd` | `d, 11` | Correct ceiling of the square root |
| `60 2 / generated from p*q` | `p, q` | Maximum bit size and arbitrary-precision arithmetic |
| `6 4 / 534ee3` | `25, 29, 3b, 3d` | Multiple Fermat representations and gcd recovery |

The requested all-equal-factor test cannot be a valid input because the problem guarantees distinct prime factors. An input such as (121=11\cdot11) would violate that guarantee and would also change the behavior of the Fermat search, so it should be tested separately only if one is testing invalid-input handling, which this problem does not require.

## Edge Cases

The floor-versus-ceiling boundary is handled by explicitly checking `a * a < n`. For

```
4 2
dd
```

we have (n=221), `isqrt(221)` gives 14, and the code increments it to 15. It then obtains (15^2-221=4), so the divisors are (15-2=13) and (15+2=17), printed as `d` and `11`.

The parity issue is handled by incrementing (a) by exactly one. For

```
4 2
8f
```

the successful value is (a=12). A search that examines only odd values would inspect 11, 13, 15, and so on and never encounter the required representation at 12. The implementation does not make any parity assumption about (a).

The four-factor case requires more than one factorization identity. For

```
6 4
534ee3
```

the first square representation produces (2257) and (2419), corresponding to (37\cdot61) and (41\cdot59). The second produces (2183) and (2501), corresponding to (37\cdot59) and (41\cdot61). Their pairwise gcds isolate all four primes. The set-based stopping condition guarantees that the algorithm does not stop after discovering only one pair.

Hexadecimal parsing is handled by `int(..., 16)`, so both uppercase and lowercase input digits are accepted even though the examples use lowercase. Output is generated with lowercase hexadecimal and no leading zeroes, so values such as decimal 11 and 13 become exactly `b` and `d`.

The largest values require no special overflow handling. A 240-bit integer is comfortably supported by Python's arbitrary-precision integers, and all intermediate values such as (a^2) remain of manageable size. The implementation never converts (n) to floating point, which avoids losing precision when (n) is close to (2^{240}).

An all-equal factor case is deliberately absent from the valid tests. For example, `4 2` with (n=121) would represent (11\cdot11), but repeated factors are forbidden by the input guarantee. The solution is allowed to rely on distinctness, and the proof of the gcd step also relies on it.
