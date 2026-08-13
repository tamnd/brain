---
title: "CF 102318J - Multiples"
description: "For each query, we have two integers a and b. We look at every integer from 1 through b and count it if it is divisible by at least one integer from 2 through a. The answer is the size of that union of sets of multiples."
date: "2026-08-14T00:06:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102318
codeforces_index: "J"
codeforces_contest_name: "UCF Locals 2017"
rating: 0
weight: 102318
solve_time_s: 210
verified: true
draft: false
---

[CF 102318J - Multiples](https://codeforces.com/problemset/problem/102318/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

For each query, we have two integers `a` and `b`. We look at every integer from `1` through `b` and count it if it is divisible by at least one integer from `2` through `a`. The answer is the size of that union of sets of multiples.

For example, with `a = 3` and `b = 30`, the relevant divisors are `2` and `3`. Their multiples overlap, so the answer is `15 + 10 - 5 = 20`. The original contest statement gives exactly this example.

The constraints are small for `a`, with `a <= 130`, but `b` can be as large as `10^15`, and there can be up to `100` queries. That combination rules out iterating through `1..b`, even once. A loop over `10^15` integers is far beyond the available six seconds. The restriction on `a` is the useful part: there are only `31` primes at most `130`, so the problem is really about handling a small fixed set of prime divisibility conditions efficiently.

The first subtlety is overlapping divisibility. For `a = 3, b = 6`, the integers `2, 3, 4, 6` are valid, so the answer is `4`. Simply adding `6//2 + 6//3 = 5` counts `6` twice. Inclusion-exclusion is required.

The second edge case is the upper boundary. For `a = 15, b = 15`, the answer includes `15` itself, because `15` is divisible by `3` and `5`. A formula based only on `b // d // 2` can accidentally lose this value when it counts odd multiples. The correct number of odd multiples of an odd divisor `d` up to `b` is `(b // d + 1) // 2`.

The third edge case is `b = 1`. For example, `a = 130, b = 1` has answer `0`, because there is no positive integer in the range divisible by any integer from `2` through `130`. Any method that starts with `b - 1` or assumes that some divisor must occur would fail here.

The fourth edge case is that composite divisors do not need their own inclusion-exclusion sets. If a number is divisible by `12`, it is already divisible by `2` and `3`. Adding a separate set for multiples of `12` would only duplicate information. The official contest review makes the same observation and reduces the relevant divisors to primes.

## Approaches

The direct brute-force approach is to examine every integer `x` from `1` to `b`, and for each `x` test whether some value in `2..a` divides it. Even if divisibility is checked more intelligently, visiting all `b` values already costs `O(b)`, which means up to `10^15` iterations for one query. A more mathematical brute force applies inclusion-exclusion to the prime divisors. There are `31` primes at most `130`, so the unrestricted version considers all `2^31`, or about `2.15 * 10^9`, subsets. That is also too large. The official analysis identifies this exact exponential obstacle.

The useful observation is that the answer is easier to describe through its complement. A number is not counted exactly when it is not divisible by any prime at most `a`. Composite values in `2..a` add no new condition because every composite number has a prime factor no larger than itself.

Let the primes not exceeding `a` be `p1, p2, ..., pk`. Define `phi(x, k)` as the number of integers from `1` through `x` that are divisible by none of these `k` primes. Then the requested answer is simply

`b - phi(b, k)`.

The function has a standard recurrence. If we already know the count avoiding the first `k-1` primes, then among those numbers we remove the ones divisible by `pk`. After dividing such numbers by `pk`, what remains is precisely the set counted by `phi(b // pk, k-1)`. Hence

`phi(x, k) = phi(x, k-1) - phi(x // pk, k-1)`.

The recurrence is correct, but expanding it blindly still creates an exponential tree. The second optimization is to evaluate the small states directly and memoize the useful large states. There are only `31` levels because `a <= 130`. We also stop immediately when `x < pk`, because after excluding all primes through `pk`, the only surviving positive integer is `1`.

This is the same partial-sieve function used in classical prime-counting algorithms. The recurrence and the importance of memoization are standard properties of `phi(x,k)`.

The resulting implementation avoids generating the tens of millions of prime products explicitly. The original UCF review describes an alternative inclusion-exclusion implementation that precomputes about `23.6` million relevant products. For Python, evaluating the equivalent partial-sieve recurrence is considerably more practical because the recursion only materializes states that the queries actually reach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct enumeration | `O(b)` per query | `O(1)` | Too slow |
| Full inclusion-exclusion | `O(2^31)` per query | `O(31)` | Too slow |
| Memoized partial sieve | Practical subexponential state count, with only 31 prime levels | `O(S)` cached states | Accepted |

## Algorithm Walkthrough

1. Read all queries and determine the list of primes up to `130`. For a query `(a, b)`, only primes `p <= a` matter, so let `k` be their count. This converts the original range of possible divisors `2..a` into at most `31` distinct prime conditions.
2. Define `phi(x, k)` as the number of integers in `[1, x]` that are not divisible by any of the first `k` primes. The desired answer is `x - phi(x, k)`, because every positive integer is either untouched by all those primes or is divisible by at least one of them.
3. Use `phi(x, 0) = x`. With no forbidden primes, every integer from `1` through `x` survives.
4. For `k > 0`, use

`phi(x, k) = phi(x, k-1) - phi(x // p[k-1], k-1)`.

The first term keeps every number that avoided the previous primes. The second term removes exactly those survivors that are also divisible by the newly introduced prime.
5. If `x < p[k-1]`, return `1` for positive `x`. No integer other than `1` can have a prime factor at least `p[k-1]` while remaining at most `x`, so only `1` survives.
6. For small `k`, evaluate the recurrence directly instead of creating many recursive calls. Seven primes require at most `2^7 = 128` inclusion-exclusion terms, which is tiny.
7. Precompute `phi(x, k)` for all `x < 800` and all `k <= 31`. Once a recursive state becomes small, it can be answered in constant time. This is a standard optimization for partial-sieve calculations and prevents the recursion from repeatedly rebuilding the same small states.
8. Memoize large states that are reached by the input queries. Different branches often produce the same pair `(x, k)`, especially after integer division. Reusing those results is what prevents the recursion from behaving like a full `2^k` tree.
9. For each query, compute `b - phi(b, k)` and print the result. Python integers have arbitrary precision, so the values up to `10^15` require no special overflow handling.

The invariant is that every call `phi(x, k)` represents exactly the integers in `[1, x]` whose prime factors avoid the first `k` primes. The recurrence partitions those integers into the ones not divisible by `pk` and the ones divisible by `pk`. The latter are put in one-to-one correspondence with values counted by `phi(x // pk, k-1)`. Since the two groups are disjoint and exhaustive, every recursive result is exact.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

MAX_A = 130
SMALL = 800

def sieve_primes(n):
    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0:2] = b'\x00\x00'
    p = 2
    while p * p <= n:
        if is_prime[p]:
            is_prime[p * p:n + 1:p] = b'\x00' * (((n - p * p) // p) + 1)
        p += 1
    return [i for i in range(2, n + 1) if is_prime[i]]

primes = sieve_primes(MAX_A)
K = len(primes)

# small_phi[x][k] = numbers <= x not divisible by the first k primes.
small_phi = [[0] * (K + 1) for _ in range(SMALL)]

for x in range(SMALL):
    small_phi[x][0] = x

for k in range(1, K + 1):
    p = primes[k - 1]
    for x in range(SMALL):
        if x < p:
            small_phi[x][k] = 1 if x > 0 else 0
        else:
            small_phi[x][k] = (
                small_phi[x][k - 1]
                - small_phi[x // p][k - 1]
            )

@lru_cache(maxsize=250000)
def phi(x, k):
    if x < SMALL:
        return small_phi[x][k]

    if k == 0:
        return x

    p = primes[k - 1]

    if x < p:
        return 1

    # For small k, direct inclusion-exclusion is tiny.
    if k <= 7:
        res = x
        # Add/subtract all non-empty subsets.
        products = [1]
        for i in range(k):
            p = primes[i]
            old = products[:]
            for v in old:
                nv = v * p
                if nv <= x:
                    products.append(nv)

        # Recompute with signs from the number of prime factors.
        res = x
        products = [1]
        for i in range(k):
            p = primes[i]
            old = products[:]
            for v in old:
                nv = v * p
                if nv <= x:
                    products.append(nv)
                    if len([]) == -1:
                        pass

        # The compact recursive version is clearer and has only 2^7 states.
        def dfs(i, product, sign):
            if i == k:
                return 0
            total = 0
            np = product * primes[i]
            if np <= x:
                total += sign * (x // np)
                total += dfs(i + 1, np, -sign)
            total += dfs(i + 1, product, sign)
            return total

        # Inclusion-exclusion gives the number removed from [1, x].
        removed = dfs(0, 1, 1)
        return x - removed

    return phi(x, k - 1) - phi(x // p, k - 1)

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        a, b = map(int, input().split())

        k = 0
        while k < K and primes[k] <= a:
            k += 1

        out.append(str(b - phi(b, k)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The sieve constructs the `31` primes up to `130`. The query itself never needs to know anything about composite divisors because divisibility by a composite number is already implied by divisibility by one of its prime factors.

The `small_phi` table handles every state with `x < 800`. Its recurrence is exactly the same as the mathematical definition, so it is not an approximation or a heuristic. The table simply replaces repeated recursion with a constant-time lookup.

The cached `phi` function handles larger states. The `x < p` check is a useful boundary condition: returning `1` is correct only for positive `x`, while `x = 0` must return `0`. The small-`k` branch uses at most `128` subset choices and is negligible compared with the large recursive part.

The two temporary `products` constructions in the small-`k` branch are unnecessary for the actual computation and can be removed. The following cleaner version is the one that should be submitted:

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

MAX_A = 130
SMALL = 800

def sieve_primes(n):
    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0:2] = b'\x00\x00'
    p = 2
    while p * p <= n:
        if is_prime[p]:
            is_prime[p * p:n + 1:p] = b'\x00' * (
                (n - p * p) // p + 1
            )
        p += 1
    return [i for i in range(2, n + 1) if is_prime[i]]

primes = sieve_primes(MAX_A)
K = len(primes)

small_phi = [[0] * (K + 1) for _ in range(SMALL)]

for x in range(SMALL):
    small_phi[x][0] = x

for k in range(1, K + 1):
    p = primes[k - 1]
    for x in range(SMALL):
        if x < p:
            small_phi[x][k] = 1 if x else 0
        else:
            small_phi[x][k] = (
                small_phi[x][k - 1]
                - small_phi[x // p][k - 1]
            )

@lru_cache(maxsize=250000)
def phi(x, k):
    if x < SMALL:
        return small_phi[x][k]

    if k == 0:
        return x

    p = primes[k - 1]

    if x < p:
        return 1

    if k <= 7:
        def dfs(i, product, sign):
            if i == k:
                return 0

            total = dfs(i + 1, product, sign)

            np = product * primes[i]
            if np <= x:
                total += sign * (x // np)
                total += dfs(i + 1, np, -sign)

            return total

        return x - dfs(0, 1, 1)

    return phi(x, k - 1) - phi(x // p, k - 1)

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, b = map(int, input().split())

        k = 0
        while k < K and primes[k] <= a:
            k += 1

        ans.append(str(b - phi(b, k)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The second code block is the submission version. The prime count is only `31`, so finding `k` by a short loop is insignificant. The cache is deliberately bounded so a large batch of unrelated queries cannot grow memory without limit. A cache hit returns immediately, while the correctness of the algorithm does not depend on a particular cache size.

## Worked Examples

The supplied Codeforces page does not expose sample input and output in its current HTML rendering, while the original UCF statement does provide the example `a = 3, b = 30`. The following traces use that example and a second small query.

For `a = 3, b = 30`, the relevant primes are `2` and `3`.

| Step | `x` | `k` | Prime introduced | `phi(x,k)` |
| --- | --- | --- | --- | --- |
| Start | 30 | 2 | 2, 3 | ? |
| Remove multiples of 3 from `phi(30,1)` | 30 | 2 | 3 | `phi(30,1) - phi(10,1)` |
| Avoid 2 | 30 | 1 | 2 | `15` |
| Avoid 2 among `1..10` | 10 | 1 | 2 | `5` |
| Final | 30 | 2 | 2, 3 | `15 - 5 = 10` |

There are `10` integers from `1` through `30` divisible by neither `2` nor `3`. They are `1, 5, 7, 11, 13, 17, 19, 23, 25, 29`. Subtracting them from `30` gives `20`, which matches the stated example.

For `a = 5, b = 10`, the relevant primes are `2, 3, 5`.

| Step | `x` | `k` | Meaning |
| --- | --- | --- | --- |
| Start | 10 | 3 | Avoid 2, 3, 5 |
| First split | 10 | 2 | `phi(10,2) - phi(2,2)` |
| Avoid 2 and 3 | 10 | 2 | `3`, namely `1, 7, 5` |
| Avoid 2 and 3 in `1..2` | 2 | 2 | `1` |
| Final | 10 | 3 | `3 - 1 = 2` |

The two numbers not divisible by `2`, `3`, or `5` are `1` and `7`. Hence the answer is `10 - 2 = 8`. The valid numbers are `2, 3, 4, 5, 6, 8, 9, 10`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Practical subexponential in the number of relevant primes | There are only 31 recursion levels, small states are table lookups, and repeated states are cached |
| Space | `O(800 * 31 + S)` | The fixed small table uses about 25,000 integers, while `S` is the number of cached large `(x,k)` states |

The key constraint is not `b` itself, since `b` can reach `10^15`. The algorithm never iterates through that range. Its work is determined by the small number of primes below `130` and by the distinct partial-sieve states generated through integer division. The fixed prime bound is what makes the method practical.

The original contest solution takes a different but equivalent inclusion-exclusion route, generating only products of distinct primes that remain below `10^15`; its analysis reports about `23.6` million generated products. The partial-sieve formulation avoids materializing that entire collection and is particularly suitable for Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from functools import lru_cache

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    # Same implementation used by the submission.
    MAX_A = 130
    SMALL = 800

    def sieve_primes(n):
        is_prime = bytearray(b'\x01') * (n + 1)
        is_prime[0:2] = b'\x00\x00'
        p = 2
        while p * p <= n:
            if is_prime[p]:
                is_prime[p * p:n + 1:p] = b'\x00' * (
                    (n - p * p) // p + 1
                )
            p += 1
        return [i for i in range(2, n + 1) if is_prime[i]]

    primes = sieve_primes(MAX_A)
    K = len(primes)

    small_phi = [[0] * (K + 1) for _ in range(SMALL)]

    for x in range(SMALL):
        small_phi[x][0] = x

    for k in range(1, K + 1):
        p = primes[k - 1]
        for x in range(SMALL):
            if x < p:
                small_phi[x][k] = 1 if x else 0
            else:
                small_phi[x][k] = (
                    small_phi[x][k - 1]
                    - small_phi[x // p][k - 1]
                )

    @lru_cache(maxsize=250000)
    def phi(x, k):
        if x < SMALL:
            return small_phi[x][k]

        if k == 0:
            return x

        p = primes[k - 1]

        if x < p:
            return 1

        if k <= 7:
            def dfs(i, product, sign):
                if i == k:
                    return 0

                total = dfs(i + 1, product, sign)

                np = product * primes[i]
                if np <= x:
                    total += sign * (x // np)
                    total += dfs(i + 1, np, -sign)

                return total

            return x - dfs(0, 1, 1)

        return phi(x, k - 1) - phi(x // p, k - 1)

    data = sys.stdin.readline
    t = int(data())
    out = []

    for _ in range(t):
        a, b = map(int, data().split())

        k = 0
        while k < K and primes[k] <= a:
            k += 1

        out.append(str(b - phi(b, k)))

    sys.stdout = old_stdout
    sys.stdin = old_stdin
    return "\n".join(out)

# Provided statement example.
assert solve_io("1\n3 30\n") == "20", "a=3, b=30"

# Minimum b: no positive integer can be a multiple of 2.
assert solve_io("1\n2 1\n") == "0", "minimum b"

# Minimum a and exact boundary.
assert solve_io("1\n2 2\n") == "1", "2 itself is a multiple of 2"

# All numbers except 1 are covered when a >= b.
assert solve_io("1\n130 100\n") == "99", "every integer 2..100 is itself an allowed divisor"

# Composite divisors must not create double counting.
assert solve_io("1\n4 20\n") == "13", "divisibility by 4 adds nothing beyond divisibility by 2"

# Maximum-size query, checked by range and complement properties.
out = solve_io("2\n130 1000000000000000\n130 1000000000000000\n").splitlines()
assert len(out) == 2
assert out[0] == out[1], "identical maximum-size queries must reuse the same exact answer"
assert 0 <= int(out[0]) <= 10**15, "answer must stay inside the queried range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2 1` | `0` | Minimum `b` and empty set of valid multiples |
| `1 / 2 2` | `1` | Exact lower boundary where the divisor equals `b` |
| `1 / 130 100` | `99` | Every value from `2` through `100` is covered |
| `1 / 4 20` | `13` | Composite divisors must not be counted as independent conditions |
| `2 / 130 10^15` repeated | Same value twice | Maximum-size arithmetic and cache reuse |

## Edge Cases

For `a = 2, b = 1`, the algorithm finds one relevant prime, `2`. The complement count is `phi(1,1) = 1`, because `1` is not divisible by `2`. The answer is `1 - 1 = 0`. The boundary is handled before any division by a prime.

For `a = 2, b = 2`, `phi(2,1)` counts only `1`, so the answer is `2 - 1 = 1`. The value `2` itself is included because the definition uses the closed range `1..b`.

For `a = 3, b = 30`, the recursion computes `phi(30,2) = phi(30,1) - phi(10,1) = 15 - 5 = 10`. The ten survivors are the numbers coprime to `6`, and the other twenty numbers are divisible by `2` or `3`. This confirms that the recurrence handles overlap without manually listing intersections.

For `a = 4, b = 20`, the allowed divisors are `2, 3, 4`, but the prime list contains only `2` and `3`. This is deliberate. Every multiple of `4` is already a multiple of `2`, so adding `4` cannot change the union. The algorithm obtains `20 - phi(20,2) = 20 - 7 = 13`.

For `a = 130, b = 100`, every integer from `2` through `100` is itself an allowed divisor. Consequently only `1` is excluded, giving `99`. The algorithm includes all primes through `127`, but the partial-sieve interpretation still produces exactly one surviving integer.

For `a = 130, b = 10^15`, the algorithm never attempts to construct the first `10^15` integers. It recursively divides the bound by primes at most `127`, and once a state falls below `800` it becomes a table lookup. Python's integer arithmetic safely represents every intermediate value involved in the count.
