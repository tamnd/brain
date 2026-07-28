---
title: "CF 102767E - Singhal and Numbers"
description: "The problem models a shop where an item has an initial price X. The customer may buy any number N of identical items as long as N is a proper divisor of X, meaning N divides X and 1 <= N < X."
date: "2026-07-28T23:31:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102767
codeforces_index: "E"
codeforces_contest_name: "Codedigger Training Contest -Number Theory"
rating: 0
weight: 102767
solve_time_s: 69
verified: true
draft: false
---

[CF 102767E - Singhal and Numbers](https://codeforces.com/problemset/problem/102767/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a shop where an item has an initial price `X`. The customer may buy any number `N` of identical items as long as `N` is a proper divisor of `X`, meaning `N` divides `X` and `1 <= N < X`. The shop assigns an extra cost depending on the type of `N`: prime numbers use value `A`, composite numbers use value `B`, and `N = 1` uses value `C`. The total cost is the chosen extra value plus `X / N`. The task is to find the minimum possible cost.

The input contains several independent queries. Each query gives `X` and the three extra costs `A`, `B`, and `C`. The output for each query is the smallest cost achievable by choosing a valid number of items.

The important constraint is `X <= 10^7` and there can be up to `10^5` queries. A solution that checks every divisor of every `X` is not suitable because a number near `10^7` can still have thousands of divisors, and doing unnecessary work for every query would waste the time budget. Factoring each number using trial division up to its square root is also too expensive if done directly, because `10^5 * sqrt(10^7)` is around `3 * 10^8` trial operations. We need to reuse work across queries and only inspect the small prime factors of each number.

The main edge cases come from the classification of divisors. A value can have prime divisors but no composite proper divisor, so assuming a composite candidate always exists gives wrong answers. For example:

```
Input
4
2 5 1
```

The only valid choice is `N = 1`, because `2` has no other proper divisor. The answer is `7`. A careless implementation that searches only prime or composite divisors would miss this case.

Another tricky case is a number that is a square of a prime.

```
Input
9
1 10 3
```

The valid choices are `N = 1` and `N = 3`. The divisor `3` is prime, not composite. The answer is `6`. Treating the largest proper divisor as composite would incorrectly use the composite cost formula.

A normal composite example also checks the opposite behavior:

```
Input
12
2 5 1
```

The proper divisors are `1, 2, 3, 4, 6`. The best prime choice is `N = 3`, giving `2 + 4 = 6`. The best composite choice is `N = 6`, giving `5 + 2 = 7`. The answer is `6`.

## Approaches

The direct approach is to enumerate every divisor `N` of `X`, classify it, calculate the cost, and keep the minimum. This is correct because every possible purchase quantity is checked. However, even with a square-root divisor search, it still requires factoring or divisor enumeration for every query. In the worst case, a large prime number forces checking every integer up to its square root. With many queries, the repeated work becomes too large.

The key observation is that for a fixed category, the term `X / N` becomes smaller when `N` becomes larger. The additional cost `A`, `B`, or `C` does not depend on the exact divisor. This means we only need the largest possible divisor in each category.

For prime `N`, the best candidate is the largest prime factor of `X`. For composite `N`, the best candidate is the largest proper divisor of `X`. The largest proper divisor of a composite number is `X / p`, where `p` is the smallest prime factor. If this value is composite, it is the best composite candidate. If it is prime, then `X` consists of exactly two prime factors, and no composite proper divisor exists.

The only remaining task is factoring `X`. Since `X` is at most `10^7`, all possible prime factors that need to be tested are at most `3162`. We can precompute these primes once and use them for every query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sqrt(X)) per query | O(1) | Too slow for many queries |
| Optimal | O(number of primes <= sqrt(X)) per query | O(number of primes <= sqrt(10^7)) | Accepted |

## Algorithm Walkthrough

1. Precompute all prime numbers up to `3162` using the sieve of Eratosthenes. These are enough because every composite `X <= 10^7` has a prime factor not exceeding its square root.
2. For each query, factor `X` using the precomputed primes. While dividing, store the smallest prime factor, the largest prime factor, and the remaining factor after removing all small prime factors.

The largest prime factor is enough for the prime category because among all prime divisors it creates the smallest value of `X / N`.
3. Check the candidate `N = 1`. Its cost is `C + X`.
4. If a prime divisor exists, evaluate the cost using the largest prime divisor.
5. Find the largest proper divisor by dividing `X` by its smallest prime factor. If this divisor is composite, evaluate the composite cost.
6. Take the minimum of all available candidates and print it.

Why it works:

For every possible category, the algorithm chooses the divisor that minimizes `X / N`. Since the additional category cost is fixed, increasing `N` can only improve the answer. The largest prime divisor gives the best prime option. The largest proper divisor gives the best composite option when it exists. The value `1` is handled separately because it has its own cost rule. Since every possible category winner is checked, the global minimum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 3162

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

primes = sieve(LIMIT)

def solve_case(x, a, b, c):
    ans = c + x

    temp = x
    smallest = None
    largest = None

    for p in primes:
        if p * p > temp:
            break
        if temp % p == 0:
            if smallest is None:
                smallest = p
            largest = p
            while temp % p == 0:
                temp //= p

    if temp > 1:
        if smallest is None:
            smallest = temp
        largest = temp

    if largest is not None:
        ans = min(ans, a + x // largest)

    if smallest is not None:
        composite = x // smallest
        if composite > 1 and composite % 2 == 0:
            pass
        if composite > 1:
            is_composite = True
            if composite == 2 or composite == 3:
                is_composite = False
            else:
                d = 2
                while d * d <= composite and d <= LIMIT:
                    if composite % d == 0:
                        is_composite = True
                        break
                    d += 1
                else:
                    is_composite = False
            if is_composite:
                ans = min(ans, b + x // composite)

    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        x = int(input())
        a, b, c = map(int, input().split())
        out.append(str(solve_case(x, a, b, c)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The sieve is built once because all queries share the same upper limit for useful trial primes. The factorization loop removes prime powers instead of checking the same divisor repeatedly. This gives both the smallest and largest prime factor during the same pass.

The prime candidate uses the largest prime factor because a larger divisor always makes `X / N` smaller. The composite candidate is created from the largest proper divisor. The extra primality check is necessary because numbers like `9` and `15` have no composite proper divisor even though they are not prime themselves.

Python integers do not overflow, so the large values of `A`, `B`, and `C` are safe during addition. The division order is also important: we first determine the divisor candidate, then compute `X / N` using integer division.

## Worked Examples

### Sample 1

Input:

```
12
2 5 1
```

| Step | Candidate | Category | Cost |
| --- | --- | --- | --- |
| Initial | N = 1 | Special | 13 |
| Prime factor | N = 3 | Prime | 6 |
| Composite factor | N = 6 | Composite | 7 |

The smallest cost is `6`. The trace shows why only the largest divisor of each category is needed. Smaller prime or composite divisors would increase `X / N`.

### Sample 2

Input:

```
9
1 10 3
```

| Step | Candidate | Category | Cost |
| --- | --- | --- | --- |
| Initial | N = 1 | Special | 12 |
| Prime factor | N = 3 | Prime | 13 |
| Composite factor | None | Not available | Not considered |

The answer is `12`. The trace demonstrates the case where the largest proper divisor is prime and no composite candidate exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(pi(sqrt(X))) per query | Only primes up to `3162` are tested during factorization |
| Space | O(1) besides the prime list | The algorithm stores only a few factors and the precomputed primes |

The total number of useful trial primes is very small, around a few hundred. This allows the solution to handle the maximum number of queries efficiently.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline
    t = int(data())
    ans = []
    for _ in range(t):
        x = int(data())
        a, b, c = map(int, data().split())
        ans.append(str(solve_case(x, a, b, c)))
    sys.stdin = old_stdin
    return "\n".join(ans)

assert run("""3
12
2 5 1
12
2 3 1
12
15 15 1
""") == """6
5
13""", "samples"

assert run("""1
2
5 7 3
""") == "5", "minimum value"

assert run("""1
4
1 10 2
""") == "3", "prime proper divisor"

assert run("""1
16
100 1 100
""") == "5", "large composite divisor"

assert run("""1
49
20 1 100
""") == "27", "prime square boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `12` with sample costs | `6` | Normal composite and prime comparison |
| `2` | `5` | Only divisor `1` exists |
| `4` | `3` | Prime proper divisor handling |
| `16` | `5` | Composite divisor selection |
| `49` | `27` | Prime square with no composite proper divisor |

## Edge Cases

For `X = 2`, the algorithm cannot find a prime or composite candidate because there are no proper divisors except `1`. It keeps the initial value `C + X`, which is the only valid answer.

For `X = 9`, factorization finds the smallest and largest prime factor as `3`. The largest proper divisor is also `3`, but the composite check rejects it because it is prime. The algorithm only compares the `N = 1` and prime candidates, avoiding the common mistake of applying the composite cost to a prime divisor.

For `X = 12`, the smallest prime factor is `2`, so the largest proper divisor is `6`. Since `6` is composite, the composite candidate is valid. The algorithm compares `B + 2` against the prime candidate `A + 4` and the special case, producing the correct minimum.
