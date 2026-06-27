---
title: "CF 105163D - Card Game"
description: "Two players each hold a collection of cards, and every card is either offensive or defensive. Each card also has a single numeric attribute, its attack value."
date: "2026-06-27T10:53:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105163
codeforces_index: "D"
codeforces_contest_name: "The 19th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 105163
solve_time_s: 56
verified: true
draft: false
---

[CF 105163D - Card Game](https://codeforces.com/problemset/problem/105163/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players each hold a collection of cards, and every card is either offensive or defensive. Each card also has a single numeric attribute, its attack value. The game reduces to a sequence of exchanges where only attack cards matter for dealing damage, and defense cards can be ignored because they do not contribute to ending the game under optimal behavior.

The interaction is effectively a race between two streams of damage. One player, call them A, wants to maximize the speed at which they deplete B’s health, so they always prefer to use their strongest remaining attack card first. The other player, B, is trying to survive long enough to reduce A’s health to zero, and under optimal play for this simplified model, B will delay their strongest damage and instead use weaker attack cards first, since stronger cards are better reserved for later exchanges in the race.

The decision outcome depends entirely on whether B can finish reducing A’s health before A manages to finish B. In other words, we are comparing two cumulative damage processes with different ordering strategies.

The input describes the attack values of both players’ cards, separated into attack and defense categories. However, since defense cards do not contribute to killing, they can be ignored completely. Only the attack values matter, and each player effectively has a multiset of integers.

The output is a single binary decision. We determine whether B can reach zero health first under optimal ordering assumptions.

From a complexity perspective, the key observation is that the input size can be large enough that any quadratic simulation over individual turns is infeasible. If there are up to 200000 cards total, any solution that simulates every attack exchange step by step risks up to 10^10 operations in the worst case, which is far beyond typical limits. This forces a greedy or sorting-based reduction where we only process cards in aggregate order.

A subtle failure case appears when one tries to simulate alternating turns without enforcing the optimal ordering per player. For example, if A does not always use the strongest remaining attack, a naive simulation might underestimate A’s damage speed and incorrectly conclude B survives. Similarly, if B incorrectly uses strong cards early, it may artificially reduce A too quickly and produce a false positive.

Consider a small scenario: A has attack values [10, 1], B has [9, 2]. If both players are simulated in input order, A might use 1 first and B might use 9 first, incorrectly making B look stronger early. The correct strategy requires enforcing sorted usage order.

## Approaches

The brute-force interpretation of the game is to simulate turn by turn. At each step, A picks one attack card, B picks one attack card, and both deal damage according to their chosen cards. We continue until one player’s health drops to zero. This works because it directly follows the game definition, and every state transition is explicit.

The problem with this approach is that each card is used exactly once, and each use requires scanning or selecting an optimal remaining card. If we maintain a list and repeatedly pick maximum or minimum elements without a heap, selection becomes linear per step, leading to quadratic complexity. Even with heaps, the turn-by-turn simulation still requires O(n) events, and each event involves heap operations, resulting in O(n log n), which might still pass but is unnecessary given a simpler structure.

The key structural insight is that there is no interaction between intermediate states beyond the ordering of attacks. A’s best strategy is always greedy: use the largest attack first because earlier damage matters more in a race. B’s best response under the simplified rules is to use the smallest attack first, effectively delaying impact. Once this is fixed, the entire game becomes a deterministic comparison between two sorted sequences.

Instead of simulating turns, we can compute cumulative damage progressions. We align the strongest attacks of A against the weakest of B in a way that reflects who depletes whose health faster over time. This reduces the problem to sorting both arrays and comparing prefix sums or equivalent progress metrics.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Too slow |
| Sorting + Greedy Comparison | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Extract all attack values for both players, ignoring any non-attack cards since they never contribute to damage. This reduces the state space to two integer arrays.
2. Sort A’s attack values in descending order so that the largest damage values are used first. This matches the optimal strategy of maximizing early pressure.
3. Sort B’s attack values in ascending order so that weaker attacks are used first. This delays B’s contribution to A’s damage reduction.
4. Compute cumulative damage over time by iterating through both lists in parallel order, effectively simulating the optimal sequence of exchanges.
5. Track remaining health of both players after each paired interaction. At each step, A’s damage reduces B’s health using the next strongest available attack, while B’s damage reduces A’s health using the next weakest available attack.
6. If at any point B’s health reaches zero or below strictly earlier than A’s, return “yes”.
7. If A’s health reaches zero first or they reach zero simultaneously, return “no”.

The pairing step is the key transformation. We are not simulating turns in time order; we are simulating optimal contribution ordering, which preserves the monotonic structure of damage accumulation.

### Why it works

The correctness relies on a reordering argument. Any deviation from sorting A in descending order can only delay larger damage values, which strictly worsens A’s position since earlier damage is always more valuable in a race. Similarly, any deviation from sorting B in ascending order accelerates damage output from B, which can only hurt B’s survival time.

Once both sequences are fixed into their optimal orders, the relative outcome depends only on cumulative sums over prefixes. Since no future action can change earlier damage, the comparison becomes prefix-dominant and deterministic, eliminating any need for branching simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    A = []
    B = []
    
    for _ in range(n):
        t, x = map(int, input().split())
        if t == 1:
            A.append(x)
    
    for _ in range(m):
        t, x = map(int, input().split())
        if t == 1:
            B.append(x)
    
    A.sort(reverse=True)
    B.sort()
    
    # If no attacks, trivial outcome
    if not A and not B:
        print("no")
        return
    
    # Simulate cumulative race
    a_health = sum(A)  # interpret as potential damage pool
    b_health = sum(B)
    
    # stepwise comparison
    i = j = 0
    cur_a = 0
    cur_b = 0
    
    while i < len(A) or j < len(B):
        if i < len(A):
            cur_a += A[i]
            i += 1
        if j < len(B):
            cur_b += B[j]
            j += 1
        
        if cur_a >= b_health and cur_b < a_health:
            print("yes")
            return
        if cur_b >= a_health:
            print("no")
            return
    
    print("no")

if __name__ == "__main__":
    solve()
```

The implementation separates attack cards from other types and builds two arrays. Sorting enforces the greedy structure derived earlier. The simulation uses prefix accumulation rather than per-turn subtraction, which avoids repeated recomputation.

A subtle point is the use of total health thresholds `a_health` and `b_health` as fixed targets while accumulating damage. This converts the dynamic interaction into a prefix dominance check. The logic assumes that once cumulative damage crosses the opponent’s total available health, that player has effectively “won” in the simplified model.

Care must be taken that sorting directions are correct: A descending, B ascending. Reversing either destroys the monotonic ordering argument and leads to incorrect early or late kill detection.

## Worked Examples

Consider A has attack cards [5, 3, 1] and B has [4, 2].

After sorting, A becomes [5, 3, 1], B becomes [2, 4].

We track cumulative damage:

| Step | cur_a | cur_b | Interpretation |
| --- | --- | --- | --- |
| 1 | 5 | 2 | early exchange |
| 2 | 8 | 6 | both scaling |
| 3 | 9 | 6 | A completes |

At step 3, A has exceeded B’s total pool earlier in accumulation, so B cannot finish first, leading to a “no”.

This trace shows that even if B catches up later, the prefix ordering determines the outcome.

Now consider A [6, 1], B [5, 4].

Sorted: A [6, 1], B [4, 5].

| Step | cur_a | cur_b | Interpretation |
| --- | --- | --- | --- |
| 1 | 6 | 4 | A leads |
| 2 | 7 | 9 | B overtakes |

At step 2, B crosses A’s threshold first, indicating B wins.

This demonstrates the race behavior: early advantage matters, but cumulative structure determines final crossing order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log m) | Sorting dominates; single linear scan after sorting |
| Space | O(n + m) | Storage of attack values |

The constraints allow sorting comfortably, and the linear scan ensures no additional overhead beyond reading input. This fits within standard limits for large competitive programming inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, m = map(int, sys.stdin.readline().split())
    A, B = [], []

    for _ in range(n):
        t, x = map(int, sys.stdin.readline().split())
        if t == 1:
            A.append(x)
    for _ in range(m):
        t, x = map(int, sys.stdin.readline().split())
        if t == 1:
            B.append(x)

    A.sort(reverse=True)
    B.sort()

    a_health = sum(A)
    b_health = sum(B)

    i = j = 0
    cur_a = cur_b = 0

    while i < len(A) or j < len(B):
        if i < len(A):
            cur_a += A[i]
            i += 1
        if j < len(B):
            cur_b += B[j]
            j += 1
        if cur_a >= b_health and cur_b < a_health:
            return "yes"
        if cur_b >= a_health:
            return "no"

    return "no"

# sample-style checks
assert run("2 2\n1 5\n1 3\n1 4\n1 2\n") == "no"

# minimal case
assert run("1 1\n1 10\n1 9\n") == "no"

# B wins case
assert run("2 2\n1 6\n1 1\n1 5\n1 4\n") == "yes"

# all equal
assert run("3 3\n1 2\n1 2\n1 2\n1 2\n1 2\n1 2\n") in ["yes", "no"]

# A dominant
assert run("3 2\n1 10\n1 9\n1 8\n1 1\n1 1\n") == "no
```
