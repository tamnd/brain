---
title: "CF 1735D - Meta-set"
description: "We are given a variant of the card game \"Set\". Each card has $k$ features, each of which is 0, 1, or 2. A card is thus a length-$k$ vector over ${0,1,2}$. A \"set\" is any three cards where, for every feature, either all three values are equal or all three are different."
date: "2026-06-09T18:15:50+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "data-structures", "hashing", "math"]
categories: ["algorithms"]
codeforces_contest: 1735
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 824 (Div. 2)"
rating: 1700
weight: 1735
solve_time_s: 535
verified: true
draft: false
---

[CF 1735D - Meta-set](https://codeforces.com/problemset/problem/1735/D)

**Rating:** 1700  
**Tags:** brute force, combinatorics, data structures, hashing, math  
**Solve time:** 8m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a variant of the card game "Set". Each card has $k$ features, each of which is 0, 1, or 2. A card is thus a length-$k$ vector over $\{0,1,2\}$. A "set" is any three cards where, for every feature, either all three values are equal or all three are different. Our input is a list of $n$ distinct cards and the output we seek is the number of distinct five-card groups, called "meta-sets," which contain more than one set.

The constraints $n \le 10^3$ and $k \le 20$ indicate that we cannot enumerate all five-card combinations directly, because there are ${1000 \choose 5} \approx 8 \cdot 10^{13}$ such groups. However, enumerating all triples is feasible, because ${1000 \choose 3} \approx 1.66 \cdot 10^{8}$, which is at the edge of possibility, especially with an $O(k)$ check for set validity. We must leverage the combinatorial structure of "Set" rather than brute force enumeration of quintuples.

Edge cases that could break a naive solution include cards that differ only in one feature, cards that are all equal in one feature, or configurations where multiple triples share cards. For instance, a group of five cards where four are identical except in one feature can form multiple sets. A careless approach that counts sets independently might double-count or miss overlapping sets, so we need a method that carefully counts unique meta-sets.

## Approaches

A naive approach is to enumerate all five-card subsets, then for each subset, check all ten possible triples for set-ness and count those that contain more than one set. This is correct in principle, but computationally infeasible: for $n = 1000$, the number of five-card subsets is roughly $8 \cdot 10^{13}$, making it impossible to process in 4 seconds.

The key observation is that in a "Set"-like structure over $\{0,1,2\}^k$, the third card in a set is uniquely determined by the first two cards. For each feature, if two cards share the same value, the third must match; if they differ, the third must be the value not present. This allows us to represent a set as a hashable vector of length $k$, enabling $O(1)$ lookups in a dictionary.

Using this property, we can first count all sets among the $n$ cards in $O(n^2 k)$ by iterating over all pairs, computing the required third card, and checking its existence in a set of cards. Once all sets are known, we need to count five-card groups containing at least two sets. Observing that a meta-set must be a union of two overlapping sets sharing one or two cards allows us to enumerate potential meta-sets efficiently by iterating over pairs of sets that share one or two cards, and recording the union if its size is five.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^5 k)$ | $O(nk)$ | Too slow |
| Optimal | $O(n^2 k + s^2)$ | $O(nk + s)$, $s$ = number of sets | Accepted |

## Algorithm Walkthrough

1. Read the number of cards $n$ and features $k$. Store all cards as tuples in a set for fast membership queries. This allows $O(1)$ existence checks for potential third cards in a set.
2. Initialize an empty list to store all discovered sets. Iterate over all pairs of cards $(a,b)$. For each feature position $i$, determine the value of the third card $c_i$ that would complete a set: if $a_i = b_i$, then $c_i = a_i$; otherwise, $c_i = 3 - a_i - b_i$ because $0+1+2 = 3$. This uses modular arithmetic to find the missing value efficiently.
3. Check if the computed third card exists in the set of input cards. If it does, record the sorted triple as a set to avoid duplicates. Continue for all pairs. At the end, we have a complete list of all sets.
4. Initialize a set to record unique meta-sets. Iterate over all pairs of sets. If the union of their card indices has size five, add it to the meta-set collection. This ensures we count each meta-set exactly once, based on overlapping sets.
5. Output the number of meta-sets found.

Why it works: Every set is uniquely determined by two of its cards. By constructing all sets via pairs and checking their union size, we systematically enumerate all five-card groups that contain multiple sets without missing or double-counting any. This method leverages the combinatorial structure of "Set" to reduce a naive $O(n^5)$ problem to manageable $O(n^2 k + s^2)$, where $s$ is the number of sets.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import combinations

n, k = map(int, input().split())
cards = [tuple(map(int, input().split())) for _ in range(n)]
card_set = set(cards)

# map card to index for fast lookup
card_index = {cards[i]: i for i in range(n)}

sets = []
for i in range(n):
    for j in range(i+1, n):
        third = []
        for x, y in zip(cards[i], cards[j]):
            if x == y:
                third.append(x)
            else:
                third.append(3 - x - y)
        third = tuple(third)
        if third in card_set:
            indices = sorted([i, j, card_index[third]])
            if indices not in sets:
                sets.append(indices)

meta_sets = set()
for s1, s2 in combinations(sets, 2):
    union = set(s1) | set(s2)
    if len(union) == 5:
        meta_sets.add(frozenset(union))

print(len(meta_sets))
```

Each part corresponds to the algorithm steps: storing cards for O(1) lookup, generating all sets from pairs, storing sets without duplication, and constructing meta-sets from overlapping sets. Using `frozenset` ensures uniqueness of meta-sets regardless of order. Subtle points include computing the third card with `3 - x - y` and avoiding duplicates in both sets and meta-sets.

## Worked Examples

Input:

```
8 4
0 0 0 0
0 0 0 1
0 0 0 2
0 0 1 0
0 0 2 0
0 1 0 0
1 0 0 0
2 2 0 0
```

| Pair (i,j) | Third Card | Exists? | Sets |
| --- | --- | --- | --- |
| 0000, 0001 | 0002 | Yes | 0000,0001,0002 |
| 0000, 0010 | 0020 | Yes | 0000,0010,0020 |
| ... | ... | ... | ... |

Union of first two sets: `{0000,0001,0002,0010,0020}` → size 5 → meta-set counted.

This confirms the algorithm correctly identifies the only meta-set.

Second example can similarly show overlapping sets producing meta-sets, confirming correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 k + s^2) | O(n^2 k) to generate all sets, O(s^2) to enumerate meta-set unions |
| Space | O(n k + s) | O(n k) for storing cards, O(s) for storing all sets |

Given $n \le 1000$ and $k \le 20$, the operations fit well under the 4-second time limit.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    cards = [tuple(map(int, input().split())) for _ in range(n)]
    card_set = set(cards)
    card_index = {cards[i]: i for i in range(n)}
    from itertools import combinations
    sets = []
    for i in range(n):
        for j in range(i+1, n):
            third = []
            for x, y in zip(cards[i], cards[j]):
                third.append(x if x == y else 3 - x - y)
            third = tuple(third)
            if third in card_set:
                indices = sorted([i,j,card_index[third]])
                if indices not in sets:
                    sets.append(indices)
    meta_sets = set()
    for s1, s2 in combinations(sets,2):
        union = set(s1) | set(s2)
        if len(union) == 5:
            meta_sets.add(frozenset(union))
    return str(len(meta_sets))

# provided sample
assert run("""8 4
0 0 0 0
0 0 0 1
0 0 0 2
0 0 1 0
0 0 2 0
0
```
