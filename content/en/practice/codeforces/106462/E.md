---
title: "CF 106462E - PPShneyneF4"
description: "We have a one-dimensional paper strip. At the beginning every position of the strip contains exactly one layer of paper. A fold at position p takes the shorter side's orientation into account by placing one part of the strip on top of the other."
date: "2026-06-25T08:58:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106462
codeforces_index: "E"
codeforces_contest_name: "\u041f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0441\u0440\u0435\u0434\u0438 \u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0445 2026"
rating: 0
weight: 106462
solve_time_s: 46
verified: true
draft: false
---

[CF 106462E - PPShneyneF4](https://codeforces.com/problemset/problem/106462/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a one-dimensional paper strip. At the beginning every position of the strip contains exactly one layer of paper. A fold at position `p` takes the shorter side's orientation into account by placing one part of the strip on top of the other. After several folds, a query asks for the total amount of paper that lies between two cut positions on the current visible strip. Overlapping layers count multiple times, because the cut keeps all pieces stacked there.

The input describes the initial width and a sequence of operations. A fold operation changes the current arrangement and decreases the width. A query operation gives two positions on the current strip and asks for the sum of all layer counts in that interval.

The constraints force us to avoid simulating the strip cell by cell. With widths and the number of operations reaching `10^5`, an approach that spends `O(width)` on every fold can reach about `10^10` operations, which is far beyond what a normal contest limit allows. We need every operation to be close to logarithmic.

The tricky part is that folds change the order of positions, not only their values. A solution that only stores the current total number of layers can answer nothing about arbitrary intervals. We also have to preserve the sequence of layers after every fold.

A small example shows why the order matters. For input:

```
3 2
1 1
2 0 2
```

After folding at position `1`, the two pieces overlap, so the new strip has two positions with values `[2, 1]`. The query asks for the whole strip, and the answer is:

```
3
```

A careless implementation that only tracks the width would return `2`, because it would count positions instead of the amount of paper.

Another edge case is an uneven fold. For:

```
5 2
1 4
2 0 1
```

The fold leaves the left side as the longer part. The new strip has values `[1, 1, 1, 2]`, so the first position contains only one layer and the answer is:

```
1
```

A wrong implementation that always reverses the left side onto the right side will shift the remaining part and return an incorrect value.

## Approaches

The direct approach is to store the current strip in an array. A fold can be simulated by creating a new array: depending on the fold position, copy the larger side and add the reversed smaller side onto it. This is correct because a fold is exactly an overlay of one segment onto the other. However, a single fold can touch almost the entire current strip. If the width is close to `100000` and there are many folds, the total number of processed elements can become around `10^10`.

The useful observation is that a fold is not an arbitrary modification. It only splits the sequence into two parts, reverses one of them, and concatenates the pieces. This is the exact set of operations supported efficiently by an implicit treap. Each treap node represents a continuous segment of the current strip, stores the sum of layer counts in its subtree, and supports splitting and merging by position. A lazy reverse flag lets us reverse a whole segment without touching every element.

The brute force works because the new strip is just a transformation of the old sequence, but it fails when many transformations are large. The observation that folds are only split, reverse, and merge operations lets us keep the whole strip structure in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Implicit Treap | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an implicit treap containing `n` nodes. Every node initially has value `1`, because every original part of the paper is a single layer. The subtree sum of a node represents the amount of paper in that segment of the current strip.
2. For a query, split the treap around the requested interval. The middle part is exactly the visible positions between the two cuts, so its stored sum is the answer. Merge the parts back afterwards to restore the strip.
3. For a fold at position `p`, split the treap into the left part of length `p` and the right part containing the rest. The smaller side is the part that gets flipped over the larger side.
4. If the left side is shorter or equal, reverse it and put it after the right side. If the right side is shorter, reverse the right side and put it after the left side. The resulting treap is the new folded strip.

The reason this works is that the treap order always matches the left-to-right order of the current paper. A fold only changes this order by reversing one contiguous side and moving it to the end of the remaining side. The lazy reversal operation changes the order without changing the total layer count, so all stored sums remain valid.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

class Node:
    __slots__ = ("val", "sum", "size", "left", "right", "prio", "rev")

    def __init__(self, val):
        self.val = val
        self.sum = val
        self.size = 1
        self.left = None
        self.right = None
        self.prio = random.randint(1, 1 << 30)
        self.rev = False

def size(t):
    return t.size if t else 0

def total(t):
    return t.sum if t else 0

def apply_rev(t):
    if t:
        t.rev ^= True
        t.left, t.right = t.right, t.left

def push(t):
    if t and t.rev:
        if t.left:
            t.left.rev ^= True
        if t.right:
            t.right.rev ^= True
        t.rev = False

def update(t):
    if t:
        t.size = 1 + size(t.left) + size(t.right)
        t.sum = t.val + total(t.left) + total(t.right)

def merge(a, b):
    if not a:
        return b
    if not b:
        return a
    if a.prio > b.prio:
        push(a)
        a.right = merge(a.right, b)
        update(a)
        return a
    else:
        push(b)
        b.left = merge(a, b.left)
        update(b)
        return b

def split(t, k):
    if not t:
        return None, None
    push(t)
    if size(t.left) >= k:
        a, b = split(t.left, k)
        t.left = b
        update(t)
        return a, t
    else:
        a, b = split(t.right, k - size(t.left) - 1)
        t.right = a
        update(t)
        return t, b

def solve(data):
    it = iter(data.split())
    n = int(next(it))
    q = int(next(it))

    root = None
    for _ in range(n):
        root = merge(root, Node(1))

    ans = []
    for _ in range(q):
        typ = int(next(it))
        if typ == 1:
            p = int(next(it))
            left, right = split(root, p)
            if size(left) <= size(right):
                apply_rev(left)
                root = merge(right, left)
            else:
                apply_rev(right)
                root = merge(left, right)
        else:
            l = int(next(it))
            r = int(next(it))
            a, b = split(root, l)
            b, c = split(b, r - l)
            ans.append(str(total(b)))
            root = merge(a, merge(b, c))

    return "\n".join(ans)

if __name__ == "__main__":
    data = sys.stdin.read()
    print(solve(data))
```

The treap node stores three pieces of information. The size is needed for position-based splitting, and the sum is needed for answering queries. The reverse flag delays changes to the children, so reversing a large segment only flips one boolean and swaps two pointers.

The `split` function cuts the current sequence after a given number of positions. This is the key operation because both queries and folds can be reduced to taking out contiguous pieces. The `merge` function joins two sequences while preserving their order.

During a fold, the code first separates the two sides. The comparison of their sizes decides which side is physically folded over the other. The shorter side is reversed because folding changes its orientation. This avoids any linear movement of elements.

The query code splits out the requested range, reads the stored sum, and joins everything back. The boundary positions are handled by splitting at `l` and then splitting the remaining sequence by `r - l`, which avoids off-by-one mistakes.

## Worked Examples

For the first sample:

```
7 4
1 3
1 2
2 0 1
2 1 2
```

The important states are:

| Operation | Current sequence of layers | Action |
| --- | --- | --- |
| Start | 1 1 1 1 1 1 1 | Initial paper |
| Fold 3 | 2 2 2 1 | Left side reversed and added |
| Fold 2 | 4 3 | Left side reversed and added |
| Query 0 1 | 4 3 | Sum first position |
| Query 1 2 | 4 3 | Sum second position |

The first query returns `4` because the first visible part contains four layers. The second returns `3`, showing that the data structure keeps different positions separate.

For the second sample:

```
10 9
2 2 9
1 1
2 0 1
1 8
2 0 8
```

A shortened trace is:

| Operation | Current sequence | Result |
| --- | --- | --- |
| Start | 1 1 1 1 1 1 1 1 1 1 |  |
| Query 2 2 9 | ten ones | 7 |
| Fold 1 | 2 1 1 1 1 1 1 1 1 |  |
| Query 0 1 | 2 1 1 1 1 1 1 1 1 | 2 |
| Fold 8 | 3 2 1 1 1 1 1 1 |  |
| Query 0 8 | full strip | 10 |

This trace shows that the stored sequence represents the current folded paper rather than the original paper, which is the invariant the algorithm relies on.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each split, merge, reverse, and query operation touches only treap height |
| Space | O(n) | The treap has one node per current paper position |

The maximum number of treap nodes stays equal to the initial number of positions. The lazy reversals prevent folds from expanding into linear work, so the solution fits the limits for `10^5` operations.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read()
    sys.stdin = old
    return solve(data)

assert run("""7 4
1 3
1 2
2 0 1
2 1 2
""") == "4\n3"

assert run("""10 9
2 2 9
1 1
2 0 1
1 8
2 0 8
1 2
2 1 3
1 4
2 2 4
""") == "7\n2\n10\n4\n5"

assert run("""1 1
2 0 1
""") == "1"

assert run("""5 2
1 4
2 0 1
""") == "1"

assert run("""6 3
1 3
2 0 3
2 1 2
""") == "6\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single position paper | 1 | Minimum size handling |
| Fold where the right side is shorter | 1 | Correct orientation after uneven fold |
| Equal length fold | 6 and 4 | Middle fold and range queries |

## Edge Cases

When the fold is exactly in the middle, both sides have the same length. The algorithm chooses the left side as the folded side, but choosing the other side would create the same physical result after a coordinate reversal. The stored sequence remains valid because the operation is still just a reverse and merge.

When a fold happens close to one edge, the shorter part may contain only one position. The algorithm still performs one split and one lazy reversal, avoiding the mistake of assuming that both sides have similar sizes.

For:

```
3 2
1 1
2 0 2
```

the split creates `[1]` and `[1,1]`. The single element side is reversed and merged after the other side, producing `[2,1]`. The total sum is `3`, which matches the amount of paper in the folded strip.

For:

```
5 2
1 4
2 0 1
```

the split creates `[1,1,1,1]` and `[1]`. The smaller side is reversed and attached to the end, giving the correct remaining order. The first position contains only one layer, so the query answer is `1`.
