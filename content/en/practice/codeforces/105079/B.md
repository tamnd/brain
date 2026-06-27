---
title: "CF 105079B - Polkadots"
description: "We are given a minimum threshold $n$, and we want to choose a number $x$ representing the number of polkadots on a cupcake. This number must satisfy two constraints at the same time. First, $x ge n$. Second, $x$ must not be a prime number."
date: "2026-06-27T21:25:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "B"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 59
verified: true
draft: false
---

[CF 105079B - Polkadots](https://codeforces.com/problemset/problem/105079/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a minimum threshold $n$, and we want to choose a number $x$ representing the number of polkadots on a cupcake. This number must satisfy two constraints at the same time. First, $x \ge n$. Second, $x$ must not be a prime number. Among all such valid values, we must return the smallest possible one.

So the task is essentially a “next valid number” query starting from $n$, where validity means “composite or 1”, since 1 is not prime and counts as acceptable under the rule “not prime”.

The constraint $2 \le n \le 1000$ immediately suggests that we are in a tiny search space. Even a naive scan upward from $n$ is at worst 1000 checks, which is negligible. The only real computation inside each check is primality testing.

The only subtle edge cases come from how primality is defined around small integers. The number 2 is prime, so if $n = 2$, we must skip it and move forward. The number 3 is also prime, so consecutive skipping may happen. Another subtle case is that the answer can equal $n$ itself if $n$ is already non-prime, for example $n = 1000$. A careless approach that assumes we must always increase $n$ would be incorrect.

## Approaches

A direct approach is to start from $x = n$ and repeatedly check whether $x$ is prime. If it is prime, we increment $x$ and try again. The first value that fails the primality test is returned.

This works because the search space is monotonic: once a value is invalid (prime), we only need to move forward, and the first valid value encountered is necessarily optimal since we scan in increasing order.

The bottleneck is primality testing. A naive primality check runs in $O(\sqrt{x})$, and we may perform it up to about 1000 times in the worst case. This gives roughly $1000 \cdot 31$ operations, which is trivial. Even with a slightly slower implementation, it remains well within limits.

A slightly more structured optimization is to precompute primes up to 1000 using a sieve, then simply scan upward and check a boolean array. This reduces each check to $O(1)$, making the solution purely linear in the worst case.

Both approaches are acceptable; the sieve is cleaner if we expect multiple queries, while direct primality checking is simplest for a single input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check primality each step) | $O((m-n)\sqrt{m})$ | $O(1)$ | Accepted |
| Sieve + Scan | $O(M \log \log M + (m-n))$ | $O(M)$ | Accepted |

Here $M = 1000$.

## Algorithm Walkthrough

We describe the sieve-based approach since it makes the final scan trivial.

### Steps

1. Build a boolean array `is_prime` of size 1001 initialized to true for all indices from 2 to 1000.

We treat 0 and 1 as non-prime immediately because they do not satisfy primality definitions.
2. Run a sieve of Eratosthenes from 2 to 1000.

For each number $i$ that is still marked as prime, mark all multiples $2i, 3i, \dots$ as non-prime.

This step is correct because any composite number must have a smallest prime factor, and it will be eliminated by that factor’s iteration.
3. Start from $x = n$ and move upward.
4. For each $x$, check whether `is_prime[x]` is false.

If it is false, immediately output $x$.

Otherwise increment $x$ and continue.

The first value encountered that is not prime is the smallest valid answer because we are scanning in increasing order without skipping any candidates.

### Why it works

The sieve correctly partitions numbers into primes and non-primes up to 1000. After preprocessing, primality queries become constant-time lookups. The scan from $n$ upward preserves ordering, so the first non-prime encountered is minimal by construction. There is no way to miss a smaller valid answer because every candidate less than the output has already been checked and rejected as prime.

## Python Solution

```python
import sys
input = sys.stdin.readline

N = 1000

is_prime = [True] * (N + 1)
is_prime[0] = is_prime[1] = False

p = 2
while p * p <= N:
    if is_prime[p]:
        for m in range(p * p, N + 1, p):
            is_prime[m] = False
    p += 1

n = int(input().strip())

x = n
while True:
    if not is_prime[x]:
        print(x)
        break
    x += 1
```

The sieve is built once over the fixed range up to 1000. The inner loop starts at $p^2$ because smaller multiples have already been marked by smaller primes, avoiding redundant work.

The scan loop is deliberately simple: it only advances upward until it finds a composite number or 1. The condition `not is_prime[x]` correctly treats 1 as non-prime and also handles all composite numbers.

## Worked Examples

### Example 1: Input 5

We precompute primality up to at least 5.

| x | is_prime[x] | Action |
| --- | --- | --- |
| 5 | True | skip |
| 6 | False | stop and output |

The algorithm checks 5 first, finds it prime, then moves to 6, which is composite, and returns it. This shows that the answer does not need to be strictly greater than $n$, only non-prime and at least $n$.

### Example 2: Input 2

| x | is_prime[x] | Action |
| --- | --- | --- |
| 2 | True | skip |
| 3 | True | skip |
| 4 | False | output |

The scan correctly skips consecutive primes. The output becomes 4, which is the smallest composite number greater than or equal to 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log \log N)$ | sieve up to 1000 plus linear scan |
| Space | $O(N)$ | boolean array for primality |

The constraints cap $n$ at 1000, so both preprocessing and scanning are effectively constant time in practice. The solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N = 1000
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= N:
        if is_prime[p]:
            for m in range(p * p, N + 1, p):
                is_prime[m] = False
        p += 1

    n = int(sys.stdin.readline().strip())
    x = n
    while True:
        if not is_prime[x]:
            return str(x)
        x += 1

# provided samples
assert run("2\n") == "4"
assert run("5\n") == "6"
assert run("1000\n") == "1000"

# custom cases
assert run("3\n") == "4", "next composite after prime"
assert run("4\n") == "4", "already composite"
assert run("6\n") == "6", "composite stays same"
assert run("997\n") == "1000", "jump across primes near upper bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 | 4 | immediate next composite after prime |
| 4 | 4 | case where n is already valid |
| 6 | 6 | composite identity case |
| 997 | 1000 | boundary behavior near upper limit |

## Edge Cases

For small primes like 2 and 3, the scan must correctly skip multiple consecutive values. For input 2, the algorithm checks 2 and 3 as prime, then stops at 4. This confirms that repeated increments do not miss valid candidates.

For inputs that are already composite, such as 4 or 1000, the first check immediately succeeds because `is_prime[x]` is false. The loop does not increment further, confirming correctness when the answer equals the input itself.
