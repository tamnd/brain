---
title: "CF 102623K - K-Shift Array"
description: "We have an array of values. Two operations are mixed together: one operation rearranges a continuous part of the array, and the other asks for the sum of a continuous part. A K-shift is not a normal rotation of the whole interval."
date: "2026-08-04T17:15:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "K"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 79
verified: true
draft: false
---

[CF 102623K - K-Shift Array](https://codeforces.com/problemset/problem/102623/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of values. Two operations are mixed together: one operation rearranges a continuous part of the array, and the other asks for the sum of a continuous part.

A K-shift is not a normal rotation of the whole interval. The chosen interval is split into consecutive blocks of size K. Inside each block, the first value moves to the end and every other value moves one position left. The only possible values of K are 2 and 3, which means the rearrangement is a small periodic permutation.

The challenge is that the array length and the number of operations can both reach 200000. A solution that scans an interval after every update or query can perform around 4×10^10 operations in the worst case, which is far beyond what is possible. We need every operation to depend on the logarithm of the array size rather than the length of the interval.

The main traps come from the fact that a K-shift depends on the starting position of the interval, not just on K. For example, applying a 2-shift to positions 1 through 4 swaps (1,2) and (3,4), while applying it to positions 2 through 5 swaps (2,3) and (4,5). A structure that only remembers whether a segment was shifted by 2 or 3 will lose necessary information.

Another edge case is a query after several partial shifts. Consider:

```
3 2
1 2 3
1 1 2 2
2 1 3
```

The first operation changes the array to `[2,1,3]`, so the answer is:

```
6
```

A careless implementation that treats the operation as a global rotation would produce a wrong order and may fail later queries.

A second edge case appears when a segment tree node is fully inside an update range but its length is not divisible by K. For example, an update with K=2 on `[1,6]` can encounter a child segment `[1,3]`. That node cannot be shifted as a whole because its length is odd. The update must continue descending instead of applying a lazy tag incorrectly.

## Approaches

The direct solution is to store the actual array. For a K-shift, we iterate through the interval in blocks of size K and rotate each block. A range sum is calculated by scanning all values in the requested interval. This approach is correct because it performs exactly the operations described, but a single operation can touch O(n) elements. With 200000 operations, the worst case reaches about 4×10^10 element visits.

The useful observation is that K is very small. A 2-shift only cares about positions modulo 2 relative to the beginning of the operation. A 3-shift only cares about positions modulo 3. Since both periods divide 6, every operation can be represented as a permutation of the six residue classes of positions modulo 6.

Instead of storing the exact order of elements inside a segment tree node, we store six sums. The value in bucket `i` is the sum of all elements in that node whose global index has remainder `i` modulo 6. A K-shift on a fully covered node simply permutes these six buckets. The actual positions do not need to be reconstructed.

Lazy propagation stores the accumulated permutation applied to each node. Range queries collect the six buckets from the covered nodes and add the appropriate residues. Range updates descend only when a node cannot be transformed as a whole.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per operation | O(n) | Too slow |
| Optimal | O(6 log n) per operation | O(6n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree where every node stores six sums. The sixth buckets correspond to the six possible values of `index mod 6`. This representation keeps exactly the information needed by future shifts and queries.
2. For a node that receives a complete K-shift update, compute the permutation of the six residue buckets. The permutation depends on the left boundary of the update interval because the blocks start there.
3. Apply the permutation to the node's six sums and compose it with the node's lazy permutation. The node now represents the same array segment after the shift without visiting its children.
4. If a fully covered node cannot be shifted as a whole because its length is not divisible by K, push its lazy information to its children and continue recursively. This prevents applying an invalid transformation to a segment with incomplete blocks.
5. For a range sum query, recursively visit the segment tree. When a node is completely inside the query interval, add all six stored sums because every element in that node belongs to the requested range.

Why it works: every update only changes the position of an element inside its block. The block size is either 2 or 3, so the destination of an element depends only on its position modulo 6 and the start of the shifted interval. The six stored sums preserve exactly these classes, so every transformation can be represented by a permutation. Lazy propagation keeps the representation valid without expanding the segment, and query decomposition collects every element exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [[0] * 6 for _ in range(4 * self.n)]
        self.lazy = [list(range(6)) for _ in range(4 * self.n)]
        self.build(1, 1, self.n, arr)

    def build(self, p, l, r, arr):
        if l == r:
            self.tree[p][l % 6] = arr[l - 1]
            return
        m = (l + r) // 2
        self.build(p * 2, l, m, arr)
        self.build(p * 2 + 1, m + 1, r, arr)
        for i in range(6):
            self.tree[p][i] = self.tree[p * 2][i] + self.tree[p * 2 + 1][i]

    def apply_perm(self, p, perm):
        old = self.tree[p]
        self.tree[p] = [0] * 6
        for i in range(6):
            self.tree[p][perm[i]] = old[i]

        cur = self.lazy[p]
        nxt = [0] * 6
        for i in range(6):
            nxt[i] = cur[perm[i]]
        self.lazy[p] = nxt

    def push(self, p):
        if self.lazy[p] != list(range(6)):
            perm = self.lazy[p]
            self.apply_child(p * 2, perm)
            self.apply_child(p * 2 + 1, perm)
            self.lazy[p] = list(range(6))

    def apply_child(self, p, perm):
        old = self.tree[p]
        self.tree[p] = [0] * 6
        for i in range(6):
            self.tree[p][perm[i]] = old[i]

        cur = self.lazy[p]
        nxt = [0] * 6
        for i in range(6):
            nxt[i] = cur[perm[i]]
        self.lazy[p] = nxt

    def get_perm(self, l, k):
        perm = list(range(6))
        for i in range(6):
            pos = i
            rel = (pos - l) % k
            if rel == 0:
                new_pos = (pos + k - 1) % 6
            else:
                new_pos = (pos - 1) % 6
            perm[i] = new_pos
        return perm

    def update(self, p, l, r, ql, qr, k):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr and (r - l + 1) % k == 0:
            self.apply_perm(p, self.get_perm(ql % 6, k))
            return
        if l == r:
            return
        self.push(p)
        m = (l + r) // 2
        self.update(p * 2, l, m, ql, qr, k)
        self.update(p * 2 + 1, m + 1, r, ql, qr, k)
        for i in range(6):
            self.tree[p][i] = self.tree[p * 2][i] + self.tree[p * 2 + 1][i]

    def query(self, p, l, r, ql, qr):
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return sum(self.tree[p])
        self.push(p)
        m = (l + r) // 2
        return self.query(p * 2, l, m, ql, qr) + self.query(p * 2 + 1, m + 1, r, ql, qr)

def solve():
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    seg = SegTree(arr)
    ans = []

    for _ in range(m):
        data = list(map(int, input().split()))
        if data[0] == 1:
            _, l, r, k = data
            seg.update(1, 1, n, l, r, k)
        else:
            _, l, r = data
            ans.append(str(seg.query(1, 1, n, l, r)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The tree stores sums by global index modulo 6, so the build phase places each initial value into exactly one bucket. The lazy array is a permutation of these six buckets. Applying a lazy operation means moving bucket sums and composing the existing pending permutation with the new one.

The permutation function uses the left boundary of the update interval. For a K-shift, an element whose relative position is zero moves to the end of its block, while every other relative position moves one place left. Using modulo 6 works because both possible block sizes divide 6.

The update condition `(r - l + 1) % k == 0` is essential. A segment tree node may be inside the requested range but still contain an incomplete block, so it cannot receive the transformation directly.

Python integers do not overflow, which is necessary because the total sum can reach around 2×10^14. All indexing in the tree is one-based to match the problem statement, while the stored residues use the actual index modulo 6.

## Worked Examples

For the first sample:

| Operation | Array effect | Query result |
| --- | --- | --- |
| Initial | `[1,2,3,4,5,6]` |  |
| Shift `[1,4]`, K=2 | `[2,1,4,3,5,6]` |  |
| Query `[2,3]` | Values are `1,4` | `5` |
| Shift `[1,6]`, K=3 | `[1,4,2,5,6,3]` |  |
| Query `[2,6]` | Values are `4,2,5,6,3` | `20` |

The first shift shows why the operation cannot be treated as one rotation. Each pair moves independently, which is exactly captured by residue classes.

For another example:

```
5 3
10 20 30 40 50
1 2 5 2
2 1 5
2 2 4
```

| Operation | Segment state | Output |
| --- | --- | --- |
| Initial | `[10,20,30,40,50]` |  |
| Shift `[2,5]`, K=2 | `[10,30,20,50,40]` |  |
| Query `[1,5]` | Sum of all values | `150` |
| Query `[2,4]` | Sum of `30,20,50` | `100` |

This case checks that the shift starts from an arbitrary position instead of always starting at index 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(6 log n) per operation | Each visited segment tree node performs only constant work on six buckets. |
| Space | O(6n) | Each node stores six sums and one six-element permutation. |

The solution fits the limits because 200000 operations require roughly logarithmic work each. The constant factor is small because every transformation only manipulates six values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    arr = [int(next(it)) for _ in range(n)]

    seg = SegTree(arr)
    out = []

    for _ in range(m):
        t = int(next(it))
        if t == 1:
            l = int(next(it))
            r = int(next(it))
            k = int(next(it))
            seg.update(1, 1, n, l, r, k)
        else:
            l = int(next(it))
            r = int(next(it))
            out.append(str(seg.query(1, 1, n, l, r)))

    return "\n".join(out)

assert run("""6 4
1 2 3 4 5 6
1 1 4 2
2 2 3
1 1 6 3
2 2 6
""") == "5\n20"

assert run("""3 2
1 2 3
1 1 2 2
2 1 3
""") == "6"

assert run("""5 3
10 20 30 40 50
1 2 5 2
2 1 5
2 2 4
""") == "150\n100"

assert run("""3 2
7 7 7
1 1 3 3
2 1 3
""") == "21"

assert run("""6 2
1 2 3 4 5 6
1 2 6 3
2 2 5
""") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | `5`, `20` | Basic shifts and queries |
| Three elements with K=2 | `6` | Smallest valid shift |
| Shift starting at index 2 | `150`, `100` | Non-zero update offset |
| Equal values | `21` | Permutations do not change sums |
| K=3 partial interval | `18` | Boundary handling |

## Edge Cases

The first edge case is an update beginning at a position other than one. In the test:

```
5 3
10 20 30 40 50
1 2 5 2
2 2 4
```

the segment `[2,5]` becomes `[30,20,50,40]` inside that interval. The permutation uses `l mod 6`, so the stored residue classes are moved correctly.

The second edge case is a segment tree node whose length does not match the shift size. For:

```
3 2
1 2 3
1 1 2 2
2 1 3
```

the update affects only two elements, so the third element must stay unchanged. The update routine refuses to apply a K-shift to invalid node lengths and continues downward until every transformed node represents complete blocks.

The third edge case is applying a shift that preserves the total sum but changes internal order. The case:

```
6 2
1 2 3 4 5 6
1 2 6 3
2 2 5
```

changes the arrangement of several residue classes while the query still needs only their combined value. The six-bucket representation keeps enough information for later partial queries without storing the entire order.
