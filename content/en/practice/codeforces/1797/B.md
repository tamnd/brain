---
title: "CF 1797B - Li Hua and Pattern"
description: "We are given an $n times n$ grid where each cell is either 0 or 1, representing two colors. We are also given a fixed number $k$ of moves. A single move flips the color of exactly one chosen cell."
date: "2026-06-09T09:56:12+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1797
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 864 (Div. 2)"
rating: 1100
weight: 1797
solve_time_s: 81
verified: true
draft: false
---

[CF 1797B - Li Hua and Pattern](https://codeforces.com/problemset/problem/1797/B)

**Rating:** 1100  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid where each cell is either 0 or 1, representing two colors. We are also given a fixed number $k$ of moves. A single move flips the color of exactly one chosen cell. We may choose the same cell multiple times, so every move is independent and only toggles a bit.

The goal is not to reach an arbitrary configuration but to end in a very specific structural condition: the grid must become identical to its version rotated by $180^\circ$. This means that for every cell $(i, j)$, its value must match the cell $(n-1-i, n-1-j)$.

The key difficulty is that we must perform exactly $k$ flips, not “at most $k$”. Extra flips cannot be discarded, so if we fix the symmetry early, remaining operations must still be usable without breaking the condition.

The constraints suggest a linear scan per test case is sufficient. The total $n$ over all tests is at most $10^3$, so an $O(n^2)$ solution is easily fast enough. Anything involving repeated simulation of operations or searching over subsets is unnecessary.

A subtle edge case appears when the grid is already symmetric. In that case, the answer depends entirely on whether we can waste exactly $k$ operations while preserving symmetry. Another edge case arises when $n$ is odd and the center cell exists alone under rotation; flipping it affects only itself, which changes parity constraints on usable moves.

## Approaches

A brute-force idea would try to simulate all sequences of $k$ flips and check if any sequence leads to a symmetric grid. This is clearly infeasible since each move doubles the state space and the grid itself already has $2^{n^2}$ states. Even a more restrained search that only considers subsets of flipped cells leads to combinatorial explosion.

The key observation is that symmetry under $180^\circ$ partitions the grid into disjoint pairs of cells $(i, j)$ and $(n-1-i, n-1-j)$, except possibly the center cell when $n$ is odd. Each pair must end up equal. For a mismatched pair, exactly one flip is needed to fix them, because flipping either cell makes them match. Thus each pair contributes a forced cost of 0 or 1 operation depending on whether it is already equal.

Let $d$ be the number of mismatched symmetric pairs. We must spend at least $d$ operations to fix all pairs. After fixing symmetry, any further operations must preserve symmetry. A symmetric state allows two kinds of neutral operations: flipping both cells of a pair twice, or flipping any pair an even number of times, and for the center cell (if it exists), each flip toggles symmetry directly.

This reduces the problem to a parity question: after reaching a symmetric configuration, we must check whether we can distribute the remaining $k - d$ operations without breaking symmetry. Each symmetric operation effectively costs 2 flips for pairs, while the center cell costs 1 flip per toggle. Thus the ability to absorb extra moves depends on whether we have at least one “free parity channel”.

If $n$ is odd, the center cell gives a direct parity adjustment, so any number of remaining moves is usable. If $n$ is even, operations must come in pairs, so the remaining moves must be even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | exponential | Too slow |
| Optimal | $O(n^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Pair each cell $(i, j)$ with $(n-1-i, n-1-j)$. Count how many pairs differ. Each differing pair represents a mandatory correction that consumes one flip.
2. Let this count be $d$. If $d > k$, we already fail because even the minimum required flips exceed the budget.
3. Compute remaining operations $r = k - d$. These are moves that must be spent without breaking final symmetry.
4. If $n$ is even, check whether $r$ is even. If it is odd, we cannot distribute flips in symmetric-preserving ways, so answer is NO.
5. If $n$ is odd, the center cell allows absorbing any parity of remaining moves, so any $r \ge 0$ works.

Why it works

Each mismatched pair has exactly two cells that are linked by rotation. Fixing symmetry reduces independently per pair because flipping one cell changes only that pair’s mismatch status. Once all pairs match, the configuration is closed under rotation. From that point, valid operations must preserve symmetry, which forces flips to occur in symmetric patterns. For even $n$, all valid operations are paired, so total extra flips must be even. For odd $n$, the center cell acts as a parity sink, allowing any leftover operation count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    
    mismatches = 0
    
    for i in range(n):
        for j in range(n):
            ni, nj = n - 1 - i, n - 1 - j
            if (i, j) < (ni, nj):
                if a[i][j] != a[ni][nj]:
                    mismatches += 1
    
    if mismatches > k:
        print("NO")
        return
    
    rem = k - mismatches
    
    if n % 2 == 0:
        print("YES" if rem % 2 == 0 else "NO")
    else:
        print("YES")

t = int(input())
for _ in range(t):
    solve()
```

The grid is scanned once, and each symmetric pair is counted exactly once by enforcing an ordering between $(i, j)$ and its mirror $(ni, nj)$. This avoids double counting and avoids special casing the center during mismatch computation.

The decision logic then separates into two cases based on parity of $n$. The even case enforces that leftover moves must be pairable into symmetric-preserving operations. The odd case ignores parity because the center cell provides a single-cell toggle that absorbs any leftover odd move.

## Worked Examples

### Example 1

Input:

```
4 3
1 0 1 1
1 0 0 0
0 1 0 1
1 1 0 1
```

We compute mismatched pairs:

| Pair | Values | Match | Mismatches |
| --- | --- | --- | --- |
| (0,0)-(3,3) | 1 vs 1 | yes | 0 |
| (0,1)-(3,2) | 0 vs 0 | yes | 0 |
| (0,2)-(3,1) | 1 vs 1 | yes | 0 |
| (0,3)-(3,0) | 1 vs 1 | yes | 0 |
| (1,0)-(2,3) | 1 vs 1 | yes | 0 |
| (1,1)-(2,2) | 0 vs 0 | yes | 0 |
| (1,2)-(2,1) | 0 vs 1 | no | 1 |
| (1,3)-(2,0) | 0 vs 0 | yes | 0 |

So $d = 1$. Remaining $r = 2$. Since $n=4$ is even, $r$ must be even, and it is even, so answer is YES.

This trace shows that only one pair enforces a correction, and leftover operations can be paired without breaking symmetry.

### Example 2

Consider:

```
3 4
0 0 0
0 1 0
0 0 0
```

Here the only central structure is the middle cell, which maps to itself.

Mismatches:

| Pair | Values | Mismatches |
| --- | --- | --- |
| corners | all 0 | 0 |
| edges | all 0 | 0 |
| center | 1 | handled separately |

So $d = 0$, $r = 4$. Since $n=3$ is odd, any remainder is acceptable.

This demonstrates the key difference between even and odd dimensions: odd grids have a parity buffer at the center.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | each cell is visited once to form symmetric pairs |
| Space | $O(1)$ | only counters and input storage are used |

The total sum of $n$ across test cases is at most $10^3$, so scanning all grids remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        mismatches = 0
        for i in range(n):
            for j in range(n):
                ni, nj = n - 1 - i, n - 1 - j
                if (i, j) < (ni, nj):
                    if a[i][j] != a[ni][nj]:
                        mismatches += 1
        if mismatches > k:
            return "NO"
        rem = k - mismatches
        if n % 2 == 0:
            return "YES" if rem % 2 == 0 else "NO"
        return "YES"

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided samples
assert run("""3
4 0
1 1 1 1
0 0 0 1
1 0 1 0
1 1 1 1
4 3
1 0 1 1
1 0 0 0
0 1 0 1
1 1 0 1
5 4
0 0 0 0 0
0 1 1 1 1
0 1 0 0 0
1 1 1 1 1
0 0 0 0 0
""") == """NO
YES
YES"""

# custom cases
assert run("""1
1 1
1
""") == "YES"

assert run("""1
2 1
1 0
0 1
""") == "NO"

assert run("""1
2 2
1 0
0 1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 with odd k | YES | odd grid absorbs parity |
| 2x2 one flip impossible | NO | parity mismatch in even grid |
| 2x2 two flips possible | YES | even leftover works |

## Edge Cases

A critical edge case is when the grid is already symmetric but $k$ is small and evenness matters. For example:

```
n = 2, k = 1
1 0
0 1
```

There are zero mismatches, but $k=1$. Since $n$ is even, remaining parity is odd and cannot be absorbed symmetrically. The algorithm correctly outputs NO because $r=1$ is odd.

For odd $n$, consider:

```
n = 3, k = 1
0 0 0
0 1 0
0 0 0
```

No mismatches exist, but one operation remains. The center cell can be flipped, preserving rotational symmetry constraints in terms of feasibility of final state because it toggles itself without affecting pairs. The algorithm outputs YES, reflecting that leftover parity is always absorbable in odd dimensions.
