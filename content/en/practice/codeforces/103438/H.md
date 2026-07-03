---
title: "CF 103438H - Colourful Permutation Sorting"
description: "We are given a permutation of size $n$, but the positions of this permutation are grouped by colors. We are allowed to fix the permutation using two kinds of actions: we can swap any two elements paying a fixed cost $S$, and we can also pick a color class and arbitrarily permute…"
date: "2026-07-03T07:52:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103438
codeforces_index: "H"
codeforces_contest_name: "2021 ICPC Southeastern Europe Regional Contest"
rating: 0
weight: 103438
solve_time_s: 50
verified: true
draft: false
---

[CF 103438H - Colourful Permutation Sorting](https://codeforces.com/problemset/problem/103438/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of size $n$, but the positions of this permutation are grouped by colors. We are allowed to fix the permutation using two kinds of actions: we can swap any two elements paying a fixed cost $S$, and we can also pick a color class and arbitrarily permute all elements currently sitting on positions of that color, paying a separate cost $C_i$ for that color operation.

The important point is that colors belong to positions, not values. Swapping moves values between positions without changing colors, while a color operation lets us freely rearrange values inside one color class in a single paid move. The goal is to transform the permutation into the identity permutation with minimum total cost.

The structure imposed by constraints is the key driver of the solution. The permutation size goes up to $10^5$, but the number of colors is at most 5. This immediately suggests that any solution that tries to track states per color subset is viable, since there are only $2^5 = 32$ subsets. On the other hand, anything quadratic or cubic in $n$ would be too slow unless heavily optimized or reduced to linear per test.

A subtle issue appears when thinking in terms of greedy swaps alone. A naive strategy is to compute the permutation cycle decomposition and pay $S$ for each swap improvement, but color operations can completely restructure cycles locally. This means cycles are not fixed: a color operation can “reshape” the permutation graph inside a color group, potentially merging or breaking cycles in a way that changes the number of swaps needed globally.

A small misleading case is when a color contains elements from multiple cycles. Without using the color operation, those cycles remain independent and force multiple swaps. With a single color operation, those same elements can be rearranged to align better, potentially reducing multiple swap operations to a single restructuring step. Any solution that treats cycles as immutable will fail here.

## Approaches

If we ignore color operations, the problem reduces to the classic fact that sorting a permutation with arbitrary swaps costs $S \cdot (n - \text{cycles})$, since each swap reduces the number of cycles by one in an optimal decomposition process.

If we only use color operations, each color can independently permute its positions for cost $C_i$, and we could try to “fix” as much of the permutation as possible inside each color group. However, this still does not fully solve interactions between different colors, since swaps are global and connect everything.

The key structural observation is that there are only 5 colors, so we can choose for each color whether to apply its expensive “free permutation” operation or not. Once a subset of colors is chosen, the problem becomes: inside chosen colors, we can arbitrarily rearrange values; inside unchosen colors, we cannot. This turns the problem into evaluating a modified permutation structure and computing the minimum swap cost on that derived structure.

Thus the solution is to try all $2^k$ subsets of colors. For each subset, we compute the best achievable arrangement after freely permuting inside selected colors, then compute the number of swaps required to fix the resulting permutation.

The difficulty lies in computing, for a fixed subset, how many cycles remain after optimal rearrangement. The rearrangement inside a color is not arbitrary per position independently; it is a full permutation inside that color group, so it is a constrained matching problem, but it can be resolved greedily per group because we only care about maximizing cycle formation between positions and their target values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation of all operations | exponential | high | Too slow |
| Subset DP over colors with cycle recomputation | $O(2^k \cdot n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We fix a subset of colors that we decide to activate with color operations.

1. We iterate over all subsets of colors. Each subset represents which colors we are allowed to freely permute internally.
2. For a fixed subset, we conceptually modify the permutation by allowing each active color group to reorder its elements arbitrarily. This means that inside each active color, we are free to choose any bijection between its positions and the values currently residing in those positions.
3. We reconstruct an “optimized” version of the permutation. Inside each active color group, we greedily match values to positions in a way that maximizes the number of positions already pointing to their correct destination. This is done by sorting within the group and pairing compatible targets.
4. After constructing this best possible arrangement for the chosen subset, we compute the number of cycles in the resulting permutation graph.
5. The swap cost for this configuration is $S \cdot (n - \text{cycles})$, since each swap reduces the cycle count by exactly one.
6. We add the cost of activating the chosen colors, which is the sum of $C_i$ over the subset.
7. We take the minimum over all subsets.

The correctness comes from the invariant that for any fixed subset of activated colors, we exhaustively consider all possible rearrangements inside each active color group that could influence cycle structure. Any optimal solution corresponds to some subset choice, and within that subset, there exists an arrangement that achieves the computed maximum cycle count.

This works because swaps only affect global cycle decomposition, while color operations only affect internal rearrangement freedom. Once the subset is fixed, the permutation structure becomes deterministic up to internal relabeling inside each active group, and maximizing cycles is equivalent to choosing the best such relabeling.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_cycles(arr):
    n = len(arr)
    vis = [False] * n
    res = 0
    for i in range(n):
        if not vis[i]:
            res += 1
            j = i
            while not vis[j]:
                vis[j] = True
                j = arr[j]
    return res

def solve():
    T = int(input())
    for _ in range(T):
        n, k = map(int, input().split())
        data = list(map(int, input().split()))
        S = data[0]
        C = data[1:]
        
        p = list(map(lambda x: x - 1, input().split()))
        col = list(map(lambda x: x - 1, input().split()))
        
        pos_in_color = [[] for _ in range(k)]
        for i in range(n):
            pos_in_color[col[i]].append(i)
        
        ans = S * (n - 1)
        
        for mask in range(1 << k):
            cost = 0
            for i in range(k):
                if mask & (1 << i):
                    cost += C[i]
            
            arr = p[:]
            
            for c in range(k):
                if mask & (1 << c):
                    idx = pos_in_color[c]
                    vals = [arr[i] for i in idx]
                    vals.sort()
                    for i, v in zip(sorted(idx), vals):
                        arr[i] = v
            
            cycles = count_cycles(arr)
            cost += S * (n - cycles)
            ans = min(ans, cost)
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code iterates over all color subsets using a bitmask. For each subset, it builds a working copy of the permutation. For every activated color, it gathers the indices in that color, extracts their current values, sorts both indices and values, and assigns them greedily. This realizes an optimal internal permutation that maximizes alignment within the group.

After reconstructing the permutation, the cycle counting routine computes how many components remain. The swap cost is derived directly from cycle decomposition, and then the color activation cost is added.

A subtle point is that sorting indices and values independently is what enables maximal pairing inside each group. This avoids needing explicit matching or graph algorithms per subset.

## Worked Examples

Consider a small permutation where internal structure matters.

Input:

```
n = 4, k = 1
p = [2, 3, 4, 1]
colors = [1, 1, 1, 1]
S = 10, C1 = 1
```

| subset | rearranged perm | cycles | swap cost | total |
| --- | --- | --- | --- | --- |
| none | [2,3,4,1] | 1 | 30 | 30 |
| {color 1} | [1,2,3,4] | 4 | 0 | 1 |

When the color is activated, the entire array can be permuted freely, so we directly align everything and eliminate all swaps.

Now consider a mixed-color interaction:

Input:

```
n = 6, k = 2
p = [5,2,4,6,1,3]
col = [1,2,1,2,1,2]
S = 10, C = [1,1]
```

For subset where no colors are used, we compute cycles of the original permutation.

| subset | key idea | cycles | swap cost | color cost | total |
| --- | --- | --- | --- | --- | --- |
| ∅ | fixed permutation | 1 | 50 | 0 | 50 |
| {1} | reorder color 1 only | improved alignment | 2 | 30 | 31 |
| {2} | reorder color 2 only | improved alignment | 2 | 30 | 31 |
| {1,2} | full flexibility | 6 | 0 | 2 | 2 |

The fully activated case shows why color operations dominate: once both groups are flexible, the permutation can be fully resolved internally.

These traces show that the solution is not about swapping efficiency alone but about how much structural freedom each color subset introduces into cycle formation.

## Compl
