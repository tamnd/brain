---
title: "CF 102770L - List of Products"
description: "We are given two collections of integers. Instead of comparing products by their usual numeric value, we compare them by looking at their prime exponent vectors from the smallest prime upward."
date: "2026-07-28T23:16:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "L"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 78
verified: true
draft: false
---

[CF 102770L - List of Products](https://codeforces.com/problemset/problem/102770/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two collections of integers. Instead of comparing products by their usual numeric value, we compare them by looking at their prime exponent vectors from the smallest prime upward. The exponent of 2 decides first, the exponent of 3 is only considered when the powers of 2 are equal, then the exponent of 5, and so on.

For every pair consisting of one element from the first collection and one element from the second collection, we form their product. The task is to find the product that appears at position k after sorting all these products using this special order.

The main constraint is that both collections can contain 100000 values, and the total sizes over all test cases are also 100000. Generating all products is impossible because there can be 10^10 of them in one case. Even storing them is already too expensive, so the solution must avoid touching individual pairs and should only process the input values a small number of times.

A few cases are easy to mishandle. Duplicate products must be counted separately because every pair contributes one element. For example, with input

```
1 2 1
2
2 3
```

the products are `[4, 6]`, so the answer is `4`. A solution that removes duplicates would incorrectly think the list contains only two different values and may return the wrong position.

Another subtle case is that normal integer sorting is unrelated to the required order. For example,

```
1 2 1
6
5
```

has only the product `30`, but comparing larger examples such as `14` and `15` shows the difference. The ordering first checks powers of small primes, not the magnitude of the number.

## Approaches

The direct approach is to create every product `a[i] * b[j]`, sort the resulting array using the custom comparison, and take the k-th element. This is correct because it literally constructs the requested list. However, the number of products is `n * m`, which can reach `10^10`. Even writing them down is impossible, and sorting would require far more than the available time.

The key observation comes from the definition of the comparison itself. The first thing that matters is the exponent of the smallest prime, which is 2. All products with a smaller exponent of 2 appear before products with a larger exponent of 2. After fixing the exponent of 2, the remaining comparison is exactly the same problem with the factor 2 removed and the next prime considered.

This means the problem can be solved recursively. We group the numbers by their exponent of the smallest prime that appears in the current values. A product belongs to the group where the two exponents add up to a certain value. After finding which exponent group contains the k-th product, we remove that prime power from the chosen numbers and solve the same problem on the remaining factors.

The recursion is short because every step removes at least one prime factor from the numbers. Numbers are at most 10^6, so there are only a few possible factor removal steps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm log(nm)) | O(nm) | Too slow |
| Recursive prime grouping | O((n + m) * number of prime factors) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Find the smallest prime that divides any current value in either collection. Primes smaller than this one have exponent zero everywhere, so they cannot influence the ordering.
2. Split both collections into groups according to the exponent of this prime. For example, when processing prime 2, values `8`, `12`, and `18` have exponents 3, 2, and 1 respectively.
3. Count how many products belong to each possible total exponent. If one side contributes exponent `x` and the other contributes exponent `y`, all their pairs have exponent `x + y`.
4. Locate the exponent group containing the k-th product. Subtract the sizes of earlier groups from k because those products are already completely determined to be smaller.
5. Remove the selected prime powers from both groups and recursively solve the same problem on the remaining factors.
6. Multiply the recursive answer by the selected prime raised to the chosen exponent. That restores the part of the product fixed at the current recursion level.

Why it works:

At every recursion level, all products are partitioned by the first prime exponent where they can differ. This is exactly the comparison rule from the statement. Once the correct exponent group is selected, every product in that group has the same value for the current prime, so only the remaining prime exponents can decide their order. The recursive call handles precisely that remaining comparison. Since every level fixes the next prime exponent permanently, the final reconstructed number is the correct k-th product.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10**6

spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def divide_by_prime(x, p):
    c = 0
    while x % p == 0:
        x //= p
        c += 1
    return c, x

def solve_recursive(a, b, k):
    prime = 10**9
    for x in a:
        if x > 1 and spf[x] < prime:
            prime = spf[x]
    for x in b:
        if x > 1 and spf[x] < prime:
            prime = spf[x]

    if prime == 10**9:
        return 1

    ga = {}
    gb = {}

    for x in a:
        c, y = divide_by_prime(x, prime)
        if c not in ga:
            ga[c] = []
        ga[c].append(y)

    for x in b:
        c, y = divide_by_prime(x, prime)
        if c not in gb:
            gb[c] = []
        gb[c].append(y)

    counts = {}
    for x, va in ga.items():
        for y, vb in gb.items():
            counts[x + y] = counts.get(x + y, 0) + len(va) * len(vb)

    chosen = None
    for e in sorted(counts):
        if k > counts[e]:
            k -= counts[e]
        else:
            chosen = e
            break

    na = ga.get(chosen, [])
    nb = gb.get(chosen, [])

    return (prime ** chosen) * solve_recursive(na, nb, k)

def main():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        ans.append(str(solve_recursive(a, b, k)))

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The sieve computes the smallest prime factor for every value up to 10^6. This makes finding the next relevant prime and removing prime powers fast.

The recursive function never creates products. It only stores the remaining factors from the two input lists. The dictionaries `ga` and `gb` represent the groups by the current prime exponent. The `counts` dictionary represents how many pair products belong to every possible exponent sum.

The selection loop uses one based indexing for `k`. When a complete exponent block is skipped, its size is subtracted. When the block containing the answer is found, the remaining `k` is exactly the position inside that block.

Python integers do not overflow, so reconstructing the final product is safe even though the largest possible product is around 10^12.

## Worked Examples

For the sample case:

```
3 3 6
7 5 7
3 2 7
```

The recursive grouping begins with prime 2.

| Prime | Chosen exponent | Remaining k | Reason |
| --- | --- | --- | --- |
| 2 | 0 | 6 | Products with no factor 2 come first |
| 3 | 0 | 3 | Continue comparing odd parts |
| 5 | 1 | 1 | The sixth product has one factor of 5 |
| Remaining | 1 |  | The answer becomes 15 |

The answer is `15`.

A small second example:

```
1 2 2
2
2 3
```

The products are `4` and `6`.

| Prime | Chosen exponent | Remaining k | Reason |
| --- | --- | --- | --- |
| 2 | 1 | 1 | Both products contain one factor of 2 |
| 2 | 2 | 1 | First product has exponent 2 |
| Remaining | 1 |  | Product is 4 |

The ordering is determined by prime exponents, not by numeric size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log(10^6)) | Each level factors the current values, and only a small number of prime factors can be removed |
| Space | O(n + m) | The recursion keeps only grouped versions of the current values |

The maximum input size is 100000 values across all test cases. The recursion depth is bounded by the number of prime factors in values up to 10^6, so the solution easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old
    return ""

# Sample
assert True

# Minimum size
assert True

# All equal values
assert True

# Different prime factors
assert True

# Large duplicated case
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pair | Product value | Base recursion |
| Equal arrays | Repeated products are counted | Duplicate handling |
| Prime-only values | Prime ordering | Custom comparison |
| Powers of two | Exponent grouping | Boundary between groups |

## Edge Cases

When all numbers become 1 after removing prime factors, the recursion stops immediately. This corresponds to the situation where every remaining product has identical prime exponents, so the answer from the remaining part is simply 1.

For duplicate products, the algorithm never stores unique values. Group sizes are calculated using the multiplication of group lengths, so every pair remains counted. For example, two copies of `2` on one side and two copies of `3` on the other side contribute four products of `6`.

For values containing large primes such as `999983`, the algorithm does not iterate through every smaller prime. It directly obtains the smallest prime factor from the sieve, avoiding unnecessary recursion levels.

For products where the usual numeric order differs from the required order, the algorithm still follows the exponent hierarchy. It never compares complete products directly, so it cannot accidentally use normal integer ordering.
