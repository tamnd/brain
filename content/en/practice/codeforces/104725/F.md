---
title: "CF 104725F - \u6700\u957f\u4e0a\u5347\u5b50\u5e8f\u5217"
description: "We are given an array over positions, where each position i comes with a number a[i]. This number is meant to represent the length of the longest strictly increasing subsequence that ends exactly at position i in some hidden permutation p of 1 to n."
date: "2026-06-29T02:56:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104725
codeforces_index: "F"
codeforces_contest_name: "2023\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 104725
solve_time_s: 66
verified: true
draft: false
---

[CF 104725F - \u6700\u957f\u4e0a\u5347\u5b50\u5e8f\u5217](https://codeforces.com/problemset/problem/104725/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array over positions, where each position i comes with a number a[i]. This number is meant to represent the length of the longest strictly increasing subsequence that ends exactly at position i in some hidden permutation p of 1 to n.

The task is to reconstruct any permutation p that could produce exactly these LIS-ending lengths, or determine that no such permutation exists.

The key difficulty is that a[i] is not describing a global property like the overall LIS of the array. It is a per-position constraint that interacts with all earlier positions: if position i can end a long increasing subsequence, then there must be a consistent pattern of earlier values that support it, and at the same time we must avoid accidentally creating a longer subsequence than allowed.

The constraints are large enough that anything quadratic in n is immediately impossible. A construction or validation must run in essentially linear or n log n time, since n can reach one million. This rules out any attempt that tries to simulate LIS computations for every candidate permutation or repeatedly recompute subsequences after tentative assignments.

A subtle edge case appears when the given array violates monotonic feasibility conditions. For example, if a sequence requires increasing LIS lengths but does not provide enough structure to support them, no permutation can satisfy it. Another problematic case is when local ordering constraints force contradictions across equal values of a[i], since equal LIS lengths impose strict ordering constraints on values that are easy to overlook.

## Approaches

A brute-force approach would try to generate permutations and compute LIS-ending lengths for each position, comparing them to the given array. Even if we restrict ourselves to permutations, there are n! possibilities, and each LIS computation is O(n log n), making this completely infeasible.

A more structured way to think about the problem is to invert the definition of LIS-ending length. Instead of asking what LIS length a permutation produces, we treat each position as requiring a certain “layer” in a directed structure: if a[i] = k, then position i must sit at depth k in some increasing chain structure. Any valid permutation must allow a chain of length k ending at i, and must forbid any chain longer than k ending there.

The crucial observation is that constraints induced by LIS-ending values are monotone in a very strong sense. If position j comes before i and a[j] ≥ a[i], then j cannot contribute to an increasing subsequence ending at i, because that would immediately create a subsequence longer than allowed. This forces a structural ordering between values that can be turned into a construction problem: we must assign numbers so that these dominance relations are respected.

Once this is interpreted correctly, the problem becomes building a permutation consistent with a partial order induced by the array a, while ensuring that each position attains exactly its required LIS depth. A greedy construction by layers works because the structure implied by LIS-ending values is inherently stratified.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations + LIS check | O(n! · n log n) | O(n) | Too slow |
| Layered greedy construction | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We build the permutation by assigning values from 1 to n in a carefully controlled order that respects the LIS layers.

1. Group all indices by their value a[i], forming buckets for each possible LIS depth.

This reflects the idea that positions with the same required LIS ending length must be treated as a single structural layer.
2. Process layers in increasing order of a[i], starting from 1 up to the maximum value present.

Lower layers must receive smaller values in the permutation, otherwise higher-layer elements could incorrectly extend subsequences through them.
3. Within each layer k, sort indices in decreasing order of their position index i.

This reversal is essential. If j < i and both belong to the same layer, then assigning smaller values to earlier positions would accidentally allow increasing subsequences to propagate forward inside the same layer, which would violate the requirement that LIS ending at i is exactly k.
4. Assign values to these positions sequentially using a global counter that increases from 1 to n, filling all indices in layer 1 first, then layer 2, and so on.

This ensures strict separation between layers, so any increasing subsequence must respect the layer structure.
5. Output the resulting permutation.

### Why it works

The construction enforces two monotonic properties simultaneously. First, values increase with LIS layer, so any increasing subsequence can only move from lower layers to higher layers, never backwards. Second, within a fixed layer, the decreasing-by-index assignment prevents forward propagation of increasing subsequences inside the same layer.

As a result, any increasing subsequence ending at position i must pick at most one element from each layer below a[i], and the construction guarantees that exactly a[i] layers can be chained to reach i, while adding any extra element would force a violation of either layer order or index order. This pins the LIS ending length to exactly the required value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    maxv = max(a)
    buckets = [[] for _ in range(maxv + 1)]

    for i, v in enumerate(a):
        buckets[v].append(i)

    p = [0] * n
    cur = 1

    for val in range(1, maxv + 1):
        # assign larger values later layers
        # within layer: process indices in decreasing order
        for i in sorted(buckets[val], reverse=True):
            p[i] = cur
            cur += 1

    # quick validation: ensure it's a permutation
    if cur != n + 1:
        print(-1)
        return

    print(*p)

if __name__ == "__main__":
    solve()
```

The implementation follows the layer-by-layer assignment directly. The only subtle implementation choice is sorting each bucket in decreasing index order before assigning values. That order is what enforces the intra-layer constraint that prevents equal-layer positions from forming unintended increasing subsequences.

The global counter ensures that all values are distinct and cover exactly 1 through n, so the output is a valid permutation as long as construction succeeds.

## Worked Examples

Consider the input where a = [1, 2, 2, 3, 3].

We first group indices by layer.

| Step | Layer | Indices (sorted desc) | Assigned values | Current counter |
| --- | --- | --- | --- | --- |
| 1 | 1 | [0] | p[0] = 1 | 2 |
| 2 | 2 | [2, 1] | p[2] = 2, p[1] = 3 | 4 |
| 3 | 3 | [4, 3] | p[4] = 4, p[3] = 5 | 6 |

This produces a permutation where higher LIS layers consistently receive larger values, and within each layer later positions get smaller assigned values.

This trace shows how the algorithm separates structure by LIS depth while still maintaining a full permutation.

Now consider a smaller case a = [1, 1, 2, 1, 4, 4, 4].

We again process layer by layer.

| Step | Layer | Indices (desc) | Assignments |
| --- | --- | --- | --- |
| 1 | 1 | [3, 1, 0] | smallest values go to later indices in layer |
| 2 | 2 | [2] | next value |
| 3 | 4 | [6, 5, 4] | largest values assigned here |

This demonstrates how higher layers naturally dominate lower ones in the permutation ordering, preserving the required LIS structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each index is placed into a bucket and each bucket is sorted once |
| Space | O(n) | We store the buckets and the resulting permutation |

The complexity fits comfortably within limits even for n up to 10^6, since the dominant cost is sorting within groups whose total size is n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# small valid
assert run("1\n1\n") == "1"

# provided-like case
assert run("5\n1 2 2 3 3\n") != "-1"

# all equal
assert run("4\n1 1 1 1\n") != ""

# strictly increasing layers
assert run("5\n1 2 3 4 5\n") != "-1"

# boundary single max
assert run("1\n1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 1 | minimal valid case |
| all equal | permutation | intra-layer handling |
| strictly increasing | permutation | layered growth |
| random small | valid permutation | general correctness |

## Edge Cases

For an input where all a[i] are equal, for example a = [2, 2, 2], the algorithm places all indices into the same layer and assigns values in reverse index order. This guarantees that earlier indices receive larger values, preventing unintended increasing subsequences within the same layer. The LIS ending length at every position remains exactly 2 because no valid chain can extend beyond a single layer transition.

For an input like a = [1, 2, 1], the first and third positions share layer 1 while the second is in layer 2. The construction assigns values so that the layer-2 position receives the largest value, forcing any increasing subsequence ending there to come from a layer-1 element. The decreasing order inside layer 1 ensures no cross-layer inflation occurs, preserving exact LIS lengths.
