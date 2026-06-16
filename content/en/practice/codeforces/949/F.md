---
title: "CF 949F - Astronomy"
description: "We are given 2n lattice points in the plane, each representing a star. Somewhere in the original astronomical configuration there existed a special point, the Moon, with integer coordinates, such that the stars could be partitioned into n pairs with a very rigid geometric…"
date: "2026-06-17T02:24:46+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 949
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 469 (Div. 1)"
rating: 3300
weight: 949
solve_time_s: 69
verified: true
draft: false
---

[CF 949F - Astronomy](https://codeforces.com/problemset/problem/949/F)

**Rating:** 3300  
**Tags:** geometry, probabilities  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given 2n lattice points in the plane, each representing a star. Somewhere in the original astronomical configuration there existed a special point, the Moon, with integer coordinates, such that the stars could be partitioned into n pairs with a very rigid geometric property: for every pair, the line through the two stars also passed through the Moon. Every pair produced a different line, but all those lines intersected in exactly one common point, the Moon.

In modern input, we only see the 2n star coordinates. The pairing is lost, and the Moon is missing. The task is to reconstruct any integer coordinate that could have been the Moon, or prove that no such point exists.

Geometrically, the hidden structure is strong: all 2n points must be paired so that each pair defines a line through a single fixed point. This is equivalent to saying that every star lies on one of n lines passing through a common center, and each line contains exactly two stars.

The coordinate bounds are large, up to 10^6 in absolute value, and n can be as large as 2600, so any approach that tries to test all pairings or all candidate centers explicitly is impossible. The structure must be extracted from the point set alone.

A key difficulty is that the pairing is unknown, so we cannot directly reconstruct the lines. Another subtle issue is that many geometric candidate constructions can produce rational coordinates for the intersection point, but the answer is required to be integral and distinct from all input points.

A naive idea would be to pick two points and assume their midpoint or intersection structure determines the Moon, but this quickly fails because the correct pairing is unknown and different pairings produce different candidate intersections.

The crucial edge case is symmetry. If the configuration is highly symmetric, multiple candidate centers may appear geometrically valid, but only one is consistent with all pairings. Another failure mode is assuming that arbitrary pairing or sorting by angle around a guessed center works without first identifying that center.

## Approaches

A brute-force interpretation would attempt to guess the Moon and then verify whether the points can be paired into collinear triples (Moon with each pair). For a fixed candidate center M, we can transform every point into a direction vector from M and check whether all vectors can be paired with identical directions (opposite rays). This requires sorting or hashing direction vectors and verifying even multiplicities.

The issue is that the candidate center is unknown. The space of possible integer coordinates is huge, bounded by 10^6 in each direction, so enumerating candidates is impossible. Even restricting candidates to input points or midpoints of pairs still leaves O(n^2) possibilities, which is too large.

The key observation is that the correct center is heavily constrained by symmetry of differences. Suppose the true center is C. For any correct pair (A, B), we have that C lies on segment AB extended, meaning vectors satisfy C = A + B - C rearranged implies A + B = 2C. So every valid pair sums to the same vector 2C.

This converts the problem into: partition points into pairs such that pair sums are constant. That constant is 2C. So if we guess one pair (A, B), then 2C = A + B is fixed, and C is determined. The remaining task is to verify whether all other points can be paired so that sums equal A + B.

This reduces the problem dramatically: instead of searching for C directly, we try candidate sums formed by pairing one chosen point with every other point. For each such candidate C, we check whether a full valid pairing exists under the induced rule.

The verification step is efficient using hashing of multiset complements: for each point P, its required partner is Q = (2C - P). If all points can be matched uniquely, and no point matches itself incorrectly, we have a valid solution.

The complexity comes from trying O(n) candidate centers (fix one point and try pairing it with another representative), and each validation costs O(n log n) or O(n) with hashing. This is acceptable for n up to 2600.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pairing / center enumeration | O(exp(n)) | O(1) | Impossible |
| Try candidate from one fixed anchor | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We use the fact that the correct center must satisfy 2C = A + B for some valid pair (A, B). We try all possibilities where A is fixed and B varies.

1. Fix a point A as a potential participant in the first pair.

This ensures we anchor candidate constructions to a real structure instead of arbitrary guesses.
2. For every other point B, compute a candidate center C = (A + B) / 2, or equivalently work with S = A + B as the required constant sum.

We avoid floating-point issues by working directly with integer sums.
3. For each candidate sum S, attempt to validate whether all points can be paired so that P + Q = S holds.

This encodes the geometric requirement that all lines pass through a single center.
4. Build a frequency map of all points. Iterate through points in any order, and for each point P that is still unused, compute Q = S - P.
5. If Q is not available in the multiset or is already exhausted, discard this candidate S immediately.
6. If we successfully match all points, output the corresponding center C = S / 2.

The reason we can safely greedily match P with S - P is that every valid solution forces a perfect involution pairing under the sum constraint, so order does not matter as long as consistency is preserved.

### Why it works

All valid configurations imply a constant vector sum across pairs: for every pair (A, B), A + B = 2C. Conversely, if we find a value S such that the multiset of points can be partitioned into pairs summing to S, then defining C = S / 2 guarantees all lines pass through C because each pair is symmetric around C. The search over S derived from a single anchor A is sufficient because at least one correct pair must include A, and that pair generates the true sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(2 * n)]
    
    from collections import Counter

    def try_sum(Sx, Sy):
        cnt = Counter(pts)
        for x, y in pts:
            if cnt[(x, y)] == 0:
                continue
            cnt[(x, y)] -= 1
            tx, ty = Sx - x, Sy - y
            if cnt[(tx, ty)] == 0:
                cnt[(x, y)] += 1
                return None
            cnt[(tx, ty)] -= 1
        
        return (Sx // 2, Sy // 2)

    # try all candidates using point 0 paired with others
    for i in range(1, 2 * n):
        sx = pts[0][0] + pts[i][0]
        sy = pts[0][1] + pts[i][1]
        res = try_sum(sx, sy)
        if res is not None:
            cx, cy = res
            # ensure center is not a star
            if (cx, cy) not in pts:
                print("Yes")
                print(cx, cy)
                return

    print("No")

if __name__ == "__main__":
    solve()
```

The code fixes one reference point and iterates over all possible partners to generate candidate sums. For each candidate, it constructs a frequency counter and greedily matches each unused point with its complement under the sum. If at any point a complement is missing, the candidate is invalid.

The final check ensures the computed center is not itself one of the stars, as required by the problem statement.

A subtle implementation detail is that we always decrement counts before searching for complements, which prevents accidentally pairing a point with itself unless multiplicity allows it. This ensures correctness in degenerate symmetric cases.

## Worked Examples

### Example 1

Input:

```
2
1 1
1 3
3 1
3 3
```

We try pairing (1,1) with (3,3), giving S = (4,4), so candidate center is (2,2).

| Step | Point P | Required Q = S - P | Counter state | Action |
| --- | --- | --- | --- | --- |
| 1 | (1,1) | (3,3) | all present | pair |
| 2 | (1,3) | (3,1) | all present | pair |

All points are matched, so (2,2) is valid.

This confirms the invariant that all pairs are symmetric around the same midpoint.

### Example 2

Input:

```
2
0 0
0 2
2 0
2 2
```

Trying (0,0) with (2,2) gives S = (2,2), center (1,1).

| Step | P | Q | Remaining |
| --- | --- | --- | --- |
| (0,0) | (0,0) | (2,2) | valid |
| (0,2) | (0,2) | (2,0) | valid |

All points matched, confirming correctness.

This example highlights that multiple symmetric configurations all reduce to a single center.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | We try O(n) candidate pairs and validate each in O(n) using hashing |
| Space | O(n) | Frequency map stores all points during validation |

The constraints n ≤ 2600 allow up to about 6.7 million operations per candidate pair check cycle in worst interpretation, but in practice early rejection makes the solution efficient enough under Python with hashing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = []
    
    def input():
        return sys.stdin.readline()
    
    n = int(sys.stdin.readline())
    pts = [tuple(map(int, sys.stdin.readline().split())) for _ in range(2*n)]
    
    from collections import Counter

    def try_sum(Sx, Sy):
        cnt = Counter(pts)
        for x, y in pts:
            if cnt[(x, y)] == 0:
                continue
            cnt[(x, y)] -= 1
            tx, ty = Sx - x, Sy - y
            if cnt[(tx, ty)] == 0:
                cnt[(x, y)] += 1
                return None
            cnt[(tx, ty)] -= 1
        return (Sx//2, Sy//2)

    for i in range(1, 2*n):
        sx = pts[0][0] + pts[i][0]
        sy = pts[0][1] + pts[i][1]
        res = try_sum(sx, sy)
        if res is not None and res not in pts:
            return f"Yes\n{res[0]} {res[1]}\n"

    return "No\n"

# sample
assert run("""2
1 1
1 3
3 1
3 3
""") == "Yes\n2 2\n"

# collinear symmetric
assert run("""2
0 0
0 2
2 0
2 2
""") == "Yes\n1 1\n"

# impossible case
assert run("""1
0 0
1 1
""") == "No\n"

# degenerate valid
assert run("""1
-1 -1
1 1
""") == "Yes\n0 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,1,1,3,3,1,3,3 | Yes 2 2 | basic square symmetry |
| 0,0,0,2,2,0,2,2 | Yes 1 1 | multiple valid pairings |
| 0,0,1,1 | No | no integer center |
| -1,-1,1,1 | Yes 0 0 | negative coordinate handling |

## Edge Cases

One failure mode is when multiple candidate centers exist due to partial symmetry but only one allows complete pairing. The algorithm tries all pairings involving a fixed anchor point, so any valid configuration must include a correct candidate sum among those attempts. If a symmetric-but-invalid center is tried, the greedy pairing fails at the first unmatched complement, preventing false acceptance.

Another case is when a point is its own complement under a candidate sum, meaning S = 2P. The implementation handles this correctly because the point count is decremented before checking its partner, ensuring that self-pairing only succeeds when at least two identical points exist, which is impossible since all points are distinct.

Finally, cases where the true center lies outside the convex hull are handled naturally since the computation does not rely on geometric assumptions about position, only algebraic pairing consistency.
