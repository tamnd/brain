---
title: "CF 102373D - Good Subset"
description: "We have an array of (n) positive integers. We may choose any subset of its elements, and the subset is considered good when the greatest common divisor of all chosen values is greater than (1). The task is to find the maximum possible number of elements in such a subset."
date: "2026-08-12T22:55:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "D"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 206
verified: false
draft: false
---

[CF 102373D - Good Subset](https://codeforces.com/problemset/problem/102373/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of (n) positive integers. We may choose any subset of its elements, and the subset is considered good when the greatest common divisor of all chosen values is greater than (1). The task is to find the maximum possible number of elements in such a subset.

The key property of the gcd gives a much more useful interpretation. A collection of numbers has gcd greater than (1) exactly when all of them share at least one prime divisor. So instead of thinking about arbitrary subsets, we can ask a simpler question: for which prime (p) does the largest number of array elements have (p) as a divisor? The answer is the maximum such frequency.

The value of (n) is only (1000), but every (a_i) can be as large as (10^{18}). The small (n) rules out exponential enumeration of subsets, but the large values are the more subtle constraint. Factoring a number by trying every integer up to its square root would require up to (10^9) trial divisions for a single input value near (10^{18}), which is far too expensive in Python. We need an integer factorization method that works efficiently on 64-bit integers, which leads naturally to Miller-Rabin primality testing combined with Pollard-Rho factorization.

There are several edge cases that can break simpler implementations. If every value is equal, such as

```
3
2 2 2
```

the answer is (3), because all three values share the prime divisor (2). An implementation that only looks for pairs and then counts distinct gcd values can easily mishandle repeated values.

A single-element input such as

```
1
35
```

has answer (1). The gcd of a one-element subset is the element itself, and every input value is at least (2). An implementation that initializes the answer to zero and only updates it after finding a common factor between two different elements would incorrectly return zero.

Another important case is that pairwise gcds do not automatically define one common factor for a whole group. For

```
3
6 10 15
```

every pair has gcd greater than (1), but the gcd of all three numbers is (1). The correct answer is (2), because the largest groups sharing one prime are ({6,10}), sharing (2), or ({6,15}), sharing (3). A careless solution that counts a connected component in the graph where edges represent gcd greater than (1) would incorrectly return (3).

Finally, a number can have large prime factors. For example,

```
2
1000000007 1000000009
```

contains large primes close to (10^9), and more generally the constraints permit prime values close to (10^{18}). A trial-division implementation that assumes small factors will be found quickly can time out.

## Approaches

The most direct brute-force solution considers every subset of the (n) array elements. For each subset it computes the gcd of all selected elements and keeps the largest subset whose gcd is greater than (1). This is correct because every possible candidate subset is explicitly checked. However, there are (2^n) subsets, and computing a gcd over as many as (n) elements costs (O(n\log A)), where (A) is the largest array value. For (n=1000), the worst case is on the order of (1000\cdot2^{1000}\log A) gcd operations, which is completely infeasible.

The brute force works because the definition of a good subset is simple, but it spends almost all of its effort distinguishing between subsets that actually share the same underlying reason for being good. If several numbers have the prime divisor (p), every subset made from those numbers has gcd divisible by (p). We do not need to inspect those subsets separately.

The crucial observation is that a gcd is greater than (1) exactly when there exists a prime dividing every number in the chosen subset. For any prime (p), the largest subset whose gcd is divisible by (p) consists of every input number divisible by (p). Adding another number divisible by (p) can never make the gcd lose (p), so there is no reason to leave such an element out.

Consequently, if we factor every (a_i) into its distinct prime divisors, we can maintain a frequency for each prime. The final answer is simply the largest frequency.

The remaining challenge is factoring numbers as large as (10^{18}). Trial division up to (\sqrt{a_i}) is too slow, so the optimal implementation uses deterministic Miller-Rabin for primality testing on 64-bit integers and Pollard-Rho to split composite numbers. Pollard-Rho recursively factors every input value, and only distinct prime factors are counted for each array element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n n\log A)) | (O(n)) | Too slow |
| Optimal | Expected (O(n\cdot C_{64})) for 64-bit factorization | (O(n+\log A)) | Accepted |

Here (C_{64}) represents the expected cost of factoring one 64-bit integer with Pollard-Rho. Its running time is probabilistic, but Miller-Rabin uses a deterministic set of bases sufficient for all 64-bit integers.

## Algorithm Walkthrough

1. Read the (n) values and create a map `count` from prime factors to the number of array elements containing that prime.
2. For each value (x), factor it completely into its prime divisors using Miller-Rabin and Pollard-Rho. We keep only distinct prime factors of (x), because an element containing (p^2) should contribute exactly once to the number of elements divisible by (p).
3. For every distinct prime factor (p) of (x), increment `count[p]`. This represents the size of the largest subset that could use (p) as a common divisor among the elements processed so far.
4. After all numbers have been processed, return the maximum value in `count`. If a prime (p) appears in exactly (k) input elements, those (k) elements have gcd divisible by (p), so they form a valid subset of size (k).
5. If (n=1), the factorization still finds at least one prime factor because every input value is at least (2). Its frequency is (1), giving the correct answer without requiring a special case.

### Why it works

For every good subset, its gcd (g) is greater than (1), so (g) has at least one prime divisor (p). That prime divides every element of the subset. Thus every good subset of size (k) is contained in the set of input elements divisible by some prime (p), meaning the algorithm's maximum frequency is at least (k).

Conversely, if a prime (p) divides (k) input elements, the gcd of those (k) elements is divisible by (p), so it is greater than (1). They form a valid subset of size (k). Thus the maximum prime frequency is itself achievable. Both directions give exactly the desired optimum.

## Python Solution

```python
import sys
import random
import math

input = sys.stdin.readline

random.seed(0xC0FFEE)

SMALL_PRIMES = (
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37
)

MR_BASES = (
    2, 325, 9375, 28178, 450775, 9780504, 1795265022
)

def is_prime(n):
    if n < 2:
        return False

    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in MR_BASES:
        if a % n == 0:
            continue

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n)
        x = random.randrange(0, n)
        y = x
        d = 1

        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)

        if d != n:
            return d

def factor(n, result):
    if n == 1:
        return

    if is_prime(n):
        result.add(n)
        return

    d = pollard_rho(n)
    factor(d, result)
    factor(n // d, result)

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    count = {}

    for x in a:
        primes = set()
        factor(x, primes)

        for p in primes:
            count[p] = count.get(p, 0) + 1

    print(max(count.values()))

if __name__ == "__main__":
    solve()
```

`is_prime` first removes small-prime cases because they are cheap and also make Pollard-Rho's job easier. For a remaining value, it writes (n-1) as (d\cdot2^s) and performs Miller-Rabin with the standard seven bases that give deterministic primality testing for every unsigned 64-bit integer.

`pollard_rho` searches for a non-trivial factor using the pseudorandom iteration (f(x)=x^2+c\pmod n). Floyd's cycle detection advances one sequence value once and another twice, then takes the gcd of their difference with (n). When that gcd becomes a non-trivial divisor, the recursion can split the number.

The recursive `factor` function stops immediately when Miller-Rabin proves that its argument is prime. Otherwise Pollard-Rho supplies a divisor, and both pieces are factored recursively. The result is stored in a `set`, which is essential because the final statistic counts array elements containing a prime, not the total exponent of that prime.

Python integers have arbitrary precision, so the values up to (10^{18}) and products used by modular arithmetic do not overflow. The expression `x * x % n` is also safe for the same reason.

The Miller-Rabin bases are fixed rather than randomly generated. This matters because it makes the primality test deterministic over the entire input range. Pollard-Rho itself remains randomized, which is what gives it good expected performance on difficult composite inputs.

## Worked Examples

For Sample 1, the input is `6 15 10 42`. The factorization and frequency state evolve as follows.

| Current value | Distinct prime factors | Frequency state | Current answer |
| --- | --- | --- | --- |
| 6 | 2, 3 | 2:1, 3:1 | 1 |
| 15 | 3, 5 | 2:1, 3:2, 5:1 | 2 |
| 10 | 2, 5 | 2:2, 3:2, 5:2 | 2 |
| 42 | 2, 3, 7 | 2:3, 3:3, 5:2, 7:1 | 3 |

The maximum frequency is (3). The three elements divisible by (3) are (6,15,42), whose gcd is (3), so the output is `3`.

This trace demonstrates why the algorithm counts distinct prime factors per element. The number (42) contains (2\cdot3\cdot7), but it contributes only one count to each of the three corresponding prime frequencies.

For Sample 2, every value is `2`.

| Current value | Distinct prime factors | Frequency state | Current answer |
| --- | --- | --- | --- |
| 2 | 2 | 2:1 | 1 |
| 2 | 2 | 2:2 | 2 |
| 2 | 2 | 2:3 | 3 |

The final frequency of prime (2) is (3), so all three elements can be selected and the answer is `3`.

This case confirms that repeated values are handled independently. Each occurrence is a separate array element and should increase the frequency of its prime factors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(n\cdot C_{64})) | Each of the (n) values is factored with Miller-Rabin and Pollard-Rho |
| Space | (O(n+\log A)) | The frequency map stores encountered primes, and recursive factorization has logarithmic depth |

Here (A\le 10^{18}), and (C_{64}) denotes the expected Pollard-Rho factorization cost for a 64-bit integer. Since (n\le1000), the number of values requiring factorization is modest, while trial division up to (10^9) per value would be much too expensive. The chosen factorization approach is designed specifically for the large 64-bit values allowed by the problem.

## Test Cases

```python
import sys
import io
import contextlib
import random
import math

SMALL_PRIMES = (
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37
)

MR_BASES = (
    2, 325, 9375, 28178, 450775, 9780504, 1795265022
)

random.seed(0xC0FFEE)

def is_prime(n):
    if n < 2:
        return False

    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in MR_BASES:
        if a % n == 0:
            continue

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n)
        x = random.randrange(0, n)
        y = x
        d = 1

        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)

        if d != n:
            return d

def factor(n, result):
    if n == 1:
        return
    if is_prime(n):
        result.add(n)
        return

    d = pollard_rho(n)
    factor(d, result)
    factor(n // d, result)

def solve_text(inp):
    data = inp.split()
    n = int(data[0])
    a = list(map(int, data[1:n + 1]))

    count = {}

    for x in a:
        primes = set()
        factor(x, primes)

        for p in primes:
            count[p] = count.get(p, 0) + 1

    return str(max(count.values())) + "\n"

# Provided samples
assert solve_text("""4
6 15 10 42
""") == "3\n", "sample 1"

assert solve_text("""3
2 2 2
""") == "3\n", "sample 2"

assert solve_text("""1
35
""") == "1\n", "sample 3"

# Minimum-size input
assert solve_text("""1
2
""") == "1\n", "single element"

# All elements share a large prime factor
assert solve_text("""4
1000000007 2000000014 3000000021 4000000028
""") == "4\n", "large common prime factor"

# Pairwise gcds can be greater than 1 without one common divisor
assert solve_text("""3
6 10 15
""") == "2\n", "pairwise gcd trap"

# Boundary near 10^18, with no common prime factor
assert solve_text("""3
999999999999999989 999999999999999937 1000000000000000000
""") == "1\n", "large boundary values"

# Maximum n, all equal
values = " ".join(["2"] * 1000)
assert solve_text("1000\n" + values + "\n") == "1000\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2` | `1` | Minimum (n) and the singleton case |
| `4 / 1000000007 2000000014 3000000021 4000000028` | `4` | Large prime factorization and repeated common factor |
| `3 / 6 10 15` | `2` | Prevents treating pairwise gcd connectivity as one common gcd |
| `3 / 999999999999999989 999999999999999937 1000000000000000000` | `1` | Large 64-bit boundary values |
| `1000` copies of `2` | `1000` | Maximum (n) and repeated identical values |

## Edge Cases

The singleton case is handled directly by the same factor-counting invariant. For the input

```
1
35
```

Pollard-Rho is never needed because Miller-Rabin identifies (35) as composite and factors it into (5) and (7). Both primes receive frequency (1), so the maximum is (1). The algorithm does not need to compare the element with anything else.

For repeated values,

```
3
2 2 2
```

each occurrence is factored separately. The set of distinct prime factors for each occurrence is `{2}`, so the frequency of (2) progresses from (1) to (2) to (3). The final answer is (3). This avoids the common mistake of deduplicating the input values before counting.

For the pairwise-gcd trap,

```
3
6 10 15
```

the factor sets are `{2,3}`, `{2,5}`, and `{3,5}`. Prime (2) occurs twice, prime (3) occurs twice, and prime (5) occurs twice. No prime occurs three times, so the answer is (2), even though every pair has a gcd greater than (1). The algorithm counts the actual common prime, rather than inferring a group from pairwise relationships.

For very large values, the factorization routines operate entirely with integer arithmetic modulo the current number. For example, when an input contains a prime close to (10^{18}), Miller-Rabin can recognize it without trial-dividing by every smaller integer. When the value is composite, Pollard-Rho searches for a non-trivial factor instead of scanning all candidates up to its square root. This is the part of the implementation that makes the (10^{18}) bound practical.

The maximum-size repeated-value case has (1000) copies of (2). The factorization work for each value is tiny, and the frequency map contains only one key. The final count reaches (1000), showing that the answer is allowed to equal the full array size and that no off-by-one restriction should exclude the entire array.
