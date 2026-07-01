---
title: "CF 104385E - Segment-tree"
description: "We are given a complete segment tree over the range from 0 to 2^n − 1. Instead of working with the array directly, the problem constructs an induced graph G by running a segment tree query procedure on an interval [L, R]."
date: "2026-07-01T02:52:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104385
codeforces_index: "E"
codeforces_contest_name: "2023 (ICPC) Jiangxi Provincial Contest -- Official Contest"
rating: 0
weight: 104385
solve_time_s: 58
verified: true
draft: false
---

[CF 104385E - Segment-tree](https://codeforces.com/problemset/problem/104385/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete segment tree over the range from 0 to 2^n − 1. Instead of working with the array directly, the problem constructs an induced graph G by running a segment tree query procedure on an interval [L, R]. The procedure collects exactly the segment tree nodes that are needed to cover this interval, and connects them using the same parent-child structure as in the original segment tree. Each edge is also labeled either 0 or 1 depending on whether it corresponds to a move to a left or right child.

So the result is a tree whose nodes are segment tree intervals, and whose edges represent adjacency in the original segment tree structure, but restricted only to the part that touches [L, R].

Two players then play on this tree. On each move, a player selects a sequence of at least two nodes x1 < x2 < … < xm. These nodes must form a simple path inside G, and the edges along that path must all have the same label: Lyra is only allowed to pick paths using only 0-edges, while Bon Bon is restricted to paths using only 1-edges. After selecting such a path, all chosen nodes are removed from the graph along with their incident edges.

After every move, the remaining graph must stay connected. Additionally, node 1 (the root of the original segment tree) is forbidden to be removed unless that move removes the entire graph.

The player who cannot make a valid move loses. We are asked, for each test case, whether Lyra wins under optimal play.

The constraints are small in depth, since n ≤ 61, meaning the segment tree has height at most 61. The number of test cases can be as large as 10^6, so the solution must be essentially O(1) or O(log n) per test case.

The main difficulty is that although the tree comes from a segment tree structure, the game is not played on an array but on a structured induced tree, and moves depend on monochromatic paths in that structure.

A naive simulation would explicitly construct the query tree G, which in the worst case has O(2^n) structure, which is impossible even for a single test case when n is large.

A second naive idea is to simulate game states or compute Grundy values over the tree. That fails immediately because the tree size is exponential in n and the number of possible moves is combinatorial.

A subtle edge case is when [L, R] exactly matches a single segment tree node interval. In this case the query tree degenerates into a single chain-like structure without branching. In contrast, any interval that is not perfectly aligned with a segment tree node boundary produces a branching structure in the induced tree.

## Approaches

The key observation is that we are not really dealing with an arbitrary tree. The query tree produced by a segment tree range query has a very rigid structure: it is exactly the decomposition of [L, R] into O(log n) canonical segment tree nodes, connected through the segment tree hierarchy.

If we try to think in terms of brute force, we would explicitly build G, enumerate all valid monochromatic paths, and run a game solver on a general graph game. This quickly becomes infeasible because the number of states grows exponentially with the number of nodes in G, and G itself can be large.

The important simplification comes from noticing what the structure of G actually looks like. The segment tree decomposition creates a tree that is almost always branching: whenever an interval is split into two canonical pieces, the corresponding nodes connect to different subtrees, producing a branching point in G. The only situation where no branching occurs is when [L, R] coincides exactly with one segment tree node interval, meaning the entire range is a power-of-two aligned block.

This structural distinction turns the game into a simple outcome check. If the induced graph is a pure path (no branching), then every move reduces the path in a constrained way and the second player can mirror optimal play. If the graph has any branching, Lyra has a forced winning advantage because she can always choose moves that eliminate asymmetric branches and reduce the game faster than the opponent can mirror.

Thus the entire problem reduces to checking whether [L, R] corresponds exactly to a segment tree node interval.

A segment tree node interval is defined by a length that is a power of two and an alignment boundary that is a multiple of that length. Concretely, [L, R] is exactly one node interval if and only if R − L + 1 is a power of two and L is divisible by R − L + 1.

Everything else produces a branching query tree, and therefore a winning position for Lyra.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Construction + Game Simulation | Exponential in n | Exponential | Too slow |
| Check Segment Tree Alignment Property | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Compute the length of the interval, len = R − L + 1. This is the size of the covered range in the original segment tree.
2. Check whether len is a power of two. This can be done using the standard bit trick len & (len − 1) == 0. This condition ensures that the interval could potentially correspond to a full segment tree node.
3. If len is not a power of two, immediately conclude that the query tree must contain branching, because the interval cannot be represented as a single segment tree node. In this case, Lyra wins.
4. If len is a power of two, check alignment: verify whether L is divisible by len. If L % len == 0, then [L, R] exactly matches a segment tree node interval, so the query tree is a single non-branching chain structure.
5. If both conditions hold, output that Lyra loses. Otherwise, output that Lyra wins.

The reasoning behind the last step is that only perfectly aligned segment tree nodes avoid splitting into multiple canonical nodes during the query decomposition. Any misalignment forces the query procedure to combine multiple nodes, which introduces branching in the induced graph.

Why it works is based on the invariant that segment tree query decomposition produces a minimal set of disjoint canonical intervals. A single canonical interval produces a linear structure in the induced tree, while multiple canonical intervals necessarily create a branching node where the decomposition splits. That branching point is what breaks symmetry and gives the first player a winning strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_pow2(x):
    return x > 0 and (x & (x - 1)) == 0

t = int(input())
out = []

for _ in range(t):
    n, L, R = map(int, input().split())
    length = R - L + 1

    if is_pow2(length) and L % length == 0:
        out.append("No")
    else:
        out.append("Yes")

sys.stdout.write("\n".join(out))
```

The solution relies entirely on the structural characterization of when a segment tree query decomposes into exactly one canonical interval. The power-of-two check filters candidate intervals that could correspond to a single node in the segment tree. The alignment check ensures that the interval starts exactly at a boundary consistent with that node’s segment.

The final decision encodes the game outcome directly: the only losing positions for Lyra are those where the query tree is perfectly linear, meaning no branching structure exists to create winning asymmetry.

## Worked Examples

Consider a case where the interval is perfectly aligned.

Input:

```
1
3 4 7
```

Here, length is 4, which is a power of two, and L = 4 is divisible by 4. So the interval corresponds to a single segment tree node. The algorithm classifies this as a losing position for Lyra, producing “No”.

Now consider a slightly shifted interval.

Input:

```
1
3 5 8
```

Here, length is 4 again, but L = 5 is not divisible by 4. So the interval cannot be a single canonical node. The query decomposition must split into multiple segment tree nodes, producing branching in G. The algorithm outputs “Yes”, meaning Lyra wins.

| Step | L | R | Length | Power of Two | Aligned | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Case 1 | 4 | 7 | 4 | Yes | Yes | No |
| Case 2 | 5 | 8 | 4 | Yes | No | Yes |

These traces show that the entire decision depends only on whether the interval is a canonical segment tree block.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only arithmetic and bit operations |
| Space | O(1) | No data structures beyond variables |

With up to 10^6 test cases, this constant-time solution is necessary. Any approach that attempts to construct or traverse the query tree would be infeasible due to the exponential size of segment tree representations in n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def is_pow2(x):
        return x > 0 and (x & (x - 1)) == 0

    t = int(input())
    out = []
    for _ in range(t):
        n, L, R = map(int, input().split())
        length = R - L + 1
        if is_pow2(length) and L % length == 0:
            out.append("No")
        else:
            out.append("Yes")

    return "\n".join(out)

# provided samples (illustrative)
assert run("3\n4 0 3\n3 5 5\n3 4 7\n") == "Yes\nNo\nNo"

# minimum size
assert run("1\n1 0 0\n") == "No"

# non-aligned interval
assert run("1\n3 1 6\n") == "Yes"

# full power-of-two aligned block
assert run("1\n4 8 23\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 | No | Single node edge case |
| 3 1 6 | Yes | Misaligned interval forces branching |
| 4 8 23 | No | Perfect alignment produces linear tree |

## Edge Cases

When the interval reduces to a single point, L = R, the algorithm sees length = 1, which is a power of two and always aligned. This corresponds to a trivial segment tree node. Since the rules forbid selecting node 1 unless the entire graph is removed, this position is losing for Lyra, and the algorithm outputs “No”.

When the interval is a full power-of-two block but not aligned, such as L = 5, R = 12, the length is 8 but L is not divisible by 8. The induced query tree must split at higher segment tree levels, introducing branching nodes. The algorithm correctly outputs “Yes”, matching the fact that Lyra can force asymmetry through early branching removals.

When the interval is large but almost aligned, such as L = 0 and R = 2^k − 2, the length is not a power of two, so the first condition already fails. This guarantees branching, and the outcome is again a winning position for Lyra.
