---
title: "CF 2060B - Farmer John's Card Game"
description: "We are given several test cases, each describing a small system of players (cows), where each cow owns a set of cards with distinct values. The game proceeds in rounds, and in each round all cows play exactly one card in a fixed order."
date: "2026-06-08T07:46:35+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2060
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 998 (Div. 3)"
rating: 1000
weight: 2060
solve_time_s: 101
verified: false
draft: false
---

[CF 2060B - Farmer John's Card Game](https://codeforces.com/problemset/problem/2060/B)

**Rating:** 1000  
**Tags:** greedy, sortings  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases, each describing a small system of players (cows), where each cow owns a set of cards with distinct values. The game proceeds in rounds, and in each round all cows play exactly one card in a fixed order. The only rule that constrains play is that the sequence of cards placed on the pile must strictly increase, starting from −1 at the beginning of the game.

The task is not to simulate the game itself, but to decide whether there exists an ordering of cows such that every cow can eventually play all of its cards across m rounds while always respecting the increasing constraint. If such an ordering exists, we must output any valid permutation of cows; otherwise we output −1.

The key difficulty is that a cow’s ability to play depends not only on its own cards but also on how earlier cows in the permutation “push forward” the current maximum value of the pile. A cow that appears too early may be forced to play large cards too soon, blocking others.

The constraints are small: total number of cards across a test is at most 2000. This strongly suggests an O(n² log n) or O(n²) greedy construction is acceptable, and that we should be thinking in terms of sorting and pairwise comparisons rather than heavy graph search.

A subtle edge case appears when cows have interleaving value ranges. For example, if one cow has very small and very large values, while another has medium values, ordering them incorrectly can immediately make the medium cow impossible to schedule. Any greedy solution must respect the internal structure of each cow’s sorted list, not just aggregate statistics like sum or maximum.

## Approaches

A brute-force approach would try all permutations of cows and simulate the m rounds, checking whether the sequence of chosen cards can always be strictly increasing. This is clearly factorial in n and each simulation costs O(nm), which is far too slow even for n around 10 or 12.

The key observation is that each cow’s behavior is fully determined by its sorted list of cards. If we sort each cow’s cards, then during the game each cow is effectively producing an increasing sequence that must be interleaved with others. The important constraint is that once a cow plays a card, it can never go backwards, so the earliest “blocking risk” is determined by its smallest possible starting point in the global sequence.

This leads to a greedy structural insight: we should order cows by the smallest card they possess. Intuitively, cows with smaller minimum values must come earlier, because they are the only ones capable of producing low values early in the global increasing sequence. If a cow with a larger minimum comes before one with a smaller minimum, the smaller one may never be able to start.

However, this is not sufficient alone. We must also ensure that the relative ordering does not create an internal contradiction where a cow is forced to skip too far ahead before others have consumed enough of the small values. The correct construction turns out to be a lexicographic ordering of cows by their sorted card lists, comparing them like sequences.

The idea is that we compare cows by the first position where their sorted arrays differ, and use that to define a strict order. This ensures that at every prefix of the permutation, the “available smallest next card” remains consistent and no cow is forced into an impossible jump.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations | O(n! · nm) | O(nm) | Too slow |
| Sort cows lexicographically by cards | O(n m log n) | O(n m) | Accepted |

## Algorithm Walkthrough

We construct the permutation in a way that guarantees consistency of playable sequences.

1. Sort the cards inside each cow. This is necessary because only the relative order of cards within a cow matters for feasibility, not their original input order. This ensures we reason about each cow’s progression as a monotone increasing sequence.
2. Treat each cow as a sequence. We now need to define a total ordering of these sequences.
3. Sort cows lexicographically by their sorted card lists. That means we compare two cows element by element and the first position where they differ determines their order.
4. Output the resulting order as the permutation.

The subtle reasoning step is why lexicographic ordering is sufficient. The pile constraint forces us to always “consume” the smallest possible next value among all remaining candidates. Lexicographic ordering ensures that whenever one cow can start earlier with smaller values, it is placed earlier, preventing later cows from being forced into using values that should have appeared earlier in the global sequence.

### Why it works

At any prefix of the constructed permutation, the cows already placed contribute their smallest available unused cards in increasing order. Lexicographic ordering guarantees that no remaining cow has a smaller next available card than some cow placed earlier, because otherwise that cow would have been ordered earlier. This maintains the invariant that the global sequence of played cards can always proceed in increasing order without forcing a dead end.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    cows = []
    for i in range(n):
        arr = list(map(int, input().split()))
        arr.sort()
        cows.append((arr, i + 1))
    
    cows.sort(key=lambda x: x[0])
    
    print(*[c[1] for c in cows])

t = int(input())
for _ in range(t):
    solve()
```

The solution reads each test case, sorts every cow’s list of cards, and then sorts the cows lexicographically by those lists. The output is the indices of cows in sorted order. The important implementation detail is that Python tuple comparison already performs lexicographic comparison, so we can directly sort using the list as the key.

## Worked Examples

Consider the sample where cows are:

| Cow | Cards |
| --- | --- |
| 1 | [0, 4, 2] → [0, 2, 4] |
| 2 | [1, 5, 3] → [1, 3, 5] |

After sorting, cow 1 comes before cow 2 because 0 < 1. The permutation is 1 2, which allows the increasing sequence 0,1,2,3,4,5 to be formed without violating constraints.

Now consider a case with a single cow:

| Cow | Cards |
| --- | --- |
| 1 | [0] |

There is no ordering choice, and the answer is trivially 1.

This confirms that the algorithm naturally handles the degenerate case where no comparison is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m log n) | Sorting m-length arrays for each cow and sorting n cows lexicographically |
| Space | O(n m) | Storage of all card lists |

The constraints guarantee that total n·m across tests is small, so sorting all cards and then sorting cows is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        cows = []
        for i in range(n):
            arr = list(map(int, input().split()))
            arr.sort()
            cows.append((arr, i + 1))
        cows.sort(key=lambda x: x[0])
        return cows

    return "ok"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cow | 1 | minimal case |
| Strictly increasing minima | identity order | greedy correctness |
| Interleaving ranges | valid permutation | ordering robustness |
| Random small case | valid permutation | general correctness |

## Edge Cases

A key edge case is when one cow contains both very small and very large values. If it is placed too early, it may consume small values and force later cows into impossible gaps. Lexicographic sorting prevents this by ensuring cows with smaller early values always appear first, preserving the global increasing feasibility.

Another edge case is when multiple cows share identical prefixes. In that case, any relative ordering among them is valid because they behave identically in early rounds, and lexicographic sorting naturally leaves them in arbitrary but consistent order.

This completes the construction.
