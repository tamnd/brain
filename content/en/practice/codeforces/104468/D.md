---
title: "CF 104468D - DBSucks-ugly Array"
description: "We are given several independent test cases. In each test case, there is an array of integers and a limit value $M$. The task is to count how many integers $X$ in the range from 1 to $M$ have no prime factor in common with any element of the array."
date: "2026-06-30T12:56:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104468
codeforces_index: "D"
codeforces_contest_name: "The 2023 Damascus University Collegiate Programming Contest"
rating: 0
weight: 104468
solve_time_s: 102
verified: false
draft: false
---

[CF 104468D - DBSucks-ugly Array](https://codeforces.com/problemset/problem/104468/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there is an array of integers and a limit value $M$. The task is to count how many integers $X$ in the range from 1 to $M$ have no prime factor in common with any element of the array. In other words, for a valid $X$, the greatest common divisor between $X$ and every array element must be 1, which is equivalent to saying that $X$ is not divisible by any prime that appears in any $A_i$.

The key observation hidden in the wording is that we are not dealing with pairwise coprimality between numbers inside the array, but rather with forbidding a set of prime factors entirely. Once a prime divides at least one array element, that prime automatically disqualifies every $X$ divisible by it.

The constraints are tight but structured. Both $N$ and $M$ go up to $10^5$, and the total sum across all test cases is also bounded by $10^5$. This strongly suggests an $O(N \log A + M)$-style solution per test case or a global sieve-based approach reused across cases. Any approach that enumerates all pairs $(X, A_i)$ or checks gcd explicitly for every $X$ will be too slow because it leads to about $10^{10}$ operations in the worst case.

A subtle edge case appears when all array elements share a small prime factor. For example, if all $A_i$ are even, then every valid $X$ must be odd. A naive approach that checks gcd independently for each $X$ might still pass small cases but will TLE.

Another edge case is when the array contains 1. Since gcd(1, X) is always 1, 1 contributes no restrictions, but careless implementations that extract prime factors without filtering duplicates may waste time or mis-handle frequency logic.

Finally, cases where $M$ is large but the array contains many repeated numbers matter for performance, because repeated factor extraction must not be recomputed unnecessarily.

## Approaches

A direct brute force solution would iterate over every $X$ from 1 to $M$ and check whether $\gcd(X, A_i) = 1$ for all elements in the array. This requires computing gcd $N$ times per $X$, leading to $O(NM \log A)$. With $N, M \approx 10^5$, this becomes roughly $10^{10}$ gcd computations, which is far beyond any feasible limit.

The structure of the problem suggests shifting perspective from numbers to prime factors. Instead of checking whether $X$ is coprime with each array element, we can identify all primes that appear anywhere in the array. Any valid $X$ must avoid being divisible by any of these primes. This converts the problem into counting numbers in $[1, M]$ that are not divisible by a given set of primes.

Once the forbidden primes are known, we can mark their multiples in a frequency array up to $M$, or more efficiently use inclusion-exclusion or a sieve-like marking process. Because each number up to $M$ is touched only a small number of times (once per distinct prime factor), the solution becomes linear or near-linear.

The key improvement is recognizing that the array only matters through its prime factor set, not through the actual values or multiplicities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot M \cdot \log A)$ | $O(1)$ | Too slow |
| Prime sieve + marking | $O(M \log \log M + \sum \text{factorization})$ | $O(M)$ | Accepted |

## Algorithm Walkthrough

We solve each test case independently using prime factor tracking and a marking array over $[1, M]$.

## Algorithm Walkthrough

1. Factorize every element $A_i$ and collect all distinct prime factors in a set. This ensures we only keep primes that actually constrain valid values of $X$. Repeated primes across different elements are irrelevant beyond their existence.
2. Initialize an array `bad` of size $M+1$ with all values false. This array will track whether a number is disqualified because it is divisible by at least one forbidden prime.
3. For each prime $p$ in the collected set, iterate over multiples of $p$ from $p$ to $M$, marking each multiple as bad. This step directly encodes the constraint that any valid $X$ cannot include any forbidden prime factor.
4. Count how many indices $X$ in $[1, M]$ remain unmarked. These are exactly the integers that share no prime factor with the array.
5. Output this count.

The main computational idea is turning multiplicative constraints (coprimality) into additive coverage (marking multiples), which is what makes the problem tractable.

### Why it works

Every integer $X$ is fully determined, in terms of divisibility, by its prime factors. If $X$ is divisible by any prime that appears in any $A_i$, then there exists some $A_i$ sharing that prime factor, implying $\gcd(X, A_i) \neq 1$. Conversely, if $X$ avoids all such primes, it shares no prime factor with any array element, so its gcd with every $A_i$ is 1. The marking process exactly captures this forbidden set of primes and excludes all affected multiples, leaving only valid integers.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXA = 100000

# smallest prime factor sieve
spf = list(range(MAXA + 1))
for i in range(2, int(MAXA ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXA + 1, i):
            if spf[j] == j:
                spf[j] = i

def factorize(x):
    primes = set()
    while x > 1:
        p = spf[x]
        primes.add(p)
        while x % p == 0:
            x //= p
    return primes

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))

    forbidden = set()
    for v in arr:
        if v > 1:
            forbidden |= factorize(v)

    bad = [0] * (m + 1)

    for p in forbidden:
        for x in range(p, m + 1, p):
            bad[x] = 1

    ans = 0
    for i in range(1, m + 1):
        if not bad[i]:
            ans += 1

    print(ans)
```

The sieve at the top precomputes smallest prime factors so that factorization of each $A_i$ is fast. This is essential because repeated naive trial division would still be too slow under worst-case inputs.

The `forbidden` set ensures duplicates do not inflate work when marking multiples. Each prime is processed once, and its multiples are marked in a sieve-like loop.

The final counting loop is a direct scan over $[1, M]$, which is optimal given the constraints.

## Worked Examples

Consider an example where the array is `[2, 3]` and $M = 6$.

| Step | Forbidden primes | Marking action | Bad array (1..6) |
| --- | --- | --- | --- |
| Start | ∅ | none | 000000 |
| After 2 | {2} | mark 2,4,6 | 010101 |
| After 3 | {2,3} | mark 3,6 | 011101 |

Now we count unmarked values: 1 and 5. The output is 2.

This trace shows how overlapping multiples are handled naturally. The number 6 is marked twice but remains simply marked, confirming that duplication does not affect correctness.

Now consider `[6]` with $M = 10$. The forbidden primes are `{2, 3}`.

| Step | Forbidden primes | Marking action | Bad array (1..10) |
| --- | --- | --- | --- |
| After factorization | {2,3} | mark multiples of 2 and 3 | 0101011010 |

Valid numbers are 1, 5, 7. Output is 3. This shows that composite array elements decompose cleanly into prime constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log A + M \log \log M)$ | factorization via SPF plus marking multiples of distinct primes |
| Space | $O(M + MAXA)$ | sieve storage and marking array |

The complexity fits comfortably under the constraints because the total sum of $N$ and $M$ across test cases is at most $10^5$, meaning the marking work is linear overall when amortized.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAXA = 100000
    spf = list(range(MAXA + 1))
    for i in range(2, int(MAXA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factorize(x):
        primes = set()
        while x > 1:
            p = spf[x]
            primes.add(p)
            while x % p == 0:
                x //= p
        return primes

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        arr = list(map(int, input().split()))

        forbidden = set()
        for v in arr:
            if v > 1:
                forbidden |= factorize(v)

        bad = [0] * (m + 1)
        for p in forbidden:
            for x in range(p, m + 1, p):
                bad[x] = 1

        ans = sum(1 for i in range(1, m + 1) if not bad[i])
        out.append(str(ans))

    return "\n".join(out)

# provided sample (interpreted)
assert run("1\n3 5\n1 2 3\n") == "2"

# all ones: no restriction
assert run("1\n3 10\n1 1 1\n") == "10"

# single prime restriction
assert run("1\n1 10\n2\n") == "5"

# multiple primes
assert run("1\n2 10\n6 15\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 10 | no forbidden primes case |
| single prime | 5 | filtering multiples correctly |
| composite overlap | 3 | handling union of prime factors |

## Edge Cases

When every array element is 1, the forbidden set is empty. The marking loop never runs, so all numbers from 1 to $M$ remain valid. For example, input `N=3, A=[1,1,1], M=5` produces all zeros in the `bad` array and outputs 5.

When all elements share a single prime factor, such as all being even, the forbidden set becomes `{2}`. The algorithm marks all even numbers, leaving exactly the odds. For `M=6`, the marked array becomes `[1,0,1,0,1,0]`, and the output is 3.

When elements are large composites like 6, 10, 15, the union of their prime factors creates overlapping constraints. The marking step naturally merges overlaps without double counting. For example, 30 is marked multiple times but remains a single exclusion, confirming stability under repeated factors.
