---
title: "CF 103492D - Primality Test"
description: "We are given a positive integer x, and we construct a value using primes around it. First, we define f(x) as the smallest prime strictly greater than x, so it is the next prime after x."
date: "2026-07-03T06:12:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103492
codeforces_index: "D"
codeforces_contest_name: "China Collegiate Programming Contest 2021, Qualification Round (Online), Rematch"
rating: 0
weight: 103492
solve_time_s: 42
verified: true
draft: false
---

[CF 103492D - Primality Test](https://codeforces.com/problemset/problem/103492/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer x, and we construct a value using primes around it. First, we define f(x) as the smallest prime strictly greater than x, so it is the next prime after x. We then apply the same idea again to f(x), giving f(f(x)), which is simply the prime after the next prime.

From these two primes, we form a number g(x) by taking their average, meaning we add them and divide by 2. The task is to decide whether this resulting number g(x) is itself a prime.

The input consists of up to 100,000 independent queries, and each x can be as large as 10^18. This immediately rules out any approach that tries to test primality or search for primes around x for each query separately. Any solution must avoid actually computing large primes per test case.

A subtle edge case appears at very small values. For x = 1, the next primes are 2 and 3, so g(x) becomes 2, which is prime. For x = 2, the next primes are 3 and 5, so g(x) becomes 4, which is not prime. These tiny inputs already suggest that the answer may depend only on the structure of the first few primes rather than on the magnitude of x.

The main difficulty is that x can be extremely large, so any reasoning must depend on properties of consecutive primes rather than their explicit values.

## Approaches

The most direct way to evaluate g(x) is to compute f(x) by searching upward until a prime is found, then compute f(f(x)) the same way, and finally check whether their average is prime. This is correct by definition, but it immediately runs into computational limits. For x up to 10^18, finding the next prime requires heavy primality testing and potentially scanning large gaps, and doing this for 100,000 queries becomes infeasible.

The key observation is that we do not actually care about the numeric value of the primes, only about their structural relationship. Let p1 = f(x) and p2 = f(f(x)). These are consecutive primes. The value g(x) is simply the midpoint between two consecutive primes.

Now we ask a simpler structural question: can the midpoint of two consecutive primes ever itself be prime? If such a midpoint m were prime, then we would have p1 < m < p2, meaning there exists a prime strictly between two consecutive primes. This contradicts the definition of consecutiveness unless the interval is extremely small. The only exception occurs at the very beginning of the prime sequence, where the consecutive primes 2 and 3 have midpoint 2.

So the entire problem collapses to checking whether the pair of consecutive primes is (2, 3), which happens only when x is small enough that the next prime is 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Prime Search | O(T · sqrt(N) or worse) | O(1) | Too slow |
| Structural Observation | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each x, determine whether the next prime after x is 2. This happens only when x = 1, since 2 is the smallest prime and no positive integer smaller than 2 has a different next prime.
2. If x = 1, we immediately identify the consecutive primes as 2 and 3, so the midpoint is 2, which is prime.
3. For any x ≥ 2, the next prime f(x) is at least 3, and the next one f(f(x)) is at least 5, forming consecutive odd primes.
4. The midpoint of any two consecutive odd primes greater than (2, 3) cannot be prime because it lies strictly between two consecutive primes, which is impossible unless it equals one of them.
5. Output YES only for x = 1, otherwise output NO.

### Why it works

Let p1 = f(x) and p2 = f(f(x)). These are consecutive primes. Suppose g(x) = (p1 + p2) / 2 is prime. Then g(x) lies strictly between p1 and p2. That would imply a prime exists between two consecutive primes, contradicting their definition. The only case where this reasoning breaks is when the interval starts at 2 and 3, where the midpoint coincides with one endpoint behaviorally due to the smallest possible gap. Thus only x = 1 survives.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        x = int(input())
        if x == 1:
            out.append("YES")
        else:
            out.append("NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation reflects the collapse of the entire prime reasoning into a single structural condition. The function f(x) and the second prime f(f(x)) are never explicitly computed, because their only relevant property is that they form consecutive primes. The decision reduces to checking whether we are in the unique case where those primes are (2, 3), which corresponds exactly to x = 1.

No edge handling is required beyond this condition, since all x ≥ 2 produce the same structural outcome.

## Worked Examples

### Example 1: x = 1

| Step | f(x) | f(f(x)) | g(x) |
| --- | --- | --- | --- |
| 1 | 2 | 3 | (2 + 3) / 2 = 2 |

The midpoint equals 2, which is prime, so the output is YES. This is the only configuration where the consecutive primes are (2, 3), allowing the midpoint to be prime.

### Example 2: x = 2

| Step | f(x) | f(f(x)) | g(x) |
| --- | --- | --- | --- |
| 1 | 3 | 5 | (3 + 5) / 2 = 4 |

The result is 4, which is composite, so the output is NO. This reflects the fact that once primes start from 3 onward, the midpoint between consecutive primes cannot be prime.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each query is a single comparison |
| Space | O(1) | Only a constant amount of storage is used |

The solution easily fits within constraints since it performs constant work per test case even when T reaches 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    input = _sys.stdin.readline
    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            x = int(input())
            out.append("YES" if x == 1 else "NO")
        print("\n".join(out))

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return res

# provided samples (interpreted)
assert run("2\n1\n2\n") == "YES\nNO"

# minimum input
assert run("1\n1\n") == "YES"

# small non-trivial
assert run("1\n3\n") == "NO"

# large value
assert run("1\n1000000000000000000\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 → 1 | YES | smallest valid case |
| 1 → 2 | NO | immediate rejection case |
| 1 → large | NO | correctness for upper bound |

## Edge Cases

The only meaningful edge case is when x = 1, where the prime chain begins with 2 and 3. For x = 1, the algorithm directly outputs YES, matching the computed midpoint (2 + 3) / 2 = 2.

For x ≥ 2, the execution always falls into the NO branch. For example, with x = 2, f(x) = 3 and f(f(x)) = 5, giving midpoint 4, which is correctly rejected.

No further boundary issues arise because the decision does not depend on arithmetic properties of large primes, only on the identity of the smallest possible prime configuration.
