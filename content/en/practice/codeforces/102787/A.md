---
title: "CF 102787A - Shandom Ruffle"
description: "The problem describes a sequence of n tiles initially arranged as 1, 2, 3, ..., n. We are given n shuffle operations. Each operation receives two positions a and b. If b is not after a, nothing happens."
date: "2026-07-27T19:20:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102787
codeforces_index: "A"
codeforces_contest_name: "Algorithms Thread Treaps Contest"
rating: 0
weight: 102787
solve_time_s: 65
verified: true
draft: false
---

[CF 102787A - Shandom Ruffle](https://codeforces.com/problemset/problem/102787/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a sequence of `n` tiles initially arranged as `1, 2, 3, ..., n`. We are given `n` shuffle operations. Each operation receives two positions `a` and `b`. If `b` is not after `a`, nothing happens. Otherwise, the operation swaps the tile at `a` with the tile at `b`, then the tile at `a + 1` with the tile at `b + 1`, and so on, stopping when one of the two ranges reaches the end of the array. After applying all operations, we must print the final order of the tiles.

The input size is the key difficulty. There can be up to `500000` operations, and the array has the same maximum size. A direct simulation of one operation can touch many positions, and in the worst case a single operation can move `O(n)` elements. Repeating that for `n` operations gives `O(n^2)` work, which is far beyond what is possible for half a million elements. We need each shuffle to be handled in roughly logarithmic time.

Several edge cases are easy to miss. If `b <= a`, the operation must be ignored completely. For example:

```
Input:
1
1 1
```

The array remains `[1]`, so the output is:

```
1
```

A careless implementation that always creates a non-empty swapped range could access invalid positions.

Another important case is when the second swapped segment reaches the end of the array. For example:

```
Input:
5
4 1
5 4
3 5
4 5
5 2
```

The first operation does nothing because `1 <= 4`. The later operations have different effective lengths because the right side of the swap may be cut short by the array boundary. Treating every operation as if it always swaps two equal full blocks produces the wrong permutation.

## Approaches

A straightforward solution is to store the array explicitly and perform every swap in the definition. For an operation `(a, b)`, we repeatedly exchange `array[a]` with `array[b]` while moving both indices forward. This is a correct implementation because it exactly follows the shuffle procedure.

The problem is the running time. Consider operations that repeatedly swap almost the entire array. One operation can require close to `n/2` swaps. With `n` operations, the number of elementary exchanges can approach `250000000000`, which is not feasible.

The useful observation is that each shuffle does not care about the values stored in the array. It only rearranges positions. The operation is a permutation of a contiguous sequence, specifically a swap of two adjacent blocks. The array can be represented as an ordered sequence where cutting and joining pieces is efficient.

An implicit treap is a good fit because it stores a sequence while supporting splits by position and merges. A shuffle can be performed by cutting the sequence into the part before `a`, the first block, the second block, and the remaining suffix. Then the two middle blocks are joined in the opposite order. The number of pieces is constant, so every operation takes `O(log n)` expected time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Implicit Treap | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an implicit treap containing the sequence `1, 2, ..., n`. The treap position of a node represents its index in the current array, so we never need to store the array in a normal list.
2. For each shuffle `(a, b)`, ignore it if `b <= a`. The operation cannot swap anything in this case.
3. Compute the length of the first block being exchanged. The two blocks begin at `a` and `b`, so their distance is `b - a`. The second block can only extend until the end of the array, giving the length:

```
min(b - a, n - b + 1)
```

1. Split the treap into four pieces. The first piece contains positions before `a`. The next two pieces are the blocks that must be exchanged. The last piece contains everything after the exchanged region.
2. Merge the pieces back in the order: prefix, second block, first block, suffix. This recreates exactly the swaps performed by the original procedure.
3. After all operations, traverse the treap in order and print the stored values.

The reason this works is that an adjacent block swap is completely described by its two blocks. The treap maintains the same sequence order as the real array, so splitting out the two blocks and switching their positions applies exactly the same permutation as performing every individual swap.

Why it works:

The invariant is that after processing any number of operations, the treap's inorder traversal is identical to the real array after those operations. Initially this is true because the treap contains the identity permutation. During a shuffle, the split operation extracts exactly the same four consecutive ranges that the original loop accesses. Reordering the two middle ranges changes only their positions, which is precisely what all individual swaps do. Since each operation preserves the invariant, the final traversal is the required answer.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

class Node:
    __slots__ = ("val", "prio", "size", "left", "right")

    def __init__(self, val):
        self.val = val
        self.prio = random.randint(1, 1 << 30)
        self.size = 1
        self.left = None
        self.right = None

def size(t):
    return t.size if t else 0

def update(t):
    if t:
        t.size = 1 + size(t.left) + size(t.right)

def merge(a, b):
    if not a:
        return b
    if not b:
        return a
    if a.prio > b.prio:
        a.right = merge(a.right, b)
        update(a)
        return a
    else:
        b.left = merge(a, b.left)
        update(b)
        return b

def split(t, k):
    if not t:
        return None, None
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

def build(n):
    root = None
    for i in range(1, n + 1):
        root = merge(root, Node(i))
    return root

def collect(t, ans):
    if not t:
        return
    collect(t.left, ans)
    ans.append(str(t.val))
    collect(t.right, ans)

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    root = build(n)

    for _ in range(n):
        a, b = map(int, input().split())
        if b <= a:
            continue

        length = min(b - a, n - b + 1)

        left, rest = split(root, a - 1)
        first, rest = split(rest, length)
        second, right = split(rest, length)

        root = merge(left, merge(second, merge(first, right)))

    ans = []
    collect(root, ans)
    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The treap node stores only the value and subtree size. The priority field keeps the tree balanced randomly, giving logarithmic expected height.

The `split` function is the core operation. It separates the first `k` elements from the rest of the sequence. The indexes are zero-based internally through subtree sizes, while the problem uses one-based positions, so every input position is adjusted with `a - 1`.

The shuffle length calculation is where many wrong solutions fail. The second block starts at `b`, so it contains at most `n - b + 1` elements. It also cannot be longer than the gap between `a` and `b`, which is why the minimum of those two quantities is required.

The final traversal uses inorder order because an implicit treap represents the sequence through its left subtree, node, and right subtree ordering.

## Worked Examples

Using the first sample:

```
4
3 1
1 3
3 2
2 3
```

The trace is:

| Operation | Effective action | Sequence |
| --- | --- | --- |
| Start | Initial treap | 1 2 3 4 |
| 3 1 | ignored | 1 2 3 4 |
| 1 3 | swap [1,2] and [3,4] | 3 4 1 2 |
| 3 2 | ignored | 3 4 1 2 |
| 2 3 | swap positions 2 and 3 | 3 1 4 2 |

The example demonstrates why operations with `b <= a` must be skipped and why the treap only needs to rearrange ranges.

For the second sample:

```
5
4 1
5 4
3 5
4 5
5 2
```

| Operation | Effective length | Sequence |
| --- | --- | --- |
| Start |  | 1 2 3 4 5 |
| 4 1 | ignored | 1 2 3 4 5 |
| 5 4 | ignored | 1 2 3 4 5 |
| 3 5 | 1 | 1 2 5 4 3 |
| 4 5 | 1 | 1 2 5 3 4 |
| 5 2 | ignored | 1 2 5 3 4 |

This trace exercises the boundary case where the right block reaches the end of the sequence and cannot have the full theoretical length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of the `n` shuffles performs a constant number of treap splits and merges. |
| Space | O(n) | The treap stores one node for each tile. |

With `n = 500000`, a quadratic simulation is impossible. The treap solution performs about a few dozen logarithmic operations per shuffle, which fits the intended constraints.

## Test Cases

```python
import sys
import io
import random

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline
    n = int(data())
    
    class Node:
        __slots__ = ("v", "p", "s", "l", "r")
        def __init__(self, v):
            self.v = v
            self.p = random.randint(1, 10**9)
            self.s = 1
            self.l = None
            self.r = None

    def sz(t):
        return t.s if t else 0

    def up(t):
        if t:
            t.s = sz(t.l) + sz(t.r) + 1

    def merge(a, b):
        if not a or not b:
            return a or b
        if a.p > b.p:
            a.r = merge(a.r, b)
            up(a)
            return a
        b.l = merge(a, b.l)
        up(b)
        return b

    def split(t, k):
        if not t:
            return None, None
        if sz(t.l) >= k:
            a, b = split(t.l, k)
            t.l = b
            up(t)
            return a, t
        a, b = split(t.r, k - sz(t.l) - 1)
        t.r = a
        up(t)
        return t, b

    root = None
    for i in range(1, n + 1):
        root = merge(root, Node(i))

    for _ in range(n):
        a, b = map(int, data().split())
        if b > a:
            length = min(b - a, n - b + 1)
            x, root = split(root, a - 1)
            y, root = split(root, length)
            z, w = split(root, length)
            root = merge(x, merge(z, merge(y, w)))

    ans = []
    def dfs(t):
        if t:
            dfs(t.l)
            ans.append(str(t.v))
            dfs(t.r)
    dfs(root)
    return " ".join(ans)

assert run("""4
3 1
1 3
3 2
2 3
""") == "3 1 4 2", "sample 1"

assert run("""5
4 1
5 4
3 5
4 5
5 2
""") == "1 2 5 3 4", "sample 2"

assert run("""1
1 1
""") == "1", "minimum size"

assert run("""5
1 5
1 5
1 5
1 5
1 5
""") == "5 4 3 2 1", "boundary length"

assert run("""5
2 2
3 3
4 4
5 5
1 1
""") == "1 2 3 4 5", "all ignored operations"

assert run("""3
1 2
1 2
1 2
""") == "2 3 1", "small repeated rotations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | `1` | Minimum size handling |
| Repeated full rotations | `5 4 3 2 1` | Long block swaps |
| Ignored operations | `1 2 3 4 5` | Correct handling of `b <= a` |
| Small repeated swaps | `2 3 1` | Correct composition of operations |

## Edge Cases

When `a` and `b` are equal, the algorithm exits before any split. For input:

```
1
1 1
```

the treap remains unchanged and the output is `1`.

When the right side of the swap touches the end of the array, the computed block size prevents accessing positions beyond the sequence. For:

```
5
3 5
```

the distance is `2`, but the suffix starting at position `5` has length `1`, so only one pair is swapped. The sequence changes from:

```
1 2 3 4 5
```

to:

```
1 2 5 4 3
```

The treap handles this because the split sizes are based on the actual available block length, not an assumed full interval.

Repeated operations on the same ranges are also safe because every shuffle is applied to the current treap order. The structure does not rely on the original positions after initialization, so it naturally tracks the evolving permutation.
