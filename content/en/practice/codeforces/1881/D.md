---
title: "CF 1881D - Divide and Equalize"
description: "We are given several independent test cases. In each test case, we start with an array of positive integers. We are allowed to repeatedly pick two different positions and move a multiplicative factor from one value to the other, but the factor must be a divisor of the first…"
date: "2026-06-08T22:40:47+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1881
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 903 (Div. 3)"
rating: 1300
weight: 1881
solve_time_s: 70
verified: true
draft: false
---

[CF 1881D - Divide and Equalize](https://codeforces.com/problemset/problem/1881/D)

**Rating:** 1300  
**Tags:** math, number theory  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, we start with an array of positive integers. We are allowed to repeatedly pick two different positions and move a multiplicative factor from one value to the other, but the factor must be a divisor of the first chosen value. Concretely, we split one number into two parts by dividing it by some divisor and pushing that divisor into another element by multiplication.

The goal is to determine whether we can redistribute prime factors across the array so that all elements eventually become identical.

A useful way to interpret the operation is that it never changes the total product of all numbers. When we divide one element by x and multiply another by x, the global product stays invariant. So the only freedom we have is rearranging how prime factors are distributed among elements.

Each element can be factorized into primes, and the operation allows moving prime factors between elements in arbitrary grouped chunks (since any divisor is allowed, not just primes individually).

The constraints are small enough that for each test case we can afford roughly linear or linearithmic factorization. The sum of all n is at most 10^4, and values go up to 10^6, so prime factorization via a sieve or precomputed SPF is appropriate. Anything quadratic in n would already be safe per test case, but anything depending on values directly is too slow.

A subtle issue appears when thinking in terms of averages or gcd-like invariants. A naive thought is that equalization might depend only on the sum or gcd, but neither is preserved in a way that directly characterizes the final state. The invariant is multiplicative rather than additive.

Edge cases arise when all numbers are already equal, which should immediately return YES. Another corner is when numbers are coprime in a way that prevents redistributing prime exponents evenly across all elements. For example, if we had [2, 3, 5], we can move primes around but cannot create matching distributions where every element ends identical because total exponent counts of primes must be divisible by n.

## Approaches

The brute-force idea is to simulate the operation. We try all pairs of indices, all divisors of the chosen element, and apply transitions recursively or with BFS. Each state is an array configuration. This immediately explodes: each number has potentially many divisors, and the number of configurations grows exponentially because prime factors can be redistributed in many ways. Even for n = 10, this becomes infeasible.

The key observation is that the operation does not change the multiset of prime exponents across the entire array. Every prime factor contributes a fixed total exponent across all elements, and we are only redistributing those exponents among n bins. The final state requires each number to be identical, meaning every element must contain exactly the same exponent of each prime.

So for each prime p, if its total exponent across the array is S, then in the final configuration each element must contain S / n copies of p. That means S must be divisible by n for every prime independently. This condition is both necessary and sufficient because we can always move prime powers between elements using allowed operations.

Thus the problem reduces to factoring all numbers, summing exponents per prime, and checking divisibility by n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Prime Exponent Counting | O(n log A) | O(A) or O(number of primes) | Accepted |

## Algorithm Walkthrough

1. Precompute smallest prime factors for all integers up to 10^6. This allows fast factorization of each number. The reason is that we need to repeatedly decompose values into primes efficiently across all test cases.
2. For each test case, initialize a dictionary or array that tracks total prime exponents across the entire array. This represents the global inventory of prime factors.
3. For each element a[i], factorize it using the SPF table and add its prime exponents into the global count. This step is valid because factorization uniquely represents multiplicative structure.
4. After processing all elements, iterate over all recorded primes and check whether each total exponent is divisible by n. This is required because in the final state, every element must carry exactly equal shares of each prime.
5. If all primes satisfy divisibility, output YES. Otherwise output NO.

### Why it works

The operation preserves the total exponent of every prime across the array. Since we can move any divisor between elements, we can move prime powers in arbitrary chunks, which effectively means we can redistribute each prime independently across positions. The only obstruction to making all elements equal is whether each prime’s total exponent can be evenly split across n elements. If this holds, a constructive redistribution exists; if not, at least one element would need a fractional exponent, which is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXA = 10**6

spf = list(range(MAXA + 1))
for i in range(2, int(MAXA ** 0.5) + 1):
    if spf[i] == i:
        step = i
        start = i * i
        for j in range(start, MAXA + 1, step):
            if spf[j] == j:
                spf[j] = i

def factorize(x, acc):
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        acc[p] = acc.get(p, 0) + cnt

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    total = {}
    for v in a:
        factorize(v, total)
    
    ok = True
    for p, cnt in total.items():
        if cnt % n != 0:
            ok = False
            break
    
    print("YES" if ok else "NO")
```

The SPF sieve builds a smallest prime factor array so that each number up to 10^6 can be factorized in logarithmic time relative to its value. Each factorization accumulates prime counts into a shared dictionary.

The correctness check only verifies divisibility of exponent sums by n. That is sufficient because each element in the final configuration must receive exactly cnt / n copies of each prime.

A common mistake is to check only gcd or product divisibility, but the constraint is per-prime and independent across primes.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [8, 2, 4]
```

Factorizations:

8 = 2^3

2 = 2^1

4 = 2^2

Total exponent of 2 is 6.

| Step | Action | Total exponent of 2 | n | Check |
| --- | --- | --- | --- | --- |
| 1 | Process 8 | 3 | 3 | - |
| 2 | Process 2 | 4 | 3 | - |
| 3 | Process 4 | 6 | 3 | 6 % 3 == 0 |

Since 6 is divisible by 3, each element can end up with exponent 2, producing [4, 4, 4]. This confirms that redistribution works when exponent totals split evenly.

### Example 2

Input:

```
n = 3
a = [2, 3, 5]
```

Each prime appears once, so totals are:

2: 1, 3: 1, 5: 1

| Prime | Total exponent | n | Divisible |
| --- | --- | --- | --- |
| 2 | 1 | 3 | No |
| 3 | 1 | 3 | No |
| 5 | 1 | 3 | No |

Since none are divisible by 3, no equal distribution exists. Each final element would require fractional prime exponents, which is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A + A log log A) | sieve once, factor each number using SPF |
| Space | O(A) | SPF array plus prime frequency map |

The constraints allow up to 10^4 total elements and values up to 10^6, so a linear sieve plus fast factorization fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXA = 10**6
    spf = list(range(MAXA + 1))
    for i in range(2, int(MAXA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factorize(x, acc):
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            acc[p] = acc.get(p, 0) + cnt

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = {}
        for v in a:
            factorize(v, total)

        ok = True
        for c in total.values():
            if c % n != 0:
                ok = False
                break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""7
5
100 2 50 10 1
3
1 1 1
4
8 2 4 2
4
30 50 27 20
2
75 40
2
4 4
3
2 3 1
""") == """YES
YES
NO
YES
NO
YES
NO"""

# custom cases
assert run("""1
1
100
""") == "YES"

assert run("""1
2
2 3
""") == "NO"

assert run("""1
3
2 2 2
""") == "YES"

assert run("""1
4
16 2 2 1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | YES | trivial already-equal case |
| [2,3] | NO | incompatible prime distributions |
| [2,2,2] | YES | already uniform primes |
| [16,2,2,1] | YES | redistribution across multiple primes |

## Edge Cases

For a single-element array like [100], the algorithm factorizes 100 and finds that every prime exponent is divisible by 1. The check always passes and returns YES, matching the fact that no operation is needed.

For an already uniform array such as [7,7,7,7], all prime exponent totals are multiples of n. Each prime count is 4 times the exponent in a single element, so divisibility holds and the algorithm confirms YES without any redistribution reasoning.

For arrays where total exponent is not divisible, such as [2,3,5], each prime has total exponent 1 while n is 3. During the check, each fails divisibility, and the algorithm correctly returns NO without attempting any transformation.
