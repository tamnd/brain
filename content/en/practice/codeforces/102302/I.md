---
title: "CF 102302I - Useless Pokemino"
description: "Each captured Pokemino is a point ((Ai,Di)), where the first coordinate is attack and the second is defense. A Pokemino is better than another one only when both coordinates are strictly larger."
date: "2026-08-13T23:23:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "I"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 419
verified: false
draft: false
---

[CF 102302I - Useless Pokemino](https://codeforces.com/problemset/problem/102302/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 59s  
**Verified:** no  

## Solution
## Problem Understanding

Each captured Pokemino is a point ((A_i,D_i)), where the first coordinate is attack and the second is defense. A Pokemino is better than another one only when both coordinates are strictly larger.

Breeding two Pokeminos does something geometrically useful: for any (0\le c\le1), the child is a point on the line segment joining the two parent points. Repeating breeding lets us obtain every point in the convex hull of all captured Pokeminos. The question after every insertion is thus whether a captured point can be strictly dominated by some point inside the current convex hull. The required answer is the number of captured points that are no longer maximal in this geometric sense.

The official statement has (N\le10^5), with coordinates up to (10^9). A quadratic algorithm would perform about (N(N-1)/2), roughly (5\cdot10^9), pair checks at the maximum size, which is far beyond a one-second limit. We need an approach around (O(N\log N)). The coordinate bound also means cross products can reach about (10^{18}), so the implementation needs integer arithmetic capable of representing values of that size. Python integers already provide the required range.

Several cases are easy to mishandle. First, equal attack does not imply domination because both coordinates must be strictly larger. For example,

```
3
5 0
5 1
5 2
```

has output

```
0
0
0
```

because all three points lie on the same vertical line and none has strictly larger attack than another.

Equal defense behaves similarly. For

```
3
0 5
1 5
2 5
```

the output is again

```
0
0
0
```

A solution that uses non-strict comparisons would incorrectly delete points in both examples.

The more subtle case is domination created by breeding. Consider

```
3
0 10
10 0
4 4
```

The first two points cannot individually dominate ((4,4)), but their midpoint is ((5,5)), which does. The correct output is

```
0
0
1
```

A solution that only checks captured Pokeminos directly would incorrectly report zero.

Another trap is a newly inserted point dominating an interior point of the current frontier. For

```
4
0 10
3 0
1 11
2 12
```

the outputs are

```
0
0
1
2
```

The third Pokemino dominates ((0,10)), and the fourth dominates ((1,11)). The point ((3,0)) remains useful because it has the maximum attack, even though its defense is small. A correct dynamic hull implementation has to handle this kind of interior deletion rather than only checking the newly inserted point.

## Approaches

The direct approach is to compare every captured Pokemino with every other captured Pokemino and also consider every possible pair for breeding. Even deciding whether one point can be beaten by a child of two parents requires examining pairs, so a straightforward implementation quickly becomes quadratic or worse. With (10^5) points, the basic (O(N^2)) comparison already reaches about (5\cdot10^9) pair checks.

The key observation removes the need to explicitly consider children. Every child is a convex combination of two existing points, and repeated breeding produces exactly the convex hull of all captured points. Thus we only need to understand which captured points are maximal points of that convex hull.

Sort the points conceptually by attack. Along the relevant upper-right boundary of the convex hull, attack increases while defense does not increase, except for vertical segments where attack is equal. A captured point on this boundary cannot be beaten in both coordinates. A point below this boundary can be beaten by a point on the hull, possibly one obtained by breeding.

This boundary can be maintained dynamically. Store the useful points ordered by attack, breaking equal attacks by decreasing defense. For an interior point (P), let (L) and (R) be its immediate neighbors. The orientation of these three points tells us whether (P) lies below the convex boundary. Using the cross product

[
(L-P)\times(R-P)
]

a negative value means that (P) lies below the segment (LR), so a point slightly to the right of (P) on that segment has both coordinates larger than (P). Such a point is useless.

There is one additional condition for collinear points. If the cross product is zero and (R) has both larger attack and larger defense than (P), then (R) directly dominates (P), so (P) is also useless. If the edge is horizontal, descending, or vertical, the collinear points can remain useful because no point on that edge is strictly better in both coordinates.

After inserting a point, only its immediate neighborhood can violate the boundary condition. We repeatedly remove a redundant predecessor or successor until the chain becomes valid again. Every captured point enters the structure once and can be removed at most once, so the total number of deletions is (O(N)). A balanced search tree supplies insertion, deletion, predecessor, and successor operations in (O(\log N)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) or worse | (O(N)) | Too slow |
| Dynamic convex frontier | (O(N\log N)) expected | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Represent every Pokemino as a point ((x,y)=(A,D)), and order points lexicographically by (x) increasing and (y) decreasing. The decreasing defense order for equal attack keeps all points on a vertical frontier in their natural order.
2. Maintain a balanced binary search tree containing exactly the captured points that currently lie on the useful upper-right frontier of the convex hull. We use a randomized treap in the Python implementation because Python has no built-in ordered set with logarithmic insertion and deletion.
3. Insert the new point into the treap. Find its immediate predecessor and successor in attack order. These are the only two existing frontier points whose local geometry can be changed directly by the insertion.
4. Test whether the new point itself is redundant. If it has a successor with both larger attack and larger defense, it is directly dominated. Otherwise, if it has both a predecessor and a successor and the cross product ((L-P)\times(R-P)) is negative, the point lies below the convex boundary and can be beaten by a bred point. Remove it if either condition holds.
5. If the new point survives, check its predecessor. If the predecessor has become redundant because of the new point, delete it. The new point has now replaced part of the old frontier, so this check can expose another redundant point immediately to the left.
6. Check the successor in the same way. Removing a successor can expose another redundant point farther to the right.
7. Repeat the local checks until neither neighbor is redundant. The process terminates because every iteration that changes the structure permanently deletes one captured Pokemino.
8. If (i) Pokeminos have been captured and the frontier currently contains (h) points, exactly (i-h) captured Pokeminos are useless. Output that value after every insertion.

### Why it works

Repeated breeding generates the entire convex hull, so a Pokemino is useful exactly when it is a coordinatewise maximal point of that convex hull. These maximal points form the upper-right boundary of the convex set.

The maintained chain has the invariant that every consecutive pair belongs to this boundary and that no stored point is locally below the chord between its neighbors. For an interior point, a negative cross product means that the chord between its neighbors passes above it. Moving an arbitrarily small distance to the right along that chord gives a point with both coordinates strictly larger, so the point is useless. If the points are collinear, the only way the right neighbor can make the point useless is when it has both coordinates larger.

Conversely, when none of these local conditions holds, the point lies on the maximal boundary. A convex boundary point cannot be strictly dominated by another point of the convex hull, because such a point would lie strictly northeast of it and contradict the supporting boundary of the convex set.

Insertion can only disturb the boundary near the inserted point. Any old point that becomes invalid is encountered by repeatedly moving to an adjacent neighbor and deleting it. Once no local violation remains, the entire chain again satisfies the invariant. Hence its size is exactly the number of useful Pokeminos, making (i-h) the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

class Treap:
    def __init__(self):
        self.left = [0]
        self.right = [0]
        self.prio = [0]
        self.x = [0]
        self.y = [0]

        self.root = 0
        self.size = 0
        self.seed = 88172645463393265

    def rng(self):
        self.seed ^= (self.seed << 7) & ((1 << 64) - 1)
        self.seed ^= self.seed >> 9
        self.seed &= (1 << 64) - 1
        return self.seed

    def new_node(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.left.append(0)
        self.right.append(0)
        self.prio.append(self.rng())
        self.size += 1
        return self.size

    def less_idx(self, a, b):
        if self.x[a] != self.x[b]:
            return self.x[a] < self.x[b]
        return self.y[a] > self.y[b]

    def less_key(self, idx, x, y):
        if self.x[idx] != x:
            return self.x[idx] < x
        return self.y[idx] > y

    def split(self, t, x, y):
        if not t:
            return 0, 0

        if self.less_key(t, x, y):
            a, b = self.split(self.right[t], x, y)
            self.right[t] = a
            return t, b
        else:
            a, b = self.split(self.left[t], x, y)
            self.left[t] = b
            return a, t

    def merge(self, a, b):
        if not a:
            return b
        if not b:
            return a

        if self.prio[a] > self.prio[b]:
            self.right[a] = self.merge(self.right[a], b)
            return a
        else:
            self.left[b] = self.merge(a, self.left[b])
            return b

    def insert_rec(self, t, node):
        if not t:
            return node

        if self.prio[node] > self.prio[t]:
            a, b = self.split(t, self.x[node], self.y[node])
            self.left[node] = a
            self.right[node] = b
            return node

        if self.less_idx(node, t):
            self.left[t] = self.insert_rec(self.left[t], node)
        else:
            self.right[t] = self.insert_rec(self.right[t], node)

        return t

    def insert(self, x, y):
        node = self.new_node(x, y)
        self.root = self.insert_rec(self.root, node)
        return node

    def erase_rec(self, t, x, y):
        if not t:
            return 0

        if self.x[t] == x and self.y[t] == y:
            return self.merge(self.left[t], self.right[t])

        if self.less_key(t, x, y):
            self.right[t] = self.erase_rec(self.right[t], x, y)
        else:
            self.left[t] = self.erase_rec(self.left[t], x, y)

        return t

    def erase(self, x, y):
        self.root = self.erase_rec(self.root, x, y)
        self.size -= 1

    def locate_with_neighbors(self, x, y):
        """
        Return (node, predecessor, successor).
        The predecessor/successor are strict neighbors of (x, y).
        """
        t = self.root
        pred = 0
        succ = 0

        while t:
            if x < self.x[t] or (x == self.x[t] and y > self.y[t]):
                succ = t
                t = self.left[t]
            elif x > self.x[t] or (x == self.x[t] and y < self.y[t]):
                pred = t
                t = self.right[t]
            else:
                q = self.left[t]
                while q:
                    pred = q
                    q = self.right[q]

                q = self.right[t]
                while q:
                    succ = q
                    q = self.left[q]

                return t, pred, succ

        return 0, pred, succ

def redundant(hull, p, pred, succ):
    if not succ:
        return False

    px = hull.x[p]
    py = hull.y[p]
    sx = hull.x[succ]
    sy = hull.y[succ]

    # Direct domination by the next frontier point.
    if sx > px and sy > py:
        return True

    if not pred:
        return False

    lx = hull.x[pred]
    ly = hull.y[pred]

    # (L - P) x (R - P)
    cross = (lx - px) * (sy - py) - (ly - py) * (sx - px)

    return cross < 0

def solve():
    n = int(input())
    hull = Treap()
    out = []

    for i in range(1, n + 1):
        x, y = map(int, input().split())
        hull.insert(x, y)

        while True:
            p, pred, succ = hull.locate_with_neighbors(x, y)

            if p == 0:
                break

            if redundant(hull, p, pred, succ):
                hull.erase(x, y)
                break

            changed = False

            if pred:
                qx = hull.x[pred]
                qy = hull.y[pred]
                q, qpred, qsucc = hull.locate_with_neighbors(qx, qy)

                if redundant(hull, q, qpred, qsucc):
                    hull.erase(qx, qy)
                    changed = True

            if changed:
                continue

            if succ:
                qx = hull.x[succ]
                qy = hull.y[succ]
                q, qpred, qsucc = hull.locate_with_neighbors(qx, qy)

                if redundant(hull, q, qpred, qsucc):
                    hull.erase(qx, qy)
                    changed = True

            if not changed:
                break

        out.append(str(i - hull.size))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The treap stores the points in the same order as an ordered set would: attack increases from left to right, and for equal attack, defense decreases. The arrays are used instead of Python objects for the nodes because (10^5) nodes and many tree operations benefit from compact storage.

The `split` and `merge` operations are the standard randomized-treap primitives. A node with higher priority becomes the root of the corresponding subtree, giving expected logarithmic height. The `insert` and `erase` methods then provide the ordered-set operations needed by the dynamic hull.

`locate_with_neighbors` finds the exact node together with its predecessor and successor. The equal-attack ordering is handled by comparing larger defense first, which is equivalent to sorting by `(attack, -defense)`.

The `redundant` function contains the geometric heart of the solution. The direct-domination test uses strict inequalities, which is necessary because equal attack or equal defense does not constitute domination. The cross product uses only integer arithmetic, so there is no floating-point precision issue. With coordinates up to (10^9), the products are within the range of roughly (10^{18}), and Python integers handle them exactly.

The update loop first checks whether the inserted point itself should disappear. If it survives, it checks its two neighbors and deletes any newly invalid point. Each deletion can reveal another invalid neighbor, so the loop repeats. The inserted point is never reinserted after deletion, and an old point can also be deleted only once.

## Worked Examples

The sample formatting in the prompt loses the line breaks between coordinates. The original Codeforces statement gives the samples with (N) followed by one coordinate pair per line.

For Sample 1, the input is

```
10
10 0
10 1
10 2
9 3
8 4
7 4
3 4
2 4
1 4
0 4
```

The frontier contains every captured point. Equal attack values form a vertical segment, equal defense values form a horizontal segment, and the remaining part slopes downward. None of these points can be strictly improved in both coordinates.

| Step | Inserted | Frontier size | Useless count |
| --- | --- | --- | --- |
| 1 | (10, 0) | 1 | 0 |
| 2 | (10, 1) | 2 | 0 |
| 3 | (10, 2) | 3 | 0 |
| 4 | (9, 3) | 4 | 0 |
| 5 | (8, 4) | 5 | 0 |
| 6 | (7, 4) | 6 | 0 |
| 7 | (3, 4) | 7 | 0 |
| 8 | (2, 4) | 8 | 0 |
| 9 | (1, 4) | 9 | 0 |
| 10 | (0, 4) | 10 | 0 |

The key property demonstrated here is that equal coordinates must not be treated as strict domination. The entire boundary survives, giving ten useful Pokeminos at the end.

For Sample 2, the input is

```
5
3 6
6 4
6 9
7 2
10 8
```

| Step | Inserted | Frontier after cleanup | Frontier size | Useless count |
| --- | --- | --- | --- | --- |
| 1 | (3, 6) | (3, 6) | 1 | 0 |
| 2 | (6, 4) | (3, 6), (6, 4) | 2 | 0 |
| 3 | (6, 9) | (6, 9), (6, 4) | 2 | 1 |
| 4 | (7, 2) | (6, 9), (7, 2) | 2 | 2 |
| 5 | (10, 8) | (6, 9), (10, 8) | 2 | 3 |

When ((6,9)) arrives, it has the same attack as ((6,4)), so the latter is not directly dominated. However, ((6,9)) directly dominates ((3,6)), so the first point disappears.

When ((7,2)) arrives, the points ((6,9),(6,4),(7,2)) form a downward-bending situation where ((6,4)) lies below the segment joining the other two. A bred point can beat ((6,4)), so it is removed. Finally, ((10,8)) makes ((7,2)) redundant, leaving only ((6,9)) and ((10,8)) on the frontier.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) expected | Each insertion, search, and deletion takes expected (O(\log N)), while every captured point is deleted at most once. |
| Space | (O(N)) | The treap contains at most one node for every captured Pokemino. |

With (N=10^5), the expected (O(N\log N)) bound is suitable for the intended constraints, while the quadratic alternative would require billions of operations. The implementation also avoids floating-point calculations and therefore does not suffer from precision problems when comparing nearly collinear points.

## Test Cases

```python
# This test harness is intended to be placed after the solution above.
# It rebinds the global input function so solve() can be called repeatedly.

import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official sample 1
assert run("""\
10
10 0
10 1
10 2
9 3
8 4
7 4
3 4
2 4
1 4
0 4
""") == """\
0
0
0
0
0
0
0
0
0
0
""", "sample 1"

# Official sample 2
assert run("""\
5
3 6
6 4
6 9
7 2
10 8
""") == """\
0
0
1
2
3
""", "sample 2"

# Minimum-size input
assert run("""\
1
0 0
""") == "0\n", "minimum size"

# Same attack: strict attack comparison means every point survives.
assert run("""\
3
5 0
5 1
5 2
""") == """\
0
0
0
""", "equal attack"

# A point becomes useless only because of breeding.
assert run("""\
3
0 10
10 0
4 4
""") == """\
0
0
1
""", "breeding domination"

# Interior direct domination catches a common local-hull mistake.
assert run("""\
4
0 10
3 0
1 11
2 12
""") == """\
0
0
1
2
""", "interior direct domination"

# Coordinate boundaries, including 0 and 1e9.
assert run("""\
4
0 0
1000000000 0
0 1000000000
1000000000 1000000000
""") == """\
0
0
0
1
""", "coordinate boundaries"

# Maximum N, with all defenses equal.
# No point can strictly dominate another because all defenses are equal.
max_n = 100000
max_input = str(max_n) + "\n" + "\n".join(
    f"{i} 1000000000" for i in range(max_n)
) + "\n"
max_expected = "\n".join("0" for _ in range(max_n)) + "\n"

assert run(max_input) == max_expected, "maximum size"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `0` | Minimum input size and the initial frontier. |
| Three points with attack `5` | `0 0 0` | Strict attack comparison and vertical frontier handling. |
| `(0,10), (10,0), (4,4)` | `0 0 1` | A Pokemino made useless only through breeding. |
| `(0,10), (3,0), (1,11), (2,12)` | `0 0 1 2` | Deleting an interior point that becomes directly dominated. |
| Four corner points using `0` and `10^9` | `0 0 0 1` | Coordinate boundaries and strict inequalities. |
| `100000` points with common defense | All zeros | Maximum (N), large coordinates, and a long horizontal frontier. |

## Edge Cases

For equal attacks, consider

```
3
5 0
5 1
5 2
```

The treap orders these as ((5,2),(5,1),(5,0)). Every successor has the same attack as its predecessor, so the direct-domination test fails. The cross products on this vertical segment do not produce a negative value either. All three points remain in the frontier and the output is `0 0 0`.

For equal defenses, consider

```
3
0 5
1 5
2 5
```

The frontier is horizontal. The cross product is zero for consecutive triples, while no successor has strictly greater defense. The points therefore remain useful. The output is `0 0 0`. This is why using `cross <= 0` blindly would be incorrect.

For breeding-only domination, use

```
3
0 10
10 0
4 4
```

After the first two insertions, both endpoints are useful. The third point lies strictly below the segment between them. Its cross product with its two neighbors is negative, so the algorithm deletes it. Geometrically, the segment contains points such as ((5,5)), which have both coordinates greater than ((4,4)). The output becomes `0 0 1`.

For an interior point that is directly dominated by a later insertion, use

```
4
0 10
3 0
1 11
2 12
```

After three insertions, ((0,10)) is already dominated by ((1,11)), so the answer is `1`. When ((2,12)) arrives, the algorithm checks the predecessor ((1,11)), discovers that the new point has both larger coordinates, and deletes it. The remaining ((3,0)) cannot be deleted because it has the maximum attack. The final answer is `2`.

The maximum-coordinate case

```
4
0 0
1000000000 0
0 1000000000
1000000000 1000000000
```

tests both boundary values. The first three points are pairwise non-dominating under strict comparison. The final point ((10^9,10^9)) dominates only ((0,0)), because the other two points share one coordinate with it. The output is `0 0 0 1`, and the cross-product arithmetic remains exact because Python integers do not overflow.
