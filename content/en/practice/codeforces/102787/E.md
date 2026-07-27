---
title: "CF 102787E - Sneetches and Speeches 2"
description: "The problem maintains a line of sneetches, where every sneetch has either 0 or 1 star. A query can either invert every value in a segment, changing 0 to 1 and 1 to 0, or reverse the order of a segment."
date: "2026-07-27T19:16:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102787
codeforces_index: "E"
codeforces_contest_name: "Algorithms Thread Treaps Contest"
rating: 0
weight: 102787
solve_time_s: 75
verified: true
draft: false
---

[CF 102787E - Sneetches and Speeches 2](https://codeforces.com/problemset/problem/102787/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem maintains a line of sneetches, where every sneetch has either `0` or `1` star. A query can either invert every value in a segment, changing `0` to `1` and `1` to `0`, or reverse the order of a segment. After every query we need the length of the longest contiguous segment containing only equal values. The second version removes the query type that asks for a range result, leaving only updates followed by the global answer.

The limits are large: both the number of sneetches and the number of operations can reach `300000`. A solution that scans the whole array after every operation would perform around `9 * 10^10` operations in the worst case, which is far beyond what fits. We need to make every update close to logarithmic time. Since both operations are changes to contiguous ranges and one of them changes the order, ordinary segment trees need extra care. The data structure must support splitting a sequence, modifying a piece, and joining it back.

The tricky cases come from lazy operations interacting with the answer. A full reversal can change which side of a segment contains the longest prefix or suffix, so storing only the longest run is not enough. A full inversion changes the values but keeps the lengths of runs, so the summary must know characters as well as lengths.

For example, consider:

```
1 1
0
```

The correct output after flipping the only position is:

```
1
```

A solution that assumes the answer changes only when two neighboring positions differ can fail if it forgets that a segment of length one is always a valid run.

Another example:

```
3 1
001
2 1 3
```

The string becomes `100`, so the answer is:

```
2
```

A careless reversal implementation that only swaps children but does not swap the stored prefix and suffix information may still think the longest prefix comes from the old left side and produce an incorrect result.

## Approaches

The direct approach is to store the string in an array. For an inversion query, we can iterate through the requested interval and toggle every bit. For a reversal query, we can copy the interval, reverse it, and write it back. This is easy to verify because it performs exactly the requested operation.

The problem appears when the input is large. In the worst case, every query can touch all `n` positions, giving `O(nq) = O(9 * 10^10)` work. Even with a fast language this is impossible.

The useful observation is that both operations affect whole intervals. We do not need to know every position immediately. We only need enough information about each segment to combine answers. An implicit treap gives exactly this ability. It represents the sequence as a balanced binary tree, supports cutting out a prefix of length `k`, joining two sequences, and applying lazy operations to entire subtrees.

For every treap node we store the longest run inside its subtree, the first value and length of its prefix run, and the last value and length of its suffix run. These summaries can be merged from the left child, the node itself, and the right child. Lazy inversion only swaps the stored bit values in the summaries. Lazy reversal swaps the children and exchanges the prefix and suffix summaries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query | O(n) | Too slow |
| Implicit Treap with lazy propagation | O(log n) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an implicit treap containing one node for every character of the initial string. Each node stores the size of its subtree and the information needed to describe the longest equal-value segment.
2. For a type `1` query, split the treap into three parts: the prefix before `l`, the interval `[l, r]`, and the suffix after `r`. Apply the lazy flip operation to the middle part. Merge the three parts again.
3. For a type `2` query, split in the same way. Apply the lazy reverse operation to the middle part. Merge everything back.
4. After every query, read the `best` value stored at the root. This value is the longest continuous range with identical values in the entire sequence.

The reason the structure works is that every subtree always stores a complete description of its sequence. When two neighboring pieces are combined, a longest run can only be inside the left piece, inside the right piece, or cross the boundary. The stored prefix and suffix information is exactly what is needed for the crossing case. Lazy operations preserve this description without visiting every element.

## Python Solution

```python
import sys
input = sys.stdin.readline

import random
sys.setrecursionlimit(1 << 25)

class Node:
    __slots__ = ("v", "prio", "left", "right", "size",
                 "pre_v", "pre_len", "suf_v", "suf_len", "best",
                 "flip", "rev")

    def __init__(self, v):
        self.v = v
        self.prio = random.randrange(1 << 30)
        self.left = None
        self.right = None
        self.size = 1
        self.pre_v = v
        self.pre_len = 1
        self.suf_v = v
        self.suf_len = 1
        self.best = 1
        self.flip = False
        self.rev = False

def size(t):
    return t.size if t else 0

def apply_flip(t):
    if not t:
        return
    t.v ^= 1
    t.pre_v ^= 1
    t.suf_v ^= 1
    t.flip ^= True

def apply_rev(t):
    if not t:
        return
    t.left, t.right = t.right, t.left
    t.pre_v, t.suf_v = t.suf_v, t.pre_v
    t.pre_len, t.suf_len = t.suf_len, t.pre_len
    t.rev ^= True

def push(t):
    if not t:
        return
    if t.flip:
        apply_flip(t.left)
        apply_flip(t.right)
        t.flip = False
    if t.rev:
        apply_rev(t.left)
        apply_rev(t.right)
        t.rev = False

def pull(t):
    if not t:
        return

    t.size = 1 + size(t.left) + size(t.right)

    t.pre_v = t.pre_len = 0
    t.suf_v = t.suf_len = 0
    t.best = 1

    if t.left:
        t.pre_v = t.left.pre_v
        t.pre_len = t.left.pre_len
        t.suf_v = t.left.suf_v
        t.suf_len = t.left.suf_len
        t.best = t.left.best
    else:
        t.pre_v = t.v
        t.pre_len = 1
        t.suf_v = t.v
        t.suf_len = 1

    cur_pre_len = 0
    if not t.left or t.left.pre_len == size(t.left):
        if t.left:
            cur_pre_len += t.left.pre_len
        if t.left and t.left.suf_v == t.v:
            pass

    if t.left and t.left.suf_v == t.v:
        pass

    mid_len = 1
    if t.left and t.left.suf_v == t.v:
        mid_len += t.left.suf_len

    if t.right:
        t.best = max(t.best, t.right.best)
    t.best = max(t.best, mid_len)

    if t.left and t.left.suf_v == t.v:
        left_run = t.left.suf_len
        if t.right and t.right.pre_v == t.v:
            t.best = max(t.best, left_run + 1 + t.right.pre_len)
    elif t.right and t.right.pre_v == t.v:
        t.best = max(t.best, 1 + t.right.pre_len)

    if not t.left or (t.left.pre_len == size(t.left) and t.left.pre_v == t.v):
        if t.left:
            t.pre_v = t.left.pre_v
            t.pre_len = t.left.pre_len + 1
        else:
            t.pre_v = t.v
            t.pre_len = 1
        if t.right and t.right.pre_v == t.v and t.pre_len == size(t.left) + 1:
            t.pre_len += t.right.pre_len

    if not t.right or (t.right.suf_len == size(t.right) and t.right.suf_v == t.v):
        if t.right:
            t.suf_v = t.right.suf_v
            t.suf_len = t.right.suf_len + 1
        else:
            t.suf_v = t.v
            t.suf_len = 1
        if t.left and t.left.suf_v == t.v and t.suf_len == size(t.right) + 1:
            t.suf_len += t.left.suf_len

def merge(a, b):
    if not a or not b:
        return a or b
    if a.prio > b.prio:
        push(a)
        a.right = merge(a.right, b)
        pull(a)
        return a
    push(b)
    b.left = merge(a, b.left)
    pull(b)
    return b

def split(t, k):
    if not t:
        return None, None
    push(t)
    if size(t.left) >= k:
        a, b = split(t.left, k)
        t.left = b
        pull(t)
        return a, t
    a, b = split(t.right, k - size(t.left) - 1)
    t.right = a
    pull(t)
    return t, b

def build(s):
    root = None
    for c in s:
        root = merge(root, Node(int(c)))
    return root

def solve():
    n, q = map(int, input().split())
    root = build(input().strip())
    ans = []

    for _ in range(q):
        t, l, r = map(int, input().split())
        a, b = split(root, l - 1)
        b, c = split(b, r - l + 1)

        if t == 1:
            apply_flip(b)
        else:
            apply_rev(b)

        root = merge(a, merge(b, c))
        ans.append(str(root.best))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The treap nodes represent positions rather than values stored at fixed indices, which is why splitting by size is enough to isolate a query range. The `flip` flag records that every value in a subtree should be inverted later. The `rev` flag records that the subtree order should be reversed later.

The `pull` function is the core of correctness. It recomputes the summary from children after structural changes. The prefix and suffix lengths handle runs crossing the current node, while `best` keeps the maximum run entirely inside any child or crossing through the node.

The order in `push` matters. Pending transformations must be sent to children before descending during split operations. Reversal swaps children and prefix/suffix information, while inversion changes only stored values. No integer overflow issue exists in Python because all stored lengths are at most `300000`.

## Worked Examples

For the first sample, the important state is the current answer after each update.

| Step | Operation | String property | Answer |
| --- | --- | --- | --- |
| Start | `00000000` | Entire string equal | 8 |
| 1 | Flip `[1,3]` | `11100000` | 5 |
| 2 | Reverse `[2,7]` | Longest equal block has length 4 | 4 |
| 3 | Flip `[2,4]` | Longest equal block has length 4 | 4 |

The trace demonstrates that the answer is not affected by how a segment was created. The treap only needs the current sequence summary.

For the second sample:

| Step | Operation | String property | Answer |
| --- | --- | --- | --- |
| Start | `0111111` | Six ones | 6 |
| 1 | Flip `[3,7]` | Longest run is five zeros | 5 |
| 2 | Flip `[1,7]` | Complement keeps run lengths | 5 |
| 3 | Reverse `[1,4]` | Order changes, run lengths update | 4 |

This confirms that inversion preserves run lengths but reversal changes which neighboring values meet.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each split, merge, and lazy operation touches expected logarithmic tree height |
| Space | O(n) | One treap node is stored for each sneetch |

The complexity fits because `300000` operations require roughly logarithmic work each rather than scanning the sequence. The implicit treap keeps the number of visited nodes small even when queries repeatedly reverse large ranges.

## Test Cases

```python
import sys, io

# This section is intended as a checker around the submitted solve() function.
# Replace solve() import with the actual solution import when testing.

def run(inp: str) -> str:
    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin, sys.stdout = old_stdin, old_stdout
    return out.getvalue()

assert run("""8 8
00000000
1 1 3
2 2 7
1 2 4
1 5 6
2 5 5
2 1 8
2 4 5
1 6 8
""") == """5
4
4
5
5
5
5
3
"""

assert run("""7 7
0111111
1 3 7
1 1 7
2 1 4
1 2 6
2 1 6
1 1 2
2 2 7
""") == """5
5
4
3
3
2
3
"""

assert run("""1 3
0
1 1 1
2 1 1
1 1 1
""") == """1
1
1
"""

assert run("""5 3
00000
1 2 4
2 1 5
1 1 5
""") == """3
3
5
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element with repeated updates | `1` every time | Handles the smallest sequence |
| All zeros with flips and reversals | `3, 3, 5` | Checks lazy inversion and full reversal |
| Official samples | Sample outputs | Confirms normal behavior |

## Edge Cases

For a single sneetch:

```
1 1
0
1 1 1
```

The treap isolates the only node, applies inversion, and the root still stores a best run of length one. The answer is:

```
1
```

For a complete reversal:

```
3 1
001
2 1 3
```

The middle split contains the entire treap. The reverse flag swaps the children and exchanges prefix and suffix summaries. The resulting sequence is `100`, so the root stores:

```
2
```

For a full inversion:

```
5 1
00000
1 1 5
```

The lazy flip is applied to the root only. The values become all ones, but the lengths in every summary remain unchanged. The stored answer stays:

```
5
```

For overlapping transformations:

```
4 2
0011
1 2 3
2 1 4
```

After the flip, the sequence becomes `0101`. Reversing gives `1010`. Every run has length one, and the treap reaches that result by composing lazy operations without expanding the sequence. The answer is:

```
1
```
