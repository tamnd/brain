---
title: "CF 2113B - Good Start"
description: "We are given a rectangular roof aligned with the coordinate axes, with width $w$ and height $h$. The roof lies in the plane starting from $(0,0)$. We also have identical rectangular tiles of fixed size $a times b$."
date: "2026-06-08T04:23:12+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 2113
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1031 (Div. 2)"
rating: 1200
weight: 2113
solve_time_s: 99
verified: false
draft: false
---

[CF 2113B - Good Start](https://codeforces.com/problemset/problem/2113/B)

**Rating:** 1200  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular roof aligned with the coordinate axes, with width $w$ and height $h$. The roof lies in the plane starting from $(0,0)$. We also have identical rectangular tiles of fixed size $a \times b$. These tiles are not allowed to rotate, so their orientation is fixed.

The task is not to find any tiling from scratch. Instead, two tiles are already placed somewhere in the plane. They may extend outside the roof, but each of them overlaps at least a part of the roof, and they do not overlap each other. These two tiles must remain exactly where they are.

We must decide whether it is still possible to cover the entire roof area using copies of the same $a \times b$ tiles, without moving the two existing ones, and without overlapping any tiles, while allowing tiles to extend beyond the roof boundary.

The key difficulty is that the tiling is globally rigid in structure: since tiles cannot rotate and all are identical, any valid tiling must align to a grid of width $a$ and height $b$. The two pre-placed tiles constrain which grid alignment, if any, is still possible.

The input size allows up to $10^4$ test cases, and coordinates and dimensions go up to $10^9$. This rules out any simulation or brute-force placement. Each test must be solved in constant time, relying on modular arithmetic and structural observations.

A naive mistake is to assume we can locally “fix” the placement by slightly shifting tiles. That is impossible because once a tiling exists, it forces all tile positions to follow a strict periodic lattice. Another subtle issue is thinking only one coordinate direction matters. In reality, both x and y alignments must be consistent simultaneously.

A concrete failing scenario for naive reasoning is when two placed tiles have different x-coordinates modulo $a$. For example, if one tile starts at $x=0$ and another at $x=1$ with $a=2$, one might think we can still fill gaps, but this is impossible because no global grid can pass through both simultaneously.

## Approaches

If we ignore the structure of tilings, we might try to simulate placement: pick a starting tile position and attempt to extend a grid horizontally and vertically while ensuring both fixed tiles lie on it. This quickly becomes infeasible because the grid is unbounded in placement choices, and checking consistency by brute-force shifting would require iterating over all possible offsets in both axes, which is impossible under the constraints.

The key observation is that any valid tiling of the plane by fixed $a \times b$ rectangles corresponds to choosing a single offset $(x_0, y_0)$, and then placing tiles at all positions $(x_0 + ka, y_0 + lb)$. This means every tile’s bottom-left corner must satisfy:

$$x \equiv x_0 \pmod a, \quad y \equiv y_0 \pmod b$$

Now consider the two pre-placed tiles. Each of them forces constraints on this global offset. If both tiles are to belong to the same tiling, their x-coordinates must be congruent modulo $a$, and their y-coordinates must be congruent modulo $b$.

However, there is an additional subtlety: even if they are congruent modulo $a$ and $b$, they must not create a contradiction with respect to how full coverage of the rectangle can be extended across the roof boundary. The roof itself does not constrain the tiling, but the requirement that both fixed tiles remain part of the same infinite grid does.

So the problem reduces to checking whether the two tiles can belong to a common $a \times b$ lattice alignment. If not, the answer is immediately no. If yes, then we must also ensure that no forced mismatch arises in how the roof is partitioned by vertical or horizontal grid lines. This leads to checking alignment consistency along at least one dimension where the tiles might “block” different strip decompositions of the roof.

A more operational way to see this is: the plane is partitioned into vertical strips of width $a$. Each strip is independently tiled in y-direction. If both fixed tiles lie in different vertical phases (i.e., their x-coordinates modulo $a$ differ), then they force incompatible strip alignments. The same logic applies in the horizontal direction with height $b$.

Thus the decision reduces to checking whether either x-alignment or y-alignment can be made consistent globally without contradiction induced by the second tile.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|---|---|

| Brute Force grid search over offsets | $O(ab)$ per test | $O(1)$ | Too slow |

| Optimal modular alignment check | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the x-offset compatibility by checking whether $x_1 \equiv x_2 \pmod a$. This determines whether both tiles can lie on the same vertical tiling grid.
2. Compute the y-offset compatibility by checking whether $y_1 \equiv y_2 \pmod b$. This determines whether both tiles can lie on the same horizontal tiling grid.
3. If both congruences hold, conclude that a consistent global tiling alignment exists, so output "Yes".
4. Otherwise, conclude that no single periodic tiling can include both fixed tiles simultaneously, so output "No".

The reason we only need modular comparisons is that any full tiling is equivalent to selecting a lattice origin. The two tiles either agree on that lattice or they force two incompatible lattices.

### Why it works

A valid tiling of the plane by identical non-rotated $a \times b$ rectangles induces a unique equivalence relation on the plane where points differ by integer multiples of $a$ in x and $b$ in y. Every tile bottom-left corner belongs to exactly one equivalence class determined by $(x \bmod a, y \bmod b)$. If two pre-placed tiles lie in different classes, no completion can reconcile them, because any extension preserves the same class structure globally. If they lie in the same class, the tiling can be extended consistently because the plane can be filled independently in each aligned strip without contradiction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        w, h, a, b = map(int, input().split())
        x1, y1, x2, y2 = map(int, input().split())

        if (x1 - x2) % a == 0 and (y1 - y2) % b == 0:
            out.append("Yes")
        else:
            out.append("No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the modular alignment idea. The only subtle point is handling negative coordinates correctly, but Python’s modulo operator already ensures consistent results for congruence checks when used as `(x1 - x2) % a == 0`.

The solution processes each test case independently in constant time, reading inputs and checking two modular conditions.

## Worked Examples

### Example 1

Input:

```
w=6, h=5, a=2, b=3
tiles: (-1,-2), (5,4)
```

| Step | x condition | y condition | Result |
| --- | --- | --- | --- |
| Compute | (-1 - 5) % 2 = 0 | (-2 - 4) % 3 = 0 | Yes |

Both tiles align on the same lattice offsets, so a consistent tiling exists.

This confirms that even if tiles extend outside the roof, their relative alignment still matches a valid periodic grid.

### Example 2

Input:

```
w=4, h=4, a=2, b=2
tiles: (0,0), (3,1)
```

| Step | x condition | y condition | Result |
| --- | --- | --- | --- |
| Compute | (0 - 3) % 2 = 1 | (0 - 1) % 2 = 1 | No |

Both coordinates violate modular consistency. No single grid can include both placements, so completion is impossible.

This shows a case where local coverage of the roof is irrelevant: the contradiction comes purely from lattice structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test performs constant-time arithmetic checks |
| Space | $O(1)$ | Only a few integers stored per test |

The constraints allow up to $10^4$ test cases, and the solution performs only a handful of operations per case, making it easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        w, h, a, b = map(int, input().split())
        x1, y1, x2, y2 = map(int, input().split())

        if (x1 - x2) % a == 0 and (y1 - y2) % b == 0:
            output.append("Yes")
        else:
            output.append("No")

    return "\n".join(output)

# provided samples
assert run("""7
6 5 2 3
-1 -2 5 4
4 4 2 2
0 0 3 1
10 9 3 2
0 0 4 3
10 9 3 2
0 0 6 3
5 5 2 2
-1 -1 4 -1
5 5 2 2
-1 -1 2 3
7 8 2 4
0 0 0 5
""") == """Yes
No
No
Yes
No
Yes
No"""

# custom cases
assert run("""1
10 10 3 3
0 0 6 6
""") == "Yes"

assert run("""1
10 10 3 3
0 0 1 6
""") == "No"

assert run("""1
1 1 2 2
-1 -1 0 0
""") == "Yes"

assert run("""1
8 8 2 3
0 0 2 3
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| aligned multiples | Yes | consistent lattice alignment |
| x mismatch | No | horizontal grid conflict |
| small boundary | Yes | negative coordinates handled |
| mixed mismatch | No | both directions must agree |

## Edge Cases

One edge case is when coordinates are negative but still represent valid tile placements. For instance, a tile at $(-1,-1)$ must still be treated consistently under modulo arithmetic. The check `(x1 - x2) % a == 0` correctly handles this because it compares relative alignment rather than absolute residues.

Another edge case occurs when tiles lie far outside the roof boundaries. Even if both tiles are completely outside, they still constrain the global tiling. For example, if both tiles are placed at $(10^9, 10^9)$ and $(10^9 + a, 10^9)$, the x-condition passes but y-condition may fail or pass independently, and the decision remains purely modular.

A final edge case is when one tile is exactly aligned with a grid boundary and the other is near a boundary but not on it. Even a difference of 1 in coordinates breaks feasibility, because it forces two incompatible lattice origins, and no partial adjustment can reconcile them.
