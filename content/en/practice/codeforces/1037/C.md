---
title: "CF 1037C - Equalize"
description: "We are given two binary strings of equal length. Think of them as two rows of switches, where each position is either on or off."
date: "2026-06-16T18:48:42+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1037
codeforces_index: "C"
codeforces_contest_name: "Manthan, Codefest 18 (rated, Div. 1 + Div. 2)"
rating: 1300
weight: 1037
solve_time_s: 569
verified: true
draft: false
---

[CF 1037C - Equalize](https://codeforces.com/problemset/problem/1037/C)

**Rating:** 1300  
**Tags:** dp, greedy, strings  
**Solve time:** 9m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two binary strings of equal length. Think of them as two rows of switches, where each position is either on or off. The goal is to transform the first row into the second row using two types of operations: we can swap any two positions in the first string, paying a cost equal to how far apart those positions are, or we can flip a single bit at unit cost.

The key difficulty is that swaps are not free and depend on distance, so moving mismatched bits around is expensive when done naively. Flips are cheap but they permanently change a bit, so deciding between fixing mismatches via movement or direct correction is the core tradeoff.

The constraint up to one million characters rules out anything quadratic or even $O(n \log n)$ with heavy constants. Any solution must essentially scan the strings a constant number of times and maintain linear data structures.

A naive but incorrect idea is to greedily fix mismatches left to right, always flipping or swapping locally. For example, if we see a mismatch at index $i$, we might flip it immediately. This fails because a mismatch at one position may be cheaper to resolve by pairing it with a later mismatch and swapping instead of paying two flips.

Another subtle failure comes from treating swaps as always beneficial when two mismatched positions exist. If we swap without considering distance, we may assume a perfect pairing exists, but the cost of bringing mismatched bits together can exceed two flips, especially when mismatches are far apart.

## Approaches

The problem reduces to understanding mismatched positions only. At any index, if $a[i] = b[i]$, it does not matter. Otherwise, we have a mismatch that must be corrected either by flipping or by pairing with another mismatch and swapping.

Let us classify mismatches into two types: positions where $a[i] = 0, b[i] = 1$, and positions where $a[i] = 1, b[i] = 0$. Call them type A and type B respectively. A swap between one A and one B can potentially fix both positions simultaneously.

The brute force idea would try all ways to pair mismatches and decide whether to swap or flip. This quickly becomes combinatorial because there are potentially $O(n)$ mismatches, leading to exponential matching possibilities or at least a minimum cost matching problem over a line with distance weights.

The key observation is that the structure is one-dimensional. If we list mismatch indices in order, pairing adjacent mismatches of opposite type is always optimal whenever swapping is used. Any non-adjacent pairing can be improved or matched by considering crossings: swapping distant mismatches forces passing over intermediate indices, which only increases cost compared to resolving locally.

This reduces the problem to scanning the string, maintaining the last unmatched mismatch, and deciding whether to pair it with the current one or pay flips.

We maintain a stack-like structure of unresolved mismatches. Whenever we see a mismatch of opposite type to the top of the stack, we can either pair them with a swap or leave them for flips. The swap cost is exactly the distance between indices, while two flips cost 2. So for each pair, we take the minimum of those two options.

Since indices are processed in order, the distance is known immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force pairing mismatches | Exponential | O(n) | Too slow |
| Greedy pairing of adjacent mismatches | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the string from left to right and maintain a list of mismatches that have not yet been resolved.

1. Scan index $i$ from 0 to $n-1$. If $a[i] = b[i]$, skip it because it requires no action.
2. If there is no pending mismatch, push the current mismatch index and its type into a structure. We remember whether it is a 0 to 1 mismatch or 1 to 0 mismatch because pairing is only meaningful between opposite types.
3. If there is a pending mismatch of the opposite type, we consider matching it with the current index. This creates a candidate swap cost equal to $i - j$, where $j$ is the previous mismatch index.
4. Compare the swap option with flipping both positions independently, which costs 2. Add the minimum of these two to the answer and clear the pending mismatch.
5. If the pending mismatch is of the same type as the current one, we cannot pair them, so we push the current mismatch and keep the previous one waiting.
6. After processing all indices, any remaining unmatched mismatches must be resolved individually by flips, each contributing 1 to the answer.

### Why it works

The algorithm relies on the fact that mismatches form two ordered sequences on a line. Any optimal solution can be transformed so that swaps only occur between consecutive opposite-type mismatches in index order. Any crossing pairing can be uncrossed without increasing cost because swap cost is linear in distance, and uncrossing reduces total distance traveled. Once restricted to adjacent pairings, every decision becomes local: either pay the swap cost for the pair or pay two flips, and no future decision can improve this choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = input().strip()
    b = input().strip()

    ans = 0

    prev_idx = -1
    prev_type = 0  # +1 for 0->1, -1 for 1->0

    for i in range(n):
        if a[i] == b[i]:
            continue

        cur_type = 1 if a[i] == '0' else -1

        if prev_idx == -1:
            prev_idx = i
            prev_type = cur_type
        else:
            if prev_type != cur_type:
                cost_swap = i - prev_idx
                ans += min(cost_swap, 2)
                prev_idx = -1
            else:
                ans += 1
                prev_idx = i
                prev_type = cur_type

    if prev_idx != -1:
        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code scans once through the strings and only tracks at most one unresolved mismatch at a time. The variable `prev_idx` stores the last unmatched mismatch position, while `prev_type` stores its direction. When a compatible mismatch appears, we evaluate pairing cost versus flipping.

A subtle point is that when two mismatches are of the same type, we cannot form a swap, so the earlier mismatch must be resolved by a flip immediately. This prevents carrying incompatible states forward and ensures correctness of greedy pairing.

At the end, any leftover mismatch is paid as a flip.

## Worked Examples

### Example 1

Input:

```
n = 3
a = 100
b = 001
```

Mismatches occur at all indices.

| i | a[i] | b[i] | Type | prev state | Action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | -1 | empty | store | 0 |
| 1 | 0 | 0 | skip | - | - | 0 |
| 2 | 0 | 1 | +1 | (-1 at 0) | swap vs flip → min(2,2)=2 | 2 |

Final answer is 2. This shows a clean pairing across the ends where swap distance equals two flips.

### Example 2

Input:

```
n = 4
a = 0101
b = 0011
```

| i | a[i] | b[i] | Type | prev state | Action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | - | empty | skip | 0 |
| 1 | 1 | 0 | -1 | empty | store | 0 |
| 2 | 0 | 1 | +1 | (-1 at 1) | swap cost 1 vs 2 flips → 1 | 1 |
| 3 | 1 | 1 | - | no mismatch | - | 1 |

This demonstrates that adjacent opposite mismatches are always best paired via swap when close.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single linear scan over the strings |
| Space | O(1) | only a constant number of state variables are stored |

The solution performs exactly one pass through strings of length up to $10^6$, which is easily within limits. Memory usage is constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []
    
    def input():
        return sys.stdin.readline()
    
    n = int(sys.stdin.readline())
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    ans = 0
    prev_idx = -1
    prev_type = 0

    for i in range(n):
        if a[i] == b[i]:
            continue
        cur_type = 1 if a[i] == '0' else -1
        if prev_idx == -1:
            prev_idx = i
            prev_type = cur_type
        else:
            if prev_type != cur_type:
                ans += min(i - prev_idx, 2)
                prev_idx = -1
            else:
                ans += 1
                prev_idx = i
                prev_type = cur_type

    if prev_idx != -1:
        ans += 1

    return str(ans)

# provided sample
assert run("3\n100\n001\n") == "2"

# all equal
assert run("5\n00000\n00000\n") == "0"

# single flip needed
assert run("1\n0\n1\n") == "1"

# two mismatches far apart
assert run("4\n1000\n0001\n") == "2"

# alternating mismatches
assert run("6\n101010\n010101\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | no operations needed |
| single mismatch | 1 | base flip case |
| symmetric ends | 2 | swap vs flip decision |
| alternating | 3 | repeated pairing logic |

## Edge Cases

For strings with no mismatches, the algorithm never enters pairing logic and immediately returns zero because no pending state is ever created.

For a single mismatch like $a = 0, b = 1$, the algorithm stores it and reaches the end, then applies a single flip cost, matching optimal behavior.

For multiple consecutive mismatches of the same type, such as all 0 to 1, the algorithm never pairs them and resolves each with flips, which is optimal because swaps cannot fix same-direction mismatches.
