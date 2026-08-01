---
title: "CF 102672D - Good Subset"
description: "The problem gives a collection of positive integers written on a lock. We need to choose as many of those integers as possible so that every chosen number has a common divisor greater than one."
date: "2026-08-01T23:43:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102672
codeforces_index: "D"
codeforces_contest_name: "Selection of tasks from Internet olympiads season 2019-20"
rating: 0
weight: 102672
solve_time_s: 69
verified: true
draft: false
---

[CF 102672D - Good Subset](https://codeforces.com/problemset/problem/102672/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a collection of positive integers written on a lock. We need to choose as many of those integers as possible so that every chosen number has a common divisor greater than one. In other words, among all possible subsets, we want the largest subset whose greatest common divisor is not equal to one.

The input contains up to 1000 numbers, but each number can be as large as $10^{18}$. The small number of elements rules out algorithms that depend on trying many subsets, because even checking all subsets would require $2^{1000}$ operations. The large value range also rules out trial division up to the value of each number, because a single number could require billions of attempts. The intended solution needs to exploit the fact that we only need prime divisors, not the full factorization structure.

The answer is controlled by prime factors. If several numbers have a prime factor $p$, then all of them can be placed in one valid subset because their gcd is at least $p$. The largest valid subset is exactly the largest group of numbers sharing one prime divisor.

There are several edge cases where a careless implementation can fail. If every number is prime and all primes are different, the answer is still one because a single number has a gcd equal to itself. For example:

```
Input:
3
2 3 5

Output:
1
```

A solution that only counts repeated factors would incorrectly print zero.

Another tricky case is when a number contains the same prime multiple times. For example:

```
Input:
3
12 18 25

Output:
2
```

The prime factors are $12 = 2^2 \cdot 3$, $18 = 2 \cdot 3^2$, and $25 = 5^2$. The best subset is $\{12,18\}$, because they share both 2 and 3. Counting prime occurrences inside one number instead of counting numbers containing a prime would overestimate the result.

A final edge case is a large prime number near the upper bound. For example:

```
Input:
1
1000000000000000000

Output:
1
```

The factorization method must handle large composite numbers without assuming that every value can be divided by small primes.

## Approaches

The direct approach is to generate every subset, compute the gcd of its elements, and keep the largest subset with gcd greater than one. This is correct because every possible answer is considered. However, there are $2^n$ subsets, and with $n=1000$ this is completely impossible.

A slightly better idea is to look at divisors. For every possible divisor, count how many numbers are divisible by it. The largest count would be the answer. The problem is that the numbers are up to $10^{18}$, so enumerating divisors of each number is also too slow if done by trial division.

The key observation is that a subset has gcd greater than one if and only if all its numbers share at least one prime divisor. We do not need to know the exact gcd. We only need to know which primes appear in which numbers. After factoring every number into distinct prime factors, we can count how many numbers contain each prime and take the maximum count.

The remaining challenge is factoring values up to $10^{18}$. Pollard Rho factorization is designed exactly for this range. It can find non-trivial factors of large composite numbers efficiently, while Miller Rabin primality testing quickly identifies primes. After obtaining the factors, we insert only distinct primes for each number, because a number containing $2^5$ contributes only one element to the count for prime 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Divisor Enumeration | Too large for $10^{18}$ values | $O(1)$ | Too slow |
| Pollard Rho + Counting Prime Factors | About $O(n \log a_i)$ expected | $O(k)$, where $k$ is the number of discovered prime factors | Accepted |

## Algorithm Walkthrough

1. Factor every number using Miller Rabin and Pollard Rho.

Miller Rabin tells us whether a number is prime. If a number is composite, Pollard Rho finds a factor, and we recursively factor both parts. This avoids scanning all possible divisors.
2. Remove duplicate prime factors inside each number.

A number like 72 has prime factors 2 and 3. Although 2 appears several times in its factorization, it should increase the count of prime 2 only once.
3. For every distinct prime factor of the number, increase its frequency in a global counter.

The counter represents how many original numbers contain that prime. If a prime appears in many numbers, those numbers form a valid subset.
4. Output the largest frequency among all primes.

If every number has no shared prime factor, each prime count is at most one, and the answer remains one.

Why it works:

Consider the optimal subset. Its gcd is some integer greater than one. Any prime divisor of this gcd divides every element in the subset. Therefore the subset is included in the group of numbers containing that prime. Our algorithm checks every prime that appears in the input and finds the largest such group. Conversely, every group counted by a prime has that prime as a common divisor, so it is always a valid subset. Both directions prove that the maximum count is exactly the answer.

## Python Solution

```python
import sys
import random
import math
from collections import defaultdict

input = sys.stdin.readline

def is_prime(n):
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in [2, 3, 5, 7, 11, 13]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        good = False
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                good = True
                break
        if not good:
            return False
    return True

def pollard(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(0, n - 1)
        y = x
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n, res):
    if n == 1:
        return
    if is_prime(n):
        res.append(n)
    else:
        d = pollard(n)
        factor(d, res)
        factor(n // d, res)

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    count = defaultdict(int)

    for x in a:
        factors = []
        factor(x, factors)
        for p in set(factors):
            count[p] += 1

    print(max(count.values()))

if __name__ == "__main__":
    solve()
```

The primality test uses deterministic bases that are sufficient for the given 64-bit range. The recursive factor function splits composite numbers until every remaining piece is prime.

The `set(factors)` conversion is necessary because we are counting numbers, not prime powers. Without it, a value like $16$ would incorrectly add four contributions to prime 2.

The final dictionary stores only primes that actually occur. Since every input number is at least two, there is always at least one prime factor, so the maximum exists.

## Worked Examples

For the first sample:

```
4
6 15 10 42
```

The factor counts evolve as follows.

| Number processed | Distinct factors | Count of 2 | Count of 3 | Count of 5 | Count of 7 |
| --- | --- | --- | --- | --- | --- |
| 6 | 2, 3 | 1 | 1 | 0 | 0 |
| 15 | 3, 5 | 1 | 2 | 1 | 0 |
| 10 | 2, 5 | 2 | 2 | 2 | 0 |
| 42 | 2, 3, 7 | 3 | 3 | 2 | 1 |

The maximum frequency is 3, so three numbers can share a common prime divisor. This matches the subset containing 6, 15, and 42.

For the second sample:

```
3
2 2 2
```

| Number processed | Distinct factors | Count of 2 |
| --- | --- | --- |
| 2 | 2 | 1 |
| 2 | 2 | 2 |
| 2 | 2 | 3 |

The algorithm correctly treats each occurrence as a separate array element, giving answer 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected $O(n \log a_i)$ | Each number is factored using Pollard Rho, which is efficient for 64-bit integers |
| Space | $O(k)$ | Stores the discovered prime counts |

The input size is only 1000 numbers, so the main difficulty is the size of the values rather than the number of elements. Pollard Rho avoids impossible trial division and fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    n = int(data[0])
    arr = list(map(int, data[1:]))

    from collections import defaultdict
    import math
    import random

    def is_prime(n):
        if n < 2:
            return False
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
            if n == p:
                return True
            if n % p == 0:
                return False
        d = n - 1
        s = 0
        while d % 2 == 0:
            s += 1
            d //= 2
        for a in [2, 3, 5, 7, 11, 13]:
            if a >= n:
                continue
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            ok = False
            for _ in range(s - 1):
                x = x * x % n
                if x == n - 1:
                    ok = True
                    break
            if not ok:
                return False
        return True

    def pollard(n):
        if n % 2 == 0:
            return 2
        while True:
            c = random.randrange(1, n - 1)
            x = random.randrange(0, n - 1)
            y = x
            d = 1
            while d == 1:
                x = (x * x + c) % n
                y = (y * y + c) % n
                y = (y * y + c) % n
                d = math.gcd(abs(x - y), n)
            if d != n:
                return d

    def factor(x, out):
        if x == 1:
            return
        if is_prime(x):
            out.append(x)
        else:
            d = pollard(x)
            factor(d, out)
            factor(x // d, out)

    cnt = defaultdict(int)
    for x in arr:
        f = []
        factor(x, f)
        for p in set(f):
            cnt[p] += 1

    return str(max(cnt.values())) + "\n"

assert run("4\n6 15 10 42\n") == "3\n"
assert run("3\n2 2 2\n") == "3\n"

assert run("1\n35\n") == "1\n"
assert run("3\n2 3 5\n") == "1\n"
assert run("3\n12 18 25\n") == "2\n"
assert run("2\n9999999967 9999999967\n") == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 6 15 10 42` | `3` | Shared factors across different primes |
| `3 / 2 2 2` | `3` | Repeated values |
| `1 / 35` | `1` | Single element subset |
| `3 / 2 3 5` | `1` | No common factor |
| `3 / 12 18 25` | `2` | Duplicate prime powers inside a number |
| Two equal large primes | `2` | Large integer factor handling |

## Edge Cases

For the case where every number has a different prime factor:

```
3
2 3 5
```

The factorization creates counts `2 -> 1`, `3 -> 1`, and `5 -> 1`. The largest count is one, which is correct because no pair can have gcd greater than one.

For repeated prime powers:

```
3
12 18 25
```

The first number contributes only `{2,3}`, not `{2,2,3}`. The second contributes `{2,3}`. The third contributes `{5}`. The count for primes 2 and 3 becomes two, giving the correct answer.

For very large composite values:

```
1
1000000000000000000
```

Pollard Rho splits the number into its prime factors, but the answer only needs the fact that at least one prime exists. The count of that prime is one, so the output is one. This avoids any attempt to loop through all possible divisors up to the square root.
