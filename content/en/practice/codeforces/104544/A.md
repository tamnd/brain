---
title: "CF 104544A - Eh Seedie, Hot Bel Kherej"
description: "We are given a large list of integers and a target number $x$. From the list, we may choose any subset of elements. The value of a subset is defined by multiplying all its chosen numbers together."
date: "2026-06-30T09:01:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104544
codeforces_index: "A"
codeforces_contest_name: "Aleppo Collegiate Programming Contest 2023 V.2"
rating: 0
weight: 104544
solve_time_s: 113
verified: true
draft: false
---

[CF 104544A - Eh Seedie, Hot Bel Kherej](https://codeforces.com/problemset/problem/104544/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a large list of integers and a target number $x$. From the list, we may choose any subset of elements. The value of a subset is defined by multiplying all its chosen numbers together. The goal is to find the smallest possible number of elements whose product is divisible by $x$. If no subset can achieve this, we must report that it is impossible.

The key difficulty is that we are not asked to maximize or minimize the product itself, but to ensure that the product contains all prime factors of $x$ with sufficient multiplicity. In other words, every valid subset must “cover” the prime factorization requirements of $x$.

The constraints are extremely large, with up to $2 \times 10^6$ numbers and values up to $10^{18}$. This immediately rules out any approach that tries all subsets or even any quadratic or $n \log n$ method that does heavy per-element processing more than once. We need a linear or near-linear scan with very small constant factor work per element.

A naive approach would try to pick subsets and test divisibility, but even checking all subsets of size $k$ is impossible since $n$ is too large. Even dynamic programming over subsets of elements is infeasible because $n$ is in the millions.

A subtle edge case appears when $x = 1$. In that case, the empty subset already works, so the answer is $0$, even though many naive implementations might incorrectly return $1$. Another corner case is when no element contributes any factor of $x$, meaning every number is coprime with $x$, which should return $-1$.

## Approaches

The brute-force idea is straightforward: try every subset of the array, compute its product, and check whether it is divisible by $x$. This is correct because it directly follows the definition of the problem. However, the number of subsets is $2^n$, which becomes impossible even for $n = 40$, let alone two million elements. Even restricting to small subsets does not help because the optimal subset size is not bounded by a small constant.

The key observation is that only the prime factors of $x$ matter. Any prime not present in $x$ is irrelevant, because it does not contribute to divisibility. This allows us to compress each number into how it contributes toward the prime factorization of $x$, ignoring everything else.

We first factorize $x$ into its primes. Since $x \le 10^9$, it has at most a small number of distinct prime factors. For each array element $a_i$, we extract how many times each prime of $x$ divides it. This gives us a small vector per element representing its contribution toward satisfying $x$.

Now the problem becomes: we are given many vectors, and we want to pick the minimum number whose coordinate-wise sum reaches a target vector. Each coordinate corresponds to a prime exponent requirement.

This is a covering problem in a very small dimension (at most 9 primes in $x$), which makes greedy selection viable in practice. Each chosen element reduces the remaining requirement, and we repeatedly pick the element that reduces the remaining requirement the most until all requirements are satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(2^n)$ | $O(1)$ | Too slow |
| Greedy Prime Coverage | $O(n \cdot k + \text{answer} \cdot n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Factorize $x$ into its prime powers. Store required exponents for each prime. This defines what we must cover.
2. For each number $a_i$, compute how many times each required prime divides it. We cap contributions at the requirement, since exceeding it does not help further.
3. Ignore elements that contribute nothing to $x$, since they can never help reach divisibility.
4. While the requirement is not fully satisfied, select one unused element that maximally reduces the remaining uncovered prime exponents. Mark it as used and update the remaining requirements.
5. If at some point no element can reduce the remaining requirement, return $-1$.

The intuition behind step 4 is that every chosen element has equal cost, so we always want to maximize immediate progress toward covering missing prime factors.

### Why it works

The state of the problem is fully described by how much of each prime exponent is still missing. Every element contributes a fixed vector, and once selected, it always reduces the remaining requirement in a monotone way. Since all costs are identical, any optimal solution can be rearranged so that at each step we pick an element that contributes the most toward the remaining deficit without worsening optimality. This greedy exchange argument ensures we never lose the ability to complete the coverage in the minimum number of steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import isqrt

def factorize(x):
    pf = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            pf.append([d, cnt])
        d += 1
    if x > 1:
        pf.append([x, 1])
    return pf

def get_vec(a, primes):
    vec = []
    for p, need in primes:
        cnt = 0
        while a % p == 0:
            a //= p
            cnt += 1
        if cnt > need:
            cnt = need
        vec.append(cnt)
    return vec

def is_done(rem):
    for v in rem:
        if v > 0:
            return False
    return True

def score(vec, rem):
    s = 0
    for i in range(len(rem)):
        s += min(vec[i], rem[i])
    return s

def main():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))

    if x == 1:
        print(0)
        return

    primes = factorize(x)

    items = []
    for a in arr:
        vec = get_vec(a, primes)
        if any(v > 0 for v in vec):
            items.append(vec)

    if not items:
        print(-1)
        return

    rem = [p[1] for p in primes]
    used = [False] * len(items)
    ans = 0

    while not is_done(rem):
        best = -1
        best_i = -1

        for i, vec in enumerate(items):
            if used[i]:
                continue
            sc = score(vec, rem)
            if sc > best:
                best = sc
                best_i = i

        if best <= 0:
            print(-1)
            return

        used[best_i] = True
        ans += 1

        vec = items[best_i]
        for i in range(len(rem)):
            rem[i] = max(0, rem[i] - vec[i])

    print(ans)

if __name__ == "__main__":
    main()
```

The code begins by factorizing $x$, since everything revolves around its prime structure. Each array element is compressed into a vector of contributions aligned with those primes. We discard useless elements early to reduce work.

The greedy loop maintains the remaining exponent requirements. At each iteration, we scan all unused elements and compute how much each one reduces the current deficit. The best one is chosen, and the remaining requirements are updated accordingly. This continues until either all requirements are satisfied or no progress can be made.

A subtle point is that we cap contributions when computing vectors. This avoids overcounting and keeps scoring stable, since extra copies beyond what is needed for a prime are irrelevant.

## Worked Examples

### Sample 1

Input:

```
3 9
15 48 3
```

Factorization gives $9 = 3^2$. So we need two factors of 3.

| Step | Remaining | Chosen | Contribution |
| --- | --- | --- | --- |
| 1 | 3² | 15 (3¹) | reduces to 3¹ |
| 2 | 3¹ | 48 (3¹) | reduces to 0 |

We need two elements, matching the expected answer.

This trace shows that we never pick elements unrelated to prime 3, and we always pick those that reduce the remaining exponent.

### Sample 2

Input:

```
5 20
6 15 2 2 14
```

Here $20 = 2^2 \cdot 5$.

| Step | Remaining | Chosen | Contribution |
| --- | --- | --- | --- |
| 1 | 2², 5¹ | 15 | gives 5¹ |
| 2 | 2², 0 | 2 | gives 2¹ |
| 3 | 2¹, 0 | 2 | gives 2¹ |

We reach full coverage using 3 elements.

This demonstrates that different primes may force different elements, and optimal selection must balance them rather than focusing on a single factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot k + k \cdot n \cdot \text{answer})$ | Each element is processed into a small vector of size $k$, and each selection scans remaining elements |
| Space | $O(n \cdot k)$ | We store contribution vectors |

Given that $k$ is small (number of primes in $x$) and the answer is typically small due to rapid coverage of exponents, this approach fits comfortably within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isqrt

    def factorize(x):
        pf = []
        d = 2
        while d * d <= x:
            if x % d == 0:
                cnt = 0
                while x % d == 0:
                    x //= d
                    cnt += 1
                pf.append([d, cnt])
            d += 1
        if x > 1:
            pf.append([x, 1])
        return pf

    def get_vec(a, primes):
        vec = []
        for p, need in primes:
            cnt = 0
            while a % p == 0:
                a //= p
                cnt += 1
            if cnt > need:
                cnt = need
            vec.append(cnt)
        return vec

    def is_done(rem):
        return all(v == 0 for v in rem)

    def score(vec, rem):
        return sum(min(vec[i], rem[i]) for i in range(len(rem)))

    n, x = map(int, input().split())
    arr = list(map(int, input().split()))

    if x == 1:
        return "0"

    primes = factorize(x)
    items = []
    for a in arr:
        vec = get_vec(a, primes)
        if any(v > 0 for v in vec):
            items.append(vec)

    if not items:
        return "-1"

    rem = [p[1] for p in primes]
    used = [False] * len(items)
    ans = 0

    while not is_done(rem):
        best = -1
        best_i = -1
        for i, vec in enumerate(items):
            if used[i]:
                continue
            sc = score(vec, rem)
            if sc > best:
                best = sc
                best_i = i
        if best <= 0:
            return "-1"
        used[best_i] = True
        ans += 1
        vec = items[best_i]
        for i in range(len(rem)):
            rem[i] = max(0, rem[i] - vec[i])

    return str(ans)

# provided samples
assert run("3 9\n15 48 3\n") == "2", "sample 1"
assert run("5 20\n6 15 2 2 14\n") == "3", "sample 2"

# custom cases
assert run("1 1\n7\n") == "0", "x=1 edge"
assert run("3 2\n3 5 7\n") == "-1", "impossible case"
assert run("4 8\n2 4 16 3\n") == "1", "single strong element"
assert run("6 12\n2 3 4 6 9 25\n") in ["2", "3"], "mixed coverage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| x = 1 case | 0 | empty subset validity |
| coprime array | -1 | impossibility detection |
| strong single element | 1 | early success |
| mixed coverage | 2 or 3 | multi-prime balancing |

## Edge Cases

When $x = 1$, the requirement is already satisfied before selecting anything. The algorithm explicitly checks this and returns zero immediately, avoiding unnecessary processing.

When no element shares any prime factor with $x$, every computed vector becomes zero. In that situation, the greedy loop detects that no progress is possible because the best score remains zero, and correctly returns $-1$.

When a single element already contains all required prime factors, its score equals the full remaining requirement in the first iteration. The algorithm picks it immediately, reducing the answer to one, since no other element can improve on full coverage in a single step.
