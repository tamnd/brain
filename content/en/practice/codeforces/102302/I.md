---
title: "CF 102302I - Useless Pokemino"
description: "Think of every Pokemino as a point ((A,D)) in the plane, where attack is the horizontal coordinate and defense is the vertical coordinate."
date: "2026-08-14T04:36:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "I"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 229
verified: false
draft: false
---

[CF 102302I - Useless Pokemino](https://codeforces.com/problemset/problem/102302/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 49s  
**Verified:** no  

## Solution
## Problem Understanding

Think of every Pokemino as a point ((A,D)) in the plane, where attack is the horizontal coordinate and defense is the vertical coordinate. A Pokemino is useful if there is no point that Laersh owns, and no point that he can obtain by breeding, whose two coordinates are both strictly larger.

Breeding takes a weighted average of two points. Repeated breeding consequently gives exactly the convex hull of all captured points. So the real geometric question is this: among the captured points, which ones are not strictly dominated by any point of their convex hull?

The answer is described by the upper-right boundary of the convex hull. If we sort points by attack from left to right, the useful points form a convex chain. A new point can make several consecutive points on that chain useless, but it cannot make two separated regions disappear independently. This locality is what makes an online hull maintenance algorithm possible.

There are up to (10^5) captures, while attack and defense can each be as large as (10^9). A quadratic algorithm would already require about (10^{10}) operations, far beyond a one-second limit. We need roughly (O(N\log N)) total work. The coordinate size also means geometric tests should be performed with exact integer arithmetic. In C++ this requires 64-bit integers because a cross product can reach around (10^{18}); Python integers handle this range automatically.

Equal attack values need special treatment. Two Pokeminos with the same attack cannot strictly dominate one another because strict improvement is required in attack. For example,

```
3
5 1
5 3
5 2
```

has output

```
0
0
0
```

A careless implementation that keeps only the highest defense for each attack would incorrectly discard the other two Pokeminos. We sort equal attacks by decreasing defense so that this vertical group is represented correctly.

A second trap is strict inequality. If a Pokemino lies exactly on a decreasing segment joining two others, it is still useful. For example,

```
3
0 10
5 5
10 0
```

has output

```
0
0
0
```

The middle Pokemino can be bred from the endpoints, but the resulting point is exactly ((5,5)), not strictly better than it. An implementation that removes every collinear point would give the wrong answer.

A third trap is that a convex combination can dominate a Pokemino even when neither parent does so individually. For example,

```
3
0 10
10 0
5 4
```

has output

```
0
0
1
```

Breeding the first two Pokeminos with equal weights produces ((5,5)), which strictly dominates ((5,4)). Checking only direct pairwise dominance would miss this case.

Finally, a point can be useless simply because a later point dominates it directly. For

```
3
0 0
2 2
1 1
```

the output is

```
0
0
1
```

When ((1,1)) arrives, ((2,2)) is already owned and dominates it. A hull implementation that only checks the orientation of three points can miss this endpoint case unless it explicitly handles the first point of the maintained chain.

## Approaches

The most direct approach is to rebuild the geometric structure after every capture. For each prefix of the input, we could construct the convex hull of all currently owned Pokeminos, then determine which captured points are strictly dominated by some point of that hull. A standard hull construction costs (O(i\log i)) for a prefix of length (i), followed by a linear scan. Repeating this for every prefix costs (O(N^2\log N)). With (N=10^5), this is on the order of (10^{11}) comparison-level operations, so rebuilding from scratch is nowhere close to the one-second limit.

The brute-force approach is correct because the convex hull contains every point obtainable through repeated breeding. The problem is that consecutive prefixes differ by only one inserted point, yet the brute-force solution throws away all previous geometric work.

The key observation is that the useful points have a very rigid order. Sort them by increasing attack, and for equal attack by decreasing defense. Consider three consecutive candidates (L,P,R). If (P) lies strictly below the segment (LR), then some convex combination of (L) and (R) has exactly the same attack as (P) and strictly larger defense. Hence (P) is useless and can be deleted.

Using the cross product, this condition is

[
(L-P)\times(R-P)<0.
]

If the point is the first point in the ordered structure, there is no left neighbor. It is useless exactly when its immediate successor has both larger attack and larger defense. If it is the last point, it cannot be useless because no owned point has larger attack.

The crucial dynamic property is that inserting one point can only invalidate consecutive neighbors around that insertion position. Once a point is removed, it never needs to return, because future captures only enlarge the convex hull. Thus every Pokemino is inserted once and removed at most once. We can maintain the ordered chain in a balanced binary search tree, giving (O(\log N)) work per insertion or deletion.

Python does not provide a built-in balanced ordered set, so the implementation below uses a randomized treap. It supports insertion, deletion, predecessor, and successor in expected (O(\log N)) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Rebuild the hull for every prefix | (O(N^2\log N)) | (O(N)) | Too slow |
| Dynamic convex chain with treap | (O(N\log N)) expected | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Represent every Pokemino as a point ((x,y)=(A,D)), and order points by increasing (x). When two points have the same (x), order the one with larger (y) first. The treap uses the key ((x,-y)) to implement exactly this ordering.

This tie-breaking is necessary because equal-attack Pokeminos cannot strictly dominate one another through attack.
2. Maintain only the Pokeminos that are currently useful. In this ordered set, a point can have at most one predecessor and one successor, so whether it has become useless can be determined locally.
3. After inserting a new point (P), first check whether (P) itself is useless. If it is the first point and its successor (R) satisfies (R_x>P_x) and (R_y>P_y), then (R) directly dominates (P), so (P) is removed immediately.
4. If (P) has both a predecessor (L) and a successor (R), compute

## (L_x-P_x)(R_y-P_y)

(L_y-P_y)(R_x-P_x).
]

When this value is negative, (P) lies strictly below the segment (LR). The appropriate convex combination of (L) and (R) has the same attack as (P) and greater defense, so (P) is useless.
5. If the new point survives, repeatedly inspect its predecessor. Whenever that predecessor satisfies the same uselessness test, erase it. The insertion may have made several consecutive points obsolete, so this continues until the predecessor is valid.
6. Repeatedly inspect the successor in the same way. Erase every successor that has become useless.
7. After all invalid points have been removed, the treap contains exactly the useful Pokeminos. If (i) Pokeminos have been captured and the treap contains (s) points, the answer is (i-s).

The reason the local test is sufficient is the maintained convex-chain invariant. Consecutive retained points form the relevant upper-right boundary of the convex hull. A point below the segment connecting its two neighbors is reachable by breeding those neighbors and is strictly dominated. Conversely, if every retained interior point is on or above its neighboring chord and the endpoints satisfy the direct-dominance condition, no convex combination from the retained chain can create a strictly better point. Inserting a point can only replace a contiguous portion of this boundary, so deleting invalid predecessors and successors restores the invariant completely.

Collinear points are deliberately retained. A collinear point on a decreasing segment is not strictly dominated by the segment endpoints. Positive-slope collinear configurations are handled by the endpoint dominance test when the dominating point enters the maintained chain.

## Python Solution

```python
import sys

input = sys.stdin.readline
sys.setrecursionlimit(1_000_000)

class Node:
    __slots__ = ("x", "y", "key", "prio", "left", "right")

    def __init__(self, x, y, prio):
        self.x = x
        self.y = y
        self.key = (x, -y)
        self.prio = prio
        self.left = None
        self.right = None

seed = 712367821

def rng():
    global seed
    seed ^= (seed << 13) & 0xFFFFFFFF
    seed ^= seed >> 17
    seed ^= (seed << 5) & 0xFFFFFFFF
    seed &= 0xFFFFFFFF
    return seed

def rotate_right(root):
    child = root.left
    root.left = child.right
    child.right = root
    return child

def rotate_left(root):
    child = root.right
    root.right = child.left
    child.left = root
    return child

def insert(root, node):
    if root is None:
        return node

    if node.key < root.key:
        root.left = insert(root.left, node)
        if root.left.prio < root.prio:
            root = rotate_right(root)
    else:
        root.right = insert(root.right, node)
        if root.right.prio < root.prio:
            root = rotate_left(root)

    return root

def merge(left, right):
    if left is None:
        return right
    if right is None:
        return left

    if left.prio < right.prio:
        left.right = merge(left.right, right)
        return left
    else:
        right.left = merge(left, right.left)
        return right

def erase(root, key):
    if root is None:
        return None

    if key == root.key:
        return merge(root.left, root.right)

    if key < root.key:
        root.left = erase(root.left, key)
    else:
        root.right = erase(root.right, key)

    return root

def predecessor(root, key):
    ans = None
    while root is not None:
        if root.key < key:
            ans = root
            root = root.right
        else:
            root = root.left
    return ans

def successor(root, key):
    ans = None
    while root is not None:
        if root.key > key:
            ans = root
            root = root.left
        else:
            root = root.right
    return ans

def cross(a, p, b):
    return (a.x - p.x) * (b.y - p.y) - \
           (a.y - p.y) * (b.x - p.x)

def inside(root, p):
    left = predecessor(root, p.key)
    right = successor(root, p.key)

    if right is None:
        return False

    if left is None:
        return right.x > p.x and right.y > p.y

    return cross(left, p, right) < 0

def solve():
    n = int(input())
    root = None
    useful = 0
    answer = []

    for _ in range(n):
        x, y = map(int, input().split())
        p = Node(x, y, rng())

        root = insert(root, p)
        useful += 1

        if inside(root, p):
            root = erase(root, p.key)
            useful -= 1
        else:
            while True:
                left = predecessor(root, p.key)
                if left is None or not inside(root, left):
                    break
                root = erase(root, left.key)
                useful -= 1

            while True:
                right = successor(root, p.key)
                if right is None or not inside(root, right):
                    break
                root = erase(root, right.key)
                useful -= 1

        answer.append(str(_ + 1 - useful))

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The `Node` class stores the two coordinates, the ordering key, a randomized priority, and the two treap children. The key is `(x, -y)`, so smaller keys correspond to smaller attack and, for equal attack, larger defense.

The treap operations implement the ordered-set operations needed by the geometric algorithm. The rotations maintain the heap property of the randomized priorities while preserving the coordinate ordering.

`predecessor` and `successor` find the immediate neighbors of a point without traversing the whole structure. The `inside` function is the geometric core. A last point cannot be useless because nothing has greater attack. A first point needs the direct-dominance test. Every other point is tested using the cross product.

The insertion procedure first adds the point and increments the number of useful points. If the new point itself is invalid, it is immediately removed. Otherwise, its predecessor and successor may have become invalid because the new point changed the chain. The two while loops remove those consecutive invalid points.

The variable `useful` avoids needing a subtree-size field in the treap. Every insertion increments it once, and every deletion decrements it once. Since the total number of deletions is at most (N), the total number of treap operations remains (O(N\log N)) expected.

No floating-point arithmetic is used. The cross product is evaluated directly with integers, which avoids precision errors around collinear points. Python's arbitrary-precision integers also avoid overflow when coordinates are near (10^9).

## Worked Examples

For the first official sample, the input contains ten points whose geometry keeps every captured Pokemino on the useful boundary. The treap therefore never loses a point.

| Capture | Point | Action | Useful count | Useless count |
| --- | --- | --- | --- | --- |
| 1 | (10, 0) | Insert | 1 | 0 |
| 2 | (10, 1) | Insert | 2 | 0 |
| 3 | (10, 2) | Insert | 3 | 0 |
| 4 | (9, 3) | Insert | 4 | 0 |
| 5 | (8, 4) | Insert | 5 | 0 |
| 6 | (7, 4) | Insert | 6 | 0 |
| 7 | (3, 4) | Insert | 7 | 0 |
| 8 | (2, 4) | Insert | 8 | 0 |
| 9 | (1, 4) | Insert | 9 | 0 |
| 10 | (0, 4) | Insert | 10 | 0 |

The equal-attack points at (x=10) remain simultaneously useful because none of them can be strictly improved in attack. The rest of the points form a non-increasing defense chain as attack increases, so no convex combination creates a strictly better point. The output is ten zeroes.

For the second official sample,

```
5
3 6
6 4
6 9
7 2
10 8
```

the important changes happen when the fourth and fifth points are inserted.

| Capture | Point | Removed points | Useful count | Useless count |
| --- | --- | --- | --- | --- |
| 1 | (3, 6) | none | 1 | 0 |
| 2 | (6, 4) | none | 2 | 0 |
| 3 | (6, 9) | none | 3 | 0 |
| 4 | (7, 2) | (6, 4) | 3 | 1 |
| 5 | (10, 8) | (7, 2), (3, 6) | 2 | 3 |

At the fourth insertion, `(6,4)` has neighbors `(6,9)` and `(7,2)`. Its cross product is negative, so it lies below their connecting segment and is obtainable with strictly greater defense at the same attack.

At the fifth insertion, `(7,2)` becomes invalid first. Once it is removed, `(3,6)` becomes the first point and its successor `(6,9)` directly dominates it. Thus three of the five captured Pokeminos are useless, giving the output

```
0
0
1
2
3
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) expected | Each point is inserted once and deleted at most once, with treap operations taking expected (O(\log N)). |
| Space | (O(N)) | The treap contains at most all (N) captured Pokeminos. |

For (N=10^5), (O(N\log N)) is suitable for the constraint, while rebuilding a hull for every prefix would require roughly quadratic work. The memory usage is linear and stays well below 256 MB.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py`. It executes that exact program, so the tests do not duplicate the implementation.

```python
# helper: run the submitted solution and return its output
import sys
import io
import subprocess

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()

# Official sample 1
sample1 = """\
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
"""
assert run(sample1) == "\n".join(["0"] * 10), "sample 1"

# Official sample 2
sample2 = """\
5
3 6
6 4
6 9
7 2
10 8
"""
assert run(sample2) == "\n".join(["0", "0", "1", "2", "3"]), "sample 2"

# Minimum-size input
assert run("1\n0 0\n") == "0", "single Pokemino"

# Equal attack values must all remain useful
same_attack = """\
4
5 0
5 100
5 50
5 1
"""
assert run(same_attack) == "\n".join(["0", "0", "0", "0"]), \
    "equal attack values"

# Direct dominance and positive-slope collinearity
positive_line = """\
3
0 0
2 2
1 1
"""
assert run(positive_line) == "\n".join(["0", "0", "1"]), \
    "direct dominance and insertion order"

# Convex combination can dominate without either parent doing so
convex = """\
3
0 10
10 0
5 4
"""
assert run(convex) == "\n".join(["0", "0", "1"]), \
    "convex combination"

# Maximum-size test with boundary coordinates.
# Every point has attack 0, so no point can have strictly greater attack.
n = 100000
lines = [str(n)]
for i in range(n):
    lines.append(f"0 {10**9 - i}")
large = "\n".join(lines) + "\n"
expected = "\n".join(["0"] * n)
assert run(large) == expected, "maximum-size equal-attack test"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `0` | Minimum input and empty-neighbor handling |
| Four points with attack `5` | `0 0 0 0` | Equal attacks and the custom ordering |
| `(0,0), (2,2), (1,1)` | `0 0 1` | Direct domination and the first-point boundary case |
| `(0,10), (10,0), (5,4)` | `0 0 1` | Domination created by breeding two Pokeminos |
| (100000) points with attack `0` | (100000) zeroes | Maximum input size, boundary coordinate, and performance |

## Edge Cases

For equal attacks, consider

```
3
5 1
5 3
5 2
```

The ordering inside the treap is `(5,3)`, `(5,2)`, `(5,1)`. No point has attack greater than `5`, so even though the defenses differ, none can be strictly dominated. The last point is automatically safe because it has no successor, while the equal-attack neighbors fail the direct-dominance condition because their successors do not have greater attack. The output is `0 0 0`.

For collinear points on a decreasing segment,

```
3
0 10
5 5
10 0
```

the middle point has cross product zero. The algorithm removes points only when the cross product is strictly negative, so `(5,5)` stays in the hull. Breeding the endpoints can reproduce `(5,5)`, but cannot produce a point strictly better in both coordinates. The output is `0 0 0`.

For convex domination,

```
3
0 10
10 0
5 4
```

the first two points remain useful. When `(5,4)` arrives, its predecessor is `(0,10)` and its successor is `(10,0)`. The cross product is

[
(-5)(-4)-(6)(5)=20-30=-10.
]

The point lies strictly below the segment joining its neighbors. Their midpoint is `(5,5)`, which has the same attack and larger defense, so `(5,4)` is removed and the answer becomes `1`.

For direct domination at an endpoint,

```
3
0 0
2 2
1 1
```

the point `(0,0)` is removed when `(2,2)` arrives because the successor is larger in both coordinates. The third point `(1,1)` is inserted after `(0,0)` has already disappeared, so `(2,2)` becomes its successor and directly dominates it. The output is `0 0 1`. This case explains why the first-point condition cannot be replaced by the cross-product test alone.

For the maximum-size boundary case, all (100000) points can have attack `0` and distinct defenses between `0` and `10^9`. Since strict domination requires larger attack, every point remains useful regardless of defense. The treap still performs one insertion per point, and no deletion occurs, so the algorithm stays within its expected (O(N\log N)) running time.
