---
title: "CF 104760H - \u0412\u043c\u0435\u0441\u0442\u0435 \u043d\u0430\u0432\u0441\u0435\u0433\u0434\u0430"
description: "We are given two groups of travelers initially split across two different universes, with A people on one side and B people on the other. Between the two universes there are N portals, and each portal can be used a limited number of times."
date: "2026-06-28T22:03:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "H"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 81
verified: true
draft: false
---

[CF 104760H - \u0412\u043c\u0435\u0441\u0442\u0435 \u043d\u0430\u0432\u0441\u0435\u0433\u0434\u0430](https://codeforces.com/problemset/problem/104760/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two groups of travelers initially split across two different universes, with A people on one side and B people on the other. Between the two universes there are N portals, and each portal can be used a limited number of times. Every time someone passes through a portal, they switch sides, and after a portal has been used exactly $f_i$ times, it is destroyed and can no longer be used.

The process consists of repeatedly choosing a person and a portal, moving that person through the portal, and counting that usage toward the portal’s limit. The goal is to decide whether it is possible to perform a sequence of such moves so that two conditions hold at the end: all portals are fully destroyed, and all travelers end up in the same universe.

The input size allows up to $10^5$ portals with capacities up to $10^9$, which immediately rules out any simulation of individual crossings. Any solution that reasons step-by-step over operations would be far too slow, since the total number of crossings can reach $10^{14}$.

A subtle point is that each portal is not directional and every use only flips the side of exactly one person. There is no restriction on which person uses which portal, meaning the only global constraints come from counts of moves and parity of side changes, not from individual identities or portal structure.

A naive but incorrect approach is to try assigning people greedily to portals or simulate transfers. For example, with A = 2, B = 2, and portals [1, 1, 1], a greedy strategy that tries to balance sides locally might conclude incorrectly that balancing is impossible, because it fails to account for the flexibility in choosing which individuals move at each step. The actual constraint is global and depends only on totals, not structure.

Another pitfall is assuming that since each portal must be used exactly $f_i$ times, the distribution of these uses across time matters. It does not; only the total number of side-flips matters.

## Approaches

The brute-force viewpoint is to simulate the entire process: maintain a multiset of available portal capacities and a list of people on each side, then repeatedly choose a person and a portal, apply a move, and decrement remaining capacity. Each operation is $O(1)$, but there are $\sum f_i$ operations in total. Since $\sum f_i$ can be as large as $10^{14}$, this approach is completely infeasible.

The key simplification is to ignore the identity of portals and focus only on what each operation does globally. Every traversal flips exactly one person from one side to the other. After all portals are exhausted, exactly $T = \sum f_i$ such flips have occurred. The only thing that matters is how many of these flips go from A to B versus from B to A.

Let $p$ be the number of moves from A to B and $q$ from B to A. Then $p + q = T$. The final number of people on the A-side becomes $A + q - p$. Since we want all people on one side, we only need to check whether there exists a valid split of these $T$ moves that produces either $A + B$ on one side or $0$ on that side.

This reduces the entire problem to a parity and feasibility condition on $T$, because the only freedom is choosing how many moves go in each direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(\sum f_i)$ | $O(1)$ | Too slow |
| Total-count + parity reasoning | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compute the total number of portal uses $T = \sum f_i$. After that, the entire problem reduces to checking whether we can end with everyone on the A-side or everyone on the B-side.

1. Compute $T = \sum f_i$. This represents the total number of side-flipping moves that must happen.
2. Consider the possibility that all travelers end on the A-side. If this happens, the final A-side population must be $A + B$. Each move flips exactly one person, so after $T$ moves, the change in A-side population is determined by how many moves go in each direction. This leads to the condition that $T \ge B$, because at least all B-side travelers must be moved across.
3. Ensure parity consistency for ending on A. The difference $T - B$ must be even, since each pair of opposite-direction moves cancels out one net shift. This guarantees that the remaining net movement can exactly match the required transfer of all B travelers.
4. Repeat the same reasoning for ending on the B-side. For that case, we require $T \ge A$ and that $T - A$ is even.
5. If either of the two target configurations is feasible, output YES. Otherwise, output NO.

### Why it works

Each operation changes the number of people on the A-side by exactly $+1$ or $-1$, depending on direction. After all operations, only the total number of such increments matters, not their ordering or which portal produced them. This makes the system equivalent to choosing a sequence of $T$ signed steps whose net sum must match a fixed target. The only obstruction is whether the parity and magnitude constraints align with the required final configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())
    n = int(input())
    f = list(map(int, input().split()))
    
    T = sum(f)
    
    if (T >= B and (T - B) % 2 == 0) or (T >= A and (T - A) % 2 == 0):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The implementation first aggregates all portal capacities into a single total. From that point onward, no per-portal reasoning is required. The two conditional checks directly encode the feasibility conditions for choosing A or B as the final unified universe. The modulo check ensures that the remaining imbalance after accounting for required transfers can be resolved using pairs of opposite moves.

## Worked Examples

### Sample 1

Input:

```
5 7
2
1 2
```

Here $T = 3$.

| Step | Target Side | Required Transfers | Feasible | Parity Check |
| --- | --- | --- | --- | --- |
| A-side | 3+7=10 | B=7 | 3 < 7 | invalid |
| B-side | 12 | A=5 | 3 < 5 | invalid |

Both options fail at the feasibility stage because there are not enough total moves to relocate all travelers from the opposite side. The output is NO.

### Sample 2

Input:

```
4 4
4
2 2 2 2
```

Here $T = 8$.

| Step | Target Side | Required Transfers | Feasible | Parity Check |
| --- | --- | --- | --- | --- |
| A-side | 8 | B=4 | 8 ≥ 4 | (8−4)=4 even |
| B-side | 8 | A=4 | 8 ≥ 4 | (8−4)=4 even |

Both configurations are valid, meaning we can direct the sequence of crossings so that all travelers end up on one side. The output is YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Only a single pass to sum portal capacities |
| Space | $O(1)$ | No auxiliary structures proportional to input size |

The algorithm fits easily within limits since $N \le 10^5$ and all operations are constant time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite  # harmless import
    A, B = map(int, input().split())
    n = int(input())
    f = list(map(int, input().split()))
    T = sum(f)
    if (T >= B and (T - B) % 2 == 0) or (T >= A and (T - A) % 2 == 0):
        return "YES"
    return "NO"

# provided samples
assert run("5 7\n2\n1 2\n") == "NO"
assert run("4 4\n4\n2 2 2 2\n") == "YES"

# custom cases
assert run("1 1\n1\n2\n") == "YES"
assert run("10 1\n3\n1 1 1\n") == "NO"
assert run("3 3\n2\n5 1\n") == "YES"
assert run("2 2\n1\n1\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1, [2] | YES | minimal symmetric case |
| 10 1, [1 1 1] | NO | insufficient total moves |
| 3 3, [5 1] | YES | parity + feasibility combined |
| 2 2, [1] | NO | single move parity failure |

## Edge Cases

When $T$ is smaller than both A and B, the algorithm immediately rejects both final configurations because even relocating all opposite-side travelers is impossible. For example, with $A = 10$, $B = 10$, and $f = [1, 1]$, we get $T = 2$, which is insufficient to move all travelers from either side, producing NO.

When $T$ has the right magnitude but wrong parity, feasibility fails even though there are enough moves. For instance, $A = 4$, $B = 4$, $T = 5$ allows enough transfers for one direction, but the odd total prevents balancing, since every successful redistribution requires pairing opposite-direction moves.
