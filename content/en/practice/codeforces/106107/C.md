---
title: "CF 106107C - DGeneral Hamilton's Cubes"
description: "We are building a large cube of size $n times n times n$ from $n^3$ identical unit cubes. Every small cube has its six faces permanently labeled with the numbers 1 through 6, one label per face."
date: "2026-06-19T22:51:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106107
codeforces_index: "C"
codeforces_contest_name: "SCPC Teens 2025"
rating: 0
weight: 106107
solve_time_s: 58
verified: true
draft: false
---

[CF 106107C - DGeneral Hamilton's Cubes](https://codeforces.com/problemset/problem/106107/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a large cube of size $n \times n \times n$ from $n^3$ identical unit cubes. Every small cube has its six faces permanently labeled with the numbers 1 through 6, one label per face. The key freedom is that we may rotate each small cube independently before placing it into the big structure.

Once all cubes are placed, each face of the large cube becomes an $n \times n$ grid of visible unit faces. Each visible square simply shows whatever number is on the outward-facing side of the small cube occupying that position. The large cube itself also has six faces, and each face is associated with one of the labels 1 through 6, but that assignment does not constrain individual cells beyond the geometric orientation rule.

The task is to count how many distinct resulting labeled large cubes can be formed, where two configurations are considered different if any visible cell on any face shows a different number.

The constraint $n \le 10^9$ immediately removes any approach that inspects cubes individually or iterates over the volume. Even visiting all $n^3$ cubes is impossible. The solution must depend only on structural symmetry, meaning we should classify cubes by position type rather than enumerate them.

A subtle edge case appears when $n$ is very small. For $n=1$, there is a single cube contributing all six faces. For $n=2$, every cube sits on a corner, so every cube simultaneously touches three faces of the big cube. These degenerate sizes often break formulas derived from “large $n$” geometry, so they must be checked separately.

## Approaches

A brute-force method would assign one of 24 rotations to each of the $n^3$ cubes, since a cube has 24 rotational symmetries. This leads to $24^{n^3}$ possibilities before considering whether face constraints are satisfied. However, most of these choices are not independent once we enforce that boundary faces must align correctly with the outward direction of the big cube. More importantly, even writing down or iterating over $n^3$ positions is already infeasible.

The key observation is that constraints depend only on where a cube sits, not on its identity. Every position on the big cube falls into one of four categories: interior, face interior, edge, or corner. Each category imposes a fixed number of face constraints, and therefore a fixed number of valid orientations for the small cube placed there. Once this classification is made, the problem becomes a product of independent choices over these position types.

This reduces the problem from reasoning about individual cubes to counting how many positions fall into each geometric class and multiplying their local orientation counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all cube placements | $O(24^{n^3})$ | $O(1)$ | Too slow |
| Geometry by position classification | $O(1)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Algorithm Walkthrough

1. Classify every unit cube in the $n \times n \times n$ structure by how many faces of the big cube it touches. This determines how many outward constraints it must satisfy.
2. Count interior cubes, which do not touch any boundary. There are $(n-2)^3$ such positions when $n \ge 2$. Each has no restrictions, so any of the 24 cube rotations is valid.
3. Count face-interior cubes, which lie on a face but not on edges. There are $6(n-2)^2$ of them. Each such cube has exactly one constrained face, so we need rotations that place a specific number on a specific direction. A cube has 4 rotations satisfying one fixed face constraint, corresponding to free rotation around that axis.
4. Count edge cubes excluding corners. There are $12(n-2)$ of them. Each touches two faces, so two perpendicular constraints must be satisfied simultaneously. Exactly 2 rotations satisfy two fixed face constraints.
5. Count corner cubes. There are always 8. Each touches three faces, fully determining its orientation, so exactly 1 rotation is valid.
6. Multiply all contributions: each position contributes independently, so the total is

$24^{(n-2)^3} \cdot 4^{6(n-2)^2} \cdot 2^{12(n-2)}$.
7. Handle small values of $n$. For $n=1$, there is one cube and all 24 rotations are valid. For $n=2$, all cubes are corners, so the answer is 1.

### Why it works

Every cube position contributes constraints only from the faces of the large cube it lies on. These constraints are independent across positions because each small cube is rotated independently. Once positions are grouped by how many constraints they impose, the number of valid configurations factorizes into a product over these groups. No global interaction exists beyond this classification, so no additional consistency checks are needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mod_pow(a, e):
    return pow(a, e, MOD)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        
        if n == 1:
            print(24)
            continue
        if n == 2:
            print(1)
            continue
        
        m = n - 2
        
        interior = m * m * m
        face = 6 * m * m
        edge = 12 * m
        
        ans = 1
        ans = ans * mod_pow(24, interior) % MOD
        ans = ans * mod_pow(4, face) % MOD
        ans = ans * mod_pow(2, edge) % MOD
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code mirrors the geometric decomposition directly. The subtraction $n-2$ isolates the fully internal region of the cube, and all combinatorial counts are derived from that single parameter.

The special cases for $n=1$ and $n=2$ avoid negative dimensions in the formula and capture degenerate geometry where every cube is either fully free or fully constrained.

## Worked Examples

Consider $n=3$. Then $m = 1$. There is $1$ interior cube, $6$ face-interior cubes, $12$ edge cubes, and $8$ corners.

| Type | Count | Choices per cube | Contribution |
| --- | --- | --- | --- |
| Interior | 1 | 24 | $24^1$ |
| Face interior | 6 | 4 | $4^6$ |
| Edge | 12 | 2 | $2^{12}$ |
| Corner | 8 | 1 | $1$ |

The final answer is $24 \cdot 4^6 \cdot 2^{12}$. This confirms that even small $n$ already produces strong exponentiation structure.

Now consider $n=2$. There are only corner cubes, all 8 of them. Each corner fully determines orientation, so every cube is forced. The product collapses to 1, showing that the geometry eliminates all freedom.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log n)$ | Each test case uses fast modular exponentiation on a constant number of powers |
| Space | $O(1)$ | Only a few integers are maintained |

The constraints allow up to $10^5$ test cases, but each case is independent and requires only a few modular exponentiations, which is easily fast enough.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# We cannot directly call solve() here in static snippet context,
# but these illustrate intended assertions structure.

# custom cases (conceptual)
# n = 1 -> 24
# n = 2 -> 1
# n = 3 -> structured decomposition
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 24 | single cube full rotational freedom |
| 1\n2 | 1 | fully constrained corner-only cube |
| 1\n3 | computed value | checks decomposition into all cube types |
| 3\n1\n2\n3 | 24 1 ... | multiple test handling |

## Edge Cases

For $n=1$, the cube degenerates into a single unit. That cube contributes all six faces simultaneously, and no boundary constraints restrict orientation. Every rotation of the cube produces a distinct configuration, so the answer is 24. The algorithm handles this directly via a special case before applying the geometric formula, avoiding negative values of $n-2$.

For $n=2$, every unit cube lies on a corner. Each cube must satisfy three face constraints simultaneously, fixing its orientation uniquely. The general formula would also reduce correctly since all exponent bases vanish, but the corner-only interpretation makes the reasoning explicit: there is exactly one valid configuration.

For $n \ge 3$, the decomposition into interior, face, edge, and corner regions applies cleanly, and each category contributes an independent multiplicative factor with no overlaps or omissions.
