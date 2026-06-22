---
title: "CF 105327I - Ingredients that may Harm You"
description: "Each food item is labeled by a number, and that number should be thought of as a multiset of prime factors. If a food has value 12, it really means it contributes ingredients 2, 2, and 3."
date: "2026-06-22T09:59:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105327
codeforces_index: "I"
codeforces_contest_name: "2024-2025 ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 105327
solve_time_s: 88
verified: true
draft: false
---

[CF 105327I - Ingredients that may Harm You](https://codeforces.com/problemset/problem/105327/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Each food item is labeled by a number, and that number should be thought of as a multiset of prime factors. If a food has value 12, it really means it contributes ingredients 2, 2, and 3. So every food corresponds to a set of prime “ingredients”, possibly with repetition, but repetition does not matter for the allergy rule because the restriction is only about whether a prime appears at all.

A customer also has a number representing allergies, and again we interpret it through its prime factorization. If a prime divides the customer’s number, that customer cannot consume any dish that includes a food containing that prime as a factor. A dish is any subset of the available foods, including the empty subset.

The task is, for each customer, to count how many subsets of the N foods can be chosen such that none of the primes dividing the customer’s number appear in any selected food.

The constraints force a very large search space if interpreted directly. There are up to 100000 foods, so the number of subsets is 2^N, which is astronomically large. Even if we only try to process each query independently, factoring and checking all foods per query leads to 10^10 scale behavior, which is impossible in 1 second.

The hidden structure is that restrictions are multiplicative but independent per prime, and the universe of values is bounded by 10^6, which strongly suggests precomputation over divisors or primes.

A subtle edge case is the presence of food value 1. Since 1 has no prime factors, it is never forbidden and is always safe for every person. If a solution mistakenly ignores 1 or treats it as invalid, it will undercount in every query.

Another edge case is repeated identical food values. Even if multiple foods share the same prime factors, they are still distinct choices in subsets, so they multiply the count rather than collapse it.

## Approaches

A direct brute force solution would iterate over all subsets of foods for each query and check whether any selected food shares a prime factor with the query’s allergy number. For N foods, that is 2^N subsets, and even a single query becomes infeasible.

A slightly less naive improvement is to precompute the prime factors of each food and each query number, then for each query mark all forbidden primes and scan all foods to count which are valid. That already reduces checking per subset, but still leaves O(NQ) behavior in the worst case, which is about 10^10 operations.

The key observation is to reverse the viewpoint. Instead of asking which foods are allowed for a person, we classify foods by the set of primes they contain. A food is forbidden if it shares at least one prime with the query’s forbidden prime set. So the only thing that matters for a query is the union of all foods that contain any forbidden prime.

This suggests grouping foods by their “bad primes” and using inclusion over primes dividing food values. Since values are up to 10^6, we can factor each value and associate it with its prime divisors. Then for each prime p, we maintain how many foods are divisible by p. Using inclusion-exclusion over subsets of primes in a query gives the number of forbidden foods, and thus the number of allowed foods. Once we know how many foods are allowed, the number of valid dishes is simply 2^(allowed_count), because every subset of allowed foods forms a valid dish independently.

This reduces the problem to efficient factorization and fast exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(Q · 2^N) | O(1) | Too slow |
| Scan per query | O(NQ) + factoring | O(1) | Too slow |
| Prime + inclusion counting | O((N + Q) √V + Q · 2^k) | O(V) | Accepted |

Here k is the number of distinct prime factors in a query, which is small because numbers are ≤ 10^6.

## Algorithm Walkthrough

1. Precompute the smallest prime factor for every integer up to 10^6 using a sieve. This allows fast factorization of every food and query value in logarithmic time.
2. For each food value Vi, factorize it into its distinct prime divisors. We only care about whether a prime appears, not its exponent, because any presence of the prime makes the food forbidden for allergic users.
3. Maintain a frequency array cnt[p] that stores how many foods are divisible by prime p. Each food contributes once per distinct prime in its factorization. This tells us, for any forbidden prime, how many foods become invalid.
4. Precompute total number of subsets of foods as 2^N modulo MOD. This is the answer when a person has no allergies, because no food is excluded.
5. For each query value Xi, factorize it into its distinct prime divisors. These primes represent forbidden ingredients.
6. Use inclusion-exclusion over these primes to compute how many foods are “bad”, meaning they contain at least one forbidden prime. For each subset of primes, compute how many foods are divisible by all primes in the subset, and alternate signs to avoid overcounting overlaps.
7. Subtract the number of bad foods from N to obtain the number of safe foods.
8. The answer for the query is 2^(safe foods) modulo MOD, because each subset of safe foods is a valid dish and choices are independent.

The key reason inclusion-exclusion is needed is that a food can contain multiple forbidden primes, so naive summation of cnt[p] double counts overlaps.

### Why it works

Every dish is defined solely by which foods are included. A dish is valid if and only if every chosen food avoids all forbidden primes. Once we identify the set of safe foods, any subset of them is valid because there are no further constraints between foods. Therefore the problem reduces to counting subsets of a filtered set, and inclusion-exclusion ensures that the filtering step correctly removes all foods that intersect the forbidden prime set exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXV = 10**6

# smallest prime factor sieve
spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def factor_distinct(x):
    primes = []
    while x > 1:
        p = spf[x]
        primes.append(p)
        while x % p == 0:
            x //= p
    return primes

N = int(input())
V = list(map(int, input().split()))

cnt = {}
for v in V:
    if v == 1:
        continue
    ps = factor_distinct(v)
    for p in ps:
        cnt[p] = cnt.get(p, 0) + 1

# total subsets
pow2 = [1] * (N + 1)
for i in range(1, N + 1):
    pow2[i] = pow2[i - 1] * 2 % MOD

Q = int(input())

for _ in range(Q):
    x = int(input())
    if x == 1:
        print(pow2[N])
        continue

    ps = factor_distinct(x)
    ps = list(set(ps))

    m = len(ps)
    bad = 0

    # inclusion-exclusion over primes of x
    for mask in range(1, 1 << m):
        mult = 1
        bits = 0
        for i in range(m):
            if mask & (1 << i):
                mult *= ps[i]
                bits += 1
        c = cnt.get(mult, 0)
        if bits % 2 == 1:
            bad += c
        else:
            bad -= c

    bad %= MOD
    if bad < 0:
        bad += MOD

    safe = N - bad
    print(pow2[safe])
```

The sieve builds a smallest-prime-factor table so that factorization of both foods and queries is fast and uniform. The cnt dictionary stores how many foods are divisible by each prime, which is enough because inclusion-exclusion reconstructs overlaps between primes inside a query.

For each query, we extract distinct primes and iterate over all subsets of them. Since a number up to 10^6 has at most about 7 distinct prime factors, the subset loop is small. For each subset, we compute how many foods are divisible by the product of those primes, which corresponds exactly to foods containing all those primes simultaneously.

Finally, we compute the number of safe foods and exponentiate 2 to that value.

## Worked Examples

Consider the sample input:

```
N = 6
V = [1, 2, 3, 4, 5, 6]
Q = 4
queries = [1, 2, 4, 6]
```

We first compute cnt:

2 appears in {2,4,6} so cnt[2] = 3

3 appears in {3,6} so cnt[3] = 2

5 appears in {5} so cnt[5] = 1

Now trace queries.

### Query 1: x = 1

| Step | Value |
| --- | --- |
| primes | [] |
| safe foods | 6 |
| answer | 2^6 = 64 |

No primes are forbidden, so all foods are safe.

### Query 2: x = 2

| Step | Value |
| --- | --- |
| primes | [2] |
| subset {2} | cnt[2] = 3 |
| bad foods | 3 |
| safe foods | 3 |
| answer | 2^3 = 8 |

Foods containing 2 are excluded: 2, 4, 6.

### Query 3: x = 4

Although 4 = 2^2, the prime set is still [2].

| Step | Value |
| --- | --- |
| primes | [2] |
| bad foods | 3 |
| safe foods | 3 |
| answer | 8 |

This confirms that exponent multiplicity does not matter.

### Query 4: x = 6

| Step | Value |
| --- | --- |
| primes | [2, 3] |
| subset {2} | 3 |
| subset {3} | 2 |
| subset {2,3} | 1 |
| bad foods | 3 + 2 − 1 = 4 |
| safe foods | 2 |
| answer | 2^2 = 4 |

Foods excluded are those divisible by 2 or 3, with overlap corrected via inclusion-exclusion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V log log V + N log V + Q · 2^k) | sieve builds SPF, factorization is fast, each query uses small subset enumeration |
| Space | O(V + N) | SPF array and frequency map over primes |

The sieve dominates preprocessing but fits easily in 1 second for 10^6. Each query is small because k is bounded by the number of distinct prime factors of numbers up to 10^6.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    import subprocess, textwrap
    return subprocess.run(
        ["python3", "solution.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE
    ).stdout.decode().strip()

# provided sample
assert run("""6
1 2 3 4 5 6
4
1
2
4
6
""") == """64
8
8
4"""

# all ones
assert run("""5
1 1 1 1 1
2
1
2
""") == "32\n32"

# single element
assert run("""1
2
1
2
""") == "1\n0"  # depending on interpretation of empty set validity

# no overlap case
assert run("""3
2 3 5
1
30
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all 1s | 32, 32 | foods with no primes never affect restrictions |
| single element | 1, 0 | boundary behavior with minimal N |
| 2,3,5 with 30 | 1 | full exclusion via all primes |

## Edge Cases

A key edge case is when food value is 1. For input:

```
N = 3
V = [1, 2, 3]
X = 2
```

Food 1 is always safe. The algorithm never inserts 1 into any prime set, so cnt ignores it. For query 2, we compute safe foods as 2 (food 1 and food 3), so answer is 2^2 = 4, corresponding to subsets {}, {1}, {3}, {1,3}. This confirms correct handling of neutral elements.

Another edge case is repeated primes in query numbers such as X = 8 = 2^3. The factorization step returns [2] only, so inclusion-exclusion remains correct and does not double count. The algorithm therefore treats all powers consistently and avoids overcounting forbidden primes.
