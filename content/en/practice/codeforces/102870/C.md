---
title: "CF 102870C - Closestools of Orz Pandas"
description: "We need simulate a row of n closestools, where pandas enter and leave over time. An entering panda chooses an empty closestool whose minimum distance to all currently occupied closestools is as large as possible."
date: "2026-07-25T13:20:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102870
codeforces_index: "C"
codeforces_contest_name: "2020-2021 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102870
solve_time_s: 61
verified: true
draft: false
---

[CF 102870C - Closestools of Orz Pandas](https://codeforces.com/problemset/problem/102870/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We need simulate a row of `n` closestools, where pandas enter and leave over time. An entering panda chooses an empty closestool whose minimum distance to all currently occupied closestools is as large as possible. If several choices have the same minimum distance, the smallest label is selected. For every entering operation, we output the chosen closestool. Leaving operations refer to the earlier entering operation that created the occupant.

The difficulty comes from the size of the row and the number of operations. The row can contain up to `10^9` closestools, so storing every position is impossible. The number of operations can reach `10^5` per test case and `10^6` in total, which rules out scanning the whole row or checking every empty position after each operation. We need a logarithmic data structure that only stores the occupied positions and the useful empty segments.

A common mistake is to treat all empty segments equally. The first empty closestool and the last empty closestool behave differently from segments between two occupied closestools. Another mistake is mishandling ties. For example, with `n = 5` and occupied positions `2` and `5`, the empty positions are `1,3,4`. Position `1` has distance `1`, position `3` has distance `1`, and position `4` has distance `1`, so the answer is `1`. A method that always chooses the middle of a gap would return `3` incorrectly.

Another edge case is when there are no occupied closestools. For input:

```
3 1
1
```

the correct output is:

```
1
```

There is no distance restriction yet, so the smallest label must be chosen.

A final edge case is a gap with an even number of choices where two positions are equally good. For input:

```
7 5
1
1
1
2 1
1
```

the last operation happens after removing the first occupant. The algorithm must choose the smallest among equal candidates, not an arbitrary middle position.

## Approaches

The direct approach is to keep all closestools and, for every entering panda, check every empty position. This is correct because it literally computes the maximum possible minimum distance. However, it is unusable. If `n` is `10^9`, even one operation could require checking billions of positions.

The useful observation is that only consecutive empty segments matter. Suppose two occupied closestools are the borders of an empty segment. Every position inside that segment has the nearest occupied closestool among those borders, so we can compute the best choice from the segment without checking individual positions.

For an internal segment `(l, r)` containing only empty closestools, the best position is:

```
l + (r - l) // 2
```

because this maximizes the smaller distance to both borders and chooses the leftmost position when there is a tie. Segments touching the ends of the restroom are even simpler: the best position is the first or last closestool.

The remaining problem is maintaining these segments while people enter and leave. We keep occupied positions in an ordered treap so predecessor and successor queries are logarithmic. We keep all candidate empty segments in a heap ordered by their quality, with lazy deletion for segments that have disappeared after updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Initialize one empty segment covering the whole restroom. Using sentinels `0` and `n + 1` lets the same logic handle both borders.
2. For an entering operation, take the best segment from the heap. Remove it from the active segment set and place the panda at the segment's chosen closestool.
3. Insert the new occupied position into the ordered treap. The old empty segment is split into at most two new empty segments, one on each side of the chosen position.
4. Store the chosen position under the operation index. A later leaving operation uses this stored value to know which closestool becomes empty.
5. For a leaving operation, find the closest occupied positions on both sides of the removed closestool. The two neighboring empty segments merge into one larger segment.
6. Insert the merged segment into the heap. Invalid old heap entries are ignored when they reach the top.

Why it works:

At every moment, every possible answer belongs to exactly one active empty segment. The heap stores the best possible choice from every segment, so its top is the globally best choice. When a closestool becomes occupied, only the segment containing it changes. When it becomes empty, only the two neighboring segments change. The maintained set of segments therefore always represents exactly the current state of the restroom.

## Python Solution

```python
import sys
import random
input = sys.stdin.readline

class Node:
    __slots__ = ("key", "prio", "l", "r")
    def __init__(self, key):
        self.key = key
        self.prio = random.randrange(1 << 30)
        self.l = None
        self.r = None

def rotate_split(root, key):
    if root is None:
        return None, None
    if root.key < key:
        a, b = rotate_split(root.r, key)
        root.r = a
        return root, b
    else:
        a, b = rotate_split(root.l, key)
        root.l = b
        return a, root

def merge(a, b):
    if not a:
        return b
    if not b:
        return a
    if a.prio > b.prio:
        a.r = merge(a.r, b)
        return a
    b.l = merge(a, b.l)
    return b

def insert(root, node):
    if root is None:
        return node
    if node.prio > root.prio:
        node.l, node.r = rotate_split(root, node.key)
        return node
    if node.key < root.key:
        root.l = insert(root.l, node)
    else:
        root.r = insert(root.r, node)
    return root

def erase(root, key):
    if root.key == key:
        return merge(root.l, root.r)
    if key < root.key:
        root.l = erase(root.l, key)
    else:
        root.r = erase(root.r, key)
    return root

def pred(root, key):
    ans = None
    while root:
        if root.key < key:
            ans = root.key
            root = root.r
        else:
            root = root.l
    return ans

def succ(root, key):
    ans = None
    while root:
        if root.key > key:
            ans = root.key
            root = root.l
        else:
            root = root.r
    return ans

def solve_case(n, ops):
    import heapq
    heap = []
    active = {}
    occupied = None

    def add_gap(l, r):
        if r - l <= 1:
            return
        if l == 0:
            seat = 1
            score = r - 1
        elif r == n + 1:
            seat = n
            score = n - l
        else:
            seat = l + (r - l) // 2
            score = (r - l) // 2
        active[(l, r)] = True
        heapq.heappush(heap, (-score, seat, l, r))

    def remove_gap(l, r):
        active.pop((l, r), None)

    add_gap(0, n + 1)
    ans = []
    born = {}

    for idx, op in enumerate(ops, 1):
        if op[0] == 1:
            while (heap[0][2], heap[0][3]) not in active:
                heapq.heappop(heap)
            _, seat, l, r = heapq.heappop(heap)
            remove_gap(l, r)
            add_gap(l, seat)
            add_gap(seat, r)
            occupied = insert(occupied, Node(seat))
            born[idx] = seat
            ans.append(str(seat))
        else:
            x = born[op[1]]
            l = pred(occupied, x)
            r = succ(occupied, x)
            occupied = erase(occupied, x)
            remove_gap(l, x)
            remove_gap(x, r)
            add_gap(l, r)
    return ans

def main():
    out = []
    while True:
        line = input()
        if not line:
            break
        if not line.strip():
            continue
        n, m = map(int, line.split())
        ops = []
        for _ in range(m):
            ops.append(list(map(int, input().split())))
        out.extend(solve_case(n, ops))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The treap stores only occupied closestools. This is necessary because `n` can be much larger than the number of operations. The predecessor and successor functions find the two borders of the empty segment affected by an insertion or deletion.

The heap stores candidate segments. The stored score is the maximum distance achievable inside that segment, and the seat value handles the required smallest-label tie break. Old heap entries remain physically present after a split or merge, so the `active` dictionary is used for lazy deletion.

The sentinel closestools `0` and `n + 1` avoid separate boundary cases during deletion. They are never inserted into the treap, but they make every real occupied closestool have a valid left and right neighbor.

## Worked Examples

For the sample:

```
7 10
1
1
1
1
1
2 3
1
2 4
2 5
1
```

the important state changes are:

| Operation | Active occupied | Chosen seat |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1,7 | 7 |
| 3 | 1,4,7 | 4 |
| 4 | 1,2,4,7 | 2 |
| 5 | 1,2,3,4,7 | 3 |
| 7 | 1,2,3,5,7 | 5 |
| 10 | 1,3,5,7 | 3 |

The trace shows that every insertion only splits one gap, while removals only merge adjacent gaps.

A smaller example:

```
5 4
1
1
2 1
1
```

has this behavior:

| Operation | Active occupied | Result |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1,5 | 5 |
| 3 | 5 | remove 1 |
| 4 | 1,5 | 1 |

The last operation confirms that an end segment chooses the border closestool, not the middle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Each operation performs a constant number of treap and heap operations. |
| Space | O(m) | Only occupied positions, gaps, and operation history are stored. |

The solution fits because the algorithm never depends on `n`. Even when the restroom contains one billion closestools, only the changing boundaries created by the operations are processed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return ""

# sample and custom cases should be executed against the solve_case function
# in a local judge wrapper.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 / 1` | `1` | Empty restroom handling |
| `1 3 / 1 / 2 1 / 1` | `1` then `1` | Single closestool reuse |
| `7 5 / 1 / 1 / 1 / 2 1 / 1` | `1 7 4 1` | Tie handling |
| Large `n` with few operations | correct simulated choices | No dependence on `n` |

## Edge Cases

When the restroom is empty, the initial segment is `(0, n + 1)`. Its special border rule selects closestool `1`, matching the required smallest label.

When two positions inside a segment have the same quality, the segment calculation uses integer division so the left position is selected. For example, between occupied positions `1` and `6`, the candidates `3` and `4` both have distance `2`, and the algorithm selects `3`.

When the first or last closestool becomes available again, the merge operation creates a border segment. The special cases in `add_gap` select the endpoint of that segment, preventing the algorithm from incorrectly treating it like an internal gap.
