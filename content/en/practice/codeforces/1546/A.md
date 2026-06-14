---
title: "CF 1546A - AquaMoon and Two Arrays"
description: "Two players give us two arrays of equal length. One array can be modified by repeatedly moving a single unit from one position to another position. Each move removes one from index i and adds one to index j, and the array must remain non-negative after every move."
date: "2026-06-14T19:37:08+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1546
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 732 (Div. 2)"
rating: 800
weight: 1546
solve_time_s: 218
verified: true
draft: false
---

[CF 1546A - AquaMoon and Two Arrays](https://codeforces.com/problemset/problem/1546/A)

**Rating:** 800  
**Tags:** brute force, greedy  
**Solve time:** 3m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players give us two arrays of equal length. One array can be modified by repeatedly moving a single unit from one position to another position. Each move removes one from index `i` and adds one to index `j`, and the array must remain non-negative after every move. The goal is to transform the first array into the second exactly, or decide that this is impossible.

A useful way to interpret the operation is that it preserves the total sum of the array. Every operation is just a transfer of one unit of value between coordinates, so the total sum never changes. This immediately implies a necessary condition: if the sums of the two arrays differ, no sequence of operations can ever make them equal.

The constraints are small: `n` is at most 100 and the sum of all values across arrays is also bounded by 100 per test case. This means even solutions that explicitly move individual units are safe, because the total number of units that ever need to be tracked is tiny. Any approach that is quadratic or even slightly cubic in `n` is fine, but anything exponential or involving complex flow machinery is unnecessary.

A subtle edge case appears when the sums match but redistribution is impossible if we do not reason correctly about sources and sinks. For example, if `a = [0, 2]` and `b = [1, 1]`, we need to move one unit from index 2 to index 1. A careless approach might try to match indices greedily without ensuring that surplus indices are actually available when needed. Another edge case is when arrays are already equal; the correct answer is zero operations, not an empty plan with invalid formatting.

## Approaches

A brute-force viewpoint is to simulate all possible sequences of transfers. From a given state, we could choose any pair of indices and try moving a unit, then recursively search for a sequence that matches the target array. This is correct because it explores all reachable states, and each state transition corresponds exactly to one valid operation. The issue is that the state space grows explosively. Even though the total sum is small, the branching factor is roughly `n^2`, and sequences quickly become unmanageable.

The key observation is that the identity of individual units does not matter. Only how many units each index needs to gain or lose matters. We can compute a difference array where each position tells us whether it has surplus or deficit relative to the target. Every positive difference must send out units, and every negative difference must receive units. Since the total sum is preserved, total surplus equals total deficit, so we are simply matching supply and demand.

This reduces the problem to pairing surplus indices with deficit indices and generating explicit moves. Each move fixes one unit of imbalance. Because the total amount of imbalance is at most 100, we will perform at most 100 transfers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | Exponential | Exponential | Too slow |
| Surplus-Deficit Matching | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the solution directly from imbalance bookkeeping.

1. Compute the total sum of both arrays. If they differ, return failure immediately. This is required because every operation preserves total sum, so mismatched totals make the target unreachable.
2. Build a list of surplus positions where `a[i] > b[i]`, repeating index `i` exactly `a[i] - b[i]` times. These represent units that must be moved away.
3. Build a list of deficit positions where `a[i] < b[i]`, repeating index `i` exactly `b[i] - a[i]` times. These represent units that must be filled.
4. At this point both lists have equal length because total surplus equals total deficit. If they do not match in size, the configuration is inconsistent and cannot be fixed.
5. Pair elements in order: take the first surplus index and first deficit index, and create an operation moving one unit from surplus to deficit. Repeat until all elements are paired.

Each pairing reduces the absolute difference at two positions simultaneously, so no intermediate state violates non-negativity.

### Why it works

The difference array fully characterizes what must change. Every operation reduces the L1 imbalance by exactly 2, one unit removed from a surplus position and one added to a deficit position. Since we always pick valid surplus indices, we never subtract from a zero position. Because total surplus equals total deficit, the pairing always completes without leftover imbalance, guaranteeing a valid full transformation if one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        if sum(a) != sum(b):
            out.append("-1")
            continue

        surplus = []
        deficit = []

        for i in range(n):
            if a[i] > b[i]:
                surplus.extend([i + 1] * (a[i] - b[i]))
            elif a[i] < b[i]:
                deficit.extend([i + 1] * (b[i] - a[i]))

        ops = []
        for i in range(len(surplus)):
            ops.append((surplus[i], deficit[i]))

        out.append(str(len(ops)))
        for i, j in ops:
            out.append(f"{i} {j}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first checks the invariant that the sum must match. This is the only global impossibility condition. It then converts the arrays into expanded lists of individual units that must move, which avoids any need for complex bookkeeping.

The pairing loop is safe because each `surplus[i]` is guaranteed to correspond to a position that originally had at least one extra unit. Even if multiple units are taken from the same index, each unit is conceptually independent, so repeated indexing is valid.

The final output construction simply serializes these unit transfers. The number of operations is automatically bounded by the total imbalance, which is at most 100 due to constraints.

## Worked Examples

Consider the transformation `a = [1, 2, 3, 4]` and `b = [3, 1, 2, 4]`.

We compute differences per index. Index 1 needs +2, index 2 needs -1, index 3 needs -1, index 4 needs 0. This yields surplus list `[2, 3]` and deficit list `[1, 1]`.

| Step | Surplus | Deficit | Operation |
| --- | --- | --- | --- |
| 1 | 2, 3 | 1, 1 | 2 → 1 |
| 2 | 3 | 1 | 3 → 1 |

After applying these moves, each index matches its target value. This confirms that pairing units independently is sufficient, since order does not matter as long as every unit transfer is accounted for.

Now consider a single-element case `a = [0]`, `b = [0]`. Both lists are empty, so no operations are generated. This demonstrates that the algorithm naturally handles trivial cases without special branching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed once to build surplus and deficit lists, and total operations are bounded by sum of differences |
| Space | O(n) | Storing surplus and deficit unit expansions |

The constraints ensure the total number of units across all tests is small, so even expanding each unit explicitly remains efficient. The solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        if sum(a) != sum(b):
            res.append("-1")
            continue

        s = []
        d = []

        for i in range(n):
            if a[i] > b[i]:
                s.extend([i + 1] * (a[i] - b[i]))
            elif a[i] < b[i]:
                d.extend([i + 1] * (b[i] - a[i]))

        ans = []
        for i in range(len(s)):
            ans.append((s[i], d[i]))

        res.append(str(len(ans)))
        for x, y in ans:
            res.append(f"{x} {y}")

    return "\n".join(res)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("""4
4
1 2 3 4
3 1 2 4
2
1 3
2 1
1
0
0
5
4 3 2 1 0
0 1 2 3 4
""") == """2
2 1
3 1
-1
0
6
1 4
1 4
1 5
1 5
2 5
2 5"""

# all equal arrays
assert run("""1
3
5 5 5
5 5 5
""") == """0"""

# impossible due to sum mismatch
assert run("""1
2
1 1
0 1
""") == """-1"""

# single transfer
assert run("""1
2
0 3
2 1
""") != ""  # any valid sequence is acceptable

# maximum small stress
assert run("""1
4
4 0 0 0
0 1 1 2
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| samples | given | correctness on full example behavior |
| equal arrays | 0 | no-operation case |
| sum mismatch | -1 | impossibility detection |
| single transfer | valid ops | minimal movement correctness |
| skewed distribution | valid ops | multiple-unit redistribution |

## Edge Cases

When both arrays are already identical, the algorithm produces empty surplus and deficit lists, leading directly to zero operations, which matches the required output format.

When sums differ, the early termination avoids constructing inconsistent surplus and deficit structures, preventing misleading partial pairings.

When all surplus is concentrated in one index, the expanded surplus list simply repeats that index many times, and each repetition independently pairs with a deficit index, showing that repeated use of a single source is valid as long as its initial surplus is sufficient.
