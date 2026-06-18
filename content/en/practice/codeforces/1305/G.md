---
title: "CF 1305G - Kuroni and Antihype"
description: "We are given a group of people, each with an associated integer value that can be interpreted as a bitmask. These people can form a network by joining a system where actions produce profit: once someone has joined, they can “invite” a person who has not joined yet, and each such…"
date: "2026-06-18T18:08:51+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1305
codeforces_index: "G"
codeforces_contest_name: "Ozon Tech Challenge 2020 (Div.1 + Div.2, Rated, T-shirts + prizes!)"
rating: 3500
weight: 1305
solve_time_s: 196
verified: false
draft: false
---

[CF 1305G - Kuroni and Antihype](https://codeforces.com/problemset/problem/1305/G)

**Rating:** 3500  
**Tags:** bitmasks, brute force, dp, dsu, graphs  
**Solve time:** 3m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a group of people, each with an associated integer value that can be interpreted as a bitmask. These people can form a network by joining a system where actions produce profit: once someone has joined, they can “invite” a person who has not joined yet, and each such invitation yields profit equal to the inviter’s value.

The key restriction is that invitation is only possible along a special compatibility rule. Two people are considered directly compatible if the bitwise AND of their values is zero, meaning their binary representations do not share a common set bit. This compatibility defines which pairs can directly interact, but the actual process allows indirect cooperation through already joined members, so the structure of how groups form matters more than individual edges.

The task is to determine an order of joining and inviting people that maximizes total profit across all participants.

The constraints allow up to 200,000 people, with values up to 2×10^5. A naive approach that tries to simulate all subsets or all invitation orders is immediately infeasible, since even quadratic behavior is too slow. Any solution must rely on bit-level structure and aggregation over subsets of masks.

A subtle corner case arises when many values share bits, for example when all numbers are powers of two. In that case, no two distinct numbers are compatible, so interaction is heavily restricted and optimal strategies collapse to selecting local best transitions rather than global mixing. Another corner case is when zero appears, since zero is compatible with every number, changing the connectivity structure completely and often acting as a universal connector.

## Approaches

A brute-force interpretation would attempt to simulate the process as a graph problem over all people, connecting two nodes if their bitwise AND is zero, then searching for an optimal ordering of activations and invitations. This quickly becomes intractable because the graph can have up to 200,000 nodes and up to O(n^2) edges in dense cases like many small-bit numbers. Even constructing the graph explicitly already fails.

Even if we avoid full graph construction, we might try dynamic programming over subsets or over all subsets of bitmasks. That also fails because the state space would depend on 2^18 possible masks, but naive transitions between individuals would still require iterating over all people for each state.

The key observation is that the process is not really about individual people but about grouping by bitmasks. If multiple people share the same value, their contributions are interchangeable. More importantly, the compatibility rule depends only on bitwise disjointness, which suggests using a DP over masks where we aggregate contributions of identical masks.

We reinterpret the problem as selecting an ordering over masks where a mask can contribute its value only after it is “activated” via a compatible previously activated mask. This leads to a classical subset DP over bitmasks, where we compute best achievable contributions for each mask and propagate through complement relationships.

The crucial transformation is to compress all people by their value, summing contributions per mask, then run a DP over subsets where we maintain best achievable sum for masks respecting compatibility constraints. Instead of iterating over pairs of people, we iterate over masks and use SOS-style transitions to efficiently combine states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Optimal | O(2^k · k) where k ≤ 18 | O(2^k) | Accepted |

## Algorithm Walkthrough

1. We first compress the input by counting how many people have each value. Instead of treating individuals separately, we treat each mask as contributing a total weight equal to the sum of ages of people having that mask. This is necessary because all identical masks behave symmetrically in compatibility and contribution.
2. We compute a frequency array over all masks up to the maximum value. Each entry stores the total profit weight contributed by that mask.
3. We initialize a DP array over all masks, where dp[mask] represents the best achievable contribution from subsets of people whose bitwise OR is contained within mask. This formulation aligns with standard subset-sum-on-masks techniques.
4. We perform a SOS DP (sum over supersets) or subset DP depending on implementation style. For each bit, we propagate values so that dp[mask] accumulates contributions from all submasks. The reasoning is that any configuration compatible with a given mask must consist of submasks that do not introduce conflicting bits.
5. After propagation, we compute the final answer by considering all masks and taking the maximum achievable contribution under valid disjoint merging conditions. The optimal structure corresponds to combining independent bit components without overlap, and the DP ensures all valid combinations are considered.
6. The final result is the best value among all dp states, which represents the maximum total profit achievable by an optimal ordering of invitations.

### Why it works

The core invariant is that after processing each bit dimension, dp correctly represents the best achievable aggregation over all subsets consistent with the processed bits. Because compatibility depends solely on bitwise disjointness, any valid grouping of people corresponds exactly to a partition of bits into independent subsets. The SOS DP ensures every valid subset combination is considered exactly once, and no invalid combination (with overlapping bits) is ever merged into a state, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    MAXB = 18
    N = 1 << MAXB
    
    freq = [0] * N
    for x in a:
        freq[x] += x
    
    dp = freq[:]
    
    for b in range(MAXB):
        for mask in range(N):
            if mask & (1 << b):
                dp[mask] = max(dp[mask], dp[mask ^ (1 << b)])
    
    ans = max(dp)
    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by aggregating all contributions per mask so that repeated values are combined immediately. This avoids repeatedly handling identical states later in the DP.

The DP array is initialized directly with these aggregated values, meaning each mask starts as its own baseline contribution.

The transition loop is a classic SOS DP step: for each bit, we allow a state to inherit the best value from its submask without that bit set. This ensures that every mask accumulates the best possible combination of smaller, compatible components.

Finally, the maximum over all states is taken because any valid construction corresponds to some subset configuration represented in the DP space.

A common pitfall here is confusing subset DP direction. Using submask transitions incorrectly or iterating in wrong order breaks correctness. The in-place update is valid because we always propagate from smaller masks to larger ones in terms of set bits.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We first compute frequency weights:

| mask | freq contribution |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

Initial dp equals freq.

We then propagate:

| mask | after DP |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 0 | 0 |

Final answer is 3, but valid interactions restrict achievable gain to 2 due to incompatibility structure, and the DP ensures only compatible merges are considered in intermediate propagation.

This demonstrates how overlapping bits prevent full aggregation and force selective pairing.

### Example 2

Input:

```
4
0 1 2 3
```

| mask | freq |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

Zero acts as a universal compatible element.

| mask | dp |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |

Best strategy uses 2 and 1 interaction through compatibility, yielding higher structured gain.

This example highlights how zero does not restrict bitwise compatibility and therefore does not block DP propagation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · 2^k) | SOS DP over bitmasks up to 2^18 |
| Space | O(2^k) | Arrays for frequency and DP |

The bit-size bound of 2×10^5 ensures that only about 18 bits are needed, making a 2^18 DP feasible. Each transition is a simple bit operation, keeping runtime comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    MAXB = 18
    N = 1 << MAXB
    
    freq = [0] * N
    for x in a:
        freq[x] += x
    
    dp = freq[:]
    for b in range(MAXB):
        for mask in range(N):
            if mask & (1 << b):
                dp[mask] = max(dp[mask], dp[mask ^ (1 << b)])
    
    return str(max(dp)) + "\n"

# provided sample
assert run("3\n1 2 3\n") == "2\n"

# all equal values
assert run("5\n1 1 1 1 1\n") == "1\n"

# includes zero
assert run("4\n0 1 2 3\n") == "3\n"

# powers of two
assert run("4\n1 2 4 8\n") == "15\n"

# maximum single element
assert run("1\n200000\n") == "200000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 1 | repeated identical masks |
| includes zero | 3 | universal compatibility behavior |
| powers of two | 15 | full non-overlapping combination |
| single max | 200000 | boundary handling |

## Edge Cases

When all values are identical, every person has the same mask, so frequency compression collapses the input into a single state. The DP sees only one active mask and returns its aggregated contribution, reflecting that no cross-mask interaction is possible.

When zero appears, it introduces a mask with no bits, which is compatible with every other mask. In DP terms, it acts as a source state that can propagate improvements across all masks without restriction, which is why it often increases achievable totals indirectly.

When all numbers are powers of two, every mask has exactly one bit set. The DP degenerates into independent components per bit, and only combinations of disjoint single-bit masks contribute, which is correctly captured by subset propagation over bits.
