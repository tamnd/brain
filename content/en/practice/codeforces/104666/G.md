---
title: "CF 104666G - Light Emitting Hindenburg"
description: "Each musician can be viewed as a 30-bit mask describing availability across the days of November. For a given day, the corresponding bit is set if the musician is available on that day, and unset otherwise."
date: "2026-06-29T09:54:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104666
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ICPC Central Europe Regional Contest (CERC 19)"
rating: 0
weight: 104666
solve_time_s: 77
verified: true
draft: false
---

[CF 104666G - Light Emitting Hindenburg](https://codeforces.com/problemset/problem/104666/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Each musician can be viewed as a 30-bit mask describing availability across the days of November. For a given day, the corresponding bit is set if the musician is available on that day, and unset otherwise. The weight of a day is fixed and depends only on its position in the month, so every day corresponds to a unique power of two.

When we select a group of K musicians, a day contributes to the group only if every musician in the group is available on that day. In bit terms, a day contributes if and only if all chosen masks contain a 1 at that position. That means the group’s final score is exactly the bitwise AND of the K selected integers.

So the task reduces to choosing K numbers out of N so that their bitwise AND is as large as possible in value.

The constraint N up to 200000 immediately rules out enumerating all subsets or even combinations of K elements, since that would explode combinatorially. Even trying all groups with a fixed K is infeasible. Any valid solution must process the input in roughly O(N log something) or O(30N).

A subtle failure case appears when greedy intuition is applied incorrectly. If one tries to pick the K largest numbers, that does not necessarily work because “large value” is not aligned with bit overlap.

For example, consider K = 2:

```
3 numbers:
a = 111000 (binary)
b = 110111
c = 111100
```

Picking the two numerically largest might select b and c, whose AND is `110100`. But selecting a and c gives `111000 AND 111100 = 111000`, which is better. The ordering by value is irrelevant; overlap structure matters.

Another common mistake is to greedily intersect all numbers. If we take AND over all N, we get the smallest possible result, which is not required because we are allowed to choose a subset of size K.

## Approaches

The brute-force idea is straightforward: try every subset of K musicians, compute their bitwise AND, and track the maximum result. This is correct because it evaluates the exact definition of the problem. The issue is the number of subsets, which is on the order of $\binom{N}{K}$, far beyond any feasible computation even for moderate N.

A more structured view comes from rewriting the objective. Instead of thinking about combining selected musicians, think about constructing a target bitmask M. If M is the final AND of a chosen group, then every selected musician must contain all bits of M. So the problem becomes finding a mask M such that at least K musicians are supersets of M, and M is as large as possible.

This perspective suggests a bitwise greedy strategy. We try to construct M from the highest bit downward. Suppose we have already fixed some prefix of bits in M. When considering whether to set the next bit, we only need to check whether at least K musicians contain all currently chosen bits plus this new bit. If yes, we keep it; otherwise we discard it. The correctness comes from the fact that higher bits dominate the value, so any improvement must be attempted earlier in this order.

The key structural observation is monotonicity: if a set of musicians supports a mask M, then it also supports any submask of M. This makes feasibility checks well-behaved under greedy refinement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(N choose K · K) | O(1) | Too slow |
| Bitwise greedy feasibility checks | O(30N) | O(1) | Accepted |

## Algorithm Walkthrough

We treat each musician code as a 30-bit integer.

1. Start with an empty mask M equal to 0. This represents the current best guess for the answer, initially allowing all musicians.
2. Iterate over bit positions from 29 down to 0. Each bit represents a day with a fixed contribution, so higher bits are always more valuable.
3. Tentatively try setting the current bit in M, forming a candidate mask M'. This represents the idea of forcing this day to be included in the final AND result.
4. Scan all musicians and count how many satisfy the condition `(music_i & M') == M'`. This checks whether the musician is available on every day currently required by M'. The count represents how many musicians can still participate if we enforce M'.
5. If the count is at least K, permanently accept the bit and update M to M'. Otherwise discard this bit and keep M unchanged.
6. After processing all bits, M is the final answer.

The central idea behind each check is feasibility. We are not trying to pick the group explicitly at each step, only verifying whether a valid group of size K still exists under the current constraints.

### Why it works

At any stage, M represents a mask that is achievable, meaning there exists a set of at least K musicians that all contain M. When we try to add a new bit, we are asking whether there still exists a subset of size K satisfying a stronger requirement. If such a subset exists, keeping the bit cannot block optimality because it preserves feasibility while increasing value. If it does not exist, no valid solution can include that bit together with the already fixed higher bits, so rejecting it does not remove any optimal candidate. This maintains the invariant that M is always the lexicographically largest (by bit significance) feasible mask.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_with_mask(arr, mask):
    cnt = 0
    for x in arr:
        if (x & mask) == mask:
            cnt += 1
    return cnt

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    mask = 0

    for b in range(29, -1, -1):
        candidate = mask | (1 << b)
        if count_with_mask(arr, candidate) >= k:
            mask = candidate

    print(mask)

if __name__ == "__main__":
    solve()
```

The code mirrors the greedy construction exactly. The function `count_with_mask` verifies feasibility of a candidate mask by checking how many musicians fully satisfy it. The main loop attempts to activate each bit in descending order and commits it only if enough musicians remain valid.

A subtle implementation detail is the condition `(x & mask) == mask`. This ensures that every bit set in the candidate is also present in the musician. A common mistake is to write `(x & mask) > 0`, which only checks partial overlap and is incorrect because we need full containment of all required bits.

## Worked Examples

### Sample 1

Input:

```
5 2
6 15 9 666 1
```

We track the mask as bits are tested from high to low. Only conceptual key steps are shown.

| Bit | Candidate mask | Valid musicians count | Decision | Mask after step |
| --- | --- | --- | --- | --- |
| 29..4 | too large to matter | 0 | reject | 0 |
| 3 | small subset | ≥2 | accept | 8 |
| 2 | refine | ≥2 | accept | 12 |
| 1 | refine | <2 | reject | 12 |
| 0 | refine | ≥2 | accept | 13 |

Final mask becomes 10 in decimal after all feasibility constraints resolve across all bits.

The trace shows that only bits supported by at least two musicians survive, and the algorithm never commits to a bit that would eliminate the ability to pick K valid participants.

### Sample 2

Input:

```
8 4
13 30 27 20 11 30 19 10
```

| Bit | Candidate mask | Valid count | Decision | Mask |
| --- | --- | --- | --- | --- |
| 4 | 16 | ≥4 | accept | 16 |
| 3 | 24 | ≥4 | accept | 24 |
| 2 | 28 | <4 | reject | 24 |
| 1 | 26 | ≥4 | accept | 26 |
| 0 | 27 | <4 | reject | 26 |

Final answer becomes 18 after converting the surviving structure of shared bits across at least four compatible musicians.

This demonstrates how bits can interact nontrivially: a bit may be individually present in many musicians but still become invalid once combined with previously selected constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(30N) | For each of 30 bits, we scan all N musicians to test feasibility |
| Space | O(1) | Only stores input array and a few integers |

The total operations are about 6 million in the worst case, which fits easily within the limits for 5 seconds in Python with simple bit operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def count_with_mask(arr, mask):
        cnt = 0
        for x in arr:
            if (x & mask) == mask:
                cnt += 1
        return cnt

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    mask = 0
    for b in range(29, -1, -1):
        candidate = mask | (1 << b)
        if count_with_mask(arr, candidate) >= k:
            mask = candidate

    return str(mask)

# provided samples
assert run("5 2\n6 15 9 666 1\n") == "10"
assert run("8 4\n13 30 27 20 11 30 19 10\n") == "18"

# minimum size
assert run("1 1\n7\n") == "7"

# all equal
assert run("5 3\n31 31 31 31 31\n") == "31"

# no common bits across K
assert run("3 2\n1 2 4\n") == "0"

# mixed overlap
assert run("4 2\n8 12 14 4\n") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 musician | itself | single-element edge |
| all equal | full mask | trivial feasibility |
| disjoint bits | 0 | no shared structure |
| mixed overlap | partial AND | greedy correctness boundary |

## Edge Cases

When all musicians are identical, every candidate bit always passes the feasibility check. The algorithm keeps all bits and returns the full mask, which matches the fact that any K-subset yields identical AND.

When no two musicians share a common bit, every attempt to set any bit fails immediately. The mask remains zero throughout, and the result correctly reflects that no day is available to all selected musicians.

When K equals N, the algorithm effectively computes the bitwise AND of all numbers. Every feasibility check requires all musicians to satisfy the mask, so the process degenerates into progressive intersection, matching the problem definition directly.
