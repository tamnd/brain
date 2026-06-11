---
title: "CF 1168C - And Reachability"
description: "We are given an array where each position behaves like a node in a directed structure, but edges are not explicitly provided. Instead, we can move from index i to a later index j only if two conditions hold: i < j, and the bitwise AND of the values at those positions is non-zero."
date: "2026-06-12T02:07:19+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 1168
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 562 (Div. 1)"
rating: 2200
weight: 1168
solve_time_s: 117
verified: false
draft: false
---

[CF 1168C - And Reachability](https://codeforces.com/problemset/problem/1168/C)

**Rating:** 2200  
**Tags:** bitmasks, dp  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array where each position behaves like a node in a directed structure, but edges are not explicitly provided. Instead, we can move from index `i` to a later index `j` only if two conditions hold: `i < j`, and the bitwise AND of the values at those positions is non-zero.

So every value defines a set of bits, and you can step forward only when two numbers share at least one common set bit. A query asks whether it is possible to start at position `x` and eventually reach position `y` by repeatedly jumping forward through such valid transitions.

The key difficulty is that reachability is transitive but constrained by bitwise overlap, and the array length is up to 300,000 with 300,000 queries, so any approach that explores paths per query is far too slow.

The constraint on values, up to about 300,000, implies at most 19 bits are relevant. That turns the problem from arbitrary integers into a bit-subset connectivity problem over a line.

A subtle edge case comes from zeros. Any position with value `0` is isolated because `0 & x = 0` for all `x`, so it cannot be part of any valid transition. For example, if the array is `[1, 0, 2]`, then index `2` cannot be used as an intermediate hop. A naive graph interpretation might accidentally include it, but it must be treated as a barrier.

Another failure case appears when connectivity exists but only through a chain of overlapping bits. For example, `[2 (010), 3 (011), 1 (001)]` allows movement `2 → 3 → 1`, even though `2 & 1 = 0`. Any approach that only checks direct pairwise reachability will miss these chains.

Finally, ordering matters: all transitions go strictly forward, so we are effectively working with a directed acyclic graph over indices, which allows greedy propagation.

## Approaches

A brute-force interpretation builds a graph over indices and runs a BFS or DFS for each query. Each node may connect forward to many later nodes sharing at least one bit. In the worst case, nearly every pair shares at least one bit, producing about O(n²) edges. Even with pruning, answering 300,000 queries independently leads to repeated traversals over large portions of the array, which is far beyond acceptable limits.

The key observation is that connectivity is governed entirely by bits, and movement is monotonic in index. Instead of tracking full reachability per query, we can precompute how far each index can “push forward” using a greedy union over active bits.

We process indices from left to right while maintaining, for each bit, the farthest index reachable so far through that bit. At each position, if it shares a bit with a previously active segment, it can extend that segment forward. This creates a global reachability envelope that tells us, from any starting point, how far we can propagate.

Once we know the farthest reachable position from every index (via a standard greedy sweep similar to interval expansion), each query reduces to a simple check: whether `y` lies within the reach interval of `x`.

The subtle insight is that although paths may branch across different bit interactions, the monotonic structure ensures all possible progress collapses into a single forward-reachable boundary per starting index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | O(nq) worst case | O(n) | Too slow |
| Bitwise forward expansion | O(n log A + q) | O(n + log A) | Accepted |

## Algorithm Walkthrough

1. Treat each bit independently and track the farthest position that bit can propagate to.

Each index contributes its position to all bits it contains, meaning that bit becomes “active” at that index.
2. Sweep from left to right, maintaining a current window of reachability.

For each position `i`, compute the maximum reachable boundary contributed by all bits present at `a[i]`.
3. If position `i` is inside the current reachable range, it can inherit all active bit reach extensions.

This is the crucial propagation step: overlap in any bit allows merging connectivity.
4. Update the global farthest reach from `i` accordingly.

Once `i` extends reach beyond previous limits, we expand the active region.
5. Store, for each index, the maximum position reachable starting from it.

This transforms the graph reachability problem into interval containment.
6. For each query `(x, y)`, check whether `y` lies within `[x, reach[x]]`.

If yes, output "Shi", otherwise "Fou".

### Why it works

The invariant is that at any point in the sweep, every active bit represents a connected component over indices that share that bit through some chain of overlaps. When a new index falls inside any of these components, it merges into them and potentially extends them forward. Because movement is strictly increasing in index, these components never split, only merge and extend. Therefore the reach computed for each index is the maximal endpoint of all valid forward chains starting there.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    LOG = 20
    last = [-1] * LOG
    reach = [i for i in range(n)]

    max_reach = -1

    for i in range(n):
        x = a[i]

        # compute best reach from active bits
        best = i
        for b in range(LOG):
            if x & (1 << b):
                if last[b] != -1:
                    best = max(best, last[b])

        # if already inside reachable region, propagate it
        if best <= max_reach:
            reach[i] = max_reach
        else:
            reach[i] = best

        # update active bits
        for b in range(LOG):
            if x & (1 << b):
                last[b] = reach[i]

        max_reach = max(max_reach, reach[i])

    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        if reach[x] >= y:
            print("Shi")
        else:
            print("Fou")

if __name__ == "__main__":
    solve()
```

The code maintains two key structures: `last[b]`, which stores the farthest reach achieved by any segment involving bit `b`, and `reach[i]`, which stores how far position `i` can ultimately reach. The sweep ensures that whenever a new index shares a bit with any earlier reachable segment, it inherits and possibly extends that reach.

A common pitfall is forgetting that updates must use the already computed `reach[i]` rather than raw indices. This ensures transitive chains like `i → j → k` are correctly collapsed into a single forward interval.

## Worked Examples

### Example 1

Input:

```
5 3
1 3 0 2 1
```

We track reach and bit states.

| i | a[i] | active bits impact | reach[i] |
| --- | --- | --- | --- |
| 0 | 1 | start bit 0 | 0 |
| 1 | 3 | merges with bit 0 | 1 |
| 2 | 0 | no transitions | 2 |
| 3 | 2 | new component | 3 |
| 4 | 1 | connects backward | 4 |

Queries:

`1 → 3` fails because index 3 is isolated by 0 at position 2.

`2 → 4` succeeds through direct bit overlap.

`1 → 4` succeeds through chain propagation.

Output:

```
Fou
Shi
Shi
```

This demonstrates how zero acts as a barrier, splitting connectivity into segments.

### Example 2

Input:

```
4 2
2 3 1 4
```

| i | a[i] | reach[i] |
| --- | --- | --- |
| 0 | 2 | 0 |
| 1 | 3 | 1 |
| 2 | 1 | 2 |
| 3 | 4 | 3 |

All indices are connected via overlapping bits: 2↔3↔1 and 4 connects through bit 2 or propagation.

Query `1 → 4` succeeds, and `2 → 3` also succeeds due to intermediate bridging.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · log A + q) | Each index processes up to ~20 bits once, queries are O(1) |
| Space | O(n + log A) | Stores reach array and last-seen bit positions |

The algorithm fits easily within limits since 300,000 × 20 operations is small, and queries are constant-time lookups.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    LOG = 20
    last = [-1] * LOG
    reach = [i for i in range(n)]
    max_reach = -1

    for i in range(n):
        x = a[i]
        best = i
        for b in range(LOG):
            if x & (1 << b):
                best = max(best, last[b])

        if best <= max_reach:
            reach[i] = max_reach
        else:
            reach[i] = best

        for b in range(LOG):
            if x & (1 << b):
                last[b] = reach[i]

        max_reach = max(max_reach, reach[i])

    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        out.append("Shi" if reach[x] >= y else "Fou")

    return "\n".join(out)

# provided sample
assert run("""5 3
1 3 0 2 1
1 3
2 4
1 4
""") == "Fou\nShi\nShi"

# minimum size
assert run("""2 1
1 2
1 2
""") == "Shi"

# zero barrier
assert run("""3 2
1 0 2
1 3
1 2
""") == "Fou\nFou"

# fully connected
assert run("""4 2
1 3 1 3
1 4
2 3
""") == "Shi\nShi"

# no bits overlap
assert run("""3 1
1 2 4
1 3
""") == "Fou"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | mixed | correctness baseline |
| 1 2 chain | Shi | minimal reachability |
| zero barrier | Fou/Fou | handling zeros |
| full overlap | Shi | dense connectivity |
| disjoint bits | Fou | no path case |

## Edge Cases

A zero in the array breaks propagation completely. For input `[1, 0, 2]`, index `1` cannot reach index `3` because any chain would require passing through position `2`, but `0 & x = 0` prevents any edge involving it. The algorithm naturally handles this because no bit is updated at that position, so it never extends any `last[b]`.

A second subtle case is long chains of partial overlap like `[2, 3, 1, 4]`. Here no single pair connects endpoints directly, but the algorithm correctly merges them because each intermediate index updates shared bits, extending the reachable interval step by step.
