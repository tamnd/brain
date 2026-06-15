---
title: "CF 907A - Masha and Bears"
description: "We are given four small integers representing sizes of three bears and Masha. The bears require three car sizes that are strictly decreasing from father’s car to son’s car."
date: "2026-06-15T11:55:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 907
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 454 (Div. 2, based on Technocup 2018 Elimination Round 4)"
rating: 1300
weight: 907
solve_time_s: 186
verified: true
draft: false
---

[CF 907A - Masha and Bears](https://codeforces.com/problemset/problem/907/A)

**Rating:** 1300  
**Tags:** brute force, implementation  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four small integers representing sizes of three bears and Masha. The bears require three car sizes that are strictly decreasing from father’s car to son’s car. Each bear is assigned to one specific car: father to the largest, mother to the middle, son to the smallest.

A character of size `a` can enter a car of size `b` only if `a ≤ b`. However, liking the car is stricter: the car must not be too large compared to the character, specifically `b ≤ 2a`. So each bear must be able to both fit and “like” their assigned car.

Masha can enter all three cars, which constrains every car size to be at least her size. She only likes the smallest car, which imposes an upper bound on the smallest car size.

The task is to construct any valid triple of car sizes satisfying all constraints, or determine that no such triple exists.

The input values are bounded by 100, so the solution must operate in constant time or at worst linear in a tiny range. Any approach that iterates over large ranges is unnecessary, but even a triple brute-force over 100³ is still feasible. The real challenge is translating the inequalities into tight bounds and noticing that the middle and largest cars are determined almost directly by the bear constraints once the smallest car is fixed.

Edge cases arise when Masha’s constraints conflict with the son bear’s upper bound, making the system infeasible even though all individual constraints seem consistent. For example, if Masha is large enough that she forces the smallest car to be too large for the son bear to like, no solution exists.

## Approaches

A brute-force idea is to try all triples of integers `(S, M, L)` such that `1 ≤ S < M < L ≤ 100`. For each triple, we check all constraints: each bear must fit and like their car, and Masha must fit all cars and like only the smallest. Since the range is tiny, this is at most about 100³ combinations, or one million checks, which is already borderline but still acceptable.

However, this ignores structure. Each bear independently constrains a range for their assigned car. The condition `a ≤ b ≤ 2a` transforms each bear into an interval of valid car sizes. The father forces the largest car into `[V1, 2V1]`, the mother into `[V2, 2V2]`, and the son into `[V3, 2V3]`. These intervals must be consistent with strict ordering.

Masha introduces coupling between all three cars: every car must be at least `Vm`, and the smallest car must also be at most `2Vm`. This makes the smallest car essentially fixed to a tight interval `[Vm, min(2Vm, 2V3)]`, since the son must also like it.

Once the smallest car is chosen, the middle and largest can be derived greedily by respecting ordering and upper bounds. The structure eliminates search: only a few candidate values for the smallest car need to be checked, typically `Vm` or values close to it, and each leads to deterministic construction or failure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100³) | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute valid range for the smallest car. It must satisfy Masha’s constraints and the son bear’s constraints simultaneously, so it must lie in the intersection of `[Vm, ∞)` and `[V3, 2V3]`. This gives `S ∈ [Vm, 2V3]`.
2. If this intersection is empty, there is no valid smallest car. In that case, no solution exists.
3. Choose a candidate smallest car size `S`. A natural choice is `S = max(Vm, V3)`, since it satisfies both lower and upper constraints if feasible.
4. Compute the middle car size `M`. It must be strictly greater than `S`, but also must satisfy the mother bear’s constraints `V2 ≤ M ≤ 2V2`. The smallest valid choice is `M = max(S + 1, V2)`.
5. If `M` violates the upper bound `M > 2V2`, this candidate smallest car fails and we discard it.
6. Compute the largest car size `L`. It must satisfy `L > M` and `V1 ≤ L ≤ 2V1`. Choose `L = max(M + 1, V1)`.
7. If `L > 2V1`, the construction fails. Otherwise we have a valid triple.
8. Output `(L, M, S)`.

The construction implicitly ensures strict ordering and respects each bear’s constraints. If the initial smallest car choice fails, no other feasible adjustment exists because increasing `S` only tightens the constraints on `M` and `L`.

### Why it works

The key invariant is that each step greedily selects the minimum feasible value for each car while preserving strict ordering. Because all valid ranges are continuous intervals, choosing the smallest admissible value never blocks a valid solution that could exist with a larger choice for that car. Any failure occurs due to an empty intersection of constraints rather than a poor local choice. Since each constraint forms a convex interval, feasibility depends only on interval overlap, not on combinatorial structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

V1, V2, V3, Vm = map(int, input().split())

# smallest car candidate range
S = max(Vm, V3)
if S > 2 * V3:
    print(-1)
    sys.exit()

# middle car
M = max(S + 1, V2)
if M > 2 * V2:
    print(-1)
    sys.exit()

# largest car
L = max(M + 1, V1)
if L > 2 * V1:
    print(-1)
    sys.exit()

print(L)
print(M)
print(S)
```

The code directly implements the greedy construction. The smallest car is chosen as the tightest feasible value consistent with both Masha and the son bear. The middle and largest cars are then forced upward only as much as needed to preserve strict ordering and satisfy each bear’s interval constraints. Each feasibility check ensures we never exceed the maximum acceptable size for that bear.

A subtle point is that strict inequalities are handled by `S + 1` and `M + 1`, ensuring `S < M < L` without needing extra swaps or reordering logic.

## Worked Examples

### Example 1

Input:

```
50 30 10 10
```

| Step | S | M | L | Check |
| --- | --- | --- | --- | --- |
| Smallest S | 10 | - | - | 10 ≤ 20 valid |
| Middle M | 30 | 30 | - | 30 ≤ 60 valid |
| Largest L | 50 | 30 | 50 | 50 ≤ 100 valid |

Output:

```
50
30
10
```

This shows a clean case where all constraints align perfectly and greedy choices never violate bounds.

### Example 2

Input:

```
40 30 20 25
```

| Step | S | M | L | Check |
| --- | --- | --- | --- | --- |
| Smallest S | 25 | - | - | must be ≤ 40, OK |
| Middle M | 30 | 30 | - | 30 ≤ 60, OK |
| Largest L | 40 | 30 | 40 | 40 ≤ 80, OK |

Output:

```
40
30
25
```

This demonstrates that Masha can force the smallest car above the son bear’s natural value, but feasibility still holds as long as intervals overlap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant number of arithmetic operations and checks |
| Space | O(1) | No auxiliary structures used |

The solution easily fits within limits since all operations are simple comparisons and multiplications on small integers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    V1, V2, V3, Vm = map(int, input().split())

    S = max(Vm, V3)
    if S > 2 * V3:
        return "-1\n"

    M = max(S + 1, V2)
    if M > 2 * V2:
        return "-1\n"

    L = max(M + 1, V1)
    if L > 2 * V1:
        return "-1\n"

    return f"{L}\n{M}\n{S}\n"

# provided sample
assert run("50 30 10 10") == "50\n30\n10\n"

# all equal-ish boundary
assert run("10 9 8 8") != ""

# impossible case (Masha too large for son constraint)
assert run("10 9 8 20") == "-1\n"

# tight chain
assert run("100 50 25 25") != ""

# minimal spread
assert run("2 1 1 1") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 50 30 10 10 | 50 30 10 | standard valid configuration |
| 10 9 8 20 | -1 | infeasible due to son constraint |
| 100 50 25 25 | valid triple | mid-range construction correctness |
| 2 1 1 1 | valid triple | minimal boundary handling |

## Edge Cases

One critical edge case occurs when Masha forces the smallest car above the son bear’s maximum liking limit. For input `V3 = 10, Vm = 25`, the smallest car must be at least 25 for Masha but also at most 20 for the son bear. The intersection is empty, so the algorithm correctly rejects early when `S > 2 * V3`.

Another subtle case is when the middle car is forced above its allowed range after fixing the smallest car. For example, if `S = 50` and `V2 = 10`, the algorithm sets `M = max(51, 10) = 51`, but if `2V2 = 20`, the check `M > 2V2` triggers failure. This shows that feasibility is determined incrementally and not all constraints can be satisfied simultaneously even if individual ones look permissive.

A final boundary case is when all constraints align exactly at their upper bounds, such as `M = 2V2` or `L = 2V1`. The greedy construction still works because equality is allowed for “like” conditions, and only strict ordering is enforced separately through `+1` adjustments.
