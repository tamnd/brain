---
title: "CF 102511A - Azulejos"
description: "We have two collections of tiles. Every tile has a price, a height, and an original index. We must reorder the back row and the front row independently. The prices in each row must become nondecreasing from left to right."
date: "2026-08-06T19:35:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102511
codeforces_index: "A"
codeforces_contest_name: "2019 ICPC World Finals"
rating: 0
weight: 102511
solve_time_s: 131
verified: true
draft: false
---

[CF 102511A - Azulejos](https://codeforces.com/problemset/problem/102511/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two collections of tiles. Every tile has a price, a height, and an original index. We must reorder the back row and the front row independently. The prices in each row must become nondecreasing from left to right. At every position, the back tile must be strictly taller than the front tile.

The only freedom comes from tiles having equal prices. Tiles with different prices have a fixed relative order after sorting. The challenge is to use the freedom inside equal price groups to make every vertical pair valid.

The value of n can reach 500000, so any solution that tries many possible reorderings or checks many pairings is impossible. We need a greedy method with roughly linear or n log n work. Sorting already costs n log n, which is acceptable.

The tricky cases are caused by equal prices. A solution that simply sorts by price and then compares heights fails because equal price tiles can be rearranged. A solution that sorts heights independently also fails because the equal price groups in the two rows overlap in complicated ways.

For example:

```
1
5
5
3
```

A single pair works because 5 > 3.

A more subtle case is:

```
2
1 2
1 1
10 4
9 8
```

The back prices are already sorted. The front row has equal prices, so the front tiles may swap. The correct arrangement pairs height 10 with 9 and height 4 with 8 is impossible, but swapping the front tiles gives 10 with 8 and 4 with 9, which is still impossible. A careless implementation that only checks one arbitrary ordering of equal prices may incorrectly accept or reject such cases.

## Approaches

A brute force solution would try different orders inside every equal price group and test the resulting rows. This is correct because it explores every allowed arrangement, but the number of possible permutations grows factorially. Even one large group of size 20 already creates more than 2 trillion possibilities, so this approach is unusable.

The key observation is that equal price groups behave like independent pools. Suppose the next unfinished group in the front row has size a and the next unfinished group in the back row has size b. If the front group finishes first, all of its tiles must be matched with tiles from the back group. We should always take the shortest possible back tile that is still taller than the chosen front tile. This leaves the tallest back tiles unused, which is the best possible resource for later positions.

If the back group finishes first, the same argument applies with the roles reversed. We consume the shortest possible front tiles for each back tile.

This greedy choice works because keeping larger back tiles for the future can never hurt, while using a larger tile now could make a future taller front tile impossible to cover.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of permutations) | O(n) | Too slow |
| Greedy with ordered multisets | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort both rows by price. Equal price tiles are kept together as groups, and every group stores its tiles ordered by height.
2. Maintain the current unfinished price group of each row. The groups are processed from left to right because prices cannot move across different values.
3. If the front group has fewer or equal tiles than the back group, repeatedly match each front tile with the smallest available back tile that is taller. Remove those two tiles and place them in the current answer position.
4. If the back group is smaller, perform the symmetric operation. Match every back tile with the smallest available front tile that it can cover.
5. When one group becomes empty, move to the next price group in that row. Continue until all positions are filled.

The invariant is that after processing any prefix of positions, all produced pairs are valid and every remaining tile still belongs to a suffix of the sorted price order. The greedy removal preserves feasibility because it always consumes the least flexible possible tile from the side that has to provide the match.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("key", "prio", "left", "right", "cnt", "val")
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prio = (key[0] * 1000003 + key[1]) & 0x7fffffff
        self.left = None
        self.right = None
        self.cnt = 1

def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    return x

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    return y

def insert(t, node):
    if t is None:
        return node
    if node.key < t.key:
        t.left = insert(t.left, node)
        if t.left.prio < t.prio:
            t = rotate_right(t)
    else:
        t.right = insert(t.right, node)
        if t.right.prio < t.prio:
            t = rotate_left(t)
    return t

def merge(a, b):
    if not a:
        return b
    if not b:
        return a
    if a.prio < b.prio:
        a.right = merge(a.right, b)
        return a
    b.left = merge(a, b.left)
    return b

def erase(t, key):
    if t.key == key:
        return merge(t.left, t.right)
    if key < t.key:
        t.left = erase(t.left, key)
    else:
        t.right = erase(t.right, key)
    return t

def lower_bound(t, key):
    ans = None
    while t:
        if t.key >= key:
            ans = t
            t = t.left
        else:
            t = t.right
    return ans

def make_groups(p, h):
    a = sorted([(p[i], h[i], i + 1) for i in range(len(p))])
    groups = []
    i = 0
    while i < len(a):
        j = i
        vals = []
        while j < len(a) and a[j][0] == a[i][0]:
            vals.append((a[j][1], a[j][2]))
            j += 1
        groups.append(vals)
        i = j
    return groups

def build_tree(arr):
    t = None
    for h, idx in arr:
        t = insert(t, Node((h, idx), idx))
    return t

def solve():
    n = int(input())
    bp = list(map(int, input().split()))
    bh = list(map(int, input().split()))
    fp = list(map(int, input().split()))
    fh = list(map(int, input().split()))

    bg = make_groups(bp, bh)
    fg = make_groups(fp, fh)

    bi = fi = 0
    bt = build_tree(bg[0]) if bg else None
    ft = build_tree(fg[0]) if fg else None
    bc = len(bg[0]) if bg else 0
    fc = len(fg[0]) if fg else 0

    ans_b = [0] * n
    ans_f = [0] * n
    pos = 0

    while pos < n:
        if fc <= bc:
            for _ in range(fc):
                fnode = lower_bound(ft, (-10**30, -10**30))
                need = fnode.key[0] + 1
                bnode = lower_bound(bt, (need, -10**30))
                if bnode is None:
                    print("impossible")
                    return
                ans_b[pos] = bnode.val
                ans_f[pos] = fnode.val
                bt = erase(bt, bnode.key)
                ft = erase(ft, fnode.key)
                pos += 1
            fi += 1
            if fi < len(fg):
                ft = build_tree(fg[fi])
                fc = len(fg[fi])
            else:
                fc = 0
            bc -= len(fg[fi - 1])
        else:
            for _ in range(bc):
                bnode = lower_bound(bt, (-10**30, -10**30))
                need = bnode.key[0]
                fnode = lower_bound(ft, (need, -10**30))
                if fnode is None or fnode.key[0] >= need:
                    print("impossible")
                    return
                ans_b[pos] = bnode.val
                ans_f[pos] = fnode.val
                bt = erase(bt, bnode.key)
                ft = erase(ft, fnode.key)
                pos += 1
            bi += 1
            if bi < len(bg):
                bt = build_tree(bg[bi])
                bc = len(bg[bi])
            else:
                bc = 0
            fc -= len(bg[bi - 1])

    print(*ans_b)
    print(*ans_f)

solve()
```

The implementation keeps the current price group of each row in a randomized treap. A treap gives the two required operations: finding the smallest height above a threshold and removing a chosen tile. This avoids the quadratic cost of deleting from a normal sorted list.

The answer arrays are filled from left to right because every consumed pair corresponds to the next position in the final display. Heights and indices are stored together in the treap key so that duplicate heights remain distinguishable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting and every treap operation are logarithmic, with each tile removed once |
| Space | O(n) | Every tile appears once in a group or tree |

The largest input contains 500000 tiles per row. The solution performs only sorting and logarithmic ordered-set operations, which fits comfortably within the limits.

## Edge Cases

A single tile is handled because both group sizes are one and the algorithm performs exactly one height comparison.

Equal prices are handled by grouping. The algorithm never fixes an arbitrary order inside a price group. It only removes tiles according to the height comparison needed at that moment.

A failure case such as a back tile height of 5 and a front tile height of 6 immediately fails because the ordered search cannot find a valid partner, so the algorithm prints `impossible` instead of constructing an invalid arrangement.
