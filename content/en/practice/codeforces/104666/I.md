---
title: "CF 104666I - Ponk Warshall"
description: "We are given two strings of equal length over the alphabet {A, C, G, T}. The second string is a permutation of the first, meaning both contain exactly the same multiset of characters."
date: "2026-06-29T09:55:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104666
codeforces_index: "I"
codeforces_contest_name: "2019-2020 ICPC Central Europe Regional Contest (CERC 19)"
rating: 0
weight: 104666
solve_time_s: 73
verified: false
draft: false
---

[CF 104666I - Ponk Warshall](https://codeforces.com/problemset/problem/104666/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings of equal length over the alphabet {A, C, G, T}. The second string is a permutation of the first, meaning both contain exactly the same multiset of characters. The task is to transform the first string into the second using swaps, where each swap exchanges two arbitrary positions in the string.

The goal is to compute the minimum number of such swaps required.

A useful way to reframe the problem is to think of aligning positions rather than characters. Each position in the first string must eventually “send” its character to some position in the second string that expects it. This creates a permutation of indices, and the question becomes: what is the minimum number of swaps needed to realize this permutation starting from the identity arrangement.

The constraints allow the string length up to 10^6, which immediately rules out any quadratic or even $O(n \log n)$ approach that relies on explicit cycle reconstruction with heavy bookkeeping. Any solution must be linear time and essentially single pass with constant work per character.

A subtle but important edge case is when characters repeat heavily. For example, if both strings are identical, the answer is zero, and any algorithm that builds mismatched mappings must correctly handle empty structures. Another edge case is when the permutation consists of long cycles. For instance, a cyclic shift of the entire string produces a single cycle of length n, and the answer should be n−1. Any greedy local mismatch fixing approach that does not recognize cycles will underestimate or overcount in such cases.

## Approaches

A naive viewpoint is to repeatedly scan the string, find a position where the current string differs from the target, and swap it with the position that contains the needed character. This is correct because each swap can fix at least one misplaced character. However, the cost of locating the correct partner position repeatedly leads to quadratic behavior. In the worst case, each of n positions may require scanning another O(n) segment, leading to O(n²) operations, which is infeasible for n up to 10^6.

The key structural observation is that swaps act on cycles in a hidden permutation between positions. If we fix a mapping from each position in the first string to the position in the second string where that character should go, then we obtain a permutation of indices. Every swap merges or breaks cycles in a predictable way, and the minimum number of swaps to sort a permutation is determined entirely by its cycle decomposition.

Each cycle of length k requires exactly k−1 swaps to be fixed optimally. This reduces the problem to identifying cycles in the position mapping and summing their contributions.

The only complication is efficiently constructing the mapping under repeated characters. Since letters are not unique, we cannot directly map by value. Instead, we match occurrences using queues: for each character, store the indices where it appears in the target string, then assign occurrences from the source string to these positions in order.

Once the mapping is built, the rest is standard cycle counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy local swaps with searching | O(n²) | O(n) | Too slow |
| Cycle decomposition via matching | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the permutation induced by aligning characters from the first string to the second.

1. For each character in the target string, store a queue of its indices. This prepares deterministic matching for duplicates, since identical letters must be matched in order to preserve feasibility.
2. Traverse the source string from left to right. For each character, assign it to the earliest unused position from the corresponding queue in the target. This builds an array `to[i]` meaning the character at position i in the source must go to position `to[i]` in the target.
3. We now interpret `to` as a permutation on indices from 0 to n−1. The task becomes finding the minimum number of swaps to realize this permutation.
4. Mark all positions unvisited, then iterate through indices. When we find an unvisited index, we traverse its cycle by repeatedly following `to[i]` until we return to a visited node.
5. For each cycle of length k, add k−1 to the answer. This corresponds to the fact that a cycle can be fixed by repeatedly swapping one element into its final position, reducing the cycle size by one each time.

### Why it works

The constructed mapping is a bijection because both strings have identical character multisets and each occurrence is used exactly once. Thus `to` decomposes into disjoint cycles covering all indices. Any swap between two positions can reduce the number of cycles or merge them, but cannot reduce the total required swaps below the sum of (cycle length − 1). Since each cycle is independent, and we can explicitly fix each cycle in k−1 swaps, the result is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()
    n = len(s)

    pos = {'A': [], 'C': [], 'G': [], 'T': []}
    for i, ch in enumerate(t):
        pos[ch].append(i)

    ptr = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    to = [0] * n

    for i, ch in enumerate(s):
        to[i] = pos[ch][ptr[ch]]
        ptr[ch] += 1

    vis = [False] * n
    ans = 0

    for i in range(n):
        if vis[i]:
            continue
        cur = i
        size = 0
        while not vis[cur]:
```
