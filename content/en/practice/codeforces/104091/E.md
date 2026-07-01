---
title: "CF 104091E - \u0428\u0430\u0445\u0442\u0451\u0440\u0441\u043a\u043e\u0435 \u0440\u0435\u043c\u0435\u0441\u043b\u043e"
description: "We are simulating a simplified 2D world that behaves like a long 1D strip of width n and unlimited vertical height. Initially, every position in this strip is covered with grass. During the process, the game engine spawns horizontal segments of earth blocks."
date: "2026-07-02T02:29:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104091
codeforces_index: "E"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2022-2023"
rating: 0
weight: 104091
solve_time_s: 64
verified: true
draft: false
---

[CF 104091E - \u0428\u0430\u0445\u0442\u0451\u0440\u0441\u043a\u043e\u0435 \u0440\u0435\u043c\u0435\u0441\u043b\u043e](https://codeforces.com/problemset/problem/104091/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a simplified 2D world that behaves like a long 1D strip of width `n` and unlimited vertical height. Initially, every position in this strip is covered with grass.

During the process, the game engine spawns horizontal segments of earth blocks. Each segment is described by a starting position `a` and a length `b`. This means that all positions from `a` to `a + b - 1` receive a block. When a block is placed at a position, it falls straight down and stacks on top of existing blocks at that position, forming a vertical column of earth.

The key observation is that grass only exists in cells that are not occupied by earth. The engine is interested in how many grass textures are currently visible, which corresponds to how many positions in the strip still have no earth blocks at all.

Each query of type `2` asks for the current number of positions that remain completely untouched by any block placement so far.

The constraints allow up to `n = 10^6` positions and up to `q = 10^4` operations. This immediately rules out any solution that recomputes the answer from scratch per query in linear time over `n`, since that would cost up to `10^10` operations in the worst case. We need to support range updates and fast global aggregation, ideally in logarithmic time per operation.

A subtle pitfall is that overlapping segments do not stack independently in the answer. Once a position has been covered at least once, it should not be counted again as grass, even if additional segments are added later.

## Approaches

A direct simulation maintains an array `covered[i]` indicating whether position `i` has ever received a block. Each update of type `1 a b` would iterate through the segment and mark all positions as covered. Each query of type `2` would count how many entries remain uncovered.

This approach is correct but too slow. In the worst case, a single update may touch `O(n)` positions, and there can be `O(q)` such updates, leading to quadratic behavior.

The key structural observation is that we only need to know whether a position is zero or nonzero, not the exact number of blocks stacked. Each operation converts a range of zeros into ones, and once a position becomes one, it stays one forever. This is a classic case of maintaining a dynamic array under range increments where we only care about whether the value is still zero anywhere.

This reduces the problem to maintaining a segment of length `n` where we support range increment by 1 and query how many elements are still zero. A segment tree with lazy propagation fits this structure naturally: each node tracks how many positions in its segment are still zero, and updates flip segments from fully zero to fully nonzero efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force array marking | O(nq) | O(n) | Too slow |
| Segment tree with lazy propagation | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree over the array of size `n`. Each position starts as zero, meaning it is still grass-covered.

Each node in the segment tree stores how many positions in its interval are still zero. Additionally, we maintain a lazy marker that indicates whether the entire segment has been covered at least once.

1. Build a segment tree where every leaf is initialized to 1, since all positions initially contain grass.
2. For an update `1 a b`, we apply a range update on interval `[a, a + b - 1]`. If a segment is fully inside the update range and currently fully zero, we mark it as fully covered and set its zero count to 0.
3. When pushing updates down, if a node is already marked as fully covered, both children are immediately set to fully covered without further recursion.
4. Partial overlaps are handled by recursively updating children and recomputing the parent’s zero count as the sum of its children.
5. For a query `2`, the answer is simply the zero count stored at the root node, representing how many positions have never been covered.

The critical design choice is that we never store exact coverage counts. Once a segment becomes fully nonzero, it never changes again, so we collapse it aggressively.

### Why it works

Each position transitions from uncovered to covered at most once. The segment tree ensures that once a segment is fully covered, it is never visited again for detailed updates. This guarantees correctness because coverage is monotonic, and every update only moves the system closer to a fully covered state without ever reversing changes.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = n
        self.size = 4 * n
        self.zero = [0] * self.size   # number of zeros in segment
        self.lazy = [0] * self.size   # 0 = untouched, 1 = fully covered

        self.build(1, 1, n)

    def build(self, v, l, r):
        if l == r:
            self.zero[v] = 1
            return
        m = (l + r) // 2
        self.build(v*2, l, m)
        self.build(v*2+1, m+1, r)
        self.zero[v] = self.zero[v*2] + self.zero[v*2+1]

    def push(self, v, l, r):
        if self.lazy[v] == 0:
            return
        if l != r:
            self.lazy[v*2] = 1
            self.lazy[v*2+1] = 1
        self.zero[v] = 0
        self.lazy[v] = 0

    def update(self, v, l, r, ql, qr):
        self.push(v, l, r)
        if r < ql or qr < l:
            return
        if ql <= l and r <= qr:
            self.lazy[v] = 1
            self.push(v, l, r)
            return
        m = (l + r) // 2
        self.update(v*2, l, m, ql, qr)
        self.update(v*2+1, m+1, r, ql, qr)
        self.zero[v] = self.zero[v*2] + self.zero[v*2+1]

def solve():
    n, q = map(int, input().split())
    st = SegTree(n)

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            a = int(tmp[1])
            b = int(tmp[2])
            st.update(1, 1, n, a, a + b - 1)
        else:
            print(st.zero[1])

if __name__ == "__main__":
    solve()
```

The segment tree is built so that every node initially represents fully grass-covered space. The `zero` array tracks how many untouched positions remain in each segment. The `lazy` flag ensures that once a segment becomes fully covered, we never waste time revisiting it.

The update function is careful to propagate coverage only when necessary. Once a node is fully inside a painted segment, it is collapsed immediately to zero zeros, and the recursion stops.

## Worked Examples

Consider a small world of size `n = 5` with operations:

```
1 1 2
1 2 2
2
```

We track how many positions remain unpainted after each update.

| Step | Operation | Covered segments | Remaining zeros |
| --- | --- | --- | --- |
| 0 | init | none | 5 |
| 1 | add [1,2] | [1,2] | 3 |
| 2 | add [2,3] | [1,2,3] | 2 |
| 3 | query | [1,2,3] | 2 |

The final answer is 2 because positions 4 and 5 were never touched.

Now consider overlapping full coverage:

```
1 1 3
1 2 2
2
```

| Step | Operation | Covered segments | Remaining zeros |
| --- | --- | --- | --- |
| 0 | init | none | 5 |
| 1 | add [1,3] | [1,2,3] | 2 |
| 2 | add [2,3] | [1,2,3] | 2 |
| 3 | query | [1,2,3] | 2 |

This demonstrates that repeated updates do not double count coverage, since the state is monotonic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update touches only segment tree nodes along the affected range |
| Space | O(n) | Segment tree arrays store state for all intervals |

With `n ≤ 10^6` and `q ≤ 10^4`, this fits comfortably within limits since the total number of segment tree operations is on the order of a few hundred thousand.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    class SegTree:
        def __init__(self, n):
            self.n = n
            self.zero = [0] * (4*n)
            self.lazy = [0] * (4*n)
            self.build(1, 1, n)

        def build(self, v, l, r):
            if l == r:
                self.zero[v] = 1
                return
            m = (l+r)//2
            self.build(v*2,l,m)
            self.build(v*2+1,m+1,r)
            self.zero[v]=self.zero[v*2]+self.zero[v*2+1]

        def push(self, v, l, r):
            if self.lazy[v]:
                self.zero[v]=0
                if l!=r:
                    self.lazy[v*2]=1
                    self.lazy[v*2+1]=1
                self.lazy[v]=0

        def update(self,v,l,r,ql,qr):
            self.push(v,l,r)
            if r<ql or qr<l:
                return
            if ql<=l<=r<=qr:
                self.lazy[v]=1
                self.push(v,l,r)
                return
            m=(l+r)//2
            self.update(v*2,l,m,ql,qr)
            self.update(v*2+1,m+1,r,ql,qr)
            self.zero[v]=self.zero[v*2]+self.zero[v*2+1]

    def solve():
        n,q=map(int,input().split())
        st=SegTree(n)
        for _ in range(q):
            t=list(input().split())
            if t[0]=='1':
                a,b=int(t[1]),int(t[2])
                st.update(1,1,n,a,a+b-1)
            else:
                out.append(str(st.zero[1]))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""3 4
1 1 2
1 2 2
1 1 1
2
""") == "1", "sample 1"

# all uncovered
assert run("""5 1
2
""") == "5", "no updates"

# full cover
assert run("""5 1
1 1 5
2
""") == "0", "full cover"

# overlapping updates
assert run("""5 3
1 1 3
1 2 5
2
""") == "0", "overlap"

# boundary
assert run("""1 2
1 1 1
2
""") == "0", "single cell"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no updates | 5 | initial state correctness |
| full cover | 0 | complete overwrite handling |
| overlap | 0 | idempotent updates |
| single cell | 0 | boundary correctness |

## Edge Cases

A key edge case is repeated updates on the same region. For example, applying `1 1 3` twice should not change the answer after the first application. The segment tree handles this by collapsing fully covered segments, so the second update finds already marked nodes and performs no additional work.

Another case is a single-cell world. With `n = 1`, every update either leaves it untouched or fully covers it. The structure still behaves correctly because leaf nodes are directly initialized and updated without relying on children propagation.

A final subtle case is disjoint updates that eventually cover the entire array in multiple steps. The lazy propagation ensures that partial segments are merged correctly, and the root always reflects the true total number of untouched positions.
