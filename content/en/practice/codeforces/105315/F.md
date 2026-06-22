---
title: "CF 105315F - Osama's Birthday"
description: "We are given several collections of flower types, where each collection (called a bouquet) is essentially a set of allowed flower labels drawn from a universe of size at most 60. For each test case, Osama chooses exactly one bouquet and then builds a garden of length $m$."
date: "2026-06-23T06:14:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "F"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 50
verified: true
draft: false
---

[CF 105315F - Osama's Birthday](https://codeforces.com/problemset/problem/105315/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several collections of flower types, where each collection (called a bouquet) is essentially a set of allowed flower labels drawn from a universe of size at most 60. For each test case, Osama chooses exactly one bouquet and then builds a garden of length $m$. Each position in the garden is filled independently by picking any flower type from the chosen bouquet, and repetition is allowed.

So if a bouquet contains $k$ distinct flower types, then that bouquet can generate exactly $k^m$ different gardens, because each of the $m$ positions can be any of the $k$ types independently.

The complication is that we are asked for the number of distinct gardens across all bouquets, meaning if two different bouquets can produce the same sequence, that sequence must only be counted once. This happens naturally when bouquet type-sets overlap.

The constraints drive the solution structure. The number of bouquets is at most 19, which immediately suggests that any exponential dependency on $n$, such as $2^n$, is acceptable. The value $m$ can be as large as $10^9$, so any approach that iterates over positions of the garden is impossible. However, since each bouquet contributes a term of the form $|S|^m$, we only ever need fast exponentiation, not iteration over length.

The most important structural observation is that the universe of flower types is only size 60, so each bouquet can be represented as a bitmask over 60 elements. This makes intersection operations fast and exact.

A subtle edge case is when different subsets of bouquets produce identical intersection sets. For example, if bouquet A and bouquet B are identical, then both contribute the same $k^m$, and naive summation would double count. Another issue is that inclusion-exclusion must be used over subsets of bouquets, otherwise overlaps cannot be corrected.

A small concrete failure case for naive thinking is:

If bouquet 1 is $\{1,2\}$ and bouquet 2 is $\{2,1\}$, and $m=2$, then both generate the same set of sequences, and simply adding $2^2 + 2^2$ would overcount. The correct answer is $4$, not $8$.

## Approaches

The brute-force idea is to treat each bouquet independently, enumerate all $k^m$ sequences conceptually, and then attempt to deduplicate across bouquets. This immediately fails because even storing or iterating over all sequences is impossible when $m$ is large. The number of sequences per bouquet grows exponentially in $m$, so any explicit construction is infeasible.

The key structural insight is that each bouquet defines a full Cartesian power of a set. The union of these powers can be handled using inclusion-exclusion over bouquets. For any subset of bouquets, their intersection corresponds to sequences that can be formed using only flower types common to all bouquets in the subset. If that intersection has size $x$, then it contributes exactly $x^m$ sequences.

Using inclusion-exclusion over all non-empty subsets ensures that every sequence is counted exactly once, because every valid sequence has a well-defined set of bouquets that contain all its used flower types, and inclusion-exclusion isolates the maximal intersection responsible for it.

Since $n \le 19$, iterating over all $2^n$ subsets is feasible. Each subset requires computing the intersection of masks and then evaluating a fast modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential in $m$ | Huge | Too slow |
| Inclusion-Exclusion over subsets | $O(2^n \cdot 60 + 2^n \log m)$ | $O(60)$ | Accepted |

## Algorithm Walkthrough

1. Represent each bouquet as a 60-bit mask. Each bit indicates whether a flower type is present in that bouquet. This allows intersections to be computed using bitwise AND, which is constant time.
2. Iterate over all non-empty subsets of bouquets using bitmasks from $1$ to $(1 \ll n) - 1$. Each subset represents a group of bouquets whose intersection we will analyze.
3. For each subset, compute the intersection mask by ANDing all bouquets in the subset. The size of this mask is the number of flower types common to all bouquets in the subset. This is the only set of types that can appear in a sequence valid for all those bouquets simultaneously.
4. Compute $x^m \bmod (10^9+7)$, where $x$ is the size of the intersection mask. This represents the number of sequences that can be formed using exactly those common types.
5. Apply inclusion-exclusion: if the subset size is odd, add this value to the answer, otherwise subtract it. This alternation corrects overcounting caused by overlaps between different bouquet groups.
6. Return the final accumulated result modulo $10^9+7$.

### Why it works

Every valid garden is a length-$m$ sequence over some set of flower types. That set must be contained in at least one bouquet, but may be contained in multiple. The inclusion-exclusion over bouquet subsets ensures that each sequence is counted once for the maximal subset of bouquets that still contain all its chosen flower types. Because intersection sizes uniquely determine the available alphabet for sequences in each subset, the contribution $x^m$ precisely counts all sequences supported by that subset, and alternating signs remove overcounting from larger overlapping subsets.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modpow(a, e):
    res = 1
    a %= MOD
    while e > 0:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        masks = []
        for _ in range(n):
            arr = list(map(int, input().split()))
            k = arr[0]
            vals = arr[1:]
            mask = 0
            for v in vals:
                mask |= 1 << (v - 1)
            masks.append(mask)

        ans = 0

        for s in range(1, 1 << n):
            inter = (1 << 60) - 1
            for i in range(n):
                if s >> i & 1:
                    inter &= masks[i]
                    if inter == 0:
                        break

            if inter == 0:
                continue

            cnt = inter.bit_count()
            val = modpow(cnt, m)

            if bin(s).count("1") % 2 == 1:
                ans = (ans + val) % MOD
            else:
                ans = (ans - val) % MOD

        print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The implementation follows the subset enumeration directly. Each bouquet is compressed into a bitmask so intersections reduce to a single AND operation. The intersection starts from all 60 bits set, ensuring correctness even when some bouquets are sparse.

The exponentiation is handled with binary exponentiation because $m$ can be as large as $10^9$. The subset parity determines whether the contribution is added or subtracted, implementing inclusion-exclusion exactly as required.

A small but important detail is early stopping when the intersection becomes zero. Once no flower types remain common, that subset contributes nothing, and further processing is skipped.

## Worked Examples

### Example 1

Input:

```
n = 2, m = 2
bouquets: {1,2}, {2,3}
```

We enumerate subsets:

| Subset | Intersection | Size | Contribution |
| --- | --- | --- | --- |
| {1} | {1,2} | 2 | +4 |
| {2} | {2,3} | 2 | +4 |
| {1,2} | {2} | 1 | -1 |

Final answer is $4 + 4 - 1 = 7$.

This matches the idea that sequences over {2} are counted twice in single-bouquet contributions and corrected by the combined subset.

### Example 2

Input:

```
n = 3, m = 1
{1,2}, {2,3}, {3}
```

| Subset | Intersection | Size | Contribution |
| --- | --- | --- | --- |
| {1} | {1,2} | 2 | +2 |
| {2} | {2,3} | 2 | +2 |
| {3} | {3} | 1 | +1 |
| {1,2} | {2} | 1 | -1 |
| {1,3} | ∅ | 0 | 0 |
| {2,3} | {3} | 1 | -1 |
| {1,2,3} | ∅ | 0 | 0 |

Sum becomes $2 + 2 + 1 - 1 - 1 = 3$.

This confirms that each single flower type is counted exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^n \cdot n \cdot 60 + 2^n \log m)$ | Each subset computes intersections over at most 19 masks and one exponentiation |
| Space | $O(n)$ | Storage for bouquet bitmasks |

With $n \le 19$, the $2^n$ factor is under 600,000, which is comfortably within limits. Each operation inside the loop is simple bit manipulation or modular arithmetic, so the solution fits easily within 3 seconds.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    def modpow(a, e):
        res = 1
        a %= MOD
        while e:
            if e & 1:
                res = res * a % MOD
            a = a * a % MOD
            e >>= 1
        return res

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        masks = []
        for _ in range(n):
            arr = list(map(int, input().split()))
            mask = 0
            for v in arr[1:]:
                mask |= 1 << (v - 1)
            masks.append(mask)

        ans = 0
        for s in range(1, 1 << n):
            inter = (1 << 60) - 1
            for i in range(n):
                if s >> i & 1:
                    inter &= masks[i]
            if inter == 0:
                continue
            cnt = inter.bit_count()
            val = modpow(cnt, m)
            if bin(s).count("1") % 2 == 1:
                ans = (ans + val) % MOD
            else:
                ans = (ans - val) % MOD

        out.append(str(ans % MOD))

    return "\n".join(out)

# provided sample (structure assumed)
assert run("""1
2 2
2 1 2
2 2 3
""") == "7"

# all same bouquet
assert run("""1
3 3
3 1 2 3
3 1 2 3
3 1 2 3
""") == str((3**3) % MOD)

# single bouquet
assert run("""1
1 4
2 1 2
""") == str(pow(2,4,MOD))

# disjoint bouquets
assert run("""1
2 2
1 1
1 2
""") == str((1**2 + 1**2) % MOD)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical bouquets | single correct count | deduplication via inclusion-exclusion |
| one bouquet | $k^m$ baseline | base correctness |
| disjoint sets | simple sum behavior | no overlap correction needed |

## Edge Cases

A case where all bouquets are identical stresses duplicate subset contributions. For input where every bouquet is `{1,2,3}` and $m=5$, every subset has the same intersection size 3. The inclusion-exclusion sum becomes $(1 - (n choose 1) + (n choose 2) - \dots) \cdot 3^5$, which evaluates to exactly $3^5$, confirming that duplicates collapse correctly.

A case with empty intersections appears when bouquets share no common element. For example `{1}`, `{2}`, `{3}` with any $m$. Every subset of size at least 2 has intersection zero and contributes nothing, leaving only singletons, so the result is $1^m + 1^m + 1^m = 3$, which matches the fact that each bouquet only generates one constant sequence.

A larger overlapping structure, such as `{1,2}`, `{2,3}`, `{1,3}`, checks that pairwise overlaps are corrected by triple intersections. The algorithm assigns correct weight to the singleton element 2, 1, and 3 without duplication, since each appears as an intersection of a specific subset family.
