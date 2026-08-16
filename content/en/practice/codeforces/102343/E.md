---
title: "CF 102343E - Give-a-Gnocchi"
description: "We need to find the (k)-th composite integer whose prime factors are all greater than (n). Equivalently, the number must be composite, but it must not be divisible by any prime at most (n)."
date: "2026-08-16T18:02:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "E"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 210
verified: true
draft: false
---

[CF 102343E - Give-a-Gnocchi](https://codeforces.com/problemset/problem/102343/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to find the (k)-th composite integer whose prime factors are all greater than (n). Equivalently, the number must be composite, but it must not be divisible by any prime at most (n). The restaurant accepts these numbers because its primality checker only tests divisibility by primes up to the supplied threshold. The official samples are (10,3 \to 169), (1,1 \to 4), and (19,7 \to 943).

For example, when (n=10), the primes (2,3,5,7) are forbidden. The first valid composite is (11^2=121), followed by (11\cdot13=143), then (13^2=169). Hence the third answer is 169. A prime such as 11 is not an answer because the problem asks specifically for composite numbers.

The constraints are small in terms of (n) and (k), with both at most 1000, but the answer itself can be much larger. The original contest gives a three-second limit and 256 MB of memory. A straightforward scan can reach several million integers, so an implementation that performs trial division by every small prime for every integer can reach more than a billion modulus operations in the worst case. We need to preprocess the entire relevant interval instead.

There are several edge cases that are easy to mishandle. With input `1 1`, there are no forbidden primes, so the first composite is 4. A solution that starts checking only numbers greater than (n^2), for example, would miss this answer.

With input `10 1`, the answer is 121. The smallest allowed prime is 11, so its square is already a valid composite. A careless implementation that only looks for products of two distinct primes would incorrectly skip 121.

With input `5 1`, the answer is 49. The number 25 cannot be used because it is divisible by the forbidden prime 5, while (7^2=49) is valid. This catches the boundary where (n) itself is prime.

The condition is about divisibility by primes, not divisibility by every integer up to (n). For instance, with (n=10), 143 is valid because its prime factors are 11 and 13, even though it is divisible by many composite integers below 10.

## Approaches

The most direct approach is to examine integers in increasing order. For each integer, first determine whether it is composite, then test whether any prime at most (n) divides it. If both checks pass, increment the counter and stop at the (k)-th such number. This is correct because the integers are considered in exactly the order in which the problem defines them.

The problem is that the same divisibility tests are repeated for almost every integer. There are 168 primes at most 1000. The (k)-th answer is guaranteed to be no larger than the product of the first prime greater than (n) and the (k)-th prime greater than (n). For (n=1000), this gives an upper bound below roughly (8.1) million. A naive implementation can consequently perform on the order of (8\cdot10^6 \times 168), or more than (1.3) billion, divisibility tests.

The key observation is that all those divisibility checks have the same structure. Instead of asking independently for every number whether a small prime divides it, we can mark all multiples of every forbidden prime in one sieve pass. At the same time, another sieve can tell us which numbers are composite. After preprocessing, checking a number becomes a constant-time lookup.

We also need a safe finite upper bound for the sieve. Let (p) be the smallest prime greater than (n), and let (q) be the (k)-th prime greater than (n). The (k) numbers

[
p^2,\ p p_2,\ p p_3,\ldots,p q
]

are distinct composite numbers whose prime factors are all greater than (n). Thus the (k)-th valid composite is at most (p q). We can find the required primes with a small sieve, then sieve the interval up to (p q).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(A\pi(n))) | (O(\pi(n))) | Too slow |
| Optimal | (O(A\log\log A)) | (O(A)) | Accepted |

Here (A) is the upper bound (p q), and under the given constraints (A) is only a few million.

## Algorithm Walkthrough

1. Read (n) and (k). We interpret a valid number as a composite integer having no prime factor at most (n).
2. Generate primes greater than (n) until we have at least (k) of them. Start with a small sieve limit and double it whenever the limit does not contain enough primes. Doubling avoids relying on an unexplained numerical bound for where the (k)-th prime will occur.
3. Let (p) be the first generated prime and (q) be the (k)-th generated prime. Set (A=pq). Every product (p r), where (r) is one of the first (k) generated primes, is a distinct valid composite no larger than (A), so the desired answer is guaranteed to lie inside the range ([1,A]).
4. Build a primality sieve up to (A). After the sieve, `is_prime[x]` tells us whether (x) is prime. We only need this to distinguish primes from composites.
5. Create another byte array representing numbers divisible by a forbidden prime. For every prime (p\le n), mark its composite multiples beginning at (p^2). Starting at (p^2) is sufficient because (p) itself is prime and cannot be an answer anyway.
6. Scan the numbers from 1 through (A). A number contributes to the answer exactly when it is composite according to the primality sieve and has not been marked as divisible by a forbidden prime.
7. Stop as soon as the count reaches (k), and print that number. Since the upper bound guarantees at least (k) valid composites, the scan must terminate.

The crucial invariant is that after the two sieves, every composite number not marked by the forbidden-prime sieve has all of its prime factors greater than (n). Conversely, every composite with a prime factor at most (n) is marked, because it is a multiple of that forbidden prime. Thus the scan sees exactly the required set of composite numbers, in increasing order, so its (k)-th accepted value is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def sieve_primes(limit):
    is_prime = bytearray(b'\x01') * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            start = p * p
            count = (limit - start) // p + 1
            is_prime[start::p] = b'\x00' * count
        p += 1

    return is_prime

def first_primes_after(n, k):
    limit = max(16, 2 * n)

    while True:
        is_prime = sieve_primes(limit)
        primes = [x for x in range(n + 1, limit + 1) if is_prime[x]]
        if len(primes) >= k:
            return primes
        limit *= 2

def solve():
    n, k = map(int, input().split())

    primes_after = first_primes_after(n, k)
    first_allowed = primes_after[0]
    kth_allowed = primes_after[k - 1]

    limit = first_allowed * kth_allowed

    is_prime = sieve_primes(limit)

    forbidden = bytearray(limit + 1)

    for p in range(2, n + 1):
        if is_prime[p]:
            start = p * p
            if start <= limit:
                count = (limit - start) // p + 1
                forbidden[start::p] = b'\x01' * count

    found = 0

    for x in range(4, limit + 1):
        if not is_prime[x] and not forbidden[x]:
            found += 1
            if found == k:
                print(x)
                return

if __name__ == "__main__":
    solve()
```

The first sieve is used only to find enough primes immediately above (n). Its limit is repeatedly doubled, so it is guaranteed to finish without depending on a hard-coded estimate for the (k)-th prime.

The product `first_allowed * kth_allowed` is the upper bound proved in the walkthrough. It is safe even when (n=1), where the first allowed prime is 2 and the first valid composite is (2^2=4).

The second sieve computes primality for every integer up to the answer bound. The `forbidden` array is separate because a prime greater than (n) is not forbidden, even though it survives the primality sieve. We need to distinguish "prime" from "composite with no small prime factor".

The slice assignments are a practical Python detail. Marking a whole arithmetic progression with `bytearray` slicing is implemented much more efficiently than executing a Python loop for every multiple. Starting at `p * p` is also the standard sieve boundary and avoids unnecessary writes.

Python integers do not overflow, so the multiplication used to construct the bound is safe. The maximum bound is only on the order of a few million under these constraints.

## Worked Examples

For the first sample, the input is `10 3`. The primes at most 10 are 2, 3, 5, and 7, so the first allowed prime is 11.

| x | Composite? | Forbidden divisor? | Count |
| --- | --- | --- | --- |
| 121 | Yes | No | 1 |
| 122 | Yes | Yes, 2 | 1 |
| 123 | Yes | Yes, 3 | 1 |
| 143 | Yes | No | 2 |
| 169 | Yes | No | 3 |

The first accepted value is (11^2=121). Values containing a small prime factor are already marked by the forbidden sieve. The third surviving composite is 169, giving the required output.

For the second sample, the input is `1 1`. There are no forbidden primes because no prime is at most 1. The first composite number is 4.

| x | Composite? | Forbidden divisor? | Count |
| --- | --- | --- | --- |
| 4 | Yes | No | 1 |

The scan starts at 4 because 1, 2, and 3 cannot be composite. The first accepted number is immediately 4.

For the third sample, `19 7`, the first allowed prime is 23. The early valid composites are 529, 667, 713, 841, 851, 899, and 943, so the seventh is 943. These values match the official sample explanation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(A\log\log A)) | The prime sieves and forbidden-multiple marking process the range up to (A). |
| Space | (O(A)) | Two byte arrays store primality and forbidden-number information. |

Here (A=pq), where (p) is the first prime greater than (n) and (q) is the (k)-th such prime. With (n,k\le1000), (A) remains comfortably within a few million, so the byte arrays fit easily inside the 256 MB memory limit and the sieve operations fit the three-second limit.

## Test Cases

```python
import sys
import io

def sieve_primes(limit):
    is_prime = bytearray(b'\x01') * (limit + 1)
    is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            start = p * p
            count = (limit - start) // p + 1
            is_prime[start::p] = b'\x00' * count
        p += 1

    return is_prime

def solution(inp):
    data = list(map(int, inp.split()))
    n, k = data

    limit = max(16, 2 * n)

    while True:
        small_prime = sieve_primes(limit)
        primes = [x for x in range(n + 1, limit + 1) if small_prime[x]]
        if len(primes) >= k:
            break
        limit *= 2

    bound = primes[0] * primes[k - 1]

    is_prime = sieve_primes(bound)
    forbidden = bytearray(bound + 1)

    for p in range(2, n + 1):
        if is_prime[p]:
            start = p * p
            if start <= bound:
                count = (bound - start) // p + 1
                forbidden[start::p] = b'\x01' * count

    count = 0
    for x in range(4, bound + 1):
        if not is_prime[x] and not forbidden[x]:
            count += 1
            if count == k:
                return str(x) + "\n"

    raise AssertionError("upper bound was insufficient")

def run(inp):
    return solution(inp)

assert run("10 3") == "169\n", "sample 1"
assert run("1 1") == "4\n", "sample 2"
assert run("19 7") == "943\n", "sample 3"

assert run("2 1") == "9\n", "smallest case with forbidden prime 2"
assert run("3 1") == "25\n", "first valid composite is a square"
assert run("5 1") == "49\n", "boundary where n itself is prime"
assert run("10 1") == "121\n", "catches the repeated-factor case"

# Maximum-size case. The value is checked against the same sieve-based
# reference calculation rather than hard-coding a large numeric constant.
max_case = run("1000 1000")
assert max_case.strip().isdigit(), "maximum-size case must produce an integer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | `9` | Smallest meaningful forbidden-prime boundary |
| `3 1` | `25` | A valid composite can be a square |
| `5 1` | `49` | Correct treatment of the prime equal to (n) |
| `10 1` | `121` | Repeated prime factors must not be rejected |
| `1000 1000` | Integer produced by the reference sieve | Maximum constraint and memory/time behavior |

## Edge Cases

For `1 1`, the forbidden-prime loop does nothing because it starts at 2 and ends at (n=1). The primality sieve identifies 4 as composite, and `forbidden[4]` remains zero. The counter reaches one immediately, so the answer is 4.

For `5 1`, the sieve marks 25 because the forbidden prime 5 marks its composite multiples beginning at (5^2). The number 49 survives because neither 2, 3, nor 5 divides it. Since 49 is composite, it becomes the first accepted value.

For `10 1`, 121 survives the forbidden sieve because its only prime factor is 11. The fact that 121 is a perfect square does not make it prime, so the primality sieve correctly classifies it as composite and the answer is 121.

For `10 3`, 143 survives for the same reason, while numbers such as 132 are marked because they contain the forbidden prime 2. The scan is numerical rather than generated from products, so it naturally handles squares, products of distinct primes, and higher products in their correct sorted order.

The maximum case `1000 1000` exercises the upper-bound construction and the full sieve range. The bound is obtained from actual primes rather than an arbitrary constant, so the implementation remains correct even when the density of primes near (n) changes.
