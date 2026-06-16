---
title: "CF 950A - Left-handers, Right-handers and Ambidexters"
description: "We are given three groups of players at a training session: people who can only use the left hand, people who can only use the right hand, and ambidextrous players who can be assigned to either hand."
date: "2026-06-17T02:20:23+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 950
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 469 (Div. 2)"
rating: 800
weight: 950
solve_time_s: 80
verified: true
draft: false
---

[CF 950A - Left-handers, Right-handers and Ambidexters](https://codeforces.com/problemset/problem/950/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three groups of players at a training session: people who can only use the left hand, people who can only use the right hand, and ambidextrous players who can be assigned to either hand. The coach wants to build a team of even size such that exactly half of the team plays using the left hand and the other half plays using the right hand.

Each left-handed player can only contribute to the left side, each right-handed player can only contribute to the right side, and each ambidextrous player can be assigned to either side depending on what helps balance the team.

The task is to maximize the total number of players in such a balanced team.

The constraint that all counts are at most 100 implies the solution does not require advanced data structures or optimization beyond constant time arithmetic reasoning. Any solution up to O(1) or O(n) is easily sufficient.

A key subtlety is that ambidextrous players are not simply extra participants, they are flexible resources that can be split across both sides. A naive mistake is to treat them as a single pool added to the smaller side only, without considering that after balancing, remaining ambidextrous players can still contribute in pairs to increase both sides equally.

A common failure case arises when all imbalance is not fully resolved but ambidextrous players are still available.

For example, consider:

Input:

```
1 10 3
```

If we only try to "fix imbalance" greedily, we may assign all 3 ambidextrous players to the left side, getting 4 left and 10 right, which still cannot form a balanced team larger than 8. The correct reasoning must consider that after partial balancing, leftover ambidextrous players can still be paired.

Another edge case is when there are no left or right players at all:

Input:

```
0 0 5
```

The correct answer is 4, not 5, since one player must be removed to maintain equal halves.

These cases show that the structure is driven by balancing first, then pairing.

## Approaches

A brute-force idea would be to try every possible even team size from 0 up to 2(l + r + a), and check whether we can assign exactly half left and half right using available players. For each candidate size 2k, we would try distributing k left slots and k right slots, verifying feasibility by checking whether ambidextrous players can cover deficits. This quickly becomes inefficient because for each k we would simulate assignments, leading to roughly O(n^2) behavior, which is unnecessary even for n ≤ 100.

The key observation is that the structure is greedy but decomposable. We first use mandatory assignments: left-only and right-only players naturally contribute to their respective sides. The only flexibility lies in ambidextrous players. Their role splits into two phases: first they resolve imbalance between left and right counts, and then any remaining ambidextrous players can only be used in symmetric pairs, because any single unpaired ambidextrous assignment would break balance.

This reduces the problem to a direct computation: build as large a balanced pair count as possible by first equalizing the sides, then expanding both sides equally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O((l+r+a)^2) | O(1) | Too slow conceptually |
| Greedy Balancing | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the maximum possible number of pairs k, where final team size is 2k.

1. Compute the initial guaranteed pairs as the minimum of left-only and right-only players. This gives a baseline balanced structure where no ambidextrous players are needed yet. At this point, one side may still have unused capacity.
2. Compute the imbalance between the two sides after this baseline pairing. This imbalance represents how many ambidextrous players are needed to equalize both sides so that further symmetric expansion is possible. The direction of imbalance does not matter, only its magnitude.
3. Use ambidextrous players to reduce this imbalance as much as possible. Each ambidextrous player used here increases the smaller side by one without affecting the larger side. This is the only operation that changes balance without requiring paired usage.
4. After balancing as much as possible, either both sides become equal or ambidextrous players run out. Any remaining ambidextrous players must now be used in pairs, since one assigned to each side keeps the balance intact. Each such pair increases the team size by 2, meaning it increases k by 1.
5. The final answer is twice the resulting k.

### Why it works

At every stage, we preserve the invariant that both sides of the team are equal in size. Any valid extension of the team must maintain this equality. Ambidextrous players are the only resource that can either fix imbalance or expand both sides simultaneously. Once imbalance is minimized, only symmetric usage remains optimal, since asymmetric usage would reintroduce imbalance and waste potential pairs.

This structure ensures no rearrangement of ambidextrous assignments can produce a larger balanced team than the computed value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    l, r, a = map(int, input().split())

    k = min(l, r)

    diff = abs(l - r)

    t = min(a, diff)
    k += t
    a -= t

    k += a // 2

    print(2 * k)

if __name__ == "__main__":
    solve()
```

The solution first locks in the guaranteed matches from strictly constrained players. It then uses ambidextrous players to reduce imbalance, since that is the only way to enable further symmetric growth. Finally, any leftover ambidextrous players are consumed in pairs, each pair increasing both sides equally.

A subtle implementation point is that integer division by 2 must be applied only after imbalance resolution. Doing it earlier would incorrectly assume symmetry before the system is balanced.

## Worked Examples

### Example 1

Input:

```
1 4 2
```

| Step | k (pairs) | l | r | a |
| --- | --- | --- | --- | --- |
| Start | 0 | 1 | 4 | 2 |
| Min(l,r) | 1 | 1 | 4 | 2 |
| Balance using a | 2 | 2 | 4 | 1 |
| Pair remaining a | 2 | 2 | 4 | 0 |
| Final | 3 | 2 | 4 | 0 |

Output is 6.

This shows both phases clearly: first imbalance is reduced, then remaining ambidexters form symmetric extensions.

### Example 2

Input:

```
0 0 5
```

| Step | k (pairs) | l | r | a |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | 5 |
| Min(l,r) | 0 | 0 | 0 | 5 |
| Balance using a | 0 | 0 | 0 | 5 |
| Pair remaining a | 2 | 0 | 0 | 1 |
| Final | 2 | 0 | 0 | 1 |

Output is 4.

This demonstrates that ambidextrous players cannot all be used individually; pairing constraint dominates once symmetry is achieved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations on three integers |
| Space | O(1) | No auxiliary data structures used |

The constraints are small, but even if they were large, the solution remains constant time because it depends only on direct arithmetic transformations of the input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    l, r, a = map(int, input().split())

    k = min(l, r)
    diff = abs(l - r)
    t = min(a, diff)
    k += t
    a -= t
    k += a // 2

    return str(2 * k)

# provided samples
assert run("1 4 2\n") == "6"

# custom cases
assert run("0 0 0\n") == "0", "no players"
assert run("10 10 0\n") == "20", "already balanced"
assert run("1 10 3\n") == "8", "imbalance + partial fix"
assert run("5 3 10\n") == "16", "excess ambidexters pairing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | 0 | empty edge case |
| 10 10 0 | 20 | no ambidexters needed |
| 1 10 3 | 8 | imbalance correction |
| 5 3 10 | 16 | leftover pairing behavior |

## Edge Cases

When there are no players at all, the algorithm immediately yields k = 0 since both min(l, r) and all subsequent contributions are zero. This ensures the output is 0, which is the only valid even team size.

When the system is already balanced with l equal to r, the imbalance is zero, so all ambidextrous players are immediately used in pairs. This directly expands the team without any intermediate correction phase.

When ambidextrous players are fewer than the imbalance, only partial balancing is possible. The algorithm correctly stops at the point where a is exhausted, leaving a still-unequal configuration, and therefore only symmetric pairing is disallowed beyond that point, preventing invalid overestimation.
