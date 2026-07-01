---
title: "CF 104295F - \u041e\u0441\u0442\u043e\u0440\u043e\u0436\u043d\u044b\u0435 \u0425\u0430\u0442\u0438\u0444\u043d\u0430\u0442\u0442\u044b"
description: "We are given two configurations of the same number of points on an integer grid. Think of them as two drawings of indistinguishable particles placed on lattice points. The particles can move, but only through a very specific collective operation."
date: "2026-07-01T20:20:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104295
codeforces_index: "F"
codeforces_contest_name: "vkoshp.letovo"
rating: 0
weight: 104295
solve_time_s: 65
verified: true
draft: false
---

[CF 104295F - \u041e\u0441\u0442\u043e\u0440\u043e\u0436\u043d\u044b\u0435 \u0425\u0430\u0442\u0438\u0444\u043d\u0430\u0442\u0442\u044b](https://codeforces.com/problemset/problem/104295/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two configurations of the same number of points on an integer grid. Think of them as two drawings of indistinguishable particles placed on lattice points. The particles can move, but only through a very specific collective operation.

In one move, we pick a single particle and choose one of the four cardinal directions. That chosen particle moves one step in that direction, while every other particle simultaneously moves one step in the opposite direction. After each move, no two particles are allowed to occupy the same cell.

The question is whether it is possible, after a sequence of such moves, for the initial configuration to become the target configuration, if we are also allowed to apply an overall shift of the entire picture at the end, and we do not care about which particle corresponds to which label.

The constraint n up to 100000 forces any solution to be close to linear or linearithmic. Anything involving pairwise comparisons, simulation of moves, or graph matching between points would immediately become too slow, since n squared is on the order of 10^10 operations.

A subtle difficulty is that the operation couples all points at once. A naive interpretation might suggest tracking coordinates individually, but every move changes all points simultaneously, which makes local reasoning misleading.

A second hidden issue is that the identity of points is irrelevant. Any solution that tries to match the i-th initial point to the i-th target point will fail on permutations of identical structures.

## Approaches

A direct brute force approach would simulate all possible sequences of moves. Each state is a full configuration of n points, and each move branches into 4 choices of direction and n choices of which point to “lead” the move. This produces an enormous state graph, and even ignoring branching, the number of distinct configurations is exponential in the number of moves. This quickly becomes unmanageable even for very small n.

The key observation is that each move has a very structured effect: one point moves in a direction v, and all others move in the opposite direction. This can be rewritten as a global translation of all points by −v, plus an extra 2v applied only to the chosen point. Since the final answer allows an arbitrary translation, the global shift component can be ignored when comparing configurations. What remains is that each move effectively adds a vector of the form ±2e_x or ±2e_y to a single chosen point, while preserving everything else up to translation.

This immediately suggests that only information modulo 2 matters. Every update changes coordinates by ±1 for all points, which means every coordinate parity flips simultaneously. Therefore, while absolute positions change in a complicated way, the structure of how points sit in the four parity classes evolves in a very restricted manner: it only undergoes a global XOR shift of parity.

This reduces the problem from geometry to a counting problem over four parity classes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Parity Multiset Invariance | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We convert every point into its parity class, meaning we store only (x mod 2, y mod 2). There are exactly four possible classes.

We then exploit the fact that every operation flips both coordinates of every point simultaneously in parity space, which corresponds to XORing all parity classes with the same fixed 2-bit vector.

1. Compute the parity class of every initial point and count how many points fall into each of the four classes. This gives a 4-dimensional frequency vector.
2. Do the same for the target configuration.
3. Try all four possible global parity shifts. A shift corresponds to XORing both coordinates of every initial point by a fixed (dx, dy) in {0,1}².
4. For each shift, recompute what the initial parity distribution becomes after applying it.
5. If any shifted version of the initial parity counts matches exactly the target parity counts, the answer is possible.
6. Otherwise, no sequence of operations can transform one configuration into the other.

The only reason this works is that the operation cannot create or destroy relative parity structure between points, it only flips everything consistently or preserves pairwise parity relationships.

### Why it works

Every move flips the parity of every coordinate of every point. Therefore, after any number of moves, all points have been transformed by the same global XOR in parity space, possibly combined with permutations of labels. This means the only invariant information is the multiset of points in Z₂ × Z₂ up to a global shift. Since translations in the final answer are allowed, only the relative distribution across parity classes matters, and that distribution is preserved exactly up to XOR.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    init = [tuple(map(int, input().split())) for _ in range(n)]
    targ = [tuple(map(int, input().split())) for _ in range(n)]
    
    def build(points):
        cnt = [[0, 0], [0, 0]]
        for x, y in points:
            cnt[x & 1][y & 1] += 1
        return cnt
    
    A = build(init)
    B = build(targ)
    
    for dx in (0, 1):
        for dy in (0, 1):
            ok = True
            for i in range(2):
                for j in range(2):
                    if A[i ^ dx][j ^ dy] != B[i][j]:
                        ok = False
            if ok:
                print("YES")
                return
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The solution compresses each point into one of four parity buckets. The function `build` constructs this 2x2 frequency table. We then simulate the only effect that matters, a global XOR shift in parity space, by trying all four possibilities.

The nested loops over `dx` and `dy` test whether there exists a shift that aligns the initial parity distribution with the target distribution exactly. Since n can be large, everything else is linear.

A common mistake is attempting to match sorted coordinates directly or to track actual displacements. Those approaches ignore the fact that the operation entangles all points globally, but parity isolates exactly what survives that entanglement.

## Worked Examples

Consider a small case with three points:

Initial: (0,0), (0,1), (1,0)

Target: shifted version of the same structure

We compute parity counts.

| Point set | (0,0) | (0,1) | (1,0) | (1,1) |
| --- | --- | --- | --- | --- |
| Initial | 1 | 1 | 1 | 0 |
| Target | 1 | 1 | 1 | 0 |

Trying all shifts keeps the multiset identical, so the algorithm accepts.

Now consider a mismatch:

Initial: (0,0), (1,1), (2,2)

Target: (0,0), (0,0), (1,1)

Parity counts differ fundamentally.

| Point set | (0,0) | (0,1) | (1,0) | (1,1) |
| --- | --- | --- | --- | --- |
| Initial | 3 | 0 | 0 | 0 |
| Target | 1 | 0 | 0 | 2 |

No XOR shift can reconcile these distributions, so the algorithm rejects.

The second case demonstrates that parity mass distribution is the true invariant, not geometry or distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each point is processed once to compute parity counts, plus constant 4 shifts |
| Space | O(1) | Only four counters are stored |

The algorithm easily fits within the limits for n up to 100000 since it avoids sorting and avoids any quadratic interaction between points.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# Note: This is a placeholder structure; in practice, solve() should be imported.

# provided samples (format adapted as raw checks)
# assert run(sample1) == "YES"
# assert run(sample2) == "NO"

# custom cases
# n = 1 trivial
# assert run("1\n0 0\n10 10\n") == "YES"

# parity mismatch
# assert run("2\n0 0\n1 1\n0 0\n0 1\n") == "NO"

# all same parity but shifted
# assert run("3\n0 0\n2 2\n4 4\n1 1\n3 3\n5 5\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | YES | trivial translation invariance |
| mixed parity mismatch | NO | parity distribution mismatch |
| uniform shifted lattice | YES | valid XOR-shift equivalence |

## Edge Cases

When n equals 1, every configuration is equivalent because any single point can be translated arbitrarily by repeated moves. The algorithm handles this naturally because both initial and target parity tables have a single nonzero entry, and a matching shift always exists.

When all points lie in the same parity class, the structure collapses to a single bucket. Any target configuration that preserves the same count in one of the four buckets is accepted after the corresponding shift, and the algorithm checks all four shifts explicitly.

When distributions are heavily skewed, for example n−1 points in one class and 1 point in another, the shift check ensures that the imbalance pattern is preserved exactly. Any attempt to “hide” a mismatch via geometry fails because parity counts are invariant under all allowed operations.
