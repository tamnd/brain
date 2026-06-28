---
title: "CF 104767I - Natatorium"
description: "We are given a target surface area $C$, which is guaranteed to be the product of two distinct primes. Alongside this, we are given a list of $M$ available side lengths, where every element in the list is also a prime number."
date: "2026-06-28T20:08:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "I"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 63
verified: true
draft: false
---

[CF 104767I - Natatorium](https://codeforces.com/problemset/problem/104767/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target surface area $C$, which is guaranteed to be the product of two distinct primes. Alongside this, we are given a list of $M$ available side lengths, where every element in the list is also a prime number.

The task is to choose two different primes from this list such that their product equals $C$. Since the pool must be rectangular and not square, we cannot pick the same number twice, and the two chosen primes must be distinct. The output is simply the smaller one first, followed by the larger one.

The constraint $C \le 10^{18}$ implies we cannot factor it using naive trial division up to $C$, but we do not need full factorization in general because the list already restricts candidates. The number of candidates $M \le 2 \cdot 10^5$ suggests that a linear or near-linear scan over the list is acceptable, but anything quadratic over the list would be unnecessary since the structure of the problem allows direct validation of complements.

The key subtlety is that both factors of $C$ are guaranteed to appear in the list, so we do not need to search for arbitrary divisors, only membership queries within the given set.

A naive mistake is to try all pairs from the list and check their product. That would require $O(M^2)$ operations, which at $M = 2 \cdot 10^5$ leads to $4 \cdot 10^{10}$ checks and is completely infeasible.

Another possible failure is iterating over primes and checking divisibility $C \bmod P_i = 0$, then trying to find $C / P_i$ via linear search. Without hashing, this degenerates into $O(M^2)$ again. The correct approach must make membership checks constant time.

## Approaches

The brute-force idea is straightforward: try every pair of primes from the list and check whether their product equals $C$. This is correct because the solution is guaranteed to exist within the list. However, it examines all $\binom{M}{2}$ pairs, which is too slow when $M$ is large.

We can improve this by changing perspective. Instead of choosing two numbers and multiplying them, we can fix one number $p$ and compute what the other must be: $q = C / p$. Since $C$ is guaranteed to be the product of two distinct primes, if $p$ is one of them, then $q$ must also be a prime in the list.

This reduces the problem to a membership test problem: for each $p$, check whether $C$ is divisible by $p$, and if so, check whether $C/p$ exists in the list. Using a hash set makes both operations $O(1)$ on average, turning the full solution into a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Check | $O(M^2)$ | $O(1)$ | Too slow |
| Hash Set Complement Check | $O(M)$ | $O(M)$ | Accepted |

## Algorithm Walkthrough

We rely on the fact that the correct pair is exactly the two prime factors of $C$, and both are guaranteed to be present in the input list.

1. Read $C$, $M$, and the list of primes. We store all primes in a hash set for constant-time lookup. This allows us to quickly check whether a candidate complement exists.
2. Iterate over each prime $p$ in the list. Each $p$ is a potential side length of the pool.
3. Check whether $p$ divides $C$. If it does not, it cannot be part of the correct pair, since both valid factors must multiply exactly to $C$.
4. If $p$ divides $C$, compute $q = C / p$. This is the only possible partner for $p$ in a valid solution.
5. Check whether $q$ exists in the set of allowed primes. If it does, we have found the two required side lengths.
6. Output the pair in sorted order so that the smaller value appears first.

### Why it works

The correctness relies on the structure of $C$. Since $C$ is the product of two distinct primes, it has exactly two prime divisors. Any valid solution must use exactly those two numbers. Therefore, any $p$ from the list that divides $C$ and yields a complementary factor $q$ that also appears in the list must be one of the two correct answers. The hash set ensures we detect membership without ambiguity or repetition, and the distinctness condition is automatically satisfied because the factors are guaranteed distinct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    C = int(input())
    M = int(input())
    arr = list(map(int, input().split()))
    
    s = set(arr)
    
    for p in arr:
        if C % p == 0:
            q = C // p
            if q in s and q != p:
                print(min(p, q), max(p, q))
                return

if __name__ == "__main__":
    solve()
```

The solution begins by placing all available side lengths into a set, enabling constant-time membership checks for complements. We then scan through each candidate $p$. The divisibility check $C \bmod p = 0$ filters out irrelevant primes early, avoiding unnecessary set lookups.

When a valid divisor is found, we compute its complement and verify it exists in the set. The condition $q \ne p$ enforces the requirement that the pool is not a square, although the problem guarantees distinct primes, so this is mainly a safety guard.

We immediately print and terminate once a valid pair is found, since uniqueness of the factorization guarantees no second valid solution exists.

## Worked Examples

### Example 1

Input:

```
15
5
7 2 5 11 3
```

The correct pair is $3$ and $5$.

| Step | p | C % p == 0 | q = C/p | q in set | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | no | - | - | skip |
| 2 | 2 | no | - | - | skip |
| 3 | 5 | yes | 3 | yes | return (3, 5) |

This trace shows that only true factors of $C$ survive the divisibility filter, and the complement check confirms correctness immediately.

### Example 2

Input:

```
21
4
2 3 5 7
```

Here $C = 21 = 3 \cdot 7$.

| Step | p | C % p == 0 | q = C/p | q in set | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | no | - | - | skip |
| 2 | 3 | yes | 7 | yes | return (3, 7) |

The algorithm finds the pair as soon as it reaches one of the valid primes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M)$ | Each element is processed once with constant-time hash operations |
| Space | $O(M)$ | Set stores all candidate primes |

The linear scan is sufficient for $M \le 2 \cdot 10^5$, and memory usage is small since we only store the input list in a hash set.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    C = int(input())
    M = int(input())
    arr = list(map(int, input().split()))
    s = set(arr)

    for p in arr:
        if C % p == 0:
            q = C // p
            if q in s and q != p:
                return f"{min(p,q)} {max(p,q)}\n"

    return ""

# provided sample
assert run("15\n5\n7 2 5 11 3\n") == "3 5\n"

# custom cases
assert run("21\n4\n2 3 5 7\n") == "3 7\n", "basic factor pair"
assert run("77\n5\n11 7 2 3 5\n") == "7 11\n", "unordered pair"
assert run("143\n4\n11 13 17 19\n") == "11 13\n", "larger primes"
assert run("6\n3\n2 3 5\n") == "2 3\n", "smallest valid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 21 case | 3 7 | basic complement logic |
| 77 case | 7 11 | ordering independence |
| 143 case | 11 13 | non-trivial primes |
| 6 case | 2 3 | minimal boundary case |

## Edge Cases

A subtle edge case is when the valid factor pair appears in reverse order in the input list. For example:

Input:

```
21
4
7 2 3 5
```

Here, the algorithm still behaves correctly. It first checks 7, computes $21/7 = 3$, and finds it in the set, so it outputs $3 7$. The ordering constraint is handled at output time using `min` and `max`, so input ordering does not matter.

Another case is when a non-factor prime divides $C$ incorrectly in integer arithmetic due to overflow concerns. In Python this cannot happen, but in fixed-width languages, careful use of 64-bit integers is required since $C$ can be up to $10^{18}$.

A final case is when the input list contains both factors but one appears early and one late. The algorithm may terminate early or late depending on scan order, but correctness is unaffected because any valid encounter immediately yields the unique solution.
