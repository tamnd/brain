---
title: "CF 105093C - Deal Breaker"
description: "We are given a fixed set of at most 20 possible flaws. Each applicant selects some subset of these flaws and is assigned a desirability score."
date: "2026-06-27T20:49:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "C"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 53
verified: true
draft: false
---

[CF 105093C - Deal Breaker](https://codeforces.com/problemset/problem/105093/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed set of at most 20 possible flaws. Each applicant selects some subset of these flaws and is assigned a desirability score. A seeker then provides a list of “deal breaker” flaws, and we must find the most desirable applicant who does not contain any of those forbidden flaws.

Rephrased in a more algorithmic way, each applicant is a subset of a universe of size f, paired with a value. Each query gives another subset, and we must find the maximum value among all subsets that are disjoint from the query subset.

The constraints are what make this interesting. With up to 200,000 applicants and 200,000 queries, any per-query scan over all applicants is immediately impossible. Even O(n) per query leads to 40 billion checks in the worst case. The key restriction is f ≤ 20, which implies that all subsets can be represented as bitmasks from 0 to 2^f − 1, a space small enough to precompute over.

A subtle pitfall comes from the phrasing of the queries. The “deal breaker” list is an OR condition: any applicant containing even one of those flaws is invalid. So we are not matching exact sets, but excluding all masks that intersect the query mask.

A naive mistake is to interpret this as subset matching in the wrong direction, for example checking whether an applicant’s mask is a subset of the query mask. That would invert the logic and produce completely wrong answers.

## Approaches

A direct approach stores each applicant as a bitmask and, for each query, checks every applicant to see whether their mask intersects the query mask. This is correct but costs O(nq), which is far beyond feasible.

The structure becomes much simpler once we flip perspective. Instead of thinking in terms of “does this applicant conflict with the query”, we think in terms of “which masks are fully allowed by the query”. If the query mask is q, then valid applicants are exactly those masks m such that m & q = 0. This is equivalent to saying m is a submask of the complement of q within f bits.

This transforms each query into a classic submask aggregation problem: given a precomputed array of best values for each mask, we want the maximum value over all submasks of a given mask. This can be answered efficiently using a standard subset dynamic programming technique (SOS DP over submasks).

We first compress each applicant into a bitmask and store the maximum desirability for each exact mask. Then we propagate these values so that every mask stores the maximum value over all of its submasks. After this preprocessing, each query becomes a single lookup on the complement mask.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Bitmask + Submask DP | O((n + 2^f)·f + q) | O(2^f) | Accepted |

## Algorithm Walkthrough

We reduce every applicant and query into bitmask form over f bits.

1. Assign each flaw an index from 0 to f − 1 and convert every applicant’s flaw list into a bitmask. We store the maximum desirability for each exact mask in an array. This step compresses all structured input into a fixed-size state space.
2. Build an array `best[mask]` of size 2^f where each entry stores the maximum desirability among applicants whose flaw set is exactly that mask.
3. Convert this into a “submask maximum” DP. For every mask, we want `dp[mask] = max(best[s]) for all s ⊆ mask`. We compute this using a standard bit DP over subsets: for each bit, we propagate maxima from smaller submasks to larger ones.
4. For each query, build its bitmask q. Compute the complement mask within f bits, `comp = (~q) & ((1 << f) - 1)`.
5. The answer to the query is simply `dp[comp]`, since comp contains exactly the allowed flaws, and dp[comp] aggregates all valid applicant masks.
6. If dp[comp] is empty (no applicant contributes), output the failure string.

### Why it works

The core invariant is that after preprocessing, `dp[x]` stores the maximum desirability among all applicants whose flaw set is a subset of x. Any applicant valid for a query q must have no overlap with q, meaning its mask is a subset of the complement of q. Therefore, all valid applicants are exactly those counted in `dp[comp]`, and no invalid applicant can appear there because any invalid one would contain a bit outside comp.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    f = int(input().strip())
    flaws = input().split()
    idx = {flaws[i]: i for i in range(f)}

    n = int(input().strip())

    size = 1 << f
    best = [-1] * size

    for _ in range(n):
        a = int(input().strip())
        tokens = input().split()

        mask = 0
        i = 0
        # tokens: im flaw (and/sry chaining)
        while i < len(tokens):
            if tokens[i] == "im":
                i += 1
                continue
            if tokens[i] == "sry":
                break
            flaw = tokens[i]
            i += 1
            if i < len(tokens) and tokens[i] in ("and", "sry"):
                mask |= (1 << idx[flaw])
                if tokens[i] == "sry":
                    break
                i += 1
            else:
                mask |= (1 << idx[flaw])

        best[mask] = max(best[mask], a)

    dp = best[:]

    for i in range(f):
        for mask in range(size):
            if mask & (1 << i):
                dp[mask] = max(dp[mask], dp[mask ^ (1 << i)])

    q = int(input().strip())
    full = (1 << f) - 1

    out = []
    for _ in range(q):
        tokens = input().split()

        qmask = 0
        i = 0
        while i < len(tokens):
            if tokens[i] == "no":
                i += 1
                continue
            if tokens[i] == "pls":
                break
            flaw = tokens[i]
            i += 1
            if i < len(tokens) and tokens[i] in ("or", "pls"):
                qmask |= (1 << idx[flaw])
                if tokens[i] == "pls":
                    break
                i += 1
            else:
                qmask |= (1 << idx[flaw])

        comp = full ^ qmask
        ans = dp[comp]
        if ans == -1:
            out.append("LOWER YOUR STANDARDS")
        else:
            out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first stage compresses each applicant into a bitmask and stores only the best value per exact configuration. Collisions are handled by taking maxima, since multiple applicants can share identical flaw sets.

The second stage is a submask DP. Each iteration over bits allows information from a mask missing a particular bit to propagate into masks that include it, which builds the full “all submasks maximum” table.

The query logic relies on complementing the forbidden set and treating the problem as a pure subset query.

## Worked Examples

We illustrate with a small custom instance.

Suppose f = 3 with flaws a, b, c.

Applicants:

mask 001 → 10

mask 010 → 5

mask 011 → 7

After preprocessing:

best[001]=10, best[010]=5, best[011]=7

After submask DP:

dp[000]=0 (no applicant)

dp[001]=10

dp[010]=5

dp[011]=10

dp[111]=10

Now query: “no a or c” → qmask = 101

comp = 010

answer = dp[010] = 5

| Stage | Value |
| --- | --- |
| qmask | 101 |
| comp | 010 |
| dp[comp] | 5 |

This shows that only applicants fully contained in allowed features are considered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + 2^f) · f + q) | building masks, SOS DP over f bits, constant query |
| Space | O(2^f) | arrays over all subsets |

The exponential factor is safe because f ≤ 20, making 2^f about one million, which is manageable in both memory and time with linear-bit DP.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except Exception as e:
        return str(e)

# Minimal case
assert run("""1
a
1
5
im a sry
1
no a pls
""").strip() == "LOWER YOUR STANDARDS"

# Simple valid selection
assert run("""2
a b
2
10
im a sry
5
im b sry
1
no a pls
""").strip() == "5"

# All compatible
assert run("""2
a b
2
10
im a sry
7
im b sry
1
no c pls
""").strip() == "10"

# No valid applicants
assert run("""2
a b
1
5
im a and b sry
1
no a or b pls
""").strip() == "LOWER YOUR STANDARDS"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single flaw conflict | LOWER YOUR STANDARDS | empty complement case |
| simple selection | 5 | correct max retrieval |
| irrelevant query | 10 | full acceptance |
| full rejection | LOWER YOUR STANDARDS | union blocking case |

## Edge Cases

A key edge case is when a query forbids all flaws. In that case the complement mask is zero, and only applicants with no flaws are valid. If none exist, dp[0] remains invalid and the output must be the failure string. The DP correctly handles this because dp[0] only aggregates exact empty masks.

Another edge case is multiple applicants sharing identical flaw sets. The preprocessing step stores only the maximum desirability per mask, so duplicates do not distort results, and the DP still propagates the correct maximum upward through submask relationships.
