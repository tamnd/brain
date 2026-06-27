---
title: "CF 105114B - Batch GCD"
description: "We are given a list of integers and need to determine whether there exists at least one pair of distinct elements whose greatest common divisor is greater than one."
date: "2026-06-27T19:48:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105114
codeforces_index: "B"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2024"
rating: 0
weight: 105114
solve_time_s: 71
verified: true
draft: false
---

[CF 105114B - Batch GCD](https://codeforces.com/problemset/problem/105114/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and need to determine whether there exists at least one pair of distinct elements whose greatest common divisor is greater than one. In more concrete terms, the task is asking whether any prime number divides at least two different numbers in the list.

The input size is large, with up to one million integers, each as large as ten billion. This immediately rules out any approach that compares pairs directly. A naive pairwise gcd check would require roughly n²/2 comparisons, which becomes about 10¹² operations in the worst case, far beyond what can be executed within time limits.

The magnitude of the values also matters. Each number is up to 10¹⁰, so any factorization strategy must only go up to the square root of that bound, which is 10⁵. That means precomputing primes up to 100000 is sufficient for complete factorization of every input value.

A subtle failure case appears when many numbers are equal to 1 or are pairwise coprime. For example, input like `1 1 1 1` should produce `NO`, because 1 has no prime factors and thus cannot contribute to a gcd greater than 1. A naive approach that mistakenly treats repeated values as automatically valid would incorrectly return `YES` if it only checks equality rather than shared prime factors.

Another edge case is repeated composite numbers. For example, `6 10 15` does not have any pair sharing a prime factor common to all pairs simultaneously, but `6` and `10` share 2, so the correct answer is already `YES`. Any correct solution must detect shared primes across any pair, not just global intersections of full factorizations.

## Approaches

The brute-force method checks every pair of numbers and computes their gcd. This works because gcd computation is efficient, roughly logarithmic in value size. However, with up to one million numbers, the number of pairs is on the order of 5 × 10¹¹, which makes this completely infeasible. Even if each gcd operation were extremely fast, the scale of pair enumeration dominates everything.

The key observation is that a pair has gcd greater than one exactly when they share at least one prime factor. This shifts the problem from pairwise interaction between numbers to tracking occurrences of prime factors globally. Instead of comparing numbers directly, we factor each number and record which primes we have already seen. If a prime appears again in a different number, we immediately know a valid pair exists.

This turns the problem into incremental factorization plus membership checking in a hash set. Each number is decomposed into primes using trial division up to its square root. During factorization, each distinct prime factor is checked against a global set. The first repetition triggers the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log A) | O(1) | Too slow |
| Prime Tracking with Factorization | O(n √A) worst-case | O(#primes) | Accepted |

## Algorithm Walkthrough

1. Precompute all prime numbers up to 100000 using a sieve. This is sufficient because any composite number up to 10¹⁰ must have a prime factor no larger than its square root.
2. Maintain an empty set that stores prime factors that have already appeared in processed numbers. This set represents all primes that have been “claimed” by earlier elements.
3. For each number in the input, factorize it using the precomputed primes. During factorization, extract each distinct prime factor at most once.
4. For every distinct prime factor of the current number, check whether it already exists in the global set. If it does, immediately output `YES` because this prime is shared between at least two numbers.
5. If a prime factor is not yet in the set, insert it and continue processing the rest of the number.
6. If all numbers are processed without detecting a repeated prime factor, output `NO`.

The important idea is that we only care about whether a prime appears in at least two different numbers. Multiplicity inside a single number does not matter, so we ensure each prime is considered once per number.

### Why it works

Every integer greater than one can be uniquely decomposed into prime factors. If two numbers have gcd greater than one, they must share at least one prime factor. Conversely, if a prime factor appears in two different numbers, those numbers automatically have gcd at least that prime. Therefore tracking first occurrences of primes across numbers is both necessary and sufficient for detecting any valid pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    if n <= 1:
        print("NO")
        return

    max_p = 100000

    is_prime = [True] * (max_p + 1)
    is_prime[0] = is_prime[1] = False
    primes = []

    for i in range(2, max_p + 1):
        if is_prime[i]:
            primes.append(i)
            step = i * i
            for j in range(step, max_p + 1, i):
                is_prime[j] = False

    seen = set()

    for x in arr:
        original = x
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                if p in seen:
                    print("YES")
                    return
                seen.add(p)
                while x % p == 0:
                    x //= p
        if x > 1:
            if x in seen:
                print("YES")
                return
            seen.add(x)

    print("NO")

if __name__ == "__main__":
    solve()
```

The sieve builds a list of primes up to 100000, which is enough to factor all input values safely. During processing, each number is reduced by dividing out its prime factors, ensuring that each prime is only considered once per number. The `seen` set stores primes that have already been associated with previous numbers, so a repeat indicates a shared factor.

A common mistake here is forgetting to remove duplicate prime factors inside the same number. Without the inner `while x % p == 0` loop, a number like 12 would incorrectly register prime 2 twice, which could falsely trigger a match.

## Worked Examples

### Example 1

Input:

```
1
2
```

| Step | Current number | Prime factors found | Seen set | Action |
| --- | --- | --- | --- | --- |
| 1 | 2 | {2} | {} | Insert 2 |

No repetition occurs, so output is `NO`.

This confirms that a single element cannot form a valid pair, regardless of its value.

### Example 2

Input:

```
2
1 1
```

| Step | Current number | Prime factors found | Seen set | Action |
| --- | --- | --- | --- | --- |
| 1 | 1 | {} | {} | Nothing |
| 2 | 1 | {} | {} | Nothing |

No primes exist in either number, so no shared factor can ever appear.

The result is `NO`, showing that duplicates of 1 do not create a valid gcd condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n √A) | Each number is factorized by trial division using primes up to its square root |
| Space | O(√A + k) | Prime sieve storage plus set of seen primes |

The constraints allow this because √A is at most 10⁵, and the sieve is manageable. The algorithm avoids any quadratic interaction between numbers, which is essential for n up to one million.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    max_p = 100000

    is_prime = [True] * (max_p + 1)
    is_prime[0] = is_prime[1] = False
    primes = []

    for i in range(2, max_p + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, max_p + 1, i):
                is_prime[j] = False

    seen = set()

    for x in arr:
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                if p in seen:
                    print("YES")
                    return
                seen.add(p)
                while x % p == 0:
                    x //= p
        if x > 1:
            if x in seen:
                print("YES")
                return
            seen.add(x)

    print("NO")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("1\n2\n") == "NO", "sample 1"
assert run("2\n1 1\n") == "NO", "sample 2"
assert run("2\n2 2\n") == "YES", "sample 3"

# custom cases
assert run("3\n2 3 5\n") == "NO", "all primes distinct"
assert run("3\n6 10 15\n") == "YES", "shared prime exists"
assert run("4\n1 1 1 1\n") == "NO", "all ones"
assert run("3\n4 9 25\n") == "NO", "perfect squares distinct primes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 distinct primes | NO | No shared factors |
| 6 10 15 | YES | Cross-number shared prime detection |
| all ones | NO | Handling numbers without primes |
| 4 9 25 | NO | Repeated structure without overlap |

## Edge Cases

One edge case is when all numbers are 1. The algorithm processes each number but never inserts anything into the prime set, so no false positives occur and the output remains `NO`.

Another edge case is repeated composite numbers like `8 8`. The first 8 inserts prime 2 into the set. The second 8 again produces prime 2, which is found in the set, immediately triggering `YES`. This demonstrates correct handling of duplicates across positions, not within a single number.

A final edge case is when numbers are pairwise coprime but large, such as `2, 3, 5, 7, 11`. Each prime is inserted once and never revisited, so the algorithm correctly completes without triggering a match.
