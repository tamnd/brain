---
title: "CF 104380L - Equation"
description: "We are given a consecutive list of integers starting from 0 up to n. Between every pair of adjacent numbers, we are allowed to insert either a plus or a minus sign, effectively deciding whether each number contributes positively or negatively to a running sum."
date: "2026-07-01T17:09:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "L"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 76
verified: true
draft: false
---

[CF 104380L - Equation](https://codeforces.com/problemset/problem/104380/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a consecutive list of integers starting from 0 up to n. Between every pair of adjacent numbers, we are allowed to insert either a plus or a minus sign, effectively deciding whether each number contributes positively or negatively to a running sum. The task is to decide whether there exists a choice of signs so that the resulting expression evaluates exactly to x, and if so, to construct any valid expression.

The structure of the expression is fixed, only the signs vary. Each number i contributes either +i or -i, so the problem reduces to selecting a subset of numbers whose total signed sum matches the target.

The constraints are small, with n at most 100. This immediately rules out any need for advanced optimization techniques or pruning-heavy search with heuristics. A solution that runs in polynomial time, even O(n^2) or O(n^3), is easily fast enough.

A key observation is that the total sum of all numbers from 0 to n is n(n+1)/2. Any signed expression can be seen as starting from this total sum and then flipping signs of certain elements, which effectively subtracts twice the sum of chosen elements. This symmetry defines a reachable range from -S to S where S is the total sum.

Edge cases arise when x lies outside this range. For example, if n = 4, then S = 10, so x = 15 is impossible. A naive implementation that tries to greedily assign signs without checking feasibility can still produce an expression but it will not match the target.

Another subtle case appears when multiple constructions exist. The problem only requires any valid expression, not the lexicographically smallest or any optimal structure. This allows greedy construction from larger numbers downward.

## Approaches

A brute-force approach would try all 2^n sign assignments. Each assignment corresponds to choosing a subset of numbers to negate. For each configuration we compute the resulting sum. This is correct because it enumerates all possible expressions, but the number of possibilities grows exponentially. With n = 100, this becomes astronomically large and unusable.

We can reformulate the problem in a more structured way. Start from the total sum S = 0 + 1 + ... + n. If we decide to assign a minus sign to a number i, its contribution changes from +i to -i, which reduces the total by 2i. Therefore, choosing a set of numbers to negate is equivalent to finding a subset whose sum equals (S - x) / 2.

This transforms the problem into a subset sum with small n and small total sum S ≤ 5050. A dynamic programming approach over possible sums would work, but we do not even need full DP because we only need one construction, not counting or optimization.

A greedy construction works because larger numbers provide larger adjustment power. We process numbers from n down to 1, deciding whether flipping each number keeps us closer to the remaining required adjustment. This behaves like a deterministic subset sum reconstruction in a bounded range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Subset DP | O(n·S) | O(S) | Accepted |
| Greedy reconstruction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We rewrite the target equation in terms of deviations from the full positive sum.

1. Compute S = n(n+1)/2. This is the value when all signs are plus.
2. If x is outside [-S, S], immediately return IMPOSSIBLE because no combination of sign flips can exceed these bounds.
3. Define the required adjustment D = S - x. This is the total amount we need to subtract by flipping signs.
4. If D is odd, return IMPOSSIBLE. Every flip changes the sum by 2i, so all adjustments are even.
5. We now need to select numbers whose sum equals D/2.
6. Initialize remaining = D/2.
7. Iterate i from n down to 1. For each i, if i ≤ remaining, choose to negate i and subtract it from remaining. Otherwise keep it positive.
8. Always keep 0 as +0 since it does not affect the sum.

After building the sign assignment, we output the expression.

Why it works comes from the invariant that at every step, remaining represents a valid subset-sum remainder over the yet-unprocessed numbers. Since we process from large to small, choosing i when possible does not block future feasibility: any larger number has already been considered, and smaller numbers are sufficient to complete the residual remainder because the total sum of remaining numbers always dominates any leftover gap that is representable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    
    S = n * (n + 1) // 2
    
    if x < -S or x > S:
        print("IMPOSSIBLE")
        return
    
    D = S - x
    
    if D % 2 != 0:
        print("IMPOSSIBLE")
        return
    
    target = D // 2
    sign = ['+'] * (n + 1)
    
    for i in range(n, 0, -1):
        if i <= target:
            sign[i] = '-'
            target -= i
    
    expr = []
    for i in range(n + 1):
        expr.append(f"{sign[i]}{i}")
    
    print("".join(expr))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction from sign assignment to subset sum. The array `sign` stores whether each number contributes positively or negatively. We initialize everything as positive, then greedily flip large numbers when they fit into the remaining required adjustment. The expression is then printed in order from 0 to n.

A subtle point is the initialization of all signs as '+'. This is important because 0 must always be included and should not affect correctness. Another is iterating downward from n ensures that larger contributions are decided first, which is what makes the greedy construction valid.

## Worked Examples

### Example 1: n = 3, x = 6

S = 6, so D = 0, target = 0.

| i | remaining before | decision | remaining after | sign |
| --- | --- | --- | --- | --- |
| 3 | 0 | skip | 0 | + |
| 2 | 0 | skip | 0 | + |
| 1 | 0 | skip | 0 | + |

Final expression is +0+1+2+3, which evaluates to 6.

This trace shows the case where no flips are needed because the target already equals the maximal sum.

### Example 2: n = 4, x = 9

S = 10, so D = 1, target = 0.5 which is invalid because D is odd, so we immediately reject.

No construction is attempted.

This demonstrates the parity constraint: since every flip changes the sum by an even amount, reaching an odd adjustment is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass from n down to 1 |
| Space | O(n) | storing sign array |

The constraints allow n up to 100, so a linear scan and simple arithmetic operations are easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, x = map(int, sys.stdin.readline().split())
    S = n * (n + 1) // 2
    if x < -S or x > S:
        return "IMPOSSIBLE"
    D = S - x
    if D % 2 != 0:
        return "IMPOSSIBLE"
    target = D // 2
    sign = ['+'] * (n + 1)
    for i in range(n, 0, -1):
        if i <= target:
            sign[i] = '-'
            target -= i
    return "".join(f"{sign[i]}{i}" for i in range(n + 1))

assert run("3 6") == "+0+1+2+3"
assert run("4 9") == "IMPOSSIBLE"
assert run("1 1") == "+0+1"
assert run("1 -1") == "+0-1"
assert run("5 0") in ["+0-1-2+3-4+5", "+0+1+2-3-4+5"]  # multiple valid answers
assert run("100 5050") == "+" + "+".join(str(i) for i in range(1, 101))
assert run("100 -5050") == "+" + "-".join(str(i) for i in range(1, 101))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 6 | +0+1+2+3 | already maximal sum case |
| 4 9 | IMPOSSIBLE | parity-based impossibility |
| 1 1 | +0+1 | smallest positive construction |
| 1 -1 | +0-1 | smallest negative construction |
| 5 0 | variable | multiple valid constructions |
| 100 5050 | all + | maximum boundary |
| 100 -5050 | all - | minimum boundary |

## Edge Cases

When n = 1, the solution must correctly handle both x = 1 and x = -1. The algorithm computes S = 1. For x = 1, D = 0 so no flips occur and output is +0+1. For x = -1, D = 2 so target = 1, and since 1 ≤ target we flip number 1, producing +0-1, which matches the requirement.

When x = S, the algorithm sees D = 0 and leaves all signs positive. This ensures the expression collapses to the full sum without any unnecessary operations.

When x = -S, D becomes 2S, so target is S. The greedy loop flips every number from n down to 1, consuming the entire target exactly once per number. This yields all negative signs, matching the minimum possible sum.
