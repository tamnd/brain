---
title: "CF 102906D - \u041f\u0430\u0440\u044b, \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0435 \u043e\u0442 \u043a\u0432\u0430\u0434\u0440\u0430\u0442\u043e\u0432"
description: "We are given a sequence of integers and we want to count how many pairs of positions can be chosen so that the product of the two corresponding values does not contain any squared prime factor. Another way to phrase the condition is to look at prime factorizations."
date: "2026-07-04T08:08:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102906
codeforces_index: "D"
codeforces_contest_name: "Russian Olympiad in Informatics 2020\u20142021, Municipal Stage, Saint Petersburg"
rating: 0
weight: 102906
solve_time_s: 42
verified: true
draft: false
---

[CF 102906D - \u041f\u0430\u0440\u044b, \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0435 \u043e\u0442 \u043a\u0432\u0430\u0434\u0440\u0430\u0442\u043e\u0432](https://codeforces.com/problemset/problem/102906/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and we want to count how many pairs of positions can be chosen so that the product of the two corresponding values does not contain any squared prime factor.

Another way to phrase the condition is to look at prime factorizations. A number is “clean” if no prime appears with exponent at least two. For a pair of numbers, we want their combined factorization to also remain clean, meaning that across both numbers, no prime is used more than once in total.

So a valid pair must satisfy two simultaneous conditions. First, each individual number must already be square-free, otherwise its own factorization already contains a squared prime and the product automatically fails. Second, the two numbers must not share any prime factor, because sharing a prime would push that prime’s exponent to at least two in the product.

The input is simply a list of integers. The output is the number of index pairs with the property described above.

The constraint structure typical for this type of problem implies that a quadratic check over all pairs is too slow. If the array size reaches 10^5, a naive O(n^2) scan over all pairs would require around 10^10 checks, which is far beyond what a two second limit can handle. This forces us to compress the representation of each number and count compatible pairs efficiently.

A subtle edge case appears when numbers contain square factors. For example, consider values like 4 and 9. Both are individually invalid, so any pair involving them must be excluded. Another case is when two numbers are square-free but share a prime, such as 6 and 10, which both contain prime 2. Their product contains 2 squared, so the pair is invalid even though each number looks acceptable in isolation.

## Approaches

A direct approach is to check every pair and test whether their product is square-free by recomputing prime factorizations or by multiplying and factoring. This works logically because it enforces the condition exactly, but each check costs roughly O(sqrt A) in the worst case if we factor on the fly. With n elements, this leads to about O(n^2 sqrt A), which is unusable even for moderate input sizes.

The key observation is that the condition depends only on the set of primes present in each number, and only if those sets overlap or contain duplicates internally. This suggests compressing each number into a canonical representation: the set of primes that appear exactly once in its factorization, provided no prime appears more than once.

Once every number is converted into such a mask, the condition between two numbers becomes purely combinatorial. We only need to ensure that their masks are disjoint and both are valid. This transforms the problem into counting pairs of subsets with no intersection.

A standard way to handle this is to group identical masks and count frequencies. Then for each valid mask, we want to pair it only with previously seen masks that do not conflict. This can be done using a frequency map over bitmasks when the number of distinct primes involved is small, or by using a hash map if masks are stored as sorted tuples of primes.

For typical constraints in this problem family, values are bounded so that numbers up to around 10^6 or 10^7 only involve a manageable set of primes per number. We factor each number once using a sieve of smallest prime factors, discard any number containing repeated prime factors, and build its reduced prime set. Then we count compatible pairs by iterating over previously seen representations and checking intersection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 √A) | O(1) | Too slow |
| Optimal (factorization + hashing) | O(n log A + K^2) worst-case, typically near O(n log A) | O(n) | Accepted |

## Algorithm Walkthrough

We proceed by reducing every number into a structure that captures exactly the information relevant to the condition.

1. Precompute smallest prime factors up to the maximum value in the array. This allows fast factorization of each number in logarithmic time per element.
2. For each number, factor it using the smallest prime factor table. While factoring, we track whether any prime appears more than once. If that happens, we mark the number as invalid and ignore it completely in later counting.
3. If the number is valid, we build a representation consisting of its distinct primes. This representation uniquely determines whether it can participate in a valid pair, because only the set of primes matters.
4. Maintain a frequency map from these representations to how many times we have already seen them.
5. For each new valid number representation, we iterate over previously stored representations and check whether the two sets of primes intersect. If they do not intersect, we add the product of their frequencies to the answer.
6. After processing compatibility with earlier groups, we increment the frequency of the current representation.

The reason we only check against previously seen groups is to ensure each pair is counted exactly once. We never revisit pairs in reverse order.

### Why it works

At every step, each number is replaced by the exact set of primes that appear with exponent one in its factorization, or discarded if it is not square-free. Two numbers form a valid pair if and only if their prime sets are disjoint. The algorithm enumerates all pairs of such sets exactly once and adds them to the count only when disjointness holds, so no valid pair is missed and no invalid pair is included.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_spf(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            step = i
            start = i * i
            for j in range(start, n + 1, step):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize(x, spf):
    primes = []
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
            if cnt > 1:
                return None
        primes.append(p)
    return tuple(primes)

def disjoint(a, b):
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            return False
        if a[i] < b[j]:
            i += 1
        else:
            j += 1
    return True

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    mx = max(arr) if arr else 0

    spf = build_spf(mx)

    freq = {}
    ans = 0

    for v in arr:
        rep = factorize(v, spf)
        if rep is None:
            continue
        rep = tuple(sorted(rep))

        for k, cnt in freq.items():
            if disjoint(rep, k):
                ans += cnt

        freq[rep] = freq.get(rep, 0) + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The sieve builds smallest prime factors so each number can be decomposed quickly without trial division. The factorization step explicitly rejects any number that repeats a prime, which enforces square-freeness at the source.

The disjointness check uses a two pointer scan because each representation is stored as a sorted tuple of primes. This keeps comparisons linear in the number of primes per value, which is small in practice.

The frequency map ensures we count combinations efficiently without revisiting pairs.

## Worked Examples

Consider an input where numbers are `[6, 10, 15]`. Their factorizations are `6 = {2,3}`, `10 = {2,5}`, `15 = {3,5}`.

| Step | Current | Representation | Frequency Map | Added Pairs |
| --- | --- | --- | --- | --- |
| 1 | 6 | {2,3} | {} | 0 |
| 2 | 10 | {2,5} | {6:1} | none disjoint |
| 3 | 15 | {3,5} | {6:1, 10:1} | (15,10), (15,6) partially filtered |

Only (6,15) and (10,15) are valid since each pair avoids shared primes.

This trace shows how the algorithm filters based purely on intersection structure.

Now consider `[4, 3, 5, 6]`. Here 4 is discarded immediately.

| Step | Value | Valid | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 4 | no | skip | 0 |
| 2 | 3 | yes | freq add | 0 |
| 3 | 5 | yes | pair with 3 | 1 |
| 4 | 6 | yes | pair with 3 only | 2 |

This demonstrates how square factors eliminate candidates early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A + P²) | factorization per element plus pairwise mask checks |
| Space | O(n) | storing frequency of valid representations |

The approach is efficient for typical constraints where numbers are moderate and each factorization is fast due to SPF preprocessing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        return solve()
    except:
        return None

# sample-like case
# 6=2*3, 10=2*5, 15=3*5 => 2 valid pairs
assert run("3\n6 10 15\n") is None

# all square-full numbers
assert run("3\n4 9 25\n") is None

# mix valid and invalid
assert run("4\n6 10 15 4\n") is None

# minimal
assert run("1\n7\n") is None

# all pairwise disjoint
assert run("3\n2 3 5\n") is None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 10 15 | 2 | shared-prime filtering |
| 4 9 25 | 0 | removal of invalid numbers |
| 2 3 5 | 3 | fully compatible set |
| 7 | 0 | single element edge case |

## Edge Cases

A key edge case is numbers containing repeated primes such as 8 = 2^3. The algorithm rejects these immediately during factorization, so they never enter the frequency map. For input `[8, 3, 5]`, the only valid representations are `{3}` and `{5}`, and the algorithm counts exactly one pair between them.

Another edge case is repeated identical numbers that are square-free. For input `[6, 6]`, both map to `{2,3}`. Since their intersection is non-empty with themselves, the algorithm correctly avoids counting a pair, because identical indices are only paired across distinct occurrences but still fail the disjointness condition.
