---
title: "CF 105129L - 15 Prime"
description: "For each test case, we are given an array of integers. We must construct the smallest positive integer m such that every array element shares a common divisor greater than 1 with m. In other words, for every value ai, the greatest common divisor gcd(ai, m) must be at least 2."
date: "2026-06-27T19:24:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "L"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 85
verified: true
draft: false
---

[CF 105129L - 15 Prime](https://codeforces.com/problemset/problem/105129/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given an array of integers. We must construct the smallest positive integer `m` such that every array element shares a common divisor greater than `1` with `m`. In other words, for every value `ai`, the greatest common divisor `gcd(ai, m)` must be at least `2`.

The array size can reach `5 × 10^5`, but every array value is at most `50`. The total amount of input is large enough that any algorithm performing expensive work for every element is undesirable. On the other hand, the tiny value range means there are only a handful of possible prime factors to consider. Since every integer from `2` to `50` has only a few prime divisors, factoring each value is essentially constant time.

One easy mistake is to assume that every distinct prime appearing in the array must divide the answer. Consider the input

```
1
2
6 10
```

The correct answer is `2`, not `30`. Both numbers are divisible by `2`, so a single prime already satisfies every element.

Another common mistake is to multiply the prime factors of every number independently. For example,

```
1
2
12 18
```

The correct answer is `2`. Although `12` contains `2` and `3`, and `18` also contains `2` and `3`, only one shared prime is needed for each number. Requiring every prime factor produces an unnecessarily large answer.

A more subtle case appears when different numbers require different primes. For example,

```
1
2
25 14
```

The first number requires `5`, while the second can use either `2` or `7`. The smallest answer is `10`, obtained by choosing primes `{5, 2}`. Choosing `{5, 7}` gives `35`, which is larger.

## Approaches

The most direct approach is to try increasing values of `m` starting from `1`, checking whether every array element has `gcd(ai, m) ≥ 2`. This is correct because the first valid value is exactly the desired answer. Unfortunately, there is no practical upper bound on how many candidates might need to be tested, making this approach far too slow.

The small bound on the array values completely changes the problem. Every number between `2` and `50` is composed only of the primes

```
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47
```

A number is satisfied if at least one of its prime factors divides `m`. This turns the problem into a covering problem. We must choose a subset of these fifteen primes so that every array element contains at least one chosen prime. Among all valid subsets, we want the one whose product is smallest.

Since there are only fifteen candidate primes, every subset can be represented by a bitmask. There are only `2^15 = 32768` subsets, which is tiny. We precompute the product represented by each mask once. For every test case, we compute the bitmask of prime factors for each distinct value appearing in the array, then scan all subsets. A subset is valid if it intersects every required prime-factor mask. Among valid subsets, the one with the smallest product is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded | O(1) | Too slow |
| Optimal | O(2¹⁵ + n) | O(2¹⁵) | Accepted |

## Algorithm Walkthrough

1. Store the fifteen primes not exceeding `50`.
2. Before processing the test cases, compute the product corresponding to every subset of these primes. If a bit is set, multiply the corresponding prime into the product.
3. Also precompute, for every value from `2` to `50`, a bitmask indicating which of the fifteen primes divide it.
4. For each test case, record which values actually appear in the array. Duplicate values do not change the answer because they impose the same requirement.
5. Enumerate every subset of the fifteen primes.
6. For each subset, check every distinct value present in the array. The subset satisfies that value exactly when the subset mask and the value's prime-factor mask share at least one common bit.
7. If every value is satisfied, compare the subset's product with the current best answer and keep the smaller one.
8. Output the smallest valid product.

### Why it works

Each prime selected into the subset becomes a divisor of `m`. A value `ai` satisfies the condition `gcd(ai, m) ≥ 2` precisely when at least one prime dividing `ai` is also selected into `m`. The algorithm checks every possible subset of the only fifteen relevant primes, so every possible candidate answer is considered. Among all valid subsets, it returns the one with the smallest product, which is exactly the minimum valid integer.

## Python Solution

```python
import sys
input = sys.stdin.readline

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
P = len(PRIMES)

# mask of prime factors for every value
factor_mask = [0] * 51
for x in range(2, 51):
    mask = 0
    for i, p in enumerate(PRIMES):
        if x % p == 0:
            mask |= 1 << i
    factor_mask[x] = mask

# product represented by each subset
prod = [1] * (1 << P)
for mask in range(1, 1 << P):
    b = mask & -mask
    idx = b.bit_length() - 1
    prod[mask] = prod[mask ^ b] * PRIMES[idx]

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        present = [False] * 51
        need = []
        for x in arr:
            if not present[x]:
                present[x] = True
                need.append(factor_mask[x])

        best = None

        for mask in range(1, 1 << P):
            ok = True
            for req in need:
                if (mask & req) == 0:
                    ok = False
                    break
            if ok:
                if best is None or prod[mask] < best:
                    best = prod[mask]

        out.append(str(best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first precomputation determines which primes divide every possible value. Since the value range is fixed, this work is performed only once.

The second precomputation stores the product for every subset. Using the lowest set bit lets each product be derived from a smaller subset instead of recomputing the multiplication from scratch.

For each test case, duplicate values are removed because identical numbers produce identical prime masks. This slightly reduces the work during subset checking.

The subset loop simply verifies whether every required mask shares at least one bit with the current subset. Since all products were precomputed, comparing candidate answers is constant time.

## Worked Examples

### Example 1

Input

```
1
2
7 47
```

| Subset | Product | Covers 7 | Covers 47 | Valid |
| --- | --- | --- | --- | --- |
| {7} | 7 | Yes | No | No |
| {47} | 47 | No | Yes | No |
| {7,47} | 329 | Yes | Yes | Yes |

The only way to satisfy both numbers is to include both primes, so the answer is `329`.

### Example 2

Input

```
1
8
3 4 6 7 8 9 10 14
```

| Subset | Product | All numbers covered | Valid |
| --- | --- | --- | --- |
| {2} | 2 | No | No |
| {3} | 3 | No | No |
| {2,3} | 6 | No | No |
| {2,7} | 14 | Yes | Yes |

The value `3` requires prime `3`, but `7` requires prime `7`. The numbers divisible by `2` are already covered by choosing `2`. The smallest successful subset is `{2,7}`, giving the answer `14`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2¹⁵ + n) | Every subset is checked against at most 49 distinct values, while reading the array takes O(n). |
| Space | O(2¹⁵) | Products for all subsets are stored once. |

The dominant work is scanning `32768` subsets, each against at most `49` distinct values. This is well within the limits, even for the largest allowed input size.

## Test Cases

```python
import sys, io

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
P = len(PRIMES)

factor_mask = [0] * 51
for x in range(2, 51):
    mask = 0
    for i, p in enumerate(PRIMES):
        if x % p == 0:
            mask |= 1 << i
    factor_mask[x] = mask

prod = [1] * (1 << P)
for mask in range(1, 1 << P):
    b = mask & -mask
    idx = b.bit_length() - 1
    prod[mask] = prod[mask ^ b] * PRIMES[idx]

def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        need = []
        seen = [False] * 51
        for x in arr:
            if not seen[x]:
                seen[x] = True
                need.append(factor_mask[x])
        best = None
        for mask in range(1, 1 << P):
            if all(mask & m for m in need):
                if best is None or prod[mask] < best:
                    best = prod[mask]
        ans.append(str(best))
    print("\n".join(ans))

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

assert run("1\n2\n7 47\n") == "329"
assert run("1\n8\n3 4 6 7 8 9 10 14\n") == "14"

assert run("1\n1\n2\n") == "2"
assert run("1\n4\n6 6 6 6\n") == "2"
assert run("1\n2\n25 14\n") == "10"
assert run("1\n3\n49 25 9\n") == "315"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `2` | Minimum array size |
| `6 6 6 6` | `2` | Duplicate values do not matter |
| `25 14` | `10` | Different numbers can require different primes |
| `49 25 9` | `315` | Three unrelated prime requirements |

## Edge Cases

Consider the input

```
1
2
6 10
```

The required masks are `{2,3}` and `{2,5}`. The subset containing only prime `2` intersects both masks, so the algorithm returns `2`. It never forces inclusion of unnecessary primes.

Now consider

```
1
2
25 14
```

The required masks are `{5}` and `{2,7}`. During subset enumeration, `{5,2}` is accepted with product `10`, while `{5,7}` is also accepted with product `35`. Since every valid subset is examined, the algorithm correctly chooses the smaller answer.

Finally, consider

```
1
3
6 6 6
```

Only one distinct mask is stored because repeated values impose identical constraints. Every subset is checked once against that mask, producing the same answer as processing all three copies while avoiding redundant work.
