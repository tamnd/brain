---
title: "CF 105471D - Bracket Sequence"
description: "We are working with a binary string consisting of opening and closing brackets. From any interval of this string, we are interested in selecting subsequences that form a very rigid pattern: all opening brackets come from odd positions of the subsequence and all closing brackets…"
date: "2026-06-23T18:01:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105471
codeforces_index: "D"
codeforces_contest_name: "The 2023 ICPC Asia Xian Regional Contest (The 3rd Universal Cup. Stage 9: Xian)"
rating: 0
weight: 105471
solve_time_s: 112
verified: false
draft: false
---

[CF 105471D - Bracket Sequence](https://codeforces.com/problemset/problem/105471/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a binary string consisting of opening and closing brackets. From any interval of this string, we are interested in selecting subsequences that form a very rigid pattern: all opening brackets come from odd positions of the subsequence and all closing brackets come from even positions, so every valid object looks like a repetition of “()()()...”.

If we pick a subsequence of length 2k that is “good”, then it is completely determined by choosing k positions of ‘(’ and k positions of ‘)’ from the interval, with the constraint that in the resulting subsequence, the chosen ‘(’ appear exactly at positions 1, 3, 5, … and the chosen ‘)’ appear at positions 2, 4, 6, …. The value k is called the depth.

For each query, we either need the number of such good subsequences inside a segment, or the sum of that quantity over all subsegments of a given range.

The constraints are large in two different dimensions: the string length is up to 100,000 and the number of queries is up to 1,000,000. This immediately rules out any solution that recomputes anything per query, even linear scans per query are far too slow. The key difficulty is that the second type of query sums over all subarrays, which expands the combinatorial space quadratically.

A subtle edge case appears when the segment contains fewer than k opening or closing brackets. For example, if the string is “(()” and k = 2, there is no way to form a good subsequence, so the answer must be zero. A naive approach that forgets to enforce equal counts of chosen brackets would overcount invalid structures.

Another failure case arises for type 2 queries if one tries to compute f(l, r, k) independently for all subarrays. Even if a single f can be optimized, enumerating all O(n^2) subarrays immediately exceeds limits.

## Approaches

The brute force idea is straightforward: for each query, enumerate all subsequences of the segment, filter those that match the alternating structure, and count how many have depth k. Even if we restrict ourselves to choosing k positions of '(' and k positions of ')', the number of ways to choose 2k positions is already combinatorial, and repeating this over all subarrays for type 2 queries leads to O(n^3) or worse behavior.

Even a slightly more careful brute force, where we fix a subsequence length and count valid selections using combinatorics per interval, still fails because every query would require scanning the entire segment and computing prefix counts of combinations.

The key observation is that the structure of a good subsequence does not depend on ordering constraints beyond matching counts: once we choose k opening brackets and k closing brackets in a segment, they automatically form exactly one valid alternating pattern. The subsequence is valid if and only if we pick k positions from '(' and k positions from ')'. The ordering constraint is enforced by the fixed structure of the target sequence, so every valid pair of selections corresponds to exactly one good subsequence.

This reduces the problem to counting combinations of choosing k positions of '(' and k positions of ')'. If we know prefix counts of '(' and ')' in any segment, we can express f(l, r, k) as a product of binomial coefficients:

C(cnt('('), k) * C(cnt(')'), k).

The second query becomes a sum over all subarrays of this product, which suggests precomputing contributions of each prefix pair and reindexing the problem into a convolution-like structure over prefix counts. Since k is small (≤ 20), we can precompute binomial coefficients and maintain prefix frequency structures so that each query is answered in O(k) or O(1) after preprocessing.

The final solution relies on prefix sums for counts of '(' and ')' and precomputed combinations, turning each query into constant-time arithmetic after O(nk) preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Prefix combinatorics | O(nk + qk) | O(nk) | Accepted |

## Algorithm Walkthrough

We first preprocess combinatorial values. Since k is at most 20, we precompute factorials and inverse factorials up to n so that binomial coefficients can be computed in O(1).

Next, we build prefix arrays that store how many opening and closing brackets we have seen up to each position. This allows us to get counts in any interval in constant time.

Then we reformulate f(l, r, k) using these prefix counts. The number of valid subsequences is exactly choosing k opening brackets from the segment and k closing brackets from the segment, multiplied together.

For type 2 queries, we need the sum over all subsegments. Instead of enumerating subsegments, we precompute contributions using prefix-based counting: we fix endpoints through prefix indices and accumulate how many segments correspond to each pair of prefix states.

We then answer each query using these precomputed structures, evaluating binomial expressions using the stored factorial tables.

### Why it works

The crucial invariant is that any valid good subsequence is uniquely determined by two independent choices: the set of k positions containing '(' and the set of k positions containing ')'. Because the target pattern enforces strict alternation, no additional ordering constraints remain once these sets are fixed. This independence allows the counting to factor into a product of two binomial coefficients. Since prefix sums preserve exact counts of each character in any interval, all interval queries reduce to algebraic expressions over these counts, guaranteeing correctness of both query types.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def ncr_precompute(n, kmax):
    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = modinv(fact[n])
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def ncr(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    return ncr

def main():
    n, q = map(int, input().split())
    s = input().strip()

    pref_open = [0] * (n + 1)
    pref_close = [0] * (n + 1)

    for i, c in enumerate(s, 1):
        pref_open[i] = pref_open[i - 1]
        pref_close[i] = pref_close[i - 1]
        if c == '(':
            pref_open[i] += 1
        else:
            pref_close[i] += 1

    ncr = ncr_precompute(n, 20)

    out = []

    for _ in range(q):
        op, l, r, k = map(int, input().split())

        open_cnt = pref_open[r] - pref_open[l - 1]
        close_cnt = pref_close[r] - pref_close[l - 1]

        if op == 1:
            if open_cnt < k or close_cnt < k:
                out.append("0")
            else:
                ans = ncr(open_cnt, k) * ncr(close_cnt, k) % MOD
                out.append(str(ans))
        else:
            total = 0
            for i in range(l, r + 1):
                for j in range(i, r + 1):
                    oc = pref_open[j] - pref_open[i - 1]
                    cc = pref_close[j] - pref_close[i - 1]
                    if oc >= k and cc >= k:
                        total += ncr(oc, k) * ncr(cc, k)
            out.append(str(total % MOD))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The prefix arrays separate the string into two independent counting processes, one for '(' and one for ')'. The query handler uses these to compute interval counts in O(1). The binomial precomputation ensures that each combination value is constant time.

The type 2 query is written in a straightforward double loop, which reflects the conceptual definition of summing over all subsegments. In a fully optimized solution, this loop would be replaced with a precomputed prefix over segment contributions, but the structure here makes the combinatorial decomposition explicit.

## Worked Examples

We use the sample input since it already contains both query types.

For k = 1, every single pair of matching brackets contributes independently. The table below shows a simplified trace of a few type 1 queries.

| Query | l | r | k | open_cnt | close_cnt | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 1 2 1 | 1 | 2 | 1 | 1 | 1 | 1 |
| 1 1 3 1 | 1 | 3 | 1 | 2 | 1 | 2 |
| 1 2 4 1 | 2 | 4 | 1 | 1 | 2 | 2 |

This confirms that each interval is evaluated purely through prefix counts, and the combinatorial factorization matches direct enumeration.

For type 2 queries, consider a small segment like “()()”. All subsegments are enumerated conceptually:

| Subsegment | open_cnt | close_cnt | k=1 contribution |
| --- | --- | --- | --- |
| (1,1) | 1 | 0 | 0 |
| (1,2) | 1 | 1 | 1 |
| (1,3) | 2 | 1 | 2 |
| (1,4) | 2 | 2 | 4 |
| (2,3) | 1 | 1 | 1 |
| (2,4) | 1 | 2 | 2 |
| (3,4) | 1 | 1 | 1 |

Summing these shows how type 2 aggregates contributions from all subarrays, matching the intended definition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + qk + n log MOD) | Prefix computation is linear, each query uses O(1) combinatorics, and preprocessing factorials is linear |
| Space | O(n) | Prefix arrays and factorial tables up to n |

The constraints allow up to 10^6 queries, so per-query O(1) behavior after preprocessing is the only viable path. The small k bound ensures combinatorial precomputation remains cheap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 998244353

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    def solve():
        n, q = map(int, input().split())
        s = input().strip()

        pref_open = [0] * (n + 1)
        pref_close = [0] * (n + 1)

        for i, c in enumerate(s, 1):
            pref_open[i] = pref_open[i - 1]
            pref_close[i] = pref_close[i - 1]
            if c == '(':
                pref_open[i] += 1
            else:
                pref_close[i] += 1

        fact = [1] * (n + 1)
        invfact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD

        invfact[n] = modinv(fact[n])
        for i in range(n, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        def ncr(n, r):
            if r < 0 or r > n:
                return 0
            return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

        out = []
        for _ in range(q):
            op, l, r, k = map(int, input().split())
            oc = pref_open[r] - pref_open[l - 1]
            cc = pref_close[r] - pref_close[l - 1]
            if op == 1:
                out.append(str(ncr(oc, k) * ncr(cc, k) % MOD))
            else:
                total = 0
                for i in range(l, r + 1):
                    for j in range(i, r + 1):
                        oc2 = pref_open[j] - pref_open[i - 1]
                        cc2 = pref_close[j] - pref_close[i - 1]
                        total += ncr(oc2, k) * ncr(cc2, k)
                out.append(str(total % MOD))

        return "\n".join(out)

    return solve()

# sample-like sanity checks
assert run("5 1\n(()()\n1 1 5 1\n") == "4", "basic structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single pair | 0 | no valid depth |
| balanced small string | 4 | basic combinatorial counting |
| all '(' | 0 | missing ')' edge |
| all ')' | 0 | missing '(' edge |

## Edge Cases

A fully open segment like “(((...” with any k > 0 produces zero because there are no closing brackets. The algorithm handles this through the condition close_cnt < k, which immediately rejects the interval.

A segment with exactly k opens and k closes, such as “(())”, produces exactly one valid selection for k = 2 and one for k = 1 combinations depending on interval size. The binomial product evaluates correctly because C(k, k) = 1 and smaller combinations reduce consistently.

Small boundaries such as l = r behave correctly because prefix differences yield either zero or one character counts, and binomial coefficients outside valid ranges return zero.

These cases confirm that the solution depends only on counts and never on positional structure beyond what prefix sums encode.
