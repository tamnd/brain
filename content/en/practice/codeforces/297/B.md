---
title: "CF 297B - Fish Weight"
description: "We are given two people, Alice and Bob, each of whom has caught a collection of fish. Every fish belongs to one of k species, and species numbers are ordered so that species with a larger index are guaranteed to be at least as heavy as those with a smaller index."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 297
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 180 (Div. 1)"
rating: 1600
weight: 297
solve_time_s: 62
verified: true
draft: false
---

[CF 297B - Fish Weight](https://codeforces.com/problemset/problem/297/B)

**Rating:** 1600  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two people, Alice and Bob, each of whom has caught a collection of fish. Every fish belongs to one of k species, and species numbers are ordered so that species with a larger index are guaranteed to be at least as heavy as those with a smaller index. What we do not know are the actual weights, only that they respect this monotonic ordering and can be any positive real numbers consistent with it.

Alice and Bob each have multisets of species labels. The task is not to compute an actual numeric comparison, but to decide whether there exists some assignment of weights to species, consistent with the ordering constraint, such that Alice’s total weight is strictly larger than Bob’s total weight.

So the question is fundamentally about whether we can “tune” the gaps between consecutive species weights to make Alice win, given only counts of each species on both sides.

The constraints are large: up to 100,000 fish per person and up to 1,000,000,000 species labels. This immediately rules out anything that depends on iterating over all species or simulating weights explicitly. Any viable solution must reduce the problem to operations on the input frequencies alone, in linear time.

A naive pitfall appears when one assumes that comparing counts of species is enough. For example, if Alice has fewer high-index fish but more low-index fish, it is tempting to conclude she cannot win. That is wrong because the weight gaps can be made arbitrarily large. Conversely, even if Alice has many high-index fish, Bob might still dominate if he has enough flexibility in lower indices.

A subtle edge case arises when Alice’s fish are a subset of Bob’s. For instance, Alice: [2, 2], Bob: [1, 1, 2, 2]. Even though Alice has only higher or equal species, Bob can always assign weights to keep parity or advantage, making Alice unable to strictly win. Any solution that ignores multiplicity and only considers set inclusion fails here.

## Approaches

A direct brute-force approach would try to assign concrete weights to each species while respecting monotonicity and test whether Alice can exceed Bob. This transforms into a feasibility problem over k variables with n + m linear contributions. Even if we restrict weights to integers in a bounded range, the search space is exponential, since each ordering allows infinitely many valid weight assignments.

The key observation is that only the ordering of fish matters, and the actual values can be chosen adversarially to favor or disfavor Alice. This means we are dealing with a linear inequality over a chain-structured variable system: w1 ≤ w2 ≤ ... ≤ wk.

We can rewrite the total difference as a sum over species counts:

Alice contributes cntA[i] and Bob contributes cntB[i]. The total difference is ∑ (cntA[i] − cntB[i]) * w[i]. The goal is to check if there exists a non-decreasing sequence w such that this sum is strictly positive.

This is a classical “choose monotone weights to maximize a linear form” problem. The optimal strategy is to push weight differences only where they matter, but monotonicity forces a structure: increasing weight at a later index also increases all previous ones indirectly.

This reduces to a greedy prefix analysis. We simulate how the difference accumulates when we move from small species to large species, maintaining the worst possible accumulated contribution under monotonic constraints. The decision becomes whether we can arrange weights so that Alice’s advantage can be concentrated in a suffix that is not canceled by earlier deficits.

The final simplification is that only prefix balances matter: if at every prefix Bob is not strictly dominating in a way that cannot be compensated later, then a construction exists. This reduces the problem to tracking cumulative differences and checking whether there exists a suffix where Alice can “turn the tide”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential / infeasible | O(k) | Too slow |
| Optimal | O(n + m) | O(k) or O(unique values) | Accepted |

## Algorithm Walkthrough

We compress the problem into counting how many fish of each species Alice and Bob have. Since k is large, we only store counts only for species appearing in input.

We then compute a net balance array over sorted species indices, where each position stores Alice count minus Bob count.

The algorithm proceeds as follows.

1. Count occurrences of each species for Alice and Bob separately. This converts the input lists into frequency maps.
2. Extract all species that appear in either list and sort them by index. The ordering is critical because weights must respect species order.
3. Build an array of net differences at each species: positive means Alice has more fish of that species, negative means Bob has more.
4. Traverse species in increasing order while maintaining a running cumulative balance. This represents how much advantage Alice has accumulated if weights were equal so far.
5. Track the minimum prefix balance. This captures how bad the situation gets before we potentially exploit larger species weights.
6. If at any point the structure allows a suffix to dominate earlier deficits, meaning the minimum prefix does not lock Alice into permanent loss, then answer is YES.
7. Otherwise, conclude that no monotone assignment can make Alice’s sum strictly larger.

The key reason this traversal works is that increasing weights later in the sequence can only amplify differences from higher indices. If Alice can survive early prefixes without being irreparably behind, we can amplify higher species weights enough to flip the total sum.

### Why it works

The algorithm relies on viewing the total difference as a linear combination over a non-decreasing sequence. The cumulative prefix balance captures all constraints imposed by earlier weights, since any increase in later weights must respect earlier ordering. If at some prefix Bob’s advantage is so strong that no future monotone scaling can offset it, that prefix minimum becomes a barrier. Conversely, if no such irreversible barrier exists, we can always choose a sufficiently steep growth in weights to favor Alice in later indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    cntA = {}
    cntB = {}

    for x in A:
        cntA[x] = cntA.get(x, 0) + 1
    for x in B:
        cntB[x] = cntB.get(x, 0) + 1

    species = sorted(set(cntA.keys()) | set(cntB.keys()))

    balance = 0
    min_prefix = 0

    for s in species:
        balance += cntA.get(s, 0) - cntB.get(s, 0)
        min_prefix = min(min_prefix, balance)

    # If Alice ever has a "controllable positive drift", she can win
    # otherwise Bob's early dominance is irreversible
    print("YES" if balance - min_prefix > 0 else "NO")

if __name__ == "__main__":
    solve()
```

The solution begins by compressing the input into frequency dictionaries so we only reason about species that actually appear. This avoids iterating up to k, which can be up to 10^9.

We then sort the relevant species, since monotonicity constraints are tied strictly to the ordering of indices. The traversal computes prefix sums of net advantage. The variable balance represents the current cumulative difference between Alice and Bob assuming unit weights. The minimum prefix tracks the deepest deficit relative to earlier prefixes.

The condition `balance - min_prefix > 0` captures whether there exists a way to amplify later species weights enough to overcome earlier losses. If this value is positive, Alice can be made to win strictly.

## Worked Examples

### Example 1

Input:

```
3 3 3
2 2 2
1 1 3
```

We compute counts:

| Step | Species | cntA | cntB | balance | min_prefix |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | -2 | -2 |
| 2 | 2 | 3 | 0 | 1 | -2 |
| 3 | 3 | 0 | 1 | 0 | -2 |

Final value is balance − min_prefix = 0 − (−2) = 2 > 0, so answer is YES.

This shows that even though Alice is not dominant everywhere, she can concentrate weight on species 2 to outweigh Bob’s advantage in species 1 and 3.

### Example 2

Input:

```
2 4 3
2 2
1 1 2 2
```

| Step | Species | cntA | cntB | balance | min_prefix |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | -2 | -2 |
| 2 | 2 | 2 | 2 | -2 | -2 |

Final value is -2 − (-2) = 0, so answer is NO.

This confirms that when Alice is fully contained within Bob’s multiset structure, no monotone weighting can produce a strict advantage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log(n + m)) | counting plus sorting distinct species |
| Space | O(n + m) | frequency maps store only seen species |

The constraints allow up to 200,000 total fish entries, so this linearithmic solution fits comfortably within time limits. Memory usage remains proportional to distinct species in input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n, m, k = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    cntA = defaultdict(int)
    cntB = defaultdict(int)

    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    species = sorted(set(cntA) | set(cntB))

    balance = 0
    min_prefix = 0

    for s in species:
        balance += cntA[s] - cntB[s]
        min_prefix = min(min_prefix, balance)

    return "YES" if balance - min_prefix > 0 else "NO"

# provided sample
assert run("""3 3 3
2 2 2
1 1 3
""") == "YES"

# Bob dominates early and ties later
assert run("""2 4 3
2 2
1 1 2 2
""") == "NO"

# Alice strictly dominates one species
assert run("""1 1 5
5
1
""") == "YES"

# identical multisets
assert run("""3 3 4
1 2 3
1 2 3
""") == "NO"

# large skew
assert run("""5 1 10
10 10 10 10 10
1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical multisets | NO | equality cannot produce strict win |
| single heavy fish | YES | suffix dominance |
| Bob-heavy prefix | NO | irreversible early deficit |
| extreme skew | YES | amplification via monotonic weights |

## Edge Cases

A key edge case is when both players have identical multisets. The algorithm computes balance as zero everywhere, and the minimum prefix is also zero, yielding zero difference. Since strict inequality is required, the condition fails correctly.

Another case is when Alice has only the highest species while Bob has only the lowest. The prefix sum becomes strongly negative early but eventually becomes positive, and the difference between final balance and minimum prefix becomes positive, correctly identifying that weights can be stretched to favor Alice.

The most subtle situation is when Alice leads only in low indices but Bob leads in a single high index. The prefix minimum captures Bob’s early dominance, and the final check ensures that no later amplification can override a sufficiently large earlier deficit, preventing false positives.
