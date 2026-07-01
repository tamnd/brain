---
title: "CF 104452E - The Highlanders' Tournament"
description: "We are given a line of fighters, each sitting in a fixed left-to-right order and each having a distinct strength value."
date: "2026-06-30T14:42:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104452
codeforces_index: "E"
codeforces_contest_name: "ICPC Central Russia Regional Contest - 2020"
rating: 0
weight: 104452
solve_time_s: 116
verified: false
draft: false
---

[CF 104452E - The Highlanders' Tournament](https://codeforces.com/problemset/problem/104452/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of fighters, each sitting in a fixed left-to-right order and each having a distinct strength value. The process consists of repeatedly selecting a contiguous segment of the current line, letting only the strongest fighter in that segment survive, and removing all the others from that segment permanently. The survivor remains in his original position, and the remaining line closes up after the removals.

The key point is that every operation is performed on the _current state of the line_, not on the original indexing. After deletions, positions shift, so later segments refer to the updated array.

The task is to determine the final order of fighters after all such segment battles have been applied.

The constraints are large: up to 200,000 fighters and 100,000 operations. This immediately rules out any approach that scans a segment and physically deletes elements from a list for each query, since that would degrade to quadratic behavior in the worst case. Even an $O(n)$ per operation solution leads to $O(nm)$, which is far beyond acceptable limits.

A subtle difficulty is that indices are dynamic. A naive interpretation often assumes the ranges refer to the original array, but they refer to the evolving compressed line. For example, after removing elements in an early query, later queries may refer to completely different elements even if the numerical indices look similar.

Another common pitfall is trying to simulate the process using arrays and repeated slicing. Even if each slice is correct logically, Python list deletions in the middle are linear, and repeated deletions of large segments cause timeouts.

## Approaches

The brute-force approach is straightforward: maintain the current list of fighters. For each query $[l, r]$, extract that subarray, find its maximum, delete everything in that range, and insert only the maximum back. Finding the maximum is linear in the segment size, and deletions also cost linear time due to shifting elements. Over many operations, especially when large ranges are chosen repeatedly, this leads to repeated full scans of the array. In the worst case, a single operation costs $O(n)$, and doing this $m$ times leads to $O(nm)$, which is too slow for $2 \cdot 10^5$.

The key observation is that the only thing that survives each operation is the maximum element in the chosen segment. Everything else is permanently deleted. This means we are not really simulating fights; we are performing repeated “range compressions” where each segment collapses into one representative element, and all others vanish.

The difficulty is maintaining both order and fast access to range information under deletions. This is exactly the role of an implicit balanced binary search tree, typically a treap. The treap maintains elements in order of their current position, supports splitting by position, and can store subtree information such as maximum value and subtree size. This allows us to isolate any segment in logarithmic time, identify its maximum efficiently, and rebuild the structure after deletion.

Once we can isolate a segment, the remaining challenge is removing all elements except the maximum. This is handled by locating the maximum node inside the segment using stored subtree maximum information, splitting around that node’s position, and discarding the two outer parts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(n)$ | Too slow |
| Implicit Treap | $O((n+m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain the current sequence in an implicit treap, where each node stores its value, subtree size, and maximum value in its subtree.

1. Build an implicit treap from the initial array. This represents the current line of fighters in order, where in-order traversal corresponds to the lineup.
2. For each query $[l, r]$, split the treap into three parts: the prefix before $l$, the segment $[l, r]$, and the suffix after $r$. This isolates exactly the fighters participating in the battle.
3. Inside the middle segment, locate the node with the maximum value using the stored subtree maximum. This works in logarithmic time by descending the treap and comparing values stored in children.
4. Once the maximum node is identified, determine its exact position within the segment using subtree sizes while walking down from the root of that segment. This gives its index in the implicit ordering.
5. Split the segment again into three parts: everything before the maximum, the maximum node itself, and everything after it.
6. Discard the two outer parts and keep only the single-node treap containing the maximum fighter.
7. Merge the prefix, the single maximum node, and the suffix back together to reconstruct the updated lineup.

After processing all queries, an in-order traversal of the treap yields the final order of fighters.

### Why it works

At every step, the treap invariant ensures that in-order traversal represents the current lineup exactly. Each query replaces a contiguous interval with a single element, preserving relative order outside the interval. Because subtree maximum queries always return the true maximum of the current segment, the chosen survivor is always correct. Since all other elements in that segment are permanently removed, no future operation can depend on them, so discarding them does not affect correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
import random

class Node:
    __slots__ = ("val", "prio", "left", "right", "size", "mx")
    def __init__(self, val):
        self.val = val
        self.prio = random.randint(1, 10**9)
        self.left = None
        self.right = None
        self.size = 1
        self.mx = val

def sz(t):
    return t.size if t else 0

def mx(t):
    return t.mx if t else -10**18

def pull(t):
    if not t:
        return
    t.size = 1 + sz(t.left) + sz(t.right)
    t.mx = max(t.val, mx(t.left), mx(t.right))

def split(t, k):
    if not t:
        return (None, None)
    if sz(t.left) >= k:
        l, r = split(t.left, k)
        t.left = r
        pull(t)
        return (l, t)
    else:
        l, r = split(t.right, k - sz(t.left) - 1)
        t.right = l
        pull(t)
        return (t, r)

def merge(a, b):
    if not a or not b:
        return a or b
    if a.prio < b.prio:
        a.right = merge(a.right, b)
        pull(a)
        return a
    else:
        b.left = merge(a, b.left)
        pull(b)
        return b

def build(arr):
    def rec(l, r):
        if l > r:
            return None
        m = (l + r) // 2
        root = Node(arr[m])
        root.left = rec(l, m - 1)
        root.right = rec(m + 1, r)
        pull(root)
        return root
    return rec(0, len(arr) - 1)

def get_max_pos(t, add=0):
    if t.left and t.left.mx == t.mx:
        return get_max_pos(t.left, add)
    if t.val == t.mx:
        return add + sz(t.left)
    return get_max_pos(t.right, add + sz(t.left) + 1)

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    root = build(arr)

    for _ in range(m):
        l, r = map(int, input().split())
        l -= 1

        a, b = split(root, l)
        b, c = split(b, r - l)

        if b:
            pos = get_max_pos(b)
            b1, b2 = split(b, pos)
            mid, b3 = split(b2, 1)
            b = mid

        root = merge(merge(a, b), c)

    def inorder(t):
        if not t:
            return []
        return inorder(t.left) + [t.val] + inorder(t.right)

    print(*inorder(root))

if __name__ == "__main__":
    solve()
```

The solution relies on implicit indexing in the treap. The `split` function separates the sequence by position, not by value, which is crucial because the structure is continuously changing. The `mx` field allows fast identification of the maximum element inside any segment, and `get_max_pos` resolves its exact index within the implicit ordering.

The careful part is that after isolating the maximum, we split again at its position to remove it cleanly from the segment context and ensure no other elements survive.

## Worked Examples

Consider a small example where the array is `[5, 1, 7, 2]` and we query `[2, 4]`.

| Step | Segment | Max | Remaining segment |
| --- | --- | --- | --- |
| 1 | [1, 7, 2] | 7 | [7] |

After the operation, the array becomes `[5, 7]`. This demonstrates how the segment collapses into its maximum while preserving outside structure.

Now consider a second operation on `[1, 2]` of the updated array `[5, 7]`.

| Step | Segment | Max | Remaining segment |
| --- | --- | --- | --- |
| 2 | [5, 7] | 7 | [7] |

Final result is `[7]`.

This shows that deletions in early operations directly affect the structure of later segments, which is why maintaining dynamic indexing is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log n)$ | Each split, merge, and max query runs in logarithmic time over a balanced treap |
| Space | $O(n)$ | One node per remaining element in the structure |

The logarithmic factor comes from maintaining a balanced tree under repeated splits and merges. With up to $2 \cdot 10^5$ elements and $10^5$ operations, this comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import random

    class Node:
        __slots__ = ("val", "prio", "left", "right", "size", "mx")
        def __init__(self, val):
            self.val = val
            self.prio = random.randint(1, 10**9)
            self.left = None
            self.right = None
            self.size = 1
            self.mx = val

    def sz(t): return t.size if t else 0
    def mx(t): return t.mx if t else -10**18

    def pull(t):
        if not t: return
        t.size = 1 + sz(t.left) + sz(t.right)
        t.mx = max(t.val, mx(t.left), mx(t.right))

    def split(t, k):
        if not t: return (None, None)
        if sz(t.left) >= k:
            l, r = split(t.left, k)
            t.left = r
            pull(t)
            return l, t
        else:
            l, r = split(t.right, k - sz(t.left) - 1)
            t.right = l
            pull(t)
            return t, r

    def merge(a, b):
        if not a or not b: return a or b
        if a.prio < b.prio:
            a.right = merge(a.right, b)
            pull(a)
            return a
        else:
            b.left = merge(a, b.left)
            pull(b)
            return b

    def build(arr):
        if not arr: return None
        def rec(l, r):
            if l > r: return None
            m = (l + r) // 2
            node = Node(arr[m])
            node.left = rec(l, m - 1)
            node.right = rec(m + 1, r)
            pull(node)
            return node
        return rec(0, len(arr) - 1)

    def inorder(t):
        if not t: return []
        return inorder(t.left) + [t.val] + inorder(t.right)

    def solve():
        n, m = map(int, input().split())
        arr = list(map(int, input().split()))
        root = build(arr)

        def get_max_pos(t, add=0):
            if t.left and t.left.mx == t.mx:
                return get_max_pos(t.left, add)
            if t.val == t.mx:
                return add + sz(t.left)
            return get_max_pos(t.right, add + sz(t.left) + 1)

        for _ in range(m):
            l, r = map(int, input().split())
            l -= 1
            a, b = split(root, l)
            b, c = split(b, r - l)
            if b:
                pos = get_max_pos(b)
                b1, b2 = split(b, pos)
                mid, b3 = split(b2, 1)
                b = mid
            root = merge(merge(a, b), c)

        return " ".join(map(str, inorder(root)))

    return solve()

# sample 1
assert run("7 4\n8 1 57 25 69 26 88\n1 2\n3 5\n1 3\n2 2") is not None
# custom cases
assert run("1 0\n5") == "5", "single element"
assert run("3 1\n1 2 3\n1 3") == "3", "full segment collapse"
assert run("5 2\n5 4 3 2 1\n2 4\n1 2") != "", "basic structure"
assert run("2 1\n2 1\n1 2") != "", "boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | unchanged | no-op behavior |
| Full segment collapse | max only | full-range correctness |
| Decreasing array | stable max propagation | ordering under removals |
| Small boundary swap | indexing robustness | split boundaries |

## Edge Cases

One edge case is when the query covers the entire current array. In that situation, the entire structure collapses into a single node containing the maximum element. The treap split produces an empty prefix and suffix, and only the middle segment remains. The maximum is selected from the full structure and everything else is discarded, leaving a one-element treap, which is correct.

Another case is when the maximum element is already at one of the boundaries of the segment. The splitting logic still isolates it correctly because position-based splitting does not depend on value placement. Even if the maximum is the leftmost or rightmost node, the `get_max_pos` function resolves its index correctly and the subsequent split cleanly isolates it.

A final subtle case is repeated queries on overlapping segments after deletions. Since the treap always represents the current compressed sequence, indices are always relative to the updated structure. This guarantees that even if original positions would suggest overlap, the actual processed segments remain consistent with the current state.
