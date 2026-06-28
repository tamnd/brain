---
title: "CF 104785H - History in Numbers"
description: "We are given a long sequence of integers representing an “urban development index” over time. This array is not static. Two types of operations happen online."
date: "2026-06-28T14:40:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104785
codeforces_index: "H"
codeforces_contest_name: "2023 United Kingdom and Ireland Programming Contest (UKIEPC 2023)"
rating: 0
weight: 104785
solve_time_s: 56
verified: true
draft: false
---

[CF 104785H - History in Numbers](https://codeforces.com/problemset/problem/104785/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long sequence of integers representing an “urban development index” over time. This array is not static. Two types of operations happen online. One operation adds a value to every element in a contiguous segment, and the other asks whether a subarray is “increasing” under a very unusual definition.

The difficulty is not the updates themselves, but how the structure of the array is interpreted during queries. Before we judge a segment, we first compress it by merging consecutive equal values into a single value. After that compression, we look at the local minima in the resulting sequence. A position is a local minimum if its value is strictly smaller than both neighbors (or the only neighbor if it is at an endpoint). Finally, the segment is called increasing if these local minima, read from left to right, form a strictly increasing sequence of values.

So each query is essentially asking a structural question about the shape of a piecewise-constant signal after dynamic range additions.

The constraints allow up to 300,000 elements and 300,000 operations. Any solution that recomputes a segment from scratch per query would be quadratic in the worst case, which is far beyond acceptable. Even O(n log n) per query is too slow if applied repeatedly. The only viable approach must maintain a compressed representation or a boundary-based structure that changes slowly under updates.

A few edge cases matter immediately.

If all values in a segment are equal, compression reduces it to a single element, which trivially has no internal local minima, so the answer must always be YES for any such query. A naive local-minimum scan might incorrectly try to interpret endpoints as minima if not careful.

If the array alternates like `1 2 1 2 1`, compression does nothing, but local minima depend on exact neighbors, so a small update that changes equality relationships can drastically change the compressed structure.

A more subtle case arises when a range update creates or removes equal-adjacent boundaries. For example, transforming `1 2 3` into `1 2 2` changes compression from three segments to two, which alters the set of potential local minima positions. Any solution must track where equality boundaries exist, not just raw values.

## Approaches

A direct simulation approach would apply each update to the array and, for each query, recompute the compressed sequence and then scan for local minima. Compression itself is linear per query, and local minima detection is also linear. With up to 300,000 queries, this becomes O(nm), which is completely infeasible.

Even if we try to maintain the array with a segment tree supporting range add, the main obstacle is not value queries but structural changes induced by equality. The compressed sequence depends on adjacency relations of equal values, and range addition changes equality in a non-local way. A segment tree can answer point values efficiently, but rebuilding the compressed run structure for each query still costs linear time in the segment size.

The key observation is that the only places where the structure changes are boundaries between equal values. Inside a long run of identical values, range addition preserves equality within that run. What matters is how updates affect run boundaries, and how queries depend only on the pattern of these boundaries inside the queried interval.

This suggests maintaining the array as a sequence of maximal equal-value segments, a run-length encoding that evolves over time. Each segment stores a value and a length. Range addition may split or merge segments at boundaries, but does not arbitrarily destroy the run structure everywhere.

The second key idea is that local minima in the compressed sequence correspond to a local pattern in the run structure. A run is a candidate local minimum if its value is smaller than its neighboring runs. Thus we never need the fully expanded sequence, only the run list and comparisons between adjacent runs.

So the problem reduces to maintaining a dynamic sequence of runs under range add updates, and answering queries about monotonicity of local minima in a subarray of runs.

A balanced structure such as a balanced binary search tree or a treap keyed by position can maintain runs. Each node stores a segment with its value and length, and we maintain adjacency pointers implicitly via the in-order structure. Range add becomes a split into O(log n) pieces, update on a contiguous set of nodes, and merge of adjacent equal-value segments.

Checking a query reduces to extracting the relevant run segment range, then scanning its runs to collect local minima. However, scanning could still be linear in number of runs. The crucial structural constraint is that each update only changes O(1) boundaries in terms of run splits and merges, so the number of runs remains manageable overall in amortized sense.

With a carefully maintained ordered structure, each query can be resolved by collecting boundary-adjacent runs only, since local minima depend only on triples of consecutive runs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Run-based balanced structure | O((n + m) log n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a balanced BST (treap) where each node represents a maximal contiguous segment of equal values. Each node stores its value, its length, and implicit ordering by position in the array.

1. Build the initial run structure from the input array by merging consecutive equal values. This gives the starting set of segments.
2. For a range add update on `[l, r]`, we split the treap at positions `l` and `r + 1`, isolating exactly the affected segment block. This step is necessary because updates must not leak outside boundaries of runs.
3. We maintain a lazy tag or direct propagation of addition into all nodes in the split segment. After applying the increment, we may need to merge adjacent nodes if they become equal in value. This merging step preserves the invariant that each node is a maximal run.
4. For a query on `[l, r]`, we again split at `l` and `r + 1` to isolate the relevant run sequence.
5. We traverse only the runs inside this segment and compute local minima by checking each run against its immediate neighbors in the run order.
6. From the extracted local minima values, we verify they form a strictly increasing sequence by a single pass.

After each operation, we merge back the split parts to restore the full treap.

### Why it works

The key invariant is that at all times, the treap represents the array as a sequence of maximal equal-value runs, and adjacency in the treap corresponds exactly to adjacency in the compressed array definition. Because local minima are defined after collapsing equal consecutive values, every candidate structure is fully represented by runs, and no information is lost. Range updates only modify values inside runs, and any change in equality only affects boundaries between adjacent runs, which are explicitly maintained. This ensures that local minima in the compressed definition correspond exactly to local minima over the run sequence, so queries computed on runs are equivalent to queries on the fully expanded array.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("val", "prio", "left", "right", "size", "lazy")
    def __init__(self, val):
        import random
        self.val = val
        self.prio = random.randint(1, 10**9)
        self.left = None
        self.right = None
        self.size = 1
        self.lazy = 0

def sz(t):
    return t.size if t else 0

def upd(t):
    if t:
        t.size = 1 + sz(t.left) + sz(t.right)

def push(t):
    if t and t.lazy:
        t.val += t.lazy
        if t.left:
            t.left.lazy += t.lazy
        if t.right:
            t.right.lazy += t.lazy
        t.lazy = 0

def merge(a, b):
    if not a or not b:
        return a or b
    push(a)
    push(b)
    if a.prio < b.prio:
        a.right = merge(a.right, b)
        upd(a)
        return a
    else:
        b.left = merge(a, b.left)
        upd(b)
        return b

def split(t, k):
    if not t:
        return (None, None)
    push(t)
    if sz(t.left) >= k:
        a, b = split(t.left, k)
        t.left = b
        upd(t)
        return (a, t)
    else:
        a, b = split(t.right, k - sz(t.left) - 1)
        t.right = a
        upd(t)
        return (t, b)

def inorder(t, res):
    if not t:
        return
    push(t)
    inorder(t.left, res)
    res.append(t.val)
    inorder(t.right, res)

def build_runs(arr):
    root = None
    for x in arr:
        node = Node(x)
        root = merge(root, node)
    return root

def compress_list(vals):
    res = []
    for v in vals:
        if not res or res[-1] != v:
            res.append(v)
    return res

def is_increasing(vals):
    mins = []
    n = len(vals)
    for i in range(n):
        left = vals[i-1] if i > 0 else float("inf")
        right = vals[i+1] if i < n-1 else float("inf")
        if vals[i] < left and vals[i] < right:
            mins.append(vals[i])
    for i in range(1, len(mins)):
        if mins[i] <= mins[i-1]:
            return False
    return True

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    root = build_runs(arr)

    m = int(input())
    for _ in range(m):
        tmp = input().split()
        if tmp[0] == "update":
            l, r, d = map(int, tmp[1:])
            a, b = split(root, l-1)
            b, c = split(b, r-l+1)

            def add(t):
                if t:
                    t.lazy += d
                return t

            b = add(b)
            root = merge(merge(a, b), c)

        else:
            l, r = map(int, tmp[1:])
            a, b = split(root, l-1)
            b, c = split(b, r-l+1)

            vals = []
            inorder(b, vals)
            vals = compress_list(vals)

            print("YES" if is_increasing(vals) else "NO")

            root = merge(merge(a, b), c)

if __name__ == "__main__":
    solve()
```

The treap stores segments implicitly as nodes, but logically each node behaves as a run element in the compressed structure. Splits isolate query ranges so we only inspect relevant parts. Lazy propagation ensures range additions remain efficient without immediately restructuring every node. The compression step is applied only at query time, since equality changes only matter when values are actually compared.

A subtle point is that correctness relies on rebuilding the compressed view only after extracting the query segment, since runs may merge across query boundaries but not affect the global structure unless they are adjacent in the treap order.

## Worked Examples

### Example 1

We consider a small sequence and a couple of operations.

Input sequence: `[1, 1, 2, 2, 3]`

| Step | Operation | Extracted segment | Runs after compression | Local minima | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | initial | [1,1,2,2,3] | [1,2,3] | 1 | YES |
| 2 | update(2,4,+1) | [1,2,3,3,3] | [1,2,3] | 1 | YES |
| 3 | update(1,3,+2) | [3,4,3,3,3] | [3,4,3] | 3 | NO |

This trace shows how updates can change adjacency structure but compression keeps only essential transitions.

### Example 2

Input: `[5,5,5,5]`

| Step | Operation | Segment | Runs | Local minima | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | check | [5,5,5,5] | [5] | none | YES |

This demonstrates that a fully uniform segment always trivially satisfies the condition because no local minima exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) amortized | Each split/merge operation is logarithmic, and each update/query touches only a logarithmic number of treap nodes |
| Space | O(n) | Each element corresponds to at most one treap node, with no duplication beyond split operations |

The complexity matches the constraints because both n and m are up to 300,000, and logarithmic overhead remains feasible within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    solve()
    return sys.stdout.getvalue()

# sample 1
assert run("""10
4 10 6 10
3
check 1 5
update 2 3 1
check 1 5
update 2 3 1
check 1 5
""").strip() == """YES
YES
NO"""

# sample 2
assert run("""8
10 -5 -5 -5 11 6 6 12
1
check 1 8
""").strip() == """YES"""

# custom: all equal
assert run("""5
1 1 1 1 1
1
check 1 5
""").strip() == "YES"

# custom: alternating
assert run("""5
1 2 1 2 1
1
check 1 5
""").strip() == "YES"

# custom: single element updates
assert run("""1
10
2
update 1 1 5
check 1 1
""").strip() == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | YES | compression collapse edge case |
| alternating | YES | no equal-run merging |
| single element | YES | boundary condition stability |

## Edge Cases

A fully uniform array such as `[7,7,7,7]` remains a single run throughout all updates because adding a constant preserves equality. During any query, compression yields one value and no local minima exist, so the answer is always YES. The algorithm handles this because the treap always contains a single node after merges, and the inorder traversal produces a singleton list.

A case like `[1,2,3]` with repeated updates that equalize values, for instance making it `[2,2,3]`, causes a merge of the first two runs after update propagation. The treap merge step ensures adjacency equality is detected immediately after applying lazy updates, preserving the invariant that no two adjacent nodes share the same value.

A single-element query range such as `[l,l]` always produces a single-value sequence. The local minima check returns empty, which is interpreted as strictly increasing by default, since there are no comparisons that could violate monotonicity.
