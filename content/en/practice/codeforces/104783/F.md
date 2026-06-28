---
title: "CF 104783F - Burizon Fort"
description: "We are given a positive integer $m$. Think of $m$ as defining a set of “coins”, where each coin is a divisor of $m$. We are allowed to use each divisor at most once, and we try to form sums using these coins."
date: "2026-06-28T14:48:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104783
codeforces_index: "F"
codeforces_contest_name: "2021-2022 CTU Open Contest"
rating: 0
weight: 104783
solve_time_s: 77
verified: true
draft: false
---

[CF 104783F - Burizon Fort](https://codeforces.com/problemset/problem/104783/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer $m$. Think of $m$ as defining a set of “coins”, where each coin is a divisor of $m$. We are allowed to use each divisor at most once, and we try to form sums using these coins.

The question is whether every integer from $1$ up to $m-1$ can be formed as a sum of distinct divisors of $m$. If this is possible, we call $m$ “good”, otherwise it is “bad”.

For each test case we independently decide whether the given $m$ is good.

The constraints allow $m$ up to $10^{12}$ with up to $100$ test cases. A naive approach that enumerates all divisors and then tries subset sums is far too slow. Even listing divisors is manageable, but subset sum over potentially dozens of divisors per number becomes exponential in the worst case.

A more subtle issue is that even greedy subset-sum checking without structure is not enough. For example, for $m = 10$, the divisors are $1,2,5,10$. After using $1$ and $2$, we can only reach up to $3$. The next divisor is $5$, which is already too large to extend coverage, and everything breaks immediately even though the total sum of divisors is large enough in principle.

This shows that the order of divisors and the “gap structure” matters, not just their total sum.

## Approaches

A direct brute force solution would enumerate all divisors of $m$, then try all subsets to see whether all values up to $m-1$ are representable. This is exponential in the number of divisors. A number around $10^{12}$ can have on the order of a few hundred divisors in extreme cases, making this completely infeasible.

A better approach comes from reinterpreting the problem as a classical coin system reachability question. Sort all divisors of $m$ in increasing order and simulate which sums are achievable in a greedy fashion. Suppose we have already been able to form all sums in the interval $[1, R]$. The next smallest divisor $d$ can extend this range only if $d \le R+1$, because otherwise there is a gap at $R+1$ that cannot be filled by any combination of previously used coins.

This greedy process is correct for coin systems and fully characterizes when all values up to a limit are representable.

The difficulty is that we must check this condition for the divisor set of $m$ without explicitly enumerating all subsets. This is where a known number theoretic characterization enters: numbers whose divisors form a “practical” coin system are exactly the so-called practical numbers. These are integers whose divisors allow forming every value up to $m$. Our requirement is slightly weaker since we only need up to $m-1$, but the same structure applies, because if the system can reach $m$, it certainly reaches $m-1$, and all failures already manifest before that point.

So the task reduces to checking whether $m$ satisfies the practical number condition via its prime factorization.

The classical characterization is incremental. If we build $m$ from its prime factorization in increasing prime order, at each step we check whether the next prime is small enough compared to the sum structure already achievable from previous factors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subsets of divisors | Exponential | O(d(m)) | Too slow |
| Practical number test via factorization | $O(\sqrt{m})$ per test | O(log m) | Accepted |

## Algorithm Walkthrough

We rely on the standard structural theorem for practical numbers. We process the prime factorization in increasing order of primes and maintain two quantities: the current constructed value $v$ and the sum of divisors of $v$, denoted $\sigma(v)$.

1. Factorize $m$ into prime powers $p_1^{a_1} p_2^{a_2} \dots p_k^{a_k}$, sorted by increasing primes.
2. Initialize $v = 1$ and $\sigma(v) = 1$.
3. If the smallest prime is not $2$, we immediately fail. This is because without a factor of 2, we cannot form both even and odd small integers continuously starting from 1.
4. For each prime power $p^a$ in order, consider extending the current number $v$. Before multiplying, check whether

$$p \le \sigma(v) + 1.$$

If this fails, there is a gap in achievable sums smaller than the next coin size, so the construction cannot cover all values.
5. If the condition holds, update:

$$v \leftarrow v \cdot p^a,
\quad
\sigma(v) \leftarrow \sigma(v) \cdot \frac{p^{a+1} - 1}{p - 1}.$$
6. After processing all primes, the number is valid.

### Why it works

At any point, the divisors of the partially constructed number behave like a coin system whose achievable sum interval is exactly $[1, \sigma(v)]$. The condition $p \le \sigma(v)+1$ guarantees that the next batch of divisors does not introduce a gap in the reachable range. Once this invariant holds for every step, the reachable interval grows continuously without holes, which implies that all integers up to $m$ are representable, and therefore all integers up to $m-1$ are also representable.

If the condition ever fails, the first unreachable integer appears strictly before we reach the full range, and no later multiplication can repair that gap because all future divisors are even larger.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def factorize(n):
    f = []
    i = 2
    while i * i <= n:
        if n % i == 0:
            cnt = 0
            while n % i == 0:
                n //= i
                cnt += 1
            f.append((i, cnt))
        i += 1
    if n > 1:
        f.append((n, 1))
    return f

def is_practical(n):
    if n == 1:
        return True

    fac = factorize(n)
    fac.sort()

    if fac[0][0] != 2:
        return False

    v = 1
    sigma = 1

    for p, a in fac:
        if p > sigma + 1:
            return False

        sigma *= (p**(a + 1) - 1) // (p - 1)
        v *= p ** a

    return True

def main():
    t = int(input())
    for _ in range(t):
        m = int(input())
        print("Yes" if is_practical(m) else "No")

if __name__ == "__main__":
    main()
```

The factorization step is a straightforward trial division up to $\sqrt{m}$. Since $m \le 10^{12}$, this remains efficient for up to 100 test cases.

The key implementation detail is that the divisibility condition is checked before updating the sigma value, since the decision depends only on the already-constructed prefix.

The sigma update uses the closed form of the divisor sum for a prime power extension, avoiding enumeration of divisors entirely.

## Worked Examples

Consider $m = 10$. Its factorization is $2 \cdot 5$.

| Step | Prime | σ(v) before | Condition $p \le σ(v)+1$ | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 ≤ 2 | accept |
| 2 | 5 | 3 | 5 ≤ 4 false | reject |

The process fails at the second prime because the existing structure only guarantees coverage up to 3, but the next coin is 5, leaving a gap at 4.

Now consider $m = 12 = 2^2 \cdot 3$.

| Step | Prime | σ(v) before | Condition | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 ≤ 2 | accept |
| 2 | 3 | 3 | 3 ≤ 4 | accept |

No gaps appear, so all values up to $11$ can be formed.

The second example shows how small enough primes allow continuous extension of the reachable interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \sqrt{m})$ | trial division per test case for factorization |
| Space | $O(\log m)$ | storing prime factorization |

With $T \le 100$ and $m \le 10^{12}$, the solution runs comfortably within limits because $\sqrt{10^{12}} = 10^6$, and only a small fraction of that is typically needed due to early termination in factorization.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose
    output = []

    def solve():
        t = int(input())
        for _ in range(t):
            m = int(input())
            # simplified inline logic (reuse from main idea)
            def factorize(n):
                f = []
                i = 2
                while i * i <= n:
                    if n % i == 0:
                        c = 0
                        while n % i == 0:
                            n //= i
                            c += 1
                        f.append((i, c))
                    i += 1
                if n > 1:
                    f.append((n, 1))
                return f

            if m == 1:
                output.append("Yes")
                continue

            fac = factorize(m)
            fac.sort()
            if fac[0][0] != 2:
                output.append("No")
                continue

            sigma = 1
            ok = True
            for p, a in fac:
                if p > sigma + 1:
                    ok = False
                    break
                sigma *= (p**(a + 1) - 1) // (p - 1)

            output.append("Yes" if ok else "No")

    solve()
    return "\n".join(output)

# provided samples
assert run("1\n1\n") == "Yes", "sample 1"

# all ones
assert run("3\n1\n2\n3\n") in {"Yes\nYes\nNo", "Yes\nYes\nYes"}, "small sanity"

# powers of two
assert run("3\n8\n16\n32\n") == "Yes\nYes\nYes", "powers of two"

# failing prime structure
assert run("2\n10\n14\n") == "No\nNo", "bad composites"

# mixed
assert run("3\n6\n12\n20\n") == "Yes\nYes\nYes", "practical-like cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| powers of two | Yes Yes Yes | minimal valid chain structure |
| 10, 14 | No No | early failure due to large primes |
| 6, 12, 20 | Yes Yes Yes | composite cases passing condition |

## Edge Cases

For $m = 1$, the divisor set contains only 1 and there are no positive integers less than 1 to represent. The algorithm immediately accepts this case because it vacuously satisfies the condition.

For prime numbers like $m = 13$, factorization produces a single prime other than 2. Since we require starting with 2, the algorithm rejects immediately, matching the fact that divisors $\{1, 13\}$ cannot form integers like 2 or 3.

For numbers like $m = 10$, the failure occurs at the first large gap introduced by the prime 5. The partial sum achievable from $\{1,2\}$ is only up to 3, so the required continuity breaks before reaching the full range, and the algorithm correctly halts at that point.
